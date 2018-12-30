# coding=utf-8
import requests
 


text="The river is deep, and runs swiftly in an east-west direction.  To the north the river eddies and enters a backwash where a small bank extends down from a dark, thick stand of trees.  It doesn't look particularly inviting however"
 

################################################################################
# NAVER PAPAGO API
################################################################################
# 
# request_url = "https://openapi.naver.com/v1/papago/n2mt"
# headers= {
#             "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
#             "X-Naver-Client-Id": "{api-id}",
#             "X-Naver-Client-Secret": "{api-secret}"
#         }
# params = {"source": "en", "target": "ko", "text": text}
# response = requests.post(request_url, headers=headers, data=params)
# print(response.text)
# result = response.json()
 
# print(result)

################################################################################
# KAKAO API
################################################################################
# 
# def Translate(text):

#     if(len(text)<=1): return ''
    
#     request_url = "https://kapi.kakao.com/v1/translation/translate"
#     url_params = {
#         "src_lang":"en", 
#         "target_lang":"kr",
#         "query" : text
#         }

#     headers = {
#         "Host": "kapi.kakao.com",
#         "Authorization": "KakaoAK {api-key}"
#     }

#     response = requests.get(request_url, headers=headers, params=url_params)

#     # 응답메시지의 Body를 JSON 객체에 담는다.
#     result = response.json()

#     print(result)
#     # 응답결과가 여러 문장을 담고 있으면 모두 합치고, 두 문장 사이에 공백문자를 하나 추가한다.
#     merged=' '.join(str(elem) for elem in result['translated_text'][0])

#     # DEBUG
#     # print(merged)

#     return merged



################################################################################
# SELENIUM API
################################################################################
import numpy as np
from selenium import webdriver
import time

class SeleniumTranslate():
    def __init__(self):
        self.driver = webdriver.Chrome('./webDriver/chromedriver')

    def translate(self, query):
        return self.translate_with_lang(query, 'ko')

    def translate_with_lang(self, query, language):

        if(len(query)<=1): return ''
        myLang = language.lower()

    
        # Construct the complete URL to search
        base_url = 'https://translate.google.com/#'
        from_lang = 'en'
        final_url = base_url + from_lang + '/' + myLang
        xpath='/html/body/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/div/span[1]/span'
               

        # Perform operation to detect the translated text
        self.driver.set_page_load_timeout(30)        # Incase Page doesn't load
        self.driver.get(final_url)                   # Search the URL
        self.driver.find_element_by_id('source').send_keys(query.lower()) 
        time.sleep(1)
        err_cnt=0
        while(True):
            try:           
                text_output = self.driver.find_element_by_xpath(xpath)
            except:
                # print('retrying' + '(' + str(err_cnt) + ')')
                err_cnt+=1

                if(err_cnt > 5):
                    # If the string is too much long, google translate returns with slightly different way
                    xpath='/html/body/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/div/span[1]'
                if(err_cnt > 10):
                    print('[ERROR] Translation : 10 Retries has been failed')
                    return '[[[[[[[[TRANSLATION FAILED]]]]]]]]]]'

                time.sleep(1)
                continue
                # return ''
            else:
                err_cnt=0
                xpath='/html/body/div[2]/div[1]/div[2]/div[1]/div[1]/div[2]/div[2]/div[1]/div[2]/div/span[1]/span'
            break

        time.sleep(1)   # Else it does not print the data
 
        return str(text_output.text)
    
    def quit(self):
        self.driver.quit()


# if __name__ == '__main__':
#     myInput = 'What can I do this?'
#     language = 'ko'
#     translated_text = translate('Through this tunnel', language)
#     print(translated_text)
#     translated_text = translate('Entrance to the castle', language)
#     print(translated_text)
    
#     driver.quit()




from os import listdir
from os.path import isfile, join


class WorldFileHandler:

    def __init__(self, path):
        self.path=path
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

        translator = SeleniumTranslate()
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
        fname = self.path + ifname
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
            

import subprocess
import threading
import sys
import util_threadpool as tp
from time import sleep    

if __name__ == "__main__":
    

    ipath = '../lib/world/wld/'
    opath = '../lib/world/wld_ko/'

    number_of_instance = 5
    pool = tp.ThreadPool(number_of_instance)

    
    files=listdir(ipath)
    for file in files:

        ofile = opath+file
        try:
            line = subprocess.check_output(['tail', '-1', ofile])
            line = line.decode("utf-8") 
        except:
            line = 'ok'
            
        # Skip already finished files even though this application is restarted.
        if( line != '$~' and line != '$~\n'):
            wldHandler = WorldFileHandler(ipath)
            wldHandler.parse_world_file(file)
            # print('translating '+file)
            pool.add_task(wldHandler.save_world_file, '../lib/world/wld_ko/'+file, translate=True)
            sleep(1)

        else:
            print('skipping '+file)
    
    pool.wait_completion()    

    print("Jobs done!")    
    
        # cnt+=1
        # if(cnt==1): break




    
