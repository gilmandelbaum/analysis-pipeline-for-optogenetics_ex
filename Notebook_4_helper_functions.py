#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 16:00:16 2020

@author: gilmandelbaum
"""
import pandas as pd



#fuction that adds a flag 

def tag_period(beh_photo_align, period_name, states_list):
    
    Period_rows_list = []

    for states in states_list:
        state_start = states[0]
        state_end = states[1]
        Period_rows_list.append(beh_photo_align.loc[(beh_photo_align['sTrial_start'] == state_start) & (beh_photo_align['sTrial_end'] == state_end)])
        
    Period_rows = pd.concat(Period_rows_list)
    Period_rows = Period_rows.sort_index()
    
    Period_rows[period_name]=Period_rows['Real_nTrials']
    Period_df = pd.DataFrame(Period_rows[period_name])
    return Period_df



