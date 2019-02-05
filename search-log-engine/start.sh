docker load <images.tar

echo "creating network dockerlocal"

if  docker network ls | grep -q dockerlocal ;
    then docker network disconnect -f dockerlocal elasticsearch-container
         docker network disconnect -f dockerlocal app-container
         docker network rm dockerlocal
         docker network create dockerlocal
    else docker network create dockerlocal
fi



if  docker container ls -a | grep -q elasticsearch-container ;
    then    docker stop elasticsearch-container
            docker rm elasticsearch-container
            #docker pull docker.elastic.co/elasticsearch/elasticsearch:6.6.0
            docker run -d --name elasticsearch-container --network dockerlocal -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.6.0
    else    #docker pull docker.elastic.co/elasticsearch/elasticsearch:6.6.0
            docker run -d --name elasticsearch-container --network dockerlocal -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.6.0
fi

echo "elastic server started"

echo "Starting dump"

sleep 3

if  docker container ls -a  | grep -q app-container ;
    then    docker stop app-container
            docker rm app-container
            #docker build -t app-docker .
            docker run -d --name app-container -p 5000:5000 --network dockerlocal app-docker:latest
    else    #docker build -t app-docker .
            docker run -d --name app-container -p 5000:5000 --network dockerlocal app-docker:latest

fi

watch docker logs app-container