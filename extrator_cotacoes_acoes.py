import argparse
from tqdm import tqdm
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import pandas as pd
from datetime import datetime
from io import StringIO  # Adicionar a importação para StringIO

# Versão do programa
VERSION = ['1.0.1']

# Options
parser = argparse.ArgumentParser(description='Extrator de dados de Cotações de tickers a partir do fundamentus.com.br.')
parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {VERSION}')
parser.add_argument('-o', '--output', help='Especifique o nome de saída do seu arquivo. O Default é fundamentus_tickers.csv.', default='fundsexplorer_ranking.csv')
args = parser.parse_args()

print(f'Started in:   {datetime.now().strftime("%B %d, %Y %H:%M:%S")}\n')
start_time = datetime.now()

# Função para configurar e instalar o driver
def setUpdate():
    try:
        driver_path = ChromeDriverManager().install()  # Instala o WebDriver atualizado
        return driver_path
    except Exception as e:
        print(f'Error Install: {e}')
        return None

# Status bar
progress_bar = tqdm(total=6, bar_format='{l_bar}{bar}| {percentage:3.0f}% ')

# Inicialize o driver do Selenium
driver_path = setUpdate()

if not driver_path:
    print("Erro ao instalar o WebDriver. Verifique sua conexão ou permissões.")
    exit(1)

progress_bar.update(1)  # Update

# Configurações de opções do Chrome
options = Options()
options.add_argument("--lang=en")
options.add_argument('--headless')
options.add_argument("--incognito")

# Inicialize o ChromeDriver com as opções e serviço configurados
serv = Service(driver_path)
driver = webdriver.Chrome(service=serv, options=options)

progress_bar.update(1)  # Update

# URL alvo
url = "https://www.fundamentus.com.br/resultado.php"

# Navegue até a página
driver.get(url)

progress_bar.update(1)  # Update

# Espere até que a tabela esteja carregada (pode ser necessário ajustar o tempo)
driver.implicitly_wait(10)

# Extraia a tabela
table = driver.find_element(By.CSS_SELECTOR, '.resultado.rowstyle-par.colstyle-col.no-arrow')

progress_bar.update(1)  # Update

# Usar StringIO para evitar o FutureWarning
table_html = table.get_attribute('outerHTML')
tickers = pd.read_html(StringIO(table_html), encoding='utf-8', decimal=".", thousands='.')[0]

# Feche o driver
driver.quit()

progress_bar.update(1)  # Update

tickers = tickers.dropna(axis=1, how='all')  # Remove colunas vazias

progress_bar.update(1)  # Update

# Salve o DataFrame em um arquivo CSV
tickers.to_csv(args.output, index=False, decimal='.')

progress_bar.update(1)  # Update

progress_bar.close()  # close

print(f'\nTotal time:    {str(datetime.now() - start_time).split(".")[0]}')
print(f'Finished at:   {datetime.now().strftime("%B %d, %Y %H:%M:%S")}\n')
