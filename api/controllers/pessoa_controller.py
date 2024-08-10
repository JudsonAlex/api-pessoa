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

def validar_dados_pessoa(pessoa):
    try:
        # 1. Verifica se todos os campos obrigatórios estão presentes
        campos_obrigatorios = ['nome', 'datanascimento', 'salario', 'observacoes', 'nomemae', 'nomepai', 'cpf']
        for campo in campos_obrigatorios:
            if campo not in pessoa:
                raise ValueError(f"O campo {campo} é obrigatório.")

        # 2. Valida o tipo de cada campo
        nome = str(pessoa['nome']).strip()  # Remove espaços em excesso
        if not nome:
            raise ValueError("O nome não pode estar vazio.")

        datanascimento = datetime.strptime(pessoa['datanascimento'], '%d/%m/%Y').date()

        salario = float(pessoa['salario'])
        if salario < 0:
            raise ValueError("O salário deve ser um número positivo.")

        observacoes = str(pessoa['observacoes']).strip()
        nomemae = str(pessoa['nomemae']).strip()
        nomepai = str(pessoa['nomepai']).strip()
        cpf = str(pessoa['cpf']).strip()
        if len(cpf) != 11 or not cpf.isdigit():
            raise ValueError("O CPF deve ter 11 dígitos numéricos.")

        # 3. Retorna os dados tratados e validados
        return {
            'nome': nome,
            'datanascimento': datanascimento,
            'salario': salario,
            'observacoes': observacoes,
            'nomemae': nomemae,
            'nomepai': nomepai,
            'cpf': cpf
        }

    except KeyError as e:
        return {"error": str(e)}

    except Exception as e:
        return {"error": f"Erro inesperado: {str(e)}"}



@bp_pessoa.route('/', methods=['POST'])
def inserirPessoa():
    pessoa = request.json
    dados_tratados = validar_dados_pessoa(pessoa)

    if 'error' in dados_tratados:
        return jsonify(dados_tratados), 400

    # nome = str(pessoa['nome'])
    # datanascimento = datetime.strptime(pessoa['datanascimento'], '%d/%m/%Y').date()
    # salario = float(pessoa['salario'])
    # observacoes = str(pessoa['observacoes'])
    # nomemae = str(pessoa['nomemae'])
    # nomepai = str(pessoa['nomepai'])
    # cpf = str(pessoa['cpf'])
    # nome, datanascimento, salario, observacoes, nomemae, nomepai, cpf
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f'select * from inserir(row(%s, %s, %s, %s, %s, %s, %s))', (dados_tratados['nome'], dados_tratados['datanascimento'], dados_tratados['salario'],
            dados_tratados['observacoes'], dados_tratados['nomemae'], dados_tratados['nomepai'], dados_tratados['cpf']))
        
        resultado = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        print(resultado[0])
        return jsonify({"idPessoa":resultado[0]})
    except psycopg2.errors.UniqueViolation as e:
        return jsonify({"erro": str(e).split('\n')[0]}), 400


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
    cursor.close()
    conn.close()
    return data

@bp_pessoa.route('/<int:id>', methods=["GET"])
def listarUM(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
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
    except psycopg2.errors.RaiseException as e:
        print(e)
        return jsonify({"message": str(e).split('\n')[0]}), 404
    
    finally:
        cursor.close()
        conn.close()

@bp_pessoa.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('select * from deletar(%s)', (id,))
        resultado = cursor.fetchone()
        conn.commit()
        print(resultado[0])
        return jsonify({"message": resultado[0]})
    except psycopg2.errors.RaiseException as e:
        return jsonify({"message": str(e).split('\n')[0]}), 404
    
    finally:
        cursor.close()
        conn.close()


@bp_pessoa.route('/update/<int:idPessoa>', methods=["PUT"])
def atualizar(idPessoa):
    conn = get_db_connection()
    cursor = conn.cursor()

    pessoa = request.json
    dados_tratados = validar_dados_pessoa(pessoa)

    if 'error' in dados_tratados:
        return jsonify(dados_tratados), 400

    # nome = str(pessoa['nome'])
    # datanascimento = datetime.strptime(pessoa['datanascimento'], '%d/%m/%Y').date()
    # salario = float(pessoa['salario'])
    # observacoes = str(pessoa['observacoes'])
    # nomemae = str(pessoa['nomemae'])
    # nomepai = str(pessoa['nomepai'])
    # cpf = str(pessoa['cpf'])

    try:
        cursor.execute('select * from atualizar(row(%s, %s, %s, %s, %s, %s, %s, %s))' ,(idPessoa ,dados_tratados['nome'], dados_tratados['datanascimento'], dados_tratados['salario'],
         dados_tratados['observacoes'], dados_tratados['nomemae'], dados_tratados['nomepai'], dados_tratados['cpf']))
        resultado = cursor.fetchone()
        conn.commit()
        print(resultado[0])
        return jsonify({"message": resultado[0]})
    except psycopg2.Error as e:
        return jsonify({"message": str(e).split('\n')[0]}), 404
    finally:
        cursor.close()
        conn.close()


