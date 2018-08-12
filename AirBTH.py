from firebase import firebase
import threading
import datetime
import socket
import bluetooth
import time

MacLocalAdd = 'B8:27:EB:75:8E:06'

global conection, phone, BdFirebase, ica25 , ica10, Icaso2
ica25  = 0
ica10  = 0
Icaso2 = 0

BdFirebase = firebase.FirebaseApplication('https://calidad-cdc99.firebaseio.com/',None)
def search():
    devices= bluetooth.discover_devices(duration = 5, lookup_names = True) 
    return devices

time.sleep(1)
a = True
while a:
    results = search()

    print (results)
    if (('14:3E:BF:5F:A2:D6', 'Z959') in results):
        a = False
if (('14:3E:BF:5F:A2:D6', 'Z959') in results):
    print ('Bth connection detected')
    port = 1
    backlog = 1
    size = 1024
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM )
    s.bind((MacLocalAdd,port))
    s.listen(backlog)
    print ('ESTAMOS MELOS??')
    try:
        client, address = s.accept()
        print('SISAS SISAS')

        while 1:
            try:
                
                data = client.recv(size)
                if data:
                    print (data)
                    data =data.decode('utf-8')
                    data = data.replace('b','')
                    data= data.split(',')
                    
                    if data[0] == 'PM10':
                        BdFirebase.put('/usuarioZ/','PM10',float(data[1]))

                        
                        if(float(data[1])<=54):
                            ica10= (49/99)*(float(data[1]))
                        elif(float(data[1])>=55 and float(data[1])<=154):
                            ica10= (49/99)*(float(data[1])-55)+51
                        elif(float(data[1])>=155 and float(data[1])<=254):
                            ica10= (49/99)*(float(data[1])-155)+101
                        else:
                            ica10= (49/99)*(float(data[1])-255)+151
                            
                    elif data[0]  == 'PM25':
                        BdFirebase.put('/usuarioZ/','PM25',float(data[1]))
                         
                        if(float(data[1])<=12):
                            ica10= (49/12)*(float(data[1]))
                        elif(float(data[1])>=12.1 and float(data[1])<=34.5):
                            ica25= (49/(35.4-12-1))*(float(data[1])-12.1)+51
                        elif(float(data[1])>=35.5 and float(data[1])<=55.4):
                            ica25= (49/(55.4-35-5))*(float(data[1])-35.4)+101
                        else:
                            ica25= (49/(150.4-55.5))*(float(data[1])-55.5)+151
                        

                    else:
                        BdFirebase.put('/usuarioZ/','SO2',float(data[1]))
                         
                        if(float(data[1])<=0.035):
                            ica10= (49/0.035)*(float(data[1]))
                        elif(float(data[1])>=0.036 and float(data[1])<=0.075):
                            Icaso2= (49/(0.075-0.036))*(float(data[1])-0.036)+51
                        elif(float(data[1])>=0.076and float(data[1])<=0.185):
                            Icaso2= (49/(0.185)-0.076)*(float(data[1])-0.076)+101
                        else:
                            Icaso2= (49/(0.304-0.186))*(float(data[1])-0.186)+151

                    
                    Icaponderado= ((ica10+ica25+Icaso2)/3)
                    BdFirebase.put('/usuarioZ/','QAIR',Icaponderado)
                    if (Icaponderado < 50):
                        BdFirebase.put('/usuarioZ/','ALERTA',1)
                    elif (Icaponderado < 100):
                        BdFirebase.put('/usuarioZ/','ALERTA',2)
                    elif (Icaponderado < 150):
                        BdFirebase.put('/usuarioZ/','ALERTA',3)
                    elif (Icaponderado < 200):
                        BdFirebase.put('/usuarioZ/','ALERTA',4)

            except Exception as e:
                print('datos')
                pass
               
                                            
    except Exception as e:
        print(e)
        client.close()
        s.close()



    
















                

    
