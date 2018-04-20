
# Parte 1 - Índice Invertido e Busca Booleana

O objetivo desta atividade é construir um índice invertido a partir de um conjunto de notícias. Após a indexação, iremos realizar buscas booleanas sobre o indexador.
  
Os [dados](https://raw.githubusercontent.com/fonluiz/SRI/master/mini-project-1/data/local_newspaper_news(pt-br).csv) utilizados na construção do índece invertido foram retirados do site [Estadão Online](http://www.estadao.com.br/). Trata-se de um arquivo csv com três colunas - titulo, conteudo e idNoticia. 

O código abaixo exibe as primeiras linhas do arquivo csv.


```python
import pandas as pd

news_df = pd.read_csv("data/local_newspaper_news(pt-br).csv", engine = "python")

news_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>titulo</th>
      <th>conteudo</th>
      <th>idNoticia</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>11 dos eleitores do País são filiados a legendas</td>
      <td>Há porém variações regionais nesse fenômeno En...</td>
      <td>7617</td>
    </tr>
    <tr>
      <th>1</th>
      <td>11 executivos integram 1º pedido de condenação...</td>
      <td>CURITIBA A força-tarefa da Operação Lava Jato ...</td>
      <td>412</td>
    </tr>
    <tr>
      <th>2</th>
      <td>11 executivos integram 1º pedido de condenação...</td>
      <td>CURITIBA A força-tarefa da Operação Lava Jato ...</td>
      <td>415</td>
    </tr>
    <tr>
      <th>3</th>
      <td>13 de deputados do PMDB quer romper com PT</td>
      <td>O Estado ouviu 54 dos 74 deputados do PMDB em ...</td>
      <td>6736</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2014 começou em 2007</td>
      <td>O estudo do Estadão Dados publicado ontem sobr...</td>
      <td>7611</td>
    </tr>
  </tbody>
</table>
</div>



### Passo 1: Criar o índice invertido

Um indice invertido é uma estrutura que guarda cada palavra em uma coleção de documentos e juntamente com essas palavras, guarda uma lista de todos os documentos em que essa palavra aparece.

A melhor estrutura de dados para se utilizar na construção de um índice invertido é tabelas hash. 

Em Python, dicionários são implementados utilizando tabelas hash. Dicionário é um array cujos índeces são obtidos aplicando uma função hash nas chaves.


```python
"""Cria uma estrutura de índice invertido.

argumentos:
df -- Um dataframe pandas 
"""
def create_indexer(df):
    global indexer
    indexer = {}

    for index, row in df.iterrows():
        document = row['titulo'] + " " + row['conteudo']
        document = preprocess(document)
        doc_id = row['idNoticia']

        for term in document.split():
            if term in indexer:
                indexer[term].add(doc_id)
            else:
                indexer[term] = set([doc_id])

"""Converte uma string para caixa baixa."""
def preprocess(text):
    return text.lower()

```

### Passo 2: Definir a função de busca

A função de busca deve ser capaz de fazer consultas simples de um termo ou consultas de dois termos com os operadores AND e OR. A entrada da função é uma string, por exemplo, "debate OR presidencial".

Abaixo encontra-se o código dessa função de busca.


```python
"""Executa uma busca booleana conjuntiva.

argumentos:
term1 -- o primeiro termo a se buscar
term2 -- o segundo termo a se buscar
"""
def and_search(term1, term2):
    term1 = preprocess(term1)
    term2 = preprocess(term2)

    posting1 = indexer[term1]
    posting2 = indexer[term2]

    return (posting1 & posting2)


"""Executa uma busca booleana disjuntiva.

argumentos:
term1 -- o primeiro termo a se buscar
term2 -- o segundo termo a se buscar
"""
def or_search(term1, term2):
    term1 = preprocess(term1)
    term2 = preprocess(term2)

    posting1 = indexer[term1]
    posting2 = indexer[term2]

    return (posting1 | posting2)


"""Executa uma busca booleana qualquer na estrutura de índece invertido.

argumentos:
query -- A consulta a se fazer, que deve conter o(s) termo(s) a se buscar e um operador (opcional)
"""
def search(query):
    and_op = " AND "
    or_op = " OR "

    if and_op in query:
        terms = query.split(and_op)
        return and_search(terms[0], terms[1])
    elif or_op in query:
        terms = query.split(or_op)
        return or_search(terms[0], terms[1])
    else:
        query = preprocess(query)
        return indexer[query]
```

### Passo 3: Avaliação das funções de busca

Vamos testar as seguintes consultas

1. candidatos
2. debate, presidencial (AND e OR);
3. presidenciáveis, corruptos (AND e OR);
4. Belo, Horizonte (AND e OR)


```python
# Primeiro criamos o indexer
create_indexer(news_df)

# Comentei esse prints para não poluir o documento
# print(search("candidatos"))
# print(search("debate OR presidencial"))
# print(search("debate AND presidencial"))
# print(search("presidenciáveis OR corruptos"))
# print(search("presidenciáveis AND corruptos"))
# print(search("Belo OR Horizonte"))
# print(search("Belo AND Horizonte"))

assert len(search("debate OR presidencial")) == 1770
assert len(search("debate AND presidencial")) == 201

assert len(search("presidenciáveis OR corruptos")) == 164
assert len(search("presidenciáveis AND corruptos")) == 0

assert len(search("Belo OR Horizonte")) == 331
assert len(search("Belo AND Horizonte")) == 242
```

### Questão bônus

Para realizar a busca conjuntiva foi criada uma nova função (**conjunctive_search**). Essa função recebe como parâmetro uma consulta de vários termos ligados com o operador *AND*. A função encontra os postings para cada um dos termos passados e os coloca em uma lista em ordem crescente de frequência dos termos. Em seguida, a lista com os postings é varrida e vai-se executando um *AND* dos postings da seguinte maneira: primeiro é calculado o *AND* dos dois primeiros postings e salva o resultado. Depois faz-se o *AND* desse resultado com o proximo posting da lista e assim continua até ter processado todos os postings.


```python
"""Executa uma pesquisa de vários termos ligados com um operador AND

argumentos:
query -- A consulta a se fazer
"""
def conjunctive_search(query):
    and_op = " AND "

    terms = query.split(and_op)

    postings = []

    for term in terms:
        term = preprocess(term)
        posting = indexer[term]
        add_posting(posting, postings)

    temp = merge(postings[0], postings[1])
    for i in range (2, len(postings)):
        temp = merge(temp, postings[i])

    return temp


"""Mescla dois posts seguindo a lógica da operação booleana AND

argumentos:
posting1 -- o primeiro posting a ser mesclado
posting2 -- o segundo posting a ser mesclado
"""
def merge(posting1, posting2):
    posting1 = sorted(posting1)
    posting2 = sorted(posting2)

    result = []

    i = 0
    j = 0
    while i < len(posting1) and j < len(posting2):
        if posting1[i] == posting2[j]:
            result.append(posting1[i])
            i += 1
            j += 1
        elif posting1[i] < posting2[j]:
            i += 1
        else:
            j += 1

    return result


"""Adiciona um posting a uma lista de forma a manter a lista ordenada em tamanho crescente dos postings.

argumentos:
posting -- O posting a ser adicionado à lista.
list -- A lista em que o posting será adicionado.
"""
def add_posting(posting, list):
    if list == []:
        list.append(posting)
    else:
        added = False
        for i in range(0, len(list)):
            p = list[i]
            if len(posting) < len(p):
                list.insert(i, posting)
                added = True
                break
        if not added:
            list.append(posting)
    return list

```

####  Avaliação da função de busca conjuntiva de vários termos

Utilizaremos alguns dos asserts utilizados anteriormente e mais alguns outros.


```python
assert len(conjunctive_search("debate AND presidencial")) == 201
assert len(conjunctive_search("presidenciáveis AND corruptos")) == 0
assert len(conjunctive_search("Belo AND Horizonte")) == 242

assert len(conjunctive_search("debate AND presidencial AND Belo")) == 12
assert len(conjunctive_search("debate AND dos AND milhão")) == 25
assert len(conjunctive_search("milhão AND que AND filiações")) == 1
assert len(conjunctive_search("do AND país AND a AND filiados")) == 26
```
