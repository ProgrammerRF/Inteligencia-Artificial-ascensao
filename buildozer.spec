[app]

# Nome do seu aplicativo
title = MeuApp

# Nome do pacote (nome do app no Android)
package.name = meuapp

# Domínio reverso (padrão para pacotes Android, pode inventar um)
package.domain = org.rafael

# Diretório onde está o main.py
source.dir = .

# Extensões de arquivos a serem incluídas no APK
source.include_exts = py,png,jpg,kv,atlas

# Versão do app
version = 0.1

# Bibliotecas necessárias
requirements = python3,kivy

# Orientação do app (retrato)
orientation = portrait

# Versão do Python no macOS (ignorada no Android)
osx.python_version = 3

# Versão do Kivy (pode deixar padrão)
osx.kivy_version = 2.3.0

# Ativar modo não-fullscreen (barra de status visível)
fullscreen = 0

# Permissões Android necessárias
android.permissions = INTERNET

# Arquiteturas Android compatíveis
android.archs = arm64-v8a, armeabi-v7a

# Modo de backup
android.allow_backup = True

# Tipo de APK de depuração (debug)
android.debug_artifact = apk

[buildozer]

# Nível de log
log_level = 2

# Aviso se rodar como root
warn_on_root = 1