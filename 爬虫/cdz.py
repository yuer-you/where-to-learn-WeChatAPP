import pandas as pd
import csv
import os
import shutil


class to_csv():
    result=0
    def read_txt(self):
        fileHandler  =  open  ("data.txt",  "r",encoding='utf-8')
        while  True:
            # Get next line from file
            line  =  fileHandler.readline()
            # If line is empty then end of file reached
            if  not  line  :
                break;
            else:
                self.pp_txt(line)

        fileHandler.close()
    def pp_txt(self,line):
        line=line.split("&")
        line = [x.strip() for x in line]
        line[1],line[2]=line[2],line[1]
        if(line[0]=="思源楼"):
            line[0]='sy'
            self.mkdir(line[0])    

            if(len(line[2])>3):
                line[2]=line[2][2:]
            self.ppp_txt(line)
        elif(line[0]=="思源西楼"):
            line[0]='sx'
            self.mkdir(line[0])    

            if(len(line[2])>3):
                line[2]=line[2][2:]
            self.ppp_txt(line)
        elif(line[0]=="思源东楼"):
            line[0]='sd'
            self.mkdir(line[0])
            if(len(line[2])>3):
                
                line[2]=line[2][2:]
            print(line)
            if(int(line[2])==102):
                result=1
            self.ppp_txt(line)
        elif(line[0]=="逸夫楼"):
            line[0]='yf'
            self.mkdir(line[0])
            if(len(line[2])>3):
                
                line[2]=line[2][2:]
                if(len(line[2])>3):
                    line[2]=line[2][1:]
            if(len(line[2])==3 and int(line[2])<=706):
                self.ppp_txt(line)
        elif(line[0]=="机械楼"):
            line[0]='z'
            self.mkdir(line[0])
            if(len(line[2])>3):
                line[2]=line[2][1:]
            if(int(line[2])<=310):
                self.ppp_txt(line)
        elif(line[0]=="九教"):
            line[0]='nine'

            self.mkdir(line[0])
            if(line[2]=="东102"):
                line[2]=6102
                self.ppp_txt(line)
            elif(line[2]=="中102"):
                line[2]=5102
                self.ppp_txt(line)
            elif( line[2]=="东201" or line[2]=="东203"):
                line[2]='6'+line[2][1:]
                self.ppp_txt(line)
        elif(line[0]=="东区一教"):
            line[0]='dq'

            self.mkdir(line[0])
            if(len(line[2])>3):
                line[2]=line[2][2:]
            if(not line[2]=="201" and not line[2]=="401"):
                self.ppp_txt(line)
        elif(line[0]=="十七教（建艺）"):
            line[0]='art'
            self.mkdir(line[0])
            self.ppp_txt(line)
        elif(line[0]=="八教"):
            line[0]='eight'
            self.mkdir(line[0])
            if(len(line[2])==4 and int(line[2])<=8208):
                self.ppp_txt(line)
    def ppp_txt(self,line):
        line[1]=line[1].replace('/','.')
        path=line[0]+"/"+line[1]+".csv"
        self.mkdir_csv(path,line[2:])
    def mkdir(self,path):
	    folder = os.path.exists('./data/'+path)
	    if not folder:                   
		    os.makedirs('./data/'+path)         
    def mkdir_csv(self,path,content):
        if(os.path.isfile('./data/'+path)):
            with open('./data/'+path,'a',encoding='utf8',newline='') as f :
                writer = csv.writer(f)
                writer.writerow(content)
        else:
            with open('./data/'+path,'w',encoding='utf8',newline='') as f :
                writer = csv.writer(f)
                writer.writerow(["classroom","1","2","3","4","5","6","7"])
                writer.writerow(content)

        


if __name__ == "__main__":
    filepath = './data/'
    if  os.path.isdir(filepath):
        shutil.rmtree("./data/")
    to_csv=to_csv()
    to_csv.read_txt()
