# youtube-etl-pipeline-airflow-mongodb
End-to-end ETL pipeline orchestrated with Apache Airflow to ingest, process, and store YouTube video data into MongoDB.

## The Airflow DAG (is459_assignment_youtube) orchestrates two sequential tasks:
1. fetch_youtube_data — Calls YouTube Data API v3 to retrieve 100 videos matching the topic, handling pagination and deduplication, and saves results to a JSON file
2. load_data_to_mongo — Reads the JSON file, loads all records into a MongoDB collection, then deletes the intermediate file

### Set up steps
1. Clone the repository and cd into the file
``` git clone https://github.com/naixinnn/youtube-etl-pipeline-airflow-mongodb.git ```
``` cd youtube-etl-pipeline-airflow-mongodb ```

2. Set up venv and activate it
MacOS/Linux:
``` python -m venv venv ```
``` source venv/bin/activate ```

Windows: 
``` python -m venv venv ```
``` venv\Scripts\activate ```

3. Install dependencies 
``` pip install -r requirements.txt ```

4. Set up env variables - note that the .env file has to be in the dags folder
``` cp .env.example .env ```

### steps to generate API Key 
https://docs.themeum.com/tutor-lms/tutorials/get-youtube-api-key/

5. Start MongoDB
MacOS (homebrew): 
``` brew services start mongodb-community ```

Linux: 
``` sudo systemctl start mongod ```

Windows: 
``` net start mongoDB ```

6. Run the pipeline 
6.1 Point the dags_folder to cloned repo
``` cd ${AIRFLOW_HOME} ```
``` nano airflow.cfg ```
change dags_folder path to the location of your repo
e.g. ``` dags_folder = /Users/Desktop/youtube-etl-pipeline-airflow-mongodb/dags ```

6.2 Start Airflow 
``` airflow standalone ```
to note: initial setup, admin user and password will be provided in the terminal

6.3 Open Airflow UI to trigger the DAG
Open Airflow UI at http://localhost:8080 then find named DAG and trigger it manually. 

Once both tasks are successfully executed, extracted youtube details can be found in MongoDB. 



