# Plano de Integração de dados com IA

-> Objetivo: 
      Integrar dados de um sistema local de saúde com uma camada de IA (Gemini ou OpenAI), utilizando **JSON como formato de troca de dados**.
	Usúario / local
	
    ->Sistema --------------> JSON ------> Gemini/OpenAi
         1- Paciente                         |
	     2- Alimentação <------------------ JSON ==> Alimento (descrição, unidade, calorias, carboidratos)               
	                                                 Insulina (nome, princípio ativo) 
                             


	1- Paciente = (insulinas, g por insulina, unidade por glicemia)
		
	2- Alimentação = (texto puro, nome insulina, qtd de unidades)
	
Essa integração visa automatizar o cálculo de nutrientes e insulina com base na descrição textual da refeição feita pelo paciente.

# Estrutura Geral do Código
 O script foi desenvolvido em Python e se organiza em módulos lógicos:

 - Carregamento da API e ambiente
 - Montagem e desmontagem de JSON
 - Definição do papel e instruções da IA
 - Envio da requisição à IA (Gemini)
 - Processamento e exibição dos resultados

# 1. Carregamento da Chave de API e Configuração do Ambiente
    from google import genai
    from dotenv import load_dotenv
    import os

    load_dotenv("C:/Users/user/Desktop/Tecnologias-Inteligentes-Aplicadas-a-Saude/trabalhoTIAS/.env")
    api_key = os.getenv("COLOQUE_SUA_API_KEY_AQUI")


 O dotenv carrega variáveis de ambiente armazenadas no arquivo .env, onde está a chave de API da IA.
 Essa chave é necessária para autenticar as requisições ao modelo Gemini.

# 2. Instanciação do Cliente Gemini
    client = genai.Client(api_key="COLOQUE_SUA_API_KEY_AQUI")


 Cria um cliente autenticado que se comunica com o modelo Gemini 2.5 Flash, permitindo o envio de prompts e o recebimento de respostas em linguagem natural.

# 3. Função para Montar o JSON
    def montar_json(medicamentos, bolus_alimentar, bolus_correcao, glicemia_atual, descricao_alimentacao):
       return {
           "medicamentos": medicamentos,
           "bolus_alimentar": bolus_alimentar,
           "bolus_correcao": bolus_correcao,
           "glicemia_atual": glicemia_atual,
           "descricao_alimentacao": descricao_alimentacao
       }
 Essa função cria um dicionário JSON com as informações do paciente e sua alimentação.
 
# 4. Função para Desmontar o JSON (resposta da IA)
    def desmontar_json(resposta_json):
    ...


 Essa função interpreta o JSON retornado pela IA, tratando diferentes formatos possíveis de resposta.

 Principais funcionalidades:

 - Remove trechos de formatação (```json e ```).

 - Converte texto JSON em objeto Python.

 - Trata casos onde os alimentos vêm:

   - Como lista (["pão", "ovo"])

   - Ou como string ("pão, ovo")

Extrai:

  - Nome dos alimentos

  - Quantidade de calorias

  - Quantidade de carboidratos

  - Quantidade de insulina necessária

 Caso haja erro no formato, retorna valores padrão (vazios ou zero).

# 5. Entradas do Sistema Local
    medicamentos = ['novorapid', 'basaglar']
    bolus_alimentar = 15
    bolus_correcao = 60
    glicemia_atual = 132
    descricao_alimentacao = "hoje de manhã comi um pão com uma maionese, e mais um ovo frito."


 Esses dados simulam as informações fornecidas pelo sistema local (ou pelo paciente).

 Após isso, o JSON é montado:

<<<<<<< HEAD
    contexto_json = montar_json(medicamentos, bolus_alimentar, bolus_correcao, glicemia_atual, descricao_al

=======
    contexto_json = montar_json(medicamentos, bolus_alimentar, bolus_correcao, glicemia_atual, descricao_al)
>>>>>>> dd5d2e1 (finaliza)
