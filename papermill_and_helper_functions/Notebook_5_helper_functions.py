#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 20:55:32 2020

@author: gilmandelbaum
"""

import pickle


def add_pickles (Tags):
    add_pickle = []
    for i in range(len(Tags)):
        tag = Tags[i]+".pickle"
        add_pickle.append(tag)
    return (add_pickle)


def combine_processed_data_and_tags (Tags,behavior_data_lick,root):
    Tags_pickles = add_pickles (Tags)
    
    for i in range(len(Tags_pickles)):
        d = Tags_pickles[i]
        my_path = root / d 
        fileToOpen = open(my_path, 'rb')
        behavior_data_lick[Tags[i]] = pickle.load(fileToOpen)
        
    return behavior_data_lick


def behavior_data_lick_split(behavior_data_lick, listofTrial_RIC_LIC):
    total=[]
    for rl in listofTrial_RIC_LIC:
        rl_l=[]
        for ic in rl:
            ic_l=[]
            for combo in ic:
                periods_dic={}
                #iterate over new flags so we create dictionary with all periods
                for period in behavior_data_lick.loc[:, 'Real_nTrials':].columns:
                    periods_dic[period] = behavior_data_lick[behavior_data_lick[period].isin(combo)]
                ic_l.append(periods_dic)                
            rl_l.append(ic_l)
        total.append(rl_l)
    return total 


