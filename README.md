# py_docker_stats_collector

project started on 21-09-2015

Data is stored in a mysql db, follow the instructions on this website to get it installed and set up. http://zetcode.com/db/mysqlpython/


This tool collects stats similarly to cadvisor, stats are stored in a db of your choosing in this case docker_stats. Just run python collector.py and leave it running in the background collecting data and so you can come back a later time to check the results.




MORE INFO: With this tool you will be able to store and analyse cpu usage, individual core usage and ram_usage for now.

To access the data open a terminal window and run mysql:  
mysql -u root -p  
mysql> USE docker_stats;  
SELECT * FROM container_id;


TODO and more INFO:  




Developer: Ruben Vasconcelos ruben.vasconcelos2@mail.dcu.ie
Feel free to email me with any sugestions/feature requests