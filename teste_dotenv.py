# Importa módulos necessários
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

# Módulo padrão do Python para acessar variáveis de ambiente
import os

# Carrega as variáveis do .env
from dotenv import load_dotenv

# Carrega o conteúdo do arquivo .env para as variáveis de ambiente
load_dotenv()  # Esse comando procura o arquivo .env e carrega suas variáveis no ambiente

# Pega as variáveis usando os nomes definidos no .env
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")


# Define a interface principal do aplicativo
class MainInterface(BoxLayout):
    def __init__(self, **kwargs):
        # Chama o construtor da classe pai
        super().__init__(**kwargs)
        self.orientation = 'vertical'  # Layout em coluna (vertical)

        # Cria um rótulo que mostra parte da chave da API (ocultando por segurança)
        chave_oculta = API_KEY[:6] + "..." if API_KEY else "Chave não encontrada"
        self.label = Label(text=f"Chave da API (parcial): {chave_oculta}", font_size='20sp')
        self.add_widget(self.label)

        # Botão para exibir a URL
        self.button = Button(text="Mostrar URL da API", size_hint=(1, 0.2))
        self.button.bind(on_press=self.mostrar_url)
        self.add_widget(self.button)

        # Label que exibirá a URL quando o botão for pressionado
        self.url_label = Label(text="", font_size='16sp')
        self.add_widget(self.url_label)

    def mostrar_url(self, instance):
        # Mostra a URL que veio do .env
        self.url_label.text = f"URL: {API_URL}" if API_URL else "URL não encontrada"


# Define a classe principal do aplicativo
class MeuApp(App):
    def build(self):
        # Retorna a interface gráfica principal
        return MainInterface()


# Executa o aplicativo
if __name__ == '__main__':
    MeuApp().run()