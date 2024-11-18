from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
import re

class WhatsApp():

    def __init__(self):

        self.driver = webdriver.Chrome(options=self.chrome_options())
        self.actions = ActionChains(self.driver)
        self.start()
        self.search_box = WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@role="textbox"]')))
        #self.get_recent_chats()
    
    def start(self):
        self.driver.get('https://web.whatsapp.com/')
        messages_loaded = False
        last_status = None; tentativas = 0
        while messages_loaded != True:
            try:
                if tentativas == 0:
                    status_div = WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[3]')))
                else:
                    status_div = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[2]/div[3]')))
                tentativas += 1

                if status_div.text != last_status:
                    last_status = status_div.text
                    print(last_status)
                if "100%" in status_div.text:
                    messages_loaded = True
            except Exception as error:
                if last_status: # Se erro ao pesquisar a barra de progresso, porém há last_status, portanto carregou.
                    print("Sessão iniciada")
                    messages_loaded = True
                else:
                    print("Erro ao iniciar sessão:", error)
            


    
    def chrome_options(self):

        # Configurações do ChromeDriver
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", False)
        chrome_options.add_argument("user-data-dir=C:/Users/jpbpi/AppData/Local/Google/Chrome/User Data")
        chrome_options.add_argument("profile-directory=Default")
        # chrome_options.add_argument("--disable-dev-shm-usage")  # Corrige problemas de memória compartilhada
        # chrome_options.add_argument("--no-sandbox")  # Executa o Chrome fora do modo sandbox
        # chrome_options.add_argument("--remote-debugging-port=9222")  # Porta de depuração

        return chrome_options
    
    def exit(self):
        self.driver.close()
    
    def search(self,search):
        self.search_box.send_keys(Keys.CONTROL + "a")  # Seleciona todo o texto (use Keys.COMMAND + "a" no macOS)
        self.search_box.send_keys(Keys.BACKSPACE)
        self.search_box.send_keys(search)
        self.search_box.send_keys(Keys.RETURN)

    def write_message(self,message):
        try:
            self.message_box = WebDriverWait(self.driver, 15).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@role="textbox"]')))[1]
            self.message_box.send_keys(Keys.CONTROL + "a")  # Seleciona todo o texto (use Keys.COMMAND + "a" no macOS)
            self.message_box.send_keys(Keys.BACKSPACE)
            self.message_box.send_keys(message)
            self.message_box.send_keys(Keys.RETURN)
            time.sleep(2)
        except:
            print('Erro ao enviar a mensagem')

    def send_message(self,name, message):

        self.search(name)
        #chatlist = self.read_chatlist()        
        #contact['element'].click()
        print("Mandando mensagem para:", name)
        self.write_message(message)

    def delete_last_message(self):

        chat_body = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div[3]/div/div[2]'))
        )
        chat_body_estruture = chat_body.find_elements(By.XPATH, './*')
        role_aplication = chat_body_estruture[len(chat_body_estruture) - 1]
        rows = role_aplication.find_elements(By.XPATH, './*')
        print(rows,len(rows))
        try:
            # Espera a última mensagem na conversa carregar
            ultima_mensagem_div = rows[len(rows)-1]
            ultima_mensagem = WebDriverWait(ultima_mensagem_div, 10).until(
                EC.visibility_of_element_located((By.XPATH, './/div/div/div[1]'))
            )
            
            # Move o mouse sobre a última mensagem para revelar o menu
            ActionChains(self.driver).move_to_element(ultima_mensagem).perform()

            # Encontra e clica no menu de opções da mensagem
            menu_opcoes = WebDriverWait(ultima_mensagem, 10).until(
                EC.element_to_be_clickable((By.XPATH, './/div[1]/span[2]/div/div'))
            )
            menu_opcoes.click()

            # Espera a opção de apagar aparecer e clica nela
            opcao_apagar = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/span[5]/div/ul/div/li[8]/div'))  # O texto pode variar conforme o idioma do WhatsApp Web
            )
            opcao_apagar.click()

            # Espera o botão de confirmação aparecer e clica nele
            botao_confirmar = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/span[2]/div/button[2]'))  # O texto pode variar
            )
            botao_confirmar.click()

            try:
                delele_for_everyone = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[text()="Delete for everyone"]'))  # O texto pode variar
                )
                delele_for_everyone.click()
            except:
                print("Não foi possivel deletar para todos.")
                delele_for_me = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[text()="Delete for me"]'))  # O texto pode variar
                )
                delele_for_me.click()
        
            print("Mensagem apagada com sucesso.")
        except Exception as e:
            print(f"Erro ao tentar apagar a última mensagem: {e}")
            

    def read_chatlist(self):

        elem_chatlist = WebDriverWait(self.driver, 100).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pane-side"]/div[1]/div/div')))
        elem_chatlist = elem_chatlist.find_elements(By.XPATH, './*')

        chatlist = []
        for elem_chat in elem_chatlist:
            try:
                div_nome_contato = elem_chat.find_element(By.CLASS_NAME, "_ak8q")
                nome_contato = div_nome_contato.find_element(By.XPATH, './*').get_attribute('title')

                objeto_contato = {"name": nome_contato, "element": elem_chat}
                chatlist.append(objeto_contato)
            except:
                pass

        return chatlist  
    
    def get_recent_chats(self):

        self.search('')
        recent_chats = self.read_chatlist()
        self.recent_chats = recent_chats

    def get_members_group(self, group):

        return "isso ainda não está funcionando."
        # [class="_amid"]
        self.search(group)
        chats = self.read_chatlist()
        for chat in chats:
            if group in chat['name']:
                chat['element'].click()

                header_group = self.driver.find_element(By.CLASS_NAME, '_amid')
                header_group.click()
                view_all_members = self.driver.find_elements(By.CLASS_NAME, '_alzk')[0]
                view_all_members.click()

                div_all_members = self.driver.find_element(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div/div[2]/div/div/div')

                # Role a div e capture números de telefone
                numeros = set(); ultimo_membro_anterior = None  # Variável para armazenar o último membro anterior
                while True:
                    membros_visiveis = div_all_members.find_elements(By.XPATH, './*')
                    
                    for membro in membros_visiveis:
                        ultimo_membro = membros_visiveis[-1]

                        # Verifique se o último membro mudou para evitar ficar preso no mesmo ponto
                        if ultimo_membro == ultimo_membro_anterior:
                            break  # Sai do loop se o último membro não mudar (fim da lista)

                        try:
                            # Navegue para encontrar o span com o title contendo o número de telefone
                            span = membro.find_element(By.XPATH, './/div[2]/div[2]/div[2]/span[1]/span')
                            numero = span.text
                            print(numero)
                            if numero not in numeros:
                                numeros.add(numero)
                        except:
                            # Caso o elemento não contenha um número, continue
                            continue

                    # Role até o último membro visível
                    self.actions.move_to_element(ultimo_membro).perform()
                    time.sleep(1)

                    # Role um pouco além do último membro visível
                    self.driver.execute_script("arguments[0].scrollTop += 150;", div_all_members)
                    time.sleep(2)

                    ultimo_membro_anterior = ultimo_membro

        print(numeros)

    def get_members_group_500limit(self, group):
        # [class="_amid"]
        self.search(group)
        chats = self.read_chatlist()
        for chat in chats:
            if group in chat['name']:
                chat['element'].click()

                done = False
                while done == False:
            
                    span_contatos = self.driver.find_element(By.XPATH, '//*[@id="main"]/header/div[2]/div[2]/span')
                    contatos_string = span_contatos.get_attribute('title')
                    if "," in contatos_string:
                        lista_membros = contatos_string.split(',')
                        done = True
                    else:
                        pass
                         
                # Limpa espaços em branco e retira o último elemento (ele é um 'read more')
                lista_membros = list(map(lambda x: x.strip(),lista_membros))[0:len(lista_membros)-1] 

                print(f''' Informações do grupo:
                      nome: {chat['name']}
                      elementos: {lista_membros}
                      quantidade: {len(lista_membros) }
                        ''')
                
                return lista_membros

    def get_contact_number(self, name):

        self.search(name)
        numero_telefone = None
        try:        
            header_contato = self.driver.find_element(By.XPATH, '//*[@id="main"]/header/div[2]')
            header_contato.click()
            span_nmr_telefone  = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[3]/div[5]/span/div/span/div/div/section/div[1]/div[2]/div/span/span')))
            numero_telefone = (span_nmr_telefone.text).strip()
            print("name:",name)
            print("tel:",numero_telefone)
        finally:
            if numero_telefone is None:
                return name
            else:
                return numero_telefone
    
    def mention_all_group(self,group):

        padrao = r'\d{2}\s\d{2}\s\d{5}-\d{4}'

        contato_membros = self.get_members_group_500limit(group)

        self.message_box = WebDriverWait(self.driver, 15).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@role="textbox"]')))[1]
        self.message_box.send_keys(Keys.CONTROL + "a")  # Seleciona todo o texto (use Keys.COMMAND + "a" no macOS)
        self.message_box.send_keys(Keys.BACKSPACE)
        
        for contato in contato_membros:
            if re.fullmatch(padrao, contato):
                contato = re.sub("[^0-9a-zA-Z]+",'',contato)

            self.message_box.send_keys(f"@{contato}")
            time.sleep(1)
            self.message_box.send_keys(Keys.TAB)
            time.sleep(0.5)
                

        print("grupo:",group)
        print("menções:", self.message_box.text)
        self.message_box.send_keys(Keys.ENTER)
        
        





    # search_box = driver.find_elements(By.XPATH, '//*[@contenteditable="true"]')[0]
    # assert "Python" in driver.title
    # elem = driver.find_element(By.NAME, "q")
    # elem.clear()
    # elem.send_keys("pycon")
    # elem.send_keys(Keys.RETURN)
    # assert "No results found." not in driver.page_source
    # driver.close()