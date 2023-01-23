# Biblioteca Tkinter: UI
from tkinter import *
from tkinter import messagebox

from main import *

# Funções relacionadas com o User
fUsers= "files/utilizadores.txt"
fUserslogin= "files/userlogado.txt"

global userLogado



def criaConta(userName, userPass, userPassConfirm, panelUsers):
    """
    Criar uma nova conta
    """
    if userPass != userPassConfirm:
        messagebox.showerror("Erro!", "A password difere do inserido na sua confirmação!")
        return  
    if userName == "" or userPass == "":
        messagebox.showerror("Erro!", "O username e a password não podem ser vazios!")
        return         
    fileUsers=open(fUsers, "r", encoding="utf-8")
    listaUsers = fileUsers.readlines()
    fileUsers.close()
    for linha in listaUsers:
        fields = linha.split(";")
        if fields[0] == userName:
            messagebox.showerror("Erro!", "Já existe um utilizador com esse username!")
            return 
    fileUsers = open(fUsers, "a")
    linha = userName + ";" + userPass + ";user\n"
    fileUsers.write(linha)
    fileUsers.close()
    messagebox.showinfo("Conta criada!", "Conta criada com sucesso!")
    panelUsers.place_forget()
