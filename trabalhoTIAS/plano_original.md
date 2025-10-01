# Plano de Integração de dados com IA

-> Transformação de dados:
    A criptografia transforma informações legíveis (texto simples) em um formato cifrado, que parece um código sem sentido.
    
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
