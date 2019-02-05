import pandas as pd
from elasticsearch import Elasticsearch
from config import elastic_hosts

def sr_index_create():

    try:
        es = Elasticsearch(hosts=[elastic_hosts])
        sr_mapping={
            "settings" : {
                "number_of_shards" : 2,
                "number_of_replicas" : 2
            },
            "mappings":{
                "_doc":{
                    "dynamic": 'false',
                    "properties":{
                        "search_term":{
                            "type":"text",
                            "analyzer":"keyword",
                            "search_analyzer": "keyword"
                        }
                    }
                }
            }
        }

        es.indices.create(index='sr', body=sr_mapping)
        print("created index")
        del es
    except Exception:
        print("except in sr")
        raise ConnectionError


def data_agg(path):

    try:
        logs_data = pd.read_json(path,lines=True)
    except Exception:
        raise FileNotFoundError

    sr_logs_data = logs_data[logs_data.result_type == 'SR']
    final_df = sr_logs_data.groupby(['search_term']).\
                            size().\
                            to_frame('count').\
                            reset_index().\
                            sort_values(["count"], ascending=False)

    final_df = final_df[final_df.search_term != '']
    vocab_list = list(final_df.search_term)
    return  vocab_list


def data_dump(vocab_list):

    try :
        print("in data_dump func")
        es = Elasticsearch(hosts=[elastic_hosts])
        for ele in vocab_list:
            doc={
                'search_term':ele
            }
            es.index(index="sr", doc_type='_doc', body=doc)
        del es
    except Exception:
        print("except in data_dump")
        raise ConnectionError


if __name__=='__main__':
    print("INFO : Dumping logs data...")
    sr_index_create()
    path = "./logs_data/sample.learn.logs.2016.json"
    vocab = data_agg(path)
    data_dump(vocab)
    print("INFO: Data dump completed !!")