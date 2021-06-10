#!/usr/bin/env python
# coding: utf-8

# In[1]:

import time
from datetime import datetime, date, timedelta
import requests
from playsound import playsound


# In[4]:

t1 = time.time()

# In[ ]:


while True:
    
    t2 = time.time()
    if t2-t1<60:
        time.sleep(60-(t2-t1))
    t1 = time.time()
    
    print('New loop Time: ' + str(datetime.now().strftime("%H:%M:%S")))
    
    try:
        response = requests.get("https://slotalert.herokuapp.com/slot/getfulldata")
        web_data = response.json()

        for day in [1,2,3,4,1,5]:
            print("Check: " + str(day))

            today = date.today()
            today += timedelta(days=day)
            dt = today.strftime("%d-%m-%y")

            for distt in web_data.keys():
                if len(web_data[distt])>0:

                    while True:

                        response = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}".format(distt, dt))
                        data = response.json()
                        
                        if 'sessions' in data.keys():
                            break
                        
                        playsound('C:/Users/rahul/OneDrive/Desktop/Ensoniq-ZR-76-01-Dope-77.wav')
                        print("Too many requests")
                        time.sleep(1)


                    for pinc in web_data[distt].keys():
                        for cent in data['sessions']:

                            if str(cent['pincode']) == str(pinc):
                                for user in web_data[distt][pinc].keys():

                                    if (web_data[distt][pinc][user]['d1']=='True' and cent['available_capacity_dose1'] > 0) or (web_data[distt][pinc][user]['d2']=='True' and cent['available_capacity_dose2'] > 0):
                                        if (web_data[distt][pinc][user]['eight']=='True' and cent['min_age_limit']== 18) or (web_data[distt][pinc][user]['five']=='True' and cent['min_age_limit']==45):

                                            if (web_data[distt][pinc][user]['free']=='True' and cent['fee_type']=='Free') or (web_data[distt][pinc][user]['paid']=='True' and cent['fee_type']=='Paid'):
                                                if (web_data[distt][pinc][user]['cvsh']=='True' and cent['vaccine']=='COVISHIELD') or (web_data[distt][pinc][user]['covax']=='True' and cent['vaccine']=='COVAXIN') or (web_data[distt][pinc][user]['sptk']=='True' and cent['vaccine']=='SPUTNIK V'):
                                                    if cent['center_id'] not in web_data[distt][pinc][user]['slot'][str(day)]:

                                                        put = requests.get('https://slotalert.herokuapp.com/slot/putdata/{}/{}/{}/'.format(user, day, cent['center_id']))
                                                        print('Updated: /putdata/{}/{}/{}/'.format(user, day, cent['center_id']))
                                                        print('Pin: ' + str(cent['pincode']))

    except:
        print("Sleeping due to error")
        time.sleep(5)
