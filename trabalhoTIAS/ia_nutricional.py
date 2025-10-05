import json
from google import genai
from dotenv import load_dotenv
import os

load_dotenv("C:/Users/user/Desktop/Tecnologias-Inteligentes-Aplicadas-a-Saude/trabalhoTIAS/.env")
api_key = os.getenv("COLOQUE_SUA_API_KEY_AQUI")
print("Chave carregada!" if api_key else "Chave não encontrada!")

'''
------------------------------
Cliente 
------------------------------
'''
client = genai.Client(api_key="COLOQUE_SUA_API_KEY_AQUI")

'''
------------------------------
Função para montar JSON
------------------------------
'''
def montar_json(medicamentos, bolus_alimentar, bolus_correcao, glicemia_atual, descricao_alimentacao):
    return {
        "medicamentos": medicamentos,
        "bolus_alimentar": bolus_alimentar,
        "bolus_correcao": bolus_correcao,
        "glicemia_atual": glicemia_atual,
        "descricao_alimentacao": descricao_alimentacao
    }

'''
------------------------------
Função para desmontar JSON ajustada para resposta da IA
------------------------------
'''
def desmontar_json(resposta_json):
    """
    Ajustada para lidar com:
    - JSON com 'nome_do_alimento' como lista ou string
    - Remover backticks e espaços extras
    """
    try:
        # remove backticks e palavra "json"
        resposta_json = resposta_json.replace("```json", "").replace("```", "").strip()
        
        data = json.loads(resposta_json)
        
        # caso nome_do_alimento exista
        if "nome_do_alimento" in data:
            nome = data["nome_do_alimento"]
            # se for lista, mantém, e se for string, transforma ela em lista
            if isinstance(nome, list):
                alimentos = nome
            else:
                # divide a string por vírgula e remove espaços extras
                alimentos = [x.strip() for x in nome.split(",")]
            
            calorias = data.get("quantidade_de_caloria", 0)
            carboidratos = data.get("quantidade_de_carboidrato", 0)
            insulina = data.get("quantidade_de_insulina_necessaria", 0)
        else:
            # formato antigo com lista de alimentos
            alimentos = [item["nome"] for item in data.get("alimentos", [])]
            calorias = sum(item.get("calorias", 0) for item in data.get("alimentos", []))
            carboidratos = sum(item.get("carboidratos", 0) for item in data.get("alimentos", []))
            insulina = data.get("insulina_necessaria", 0)
            
        return alimentos, calorias, carboidratos, insulina
    
    except Exception as e:
        print("Erro ao desmontar JSON:", e)
        return [], 0, 0, 0



'''
------------------------------
Variáveis de entrada
------------------------------
'''
medicamentos = ['novorapid', 'basaglar']
bolus_alimentar = 15  # 15g de carboidrato por 1 unidade de insulina
bolus_correcao = 60   # 60mg/dL por 1 unidade de insulina
glicemia_atual = 132

descricao_alimentacao = """
hoje de manhã comi um pão com uma maionese, e mais um ovo frito. 
"""

# montando JSON
contexto_json = montar_json(medicamentos, bolus_alimentar, bolus_correcao, glicemia_atual, descricao_alimentacao)

'''
------------------------------
Papel IA e instruções
------------------------------
'''
papel_esperado_ia = """
Você é nutricionista especializada em contagem de carboidratos, calorias e cálculo da insulina necessária
com base na alimentação e nos níveis de glicose informados.
"""

resposta_instrucao = """
Você deve retornar SOMENTE um JSON com:
- nome do alimento
- quantidade de carboidrato
- quantidade de caloria
- glicemia enviada
- quantidade de insulina necessária
"""

prompt = f"""
Papel:
{papel_esperado_ia}

Contexto:
{json.dumps(contexto_json, indent=2, ensure_ascii=False)}

Resposta:
{resposta_instrucao}
"""

'''
------------------------------
Chamando Gemini
------------------------------
'''
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

resposta_json = response.candidates[0].content.parts[0].text.strip()

'''
------------------------------
Estimativa de tokens
------------------------------
'''
palavras = prompt.split() + resposta_json.split()
tokens_estimados = int(len(palavras) * 1.33)
print(f"Tokens estimados: {tokens_estimados}")

print("Resposta JSON bruta da IA:\n", resposta_json)

'''
------------------------------
Processamento da resposta
------------------------------
'''
lista_alimentos, calorias, carboidratos, qtd_insulina = desmontar_json(resposta_json)

'''
------------------------------
Resultado final
------------------------------
'''
print("\nLista de alimentos:", lista_alimentos)
print("Total de calorias:", calorias)
print("Total de carboidratos:", carboidratos)
print("Quantidade de insulina necessária:", qtd_insulina)
