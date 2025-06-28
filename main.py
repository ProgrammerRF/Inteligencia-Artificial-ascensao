#!/user/bin/env python
#-*-coding:utf8-*-
#qpy:3
#qpy:kivy

__Author__ = "Rafael Moraes De Oliveira"
__Date__ = "Sábado (08/03/2025)"

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
from firebase import firebase
from kivy.core.window import Window

# Sua chave da API Together
API_KEY = '''tgp_v1_qHmRJD_1nhQKYnrVYUm6TDKTmXXJa58hNv1xkmNqsuE'''
API_URL = 'https://api.together.ai/v1/chat/completions'

firebase_app = firebase.FirebaseApplication("https://inteligencia-artificial-37d91-default-rtdb.firebaseio.com/",None)

user_name = []
photo_profile = []
user_email = []

class Menu(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        
    def on_pre_enter(self):
        Window.bind(on_keyboard=self.tecla_voltar)
        
    def tecla_voltar(self,window,key,*args):
        if key == 27:
        	self.sair()
        	return True
       
    def sair(self):
        float = FloatLayout()
        titulo = Label(text='Você quer realmente sair?',pos_hint={'right':0.70,'top':1},font_size=(45),size_hint=(0.40,0.30),color=(0,1,0,1))
        bt1 = Button(text='Sim',pos_hint={'right':0.42,'top':0.6},size_hint=(0.40,0.30),background_color=(0,0,0,0))
        bt1.bind(on_press=self.saida)
        
        bt1_image = Image(source='/storage/emulated/0/Python/Inteligencia_Artificial/fotos/Botao.png',pos_hint={'right':0.42,'top':0.6},size_hint=(0.40,0.30))
        
        bt2 = Button(text='Não',pos_hint={'right':0.95,'top':0.6},size_hint=(0.40,0.30),background_color=(0,0,0,0))
        bt2.bind(on_press=self.dispensar)
        
        bt2_image = Image(source='/storage/emulated/0/Python/Inteligencia_Artificial/fotos/Botao.png',pos_hint={'right':0.95,'top':0.6},size_hint=(0.40,0.30))
        
        float.add_widget(titulo)
        
        float.add_widget(bt1_image)
        float.add_widget(bt1)
        
        float.add_widget(bt2_image)
        float.add_widget(bt2)
        
        self.popup = Popup(title=''.center(90),content=float,pos_hint={'right':1,'top':0.7},size_hint=(1,0.30),background="/storage/emulated/0/Python/Inteligencia_Artificial/fotos/fundo_preto.png")
        
        self.popup.open()
    
    def formatar_email(self,email,*args):
        return email.replace('.',',').replace('@','_')
    
    def mostrarsenha(self):
        self.ids['senha_user'].password = False
        
    def ocultarsenha(self):
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
        elif '@' not in email:
        	self.ids['label_error'].text = 'E-mail deve conter @'
        elif '.com' not in email:
        	self.ids['label_error'].text = 'E-mail deve conter .com'
        elif senha == '':
        	self.ids['label_error'].text = 'Digite uma senha'
        elif len(senha) < 6:
        	self.ids['label_error'].text = 'A senha deve conter pelo menos 6 digitos'
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
	        			
	        			self.manager.current = 'homepage'
	        		else:
	        			self.ids['label_error'].text = 'Senha Incorreta'
	        	else:
	        	    	self.ids['label_error'].text = 'Email não cadastrado' 
        		
        	except Exception as c:
        		print(c)
        
    def saida(self,*args):
        exit()
        
    def dispensar(self,*args):
       self.popup.dismiss()
         	
        
class LabelButton(ButtonBehavior,Label):
        def __init__(self,**kwargs):
        	super().__init__(**kwargs)
        
class Cadastro(Screen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		
	def on_pre_enter(self):
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
		self.ids['senha1_input'].password = False
	
	def mostrarsenha2(self):
		self.ids['senha2_input'].password = False
	
	def ocultarsenha1(self):
		self.ids['senha1_input'].password = True
	
	def ocultarsenha2(self):
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
		elif '@' not in email:
			self.ids['label_error'].text = 'E-mail deve conter @'
			self.ids['label_error'].color = 1,0,0,1
		elif '.com' not in email:
			self.ids['label_error'].text = 'E-mail deve conter .com'
			self.ids['label_error'].color = 1,0,0,1
		elif nome == '':
			self.ids['label_error'].text = 'Digite seu nome'
			self.ids['label_error'].color = 1,0,0,1
		elif senha1 == '':
			self.ids['label_error'].text = 'Digite uma senha'
			self.ids['label_error'].color = 1,0,0,1
		elif len(senha1) < 6:
			self.ids['label_error'].text = 'A senha deve conter pelo menos 6 digitos'
			self.ids['label_error'].color = 1,0,0,1
		elif senha2 == '':
			self.ids['label_error'].text = 'Digite a senha novamente'
			self.ids['label_error'].color = 1,0,0,1
		elif senha1 != senha2:
			self.ids['label_error'].text = 'As senhas não conferem'
			self.ids['label_error'].color = 1,0,0,1
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
					
					self.manager.current = 'homepage'
			except:
				self.ids['label_error'].text = 'Você não está conectado a internet'
				self.ids['label_error'].color = 1,0,0,1
				pass
	   
class HomePage(Screen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		
	def on_pre_enter(self):
	    Window.bind(on_keyboard=self.tecla_voltar)
	    
	    nome_do_usuario = str(user_name)
	    self.ids['user_name'].text = nome_do_usuario.replace('[','').replace(']','').replace("'",'')
	    #self.ids['resposta_ia'].text = 'Como posso te ajudar ? ' #'teste '*250
	    
	    resposta = self.ids['resposta_ia'].text
	
	    separar = resposta.split()
	    
	    try:
		    email = user_email[0]
		  	    
		    email_formatado = email.replace("@",'_').replace(".",',').replace(']','').replace('[','').replace("'",'')
		    
		    print('_'*30)
		    print(email_formatado)
		    
		    foto = firebase_app.get(f'/Usuarios/{email_formatado}/foto_perfil',None)
		    nome = firebase_app.get(f'/Usuarios/{email_formatado}/nome',None)
		    
		    print("WHERE IS THE ERROR")
		    print(nome)
		    
		    self.ids['user_name'].text = nome or ''
		    
		    print(email)
		    print()
		    print(foto)
		    
		    foto_perfil = str(photo_profile)
		    foto_perfil_formatada = foto_perfil.replace('[','').replace("]",'').replace("'",'')
		    
		    self.ids['foto_usuario'].source = f'/storage/emulated/0/Python/Inteligencia_Artificial/foto_usuario/{foto}'
	    	
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
	       
	       bt1_image = Image(source='/storage/emulated/0/Python/Inteligencia_Artificial/fotos/Botao.png',pos_hint={'right':0.42,'top':0.6},size_hint=(0.40,0.30))
	       
	       bt2 = Button(text='Não',pos_hint={'right':0.95,'top':0.6},size_hint=(0.40,0.30),background_color=(0,0,0,0))
	       bt2.bind(on_press=self.dispensar)
	       
	       bt2_image = Image(source='/storage/emulated/0/Python/Inteligencia_Artificial/fotos/Botao.png',pos_hint={'right':0.95,'top':0.6},size_hint=(0.40,0.30))
	       
	       float.add_widget(titulo)
	       float.add_widget(bt1_image)
	       float.add_widget(bt1)
	       float.add_widget(bt2_image)
	       float.add_widget(bt2)
	       
	       self.popup = Popup(title=''.center(90),content=float,pos_hint={'right':1,'top':0.7},size_hint=(1,0.30),background="/storage/emulated/0/Python/Inteligencia_Artificial/fotos/fundo_preto.png")
	       
	       self.popup.open()
	       
	       
	def saida(self,*args):
		self.popup.dismiss()
		user_email.clear()
		self.ids['resposta_ia'].text = 'Como posso ajudar você?'
		self.ids['resposta_ia'].size_hint = (1,0.40)
		self.manager.current = 'menu'
		
	def dispensar(self,*args):
		self.popup.dismiss() 
	
	def send_question(self, *args):
		pergunta = self.ids['entrada_usuario'].text
		
		headers = { "Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json",}
		
		data = {"model": "mistralai/Mistral-7B-Instruct-v0.2","messages": [{"role": "user", "content": pergunta}]}
		
		response = requests.post(API_URL, headers=headers, json=data)
		
		self.ids['entrada_usuario'].text = ''
		
		if response.status_code == 200:
		    resposta = response.json()['choices'][0]['message']['content']
		    self.ids['resposta_ia'].text = "Resposta: " + resposta
		    
		    resposta = self.ids['resposta_ia'].text
	
		    separar = resposta.split()
		    
		    print(len(separar))
		    
		    if len(separar) < 100:
		    	self.ids['resposta_ia'].size_hint = (1,3.90)
		    	
		    elif len(separar) == 100:
		    	self.ids['resposta_ia'].size_hint = (1,3.90)
		    
		    elif len(separar) < 250 and len(separar) > 100:
		    	self.ids['resposta_ia'].size_hint = (1,3.90)
		    
		    elif len(separar) == 250:
		    	self.ids['resposta_ia'].size_hint = (1,3.90)
		    	
		    elif len(separar) < 500 and len(separar) > 250:
		    	self.ids['resposta_ia'].size_hint = (1,5.10)
		    
		    elif len(separar) == 500:
		    	self.ids['resposta_ia'].size_hint = (1,5.10)
		    	
		    elif len(separar) < 750 and len(separar) > 500:
		    	self.ids['resposta_ia'].size_hint = (1,5.10)	    		
		    elif len(separar) == 750:
		    	self.ids['resposta_ia'].size_hint = (1,5.10)
		    	
		    elif len(separar) < 1000 and len(separar) > 750:
		    	self.ids['resposta_ia'].size_hint = (1,5.10)
		    	
		    elif len(separar) == 1000:
		    	self.ids['resposta_ia'].size_hint = (1,5.10)
		    	
		    elif len(separar) < 1250 and len(separar) > 1000:
		    	self.ids['resposta_ia'].size_hint = (1,5.20)
		    	
		    elif len(separar) == 1250:
		    	self.ids['resposta_ia'].size_hint = (1,5.20)
		    	
		    elif len(separar) < 1500 and len(separar) > 1250:
		    	self.ids['resposta_ia'].size_hint = (1,6.20)
		    	
		    elif len(separar) == 1500:
		    	self.ids['resposta_ia'].size_hint = (1,6.20)
		    
		    elif len(separar) < 1750 and len(separar) > 1500:
		    	self.ids['resposta_ia'].size_hint = (1,7.10)
		    	
		    elif len(separar) == 1750:
		    	self.ids['resposta_ia'].size_hint = (1,7.10)
		    	
		    elif len(separar) < 2000 and len(separar) > 1750:
		    	self.ids['resposta_ia'].size_hint = (1,8.20)
		    	
		    elif len(separar) == 2000:
		    	self.ids['resposta_ia'].size_hint = (1,8.20)
		    	
		    elif len(separar) < 2232 and len(separar) > 2000:
		    	self.ids['resposta_ia'].size_hint = (1,9)
		    	
		    elif len(separar) == 2232:
		    	self.ids['resposta_ia'].size_hint = (1,9)
	
	
	
	
		    
		    print(len(separar))
		    # 500
		    
		    # Organizando em linhas de 8 palavras
		    linhas = []
		    for i in range(0, len(separar), 6):
		        linha = ' '.join(separar[i:i+6])
		        linhas.append(linha)
		    
		    self.ids['resposta_ia'].text = '\n'.join(linhas).replace('.','\n\n').strip()
		else:
			self.ids['resposta_ia'].text = "Erro: " + str(response.json())
		
			
		
		
		
	def alterar_posicao(self):
		if self.ids['entrada_usuario'].focus == True:
			self.ids['entrada_usuario'].pos_hint = {'right':1,'top':0.40}
		else:
			self.ids['entrada_usuario'].pos_hint = {'right':1,'top':0.18}
			
class Configuracoes(Screen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		
	def on_pre_enter(self):
		Window.bind(on_keyboard=self.tecla_voltar)
	
	def tecla_voltar(self,window,key,*args):
		if key == 27:
			self.manager.current = 'homepage'
			return True
	
	def on_pre_leave(self):
		Window.unbind(on_keyboard=self.tecla_voltar)
		
class Mudar_Foto(Screen,Image,FloatLayout):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		
class ImageButton(ButtonBehavior,Image):
	pass

class Mudar_Foto(Screen):
    def on_pre_enter(self):
        Window.bind(on_keyboard=self.tecla_voltar)
        
        scroll = self.ids['teste']

        # Grid para mostrar 3 imagens por linha
        grid = GridLayout(cols=3, spacing=10, padding=10, size_hint_y=None)#10
        grid.bind(minimum_height=grid.setter('height'))

        os.chdir("/storage/emulated/0/Python/Inteligencia_Artificial/foto_usuario")
        fotos = sorted(os.listdir())

        for foto in fotos:
            if foto.endswith('.png') or foto.endswith('.jpg'):
                img = ImageButton(source=os.path.join(os.getcwd(), foto),
                            size_hint_y=None,
                            height=200, 
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
	    	self.manager.current = 'homepage'
    	except:
    		self.ids["label_error"].text = 'Você não está conectado a internet'
    		self.ids['label_error'].color = 1,0,0,1
    		
    def on_pre_leave(self):
    	Window.unbind(on_keyboard=self.tecla_voltar)
    	self.ids['label_error'].text = ''
    
    def tecla_voltar(self,window,key,*args):
    	if key == 27:
    		self.manager.current = 'configuracoes'
    		return True
    	
class Mudar_Nome(Screen):
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		
	def on_pre_enter(self):
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
		
	def on_pre_enter(self):
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
		self.ids['senha1_input'].password = False
	
	def mostrarsenha2(self):
		self.ids['senha2_input'].password = False
		
	def mostrarsenha3(self):
		self.ids['senha3_input'].password = False
	
	def ocultarsenha1(self):
		self.ids['senha1_input'].password = True
	
	def ocultarsenha2(self):
		self.ids['senha2_input'].password = True
		
	def ocultarsenha3(self):
		self.ids['senha3_input'].password = True
		
	def mudar_senha(self):
		email_formatado = str(user_email[0])
		
		validacao_senha = firebase_app.get(f'/Usuarios/{email_formatado}/senha',None)
		
		if self.ids['senha1_input'].text == '':
			self.ids['label_error'].text = 'Digite sua senha antiga'
			self.ids['label_error'].color = 1,0,0,1
			
		elif len(self.ids['senha1_input'].text) < 6:
			self.ids['label_error'].text = 'Sua senha antiga deve ter pelo menos 6 caracteres'
			self.ids['label_error'].color = 1,0,0,1
			
		elif self.ids['senha2_input'].text == '':
			self.ids['label_error'].text = 'Digite sua nova senha'
			self.ids['label_error'].color = 1,0,0,1
			
		elif len(self.ids['senha2_input'].text) < 6:
			self.ids['label_error'].text = 'Sua nova senha deve ter pelo menos 6 caracteres'
			self.ids['label_error'].color = 1,0,0,1
			
		elif self.ids['senha3_input'].text == '':
			self.ids['label_error'].text = 'Digite sua nova senha novamente'
			self.ids['label_error'].color = 1,0,0,1
			
		elif len(self.ids['senha3_input'].text) < 6:
			self.ids['label_error'].text = 'Sua nova senha deve ter pelo menos 6 caracteres'
			self.ids['label_error'].color = 1,0,0,1
			
		elif self.ids['senha2_input'].text != self.ids['senha3_input'].text:
			self.ids['label_error'].text = 'As senhas não conferem'
		
		elif self.ids['senha1_input'].text == self.ids['senha2_input'].text and self.ids['senha3_input'].text:
			self.ids['label_error'].text = 'Sua nova senha deve ser diferente da antiga'
			self.ids['label_error'].color = 1,0,0,1
			
		elif self.ids['senha1_input'].text != validacao_senha:
			self.ids['label_error'].text = 'Senha antiga está incorreta'
			self.ids['label_error'].color = 1,0,0,1
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
			
		elif '@' not in email:
			self.ids['label_error'].text = 'O email deve conter @'
			self.ids['label_error'].color = 1,0,0,1
			
		elif '.com' not in email:
			self.ids['label_error'].text = 'O email deve conter .com'
			self.ids['label_error'].color = 1,0,0,1
		
		elif email == validacao_email:
			self.ids['label_error'].text = 'O novo E-mail deve ser diferente do antigo'
			
		else:
			self.email = self.ids['campo_alterar_email'].text
			try:
				email = user_email[0]
				email_formatado = self.formatar_email(email)
				
				print(email_formatado)
				
				email = firebase_app.get(f'/Usuarios/{email_formatado}/email',None)
				
				foto_perfil = firebase_app.get(f'/Usuarios/{email_formatado}/foto_perfil',None)
				
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
				'nome': nome,
				'senha': senha
				}
				
				resultado = firebase_app.put('/Usuarios',novo_email,dados_cliente)
				
				user_email.clear()
				
				user_email.append(novo_email)
				
				self.ids['label_error'].text = ''
				self.ids['campo_alterar_email'].text = ''
				self.manager.current = 'homepage'
				
			except Exception as erro:
				print(erro)
				self.ids["label_error"].text = 'Você não está conectado a internet'
				self.ids['label_error'].color = 1,0,0,1
		

	def formatar_email(self,email,*args):
		email = str(email)
		return email.replace('.',',').replace('@','_')
		
	
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
        return sm

if __name__ == '__main__':
	Inteligencia_Artificial().run()





