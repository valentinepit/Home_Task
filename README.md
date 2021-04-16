In the case of AdjustHomeTask
This API is made using technology: Python 3.9, Flask, SQLAlchemy, PostgreSQL



запрос должен начинаться с query;
отделение команд от параметров через ;
разделение между командами &&
разделение между параметрами &

1. http://127.0.0.1:5000/query;cols;channel&country&sum(impressions)&sum(clicks)&&where;date%3C%222017-06-01%22&&group;channel&country&&order;desc(clicks)
2.http://127.0.0.1:5000/query;cols;date&sum(installs)&&where;date_to=%222017-05-31%22&date_from=%222017-05-1%22&os=%22ios%22&&group;date&&order;date
3.http://127.0.0.1:5000/query;cols;os&sum(revenue)&&where;date_to=%222017-05-31%22&country=%22US%22&&group;os&&order;desc(revenue)
4.http://127.0.0.1:5000/query;cols;channel&sum(revenue:installs)&&where;country=%22CA%22&&group;channel&&order;desc(CPI)