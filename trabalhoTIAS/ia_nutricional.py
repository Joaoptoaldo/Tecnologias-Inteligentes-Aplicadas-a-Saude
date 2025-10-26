import os
import re
import json
from dotenv import load_dotenv
from google import genai

# Carrega .env (opcional: passe o caminho completo se necessário)
# Ex: load_dotenv(r"C:\Users\user\Desktop\...\ .env")
load_dotenv()  # chama sem argumento tenta carregar .env do diretório atual

# Tente múltiplos nomes comuns para a variável de ambiente
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("COLOQUE_SUA_API_KEY_AQUI")
if api_key:
    print("Chave carregada!")
else:
    raise RuntimeError("Chave não encontrada! Defina GEMINI_API_KEY ou COLOQUE_SUA_API_KEY_AQUI no .env ou nas variáveis de ambiente.")

# Inicializa o client
client = genai.Client(api_key=api_key)

def montar_json(medicamentos, bolus_alimentar, bolus_correcao, glicemia_atual, descricao_alimentacao):
    dados = {
        "medicamentos": medicamentos,
        "parametros_insulina": {
            "bolus_alimentar": {"carb_por_unidade_g": int(bolus_alimentar)},
            "bolus_correcao": {"mg_dl_por_unidade": int(bolus_correcao)}
        },
        "medicoes": {
            "glicemia_atual_mg_dl": int(glicemia_atual)
        },
        "alimentacao": {
            "descricao": descricao_alimentacao.strip()
        },
        "instrucoes": "Responda apenas com JSON válido. Veja o schema em exemplo_json."
    }
    return json.dumps(dados, ensure_ascii=False, indent=2)

exemplo_json = {
    "alimentos": [
        {
            "nome_do_alimento": "pão francês",
            "quantidade_de_carboidrato_g": 30,
            "quantidade_de_caloria_kcal": 150,
            "quantidade_de_glicemia_enviada_mg_dl": 0,
            "quantidade_de_insulina_necessaria_u": 2
        }
    ],
    "resumo": {
        "carboidratos_totais_g": 30,
        "calorias_totais_kcal": 150,
        "insulina_total_necessaria_u": 2
    }
}

def limpar_json_da_ia(texto):
    texto = texto.strip()
    # Remove blocos de código ``` ou ```json
    texto = re.sub(r"^```(?:json)?\s*", "", texto, flags=re.I)
    texto = re.sub(r"\s*```$", "", texto)
    # Extrai o primeiro objeto JSON {} ou array []
    m_obj = re.search(r"(\{.*\})", texto, flags=re.S)
    if m_obj:
        return m_obj.group(1).strip()
    m_arr = re.search(r"(\[.*\])", texto, flags=re.S)
    if m_arr:
        return m_arr.group(1).strip()
    return texto

def parsear_json_possivel(texto):
    texto_limpo = limpar_json_da_ia(texto)
    try:
        return json.loads(texto_limpo)
    except Exception as e:
        # Falhou: incluir conteúdo limpo para depuração
        raise ValueError(f"Falha ao converter resposta em JSON. Conteúdo recebido (limpo):\n{texto_limpo}\nErro: {e}")

def contar_tokens_aproximado(texto):
    # Aproximação simples: 1 token ≈ 4 caracteres
    return max(1, int(len(texto) / 4))

# --- parâmetros de entrada ---
medicamentos = ['novorapid', 'basaglar']
bolus_alimentar = 15
bolus_correcao = 60
glicemia_atual = 132
descricao_alimentacao = """
hoje de manhã comi um pão frances com uma fatia de queijo prato mais um ovo cozido. Também tomei um café com leite, mais café do que leite.
"""

contexto_json = montar_json(medicamentos, bolus_alimentar, bolus_correcao, glicemia_atual, descricao_alimentacao)
prompt = (
    "Você é um nutricionista. Calcule carboidratos (g), calorias (kcal) e insulina necessária (U) "
    "para a alimentação descrita. Retorne APENAS um JSON válido no formato do exemplo abaixo, sem texto adicional.\n\n"
    f"Contexto:\n{contexto_json}\n\n"
    f"Exemplo de saída JSON:\n{json.dumps(exemplo_json, ensure_ascii=False, indent=2)}\n\n"
    "Responda agora com o JSON preenchido."
)

tokens_input = contar_tokens_aproximado(prompt)

# Chamada ao modelo (determinística: temperature=0)
try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        temperature=0.0,
        max_output_tokens=800
    )
except Exception as e:
    raise RuntimeError(f"Erro ao chamar a API do modelo: {e}")

# Extrair texto bruto de forma compatível com variações da SDK
raw_text = None
# Possíveis caminhos na resposta: adapte se sua versão SDK usa estrutura diferente
try:
    raw_text = response.candidates[0].content.parts[0].text
except Exception:
    try:
        raw_text = response.output[0].content[0].text
    except Exception:
        # fallback: tentar imprimir objeto response para depuração
        raise RuntimeError(f"Não foi possível localizar o texto da resposta da API. Resposta bruta: {response}")

resposta_json = raw_text.strip()
tokens_output = contar_tokens_aproximado(resposta_json)
tokens_total = tokens_input + tokens_output

# Parse robusto
dados = parsear_json_possivel(resposta_json)

# Aceita dict com chave 'alimentos' ou lista direta
if isinstance(dados, dict) and "alimentos" in dados:
    alimentos = dados["alimentos"]
elif isinstance(dados, list):
    alimentos = dados
else:
    raise ValueError("Formato JSON inesperado. Esperado lista de alimentos ou dict com chave 'alimentos'.")

# Imprime resultados
for item in alimentos:
    nome = item.get("nome_do_alimento")
    carb = item.get("quantidade_de_carboidrato_g")
    kcal = item.get("quantidade_de_caloria_kcal")
    glic = item.get("quantidade_de_glicemia_enviada_mg_dl", 0)
    insu = item.get("quantidade_de_insulina_necessaria_u")
    print(f"Alimento: {nome!r}, Carboidratos: {carb}, Calorias: {kcal}, Glicemia enviada: {glic}, Insulina (U): {insu}")

print("\nContagem de tokens (aprox.):")
print(f"Input: {tokens_input}, Output: {tokens_output}, Total: {tokens_total}")