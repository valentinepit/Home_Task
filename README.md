In the case of AdjustHomeTask
This API is made using technology: Python 3.9, Flask, SQLAlchemy, PostgreSQL

This project consist of three main moduls: app.py, constructor.py, config.py

app.py 

It's a Flask modul which take requests from HTTP and returns results as html temlates

constructor.py

Getting a values from app.py and converting it to SQL query. After that 
executing SQL query and returns results to app.py

config.py 

File to save settings and parameters of connection 

How to:
Request must be started by "query;"
Command-parameters separator ";" (order;os)
Command-command separator "&&" (group;os&&order;os)
Parameter-parameter separator "&" (order;os&date)

To choose columns use "cols;"
To use WHERE use "where;"
To use ORDER_BY use 'order;'
To use GROUP_BY use 'group;'
To use DESC use 'desc(column)'
To SUM use "sum(column)"
If You need to find CPI use "sum(revenue:installs)"


1. http://127.0.0.1:5000/query;cols;channel&country&sum(impressions)&sum(clicks)&&where;date%3C%222017-06-01%22&&group;channel&country&&order;desc(clicks)
2.http://127.0.0.1:5000/query;cols;date&sum(installs)&&where;date_to=%222017-05-31%22&date_from=%222017-05-1%22&os=%22ios%22&&group;date&&order;date
3.http://127.0.0.1:5000/query;cols;os&sum(revenue)&&where;date_to=%222017-05-31%22&country=%22US%22&&group;os&&order;desc(revenue)
4.http://127.0.0.1:5000/query;cols;channel&sum(revenue:installs)&&where;country=%22CA%22&&group;channel&&order;desc(CPI)