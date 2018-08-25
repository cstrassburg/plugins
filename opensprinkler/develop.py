from plugins.opensprinkler import OpenSprinkler
class SmartHome():
    class Scheduler():
        def add(self,name, obj, cycle):
            print (name,obj,cycle)

    scheduler = Scheduler()

if __name__ == '__main__':



#    num= 1
 #   print(bit(num, 0) + bit(num, 1) + bit(num, 2) + bit(num, 3) + bit(num, 4) + bit(num, 5) + bit(num, 6) + bit(num, 7))
    sh = SmartHome()
    os = OpenSprinkler(sh=sh, username= '',host='192.168.0.190',port = 8080 , cycle=300, password='a6d82bced638de3def1e9bbb4983225c')
    #os = OpenSprinkler(sh=sh, username= '',host='raspberrypi.nhw16',port = 8080 , cycle=300, password='opendoor')
    os.run()
    #os.readAllVars()
    os.readStatus()
    #os.printtest()


    #os.setOn(7)
    #os.setOff(7)
    #os.printtest()
    #os.fetchCommand(commands['change_values'],'&rsn=1')
    #os.readAllVars()
    #os.enableSystem()
    #os.disableSystem()
    os.readSystemStatus()

    #print(os.toMD5("opendoor") )
   # print (os.toSHA512("opendoor") )

    #data = '{"devt":1483828655,"nbrd":1,"en":1,"rd":0,"rs":0,"rdst":0,"loc":"52.51925,9.76590","wtkey":"","sunrise":510,"sunset":986,' \
    #       '"eip":1505139458,"lwc":1483827636,"lswc":1483813228,"lrun":[3,1,600,1483767601],"sbits":[0,0],' \
    #       '"ps":[[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],"wto":{},"ifkey":""}'
    #response = json2obj(data)
    #print(response.en)

