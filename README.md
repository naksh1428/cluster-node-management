# Cluster Node Management

-- `Functionality` :
 Telecom service provider provides multiple services to end users.
 In the cities we have multiple services(Group) and multiple nodes .One group can have serveral nodes.
 There is a cluster consisting of several nodes.
 Nodes having their dedicated groups, here we performed CRUD operations on groups. 
 If group got deleted then Group_Id will get removed from dedicated nodes too.
  
## Prerequisites

1. FastAPI 
2. Python installed 
3. mysql 8.0 Community installed
4. Docker
5. Docker Compose
6. kubectl
7. minikube



## Project structure
cluster-node-management/

    app/
        __init__.py
        main.py
        models.py
        schemas.py
        database.py
        test/
            __init__.py
            conftest.py
            test_endpoints.py
    Dockerfile
    docker-compose.yaml
    requirenments.txt
    REDME.md
    kubectl/
    
         deployemnt.yaml
         service.yaml
      
    

- `main.py` : FastAPI CRUD operation
- `tests/test_main.py`: Contains the pytest test cases for the FastAPI application.
-  `Dockerfile`: contains Docker image for the FastAPI application.
- `docker-compose.yml`: Configuration of Docker services for the application and testing.
- `requirements.txt`: Lists the Python dependencies for the project.
        
## Run the Project  
1. Deploy project using docker-compose (up and running)
    
Here Created a Docker Compose file to manage the Docker container for the FastAPI application and database.
Run the Docker Compose to build and run the FastAPI application,
It will run the pytest within docker container.

        `command` : 
                    docker-compose up --build


The command will build Image and run container, will the start the application on http://localhost:8000.

2 Deploy Project using kubernetes(minikube) (attempted)
    

Created 2 files deployment.yaml and service.yaml

- `deployment.yaml` : 

The first part of the file will configure the application pods and the resources of  deployed application. 
It will create two pods. Pods are replicas or instances of the deployed application. 
It will use the created image.

- `service.yaml` : 

This second type of file configures the Kubernetes Service for the application. 
It uses the LoadBalancer Kubernetes Service to equally distribute traffic to the two container pods. 
Minikube will assign an External IP address to the Kubernetes Service. 
It will enable us to access the deployed Fast API application

create docker Image:


          `command` : 
                    docker build -t  <image-name> .
    


           `command` : 
                    kubectl apply -f .


- `Few kubernetes important commands ` :
                 kubectl get deployment
                 kubectl get service
                 minikube service <service_name>


## API Endpoints
- Create group

        POST /v1/group
        Request Body: {
                         "group_name": "E-sim",
                         "city": "Zurich"
                       }

        Response: response code 201.
- Read Single group

      GET /v1/groups/{group_id}
      Response: The group with the specified ID with response code 200.


- Read All Groups

      GET /v1/groups/
      Response: A list of all groups with response code 200.


- Delete group

       DELETE /v1/groups/{group_id}
       Response: response code 200 with successful deletion.

- Create Node 

          POST /v1/node
          Request Body: {
                           "node": "node1.com",
                           "group_id": 1
                         }

          Response: response code 201

- Read All nodes

      GET /v1/nodes/
      Response: A list of all nodes with response code 200.
