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

 - Carregamento da API e ambiente (.env)
 - Montagem e desmontagem de JSON
 - Definição de contexto e instruções para a IA
 - Envio da requisição à IA (Gemini)
 - Processamento e exibição dos resultados

# 1. Carregamento da Chave de API e Configuração do Ambiente
    import os
    from dotenv import load_dotenv
    from google import genai

    # Carrega o arquivo .env do diretório atual
    load_dotenv()

    # Busca múltiplos nomes possíveis para a variável de ambiente
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("COLOQUE_SUA_API_KEY_AQUI")

    if api_key:
        print("Chave carregada!")
    else:
        raise RuntimeError("Chave não encontrada! Defina GEMINI_API_KEY ou COLOQUE_SUA_API_KEY_AQUI no .env ou nas variáveis de ambiente.")
		
 O .env deve conter uma linha como:

     GEMINI_API_KEY="sua_chave_aqui"

 Essa chave autentica as requisições enviadas ao modelo Gemini.


# 2. Instanciação do Cliente Gemini

    client = genai.Client(api_key=api_key)
	
 O cliente é responsável por enviar prompts ao modelo Gemini 2.5 Flash e receber as respostas.
 A chamada principal é feita com client.models.generate_content(...).

 Cria um cliente autenticado que se comunica com o modelo Gemini 2.5 Flash, permitindo o envio de prompts e o recebimento de respostas em linguagem natural.

# 3. Montagem do JSON de Contexto
A função montar_json() organiza os dados de entrada do paciente e sua refeição:

    def montar_json(medicamentos, bolus_alimentar, bolus_correcao, glicemia_atual, descricao_alimentacao):
    dados = {
        "medicamentos": medicamentos,
        "parametros_insulina": {
            "bolus_alimentar": {"carb_por_unidade_g": int(bolus_alimentar)},
            "bolus_correcao": {"mg_dl_por_unidade": int(bolus_correcao)}
        },
        "medicoes": {"glicemia_atual_mg_dl": int(glicemia_atual)},
        "alimentacao": {"descricao": descricao_alimentacao.strip()},
        "instrucoes": "Responda apenas com JSON válido. Veja o schema em exemplo_json."
    }
    return json.dumps(dados, ensure_ascii=False, indent=2)

 Esse JSON serve de contexto estruturado para o modelo IA entender o cenário clínico e alimentar.
 
# 4. Limpeza e Interpretação da Resposta JSON da IA
 A resposta do modelo pode vir com marcações de código ou texto extra.
 As funções abaixo garantem que apenas um JSON puro e válido seja interpretado:
 
    def limpar_json_da_ia(texto):
    texto = texto.strip()
    texto = re.sub(r"^```(?:json)?\s*", "", texto, flags=re.I)
    texto = re.sub(r"\s*```$", "", texto)
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
	        raise ValueError(f"Falha ao converter resposta em JSON.\nConteúdo recebido:\n{texto_limpo}\nErro: {e}")
    ...


 Essas funções tornam o sistema resiliente a formatações diferentes que o modelo Gemini possa retornar.

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
 Exemplo de parâmetros enviados ao modelo:
 
    medicamentos = ['novorapid', 'basaglar']
	bolus_alimentar = 15
	bolus_correcao = 60
	glicemia_atual = 132
	descricao_alimentacao = """
	hoje de manhã comi um pão francês com uma fatia de queijo prato mais um ovo cozido.
	Também tomei um café com leite, mais café do que leite.
	"""
	
 Essas informações simulam os dados coletados de um paciente real ou sistema de registro clínico.

 O prompt final combina instruções, contexto e um exemplo JSON de resposta esperada.

# 6. Envio ao Modelo Gemini
 A chamada ao modelo é feita de forma determinística (temperature=0):

	response = client.models.generate_content(
	    model="gemini-2.5-flash",
	    contents=prompt,
	    temperature=0.0,
	    max_output_tokens=800
	)

O script então extrai o texto retornado de forma compatível com variações da SDK:

	try:
	    raw_text = response.candidates[0].content.parts[0].text
	except Exception:
	    raw_text = response.output[0].content[0].text
		
# 7. Contagem Aproximada de Tokens
 Para monitorar custo e desempenho:
 
	def contar_tokens_aproximado(texto):
		return max(1, int(len(texto) / 4))

# 8. Processamento e Exibição dos Resultados
 Após o parse do JSON, os dados são exibidos em formato legível:
	
	 for item in alimentos:
	    print(f"Alimento: {item.get('nome_do_alimento')!r}, "
	          f"Carboidratos: {item.get('quantidade_de_carboidrato_g')}, "
	          f"Calorias: {item.get('quantidade_de_caloria_kcal')}, "
	          f"Glicemia enviada: {item.get('quantidade_de_glicemia_enviada_mg_dl', 0)}, "
	          f"Insulina (U): {item.get('quantidade_de_insulina_necessaria_u')}")
			  
 Exemplo de saída:
 
	 Alimento: 'pão francês', Carboidratos: 30, Calorias: 150, Glicemia enviada: 0, Insulina (U): 2
	
	 Contagem de tokens (aprox.):
	 Input: 480, Output: 140, Total: 620

 Exemplo de Estrutura de Resposta Esperada

	{
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
	
# Dependências
 Instale as bibliotecas necessárias:

	 pip install python-dotenv google-genai

	

