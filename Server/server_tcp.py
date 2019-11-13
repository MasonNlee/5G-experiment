import time
import socket
import datetime
import threading
from pymongo import MongoClient

client = MongoClient()
production_env = True
host = "0.0.0.0"
port_recv = 55880
port_send = 55881

Latitude = ""
Longitude = ""
Temperature = ""
Height = ""
dataTemp = ""
dataFlag = False

isModule = False


class SendBackThread (threading.Thread):
    def __init__(self, socket_inst):
        threading.Thread.__init__(self)
        self.mySocket = socket_inst
        self.mySocket.settimeout(120)

    def send_msg(self, index_send, server_time_start, time_initial):
        server_duration = time.time() - server_time_start
        index_send = "index: " + index_send + "; server_process_time: "+ str(int(server_duration*1000) + "; client_time_start"+ time_initial)
        self.mySocket.sendall(bytes(index_send, 'utf-8'))

        # socket.write("") -> self.mySocket.sendall(bytes(message, 'utf-8'))

class myThread (threading.Thread):
    def __init__(self, socketInstance, time):
        threading.Thread.__init__(self)
        self.time = time
        self.mySocket = socketInstance
        self.mySocket.settimeout(120)
        
    def run(self):
        
        while True:
            global Latitude
            global Longitude
            global Temperature
            global Height
            global dataTemp
            global dataFlag
            
            try:
                rawData = self.mySocket.recv(8192).decode()
                server_time_start = time.time() # record start time
                print("recv: " + rawData) if not production_env else None

                From = rawData.replace(";",":").split(": ")

                if not production_env or "Phone" in From:

                    rawData = rawData.split("\r\n") if production_env else rawData

                    for dataItem in rawData if production_env else [rawData]:

                        if dataItem != "":

                            if dataFlag:
                                dataItem = dataTemp + dataItem
                                dataTemp = ""
                                dataFlag = False


                            data = dataItem.split("; ")

                            dbData = {

                            }
                            for item in data:
                                if item != "":
                                    items = item.split(": ")
                                    if (len(items) == 2 and items[1] != ""):
                                        if (items[0] == "Time"):
                                            timestr = dbData['Time'] = items[1]
                                            time_initial = items[1]
                                            # print(timestr)
                                            # duration = time.time() - float(timestr)
                                            # print(duration * 1000)
                                            # dbData['sentDurationMs'] = duration * 1000
                                        if (items[0] == "CSQ"):
                                            dbData['CSQ'] = items[1]
                                        if (items[0] == "Index"):
                                            dbData['Index'] = items[1]
                                            index_send = items[1]
                                        if (items[0] == "Height"):
                                            dbData['Height'] = items[1]
                                        if (items[0] == "Lati"):
                                            dbData['Latitude'] = items[1]
                                        if (items[0] == "Long"):
                                            dbData['Longitude'] = items[1]
                                        if (item[0] == "Network"):
                                            dbData['Network'] = items[1]


                            if Latitude != "":
                                dbData['Latitude'] = Latitude
                            if Longitude != "":
                                dbData['Longitude'] = Longitude
                            if Temperature != "":
                                dbData['Temperature'] = Temperature
                            if Height != "":
                                dbData['Height'] = Height

                            if (("Time" in dbData) and ("CSQ" in dbData) and ("Index" in dbData) and ("Height" in dbData)):
                                if production_env:
                                    mongo = client.surf
                                    table = mongo[self.time]
                                    table.insert_one(dbData)
                                    pass
                            else:
                                dataTemp = dataItem
                                dataFlag = True
                            
                if "Module" in From:

                    isModule = True

                    data = rawData.split("; ")

                    for item in data:

                        items = item.split(": ")

                        if len(items) == 2:

                            if (items[0] == "Latitude" and items[1] != ""):
                                Latitude = items[1]

                            if (items[0] == "Longitude" and items[1] != ""):
                                Longitude = items[1]

                            if (items[0] == "Temperature" and items[1] != ""):
                                Temperature = items[1]

                            if (items[0] == "Height" and items[1] != ""):
                                Height = items[1]

                if rawData == "":
                    self.mySocket.shutdown(2)
                    self.mySocket.close()

                    # print("Connection Ended by Client\n")
                    # break
                
                # Start sending back data to Client(Phone)
                newSend = SendBackThread(conn2)
                newSend.send_msg(index_send, server_time_start, time_initial)
                # Send ended

                self.mySocket.sendall(bytes('finish', 'utf-8'))
            except Exception as err:
                self.mySocket.shutdown(2)
                self.mySocket.close()
                print(err)
                break

#Initialize sending and receiving sockets
tcps = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

tcps.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

tcps.bind((host,port_recv))

tcps.listen(1)

send_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

send_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

send_socket.bind((host,port_send))

send_socket.listen(1)
#Initialized

while True:
    print("Waiting for incoming connections\n")
    conn, addr = tcps.accept()
    conn2, addr2 = send_socket.accept()
    dt = datetime.datetime.now()
    currentTime = dt.strftime('%m-%d %H:%M')
    
    print("incoming connection from: ", addr,"\n")
    newThread = myThread(conn, currentTime)
    newThread.start()
    
    

