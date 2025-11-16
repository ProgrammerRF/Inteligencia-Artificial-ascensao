#!/user/bin/env python3 # O comando env procura a localização do interpretador no dispositivo
#-*-coding:utf-8-*- # Define a codificação UTF-8. opcional no python3
#qpy:3 # Define o uso do python3
#qpy:kivy # Define o uso do kivy para criar interface gráfica

# Versão Mobile

# Metadados
__Author__ = "Rafael Moraes De Oliveira"
__Date__ = "Sábado (08/03/2025)"

#Importa modulos necessários
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.button import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
import os
import requests
import socket
import time
from firebase import firebase
from kivy.core.window import Window
from texto import fala, parar_audio
from kivy.animation import Animation
from kivy.clock import Clock

import threading 
#Carrega as variaveis do .env
from dotenv import load_dotenv

# Carrega o conteudo do arquivo .dotenv para as variaveis de sistema
load_dotenv() # Procura o comando .env e carrega suas variaveis no sistema

# Sua chave da API Together
API_KEY = os.getenv('API_KEY') 
API_URL = os.getenv('API_URL')

#Integração com o firebase
firebase_app = firebase.FirebaseApplication("https://inteligencia-artificial-37d91-default-rtdb.firebaseio.com/",None)

"""
A lista user_name inicia vazia, porém conforme o usuario interage com o aplicativo armazena o nome do usuario que é fornecido após uma consulta no firebase através do email quando o usuario faz login ou se cadastra.

A lista photo_profile tambem inicializa vazia, porém quando o usuario faz login a lista armazena o numero e o tipo da foto que está registrada no firebase.

E a lista user_email tambem inicializa vazia, porém quando o usuario faz login ou se cadastra armazena o email do usuario.

essas listas tem o objetivo de manter os dados persistentes no app sem ter que fazer excessivas consultas no banco de dados.
"""

user_name = [] # Essa lista global armazena o nome do usuario
photo_profile = [] # Essa lista armazena o numerovda foto selecionada pelo usuario
user_email = [] # Essa lista contem o email do usuario
historico_nome = [] # Essa lista contem a pergunta feita pelo usuario
historico_conteudo = [] # Essa lista contem a resposta da IA
ativar = True # Essa lista contem a decisão do usuario referente a voz da IA
contador = 0

class Menu(Screen):	
    def __init__(self,password=0,**kwargs):
        # Metodo construtor que inicializa a tels e repassa os parametros adicionados para a superclasse 
        super().__init__(**kwargs)
        self.password = 0 
        
        # Essa função carrega novamente os parametros da classe Screen e mantem os parametros adicionados

    def on_pre_enter(self):
        global ativar
        """Assim que o usuario inicializa o programa a tecla voltar do android recebe a funcionalidade de apresentar um popup antes de encerrar o app perguntando se o usuario quer realmente fechar o programa"""
        Window.bind(on_keyboard=self.tecla_voltar)
        parar_audio(3)
        fala(3,'Olá, para acessar a plataforma faça login.','Audios/resposta_ia.mp3',ativar)
        
        if ativar == True:
        	self.ids['icone_audio'].source = 'fotos/desativar_audio.png'
        else:
        	self.ids['icone_audio'].source = 'fotos/ativar_audio.png'
        

    def tecla_voltar(self,window,key,*args):
        """ 27 é o numero correspondente a tecla voltar do android. quando o usuario pressiona essa tecla chama a função sair que abre um Popup perguntando se o usuario realmente quer sair.
        """
        if key == 27: # Se o usuario pressionar o botão de voltar no android ou a tecla ESC no computador o PopUp é chamado
        	self.sair()
        	return True
       
    def sair(self):
        float = FloatLayout()
        titulo = Label(text='Você quer realmente sair?',pos_hint={'right':0.70,'top':1},font_size=(45),size_hint=(0.40,0.30),color=(0,1,0,1))
        bt1 = Button(text='Sim',pos_hint={'right':0.42,'top':0.6},size_hint=(0.40,0.30),background_color=(0,0,0,0))
        bt1.bind(on_press=self.saida)
        
        bt1_image = Image(source='fotos/Botao.png',pos_hint={'right':0.42,'top':0.6},size_hint=(0.40,0.30))
        
        bt2 = Button(text='Não',pos_hint={'right':0.95,'top':0.6},size_hint=(0.40,0.30),background_color=(0,0,0,0))
        bt2.bind(on_press=self.dispensar)
        
        bt2_image = Image(source='fotos/Botao.png',pos_hint={'right':0.95,'top':0.6},size_hint=(0.40,0.30))
        
        float.add_widget(titulo)
        
        float.add_widget(bt1_image)
        float.add_widget(bt1)
        
        float.add_widget(bt2_image)
        float.add_widget(bt2)
        
        self.popup = Popup(title=''.center(90),content=float,pos_hint={'right':1,'top':0.7},size_hint=(1,0.30),background='fotos/aurora.jpg')
        
        parar_audio(3)
        fala(3,'Se você deseja sair pressione Sim','Audios/resposta_ia.mp3',ativar)
        
        anim = Animation(pos_hint={'right':0.80,'top':0.7},duration=0.1) + Animation(pos_hint={'right':1.30,'top':0.7},duration=0.1) + Animation(pos_hint={'right':1,'top':0.7},duration=0.1)
        anim.start(self.popup)
        
        anim_color = Animation(color=(0,1,0,1)) + Animation(color=(1,0,0,1))
        anim_color.repeat = True
        anim_color.start(bt1)
        self.popup.open()
    
    def formatar_email(self,email,*args):
        return email.replace('.',',').replace('@','_')
    
    def mostrarsenha(self):
        if self.password == 0:
        	self.password = 1
        	self.ids['imagemsenha'].source = 'fotos/ocultarsenha.png'
        	self.ids['senha_user'].password = False
        else:
        	self.password = 0
        	self.ids['imagemsenha'].source = 'fotos/mostrarsenha.png'
        	self.ids['senha_user'].password = True
        
    def verificar_conexao(self):
    	try:
    		socket.create_connection(('www.google.com',443),timeout=5)
    		return True
    	except:
    	   return False
    	   
    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.tecla_voltar)
        self.ids['label_error'].text = ''
        
    def login(self,**kwargs):
        email = self.ids['email_user'].text
        senha = self.ids['senha_user'].text
        
        if self.verificar_conexao():
        	print(':&&&')
        else:
         	print('Errro')
         	self.ids['label_error'].text = 'Você não està conectado a internet'
         	self.ids['label_error'].color = 1,0,0,1
        
        if email == '':
        	self.ids['label_error'].text = 'Digite seu E-mail'
        	parar_audio(3)
        	fala(3,'Digite seu E-mail','Audios/resposta_ia.mp3',ativar)
        elif '@' not in email:
        	self.ids['label_error'].text = 'E-mail deve conter @'
        	parar_audio(3)
        	fala(3,'Seu E-mail deve conter @','Audios/resposta_ia.mp3',ativar)
        elif '.com' not in email:
        	self.ids['label_error'].text = 'E-mail deve conter .com'
        	parar_audio(3)
        	fala(3,'Seu E-mail deve conter .com','Audios/resposta_ia.mp3',ativar)
        elif senha == '':
        	self.ids['label_error'].text = 'Digite uma senha'
        	parar_audio(3)
        	fala(3,'Digite sua senha','Audios/resposta_ia.mp3',ativar)
        elif len(senha) < 6:
        	self.ids['label_error'].text = 'A senha deve conter pelo menos 6 digitos'
        	parar_audio(3)
        	fala(3,'Sua senha deve ter pelo menos 6 digitos','Audios/resposta_ia.mp3',ativar)
        else:
        	try:
        		email_formatado = self.formatar_email(email)
        		
        		nome_usuario = firebase_app.get(f'/Usuarios/{email_formatado}/nome',None)
        	
	        	validacao_email = firebase_app.get(f'/Usuarios/{email_formatado}/email',None)
	        	
	        	validacao_senha = firebase_app.get(f'/Usuarios/{email_formatado}/senha',None)
	        	
	        	foto_perfil = firebase_app.get(f'/Usuarios/{email_formatado}/foto_perfil',None)
	        	
	        	print(email_formatado)
	        	print(validacao_email)
	        	
	        	if email == validacao_email:
	        		if senha == validacao_senha:
	        			self.ids['label_error'].text = ''
	        			self.ids['email_user'].text = ''
	        			self.ids['senha_user'].text = ''
	        			
	        			user_name.append(nome_usuario)
	        			user_email.append(email_formatado)
	        			photo_profile.append(foto_perfil)
	        			parar_audio(3)
	        			fala(3,f'Olá, {user_name}. Seja muito bem vindo a ascensão. Como posso te ajudar hoje ','Audios/resposta_ia.mp3',ativar)
	        			
	        			self.manager.current = 'homepage'
	        		else:
	        			self.ids['label_error'].text = 'Senha Incorreta'
	        			parar_audio(3)
	        			fala(3,'Sua senha está incorreta','Audios/resposta_ia.mp3',ativar)
	        	else:
	        	    	self.ids['label_error'].text = 'Email não cadastrado' 
	        	    	parar_audio(3)
	        	    	fala(3,'Seu E-mail não está cadastrado','Audios/resposta_ia.mp3',ativar)
        		
        	except Exception as c:
        		print(c)
        
    def saida(self,*args):
        parar_audio(3)
        fala(3,'Vá em paz. Volte sempre','Audios/resposta_ia.mp3',ativar)
        time.sleep(3)
        exit()
        
    def dispensar(self,*args):
       parar_audio(3)
       fala(3,'Fico feliz por ter decidido ficar','Audios/resposta_ia.mp3',ativar)
       self.popup.dismiss()
       
    def desativar_audio(self):
    	global ativar
    	global contador
    	if contador == 0:
    		contador = 1
	    	ativar = False
	    	parar_audio(3)
	    	fala(3,'Sistema de áudio desativado','Audios/resposta_ia.mp3',ativar=True)
	    	self.ids['icone_audio'].source = 'fotos/ativar_audio.png'
    	elif contador == 1:
	    	contador = 0
	    	ativar = True
	    	parar_audio(3)
	    	fala(3,'Sistema de áudio ativado','Audios/resposta_ia.mp3',ativar=True)
	    	self.ids['icone_audio'].source = 'fotos/desativar_audio.png'
         	
        
class LabelButton(ButtonBehavior,Label):
        def __init__(self,**kwargs):
        	super().__init__(**kwargs)
        
class Cadastro(Screen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.password = 0
		self.password2 = 0
		
	def on_pre_enter(self):
		parar_audio(3)
		fala(3,'Se você deseja se cadastrar, preencha os campos do formulário','Audios/resposta_ia.mp3',ativar)
		Window.bind(on_keyboard=self.tecla_voltar)
	
	def tecla_voltar(self,window,key,*args):
		if key == 27:
			self.manager.current = 'menu'
			return True
	
	def on_pre_leave(self):
		Window.unbind(on_keyboard=self.tecla_voltar)
			
		
	def formatar_email(self,email,*args):
		return email.replace('.',',').replace('@','_')
		
	def mostrarsenha1(self):
		if self.password == 0:
			self.password = 1
			self.ids['imagemsenha1'].source = 'fotos/ocultarsenha.png'
			self.ids['senha1_input'].password = False
		else:
			self.password = 0
			self.ids['imagemsenha1'].source = 'fotos/mostrarsenha.png'
			self.ids['senha1_input'].password = True
	
	def mostrarsenha2(self):
		if self.password2 == 0:
			self.password2 = 1
			self.ids['imagemsenha2'].source = 'fotos/ocultarsenha.png'
			self.ids['senha2_input'].password = False
		else:
			self.password2 = 0
			self.ids['imagemsenha2'].source = 'fotos/mostrarsenha.png'
			self.ids['senha2_input'].password = True
		
	def verificar_conexao(self,*args):
		try:
			socket.create_connection(('www.google.com',443),timeout=5)
			return True
		except:
			return False
			
	def on_pre_leave(self):
		self.ids['label_error'].text = ''
		
	def enviar(self):
		email = self.ids['email_input'].text
		nome = self.ids['nome_input'].text
		senha1 = self.ids['senha1_input'].text
		senha2 = self.ids['senha2_input'].text
		
		if self.verificar_conexao():
			pass
		else:
			self.ids['label_error'].text = 'Você não está conectado a internet'
			self.ids['label_error'].color = 1,0,0,1
			
		
		print("""

{}

{}

{}

		""".format(email,senha1,senha2))
		
		if email == '':
			self.ids['label_error'].text = 'Digite seu E-mail'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			fala(3,'Digite seu E-mail','Audios/resposta_ia.mp3',ativar)
		elif '@' not in email:
			self.ids['label_error'].text = 'E-mail deve conter @'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			fala(3,'Seu E-mail deve conter @','Audios/resposta_ia.mp3',ativar)
		elif '.com' not in email:
			self.ids['label_error'].text = 'E-mail deve conter .com'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			fala(3,'Seu E-mail deve conter .com','Audios/resposta_ia.mp3',ativar)
		elif nome == '':
			self.ids['label_error'].text = 'Digite seu nome'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			fala(3,'Digite seu nome','Audios/resposta_ia.mp3',ativar)
		elif senha1 == '':
			self.ids['label_error'].text = 'Digite uma senha'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			fala(3,'Digite sua senha','Audios/resposta_ia.mp3',ativar)
		elif len(senha1) < 6:
			self.ids['label_error'].text = 'A senha deve conter pelo menos 6 digitos'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			fala(3,'Sua senha deve ter pelo menos 6 dígitos','Audios/resposta_ia.mp3',ativar)
		elif senha2 == '':
			self.ids['label_error'].text = 'Digite a senha novamente'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			fala(3,'Digite sua senha novamente','Audios/resposta_ia.mp3',ativar)
		elif senha1 != senha2:
			self.ids['label_error'].text = 'As senhas não conferem'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			fala(3,'As senhas não conferem','Audios/resposta_ia.mp3',ativar)
		else:
			self.ids['label_error'].text = ''
			self.ids['nome_input'].text = ''
			self.ids['email_input'].text = ''
			self.ids['senha1_input'].text = ''
			self.ids['senha2_input'].text = ''
			
			try:
				email_formatado = self.formatar_email(email)
				
				validacao = firebase_app.get(f'/Usuarios/{email_formatado}',None)
				
				if validacao:
					self.ids['label_error'].color = 1,0,0,1
					self.ids['label_error'].text = 'Email já cadastrado'
					parar_audio(3)
					fala(3,'Esse E-mail já está cadastrado na plataforma','Audios/resposta_ia.mp3',ativar)
				else:
					dados_cliente = {
					'email':email,
					'nome':nome,
					'senha':senha1,
					'foto_perfil':'foto1.png'
					}
					user_email.append(email_formatado)
					user_name.append(nome)
					photo_profile.append('foto1.png')
					resultado = firebase_app.put('/Usuarios',email_formatado,dados_cliente)
					parar_audio(3)
					fala(3,f'Olá, {user_name}. Seja muito bem vindo a ascensão. Como posso te ajudar hoje ','Audios/resposta_ia.mp3',ativar)
					
					self.manager.current = 'homepage'
			except:
				self.ids['label_error'].text = 'Você não está conectado a internet'
				self.ids['label_error'].color = 1,0,0,1
				pass
	   
class HomePage(Screen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		
	def on_pre_enter(self):
	    # Conecta e chama a função tecla_voltar
	    Window.bind(on_keyboard=self.tecla_voltar)
	    
	    nome_do_usuario = str(user_name)
	    self.ids['user_name'].text = nome_do_usuario.replace('[','').replace(']','').replace("'",'')
	    #self.ids['resposta_ia'].text = 'Como posso te ajudar ? ' #'teste '*250
	    
	    if len(historico_nome) == 0:
	    	resposta = self.ids['resposta_ia'].text
	    else:
	    	try:
	    		self.ids['resposta_ia'].text = str(historico_conteudo[0])
	    	except:
	    		pass
	    		
	    	resposta = self.ids['resposta_ia'].text
	    
	    try:
		    email = user_email[0]
		  	    
		    email_formatado = email.replace("@",'_').replace(".",',').replace(']','').replace('[','').replace("'",'')
		    
		    print('_'*30)
		    print(email_formatado)
		    
		    foto = firebase_app.get(f'/Usuarios/{email_formatado}/foto_perfil',None)
		    nome = firebase_app.get(f'/Usuarios/{email_formatado}/nome',None)
		    
		    self.ids['user_name'].text = nome or ''
		    	    
		    foto_perfil = str(photo_profile)
		    foto_perfil_formatada = foto_perfil.replace('[','').replace("]",'').replace("'",'')
		    
		    if 'foto_usuario' in os.getcwd():
		    	self.ids['foto_usuario'].source = f'{foto}'
		    else:
		    	self.ids['foto_usuario'].source = f'foto_usuario/{foto}'
	    	
	    except Exception as erro:
	    	print(erro)
	    	
	    	self.ids['label_error'].text = 'Você não está conectado a internet'
	    	self.ids['label_error'].color = 1,0,0,1
	    	
	def tecla_voltar(self,window,key,*args):
		if key == 27:
			self.sair()
			return True

	def on_pre_leave(self):
		Window.unbind(on_keyboard=self.tecla_voltar)
		self.ids['label_error'].text = ''
		
	def sair(self):
	       float = FloatLayout()
	       titulo = Label(text='Você quer realmente sair?',pos_hint={'right':0.70,'top':1},font_size=(45),size_hint=(0.40,0.30),color=(0,1,0,1))
	       bt1 = Button(text='Sim',pos_hint={'right':0.42,'top':0.6},size_hint=(0.40,0.30),background_color=(0,0,0,0))
	       bt1.bind(on_press=self.saida)
	       
	       parar_audio(3)
	       fala(3,'Se você deseja sair, pressione Sim','Audios/resposta_ia.mp3',ativar)
	       
	       bt1_image = Image(source='fotos/Botao.png',pos_hint={'right':0.42,'top':0.6},size_hint=(0.40,0.30))
	       
	       bt2 = Button(text='Não',pos_hint={'right':0.95,'top':0.6},size_hint=(0.40,0.30),background_color=(0,0,0,0))
	       bt2.bind(on_press=self.dispensar)
	       
	       bt2_image = Image(source='fotos/Botao.png',pos_hint={'right':0.95,'top':0.6},size_hint=(0.40,0.30))
	       
	       float.add_widget(titulo)
	       float.add_widget(bt1_image)
	       float.add_widget(bt1)
	       float.add_widget(bt2_image)
	       float.add_widget(bt2)
	       
	       self.popup = Popup(title=''.center(90),content=float,pos_hint={'right':1,'top':0.7},size_hint=(0.40,0.30),background="fotos/aurora.jpg")
	       
	       anim = Animation(pos_hint={'right':0.75,'top':0.7},size_hint=(1,0.30),duration=0.1) + Animation(pos_hint={'right':1.20,'top':0.7},size_hint=(1,0.30),duration=0.1) + Animation(pos_hint={'right':1,'top':0.7},size_hint=(1,0.30),duration=0.1)
	       anim.start(self.popup)
	       
	       anim_color = Animation(color=(0,1,0,1)) + Animation(color=(1,0,0,1))
	       anim_color.repeat = True
	       anim_color.start(bt1)
	       
	       self.popup.open()
	       
	       
	def saida(self,*args):
		self.popup.dismiss()
		user_email.clear()
		self.ids['resposta_ia'].text = 'Como posso ajudar você?'
		self.ids['resposta_ia'].size_hint = (1,0.40)
		self.manager.current = 'menu'
		
	def dispensar(self,*args):
		self.popup.dismiss() 
		parar_audio(3)
		fala(3,'Como posso te ajudar?','Audios/resposta_ia.mp3',ativar)
		
	def formatar_pergunta(self,pergunta,*args):
		return pergunta.replace('.','').replace('@','').replace('#','').replace('[','').replace(']','').replace('/','').replace('$','').replace('?','')
		
	def iniciar_processo(self):
		Clock.schedule_once(lambda dt: self.processo_iniciado())
		
	def processo_iniciado(self):
		self.pergunta = self.ids['entrada_usuario'].text
		headers = {'Authorization': f"Bearer {API_KEY}", 'Content_Type': 'application/json'}
		data = {
		"model": "Qwen/Qwen2.5-7B-Instruct-Turbo",
		"messages": [{"role":"user",'content': self.pergunta}]		
		}
		threading.Thread(target=self.processando,args=(self.pergunta,headers,data),daemon=True).start()
		
	def processando(self,pergunta,headers,data):
		response = requests.post(API_URL, headers=headers,json=data,timeout=30)
		
		if response.status_code == 200:
			try:
				resposta_text = response.json()['choices'][0]['message']['content']
				self.ids['resposta_ia'].text = '\nResposta\n\n' + resposta_text.strip()
				self.resposta = self.ids['resposta_ia'].text
				threading.Thread(target=self.atualizando_texto,daemon=True).start()
							
			except Exception as e:
				self.ids['resposta_ia'].text = f"Erro {e}"
				
	def atualizando_texto(self):
		threading.Thread(target=self.atualizando_ui,daemon=True).start()
		
	def atualizando_ui(self):
				parar_audio(3)
				fala(3,self.resposta,'Audios/resposta_ia.mp3',ativar)
				
				pergunta_formatada = self.formatar_pergunta(self.pergunta)
				
				email = str(user_email[0])
				
				email_formatado = email.replace('.',',').replace('@','_')
				
				info = {f'{pergunta_formatada}': f"{self.resposta}"}
				
				historico_conversa = firebase_app.patch(f'/Usuarios/{email_formatado}/historico',info)
				
				Clock.schedule_once(lambda dt: self.ids['resposta_ia'].texture_update(), 0.1)
				Clock.schedule_once(
				lambda dt: setattr(
					self.ids['resposta_ia'],
					'height',
					self.ids['resposta_ia'].texture_size[1] + 50 # Espaço extra
				), 0.15
				)
				
	def alterar_posicao(self):
		if self.ids['entrada_usuario'].focus == True:
			self.ids['entrada_usuario'].pos_hint = {'right':1,'top':0.50}
		else:
			self.ids['entrada_usuario'].pos_hint = {'right':1,'top':0.18}
			
class Configuracoes(Screen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		
	def on_pre_enter(self):
		parar_audio(3)
		fala(3,'Tela de configurações','Audios/resposta_ia.mp3',ativar)
		Window.bind(on_keyboard=self.tecla_voltar)
		
		if ativar == True:
			self.ids['icone_audio'].source = 'fotos/desativar_audio.png'
		else:
			self.ids['icone_audio'].source = 'fotos/ativar_audio.png'
	
	def tecla_voltar(self,window,key,*args):
		if key == 27:
			self.manager.current = 'homepage'
			return True
			
	def desativar_audio(self):
		global ativar
		global contador
		
		if contador == 0:
			ativar = False
			contador = 1
			self.ids['icone_audio'].source = 'fotos/ativar_audio.png'
			parar_audio(3)
			fala(3,'Sistema de áudio desativado','Audios/resposta_ia.mp3',ativar=True)
		elif contador == 1:
			ativar = True
			contador = 0
			self.ids['icone_audio'].source = 'fotos/desativar_audio.png'
			parar_audio(3)
			fala(3,'Sistema de áudio ativado','Audios/resposta_ia.mp3',ativar=True)
			
	
	def on_pre_leave(self):
		Window.unbind(on_keyboard=self.tecla_voltar)
		
class Mudar_Foto(Screen,Image,FloatLayout):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		
class ImageButton(ButtonBehavior,Image):
	pass

class Mudar_Foto(Screen):
    def on_pre_enter(self):
        parar_audio(3)
        fala(3,'Para alterar a foto de perfil, selecione uma das opções disponíveis','Audios/resposta_ia.mp3',ativar)
        Window.bind(on_keyboard=self.tecla_voltar)
        
        scroll = self.ids['teste']

        # Grid para mostrar 3 imagens por linha
        grid = GridLayout(cols=3, spacing=10, padding=10, size_hint_y=None)#10
        grid.bind(minimum_height=grid.setter('height'))
        
        print(os.getcwd())
        
        if 'foto_usuario' in os.getcwd():
        	pass
        else:
        	os.chdir("foto_usuario")
        	
        fotos = sorted(os.listdir())

        for foto in fotos:
            if foto.endswith('.png') or foto.endswith('.jpg'):
                img = ImageButton(source=os.path.join(os.getcwd(), foto),
                            size_hint_y=None,
                            height=170, 
                            allow_stretch=True,
                            keep_ratio=True)
                img.bind(on_press=lambda instance, foto=foto:self.mudar_foto_perfil(foto))
                grid.add_widget(img)
                

        scroll.clear_widgets()
        scroll.add_widget(grid)
        
    def mudar_foto_perfil(self,foto,**args):
    	try:
    		info = f'{{"foto_perfil": "{foto}"}}'
	    	print(info)
	    	nome_usuario = str(user_email)
	    	nome_usuario_formatado = nome_usuario.replace('[','').replace(']','').replace("'",'')
	    	print(nome_usuario_formatado)
	    	requisicao = requests.patch(f"https://inteligencia-artificial-37d91-default-rtdb.firebaseio.com/Usuarios/{nome_usuario_formatado}.json",data=info)
	    	print(requisicao.status_code)
	    	print(requisicao.text)
	    	parar_audio(3)
	    	fala(3,'Foto alterada com sucesso','Audios/resposta_ia.mp3',ativar)
	    	self.manager.current = 'homepage'
    	except:
    		self.ids["label_error"].text = 'Você não está conectado a internet'
    		self.ids['label_error'].color = 1,0,0,1
    		
    		
    def on_pre_leave(self):
    	Window.unbind(on_keyboard=self.tecla_voltar)
    	self.ids['label_error'].text = ''
    	
    	if 'foto_usuario' in os.getcwd():
    		os.chdir('..')
    	else:
    		pass
    
    def tecla_voltar(self,window,key,*args):
    	if key == 27:
    		self.manager.current = 'configuracoes'
    		return True
    	
class Mudar_Nome(Screen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		
	def on_pre_enter(self):
		parar_audio(3)
		fala(3,'Se você deseja mudar o nome, digite o nome de preferencia','Audios/resposta_ia.mp3',ativar)
		Window.bind(on_keyboard=self.tecla_voltar)
		
	def mudar_nome_perfil(self,**args):
	    self.nome = self.ids['campo_alterar_nome'].text
	    try:
    		info = f'{{"nome": "{self.nome}"}}'
	    	print(info)
	    	nome_usuario = str(user_email)
	    	nome_usuario_formatado = nome_usuario.replace('[','').replace(']','').replace("'",'')
	    	print(nome_usuario_formatado)
	    	requisicao = requests.patch(f"https://inteligencia-artificial-37d91-default-rtdb.firebaseio.com/Usuarios/{nome_usuario_formatado}.json",data=info)
	    	print(requisicao.status_code)
	    	print(requisicao.text)
	    	parar_audio(3)
	    	fala(3,'Nome alterado com sucesso','Audios/resposta_ia.mp3',ativar)
	    	self.manager.current = 'homepage'
	    except Exception as erro:
	    	print(erro)
    		self.ids["label_error"].text = 'Você não está conectado a internet'
    		self.ids['label_error'].color = 1,0,0,1
    
	def on_pre_leave(self):
		Window.unbind(on_keyboard=self.tecla_voltar)
		self.ids['label_error'].text = ''
		self.ids['campo_alterar_nome'].text = ''
	
	def tecla_voltar(self,window,key,*args):
		if key == 27:
			self.manager.current = "configuracoes"
			return True

class Mudar_Senha(Screen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.password = 0
		self.password2 = 0
		self.password3 = 0
		
	def on_pre_enter(self):
		parar_audio(3)
		fala(3,'Se você deseja alterar sua senha, preencha os campos em branco','Audios/resposta_ia.mp3',ativar)
		Window.bind(on_keyboard=self.tecla_voltar)
		
	def tecla_voltar(self,window,key,*args):
		if key == 27:
			self.manager.current = 'configuracoes'
			return True
	
	def on_pre_leave(self):
		Window.unbind(on_keyboard=self.tecla_voltar)
		
	def formatar_email(self,email,*args):
		email = str(email)
		return email.replace('.',',').replace('@','_')
		
	def mostrarsenha1(self):
		if self.password == 0:
			self.password = 1
			self.ids['imagemsenha1'].source = 'fotos/ocultarsenha.png'
			self.ids['senha1_input'].password = False
		else:
			self.password = 0
			self.ids['imagemsenha1'].source = 'fotos/mostrarsenha.png'
			self.ids['senha1_input'].password = True
	
	def mostrarsenha2(self):
		if self.password2 == 0:
			self.password2 = 1
			self.ids['imagemsenha2'].source = 'fotos/ocultarsenha.png'
			self.ids['senha2_input'].password = False
		else:
			self.password2 = 0
			self.ids['imagemsenha2'].source = 'fotos/mostrarsenha.png'
			self.ids['senha2_input'].password = True
		
	def mostrarsenha3(self):
		if self.password3 == 0:
			self.password3 = 1
			self.ids['imagemsenha3'].source = 'fotos/ocultarsenha.png'
			self.ids['senha3_input'].password = False
		else:
			self.password3 = 0
			self.ids['imagemsenha3'].source = 'fotos/mostrarsenha.png'
			self.ids['senha3_input'].password = True
		
	def mudar_senha(self):
		email_formatado = str(user_email[0])
		
		validacao_senha = firebase_app.get(f'/Usuarios/{email_formatado}/senha',None)
		
		if self.ids['senha1_input'].text == '':
			self.ids['label_error'].text = 'Digite sua senha antiga'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			fala(3,'Digite sua senha antiga','Audios/resposta_ia.mp3',ativar)
			
		elif len(self.ids['senha1_input'].text) < 6:
			self.ids['label_error'].text = 'Sua senha antiga deve ter pelo menos 6 caracteres'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			fala(3,'Sua senha antiga deve ter pelo menos 6 caracteres','Audios/resposta_ia.mp3',ativar)
			
		elif self.ids['senha2_input'].text == '':
			self.ids['label_error'].text = 'Digite sua nova senha'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			fala(3,'Digite sua nova senha','Audios/resposta_ia.mp3',ativar)
			
		elif len(self.ids['senha2_input'].text) < 6:
			self.ids['label_error'].text = 'Sua nova senha deve ter pelo menos 6 caracteres'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			fala(3,'Sua nova senha deve ter pelo menos 6 caracteres','Audios/resposta_ia.mp3',ativar)
			
		elif self.ids['senha3_input'].text == '':
			self.ids['label_error'].text = 'Digite sua nova senha novamente'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			fala(3,'Digite sua nova senha novamente','Audios/resposta_ia.mp3',ativar)
			
		elif len(self.ids['senha3_input'].text) < 6:
			self.ids['label_error'].text = 'Sua nova senha deve ter pelo menos 6 caracteres'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			fala(3,'Sua nova senha deve ter pelo menos 6 caracteres','Audios/resposta_ia.mp3',ativar)
			
		elif self.ids['senha2_input'].text != self.ids['senha3_input'].text:
			self.ids['label_error'].text = 'As senhas não conferem'
			parar_audio(3)
			fala(3,'As duas senhas não conferem','Audios/resposta_ia.mp3',ativar)
		
		elif self.ids['senha1_input'].text == self.ids['senha2_input'].text and self.ids['senha3_input'].text:
			self.ids['label_error'].text = 'Sua nova senha deve ser diferente da antiga'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			fala(3,'Sua senha deve ser diferente da antiga','Audios/resposta_ia.mp3',ativar)
			
		elif self.ids['senha1_input'].text != validacao_senha:
			self.ids['label_error'].text = 'Senha antiga está incorreta'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			fala(3,'Sua senha antiga está incorreta','Audios/resposta_ia.mp3',ativar)
		else:
		    self.senha = self.ids['senha2_input'].text
		    try:
	    		info = f'{{"senha": "{self.senha}"}}'
		    	print(info)
		    	nome_usuario = str(user_email)
		    	nome_usuario_formatado = nome_usuario.replace('[','').replace(']','').replace("'",'')
		    	print(nome_usuario_formatado)
		    	requisicao = requests.patch(f"https://inteligencia-artificial-37d91-default-rtdb.firebaseio.com/Usuarios/{nome_usuario_formatado}.json",data=info)
		    	print(requisicao.status_code)
		    	print(requisicao.text)
		    	print('Acerttoy')
		    	self.ids['senha1_input'].text = ''
		    	self.ids['senha2_input'].text = ''
		    	self.ids['senha3_input'].text = ''
		    	self.ids['label_error'].text = ''
		    	parar_audio(3)
		    	fala(3,'Senha alterada com sucesso','Audios/resposta_ia.mp3',ativar)
		    	self.manager.current = 'homepage'
		    except Exception as erro:
		    	print(erro)
	    		self.ids["label_error"].text = 'Você não está conectado a internet'
	    		self.ids['label_error'].color = 1,0,0,1
    		
	def on_pre_leave(self):
		self.ids['label_error'].text = ''
		
class Mudar_Email(Screen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		
	def on_pre_enter(self):
		parar_audio(3)
		fala(3,'Se você deseja mudar seu E-mail, digite o E-mail de preferencia','Audios/resposta_ia.mp3',ativar)
		Window.bind(on_keyboard=self.tecla_voltar)
		
	def tecla_voltar(self,window,key,*args):
		if key == 27:
			self.manager.current = 'configuracoes'
			return True
			
	def on_pre_leave(self):
		Window.unbind(on_keyboard=self.tecla_voltar)
		
	def mudar_email(self):
		email = self.ids['campo_alterar_email'].text
		email_formatado = self.formatar_email(email)
		validacao_email = firebase_app.get(f'/Usuarios/{email_formatado}/email',None)
		
		if email == '':
			self.ids['label_error'].text = 'Digite o novo E-mail'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			fala(3,'Digite seu novo E-mail','Audios/resposta_ia.mp3',ativar)
			
		elif '@' not in email:
			self.ids['label_error'].text = 'O email deve conter @'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			fala(3,'Seu E-mail deve conter @','Audios/resposta_ia.mp3',ativar)
			
		elif '.com' not in email:
			self.ids['label_error'].text = 'O email deve conter .com'
			self.ids['label_error'].color = 1,0,0,1
			parar_audio(3)
			fala(3,'Seu E-mail deve conter .com','Audios/resposta_ia.mp3',ativar)
		
		elif email == validacao_email:
			self.ids['label_error'].text = 'O novo E-mail deve ser diferente do antigo'
			parar_audio(3)
			fala(3,'O novo E-mail deve ser diferente do antigo','Audios/resposta_ia.mp3',ativar)
			
		else:
			self.email = self.ids['campo_alterar_email'].text
			try:
				email = user_email[0]
				email_formatado = self.formatar_email(email)
				
				print(email_formatado)
				
				email = firebase_app.get(f'/Usuarios/{email_formatado}/email',None)
				
				foto_perfil = firebase_app.get(f'/Usuarios/{email_formatado}/foto_perfil',None)
				
				try:
					self.historico = firebase_app.get(f'/Usuarios/{email_formatado}/historico',None)
				except:
					pass
				
				nome = firebase_app.get(f'/Usuarios/{email_formatado}/nome',None)
				
				senha = firebase_app.get(f'/Usuarios/{email_formatado}/senha',None)
				
				print("OVER HERE, STRANGER")
				print(email)
				print(foto_perfil)
				print(nome)
				print(senha)
				
				url = f"https://inteligencia-artificial-37d91-default-rtdb.firebaseio.com/Usuarios/{email_formatado}.json"
				
				res = requests.delete(url)
				
				novo_email = self.formatar_email(self.ids['campo_alterar_email'].text)
				
				dados_cliente = {
				'email': self.ids['campo_alterar_email'].text,
				'foto_perfil': foto_perfil,
				'historico':self.historico,
				'nome': nome,
				'senha': senha
				}
				
				resultado = firebase_app.put('/Usuarios',novo_email,dados_cliente)
				
				user_email.clear()
				
				user_email.append(novo_email)
				
				self.ids['label_error'].text = ''
				self.ids['campo_alterar_email'].text = ''
				parar_audio(3)
				fala(3,'E-mail alterado com sucesso','Audios/resposta_ia.mp3',ativar)
				self.manager.current = 'homepage'
				
			except Exception as erro:
				print(erro)
				self.ids["label_error"].text = 'Você não está conectado a internet'
				self.ids['label_error'].color = 1,0,0,1
		

	def formatar_email(self,email,*args):
		email = str(email)
		return email.replace('.',',').replace('@','_')

class Historico_Conversas(Screen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		
	def on_pre_enter(self):
		parar_audio(3)
		fala(3,'Se você deseja continuar ou excluir uma conversa anterior, selecione uma das opçōes disponíveis','Audios/resposta_ia.mp3',ativar)
		Window.bind(on_keyboard=self.voltar)
		
		email = str(user_email[0])
		
		email_formatado = email.replace('@','_').replace('.',',')
		
		try:
			self.historico = firebase_app.get(f'/Usuarios/{email_formatado}/historico',None)
			
			for palavra in self.historico.keys():
				if self.historico.keys == None:
					pass
				else:
					grid = FloatLayout(size_hint_y=None,height=140)
					self.button = Button(text=str(palavra),pos_hint={'center_x':0.5,'center_y':0.2},size_hint=(0.5,None),size_hint_y=None,background_color=(0,0,0,0),height=100)
					self.button.bind(on_press=self.iniciar_processo)
					self.botao_excluir = Button(text=str(palavra),color=(0,0,0,0),pos_hint={'center_x':0.9,'center_y':0.2},size_hint=(0.1,None),size_hint_y=None,height=80,background_disabled_normal='',background_normal='',background_color=(0,0,0,0))
					self.botao_excluir.bind(on_press=self.excluir_conversa_arquivada)
					self.foto_excluir = Image(pos_hint={'center_x':0.9,'center_y':0.2},size_hint=(0.1,None),size_hint_y=None,height=80,source='fotos/excluir2.png')
					grid.add_widget(self.botao_excluir)
					grid.add_widget(self.button)
					grid.add_widget(self.foto_excluir)
					self.ids['float'].add_widget(grid)
		except Exception as erro:
			print('Erro')
			
	def on_leave(self):
		self.ids['float'].clear_widgets()
		
	def voltar(self,window,key,*args):
		if key == 27:
			self.manager.current = 'configuracoes'
			return True
			
	def excluir_conversa_arquivada(self,instance,*args):
			historico_nome.clear()
			historico_conteudo.clear()
			historico_nome.append(instance.text)
			
			email = str(user_email[0])
			
			email_formatado = email.replace('.',',').replace('@','_')
			
			url = f"https://inteligencia-artificial-37d91-default-rtdb.firebaseio.com/Usuarios/{email_formatado}/historico/{historico_nome[0]}.json" 
			requests.delete(url)
			
			parar_audio(3)
			fala(3,'Conversa Excluída com sucesso','Audios/resposta_ia.mp3',ativar)
			
			self.manager.current = 'homepage'
			
	def iniciar_processo(self,instance):
		
		self.manager.current = 'aguardando'
		
		self.instancia = instance
		Clock.schedule_once(lambda dt: self.processo_iniciado())
		
	def processo_iniciado(self):
		threading.Thread(target=self.conversa_arquivada,daemon=True).start()
			
	def conversa_arquivada(self,*args):
		parar_audio(3)
		fala(3,'Carregando conversa','Audios/resposta_ia.mp3',ativar)
		time.sleep(3)
		try:
			historico_nome.clear()
			historico_conteudo.clear()
			historico_nome.append(self.instancia.text)
			
			email = str(user_email[0])
			email_formatado = email.replace('@','_').replace('.',',')
			
			pergunta = self.instancia.text
			self.historico_conteudo = firebase_app.get(f'/Usuarios/{email_formatado}/historico/{historico_nome[0]}',None)
			historico_conteudo.append(self.historico_conteudo)
			
		except Exception as erro:
			print(erro)
		
		parar_audio(3)
		fala(3,historico_conteudo[0],'Audios/resposta_ia.mp3',ativar)
		
		Clock.schedule_once(lambda dt: setattr(self.manager,'current','homepage'))

	def formatar_pergunta(self,pergunta,*args):
		return pergunta.replace('.',',').replace('@','_').replace('#','').replace('[','').replace(']','').replace('/','').replace('$','').replace(' ','')

class Aguardando(Screen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.frame = 0
		
	def on_pre_enter(self):
		self.rotulo = Label(text='',pos_hint={'top':1,'right':1},size_hint=(1,1),font_size=55)
		self.ids['float'].add_widget(self.rotulo)
		
		self.anim = Animation(color=(1,1,1,1),duration=3) + Animation(color=(0,1,0,1),duration=2) + Animation(color=(1,1,1,1),duration=3) + Animation(color=(0,0,1,1),duration=2) + Animation(color=(1,1,1,1),duration=3) + Animation(color=(1,0,0,1),duration=2)
		self.anim.repeat = True
		self.anim.start(self.rotulo)
		Clock.schedule_interval(self.atualizar_texto,0.5)
		
	def atualizar_texto(self,dt):
		pontos = '.' * (self.frame % 4)
		self.rotulo.text = f"Carregando {pontos}"
		self.frame += 1
		
	def on_pre_leave(self):
		self.ids['float'].remove_widget(self.rotulo)
		
Gui = Builder.load_file('main.kv')

class Inteligencia_Artificial(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Menu(name='menu'))
        sm.add_widget(Cadastro(name='cadastro'))
        sm.add_widget(HomePage(name='homepage'))
        sm.add_widget(Configuracoes(name='configuracoes'))
        sm.add_widget(Mudar_Foto(name='mudar_foto'))
        sm.add_widget(Mudar_Nome(name='mudar_nome'))
        sm.add_widget(Mudar_Senha(name='mudar_senha'))
        sm.add_widget(Mudar_Email(name='mudar_email'))
        sm.add_widget(Historico_Conversas(name='historico_conversas'))
        sm.add_widget(Aguardando(name='aguardando'))
        return sm

if __name__ == '__main__':
	Inteligencia_Artificial().run()





