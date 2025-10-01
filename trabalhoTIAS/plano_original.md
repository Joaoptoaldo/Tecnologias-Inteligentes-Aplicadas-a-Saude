# Plano de Integração de dados com IA

-> Objetivo: 
     Integrar dados de um sistema local de saúde com uma camada de IA (Gemini ou OpenAI), utilizando **JSON como formato de troca de dados**.
    
        -sistema ----> JSON ------> gemini/opneai
         1- paciente                       |
	     2- alimentação   <--------------JSON-->alimento (descrição, unidade, calorias, carboidratos)               
	                                             insulina (nome, princioativo) 



1-paciente ---> insulinas
	              g por insulina 
		            unidade por glicemia

2-alimentação -> texto puro
                 nome insulina
		             qtd de unidades
