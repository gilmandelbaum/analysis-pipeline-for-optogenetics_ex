#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 14:30:28 2020

@author: gilmandelbaum
"""


import os 
import papermill as pm




def make_nb_list(List_of_versions,List_of_versions_str):
    nb_list = []
    for nb,nb_str in zip(List_of_versions,List_of_versions_str):
        #print (nb_str)
        #print (nb)
        for i in range(0,len(nb)):
            nb_version = nb_str+"_"+nb[i]
            nb_list.append(nb_version)
    return (nb_list)       
            
#Make String with notebook+version sequence path
def make_sequence_string(nb_seq, list_of_versions):
    string=''
    for i in range(0, len(nb_seq)):
        nb_number = nb_seq[i]
        string+=str(nb_number)
        version= list_of_versions[i]
        if len(version)==1:
            v= version
            string+=v
        else:
            for v in version:
                string+=v
    print ("seq"+string+" "+"will be used")
    return (string)





def generate_date_(Date):
    return('20'+str(Date)[:2]+'_'+str(Date)[2:4]+'_'+str(Date)[4:6])

def generate_name_and_date(Date,Mouse):
    return ('20'+str(Date)[:2]+'_'+str(Date)[2:4]+'_'+str(Date)[4:6]+'__'+Mouse)


def run_dataset (Mouse_Date_FileName,nb_list,nb_path,seq_str,dict_for_pm):   
    
    folder_name_dict = {"0": "Nb_0x_pre_analysis",
                        "1": "Nb_1x_define_trials_of_interest",
                        "2": "Nb_2x_import_lick_data",
                        "4": "Nb_4x_assign_licks_to_behavioral_states",
                        "5": "Nb_5x_form_one_structure_with_all_data",
                        "6": "Nb_6x_extract_specific_information"}
    
    #generate 3 lists.
    l_mouse = list(Mouse_Date_FileName["Mouse"]) 
    l_date_ = list(Mouse_Date_FileName.apply(lambda x: generate_date_(x["Date"]),axis=1))  
    l_date_and_name = list(Mouse_Date_FileName.apply(lambda x: generate_name_and_date(x["Date"],x["Mouse"]),axis=1))
 
    
    data_dir_output = dict_for_pm["data_dir_output"]
    HowManyBack = dict_for_pm["HowManyBack"]
    #these are the 3 variables that change each session (what we will call the outer loop)
    for (mouse, date_, date_and_name) in zip(l_mouse, l_date_, l_date_and_name):
        
        for notebook in nb_list: 
            
            notebook_number = notebook[2]
            notebook_version = notebook[-1]
            folder_name = folder_name_dict[notebook_number]

            
            #make notebook path: 
            if notebook_number in ["0","1","2","3","4"]:
                notebook_path = ""
            elif notebook_number == "5": 
                notebook_path = "_seq"+seq_str[:seq_str.index('6')]
            else:
                notebook_path = '_seq'+seq_str


            if os.path.isfile(data_dir_output+"/"+mouse+"/"+date_and_name+'/'+str(HowManyBack)+'_Back/'+mouse+"_"+date_+'Notebook_'+str(notebook_number)+'_'+notebook_version+notebook_path+'.pickle'):
                pass
                print(mouse+"_"+date_+'_Notebook_'+str(notebook_number)+'_'+notebook_version+notebook_path+': This session already exists - no need to re-run ;)')
            
            else:
                #if we need to run the notebook we need to add 3 keys to the dict_for_pm. 
                
                dict_for_pm["mouse"]=mouse 
                #dict_for_pm["date_and_name"]=date_and_name
                #dict_for_pm["date_"]=date_
                dict_for_pm["data_day"]=date_and_name
                dict_for_pm["date"]=date_
                
                print('Notebook_'+notebook_number+'_'+notebook_version+'.ipynb is being executed')
                pm.execute_notebook(nb_path+folder_name+"/"+'Notebook_'+str(notebook_number)+'_'+notebook_version+'.ipynb', 'TestOutPut.ipynb',kernel_name = "optogenetics_env", parameters= dict_for_pm,nest_asyncio=True)
    return 



