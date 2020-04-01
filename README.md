# Datastore serialization performance test

Google App Engine's Python original datastore library called "db" has very slow deserialization for models that have many properties. This project benchmarks this library, and compares it to ndb and our own hacked up minimal version. For details [see my blog post](http://www.evanjones.ca/app-engine-db-serialization.html).


## Setup

1. Build the docker-compose app

   ```shell script
   docker-compose build
   ```

2. Run the unit tests to verify the dependcies are setup and running correctly

   ```shell script
   docker-compose up -d
   ```

3. Create a new App Engine project to tests your code in:

   ```shell script
   open "https://console.cloud.google.com/projectcreate"
   ```

4. Deploy your app to Google App Engine Standard (python 2.7)

   ```shell script
   docker-compose exec app gcloud auth login
   docker-compose exec app gcloud config set project [YOUR PROJECT ID]
   docker-compose exec app gcloud app deploy performance.yaml 
   ```
   
   This will deploy your app to:
   > https://performance-test-dot-[YOUR PROJECT ID].appspot.com

5. Developing the benchmark app. If you are doing development on the benchmark app and need to install new requirements run this to install them in the running container: 

    ```shell script
     docker-compose exec app pip install -r requirements.txt
    ```

    Or run this to tear it down and re-build the app entirely
    ```shell script
     docker-compose down
     docker-compose build
     docker-compose up -d 
    ```
   
6. Run the unit tests 

    ```shell script
     docker-compose exec app pytest
    ```


## Local Benchmark Testing

1. Setup the app
    ```shell script
     docker-compose down
     docker-compose build
     docker-compose up -d 
    ```

1. Run the serialization benchmarks
    ```shell script
     docker-compose exec app python manage.py benchmark-serialization
     docker-compose exec app python manage.py benchmark-crud 
    ```

1. Run the CRUD benchmarks against a mock datastore / local database
    ```shell script
     docker-compose exec app python manage.py benchmark-crud 
    ```

1. Run the CRUD benchmarks against a mock datastore / local database
    ```shell script
    docker-compose exec app gcloud auth login
    docker-compose exec app gcloud config set project [YOUR PROJECT ID]
    docker-compose exec app bash -c 'APPLICATION_ID=bluecore-qa python manage.py benchmark-crud'

    ```



1. Create a set of instances that get used for the test. This needs to be done only once:

   ```shell script
    open "https://performance-test-dot-[YOUR PROJECT ID].appspot.com/db_entity_setup"
   ```

2. Run the performance test

   ```shell script
    open "https://performance-test-dot-[YOUR PROJECT ID].appspot.com/db_entity_test"
   ```

   ```shell script
    open "https://performance-test-dot-[YOUR PROJECT ID].appspot.com/serialization_test"
   ```
