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
 O trecho imprime se a chave foi carregada com sucesso.

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



