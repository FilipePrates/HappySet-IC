# Problema MaxHS - Projeto de Iniciação Científica

Este repositório foi desenvolvido durante um projeto de iniciação científica sob a orientação do Professor Luidi Simonetti. O projeto aborda o problema MaxHS, modelado conforme descrito em [Max_Happy_Set-Definition.pdf](./Max_Happy_Set-Definition.pdf). A implementação desta modelagem pode ser encontrada no script `happyset.py`.
Diferentes instâncias do problema então são criadas, com diferentes combinações de parâmetros inciais (classe do grafo de input, tamanho do grafo de input, e K (número de escolhas)), e o tempo necessário para se obter uma resposta com esta modelagem para cada uma dessas instâncias é gravado.

Para resolver o problema modelado, será necessário o pacote `cplex`. Você pode obtê-lo através do **CPLEX Optimization Studio**, que está disponível gratuitamente para fins acadêmicos via IBM Academic Initiative:

[IBM Academic Initiative - CPLEX Optimization Studio](https://academic.ibm.com/a2mt/email-auth#/)

### Geração de Grafos de Input

Para gerar os grafos de input necessários para o problema, utilize o seguinte notebook:

- [generateFiles.ipynb](./generateFiles.ipynb)

### Resolução de Instâncias

Uma vez que os grafos de input forem gerados, você pode aplicar a modelagem e solucionar as instâncias do problema utilizando o seguinte notebook:

- [generateResults.ipynb](./generateResults.ipynb)

### Visualização de Resultados

Após obter os resultados, você pode visualizá-los utilizando o seguinte notebook:

- [viewResults.ipynb](./viewResults.ipynb)

Filipe Prates
116011311
