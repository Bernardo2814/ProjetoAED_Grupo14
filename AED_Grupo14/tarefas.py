# Biblioteca Tkinter: UI
from tkinter import *
from tkinter import messagebox
from tkinter import ttk          # extensão do tkinter, inclui treeview


fTarefas= "files/tarefas.txt"
fUserLogado = "files/userLogado.txt"

with open(fUserLogado, "r", encoding="utf-8") as f:
    userLogado = f.read().split(";")


#Funçao adicionar a tarefa, data, categoria e estado na treeview e no ficheiro
def adicionarTarefa(tarefa, data, categoria, estadoTarefa, tview):
    fileTarefas=open(fTarefas, "a", encoding="utf-8")
    fileTarefas.write(tarefa + ";" + data + ";" + categoria + ";" + estadoTarefa + ";" + userLogado[0] + "\n")
    fileTarefas.close()
    lista = lerTarefas()
    #filtrar só as tarefas do user logado
    lista = [x for x in lista if x.split(";")[4] == userLogado[0]]
    refreshListboxTarefas(lista, tview)


#Funçao remover a tarefa, data, categoria e estado da treeview e do ficheiro
def removerTarefa(tview):    
    tview.delete(tview.selection())

    fileTarefas=open(fTarefas, "w", encoding="utf-8")
    for line in tview.get_children():
           atividade = tview.item(line)["values"][0] + ";" + tview.item(line)["values"][1] + ";" + tview.item(line)["values"][2] + ";" + tview.item(line)["values"][3] + ";" + userLogado[0]
           fileTarefas.write(atividade)         # Guarda em ficheiro
    fileTarefas.close()

    lista = lerTarefas()
    #filtrar só as tarefas do user logado
    lista = [x for x in lista if x.split(";")[4] == userLogado[0]]

    refreshListboxTarefas(lista, tview)


#Funçao ler tarefas do ficheiro
def lerTarefas():
    fileTarefas=open(fTarefas, "r", encoding="utf-8")
    lista = fileTarefas.readlines()
    fileTarefas.close()
    return lista

#Funçao atualizar a treeview
def refreshListboxTarefas(lista, tview):
    with open(fUserLogado, "r", encoding="utf-8") as f:
        userLogado = f.read().split(";")
    tview.delete(*tview.get_children())
    with open(fTarefas, "r") as f:
      for line in f:
         pol = line.split(";")[4]
         if pol.strip() == userLogado[0].strip():
            #tview.insert("", "end", values = line.split(";")[0:4])
            tview.insert("", 0, values = line.split(";"))



#Funçao ordener as tarefas por ordem alfabetica
def ordenarTarefas(tview, opcao):
    if opcao == "Tarefa":
        lista = lerTarefas()
        lista.sort()
        refreshListboxTarefas(lista, tview)
    elif opcao == "Data":
        lista = lerTarefas()
        lista.sort(key=lambda x: x.split(";")[1])
        refreshListboxTarefas(lista, tview)
    elif opcao == "Categoria":
        lista = lerTarefas()
        lista.sort(key=lambda x: x.split(";")[2])
        refreshListboxTarefas(lista, tview)
    elif opcao == "Estado":
        lista = lerTarefas()
        lista.sort(key=lambda x: x.split(";")[3])
        refreshListboxTarefas(lista, tview)
    
def atualizarEstado(tview, opcao):
    if opcao == "Por Iniciar":
        tview.item(tview.selection(), values=(tview.item(tview.selection())["values"][0], tview.item(tview.selection())["values"][1], tview.item(tview.selection())["values"][2], "Por Iniciar"))
    elif opcao == "Em Progresso":
        tview.item(tview.selection(), values=(tview.item(tview.selection())["values"][0], tview.item(tview.selection())["values"][1], tview.item(tview.selection())["values"][2], "Em Progresso"))
    elif opcao == "Concluída":
        tview.item(tview.selection(), values=(tview.item(tview.selection())["values"][0], tview.item(tview.selection())["values"][1], tview.item(tview.selection())["values"][2], "Concluída"))

    fileTarefas=open(fTarefas, "w", encoding="utf-8")
    for line in tview.get_children():
           atividade = tview.item(line)["values"][0] + ";" + tview.item(line)["values"][1] + ";"+ tview.item(line)["values"][2] + ";" + tview.item(line)["values"][3] + ";" + userLogado[0]
           fileTarefas.write(atividade)         # Guarda em ficheiro
    fileTarefas.close()

    lista = lerTarefas()
    #filtrar só as tarefas do user logado
    lista = [x for x in lista if x.split(";")[4] == userLogado[0]]

    refreshListboxTarefas(lista, tview)



