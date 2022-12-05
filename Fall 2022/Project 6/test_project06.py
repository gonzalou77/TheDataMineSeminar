import pytest
import pandas as pd
import hashlib
import os

from project06 import find_longest_timegap, space_in_dir, event_plotter, player_info

def test_find_longest_timegap():
    weather = pd.read_csv("/anvil/projects/tdm/etc/time_sample.csv")
    
    assert find_longest_timegap(weather['observation_time']) == 23.75
    

def test_space_in_dir():
    assert space_in_dir("/anvil/projects/tdm/bin") == 338665316
    

def test_event_plotter():
    
    results = event_plotter("Swimming Men's 100 metres Backstroke")
    
    with open(f"{os.getenv('HOME')}/gold.jpeg", 'rb') as g:
        my_bytes = g.read()
        m = hashlib.sha256()
        m.update(my_bytes)
        gold = m.hexdigest()
            
    with open(f"{os.getenv('HOME')}/silver.jpeg", 'rb') as s:
        my_bytes = s.read()
        m = hashlib.sha256()
        m.update(my_bytes)
        silver = m.hexdigest()
        
    with open(f"{os.getenv('HOME')}/bronze.jpeg", 'rb') as b:
        my_bytes = b.read()
        m = hashlib.sha256()
        m.update(my_bytes)
        bronze = m.hexdigest()
        
    assert gold == '7dacb73d8f1f84e1a01d84d3ac05449813c6a12a316b723d3cb273bbee1dc60f'
    assert results.loc[(results['Medal']=='Gold') & (results['NOC']=='USA'),'Age'].values[0] == 21.066666666666666
    assert bronze == '363a6fed2372a0dcab9ab5429daa1f78e5b236004612c3dcfbcae901f2d8329a'
    assert silver == '9b8af11195fdef3dbe4b136854dab83c6216dc52012fb5796c8e7db14dc35022'
    
def test_player_info():
    info = player_info("vinicius junior")
    assert info=='Name: Vinicius Júnior\nBirthday: July 12, 2000\nTotal goals: 37'