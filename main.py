import re
from time import sleep
from playwright.sync_api import Playwright, sync_playwright, expect

#TODO: criar uma lógica para que ele reconheça e volte para a página correta indepentemente do ano selecionado. Atualmente está funcionando corretamente apenas nos anos 2022 e 2023.
# criar uma forma de retornar à url certa. Talvez a url deva ser construida do zero
def muda_pagina(page):

    page.get_by_role("link", name=" Próximo »").click()
    print("mudando de pagina")
    sleep(2)

def baixar_pdf(page):
    sleep(3)
    pdf_item = page.get_by_text('EDITAL').all()
    print(f'Há {len(pdf_item)} editais a serem baixados nessa página. Fazendo download')
    for p in pdf_item:
    # for p in pdf_item[-2:-1]: #retirar o comentário apenas para fins de testes
        print(f"tentando obter o link de pdf de {p}")
        p.click()
        sleep(2)
        # page.go_back() # descomentar e comentar o bloco with para fazer a navegação de páginas sem dolwnload

        with page.expect_download() as download_info:
            page.locator('xpath=//*[@id="content-core"]/p/a').click()
        download = download_info.value
        download.save_as("./"+download.suggested_filename)
        page.go_back()
        sleep(3)

    try:
        muda_pagina(page)
        baixar_pdf(page)
    except:
        page.go_back()
def percorre_itens(page):
    #percorrer cada link contido na página
    link_item = page.get_by_text('Concurso N').all()

    for link in link_item:
        link.click()
        sleep(2)
        page.get_by_text(re.compile(r"^Convocações$")).click()
        sleep(2)
        print(f'a url atual é {page.url}')
        cards_item_2 = page.locator("css=div.card").all()
        print(f"Há {len(cards_item_2)} cards nesta página. Clicando...")
        #acessando a pagina dos hospitais

        # baixar_pdfs do ano que não tiver cards
        if len(cards_item_2) < 1:
            baixar_pdf(page)
            page.goto("https://www.gov.br/ebserh/pt-br/acesso-a-informacao/agentes-publicos/concursos-e-selecoes/concursos")
        else:
        #percorre cada página dentro da página de cada hospital
            for c2 in cards_item_2:
                c2.click()
                baixar_pdf(page)
                page.goto("https://www.gov.br/ebserh/pt-br/acesso-a-informacao/agentes-publicos/concursos-e-selecoes/concursos/2023/concurso-no-01-2023-ebserh-nacional/convocacoes")
        sleep(2)
            #acessando os editais dentro de cada hospital

    page.goto("https://www.gov.br/ebserh/pt-br/acesso-a-informacao/agentes-publicos/concursos-e-selecoes/concursos")


#Loop principal
def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    global url
    url = "https://www.gov.br/ebserh/pt-br/acesso-a-informacao/agentes-publicos/concursos-e-selecoes/concursos"
    page = context.new_page()
    page.goto(url)
    page.get_by_label("Fechar overlay").click()
    lista_ano = ['2022', '2023']
    for p in lista_ano:
        page.get_by_role("link", name=p). click()
        sleep(1)
        percorre_itens(page)
        sleep(1)

    sleep(2)
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
