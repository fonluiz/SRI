# Bibliotecas
import nltk
import numpy as np
import pandas as pd

news_df = pd.read_csv("data/local_newspaper_news(pt-br).csv", engine = "python")

# Construção de índice invertido
# A melhor estrutura de dados para se utilizar na construção do índice invertido é tabela hash.
# Em Python, dicionários são implementados utilizando tabelas hash. Dicionário é um array cujos índeces
# são obtidos aplicando uma função hash nas chaves.
def create_indexer(df):
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

    return indexer

def preprocess(text):
    return text.lower()

news_indexer = create_indexer(news_df)

def and_search(term1, term2):
    result = []

    term1 = preprocess(term1)
    term2 = preprocess(term2)

    posting1 = news_indexer[term1]
    posting2 = news_indexer[term2]

    iterator1 = iter(posting1)
    iterator2 = iter(posting2)

    element1 = next(iterator1, None)
    element2 = next(iterator2, None)

    while (element1 != None) and (element2 != None):
        if element1 == element2:
            result.append(element1)
        elif element1 < element2:
            element1 = next(iterator1, None)
        else:
            element2 = next(iterator2, None)

    print("result")


and_search("Campina", "Grande")
