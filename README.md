# TDEI-gtfs-flex-validation-python
## Introduction 
Service to Validate the GTFS flex file that is uploaded. At the moment, the service does the following:
- Listens to the topic _gtfs-flex-validation_ for any new message (that is triggered when a file is uploaded)
- Consumes the message and checks the filename in the message
  - if the filename contains the word _valid_ returns **valid** as the result
  - if the filename contains the word _invalid_ returns **invalid** as the result
  - if the file name does not contain either, it will return **invalid** as the result
- Publishes the result to the topic _gtfs-flex-validation_

## Getting Started
The project is built on Python with FastAPI framework. All the regular nuances for a Python project are valid for this.

### System requirements
| Software   | Version |
|------------|---------|
| Python     | 3.10.x  |


### Connectivity to cloud
- Connecting this to cloud will need the following in the `.env` file

```bash
UPLOAD_TOPIC=xxxx
UPLOAD_SUBSCRIPTION=xxxx
VALIDATION_TOPIC=xxxx
QUEUECONNECTION=xxxx
```
The application right now does not connect with the storage but validates via the file name.

### Build and Test
Follow the steps to install the node packages required for both building and running the application

1. Setup virtual environment
    ```
    python3.10 -m venv .venv
    source .venv/bin/activate
    ```

2. Install the dependencies. Run the following command in terminal on the same directory as `requirements.txt`
    ```
    pip install -r requirements.txt
    ```
3. The http server by default starts with `8000` port 
4. Run server
    ```
    uvicorn src.main:app --reload
    ```
5. By default `get` call on `localhost:8000/health` gives a sample response
6. Other routes include a `ping` with get and post. Make `get` or `post` request to `http://localhost:8000/health/ping`
7. Once the server starts, it will start to listening the subscriber(`UPLOAD_SUBSCRIPTION` should be in env file)
8. To publish a message to the same topic, hit `http://127.0.0.1:8000/publish` API
9. Once the above API(Step 8) is done, the message will be received in validation automatically





### Messaging

This micro service deals with two topics/queues. 
- upload queue from gtfs-flex-upload
- validation queue from gtfs-flex-validation


```mermaid
graph LR;
  A(gtfs-flex-upload)-->B[gtfs-flex-validation-service];
  B-->C(gtfs-flex-validation)
```
#### Incoming
The incoming messages will be from the upload queue `gtfs-flex-upload`.
The format is mentioned in [msg-gtfs-flex-upload.json](./src/assets/msg-gtfs-flex-upload.json)

#### Outgoing
The outgoing messages will be to the `gtfs-flex-validation` topic.
The format of the message is at [gtfs-flex-validation.json](./src/assets/msg-gtfs-flex-validation.json)

