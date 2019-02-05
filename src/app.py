from flask import Flask, request, render_template
from config import elastic_hosts,serving_host,path

from elasticsearch import Elasticsearch
app = Flask(__name__)


@app.route('/',methods=['GET','POST'])
def get_index():
    if request.method=='GET':
        return  render_template('index.html')

    if request.method == 'POST':
        es = Elasticsearch(hosts=[elastic_hosts])
        query =  request.form['input_query']

        search_body = {
            "query": {
                "match": {
                    "search_term": {
                        "query": query,
                        "fuzziness": 2,
                        "prefix_length":3
                    }
                }
            }
        }

        res = es.search(index="sr", body=search_body)
        print("Got %d Hits:" % res['hits']['total'])
        resls = []
        for hit in res['hits']['hits']:
            resls.append((hit["_source"]['search_term']))
        return render_template('index.html', val=resls,query=[query])


@app.route('/search',methods=['GET','POST'])
def trial():
    print("trial")
    return request.form


if __name__ == '__main__':
    #data_dump_final(path)
    print("INFO: Running service at " + serving_host)
    port=5000
    debug=True
    app.run(host=serving_host,port=port,debug=debug)
