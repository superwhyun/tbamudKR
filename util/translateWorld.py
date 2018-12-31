# coding=utf-8

import translateAPI as transAPI

class WorldFileHandler:

    def __init__(self):
        
        self.fp = None
        pass

    def fread_string(self):
        ret_str = ""
        done=True
        
        while(done):
            line=self.fp.readline().rstrip()

            if(line.endswith('~')):
                ret_str+=line
                ret_str = ret_str.replace('~',"")
                done=False
                
            else:
                ret_str+=line
                ret_str+=" "

        return ret_str

    
    def parse_room_field(self, room_number):
        room_info=dict()
        
        room_info["number"]=room_number
        done=True
        while(done):
            room_info["name"] = self.fread_string()
            room_info["description"] = self.fread_string()
            room_info["roomflag"]=self.fp.readline().rstrip()

            done=False

        return room_info

    def parse_direction_field(self, dir_number):  
        dir_info=dict()

        dir_info["direction_number"] = dir_number
        dir_info["direction_description"] = self.fread_string()
        dir_info["direction_keyword"] = self.fread_string()
        dir_info["direction_attributes"] = self.fp.readline().rstrip() # door_flag key_number room_linked

        return dir_info

    def parse_extra_field(self):
        extra_info=dict()

        extra_info["keywords"] = self.fread_string()
        extra_info["descriptions"] = self.fread_string()

        return extra_info

    
    def save_world_file(self, ofname, translate):

        if(self.world_info is None): 
            print('world info is not ready. parse first')
            return

        if(translate): translator = transAPI.SeleniumTranslate()
        
        print('processing ' + ofname + 'by ' + str(id(translator)) )
        ofp = open(ofname, "w")

        for room in self.world_info:

            
            ofp.write('#'+room['number']+"\n")

            if(translate): 
                print('\t translating ' + room['number'] + ' by ' + str(id(translator))+ ' to ' + ofname)
                ofp.write(translator.translate(room['name'])+'~'+"\n")
                ofp.write(translator.translate(room['description'])+'\n'+'~'+"\n")
            else:          
                ofp.write(room['name']+'~'+"\n")
                ofp.write(room['description']+'\n'+'~'+"\n")
            ofp.write(room['roomflag']+'\n')
            
            if('direction' in room):
                for dir in room['direction']:
                    ofp.write(dir['direction_number']+'\n')
                    if(translate):
                        if(len(dir['direction_description'])>1):
                            ofp.write(translator.translate(dir['direction_description'])+'\n'+'~'+'\n')
                        else:
                            ofp.write('~'+'\n')
                    else:
                        ofp.write(dir['direction_description']+'\n'+'~'+'\n')
                    ofp.write(dir['direction_keyword']+'~'+'\n')
                    ofp.write(dir['direction_attributes']+'\n')
            
            if('extra' in room):
                for extra in room['extra']:
                    ofp.write('E'+'\n')
                    ofp.write(extra['keywords']+'~'+'\n')

                    if(translate):
                        if(len(extra['descriptions'])>1):
                            ofp.write(translator.translate(extra['descriptions'])+'\n'+'~'+'\n')
                        else:
                            ofp.write('~'+'\n')
                    else:
                        ofp.write(extra['descriptions']+'\n'+'~'+'\n')

            ofp.write('S'+'\n')

            if('trigger' in room):
                ofp.write(room['trigger']+'\n')

        ofp.write('$~')

        ofp.close()
        print('completed')
        translator.quit()
        return True




    def parse_world_file(self, ifname):

        # print('parsing ' + ifname + '.....')
        fname = ifname
        self.fp = open(fname, "r")
        if(self.fp is None): return None

        loop=True
        line_cnt=0
        self.world_info=list()
        while(loop):
            line_cnt+=1
            line=self.fp.readline()
            if(line==''): loop=False

            line=line.rstrip()
            
            if(line.startswith('#')): 
                roominfo=self.parse_room_field(line.replace('#',""))
                
            elif(line.startswith('D')):
                dirinfo=self.parse_direction_field(line)
                if("direction" not in roominfo):
                    roominfo["direction"]=list()
                roominfo["direction"].append(dirinfo)
    
            elif(line.startswith('E')): 
                extrainfo=self.parse_extra_field()
                if("extra" not in roominfo):
                    roominfo["extra"]=list()
                roominfo["extra"].append(extrainfo)

            elif(line.startswith('S')):    
                self.world_info.append(roominfo)
                # print(roominfo)
            elif(line.startswith('T')):
                    roominfo['trigger']=line

            elif(line.startswith('$~')): 
                # print('.........ok')
                loop=False

            else:
                print("ERROR : " + str(line_cnt)+" "+line)
        
        self.fp.close()


import subprocess
import threading
import sys
import util_threadpool as tp
from time import sleep    
import glob
from os.path import basename

if __name__ == "__main__":
    

    ipath = '../lib/world/wld/'
    opath = '../lib/world/wld_ko/'

    number_of_instance = 5
    pool = tp.ThreadPool(number_of_instance)

    files = glob.glob(ipath+'*.wld')
    for file in files:

        ofile = opath+file
        try:
            line = subprocess.check_output(['tail', '-1', ofile])
            line = line.decode("utf-8") 
        except:
            line = 'ok'
            
        # Skip already finished files even though this application is restarted.
        if( line != '$~' and line != '$~\n'):
            wldHandler = WorldFileHandler()
            wldHandler.parse_world_file(file)
            # print('translating '+file)
            pool.add_task(wldHandler.save_world_file, opath+basename(file), translate=True)
            sleep(1)

        else:
            print('skipping '+file)
    
    pool.wait_completion()    

    print("Jobs done!")    
    
        # cnt+=1
        # if(cnt==1): break




    
