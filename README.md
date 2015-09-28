# py_docker_stats_collector

project started on 21-09-2015

Data is stored in a mysql db, follow the instructions on this website to get it installed and set up. http://zetcode.com/db/mysqlpython/


This tool collects stats similarly to cadvisor, stats are stored in a db of your choosing in this case docker_stats. Just run python collector.py and leave it running in the background collecting data and so you can come back a later time to check the results.




MORE INFO: With this tool you will be able to store and analyse cpu usage, individual core usage and ram_usage for now.

Collector mode: python collector.py  

Analyser mode: python collector.py -m 'analyse' -id $(container_id)  

Example output:  
(T - Cpu - Core1 - Core2 - Core3 - Core4 - Memory - Ram)  
1 15868738 4168148 8452622 1585063 1662905 544768 0  
2 15868738 4168148 8452622 1585063 1662905 544768 0  
3 15868738 4168148 8452622 1585063 1662905 544768 0  
4 15868738 4168148 8452622 1585063 1662905 544768 0  


T/100 = time since container startup in secons. Ex = if T=1 than time in secs = 0.01

All other values are in bytes.

TODO and more INFO: 
the ram stats collecting fuction needs to be implemented.




Developer: Ruben Vasconcelos ruben.vasconcelos2@mail.dcu.ie
Feel free to email me with any sugestions/feature requests
