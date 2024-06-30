<<<<<<< Updated upstream
import pandas as pd
import numpy as np

def binsHandler(dfCaixas):
    """ pega somente as caixas que vamos utilizar e cria o campo de volume util da caixa"""
    dfCaixas.columns = dfCaixas.columns.str.replace(' ', '_')
    dfCaixas['volume_util_caixa'] = dfCaixas['Comprimento_(mm)'] * dfCaixas['Largura_(mm)'] * dfCaixas['Altura_(mm)'] * dfCaixas['Fator_de_ocupação']
    dfCaixasPadrao = dfCaixas.loc[[1, 5]]
    return dfCaixasPadrao

def backLogHandler(dfBackLog):
    """ Tratamento Coluna e Criacao de novos campos, alem da separacao das restricoes de rotas"""
    dfBackLog.columns = dfBackLog.columns.str.replace(' ', '_')
    dfBackLog["Volume_total"] = dfBackLog["Volume_unit"] * dfBackLog["Peças"]
    dfBackLog["Peso_total"] = dfBackLog["Peso_unit"] * dfBackLog["Peças"]
    dfBackLog['item_loja'] = dfBackLog.groupby(['Loja']).cumcount() + 1

    df_routes = dfBackLog[['Rota', 'Capacidade']].drop_duplicates()
    return dfBackLog, df_routes

def firstFitDecreasing(df, bin_restrictions, route_restrictions):
    # Sort items in decreasing order of volume and increasing order of date (FIFO)
    df_sorted = df.copy()
    df_sorted['Inv_Volume_total'] = (1 / df_sorted['Volume_total']).replace(np.inf, 0)
    df_sorted = df_sorted.sort_values(by=['Data_da_ordem_de_produção', 'Inv_Volume_total', 'pai_cor'], ascending=True)
    
    # Initialize bins list
    bins = []
    leftover_items = pd.DataFrame(columns=df_sorted.columns)  # Initialize leftover items DataFrame
    
    # Flag to track if a split was made
    split_made = True
    items_to_drop = []
    df_sorted = df_sorted.reset_index(drop=True)
    items_to_add = []

    while len(df_sorted) != 0:
        split_made = False
        df_sorted = df_sorted[~df_sorted.index.isin(items_to_drop)]

        # Add needed items to df_sorted
        if len(items_to_add) != 0:
            df_sorted = pd.concat([df_sorted, pd.DataFrame(items_to_add)])
        items_to_add = []
        df_sorted = df_sorted.reset_index(drop=True)
        items_to_drop = []
        
        # Make a copy of the sorted DataFrame
        df_sorted_copy = df_sorted.copy()
        
        # Iterate over items in the copy of the sorted DataFrame
        for index, item in df_sorted_copy.iterrows():
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
                    
                    bin['Items_id'].append(item['id'])
                    bin['Items_index'].append(index)
                    bin['Volume'] += item['Volume_total']
                    bin['Peso_total'] += item['Peso_total']
                    bin['Amt.Items'] += item['Peças']

                    # Remove the item from the original DataFrame
                    items_to_drop.append(index)
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
                split_made = True
                
                # Try to place the reduced item in existing bins
                for bin in bins:
                    if (bin['Volume'] + item['Volume_total']) <= bin["vol_limit"] \
                        and (bin['Peso_total'] + item['Peso_total']) <= 23 \
                        and bin['Amt.Items'] + item['Peças'] <= bin["item_limit"] \
                        and item["Loja"] == bin["Loja"] \
                        and item["Rota"] == bin["Rota"] \
                        and item["Tipo_de_buffer"] == bin["Buffer"] \
                        and item["Classe_de_onda"] == bin["Wave"]:
                        
                        bin['Items_id'].append(item['id'])
                        bin['Items_index'].append(index)
                        bin['Volume'] += item['Volume_total']
                        bin['Peso_total'] += item['Peso_total']
                        bin['Amt.Items'] += item['Peças']

                        items_to_drop.append(index) # Remove the reduced item from the original DataFrame
                        placed = True
                        break
            
            # If the item still couldn't be placed, create a new bin
            if not placed:
                # Check if creating a new bin exceeds route capacity
                if len([bin for bin in bins if bin['Rota'] == item["Rota"]]) >= route_restrictions[route_restrictions["Rota"] == item["Rota"]]["Capacidade"].values[0]:
                    leftover_items = leftover_items.append(item)  # Add item to leftover items DataFrame
                else:
                    bins.append({
                        'Items_id': [item['id']],
                        'Items_index': [index],
                        'Volume': item['Volume_total'],
                        'Peso_total': item['Peso_total'],
                        'Amt.Items': item['Peças'],
                        "Loja": item["Loja"],
                        "Rota": item["Rota"],
                        "Buffer": item["Tipo_de_buffer"],
                        "Wave": item["Classe_de_onda"],
                        "vol_limit": bin_restrictions[bin_restrictions["Tipo_de_buffer"] == item["Tipo_de_buffer"]]["volume_util_caixa"].values[0],
                        "item_limit": bin_restrictions[bin_restrictions["Tipo_de_buffer"] == item["Tipo_de_buffer"]]["Peças_max"].values[0]
                    })
                    items_to_drop.append(index)
                    placed = True
                    break
    

    return bins, leftover_items

def postProcessBins(bins, df):
    rows = []
    for bin_index, bin in enumerate(bins):
            for item_id in bin['Items_id']:
                item = df.loc[item_id].copy()
                item['Bin'] = bin_index  # Add the bin index
                item['Amt_in_bin'] = item['Peças']  # Add the amount in the bin
                item['bin_index'] = bin_index
                rows.append(item)
    # Create a DataFrame from the rows
    result_df = pd.DataFrame(rows)
    return result_df

=======
import pandas as pd
import numpy as np

def binsHandler(dfCaixas):
    """ pega somente as caixas que vamos utilizar e cria o campo de volume util da caixa"""
    dfCaixas.columns = dfCaixas.columns.str.replace(' ', '_')
    dfCaixas['volume_util_caixa'] = dfCaixas['Comprimento_(mm)'] * dfCaixas['Largura_(mm)'] * dfCaixas['Altura_(mm)'] * dfCaixas['Fator_de_ocupação']
    dfCaixasPadrao = dfCaixas.loc[[1, 5]]
    return dfCaixasPadrao

def backLogHandler(dfBackLog):
    """ Tratamento Coluna e Criacao de novos campos, alem da separacao das restricoes de rotas"""
    dfBackLog.columns = dfBackLog.columns.str.replace(' ', '_')
    dfBackLog["Volume_total"] = dfBackLog["Volume_unit"] * dfBackLog["Peças"]
    dfBackLog["Peso_total"] = dfBackLog["Peso_unit"] * dfBackLog["Peças"]
    dfBackLog['item_loja'] = dfBackLog.groupby(['Loja']).cumcount() + 1

    ## Tratamento para o inner:
    # Função para expandir as linhas
    def _expand_row(row):
        inner = row['Inner']
        if inner == 1:
            return [row]
        
        rows = []
        for i in range(inner):
            new_row = row.copy()
            new_row['id'] = f"{row['id']}_{i+1}"  # Opção para diferenciar IDs, se necessário
            new_row['Inner'] = 1
            new_row['Peças'] = row['Peças'] // inner
            new_row['Volume_total'] = row['Volume_total'] // inner
            dfBackLog["Peso_total"] = row['Peso_total'] // inner
            rows.append(new_row)
        return rows

    # Expande o DataFrame
    expanded_rows = []
    for _, row in dfBackLog.iterrows():
        expanded_rows.extend(_expand_row(row))
    # Cria um novo DataFrame com as linhas expandidas
    dfBackLog = pd.DataFrame(expanded_rows)

    ## Tratamento para a rota: 
    df_routes = dfBackLog[['Rota', 'Capacidade']].drop_duplicates()
    return dfBackLog, df_routes

def firstFitDecreasing(df, bin_restrictions, route_restrictions):
    # Sort items in decreasing order of volume and increasing order of date (FIFO)
    df_sorted = df.copy()
    df_sorted['Inv_Volume_total'] = (1 / df_sorted['Volume_total']).replace(np.inf, 0)
    df_sorted = df_sorted.sort_values(by=['Data_da_ordem_de_produção', 'Inv_Volume_total', 'pai_cor'], ascending=True)
    
    # Initialize bins list
    bins = []
    leftover_items = pd.DataFrame(columns=df_sorted.columns)  # Initialize leftover items DataFrame
    
    # Flag to track if a split was made
    items_to_drop = []
    df_sorted = df_sorted.reset_index(drop=True)
    items_to_add = []

    while len(df_sorted) != 0:
        df_sorted = df_sorted[~df_sorted.index.isin(items_to_drop)]
        # Add needed items to df_sorted
        df_sorted = df_sorted.reset_index(drop=True)
        items_to_drop = []
        
        # Make a copy of the sorted DataFrame
        df_sorted_copy = df_sorted.copy()
        
        # Iterate over items in the copy of the sorted DataFrame
        for index, item in df_sorted_copy.iterrows():
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
                    
                    item_dict = {'Item_id': item['id'], 'Pecas': item['Peças']}
                    bin['Items_info'].append(item_dict)
                    bin['Items_index'].append(index)
                    bin['Volume'] += item['Volume_total']
                    bin['Peso_total'] += item['Peso_total']
                    bin['Amt.Items'] += item['Peças']


                    # Remove the item from the original DataFrame
                    items_to_drop.append(index)
                    placed = True
                    break
            
            # If the item still couldn't be placed, create a new bin
            if not placed:
                # Check if creating a new bin exceeds route capacity mm3
                if sum([bin['Volume'] for bin in bins if bin['Rota'] == item["Rota"]]) >= route_restrictions[route_restrictions["Rota"] == item["Rota"]]["Capacidade"].values[0]:
                    leftover_items = leftover_items.append(item)  # Add item to leftover items DataFrame
                else:
                    bins.append({
                        'Items_info': [{'Item_id': item['id'], 'Pecas': item['Peças']}],
                        'Items_index': [index],
                        'Volume': item['Volume_total'],
                        'Peso_total': item['Peso_total'],
                        'Amt.Items': item['Peças'],
                        "Loja": item["Loja"],
                        "Rota": item["Rota"],
                        "Buffer": item["Tipo_de_buffer"],
                        "Wave": item["Classe_de_onda"],
                        "vol_limit": bin_restrictions[bin_restrictions["Tipo_de_buffer"] == item["Tipo_de_buffer"]]["volume_util_caixa"].values[0],
                        "item_limit": bin_restrictions[bin_restrictions["Tipo_de_buffer"] == item["Tipo_de_buffer"]]["Peças_max"].values[0]
                    })
                    items_to_drop.append(index)
                    placed = True
                    break
    

    return bins, leftover_items

def postProcessBins(bins, df):
    rows = []
    for bin_index, bin in enumerate(bins):
        for itemDict in bin['Items_info']:
            item_id = itemDict['Item_id']
            df_items = df.loc[df['id'] == item_id].copy()
            df_items['Pecas_alocadas'] = itemDict['Pecas']
            df_items['Amt_in_bin'] = bin['Amt.Items']  # Add the amount in the bin
            df_items['bin_index'] = bin_index
            rows.append(df_items)

    # Concatenate the DataFrames in rows
    result_df = pd.concat(rows, ignore_index=True)
    return result_df

>>>>>>> Stashed changes
