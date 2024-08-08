from flask import Blueprint, request, jsonify, make_response
from dotenv import load_dotenv
from config import DB_HOST, DB_NAME, DB_PASS,DB_PORT,DB_USER # dados coletados de .env
import psycopg2
from datetime import datetime

load_dotenv()

bp_pessoa = Blueprint('pessoa',__name__)


def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT
    )
    return conn


@bp_pessoa.route('/', methods=['POST'])
def inserirPessoa():
    pessoa = request.json

    nome = str(pessoa['nome'])
    datanascimento = datetime.strptime(pessoa['data'], '%d/%m/%Y').date()
    salario = float(pessoa['salario'])
    observacoes = str(pessoa['obs'])
    nomemae = str(pessoa['nomemae'])
    nomepai = str(pessoa['nomepai'])
    cpf = str(pessoa['cpf'])
    

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f'select * from inserir(row(%s, %s, %s, %s, %s, %s, %s))', (nome, datanascimento, salario, observacoes, nomemae, nomepai, cpf))
    resultado = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    print(resultado[0])
    return jsonify(resultado[0])


@bp_pessoa.route('/', methods=["GET"])
def listarTodos():
    lista_pessoas = []
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('select * from listar()')
    resultado = cursor.fetchall()
    if resultado:
        for pessoa in resultado:
            obj ={
                'idPessoa': pessoa[0],
                'nome': pessoa[1],
                'datanascimento': pessoa[2],
                'salario': pessoa[3],
                'observacoes': pessoa[4],
                'nomemae': pessoa[5],
                'nomepai': pessoa[6],
                'cpf': pessoa[7]
            }
            lista_pessoas.append(obj)
    data = jsonify(lista_pessoas)
    print(data)
    return data

@bp_pessoa.route('/<int:id>', methods=["GET"])
def listarUM(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f'select * from listarum({id})')
    resultado = cursor.fetchone()
    obj ={
                'idPessoa': resultado[0],
                'nome': resultado[1],
                'datanascimento': resultado[2],
                'salario': resultado[3],
                'observacoes': resultado[4],
                'nomemae': resultado[5],
                'nomepai': resultado[6],
                'cpf': resultado[7]
            }
    print(obj)
    return jsonify(obj)

@bp_pessoa.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('select * from deletar(%s)', (id,))
    resultado = cursor.fetchone()
    conn.commit()
    print(resultado[0])
    return jsonify(resultado[0])

@bp_pessoa.route('/update/<int:idPessoa>', methods=["PUT"])
def atualizar(idPessoa):
    conn = get_db_connection()
    cursor = conn.cursor()

    pessoa = request.json

    nome = str(pessoa['nome'])
    datanascimento = datetime.strptime(pessoa['data'], '%d/%m/%Y').date()
    salario = float(pessoa['salario'])
    observacoes = str(pessoa['obs'])
    nomemae = str(pessoa['nomemae'])
    nomepai = str(pessoa['nomepai'])
    cpf = str(pessoa['cpf'])

    try:
        cursor.execute('select * from atualizar(row(%s, %s, %s, %s, %s, %s, %s, %s))' ,(int(idPessoa), nome, datanascimento, salario, observacoes, nomemae, nomepai, cpf))
        resultado = cursor.fetchone()
        conn.commit()
        print(resultado[0])
        return jsonify(resultado[0])
    except psycopg2.errors as e:
        return e
    finally:
        cursor.close()
        conn.close()


