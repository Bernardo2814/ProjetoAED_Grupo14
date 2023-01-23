# Biblioteca Tkinter: UI
from tkinter import *
from tkinter import ttk          # extensão do tkinter, inclui treeview
from tkinter import filedialog   # filedialog boxes
from PIL import ImageTk,Image    # Imagens .jpg ou .png
from tkinter import messagebox   #  messagebox
from tkinter.ttk import Combobox # combo

from utilizadores import *
from tarefas import *


fCategorias="files/categorias.txt"
fUsers="files/utilizadores.txt"
fUserslogin="files/userlogado.txt"


def containerCasa():
   #-- Painel com opções de menu
   panel2 = PanedWindow(window, width=750, height=450)
   panel2.place(x=250, y=50)
   #------------- Imagem de entrada da App
   ctnCanvas = Canvas(panel2, width = 750, height= 450)
   ctnCanvas.place(x=0, y= 0)
   global img
   img = PhotoImage(file = "imagens\\fundo1.png")
   ctnCanvas.create_image(750, 400, image = img)

def containerMenuAdmin():
   paneladmin = PanedWindow(window, width=750, height=450)
   paneladmin.place(x=250, y=100)
   """ Adicionar um titulo """
   lblTitulo = Label(paneladmin, text="Menu Administrador", font=("Arial", 20))
   lblTitulo.place(x=250, y=10)
   """ Adicionar uma label para escrever novas categorias """
   lblCategoria = Label(paneladmin, text="Nova Categoria:", font=("Arial", 12))
   lblCategoria.place(x=50, y=100)
   """ Adicionar uma caixa de texto para escrever novas categorias """
   txtCategoria = Entry(paneladmin, width=20)
   txtCategoria.place(x=200, y=100)  
   """ Adicionar um botao para adicionar esta categoria as categorias que estao no painel de gerir tarefas """
   btnAdicionar = Button(paneladmin, text="Adicionar", width=10, height=1, command=lambda: adicionarCategoria(txtCategoria))
   btnAdicionar.place(x=350, y=100)
   """ Adicionar uma label para remover categorias """
   lblCategoria = Label(paneladmin, text="Remover Categoria:", font=("Arial", 12))
   lblCategoria.place(x=50, y=150)
   """ Adicionar uma caixa de texto para escrever novas categorias """
   txtRemoveCategoria = Entry(paneladmin, width=20)
   txtRemoveCategoria.place(x=200, y=150)

   """ Adicionar um botao para remover esta categoria as categorias que estao no painel de gerir tarefas """
   btnRemover = Button(paneladmin, text="Remover", width=10, height=1, command=lambda: removerCategoria(txtRemoveCategoria))
   btnRemover.place(x=350, y=150)

   
def removerCategoria(txtCategoria):
   """ Remover uma categoria do ficheiro de categorias """
   categoriaARemover = txtCategoria.get()
   if categoriaARemover != "":
      f = open(fCategorias, "r")
      categorias = f.readlines()
      f.close()
      f = open(fCategorias, "w")
      for categoria in categorias:
         if categoria.strip() != categoriaARemover:
            f.write(categoria)
      f.close()
      messagebox.showinfo("Sucesso", "Categoria removida com sucesso")
   else:
      messagebox.showerror("Erro", "Categoria inválida")


def adicionarCategoria(txtCategoria):
   """ Adicionar uma nova categoria ao ficheiro de categorias """
   novaCategoria = txtCategoria.get()
   if novaCategoria != "":
      f = open(fCategorias, "a")
      f.write("\n" + novaCategoria)
      f.close()
      messagebox.showinfo("Sucesso", "Categoria adicionada com sucesso")
   else:
      messagebox.showerror("Erro", "Categoria inválida")


def verificarAdmin ():
   with open(fUserslogin, "r") as f:
      linha = f.readline()
      tipo = linha.split(";")[1][:-1]
      if tipo == "admin":
         containerMenuAdmin()
      else:
         messagebox.showerror("Erro", "Não tem permissões para aceder a esta área")

def logOut():
   global userAutenticado
   userAutenticado.set("")
   btnLogin.config(text = "Login", command=panelAutenticarUser)
   with open(fUserLogado, "w") as f:
      f.write("")


def validaConta(userName, userPass, panelUsers):
    """
    Validar cautenticação com uma conta
    """
    fileUsers=open(fUsers, "r", encoding="utf-8")
    listaUsers = fileUsers.readlines()
    fileUsers.close()
    for linha in listaUsers:
        if linha.split(";")[0] == userName and linha.split(";")[1] == userPass:
            msg = "Bem-Vindo " + userName
            messagebox.showinfo("Login feito com sucesso!", msg)
            btnLogin.config(text="Logout", command=logOut)
            with open(fUserslogin, "w") as file:
                linha = userName + ";" + linha.split(";")[2]
                file.write(linha)
            panelUsers.place_forget()
            return msg
    messagebox.showerror("Erro!", "O UserName ou a Password estão incorretos!")
    panelUsers.place_forget()
    return ""


def panelAutenticarUser():

   if userAutenticado.get() != "":     # SE JÁ EXISTE um user autenticado, a ideia é terminar sessão
        userAutenticado.set("")
        btnLogin.config(text = "Login")
        return
   panelUsers = PanedWindow(window, width = 550, height = 300, relief = "sunken")
   panelUsers.place(x=370, y=100)    # 450, 50
 
# Imagem
   containerImage = Canvas(panelUsers, height = 128, width=128)
   containerImage.place(x=50, y=70) 
   img = PhotoImage(file = "imagens\\entrar1.png")
   containerImage.create_image(64, 64, image = img)
  # Username
   labelUsers = Label(panelUsers, text ="Username:")
   labelUsers.place(x=200, y= 100)
   userName = StringVar()
   txtUser = Entry(panelUsers, width=20, textvariable=userName)
   txtUser.place(x=280, y= 100)
#Password
   labelPass = Label(panelUsers, text ="Password:")
   labelPass.place(x=200, y= 150)
   userPass = StringVar()
   txtPass = Entry(panelUsers, width=20, textvariable = userPass, show = "*")
   txtPass.place(x=280, y= 150)

   btnValidar= Button(panelUsers, text = "Validar Conta", width=25, height=3,
                      command = lambda: validaConta(userName.get(), userPass.get(), panelUsers))
   btnValidar.place(x=260, y= 200) 
   

def autenticarUser(userName, userPass, panelUsers):
   global userAutenticado
   userAutenticado.set(validaConta(userName, userPass))
   if userAutenticado.get() != "":
      btnLogin.config(text = "Terminar Sessão", command=logOut)
      panelUsers.place_forget()
      containerCasa()
      containerGerirTarefas()
   else:
      messagebox.showerror("Erro", "Username ou Password inválidos")


def panelCriarConta():

   panelUsers = PanedWindow(window, width = 550, height = 300, relief = "sunken")
   panelUsers.place(x=370, y=100)
   # Imagem
   containerImage = Canvas(panelUsers, height = 128, width=128)
   containerImage.place(x=50, y=70) 
   img = PhotoImage(file = "imagens\\criar_conta1.png")
   containerImage.create_image(64, 64, image = img)
# Username
   labelUsers = Label(panelUsers, text ="Username:")
   labelUsers.place(x=200, y= 50)
   userName = StringVar()
   txtUser = Entry(panelUsers, width=20, textvariable=userName)
   txtUser.place(x=280, y= 50)
#Password
   labelPass = Label(panelUsers, text ="Password:")
   labelPass.place(x=200, y= 100)
   userPass = StringVar()
   txtPass = Entry(panelUsers, width=20, textvariable = userPass, show = "*")
   txtPass.place(x=280, y= 100)
#Confirmar password
   labelPass = Label(panelUsers, text ="Confirmar \nPassword:")
   labelPass.place(x=200, y= 150)
   userPassConfirm = StringVar()
   txtPass = Entry(panelUsers, width=20, textvariable = userPassConfirm, show = "*")
   txtPass.place(x=280, y= 150)

   btnValidar= Button(panelUsers, text = "Criar Conta", width=25, height=3,
                      command = lambda: criaConta(userName.get(), userPass.get(), userPassConfirm.get(), panelUsers))
   btnValidar.place(x=260, y= 200) 


def containerGerirTarefas():
    panelTarefas = PanedWindow(window, width = 750, height= 450)
    panelTarefas.place(x=250, y= 50)

    lblTarefa = Label(panelTarefas, text = "Tarefa :")
    lblTarefa.place(x=30, y=70)

    tarefa = StringVar()
    entryTarefa = Entry(panelTarefas, width=25, textvariable=tarefa)
    entryTarefa.place(x=80, y= 70) 

    lblData = Label(panelTarefas, text = "Data :")
    lblData.place(x=30, y=120)

    data = StringVar()
    entryData = Entry(panelTarefas, width=25, textvariable=data)
    entryData.place(x=80, y= 120) 

    lblCategoria = Label(panelTarefas, text = "Categoria :")
    lblCategoria.place(x=30, y=170)

    #Combobox
    
    categoria=StringVar()
    categorias = []
    with open(fCategorias, "r") as f:
        for line in f:
            categorias.append(line.strip())
    categoria.set(categorias[0])

    cbCategorias = ttk.Combobox(panelTarefas, values=categorias, width=20)
    cbCategorias.current(0)
    cbCategorias.pack()
    cbCategorias.place(x=100, y=170)

    #Estado das tarefas
    lblEstado= Label(panelTarefas, text = "Estado :")
    lblEstado.place(x=30, y=220)

    estadoTarefa = StringVar()
    estadoTarefa.set("Por Iniciar")
    rd1 = Radiobutton(panelTarefas, text = "Por Iniciar", value = "Por Iniciar", variable= estadoTarefa)
    rd2 = Radiobutton(panelTarefas, text = "Em Progresso", value = "Em Progresso", variable= estadoTarefa)
    rd3 = Radiobutton(panelTarefas, text = "Concluída", value = "Concluída", variable= estadoTarefa)
    rd1.place(x= 90, y= 220)
    rd2.place(x= 90, y= 250)
    rd3.place(x= 90, y= 280)


    #Ordenar tarefas
    lblOrdenar= Label(panelTarefas, text = "Ordenar :")
    lblOrdenar.place(x=30, y=320)

    ordenarRadio = StringVar()
    ordenarRadio.set("Tarefa")
    rd4 = Radiobutton(panelTarefas, text = "Tarefa", value = "Tarefa", variable= ordenarRadio)
    rd5 = Radiobutton(panelTarefas, text = "Data", value = "Data", variable= ordenarRadio)
    rd6 = Radiobutton(panelTarefas, text = "Categoria", value = "Categoria", variable= ordenarRadio)
    rd7 = Radiobutton(panelTarefas, text = "Estado", value = "Estado", variable= ordenarRadio)
    rd4.place(x= 90, y= 320)
    rd5.place(x= 90, y= 350)
    rd6.place(x= 90, y= 380)
    rd7.place(x= 90, y= 410)


    tview = ttk.Treeview(panelTarefas, height=10,  selectmode= "browse", 
            columns = ("Tarefa", "Data", "Categoria", "Estado"), show = "headings")
    
    tview.column("Tarefa", width = 100,   anchor="c")
    tview.column("Data", width = 100,  anchor="c")          # c- center
    tview.column("Categoria", width = 100,   anchor="c")
    tview.column("Estado", width = 140,   anchor="c")
    tview.heading("Tarefa", text = "Tarefa")
    tview.heading("Data", text = "Data")
    tview.heading("Categoria", text = "Categoria")
    tview.heading("Estado", text = "Estado")
    tview.place(x=280, y=70)
    #preencher a treeview com as tarefas do userLogado
    with open(fUserLogado, "r") as f:
         userLogado = f.read().split(";")
    tview.delete(*tview.get_children())
    try:
      with open(fTarefas, "r") as f:
         for line in f:
            pol = line.split(";")[4]
            if pol.strip() == userLogado[0].strip():
               tview.insert("", "end", values = line.split(";")[0:4])
    except:
         pass
    

    btnAdicionar = Button(panelTarefas, width=15, height=3, text = "Adicionar Tarefa", compound=LEFT,
                  command= lambda: adicionarTarefa(tarefa.get(), data.get(), categoria.get(), estadoTarefa.get(), tview))
    btnAdicionar.place(x=470, y= 312)

    btnApagar = Button(panelTarefas, width=15, height=3, text = "Apagar Tarefa", compound=LEFT,
                command= lambda: removerTarefa(tview))
    btnApagar.place(x=608, y= 312)

    btnOrdenar = Button(panelTarefas, width=15, height=3, text = "Ordenar Tarefas", compound=LEFT,
                command= lambda: ordenarTarefas(tview, ordenarRadio.get()))
    btnOrdenar.place(x=280, y= 385)

    btnAtualizar = Button(panelTarefas, width=15, height=3, text = "Atualizar Estado", compound=LEFT,
                  command= lambda: atualizarEstado(tview, estadoTarefa.get()))
    btnAtualizar.place(x=280, y= 312)



window = Tk()
screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()
appWidth = 1000                             # tamanho (pixeis) da window a criar 900 / 500
appHeight = 500 
#Posiçao de baixo da window
#Retangular
x = (screenWidth/2) - (appWidth/2)
y = (screenHeight/2) - (appHeight/2)
window.geometry("{:.0f}x{:.0f}+{:.0f}+{:.0f}" .format(appWidth, appHeight, int(x), int(y)))
window.title('To Do List App')

#-- Painel com opções de menu
panel1 = PanedWindow(window, bg = "light green", width=250, height=500)
panel1.place(x=0, y=0)

imageCasa = PhotoImage(file = "imagens\\casa1.png" )
btnCasa = Button(panel1, text = "Início", compound=LEFT, relief = "sunken", 
                    width = 230, height = 68, font="calibri, 11",
                    command=containerCasa)
btnCasa.place (x=5, y=50)
btnCasa.config(image=imageCasa)

imageGerir = PhotoImage(file = "imagens\\gerir_tarefas1.png" )
btnGerir = Button(panel1, text = "Gerir \nTarefas", compound=LEFT, relief = "sunken", 
                    width = 230, height = 68, font="calibri, 11",
                    command=containerGerirTarefas)
btnGerir.place (x=5, y=130)
btnGerir.config(image=imageGerir)



btnAdmin= Button(panel1, text = "Menu Admin", compound=LEFT, relief = "sunken",
                     width = 230, height = 68, font="calibri, 11", command=verificarAdmin)
btnAdmin.place (x=5, y=210)
btnAdmin.config(image=imageGerir)








imageSair = PhotoImage(file = "imagens\\sair1.png" )
btnSair = Button(panel1, text = "Sair \nda App", relief = "sunken", compound=LEFT,
                width = 230, height = 68,  font="calibri, 11", 
                command = window.destroy)
btnSair.place (x=5, y=370)
btnSair.config(image=imageSair)


#Painel do profile apos o user estar autenticado com foto de perfil, nome, e total de tarefas
def panelPerfilUser():
      panelPerfil = PanedWindow(window, bg = "gray", width=250, height=500)
      panelPerfil.place(x=0, y=0)

      imagePerfil = PhotoImage(file = "imagens\\profile1.png" )
      btnPerfil = Button(panelPerfil, text = "Perfil", compound=LEFT, relief = "sunken", 
                        width = 230, height = 68, font="calibri, 11",
                        command=containerPerfil)
      btnPerfil.place (x=5, y=300)
      btnPerfil.config(image=imagePerfil)

      imageSair = PhotoImage(file = "imagens\\sair1.png" )
      btnSair = Button(panelPerfil, text = "Sair \nda App", relief = "sunken", compound=LEFT,
                    width = 230, height = 68,  font="calibri, 11", command = window.destroy)
      btnSair.place (x=5, y=370)
      btnSair.config(image=imageSair)


#Container perfil com foto de perfi, nome, numero total de tarefas
def containerPerfil():

      panelPerfil = PanedWindow(window, bg = "gray", width=250, height=500)
      panelPerfil.place(x=0, y=0)

      imagePerfil = PhotoImage(file = "imagens\\profile1.png" )
      btnPerfil = Button(panelPerfil, text = "Perfil", compound=LEFT, relief = "sunken", 
                        width = 230, height = 68, font="calibri, 11",
                        command=containerPerfil)
      btnPerfil.place (x=5, y=300)
      btnPerfil.config(image=imagePerfil)

      imageSair = PhotoImage(file = "imagens\\sair1.png" )
      btnSair = Button(panelPerfil, text = "Sair \nda App", relief = "sunken", compound=LEFT,
                    width = 230, height = 68,  font="calibri, 11", command = window.destroy)
      btnSair.place (x=5, y=370)
      btnSair.config(image=imageSair)


# ------------- HEADER
global userAutenticado
userAutenticado = StringVar()
userAutenticado.set("")
labelHeader = Label(window, textvariable= userAutenticado, fg = "blue", font="calibri, 11")
labelHeader.place(x= 400, y= 10)


global btnLogin
imageLogin = PhotoImage(file = "imagens\\entrar1.png" )
btnLogin = Button (window, relief = "flat",  compound=TOP,
                     width = 78, height=38, text = "Login",command = panelAutenticarUser) 
btnLogin.place(x=790, y=5)
btnLogin.config(image=imageLogin)

global btnCriarConta
imageCriarConta = PhotoImage(file = "imagens\\criar_conta1.png" )
btnCriarConta = Button (window, relief = "flat",  compound=TOP,
                     width = 78, height=38, text = "Criar Conta", command = panelCriarConta)
btnCriarConta.place(x=870, y=5)
btnCriarConta.config(image=imageCriarConta)


containerCasa()


window.mainloop()





