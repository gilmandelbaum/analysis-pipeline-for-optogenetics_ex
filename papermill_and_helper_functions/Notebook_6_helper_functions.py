#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 14:44:51 2020

@author: gilmandelbaum
"""
import itertools
import pandas as pd


"""
general
"""

def make_combinations (HowManyBack):
    combinations =list(itertools.product([2,1], repeat=HowManyBack*2))
    return (combinations)

def combinations_string(HowManyBack):
    combinations = make_combinations (HowManyBack)
    total=[]
    for i in combinations:
        total.append(''.join(str(e) for e in i))    
    return total


"""
for notebook 6_a and for 6_b
"""

def get_tStates_perTrial_per_period_df(data):
    BehPhoto = data.copy()
    final_list = []
    for rl in BehPhoto:
        rl_list = []
        for ic in rl:
            ic_list =[]
            for combo in ic:
                ic_list.append(get_tStates_perTrial_per_period_helper(combo))
            rl_list.append(ic_list)
        final_list.append(rl_list)
        
        #side = 'L'
        
    return final_list


"""
for notebook 6_a and for 6_b
"""
def get_tStates_perTrial_per_period_helper(combo): #this has the trials in columns  
    combo_dict = dict()
    try:
        for key, value in combo.items():
            Real_nTrials_list = combo['Real_nTrials']['Real_nTrials'].unique().tolist() 
            period_str = key
            period_data = value
   
            total_ntrials_df=[]
            ntrials = period_data[period_str].unique()
            
            for i in ntrials:
                total_ntrials_df.append(period_data[period_data[period_str]==i])
         
            df_list = []
            
            
            for trial_i in range(0, len(total_ntrials_df)):
                trial = total_ntrials_df[trial_i]
                ntrial = ntrials[trial_i]
                new_df = pd.DataFrame(trial['tState']).reset_index(drop=True)    
                new_df.columns = [ntrial]            
                df_list.append(new_df)
                
           
            basic_df = pd.DataFrame(columns = Real_nTrials_list)
            try:
                df_AllTrials = pd.concat(df_list, axis=1)
                df_AllTrials = pd.concat([basic_df, df_AllTrials])
                combo_dict[period_str] = df_AllTrials
            except:
                combo_dict[period_str]= basic_df 
    except:
        pass
    return combo_dict


"""
for notebook 6_b
"""

def count_licks_perPeriod(data_tStates_perTrial):
    total =[]
    for rl in data_tStates_perTrial:
        rl_list = []
        for ic in rl:
            ic_list = []
            for combo in ic:
                combo_dict = {}
                for key, value in combo.items():
                    combo_dict[key] = value.count().values
                ic_list.append(combo_dict)
            rl_list.append(ic_list)
        total.append(rl_list)
    return total



"""
for notebook 6_b
"""

def count_licks_perPeriod_make_df(LickCount_perTrial,combination_stringlist):
    total =[]
    for rl in LickCount_perTrial:
        rl_list = []
        for ic in rl:
            ic_list = []
            for combo in ic:
                #combo_dict = {}
                df = pd.DataFrame.from_dict(combo)
                ic_list.append(df)
            df_allcombos = pd.concat(ic_list, axis=1, keys=combination_stringlist)
            rl_list.append(df_allcombos)
        df_ipsicontra = pd.concat(rl_list, axis=1, keys=['ipsi', 'contra'])
        total.append(df_ipsicontra)
    df_final = pd.concat(total, axis=1, keys=['R', 'L'])
    return df_final




"""
for notebook 6_c
"""

def count_licks_perPeriod_with_direction_helper(combo): #this has the trials in columns  
    combo_dict = dict()
    try:
        for key, value in combo.items():
            #Real_nTrials_list = combo['Real_nTrials']['Real_nTrials'].unique().tolist() 
            period_str = key
            period_data = value
            #print(period_str)
            total_ntrials_df=[]
            try:
                ntrials = period_data[period_str].unique()

                for i in ntrials:
                    total_ntrials_df.append(period_data[period_data[period_str]==i])
                    #print(i)   
                df_list = []

                for trial_i in range(0, len(total_ntrials_df)):
                    trial = total_ntrials_df[trial_i]
                    #ntrial = ntrials[trial_i]


                    Right_Licks =  len(trial[trial['iSpout']==2])
                    Left_Licks = len(trial[trial['iSpout']==1])


                    v= [Right_Licks, Left_Licks]
                    df = pd.DataFrame(v).transpose()
                    df.columns= ['R', 'L']
                    df_list.append(df)
                combo_dict[period_str] = pd.concat(df_list)
            
        
            except:
                df = pd.DataFrame(columns=['R', 'L'])
                combo_dict[period_str] = df

    except:
        print(key)
        pass
    column_labels=[]
    df_list=[]
    for key, value in combo_dict.items():
        column_labels.append(key)
        value.columns = pd.MultiIndex.from_product([[key], ['R','L']])
        value= value.reset_index(drop=True)
        df_list.append(value)
    df= pd.concat(df_list, axis=1)
    return df


"""
for notebook 6_c
"""

def count_licks_perPeriod_with_direction(data):
    BehPhoto = data.copy()
    final_list = []
    for rl in BehPhoto:
        rl_list = []
        for ic in rl:
            ic_list =[]
            for combo in ic:
                ic_list.append(count_licks_perPeriod_with_direction_helper(combo))
            rl_list.append(ic_list)
        final_list.append(rl_list)
        
        #side = 'L'
        
    return final_list

"""
for notebook 6_c
"""

def count_licks_perPeriod_with_direction_make_df(LickCount_perTrial,combination_stringlist):
    total =[]
    for rl in LickCount_perTrial:
        rl_list = []
        for ic in rl:
            #ic_list = []
            df_allcombos = pd.concat(ic, axis=1, keys=combination_stringlist)
            rl_list.append(df_allcombos)
        df_ipsicontra = pd.concat(rl_list, axis=1, keys=['ipsi', 'contra'])
        total.append(df_ipsicontra)
    df_final = pd.concat(total, axis=1, keys=['R', 'L'])
    return df_final






