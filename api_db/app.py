from flask import Flask, request, jsonify
import mysql.connector as mysql

def con_db():
    conn = mysql.connect(
            host = "127.0.0.1",
            user = "ever",
            password = "1234",
            database = "cadastro"
            )
    cursor = conn.cursor()
    return conn

app = Flask(__name__)

@app.route("/cadastro", methods=["POST"])
def cadastro():
    data = request.get_json()
    
    if "name" not in data or "id" not in data or "email" not in data:
        return jsonify({"error" : "url invalida! Url deve conter os parametros: id, name e email"}), 400
    else:
        name = data.get("name")
        id_user = data.get("id") 
        email = data.get("email")
        phone = data.get("tel", "+5599999999")
        if "@" not in email:
            return jsonify({"error": "email invalido"}), 400
        if not phone.startswith("+55"):
            return jsonify({"error": "telefone tem que seguir o formato: +5531999999999"}), 400
        try:
            conn = con_db()
            cursor = conn.cursor()
            cursor.execute("insert into usuarios(id, nome, telefone, email1) values(%s, %s, %s, %s)", (id_user, name, phone, email))
            conn.commit()
            conn.close()
            return jsonify({"message": "cadastro realizado com sucesso!"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        finally:
            cursor.close()
            conn.close()

@app.route("/list", methods=["GET"])
def list_db():
    conn = con_db()
    cursor = conn.cursor()
    cursor.execute("select * from usuarios")
    data = cursor.fetchall()
    conn.close()
    return jsonify({"usuarios" : data}), 200

@app.route("/delete", methods=["GET"])
def delete():
    id_user = request.args.get("id")
    if not id_user.isdigit():
        return jsonify({"error": "id invalido"}), 400

    try:
        conn = con_db()
        cursor = conn.cursor()
        cursor.execute("delete from usuarios where id = %s",(id_user,))
        conn.commit()
        return jsonify({"message": "usuario removido"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)




