#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 00:01:11 2020

@author: gilmandelbaum
"""
import pandas as pd 
import numpy  as np

"""
#direction column reports choice to R (right), L (left), or TO (time out)
"""

def define_current_choice_direction(behavior_data_trial):
    conditions = [
        behavior_data_trial['iSpout'].eq(1) & behavior_data_trial['sSelection'].eq(1),
        behavior_data_trial['iSpout'].eq(1) & behavior_data_trial['sSelection'].eq(2),
        behavior_data_trial['iSpout'].eq(1) & behavior_data_trial['sSelection'].eq(3),
        behavior_data_trial['iSpout'].eq(0) & behavior_data_trial['sSelection'].eq(1),
        behavior_data_trial['iSpout'].eq(0) & behavior_data_trial['sSelection'].eq(2),
        behavior_data_trial['iSpout'].eq(0) & behavior_data_trial['sSelection'].eq(3)]

    behavior_data_trial['direction'] = np.select(conditions, ["R","L","TO","L","R","TO"])
    
    return behavior_data_trial


"""
add a column that reports if the previous trial(s) was rewarded or not 

"""

def get_previous_rewarded_or_not(df, HowManyBack):
    
    p_list = list(range(1, HowManyBack+1))
    
    Reward_data = df['iReward'].values.tolist()
    rew = df.iReward.unique().tolist()
    rew.remove(0)

    total= []  
    
    for previous in p_list:       
        new_index = df.index.values+previous
        new_index= new_index.tolist()
        df_prev = pd.DataFrame(index= new_index)
        df_prev['-'+str(previous)+'_r'] = Reward_data      
        total.append(df_prev)       
        
    df_prev_all = pd.concat(total, axis =1)
    df_prev_all=df_prev_all.replace(rew, 1)
    df_prev_all=df_prev_all.replace([0], 2)
    
    string_p_list =[]
    for i in p_list:
        string_p_list.append('-'+str(i)+'_r') 
    string_p_list = list(reversed(string_p_list))    
    df_prev_all =  df_prev_all[string_p_list]

    final_df = pd.concat([df, df_prev_all], axis=1, join= 'inner') 
    
    return final_df


"""
add a column that reports if the previous direction of choice was the same or not.
a helper function for 
get_previous_choice_direction_same_or_not below. 

"""


def define_previous_choice_direction_same_or_not(df):   
    
    df['SamePastDirection'] = np.nan    
    for row in df.iterrows():        
        try:
            prev_trial  = row[0]-1
            direc_prev_trial = df.loc[prev_trial, ['direction']][0]
            current_prev_trial = row[1]['direction']    
            
            if current_prev_trial == 'TO':
                
                df.at[row[0], 'SamePastDirection'] = 3#Time Out
                
            elif direc_prev_trial=='TO':
                df.at[row[0], 'SamePastDirection'] = 3#Time Out
                
            elif current_prev_trial != 'TO':
                if current_prev_trial == direc_prev_trial:
                    df.at[row[0], 'SamePastDirection'] = 1#same
                else:
                    df.at[row[0], 'SamePastDirection'] = 2#not same 

        except:
            pass
        
    return df



"""
add a column that reports if the previous direction of choice(s) was the same or not 


"""

def get_previous_choice_direction_same_or_not(df, HowManyBack):
    
    df = define_previous_choice_direction_same_or_not(df)
    
    p_list = list(range(1, HowManyBack+1))
    sameDirection_data = df['SamePastDirection'].values.tolist()
    total= []    
    for previous in p_list:       
        new_index = df.index.values+previous-1
        new_index= new_index.tolist()
        df_prev = pd.DataFrame(index= new_index)
        df_prev['-'+str(previous)+'_d'] = sameDirection_data      
        total.append(df_prev)       
        
    df_prev_all = pd.concat(total, axis =1)
    string_p_list =[] 
    for i in p_list:
        string_p_list.append('-'+str(i)+'_d') 
    string_p_list = list(reversed(string_p_list))    
    df_prev_all =  df_prev_all[string_p_list]    

    final_df = pd.concat([df, df_prev_all], axis=1, join= 'inner')      
    
    return final_df



