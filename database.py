import pandas as pd

# Lendo o arquivo de e-mails de fornecedores
df_emails = pd.read_excel('dados/fornecedores.xlsx')

df_cobrados = pd.read_excel('dados/pedidos_cobrados.xlsx')

# Lendo o arquivo de pedidos
df = pd.read_excel('dados/pedidos.xlsx')

# Formatando as colunas de data no formato datetime
df['Data Entrega'] = pd.to_datetime(df['Data Entrega'], dayfirst=True, errors='coerce')
df['Data Pedido'] = pd.to_datetime(df['Data Pedido'], dayfirst=True, errors='coerce')

# Formatando a coluna de "Valor Total"
df['Valor Total'] = df['Valor Total'].apply(lambda x: f"R$ {x:,.2f}".replace(",","X").replace(".",",").replace(",","."))

# Calculando atrasos de entrega
df['Dias para Entrega'] = (df['Data Entrega'] - pd.Timestamp.today().normalize()).dt.days

# Criando a coluna "Status" e calculando se os pedidos estão atrasados
df.insert(0, 'Status', None)
df['Status'] = df['Dias para Entrega'].apply(lambda x: "ATRASADO" if x <=0 else "DENTRO DO PRAZO")

# Criando a coluna "Cobrado" e calculando se o fornecedor foi cobrado ou não
df.insert(7, "Cobrado", "NÃO COBRADO")
df.loc[df['Pedido'].isin(df_cobrados['Pedido']), 'Cobrado'] = "COBRADO"

# Formatação final da base de dados
df = df.drop(columns=['Dias para Entrega'])