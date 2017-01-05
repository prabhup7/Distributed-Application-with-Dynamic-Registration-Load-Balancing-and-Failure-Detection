# Distributed-Application-with-Dynamic-Registration-Load-Balancing-and-Failure-Detection

### Abstract

In this project, we build a sample expense management application to achieve the following:

* Dynamic Replica Registration
* Dynamic Load Balancing 
* Failure Detection


* Dynamic Replica Registration

A new component called Router will be implemented based on this tiny [Python TCP proxy server](http://voorloopnul.com/blog/a-python-proxy-in-less-than-100-lines-of-code/). 

As part of the node registration, whenever we launch the expense management application's Docker instance, it will auto-register to the own instance
to the router.


* Failure Detection (via CircutBreaker)

Whenever a node reaches its CircuitBreaker's error count, the router deregisters the failed node from the routing table in Redis and forward the same request to the next available node.  
