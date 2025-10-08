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
