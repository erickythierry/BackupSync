from tkinter import *
from tkinter import ttk
import threading
import os
import time
from pystray import MenuItem as item
import pystray
import PIL.Image

class Tela:
    imagePath = 'img/bk.png'
    login = os.getlogin()
    bkp = login + '.old'
    dirBkp = 'F:/bkp'
    
    def __init__(self):
        self.image = PIL.Image.open("img/image.png")
        self.menu = (item('abrir', self.inicio), item('sair', self.sair))
        self.icon = pystray.Icon("backup", self.image, "backup", self.menu)

    
    def copiando(self):      
        t3 = threading.Thread(target=self.pb)
        t3.start()
        self.lblFim['text']='Recuperando Backup'
        self.lblFim.place(relx=0.5, rely=0.925, anchor=CENTER)
        self.copy = os.system(f'robocopy.exe {os.path.join(self.dirBkp, self.bkp)} %userprofile%\ /s /e')
        os.renames(os.path.join(self.dirBkp, self.bkp), os.path.join(self.dirBkp, self.login + '.bkpRestaurado'))
        self.fim()        
        
    def inicio(self):
        self.root = Tk()
        self.root.iconbitmap('img/logo.ico')
        self.root.geometry('300x300+300+100')
        self.root.maxsize(300, 300)
        self.root.title('Backup Restore - v_1.0')
        self.photo = PhotoImage(file=self.imagePath)
        self.w = Label(self.root, image=self.photo)
        self.w.pack()

        self.btnStart = Button(self.root, height='2', width='10', text='Fazer Backup', font=('arial', 10), command=self.fazerBkp)
        self.btnStart.place(relx=0.5, rely=0.3, anchor=CENTER)
        self.btnStart = Button(self.root, height='2', width='10', text='Recuperar', font=('arial', 10), command=self.consultaBkp)
        self.btnStart.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.btnSair = Button(self.root, height='2', width = '10',text='Sair', font=('arial', 10), command=self.root.destroy)
        self.btnSair.place(relx=0.5, rely=0.7, anchor=CENTER)
        self.lblFim = Label(self.root, text='', font=('arial', 10), fg='red', relief='groove')
        self.root.mainloop()

    def pb(self):
        self.progress = ttk.Progressbar(self.root, orient='horizontal', length=280, mode='indeterminate')
        self.progress.place(relx=0.5, rely=0.85, anchor=CENTER)
        self.progress.start(10)
               

    def fazBkp(self):
        t5 = threading.Thread(target=self.pb)
        t5.start()
        self.lblFim['text']='fazendo Backup'
        self.lblFim.place(relx=0.5, rely=0.925, anchor=CENTER)
        self.copy = os.system(f'robocopy.exe %userprofile% {os.path.join(self.dirBkp, self.bkp)}\ /s /e')
        
        self.fim()   


    def consultaBkp(self):
        
        self.bkpDisponiveis = os.listdir(self.dirBkp)

        if self.bkp in self.bkpDisponiveis:
            self.confirmaBkp()
        else:
            self.rootAlert2 = Tk()
            self.rootAlert2.iconbitmap('img/logo.ico')
            self.rootAlert2['bg'] = '#C0C0C0'
            self.rootAlert2.geometry('400x100+300+450')
            self.rootAlert2.maxsize(400, 100)
            self.rootAlert2.title('Alerta!')
            self.lblConfirm = Label(self.rootAlert2, text=f'Não foi localizado nenhum backup para o login "{self.login}"',font=('arial', 10), bg='#C0C0C0',relief='groove')
            self.lblConfirm.place(relx=0.5, rely=0.2, anchor=CENTER)
            self.btnSair2 = Button(self.rootAlert2, width = '10', height='2', text='Ok', command=self.rootAlert2.destroy)
            self.btnSair2.place(relx=0.5, rely=0.65, anchor=CENTER)


    def confirmaBkp(self):
        self.rootAlert1 = Tk()
        self.rootAlert1.iconbitmap('img/logo.ico')
        self.rootAlert1['bg']='#C0C0C0'
        self.rootAlert1.geometry('400x100+300+450')
        self.rootAlert1.maxsize(400, 100)
        self.rootAlert1.title('Alerta!')        
        self.lblConfirm = Label(self.rootAlert1, text = f'Localizado um backup para o login "{self.login}"\nVocê gostaria de recuperar esse backup?', font=('arial', 10), bg='#C0C0C0',relief='groove')
        self.lblConfirm.place(relx=0.5, rely=0.25, anchor=CENTER)
        self.btnSim = Button(self.rootAlert1, width = '10', text = 'Sim', height='2', command = self.recuperaBkp)
        self.btnSim.place(relx=0.25, rely=0.55)
        self.btnNao = Button(self.rootAlert1, width = '10', text = 'Não', height='2', command = self.rootAlert1.destroy)
        self.btnNao.place(relx=0.55, rely=0.55)        

    def recuperaBkp(self):        
        self.rootAlert1.destroy()        
        t1 = threading.Thread(target=self.copiando)
        t1.start()      

    def fazerBkp(self):  
        t4 = threading.Thread(target=self.fazBkp)
        t4.start()

            
    def fim(self):
        self.progress['mode']='determinate'
        self.progress.stop()
        self.progress['value'] = 100
        self.lblFim['text']='Backup Finalizado'

    def sair(self):
        self.icon.stop()
        try:
           self.root.destroy
        except Exception as e:
           pass