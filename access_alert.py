import os
import time
import requests as r
from requests.auth import HTTPDigestAuth
import mysql.connector as mysql

conn = mysql.connect(
         
             host = os.getenv("HOST_DB"),
             user = os.getenv("USER_DB"),
             password = os.getenv("PASSWD_DB"),
             database = os.getenv("DATABASE")
             
             ) 

create_table = """
CREATE TABLE IF NOT EXISTS usuarios (
id INT PRIMARY KEY,
nome VARCHAR(100) NOT NULL,
telefone VARCHAR(16),
email1 VARCHAR(100) NOT NULL
);
"""
cursor = conn.cursor()
cursor.execute(create_table)

conn.close()

#função retorna o id do ultimo acesso liberado
def get_id(url, params, user_api, passwd_api):

    response = r.get(url,params=params, auth=HTTPDigestAuth(user_api,passwd_api))
    resposta = response.text.split()
    last_id = ""
    for i in resposta:
        
        if "UserID" in i:
            last_id = (i.split("=")[-1])

    return  last_id

#função que recebe o valor armazenado no arquivo idprevio
def get_last_id():
    
    try:
        with open("idprevio","x") as file:
            pass
    except FileExistsError:
        pass

    with open("idprevio","r") as file:
        id_previo = file.read()
    return id_previo    

#função que retorna o usuario do Database com base no id de acesso
def get_user_db(get_id, get_last_id):
    
    user_db = "0"
    if get_id != get_last_id and get_id != "":# veifica se o id não é igual ao anterior para não fazer consultas duplicadas
        with open("idprevio","w") as file: # atualiza o id armazenado no arquivo idprevio
            file.write(get_id)
    
        conn = mysql.connect(
         
             host= os.getenv("HOST_DB"),
             user= os.getenv("USER_DB"),
             password= os.getenv("PASSWD_DB"),
             database= os.getenv("DATABASE")
             
             ) 

        cursor = conn.cursor()
        cursor.execute("select id, nome, telefone, email1 from usuarios where id = %s",(get_id,))

        user_db = cursor.fetchall() 
        conn.close()
    return user_db

def send_data(user_db, url_aws):
   """ função responsável pelo envio dos dados do usuario para a aws """
   if user_db != "0": 
        data = user_db[0]
        id_user = data[0]
        name = data[1]
        phone = data[2]
        email = data[3]
        date = time.ctime()
        data_json = { "nome": name,
                      "id" : id_user,
                      "telefone" : phone,
                      "email" : email,
                      "data" : date
                     }

        send = r.post(url_aws, json=data_json)
    
        if send.status_code == 200:
             print("Dados enviados com sucesso:", send.json())
        else:
             print(f"Erro ao enviar dados: {send.status_code}, {send.text}")

         
def main():
    while True:
        StartTime = int(time.time() - 200000) #tempo inicial da consulta  
        EndTime = int(time.time() + 200000) #tempo final da consulta
        user_api = os.getenv("USER_API") 
        passwd_api = os.getenv("PASSWD_API")
        params = {
                "action" : "find",
                "name" : "AccessControlCardRec",
                "StartTime" : StartTime,   
                "EndTime" :  EndTime
                }
        #url do controlador de acesso intelbras
        url = os.getenv("URL_CONTROLADOR") #"http://192.168.1.123:80/cgi-bin/recordFinder.cgi"
        #url do api_gateway aws
        url_aws = os.getenv("URL_AWS")
     
        id_access = get_id(url, params, user_api, passwd_api)
        id_previo =  get_last_id() 
        user_db = get_user_db(id_access, id_previo)
        send_data(user_db, url_aws)
        time.sleep(2)

 if __name__ == "__main__":
     main()
      
