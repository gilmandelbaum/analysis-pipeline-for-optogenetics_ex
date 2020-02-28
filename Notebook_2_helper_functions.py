#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 12:50:21 2020

@author: gilmandelbaum
"""

import pandas as pd 
import numpy  as np


#define state transitions:
#ENL
state_ENL = [(23, 29), (29, 30), (30, 30), (30, 32), (32, 33), (33, 33), (33, 29), (30,38)]
state_ENL_and_ENLpenalties = [(29, 30), (29, 32), (30, 30), (30, 32), (31, 32), (32, 33), (33, 33), (33, 29)]
state_ENLp = [(29, 32), (30, 32)]#, (31, 32), (32, 33), (32, 32), (30, 33), (33, 33)]

#Cue and Selection Time
state_Cue_to_Selection = [(38, 39), (38, 41), (39, 39), (39, 41), (41, 42), (42, 42)]+[(39, 47), (47, 48), (48, 48), (48, 49)]
state_Selection =[(39, 47), (47, 48), (48, 48), (48, 49)]
#Selection 
state_SelectRew=[(47,50), (48, 50)]
state_SelectNonRew=[(47, 54), (48, 54)]

#Consumption
state_collectRew=[(53, 53),(50, 51), (51, 51), (51, 52), (52, 53), (53, 61)] 
state_NonRew= [(55, 55), (54, 55), (55, 56)]

states_EndOfTrial_notIdentified= [(61, 82), (82, 62), (62, 63), (55, 61), (63, 78),  (78, 66), (66, 75), (58, 61), (58, 58), (75, 16)]
states_StartOfTrial_notIdentified = [(20, 21), (21,14), (14, 24), (24, 25), (25, 27), (27, 23), (16, 20), (63, 20)]
states_FreeRewards = [(63, 93), (93, 94), (94, 94), (94, 95), (95, 96), (96, 96), (96, 20)]
state_TO = [(58, 58)]



def get_nTrial_DataLick_list(session):
    block=1
    nTrial= 0
    l=[]
    
    for row in session.iterrows(): 
        (iblock, iTrial)= (row[1]["iBlock"], row[1]["iTrial"])
        if iblock!=block:
            block+=1
            nTrial+=(iTrial)
            l.append((nTrial))
        else:
            if iTrial>nTrial:
                nTrial+=(iTrial-nTrial)
                l.append((nTrial))

            elif iTrial<nTrial:
                nTrial+= iTrial - (session.get_value(row[0]-1, "iTrial"))
                l.append((nTrial))
            else:
                l.append((nTrial))
    session["nTrial"]= l
    return session




def tag_RealFullTrial(data_lick):
    data_lick = data_lick.reset_index(drop=True)
    Consump_NonRewarded_rows_list = []
    Non_defined_state_list = []
    RestOfBins = data_lick.copy()
    
    for states in state_collectRew+state_NonRew+states_EndOfTrial_notIdentified+states_FreeRewards: #Take out free rewards (after you take the trials)
        state_start = states[0]
        state_end = states[1]
        
        #this state is sometimes aligned with trial n and sometimes to n-1 so to account for this...
        if (state_start, state_end)== (75, 16): 
            Non_defined_state_list.append(data_lick.loc[(data_lick['sTrial_start'] == state_start) & (data_lick['sTrial_end'] == state_end)])
        else:   
            Consump_NonRewarded_rows_list.append(data_lick.loc[(data_lick['sTrial_start'] == state_start) & (data_lick['sTrial_end'] == state_end)])
        RestOfBins = RestOfBins[~((RestOfBins['sTrial_start'] == state_start) & (RestOfBins['sTrial_end'] == state_end))]
        
    Consumption_NonRewarded_rows = pd.concat(Consump_NonRewarded_rows_list)
    Consumption_NonRewarded_rows = Consumption_NonRewarded_rows.sort_index()
    
    Consumption_NonRewarded_rows['R_nTrials_CNR']=Consumption_NonRewarded_rows['nTrial']+1
    Consumption_NonRewarded_df = pd.DataFrame(Consumption_NonRewarded_rows['R_nTrials_CNR'])

    RestOfBins['R_nTrials_RoB']= RestOfBins['nTrial']
    RestOfBins_df = pd.DataFrame(RestOfBins['R_nTrials_RoB'])

    df_Real_nTrials = pd.concat([Consumption_NonRewarded_df, RestOfBins_df], axis= 1)
    
    arr = df_Real_nTrials.values
    df_Real_nTrials['Real_nTrials_1'] = arr[~np.isnan(arr)].astype(int)
    df_Real_nTrials = df_Real_nTrials.drop(['R_nTrials_CNR', 'R_nTrials_RoB'], axis=1)
    
    #still accounting for weird state
    Non_defined_state = pd.concat(Non_defined_state_list)
    Non_defined_state = Non_defined_state.sort_index()
    df_prevTrial= df_Real_nTrials[df_Real_nTrials.index.isin(Non_defined_state.index-1)]
    df_prevTrial['new_index'] = df_prevTrial.index+1
    Non_defined_state_df = df_prevTrial.set_index('new_index')
    Non_defined_state_df.index.name=None
    Non_defined_state_df.columns=['non_defined']
    
    df_Real_nTrials = pd.concat([df_Real_nTrials, Non_defined_state_df], axis= 1)
    arr = df_Real_nTrials.values
    df_Real_nTrials['Real_nTrials'] = arr[~np.isnan(arr)].astype(int)
    df_Real_nTrials = df_Real_nTrials.drop(['Real_nTrials_1', 'non_defined'], axis=1)
    
    Final_df = pd.concat([data_lick, df_Real_nTrials], axis=1)
    return Final_df

