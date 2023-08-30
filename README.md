# NivoDashboard
Nivo backend Dashboard for tracking app users

Using Flask, Apache Kafka, ClickHouse SQL DB, and WSGI for designing this Backend Dashboard.
Main.py is our producer file where we send the user data to our database. 
We also use Apache Kafka for multi-thread and server failure purposes.

r.txt includes all the module versions we have used for this dashboard.
bc.py, e.py, and pv.py all are from the user side (consumer).
