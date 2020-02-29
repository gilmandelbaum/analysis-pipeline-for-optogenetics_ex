
from pathlib import Path
import pickle
import pandas as pd 


"""
general to load a pickle data set
"""

def loadSession_pickle (Mouse_Date_FileName,data_dir_output,HowManyBack,folder_name,seq_str,file_name): 

    data_list = list()

    for row in Mouse_Date_FileName.iterrows():
        
        dfPerSession = row[1]
        mouse = dfPerSession["Mouse"]
        date = dfPerSession["Date"]
        
        __mouse = "__"+mouse
        data_day= '20'+str(date)[:2]+'_'+str(date)[2:4]+'_'+str(date)[4:6]
        
        root = Path(data_dir_output+"/"+mouse+"/"+data_day+__mouse+'/'+str(HowManyBack)+"_Back")
        #print (mouse+"/"+data_day)
        d = folder_name+"_"+seq_str+"/"+file_name+'.pickle'
        
        my_path = root / d 
        # open a file, where you stored the pickled data
        fileToOpen = open(my_path, 'rb')
        #print (fileToOpen)
        # dump information to that file
        
        
        data = pickle.load(fileToOpen)
        data_list.append(data)
        
    return (data_list)


"""
general to load a csv data set
"""

def loadSession_csv (Mouse_Date_FileName,data_dir_output,HowManyBack,folder_name,seq_str,file_name): 

    data_list = list()

    for row in Mouse_Date_FileName.iterrows():
        
        dfPerSession = row[1]
        mouse = dfPerSession["Mouse"]
        date = dfPerSession["Date"]
        
        __mouse = "__"+mouse
        data_day= '20'+str(date)[:2]+'_'+str(date)[2:4]+'_'+str(date)[4:6]
        
        root = data_dir_output+"/"+mouse+"/"+data_day+__mouse+'/'+str(HowManyBack)+"_Back/"
        #print (mouse+"/"+data_day)
        d = folder_name+"_"+seq_str+"/"+file_name+'.csv'
        
        data = pd.read_csv(root+d)
        data_list.append(data)
        
    return (data_list)


def loadSession_from_rawdata_xls (Mouse_Date_FileName,data_dir_input): 
    #Mouse_Date_FileName_c = len(Mouse_Date_FileName)
    data_list = list()
    counter = 0 
    for row in Mouse_Date_FileName.iterrows():
        #print (counter)
        dfPerSession = row[1]
        mouse = dfPerSession["Mouse"]
        #__mouse = "__"+mouse
        date = dfPerSession["Date"]
        data_day= '20'+str(date)[:2]+'_'+str(date)[2:4]+'_'+str(date)[4:6]
        
        
        #import trial by trial data from behavioral system:
        #behavior_data_trial = []
        behavior_data_trial = pd.read_excel(data_dir_input+"/"+mouse+"/"+data_day+"__"+mouse+"/"+mouse+"_dataTrial_label.xlsx")
        #Add a column to each of these data frames to define its date, which mouse it is and make the trial column the index.  
        behavior_data_trial["Date"]= date
        behavior_data_trial["Mouse"]= mouse
        behavior_data_trial=behavior_data_trial.set_index("nTrial")
        data_list.append(behavior_data_trial)
        counter = counter +1
    return (data_list)



"""
used in data_set_stimSuccessRate notebook
"""
def stimSuccessRate (dataSet,Mouse_Date_FileName): 
    
    dataSet_c=len(dataSet)
    
    dfResults = pd.DataFrame({'mouse': [],"date": [],"D": [],"SideOfStim": [],
                              'licksStim': [],"licksOtherSide": [], "licksStimControl": [], 
                              "licksOtherSideControl": []})

    for i in range (dataSet_c):
    
        sessionInfo = Mouse_Date_FileName.iloc[i,:]
        mouse = sessionInfo["Mouse"] 
        date = sessionInfo["Date"]
        cellType = sessionInfo["D"]
        sideOfStim = sessionInfo["SideOfStim"]        
        dataSetPerSession = dataSet[i]
    
        if cellType==1:
            
            if sideOfStim =="R":
                licksStim = len(dataSetPerSession["L"]["ipsi"]["12"].dropna())
                licksOtherSide = len(dataSetPerSession["R"]["ipsi"]["11"].dropna())
                licksStimControl = len(dataSetPerSession["R"]["ipsi"]["12"].dropna())
                licksOtherSideControl = len(dataSetPerSession["L"]["ipsi"]["11"].dropna())
            elif sideOfStim =="L":
                licksStim = len(dataSetPerSession["R"]["ipsi"]["12"].dropna())
                licksOtherSide = len(dataSetPerSession["L"]["ipsi"]["11"].dropna())
                licksStimControl = len(dataSetPerSession["L"]["ipsi"]["12"].dropna())
                licksOtherSideControl = len(dataSetPerSession["R"]["ipsi"]["11"].dropna())
       
        if cellType==2:   
            if sideOfStim =="R":
                licksStim = len(dataSetPerSession["R"]["ipsi"]["12"].dropna())
                licksOtherSide = len(dataSetPerSession["L"]["ipsi"]["11"].dropna())
                licksStimControl = len(dataSetPerSession["L"]["ipsi"]["12"].dropna())
                licksOtherSideControl = len(dataSetPerSession["R"]["ipsi"]["11"].dropna())
            elif sideOfStim =="L":
                licksStim = len(dataSetPerSession["L"]["ipsi"]["12"].dropna())
                licksOtherSide = len(dataSetPerSession["R"]["ipsi"]["11"].dropna())
                licksStimControl = len(dataSetPerSession["R"]["ipsi"]["12"].dropna())
                licksOtherSideControl = len(dataSetPerSession["L"]["ipsi"]["11"].dropna())
    
    
        dfResults.loc[i] = pd.Series({'mouse': mouse,"date": date ,"D": cellType,"SideOfStim": sideOfStim,
                                      'licksStim':licksStim,"licksOtherSide":licksOtherSide, 
                                      "licksStimControl":licksStimControl,
                                      "licksOtherSideControl":licksOtherSideControl})
                             
    df = dfResults.rename (columns={"licksStim": "stimSwit", "licksOtherSide": "stimNoSwit",
                                    "licksStimControl":"controlSwit","licksOtherSideControl":"controlNoSwit"})
    
    return (df)
    


"""
used in data_set_response_times
"""

def extract_data_set (Mouse_Date_FileName,rt_stay_right,rt_switch_right,rt_stay_left,rt_switch_left): 
    
    dfResults = pd.DataFrame(columns = ['mouse',"date","D","SideOfStim",
                                        "switchSide_switch",
                                        "switchSide_Stay",
                                        "NOswitchSide_switch",
                                        "NOswitchSide_Stay"])
    
    
    leng = len (rt_stay_right)
    
    for i in range (leng):
        
        sessionInfo = Mouse_Date_FileName.iloc[i,:]
        mouse = sessionInfo["Mouse"] 
        date = sessionInfo["Date"]
        cellType = sessionInfo["D"]
        sideOfStim = sessionInfo["SideOfStim"]  
        
        if rt_stay_right[i].empty: 
            rt_stay_right_i = 0 
        else:  
            rt_stay_right_i = rt_stay_right[i][0].median()
            
        if rt_switch_right[i].empty:
            rt_switch_right_i = 0 
        else: 
            rt_switch_right_i = rt_switch_right[i][0].median()
            
        if rt_stay_left[i].empty:
            rt_stay_left_i = 0 
        else:   
            rt_stay_left_i = rt_stay_left[i][0].median()
        
        if rt_switch_left[i].empty:
            rt_switch_left_i = 0 
        else: 
            rt_switch_left_i = rt_switch_left[i][0].median()
    
        
        
        if cellType==1:
            
            if sideOfStim =="R":
                switchSide_switch = rt_switch_left_i
                switchSide_Stay = rt_stay_right_i
                
                NOswitchSide_switch = rt_switch_right_i
                NOswitchSide_Stay = rt_stay_left_i
                
            elif sideOfStim =="L":
                
                switchSide_switch = rt_switch_right_i
                switchSide_Stay = rt_stay_left_i
                
                NOswitchSide_switch = rt_switch_left_i
                NOswitchSide_Stay = rt_stay_right_i
                
        if cellType==2:
            
            if sideOfStim =="R":
                
                switchSide_switch = rt_switch_right_i
                switchSide_Stay = rt_stay_left_i
                
                NOswitchSide_switch = rt_switch_left_i
                NOswitchSide_Stay = rt_stay_right_i
                
            elif sideOfStim =="L":
            
                switchSide_switch = rt_switch_left_i
                switchSide_Stay = rt_stay_right_i
                
                NOswitchSide_switch = rt_switch_right_i
                NOswitchSide_Stay = rt_stay_left_i 
                
                
        dfResults.loc[i] = pd.Series({'mouse': mouse,"date": date,"D": cellType,
                                      "SideOfStim": sideOfStim,
                                      'switchSide_switch': switchSide_switch,
                                      "switchSide_Stay": switchSide_Stay, 
                                      "NOswitchSide_switch": NOswitchSide_switch, 
                                      "NOswitchSide_Stay": NOswitchSide_Stay})
        
    return (dfResults)



"""
used in data_set_lick_direction
"""



def stimLickDirections (dataSet,Mouse_Date_FileName): 
    
    dataSet_c=len(dataSet)
    
    dfResults = pd.DataFrame({'mouse': [],"date": [],"D": [],"SideOfStim": [],
                              'Switch_StimSide': [],"Switch_NotStimSide": [], 
                              "NoSwitch_StimSide": [], "NoSwitch_NotStimSide": [],
                              "ControlSwitch_StimSide": [],"ControlSwitch_NotStimSide":[],
                              "ControlNOSwitch_StimSide":[],"ControlNOSwitch_NotStimSide":[]})

    
    #c = Mouse_Date_FileName.index.values.tolist()
    
    for i in range (dataSet_c):
    
        sessionInfo = Mouse_Date_FileName.iloc[i,:]
        mouse = sessionInfo["Mouse"] 
        date = sessionInfo["Date"]
        cellType = sessionInfo["D"]
        sideOfStim = sessionInfo["SideOfStim"]        
        dataSetPerSession = dataSet[i]
    
        if cellType==1:
            
            if sideOfStim =="R":
                
                Switch_StimSide = dataSetPerSession["R"]["contra"]["12"]["Reward_NoReward_tag"]["R"].mean()
                Switch_NotStimSide = dataSetPerSession["R"]["contra"]["12"]["Reward_NoReward_tag"]["L"].mean()
                ###
                NoSwitch_StimSide = dataSetPerSession["R"]["ipsi"]["11"]["Reward_NoReward_tag"]["R"].mean()
                NoSwitch_NotStimSide = dataSetPerSession["R"]["ipsi"]["11"]["Reward_NoReward_tag"]["L"].mean()
                ###
                ControlSwitch_StimSide = dataSetPerSession["R"]["ipsi"]["12"]["Reward_NoReward_tag"]["L"].mean()
                ControlSwitch_NotStimSide = dataSetPerSession["R"]["ipsi"]["12"]["Reward_NoReward_tag"]["R"].mean()
                ###
                ControlNOSwitch_StimSide = dataSetPerSession["R"]["contra"]["11"]["Reward_NoReward_tag"]["L"].mean()
                ControlNOSwitch_NotStimSide = dataSetPerSession["R"]["contra"]["11"]["Reward_NoReward_tag"]["R"].mean()
                
      
            elif sideOfStim =="L":
                
                Switch_StimSide = dataSetPerSession["L"]["contra"]["12"]["Reward_NoReward_tag"]["L"].mean()
                Switch_NotStimSide = dataSetPerSession["L"]["contra"]["12"]["Reward_NoReward_tag"]["R"].mean()
                ###
                NoSwitch_StimSide = dataSetPerSession["L"]["ipsi"]["11"]["Reward_NoReward_tag"]["L"].mean()
                NoSwitch_NotStimSide = dataSetPerSession["L"]["ipsi"]["11"]["Reward_NoReward_tag"]["R"].mean()
                ###
                ControlSwitch_StimSide = dataSetPerSession["L"]["ipsi"]["12"]["Reward_NoReward_tag"]["R"].mean()
                ControlSwitch_NotStimSide = dataSetPerSession["L"]["ipsi"]["12"]["Reward_NoReward_tag"]["L"].mean()
                
                ControlNOSwitch_StimSide = dataSetPerSession["L"]["contra"]["11"]["Reward_NoReward_tag"]["R"].mean()
                ControlNOSwitch_NotStimSide = dataSetPerSession["L"]["contra"]["11"]["Reward_NoReward_tag"]["L"].mean()
                
                
                
        if cellType==2:   
            if sideOfStim =="R":
                
                Switch_StimSide = dataSetPerSession["R"]["ipsi"]["12"]["Reward_NoReward_tag"]["L"].mean()
                Switch_NotStimSide = dataSetPerSession["R"]["ipsi"]["12"]["Reward_NoReward_tag"]["R"].mean()
                ###
                NoSwitch_StimSide = dataSetPerSession["R"]["contra"]["11"]["Reward_NoReward_tag"]["L"].mean()
                NoSwitch_NotStimSide = dataSetPerSession["R"]["contra"]["11"]["Reward_NoReward_tag"]["R"].mean()
                ###
                ControlSwitch_StimSide = dataSetPerSession["R"]["contra"]["12"]["Reward_NoReward_tag"]["R"].mean()
                ControlSwitch_NotStimSide = dataSetPerSession["R"]["contra"]["12"]["Reward_NoReward_tag"]["L"].mean()
                ##
                ControlNOSwitch_StimSide = dataSetPerSession["R"]["ipsi"]["11"]["Reward_NoReward_tag"]["R"].mean()
                ControlNOSwitch_NotStimSide = dataSetPerSession["R"]["ipsi"]["11"]["Reward_NoReward_tag"]["L"].mean()
                
            elif sideOfStim =="L":
            
                Switch_StimSide = dataSetPerSession["L"]["ipsi"]["12"]["Reward_NoReward_tag"]["R"].mean()
                Switch_NotStimSide = dataSetPerSession["L"]["ipsi"]["12"]["Reward_NoReward_tag"]["L"].mean()
                ###
                NoSwitch_StimSide = dataSetPerSession["L"]["contra"]["11"]["Reward_NoReward_tag"]["R"].mean()
                NoSwitch_NotStimSide = dataSetPerSession["L"]["contra"]["11"]["Reward_NoReward_tag"]["L"].mean()
                ###
                ControlSwitch_StimSide = dataSetPerSession["L"]["contra"]["12"]["Reward_NoReward_tag"]["L"].mean()
                ControlSwitch_NotStimSide = dataSetPerSession["L"]["contra"]["12"]["Reward_NoReward_tag"]["R"].mean()
                ###
                ControlNOSwitch_StimSide = dataSetPerSession["L"]["ipsi"]["11"]["Reward_NoReward_tag"]["L"].mean()
                ControlNOSwitch_NotStimSide = dataSetPerSession["L"]["ipsi"]["11"]["Reward_NoReward_tag"]["R"].mean()
                
        
        dfResults.loc[i] = pd.Series({'mouse': mouse,"date": date,"D": cellType,"SideOfStim": sideOfStim,
                                      'Switch_StimSide': Switch_StimSide,"Switch_NotStimSide": Switch_NotStimSide, 
                                      "NoSwitch_StimSide": NoSwitch_StimSide, "NoSwitch_NotStimSide": NoSwitch_NotStimSide,
                                      "ControlSwitch_StimSide": ControlSwitch_StimSide,"ControlSwitch_NotStimSide":ControlSwitch_NotStimSide,
                                      "ControlNOSwitch_StimSide":ControlNOSwitch_StimSide,"ControlNOSwitch_NotStimSide":ControlNOSwitch_NotStimSide})
        
        
       
    return (dfResults)
    