# Invoice-Payment pairing tool
This is an example project showcasing how you can use automate simple but tedious bookkeeping tasks, like payment reconciliation, by the use of automated ETL(extract, transform, load) pipelines and store the reconciled payments in a database. 


## How to use:
First of all you'll need somewhere to run this dockerized project. The method I've used when running this project is by simply having the docker desktop running in the background when running the different processes that are part of the project.

After that you can simply run the project by running;
```
docker compose up --build
```
when youre in the project catalog. 

After that you should be able to display the table that has been created in the postgreql database by running:
```
docker exec -it postgres psql -U airflow -d etl

SELECT * FROM paired;
```

> Disclaimer: Make sure the docker project is running and that the port 5432 is not used by another service

You can also watch how the automated tasks are performing (suceeeding or failing and some additional output) in real-time by putting in http://localhost:8080/ into your search bar while running the project