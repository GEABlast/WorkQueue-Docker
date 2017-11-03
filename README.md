# CCTools WorkQueue + Docker

A Docker base image for creating CCTools WorkQueue applications. 

For information about CCTools/WorkQueue, check out [The Cooperative Computing Lab](http://ccl.cse.nd.edu/).

## Usage

To use the base image interactively:
```
docker run --rm -it -p 9123:9123 asherkhb/workqueue-docker:base /bin/bash
```

To use in your own applications, simply use:
```
FROM asherkhb/workqueue-docker:base
```

To build from the Dockerfile, clone the repository then:
```
docker build --rm -t workqueue-docker:<version> .
```

To test connectivity, use included test scripts:
```
docker run --name master -d -p 9123:9123 asherkhb/workqueue-docker:base /bin/bash -c "test_master.py"
docker run --name worker -d asherkhb/workqueue-docker:base /bin/bash -c "work_queue_worker -d all --cores 0 <IP> 9123
```
*NOTE: You can probably find the IP address by running `docker inspect master`, then looking for NetworkSettings - Networks - Gateway*

After test script is complete, master will stop. You can check for the results using:
```
docker start master
docker exec -it master /bin/bash
root@hash:/# cat run0.txt
```
*NOTE: You can also check for problems and other stats using `docker logs`*

## Specifics
* CCTools/WorkQueue: version 6.2.2
* python 2.7 + PIP + Dev
  * Additional packages: psutil
* python3 + PIP + Dev