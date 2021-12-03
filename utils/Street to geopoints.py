#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

import  geopy

from geopy.geocoders import Nominatim

from geopy.extra.rate_limiter import RateLimiter

tickets = pd.read_csv(r"C:\Users\jenni\OneDrive\GaTech\CSE 6242\Parking_Violations_Issued_-_Fiscal_Year_2022.csv")


# In[2]:


from random import randint

tickets['addr'] = tickets['House Number'].fillna('')+' '+ tickets['Street Name'].fillna('')



# In[95]:


def geopt_convert(df):
    from collections import defaultdict
    geopt = defaultdict()
    geolocator = Nominatim(user_agent="ram")
    for addr in df['addr']:  
        #print (addr.strip())
        location = geolocator.geocode(addr.strip(), timeout=10000, language = 'en')
        if location is not None:
            geopt[addr]= (location.latitude,location.longitude)
    print ('Done')
    return geopt
        
    

def combine_df(geopt):
    addr_map = pd.DataFrame(geopt.items(), columns=['addr', 'geopoint'])
    addr_map['latitude'], addr_map['longitude'] = zip(*addr_map.geopoint)
    total = tickets.merge(addr_map, how = 'inner', on = 'addr')
    return total


# In[3]:


all_addr = tickets.groupby('addr')['Summons Number'].count().reset_index().sort_values('Summons Number', ascending = False).head(10000).reset_index(drop=True)


# In[99]:


all_addr_1 = tickets.groupby('addr')['Summons Number'].count().reset_index().sort_values('Summons Number', ascending = False).reset_index(drop=True)

all_addr1 = all_addr_1[(all_addr_1.index>=10000) & (all_addr_1.index<20000) ]


# In[100]:


geopt = geopt_convert(all_addr1)
total2 =  combine_df(geopt)


# In[101]:


total2.to_csv(r"C:\Users\jenni\OneDrive\GaTech\CSE 6242\geopt1.csv", index=False)


# In[102]:


all_addr_2 = tickets.groupby('addr')['Summons Number'].count().reset_index().sort_values('Summons Number', ascending = False).reset_index(drop=True)

all_addr2 = all_addr_2[(all_addr_2.index>=20000) & (all_addr_2.index<30000) ]


# In[103]:


geopt = geopt_convert(all_addr2)
total3 =  combine_df(geopt)


# In[104]:


total3.to_csv(r"C:\Users\jenni\OneDrive\GaTech\CSE 6242\geopt2.csv", index=False)


# In[112]:


all_addr_3 = tickets.groupby('addr')['Summons Number'].count().reset_index().sort_values('Summons Number', ascending = False).reset_index(drop=True)

all_addr3 = all_addr_3[(all_addr_3.index>=30000) & (all_addr_3.index<50000) ]


# In[113]:


geopt = geopt_convert(all_addr3)
total4 =  combine_df(geopt)


# In[118]:


all_addr_5 = tickets.groupby('addr')['Summons Number'].count().reset_index().sort_values('Summons Number', ascending = False).reset_index(drop=True)

all_addr5 = all_addr_5[(all_addr_5.index>=60000) & (all_addr_5.index<80000) ]


# In[ ]:


geopt = geopt_convert(all_addr5)
total5 =  combine_df(geopt)


# In[ ]:


df = pd.concat([total,total2,total3, total4, total5]).reset_index(drop=True)


# In[ ]:


len(df)


# In[117]:


df.to_csv(r"C:\Users\jenni\OneDrive\GaTech\CSE 6242\geopt_partial_parking.csv", index=False)

