# Bibliotecas
import nltk
import numpy as np
import pandas as pd

# Construção de índice invertido
# A melhor estrutura de dados para se utilizar na construção do índice invertido é tabela hash.
# Em Python, dicionários são implementados utilizando tabelas hash. Dicionário é um array cujos índeces
# são obtidos aplicando uma função hash nas chaves.
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


def preprocess(text):
    return text.lower()

def and_search(term1, term2):
    term1 = preprocess(term1)
    term2 = preprocess(term2)

    posting1 = indexer[term1]
    posting2 = indexer[term2]

    return (posting1 & posting2)

def or_search(term1, term2):
    term1 = preprocess(term1)
    term2 = preprocess(term2)

    posting1 = indexer[term1]
    posting2 = indexer[term2]

    return (posting1 | posting2)

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


news_df = pd.read_csv("data/local_newspaper_news(pt-br).csv", engine = "python")

create_indexer(news_df)

assert len(search("debate OR presidencial")) == 1770
assert len(search("debate AND presidencial")) == 201

assert len(search("presidenciáveis OR corruptos")) == 164
assert len(search("presidenciáveis AND corruptos")) == 0

assert len(search("Belo OR Horizonte")) == 331
assert len(search("Belo AND Horizonte")) == 242

# Bônus
def conjunctive_search(query):
    and_op = " AND "

    terms = query.split(and_op)

    for i in range(0, len(terms)):
        terms[i] = preprocess(terms[i])
