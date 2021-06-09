#!/usr/bin/env python
# coding: utf-8

# In[1]:


import smtplib, ssl
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import json
import time
from datetime import datetime, date, timedelta


# In[4]:


driver = webdriver.Chrome("C:/Users/rahul/Downloads/chromedriver_win32/chromedriver.exe")
t1 = time.time()


# In[ ]:


while True:
    
    t2 = time.time()
    if t2-t1<60:
        time.sleep(60-(t2-t1))
    t1 = time.time()
    
    print('New loop Time: ' + str(datetime.now().strftime("%H:%M:%S")))
    try:
        link = "https://slotalert.herokuapp.com/slot/getfulldata"
        driver.get(link)
        pre = driver.find_element_by_tag_name("body").text
        web_data = json.loads(pre)
        web_data

        for day in [1,2,5,1,4,3]:
            print("Check: " + str(day))

            today = date.today()
            today += timedelta(days=day)
            dt = today.strftime("%d-%m-%y")

            for distt in web_data.keys():
                if len(web_data[distt])>0:

                    while True:

                        link = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}".format(distt, dt)
                        driver.get(link)
                        pre = driver.find_element_by_tag_name("pre").text

                        if pre[0:12] == '{"sessions":':
                            break
                        
                        print("Sleeping due to too many requests")
                        time.sleep(60)


                    data = json.loads(pre)


                    for pinc in web_data[distt].keys():
                        for cent in data['sessions']:

                            if str(cent['pincode']) == str(pinc):
                                for user in web_data[distt][pinc].keys():

                                    if (web_data[distt][pinc][user]['d1']=='True' and cent['available_capacity_dose1'] > 0) or (web_data[distt][pinc][user]['d2']=='True' and cent['available_capacity_dose2'] > 0):
                                        if (web_data[distt][pinc][user]['eight']=='True' and cent['min_age_limit']== 18) or (web_data[distt][pinc][user]['five']=='True' and cent['min_age_limit']==45):

                                            if (web_data[distt][pinc][user]['free']=='True' and cent['fee_type']=='Free') or (web_data[distt][pinc][user]['paid']=='True' and cent['fee_type']=='Paid'):
                                                if (web_data[distt][pinc][user]['cvsh']=='True' and cent['vaccine']=='COVISHIELD') or (web_data[distt][pinc][user]['covax']=='True' and cent['vaccine']=='COVAXIN') or (web_data[distt][pinc][user]['sptk']=='True' and cent['vaccine']=='SPUTNIK V'):
                                                    if cent['center_id'] not in web_data[distt][pinc][user]['slot'][str(day)]:

                                                        driver.get('https://slotalert.herokuapp.com/slot/putdata/{}/{}/{}/'.format(user, day, cent['center_id']))
                                                        print('Updated: /putdata/{}/{}/{}/'.format(user, day, cent['center_id']))
                                                        print('Pin: ' + str(cent['pincode']))

    except:
        print("Sleeping due to error")
        time.sleep(10)

