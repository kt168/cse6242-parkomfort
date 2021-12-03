#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd

import  geopy

from geopy.geocoders import Nominatim

from geopy.extra.rate_limiter import RateLimiter

meter = pd.read_csv(r"C:\Users\jenni\Downloads\NYC Meter info.csv", dtype =str)


# In[4]:


meter


# In[ ]:


geolocator = Nominatim(user_agent="application")

reverse = RateLimiter(geolocator.reverse, min_delay_seconds=1)
location = {}
for pt in zip(meter['LAT'],meter['LONG']):
    location[pt] = reverse(pt, language='en', exactly_one=True)
location

