# See if this script is being executed from 03-Source directory
# If not, raise exception and stop execution
if __name__ == "__main__":
    import os
    if os.getcwd().split("/")[-1] != "03-Source":
        raise Exception("This script should be executed from 03-Source directory!")
    from ffd import FirstFitDecreasing
    import pandas as pd

    # Load the datastet from our standard data dir
    df_bak = pd.read_excel('../01-Data/ordens_pre_process_revisado.xlsx')

    # Load requirements from our standard data dir
    df_caixas_tipo = pd.read_excel('../01-Data/Dados - desafio disciplina RPVMM.xlsx', sheet_name='Tipos de caixa')
    df_caixas_tipo.columns = df_caixas_tipo.columns.str.replace(' ', '_')
    df_caixas_tipo['volume_util_caixa'] = df_caixas_tipo['Comprimento'] * df_caixas_tipo['Largura'] * df_caixas_tipo['Altura'] * df_caixas_tipo['Fator_de_ocupação']
    
    route_restrictions = df_bak[['Rota', 'Capacidade']].drop_duplicates()

    # Drop all unnamed columns
    df = df_bak.loc[:, ~df_bak.columns.str.contains('^Unnamed')]
    df = df.query("chave_loja_buffer_onda in ('2_EN_3', '10_CX_1', '31_EN_3', '33_EN_3', '3_CX_9')")

    print(f'Original dataset shape: {df.shape}')


    # Create an instance of the FirstFitDecreasing class
    ffd = FirstFitDecreasing(df_caixas_tipo, route_restrictions, {"cx_item_lim": 120000, "en_item_lim": 100000})

    # Perform the First Fit Decreasing algorithm
    packed_bins = ffd.perform(df)

    print(packed_bins.head())

    print(f'Total leftover items: {ffd.leftovers.shape[0]}')


