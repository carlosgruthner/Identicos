pyinstaller --onefile --windowed --icon=file.ico --add-data "file.ico;." --add-data "C:\Python313\Lib\site-packages\customtkinter;customtkinter" --hidden-import customtkinter --hidden-import darkdetect .\Identicos.py
#Obs - C:\Python313 é a versão do python que estou usando. Selecione a versão correta.