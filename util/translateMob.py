# coding=utf-8

import translateAPI as transAPI

class MobFileHandler:

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

    def fread_stringE(self):
        ret_str = ""
        done=True
        
        while(done):
            line=self.fp.readline()

            if(line=='E\n'):
                done=False
            else:
                ret_str+=line

        return ret_str

    def save_mob_file(self, ofname, translate):

        if(self.mobsinfo is None): 
            print('mobinfos is not ready. parse first')
            return
        ofp = open(ofname, "w")
        if(translate):         translator = transAPI.SeleniumTranslate()

        for mob in self.mobsinfo:
            print('\t translating ' + mob['number'] + ' by ' + str(id(translator))+ ' to ' + ofname)
            ofp.write('#'+mob['number']+"\n")
            ofp.write(mob['alias_list']+'~'+"\n")
            if(translate):  
                ofp.write(translator.translate(mob['short_description'])+'~'+"\n")
                ofp.write(translator.translate(mob['long_description'])+'\n'+'~'+"\n")
                ofp.write(translator.translate(mob['detail_description'])+'\n'+'~'+"\n")
            else:           
                ofp.write(mob['short_description']+'~'+"\n")
                ofp.write(mob['long_description']+'\n'+'~'+"\n")
                ofp.write(mob['detail_description']+'\n'+'~'+"\n")
            ofp.write(mob['attributes']+'\n')
            ofp.write(mob['attr01']+'\n')
            ofp.write(mob['attr02']+'\n')
            ofp.write(mob['attr03']+'\n')

            if(self.mobinfo['attributes'].endswith('E')):
                if(len(mob['attr04'])>0): ofp.write(mob['attr04'])
                ofp.write('E\n')

            if('trigger' in mob):
                ofp.write(mob['trigger'])

        ofp.write('$'+'\n')
        ofp.close()
        translator.quit()



    def parse_mob_file(self, ifname):
        fname = ifname
        self.fp = open(fname, "r")
        if(self.fp is None): return None

        loop=True
        line_cnt=0

        self.mobsinfo=list()

        while(loop):
            line_cnt+=1
            line=self.fp.readline()
            if(line==''): loop=False

            line=line.rstrip()

            if(line.startswith('#')): 
                self.mobinfo=dict()
                
                self.mobinfo['number']=line.replace('#',"")
                self.mobinfo['alias_list']=self.fread_string()
                self.mobinfo['short_description']=self.fread_string()
                self.mobinfo['long_description']=self.fread_string()
                self.mobinfo['detail_description']=self.fread_string()
                self.mobinfo['attributes']=self.fp.readline().rstrip()
                self.mobinfo['attr01']=self.fp.readline().rstrip()
                self.mobinfo['attr02']=self.fp.readline().rstrip()
                self.mobinfo['attr03']=self.fp.readline().rstrip() 

                if(self.mobinfo['attributes'].endswith('E')):
                    self.mobinfo['attr04']=self.fread_stringE()

                self.mobsinfo.append(self.mobinfo)
                

            elif(line.startswith('T')):
                if('trigger' not in self.mobinfo):
                    self.mobinfo['trigger']=''
                self.mobinfo['trigger']+=line
                self.mobinfo['trigger']+='\n'

            elif(line.startswith('$')): 
                # print('completed')
                return

            else:
                print("ERROR : " + ifname + ' ' + str(line_cnt)+" "+line)

        self.fp.close() 
            



import subprocess
import threading
import sys
import util_threadpool as tp
from time import sleep    
import glob
from os.path import basename

if __name__ == "__main__":
    

    ipath = '../lib/world/mob/'
    opath = '../lib/world/mob_ko/'

    number_of_instance = 1
    pool = tp.ThreadPool(number_of_instance)

    files = glob.glob(ipath+'*.mob')
    for file in files:

        ofile = opath+basename(file)
        try:
            line = subprocess.check_output(['tail', '-1', ofile])
            line = line.decode("utf-8") 
        except:
            line = 'ok'
            
        # Skip already finished files even though this application is restarted.
        if( line != '$' and line != '$\n'):
            mobHandler = MobFileHandler()
            mobHandler.parse_mob_file(file)
            

            pool.add_task(mobHandler.save_mob_file, opath+basename(file), translate=True)
            sleep(1)

        else:
            print('skipping '+opath+basename(file))
    
    pool.wait_completion()    

    print("Jobs done!")    
    
