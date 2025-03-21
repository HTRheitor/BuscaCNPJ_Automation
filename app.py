import PySimpleGUI as sg
import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


sg.theme('reddit')

tela_login = [
    [sg.Text('Usuário')],
    [sg.Input(key='usuario')],
    [sg.Text('Senha')],
    [sg.Input(password_char='*', key='senha')],
    [sg.Text('Lista de CNPJs (um por linha):')],
    [sg.Multiline(size=(40, 5), key='cnpjs')],
    [sg.Text('Pasta Dropbox:')],
    [sg.Input(key='pasta_dropbox'), sg.FolderBrowse()],
    [sg.Button('Enviar')],
    [sg.Output(size=(43, 10))]
]

janela = sg.Window('Login', layout=tela_login)

def acessar_site_prefeitura(usuario, senha, cnpjs, pasta_dropbox):
    
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    try:
      
        driver.get("https://site_da_prefeitura.gov.br/login")
        print("Acessando site da prefeitura...")
        
        
        wait = WebDriverWait(driver, 10)
        campo_cpf = wait.until(EC.presence_of_element_located((By.ID, "cpf")))
        campo_cpf.send_keys(usuario)
        
        campo_senha = driver.find_element(By.ID, "senha")
        campo_senha.send_keys(senha)
        
        botao_login = driver.find_element(By.XPATH, "//button[contains(text(), 'Entrar')]")
        botao_login.click()
        
        print("Login realizado com sucesso!")
        time.sleep(3)
        
        
        for cnpj in cnpjs:
            cnpj = cnpj.strip()
            if not cnpj:
                continue
                
            print(f"\nProcessando CNPJ: {cnpj}")
            
         
            campo_cnpj = wait.until(EC.presence_of_element_located((By.ID, "cnpj_cliente")))
            campo_cnpj.clear()
            campo_cnpj.send_keys(cnpj)
            
            botao_acessar = driver.find_element(By.XPATH, "//button[contains(text(), 'Acessar')]")
            botao_acessar.click()
            
            print("Acessando área do cliente...")
            time.sleep(3)
            
            
            pasta_cliente = os.path.join(pasta_dropbox, f"Cliente_{cnpj}")
            if not os.path.exists(pasta_cliente):
                os.makedirs(pasta_cliente)
            
           
            menu_nf = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Notas Fiscais')]")))
            menu_nf.click()
            
            print("Acessando menu de Notas Fiscais...")
            time.sleep(2)
            
           
            botao_download_xml = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Download XML')]")))
            botao_download_xml.click()
            
            print("Baixando arquivos XML...")
            time.sleep(5)  
            
            
            mover_arquivos_recentes(os.path.join(os.path.expanduser("~"), "Downloads"), 
                                    pasta_cliente, 
                                    ".xml")
            
           
            menu_declaracao = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Declaração de Serviços')]")))
            menu_declaracao.click()
            
            print("Acessando menu de Declaração de Serviços...")
            time.sleep(2)
            
           
            botao_entregar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Entregar Declaração')]")))
            botao_entregar.click()
            
            print("Entregando declaração...")
            time.sleep(3)
            
           
            botao_recibo = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Baixar Recibo')]")))
            botao_recibo.click()
            
            print("Baixando recibo da declaração...")
            time.sleep(5) 
            
          
            mover_arquivos_recentes(os.path.join(os.path.expanduser("~"), "Downloads"), 
                                    pasta_cliente, 
                                    ".pdf")
            
            print(f"Processamento do CNPJ {cnpj} concluído!")
            
            
            botao_voltar = driver.find_element(By.XPATH, "//button[contains(text(), 'Voltar')]")
            botao_voltar.click()
            time.sleep(2)
            
        print("\nTodos os CNPJs foram processados com sucesso!")
        
    except Exception as e:
        print(f"Erro durante a execução: {str(e)}")
    finally:
        
        driver.quit()

def mover_arquivos_recentes(pasta_origem, pasta_destino, extensao, minutos=2):
    """Move arquivos recentes de uma pasta para outra"""
    import shutil
    from datetime import datetime, timedelta
    
    
    tempo_limite = datetime.now() - timedelta(minutes=minutos)
    
    
    for arquivo in os.listdir(pasta_origem):
        if arquivo.endswith(extensao):
            caminho_completo = os.path.join(pasta_origem, arquivo)
            
            
            tempo_modificacao = datetime.fromtimestamp(os.path.getmtime(caminho_completo))
            if tempo_modificacao > tempo_limite:
              
                shutil.move(caminho_completo, os.path.join(pasta_destino, arquivo))
                print(f"Arquivo {arquivo} movido para a pasta do cliente.")

while True: 
    event, values = janela.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Enviar':
        usuario_digitado = values['usuario']
        senha_digitada = values['senha']
        lista_cnpjs = values['cnpjs'].split('\n')
        pasta_dropbox = values['pasta_dropbox']
        
        if not pasta_dropbox:
            sg.popup_error("Por favor, selecione uma pasta Dropbox para salvar os arquivos.")
            continue
            
        print("Iniciando automação...")
        print(f"Total de CNPJs a processar: {len([cnpj for cnpj in lista_cnpjs if cnpj.strip()])}")
        
        acessar_site_prefeitura(usuario_digitado, senha_digitada, lista_cnpjs, pasta_dropbox)

janela.close()