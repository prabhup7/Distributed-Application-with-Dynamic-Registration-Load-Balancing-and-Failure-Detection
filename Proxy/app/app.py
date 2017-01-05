#!/usr/bin/python
# This is a simple port-forward / proxy, written using only the default python
# library. If you want to make a suggestion or fix something you can contact-me
# at voorloop_at_gmail.com
# Distributed over IDC(I Don't Care) license
import socket
import select
import time
import sys
import redis
from cb3 import CircuitBreaker3
from cb2 import CircuitBreaker2
from cb1 import CircuitBreaker1


MY_EXCEPTION = 'Threw Dependency Exception'


r =redis.Redis(host ='pedantic_davinci',port = 6379)




# Changing the buffer_size and delay, you can improve the speed and bandwidth.
# But when buffer get to high or delay go too down, you can broke things
buffer_size = 4096
delay = 0.0001
count = 0
forward_port = 0


class Forward:
    def __init__(self):
        self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        try:
            self.forward.connect((host, port))
            return self.forward
        except Exception, e:
            print "excpt forward"
            return False

class TheServer:
    input_list = []
    channel = {}

    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(200)

    def main_loop(self):
        self.input_list.append(self.server)
        while 1:
            time.sleep(delay)
            ss = select.select
            inputready, outputready, exceptready = ss(self.input_list, [], [])
            print inputready
            for self.s in inputready:
                if self.s == self.server:
                    self.on_accept()
                    break

                self.data = self.s.recv(buffer_size)
                if len(self.data) == 0:
                    self.on_close()
                    break
                else:

                    self.on_recv()

    def on_accept(self):
        global forward_port
        port_list = r.lrange('ports',0,100)
        global count
        print port_list
        for z in port_list:
            
            if count == len(port_list) or count > len(port_list):
                count = 0
            forward_port= int(port_list[count])
            print "forwar_port %d",forward_port
            count = count + 1
            break

        forward = Forward().start('small_almeida',forward_port)
        print forward
        clientsock, clientaddr = self.server.accept()
        if forward:
            print clientaddr, "has connected"
            self.input_list.append(clientsock)
            self.input_list.append(forward)
            self.channel[clientsock] = forward
            self.channel[forward] = clientsock
        else:
            

            if forward_port == 5000:
                self.dependency_call1()
            elif forward_port == 5001:
                self.dependency_call2()
            else:
                self.dependency_call3()
            
            print "Can't establish connection with remote server.",
            print "Closing connection with client side", clientaddr
            clientsock.close()
    
    @CircuitBreaker1(max_failure_to_open=3, reset_timeout=3)
    def dependency_call1(self):
        

        print "calling circuit brekaer1"
        
        return "xception(MY_EXCEPTION)"
    @CircuitBreaker2(max_failure_to_open=3, reset_timeout=3)
    def dependency_call2(self):
        

        print "calling circuit brekaer2"
        
        return "xception(MY_EXCEPTION)"
    
    @CircuitBreaker3(max_failure_to_open=3, reset_timeout=3)
    def dependency_call3(self):
        

        print "calling circuit brekaer3"
        
        return "xception(MY_EXCEPTION)"

    def on_close(self):
        print self.s.getpeername(), "has disconnected"
        #remove objects from input_list
        self.input_list.remove(self.s)
        self.input_list.remove(self.channel[self.s])
        out = self.channel[self.s]
        # close the connection with client
        self.channel[out].close()  # equivalent to do self.s.close()
        # close the connection with remote server
        self.channel[self.s].close()
        # delete both objects from channel dict
        del self.channel[out]
        del self.channel[self.s]

    def on_recv(self):
        data = self.data
        # here we can parse and/or modify the data before send forward
        print data
        self.channel[self.s].send(data)

if __name__ == '__main__':
        server = TheServer('', 9090)
        try:
            server.main_loop()
        except KeyboardInterrupt:
            print "Ctrl C - Stopping server"
            sys.exit(1)
