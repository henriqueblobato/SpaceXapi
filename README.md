# SpaceXapi
This project reads a json file of ships from the starlink project and adds them to a database. To use it you just need to specify the file directory in the .env file and run the containers.
An api will be made available for you to consume the data. All answers contain pagination for a faster response.

## How to run 
1. Set your .env file, here is a sample
```
SPACECRAFT_FILE=starlink.json

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=postgres
DB_PORT=5432
```
2. Run the containers
```
docker-compose up --build -d
```
When preparing the environment, a progress bar will show the percentage of files and the progress of the completion of the file that has already been sent to the database.
```
100%|██████████| 3141/3141 [00:32<00:00, 98.05it/s] 
```

## Available endpoints

### "/spacetracks/"
POST GET PUT PATH of SpaceTracks

Available filters:
- /spacetracks/?object_name=SPACE_SHIP_NAME
- /spacetracks/?country_code=US
- /spacetracks/?ts=2021-12-05
- /spacetracks/?identifier=a1b2c3r4t5y6
- /spacetracks/?coordinates=-12.123123,12.345345

Also available in all mixins
- /spacetracks/?object_name=SPACE_SHIP_NAME&identifier=a1b2c3r4t5y6&ts=2021-12-05
- /spacetracks/?object_name=SPACE_SHIP_NAME&coordinates=-12.123123,12.345345&ts=2021-12-05&country_code=US

Importantly, when the timestamp is informed, the order of response will always be in the lagitude and longitude of the closest ships to the location in kilometers, using the Haversine calculation.

### "/launch/"
POST GET PUT PATH of Launches, based on their IDs

### "/objecttype/"
POST GET PUT PATH for the aircraft object type. I thought there would be more :)

## Online deployed server
```
https://spacex-api-123.herokuapp.com/
```
