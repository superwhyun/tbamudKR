# coding=utf-8

import requests
 
 

################################################################################
# NAVER PAPAGO API
################################################################################

class PapagoTranslate():
    def __init__(self):
        pass

    def Translate(self, text):    
        request_url = "https://openapi.naver.com/v1/papago/n2mt"
        headers= {
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "X-Naver-Client-Id": "{api-id}",
                    "X-Naver-Client-Secret": "{api-secret}"
                }
        params = {"source": "en", "target": "ko", "text": text}
        response = requests.post(request_url, headers=headers, data=params)
        print(response.text)
        result = response.json()
        
        return result

################################################################################
# KAKAO API
################################################################################

class KakaoTranslate():
    def __init__(self):
        pass

    def Translate(self, text):

        if(len(text)<=1): return ''
        
        request_url = "https://kapi.kakao.com/v1/translation/translate"
        url_params = {
            "src_lang":"en", 
            "target_lang":"kr",
            "query" : text
            }

        headers = {
            "Host": "kapi.kakao.com",
            "Authorization": "KakaoAK {api-key}"
        }

        response = requests.get(request_url, headers=headers, params=url_params)

        # 응답메시지의 Body를 JSON 객체에 담는다.
        result = response.json()

        print(result)
        # 응답결과가 여러 문장을 담고 있으면 모두 합치고, 두 문장 사이에 공백문자를 하나 추가한다.
        merged=' '.join(str(elem) for elem in result['translated_text'][0])

        # DEBUG
        # print(merged)

        return merged



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



