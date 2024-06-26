import pandas as pd
import numpy as np
from tqdm import tqdm
import uuid

class FirstFitDecreasing:
    def __init__(self, bin_types, route_restrictions, global_restrictions):
        self.bin_types = bin_types
        self.route_restrictions = route_restrictions
        self.global_restrictions = global_restrictions
        self.leftovers = pd.DataFrame()

    def perform(self, df):
        # Preprocess the DataFrame
        preprocessed_df = self.preprocess(df)

        # Perform the First Fit Decreasing algorithm
        bins = self.functional_ffd(preprocessed_df)

        print(f'Total leftover items: {self.leftovers.shape[0]}')
        print(f'Total packed items: {preprocessed_df.shape[0] - self.leftovers.shape[0]}')
        print(f'Total bins used: {len(bins)}')

        # Postprocess the results
        processed_results = self.postprocess_results(preprocessed_df, bins)

        return processed_results

    def preprocess(self, df):
        df.columns = df.columns.str.replace(' ', '_')

        # Include uuid column
        df['uuid'] = df['Cor'].apply(lambda x: str(uuid.uuid4()))

        # Include total volume and weight columns
        df['Volume_total'] = df['Volume_unit'] * df['Peças']
        df['Peso_total'] = df['Peso_unit'] * df['Peças']

        cx_item_lim = self.global_restrictions["cx_item_lim"]
        en_item_lim = self.global_restrictions["en_item_lim"]

        # Sort by date
        df = df.sort_values(by=['Data_da_ordem_de_produção'], ascending=True)
        
        cx_df = df[df["Tipo_de_buffer"] == "CX"].copy()
        en_df = df[df["Tipo_de_buffer"] == "EN"].copy()

        # Count the cumulative sum of items for each buffer type
        cx_df['cumsum'] = cx_df.groupby('Tipo_de_buffer').cumcount()
        en_df['cumsum'] = en_df.groupby('Tipo_de_buffer').cumcount()

        # Take first 120000 items for CX and 100000 items for EN, storing the leftovers in self.leftovers
        cx_df = cx_df[cx_df['cumsum'] < cx_item_lim]
        en_df = en_df[en_df['cumsum'] < en_item_lim]
        self.leftovers = pd.concat([self.leftovers, cx_df[cx_df['cumsum'] >= cx_item_lim], en_df[en_df['cumsum'] >= en_item_lim]])

        parsed_df = pd.concat([cx_df, en_df])
        parsed_df = parsed_df.drop(columns=['cumsum'])

        # Check if there is any item_loja (in any combination of these words) column in the DataFrame
        if 'item_loja' not in parsed_df.columns.str.lower():
            parsed_df = self.add_item_loja_column(parsed_df)
        
        return parsed_df

    def add_item_loja_column(self, df):
        # Group by 'Loja' and 'Produto' and use cumcount to assign a sequential number starting from 1
        df['item_loja'] = df.groupby(['Loja']).cumcount() + 1
        return df

    def postprocess_results(self, input_df, results_df):
        # Initialize a list to store the rows for the final DataFrame
        rows = []

        # Iterate over the bins to extract item information
        for bin_index, bin in enumerate(results_df):
            for item_uuid in bin['Items']:
                item = input_df[input_df['uuid'] == item_uuid].copy()
                if not item.empty:
                    item['Bin'] = bin_index  # Add the bin index
                    item['Amt_in_bin'] = item['Peças']  # Add the amount in the bin
                    rows.append(item.to_dict(orient='records')[0])  # Convert the item to a dictionary and append

        # Create a DataFrame from the rows
        processed_results = pd.DataFrame(rows)

        return processed_results


    def functional_ffd(self, df):
        # Sort items in decreasing order of volume and increasing order of date (FIFO)
        df_sorted = df.copy()
        df_sorted['Inv_Volume_total'] = (1 / df_sorted['Volume_total']).replace(np.inf, 0)
        df_sorted = df_sorted.sort_values(by=['Data_da_ordem_de_produção', 'Inv_Volume_total', 'pai_cor'], ascending=True)
        
        # Initialize bins list
        bins = []
        leftover_items = pd.DataFrame(columns=df_sorted.columns)  # Initialize leftover items DataFrame
        
        items_to_drop = []
        df_sorted = df_sorted.reset_index(drop=True)
        items_to_add = []

        runs = 0

        while len(df_sorted) != 0:
            df_sorted = df_sorted[~df_sorted['uuid'].isin(items_to_drop)]

            # Add needed items to df_sorted
            if len(items_to_add) != 0:
                df_sorted = pd.concat([df_sorted, pd.DataFrame(items_to_add)])
            items_to_add = []
            items_to_drop = []
            
            # Make a copy of the sorted DataFrame
            df_sorted_copy = df_sorted.copy()
            
            # Iterate over items in the copy of the sorted DataFrame
            # for index, item in tqdm(df_sorted_copy.iterrows(), desc=f'Run {runs}', total=len(df_sorted_copy)):
            for index, item in df_sorted_copy.iterrows():
                runs += 1
                # Flag to check if the item is placed
                placed = False
                
                # Try to place the item in existing bins
                for bin in bins:
                    if (bin['Volume'] + item['Volume_total']) <= bin["vol_limit"] \
                        and (bin['Peso_total'] + item['Peso_total']) <= 23 \
                        and bin['Amt.Items'] + item['Peças'] <= bin["item_limit"] \
                        and item["Loja"] == bin["Loja"] \
                        and item["Rota"] == bin["Rota"] \
                        and item["Tipo_de_buffer"] == bin["Buffer"] \
                        and item["Classe_de_onda"] == bin["Wave"]:
                        
                        bin['Items'].append(item['uuid'])
                        bin['Volume'] += item['Volume_total']
                        bin['Peso_total'] += item['Peso_total']
                        bin['Amt.Items'] += item['Peças']

                        # Remove the item from the original DataFrame
                        items_to_drop.append(item['uuid'])
                        placed = True
                        break
                
                # If the item couldn't be placed entirely, reduce it by "inner" means until it fits into a bin
                while not placed and item['Peças'] > item['Inner']:
                    # Reduce the item to its inner size
                    detached_portion = item.copy()
                    detached_portion['Peças'] = item['Inner']
                    detached_portion['Volume_total'] = item['Volume_unit'] * item['Inner']
                    detached_portion['Peso_total'] = item['Peso_unit'] * item['Inner']
                    
                    # Update the remaining portion of the item
                    item['Peças'] -= item['Inner']
                    item['Volume_total'] -= item['Volume_unit'] * item['Inner']
                    item['Peso_total'] -= item['Peso_unit'] * item['Inner']
                    
                    # Concatenate the reduced portion back to the original DataFrame
                    items_to_add.append(detached_portion)
                    
                    # Try to place the reduced item in existing bins
                    for bin in bins:
                        if (bin['Volume'] + item['Volume_total']) <= bin["vol_limit"] \
                            and (bin['Peso_total'] + item['Peso_total']) <= 23 \
                            and bin['Amt.Items'] + item['Peças'] <= bin["item_limit"] \
                            and item["Loja"] == bin["Loja"] \
                            and item["Rota"] == bin["Rota"] \
                            and item["Tipo_de_buffer"] == bin["Buffer"] \
                            and item["Classe_de_onda"] == bin["Wave"]:
                            
                            bin['Items'].append(item['uuid'])
                            bin['Volume'] += item['Volume_total']
                            bin['Peso_total'] += item['Peso_total']
                            bin['Amt.Items'] += item['Peças']

                            items_to_drop.append(item['uuid'])
                            placed = True
                            break
                
                # If the item still couldn't be placed, create a new bin
                if not placed:
                    # Check if creating a new bin exceeds route capacity
                    if len([bin for bin in bins if bin['Rota'] == item["Rota"]]) >= self.route_restrictions[self.route_restrictions["Rota"] == item["Rota"]]["Capacidade"].values[0]:
                        leftover_items = leftover_items.append(item)  # Add item to leftover items DataFrame
                    else:
                        bins.append({
                            'Items': [item['uuid']],
                            'Volume': item['Volume_total'],
                            'Peso_total': item['Peso_total'],
                            'Amt.Items': item['Peças'],
                            "Loja": item["Loja"],
                            "Rota": item["Rota"],
                            "Buffer": item["Tipo_de_buffer"],
                            "Wave": item["Classe_de_onda"],
                            "vol_limit": self.bin_types[self.bin_types["Tipo_de_buffer"] == item["Tipo_de_buffer"]]["volume_util_caixa"].values[0],
                            "item_limit": self.bin_types[self.bin_types["Tipo_de_buffer"] == item["Tipo_de_buffer"]]["Peças_max"].values[0]
                        })
                        items_to_drop.append(item['uuid'])
                        placed = True
                        break
        
        self.leftovers = pd.concat([self.leftovers, leftover_items])
        
        return bins
