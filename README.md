In the case of AdjustHomeTask
This API is made using technologies: Python 3.9, Flask, SQLAlchemy, PostgreSQL

This project consist of three main moduls: app.py, constructor.py, config.py

app.py 

It's a Flask modul which take requests from HTTP and returns results as html temlates

constructor.py

Getting a values from app.py and converting it to SQL query. After that 
executing SQL query and returns results to app.py

config.py 

File to save settings and parameters of connection 
Use SQLALCHEMY_DATABASE_URI to connect DB to project

How to:
Request must be started by "query;"
Command-parameters separator ";" (order;os)
Command-command separator "&&" (group;os&&order;os)
Parameter-parameter separator "&" (order;os&date)

To choose columns use "cols;"
To use WHERE type "where;"
To use ORDER_BY type  'order;'
To use GROUP_BY type  'group;'
To use DESC type  'desc(column)'
To SUM type  "sum(column)"
If You need to find CPI use "(revenue:installs)"
To ORDER or GROUP by CPI use "order(CPI)" or group(CPI)


1. Show the number of impressions and clicks that occurred before the 1st of June 2017, 
   broken down by channel and country, sorted by clicks in descending order.
http://127.0.0.1:5000/query;cols;channel&country&sum(impressions)&sum(clicks)&&where;date%3C%222017-06-01%22&&group;channel&country&&order;desc(clicks)

2. Show the number of installs that occurred in May of 2017 on iOS, broken down by date, sorted by date in ascending order.
http://127.0.0.1:5000/query;cols;date&sum(installs)&&where;date_to=%222017-05-31%22&date_from=%222017-05-1%22&os=%22ios%22&&group;date&&order;date
3. Show revenue, earned on June 1, 2017 in US, broken down by operating system and sorted by revenue in descending order.
http://127.0.0.1:5000/query;cols;os&sum(revenue)&&where;date_to=%222017-05-31%22&country=%22US%22&&group;os&&order;desc(revenue)
4. Show CPI and spend for Canada (CA) broken down by channel ordered by CPI in descending order. 
   Please think carefully which is an appropriate aggregate function for CPI.
http://127.0.0.1:5000/query;cols;channel&sum(revenue:installs)&&where;country=%22CA%22&&group;channel&&order;desc(CPI)