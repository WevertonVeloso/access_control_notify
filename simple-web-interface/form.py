import streamlit as st
import mysql.connector as my
import time 

nome1 = " "
phone1 = " "
email1 = " "
def db_conn():
    conn = my.connect(
             host = os.getenv("HOST_DB"),
             user = os.getenv("USER_DB"),
             password = os.getenv("PASSWD_DB"),
             database = os.getenv("DATABASE")          
            )
    
    return conn
def cadastro():
    try:
     conn = db_conn()
     cursor = conn.cursor()
     cursor.execute( """
                     
               INSERT INTO usuarios(id, nome, telefone, email1) VALUES(%s, %s, %s, %s)
        """,(id_user, nome, phone, email))
     conn.commit()
     conn.close()
     mensagem = st.empty()
     mensagem.success("Cadastro realizado com sucesso!")
     time.sleep(1)
     mensagem.empty()
    except:
        msg = st.empty()
        msg.success("Error: ID existente!")
        time.sleep(1)
        msg.empty()
    finally:
        conn.close()

def remove(id_user):
    conn = db_conn()
    cursor = conn.cursor()
    cursor.execute("delete from usuarios where id = %s", (id_user,))
    conn.commit()
    with col1:
        mensagem = st.empty()
        mensagem.success("removido com sucesso!")
        time.sleep(1)
        mensagem.empty()

    conn.close()

tab1, tab2 = st.tabs(["Cadastro", "Atualizar Cadastro"])
with tab1:
    st.title("Cadastro de alunos")

    id_user = st.number_input("Digite ID:", min_value=1)
    nome = st.text_input("Digite o Nome:")
    phone = st.text_input("Digite o Telefone:", placeholder="+55999999999")
    email = st.text_input("Digite o Email:", placeholder="exemplo@exemplo.com")
    col1, col2 = st.columns([4, 0.8])
    with col1:
        if st.button("CADASTRAR"):
            cadastro()
            
    with col2:
      if st.button("REMOVER"):
        remove(id_user)

    alun = st.text_input("Encontrar Aluno")
    aluno = f"%{alun}%"
    conn = db_conn()
    cursor = conn.cursor()
    if aluno:
       cursor.execute("select id, nome, telefone, email1 from usuarios where nome like %s", (aluno,))
       table = cursor.fetchall()
       table.insert(0,("id", "nome", "telefone", "email"))
       st.table(table)
       conn.close()

with tab2:
    st.title("Atualizar cadastro")
    iduser = st.text_input("ID", placeholder="digite o id do usuario que deseja atualizar")
       
    if not iduser.isnumeric():
        mensagem = st.empty()
        mensagem.error("ID invalido!")
        time.sleep(2)
        mensagem.empty()
    else: 
        conn = db_conn()
        cursor = conn.cursor()
        if iduser:
            try: 
                 cursor.execute("select nome, telefone, email1 from usuarios where id = %s", (iduser,))
                 table = cursor.fetchall()
                 nome1 = table[0][0]
                 phone1 = table[0][1]
                 email1 = table[0][2]

                 nome = st.text_input("Nome", value=nome1)
                 telefone = st.text_input("Telefone", phone1)
                 email = st.text_input("Email", email1)

                 if st.button("ATUALIZAR"):
                     cursor.execute(" update usuarios set nome = %s, telefone = %s, email1 = %s where id = %s",(nome, telefone, email, iduser)) 
                     conn.commit()
                     st.success("Cadastro realizado com sucesso!"

            except:
                 mensagem = st.empty()
                 mensagem.warning("ID não encontrado!")
                 time.sleep(2)
                 mensagem.empty()
            finally:
                conn.close() 
