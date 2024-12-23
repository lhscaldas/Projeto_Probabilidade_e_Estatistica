# README.MD

## Contexto
Este repositório contém o projeto final da disciplina COS868 - Probabilidade e Estatística para Aprendizado de Máquina, do Programa de Engenharia de Sistemas e Computação (PESC) do Instituto Alberto Luiz Coimbra de Pós-Graduação e Pesquisa de Engenharia (COPPE/UFRJ).

## Professora
- Profa. Dra. Rosa M. Leão (PESC/COPPE/UFRJ)

## Aluno
- Luiz Henrique Souza Caldas

## Sumário

Clique no título de cada seção para ir ao arquivo do código python referente a ela. Na ultima seção, o link leva para o relatório em pdf.

### [Dataset](códigos/preprocessamento.py)
O projeto envolve a análise de dados fornecidos por um provedor de Internet, contendo taxas de upload e download em bps de dispositivos domésticos (Smart-TV e Chromecast). Cada dataset inclui campos como `device id`, `date hour`, `bytes up` e `bytes down`. Devido à variação em ordens de grandeza das taxas, os valores devem ser escalados para log base 10 antes da análise. Nesta seção é feita a Análise Exploratória e o Pré-processamento dos dados. 

### [Estatísticas gerais](códigos/estatisticas_gerais.py)
Os dados são analisados independentemente do horário de coleta. As métricas incluem histogramas, funções de distribuição empírica, box plots, médias, variâncias e desvios padrão para upload e download, separadamente para Smart-TV e Chromecast. As estatísticas devem ser interpretadas com foco nas diferenças e similaridades entre os dispositivos.

### [Estatísticas por horário](códigos/estatisticas_por_horario.py)
A análise considera o horário de coleta, calculando box plots, médias, variâncias e desvios padrão para cada hora. Os gráficos devem mostrar as tendências diárias para upload e download, destacando diferenças e padrões únicos entre os dispositivos.

### [Caracterizando os horários com maior valor de tráfego](códigos/caracterizando_os_horarios.py)
Os dois horários com maior média para upload e download são identificados para cada dispositivo. São gerados histogramas, estimativas de máxima verossimilhança (MLE) para distribuições Gaussiana e Gamma, e gráficos comparativos (Probability Plot e QQ Plot) para verificar se os dados se ajustam a essas distribuições.

### [Análise da correlação entre as taxas de upload e download](códigos/correlação.py)
A correlação entre upload e download é investigada para os horários de maior tráfego, calculando coeficientes de correlação e utilizando scatter plots. A análise avalia a relação entre as taxas para cada dispositivo.

### [Comparação dos dados gerados pelos dispositivos Smart-TV e Chromecast](códigos/G_test.py)
Utilizando o teste estatístico G (G-test), compara-se a similaridade entre as distribuições de upload e download dos dois dispositivos nos horários de maior tráfego. Os histogramas devem ser padronizados para permitir a comparação.

### [Relatório](relatório/relatorio.pdf)
O relatório final deve compilar todos os resultados, detalhar as metodologias utilizadas e comentar sobre a aplicabilidade das conclusões para auxiliar o provedor de Internet a compreender melhor o comportamento de sua rede. O código-fonte deve ser disponibilizado por meio de um link no relatório.

