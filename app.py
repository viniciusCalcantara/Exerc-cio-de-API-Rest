from flask import Flask, jsonify, request
import json

app = Flask(__name__)

STATUS = ["nao iniciada", "em andamento", "finalizada"]
tarefas = [
    {
        "id" : 0,
        "status" : STATUS[0],
        "responsavel" : "rebeca",
        "tarefa" : "fazer as migrations"
    },
    {
        "id" : 1,
        "status" : STATUS[1],
        "tarefa" : "resolver o problema da automação do publish",
        "responsavel" : "filipe"
    },
    {
        "id" : 2,
        "responsavel" : "davi",
        "tarefa" : "criar projetos de aprendizado para a turma 2 do Edge Academy",
        "status" : STATUS[1]
    }
]

@app.route("/")
def index():
    return "Index page"

@app.get("/tarefas")
def listar_tarefas():
    
    response = {
        "status" : "falha",
        "mensagem" : "algum erro ocorreu"
    }

    try:
        response["tarefas"] = tarefas
        if len(tarefas) == 0:
            raise Exception
        
        response["status"] = "sucesso"
        response["mensagem"] = "tarefas retornadas com sucesso"
    except Exception:
        response["mensagem"] = "não há nenhuma tarefa"

    return response
    
       
@app.post("/tarefas")
def adicionar_nova_tarefa():

    response = {
        "status" : "falha",
        "mensagem" : "algum erro ocorreu"
    }

    try:
        tamanho_antigo = len(tarefas)
        task = json.loads(request.data)
        tarefas.append(task)
        tamanho_novo = len(tarefas)

        if (tamanho_antigo != tamanho_novo - 1):
            raise Exception 
    
    except Exception:
        response["mensagem"] = "Algo deu errado e a tarefa não foi incluída"
    else:
        response["status"] = "sucesso"
        response["mensagem"] = "Tarefa adicionada com sucesso"
        response["tarefa_adicionada"] = task
    
    return response


@app.get("/tarefas/<int:id>")
def consultar_tarefa(id):

    response = {
        "status" : "falha",
        "mensagem" : "algum erro aconteceu"
    }
    
    print("entrou")
    try:
        find_task = False
        target_task = {}
        for task in tarefas:
            if task["id"] == id:
                find_task = True
                target_task = task
        if find_task == False:
            raise Exception
    except Exception:
        response["mensagem"] = "tarefa não encontrada"
    else:
        response["status"] = "sucesso"
        response["mensagem"] = f"Tarefa {id} encontrada"
        response["tarefa_buscada"] = target_task

    return response

@app.put("/tarefas/<int:id>")
def alterar_status(id):

    response = {
        "status" : "falha",
        "mensagem" : "algum erro aconteceu"
    }

    try:
        find_task = False
        for task in tarefas:
            if task["id"] == id:
                find_task = True
                task["status"] = json.loads(request.data)["status"]
                response["estado_final_da_tarefa"] = task

        if find_task == False:
            raise Exception
    
    except Exception:
        response["mensagem"] = "tarefa não encontrada"
    
    else:        
        response["status"] = "sucesso"
        response["mensagem"] = f"status da tarefa {id} atualizado"

    return response

@app.delete("/tarefas/<int:id>")
def deletar_tarefa(id):

    response = {
        "status" : "falha",
        "mensagem" : "algum erro aconteceu"
    }

    try:
        find_task = False
        pos = 0
        for task in tarefas:
            if task["id"] == id:
                find_task = True
                tarefas.pop(pos)
                response["tarefa_excluida"] = task
            pos = pos + 1

        if find_task == False:
            raise Exception
    
    except Exception:
        response["mensagem"] = "tarefa não encontrada"
    
    else:        
        response["status"] = "sucesso"
        response["mensagem"] = f"status da tarefa {id} atualizado"

    return response



    






