# py_docker_stats_collector

project started on 21-09-2015  

This tool collects stats similarly to cadvisor, but in addition it also stores them. So you can use it with other programs or if you simply want to keep a record of your containers stats.

To change the way data is stored/displayed, update save_data() or analyse_data() respectively.  

MORE INFO: With this tool you will be able to store and analyse cpu usage, individual core usage and memory usage for now.

Usage help: python collector.py --help  

Collector mode: python collector.py  

Analyser mode: python collector.py -m 'analyse' -id $(container_id)  

Example output:  
cpu core1 core2 core3 core4 memory  
15868738 4168148 8452622 1585063 1662905 544768  
...   


By default the time frame for collection is 0.01 so the line number/100 = time since container startup in secons. Ex = num of lines=1 than runtime in secs = 0.01  

All other values are in bytes.  

TODO and more INFO:  
Testing, fix bugs + add io stats.  


Developer: Ruben Vasconcelos ruben.vasconcelos2@mail.dcu.ie
Feel free to email me with any sugestions/feature or requests.
