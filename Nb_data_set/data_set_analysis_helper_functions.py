
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
        
        root = Path(data_dir_output+"/"+mouse+"/"+data_day+__mouse+'/'+str(HowManyBack)+"_Back"+"/"+"analysis")
        #print (mouse+"/"+data_day)
        d = folder_name+"_"+seq_str+"/"+file_name+'.pickle'
        
        my_path = root / d 
        # open a file, where you stored the pickled data
        fileToOpen = open(my_path, 'rb')
        #print (fileToOpen)
        # dump information to that file
        
        
        data = pickle.load(fileToOpen)
        #data_final= data.drop("Unnamed: 0",axis=1)
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
        
        root = data_dir_output+"/"+mouse+"/"+data_day+__mouse+'/'+str(HowManyBack)+"_Back"+"/"+"analysis"+"/"
        #print (mouse+"/"+data_day)
        d = folder_name+"_"+seq_str+"/"+file_name+'.csv'
        
        data = pd.read_csv(root+d)
        data_final= data.drop("Unnamed: 0",axis=1)
        data_list.append(data_final)
        
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
                
                licksStim= len(dataSetPerSession["L"]["ipsi"]["12"].dropna())
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

def extract_data_set_respose_time (Mouse_Date_FileName,rt_stay_right,rt_switch_right,rt_stay_left,rt_switch_left): 
    
    dfResults = pd.DataFrame(columns = ['mouse',"date","D","SideOfStim",
                                        "switchSide_switch",
                                        "switchSide_Stay",
                                        "NOswitchSide_switch",
                                        "NOswitchSide_Stay"])
    
    
    leng = len (rt_stay_right) #could look at any of the data set lists. 
    
    for i in range (leng):
        
        sessionInfo = Mouse_Date_FileName.iloc[i,:]
        mouse = sessionInfo["Mouse"] 
        date = sessionInfo["Date"]
        cellType = sessionInfo["D"]
        sideOfStim = sessionInfo["SideOfStim"]  
        
        if rt_stay_right[i].empty: 
            rt_stay_right_i = 0 
        else:  
            rt_stay_right_i = rt_stay_right[i].loc[0].median()
            
        if rt_switch_right[i].empty:
            rt_switch_right_i = 0 
        else: 
            rt_switch_right_i = rt_switch_right[i].loc[0].median()
            
        if rt_stay_left[i].empty:
            rt_stay_left_i = 0 
        else:   
            rt_stay_left_i = rt_stay_left[i].loc[0].median()
        
        if rt_switch_left[i].empty:
            rt_switch_left_i = 0 
        else: 
            rt_switch_left_i = rt_switch_left[i].loc[0].median()
    
        
        
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

"""
used in data_set_time_consumption_licks
"""

def extract_data_set_consumption_times (Mouse_Date_FileName,
                                        Reward_NoReward_stay_right,
                                        Reward_NoReward_switch_right,
                                        Reward_NoReward_stay_left,
                                        Reward_NoReward_switch_left): 
    
    
    data_list = list()

    leng=len(Reward_NoReward_stay_right)
    
        
    for i in range (leng):
        
        dfResults = pd.DataFrame(columns = ["switchSide_switch","switchSide_Stay",
                                        "NOswitchSide_switch","NOswitchSide_Stay"])
        
        sessionInfo = Mouse_Date_FileName.iloc[i,:]
        
        cellType = sessionInfo["D"]
        sideOfStim = sessionInfo["SideOfStim"]        
       
        Reward_NoReward_stay_right_i = Reward_NoReward_stay_right[i].median(axis=1)
        Reward_NoReward_switch_right_i = Reward_NoReward_switch_right[i].median(axis=1)
        Reward_NoReward_stay_left_i = Reward_NoReward_stay_left[i].median(axis=1)
        Reward_NoReward_switch_left_i = Reward_NoReward_switch_left[i].median(axis=1)
    
        if cellType==1:
            
            if sideOfStim =="R":
                
                switchSide_switch = Reward_NoReward_switch_left_i
                switchSide_Stay = Reward_NoReward_stay_right_i
                
                NOswitchSide_switch = Reward_NoReward_switch_right_i
                NOswitchSide_Stay = Reward_NoReward_stay_left_i
                
                
      
            elif sideOfStim =="L":
                
                switchSide_switch = Reward_NoReward_switch_right_i
                switchSide_Stay = Reward_NoReward_stay_left_i
                
                NOswitchSide_switch = Reward_NoReward_switch_left_i
                NOswitchSide_Stay = Reward_NoReward_stay_right_i
                
                
            
        if cellType==2:
            
            if sideOfStim =="R":
                
                switchSide_switch = Reward_NoReward_switch_right_i
                switchSide_Stay = Reward_NoReward_stay_left_i
                
                NOswitchSide_switch = Reward_NoReward_switch_left_i
                NOswitchSide_Stay = Reward_NoReward_stay_right_i
                
            elif sideOfStim =="L":
            
                switchSide_switch = Reward_NoReward_switch_left_i
                switchSide_Stay = Reward_NoReward_stay_right_i
                
                NOswitchSide_switch = Reward_NoReward_switch_right_i
                NOswitchSide_Stay = Reward_NoReward_stay_left_i
                
        
        dfResults = pd.DataFrame({'switchSide_switch': switchSide_switch,
                                  "switchSide_Stay": switchSide_Stay, 
                                  "NOswitchSide_switch": NOswitchSide_switch, 
                                  "NOswitchSide_Stay": NOswitchSide_Stay})
        
        
        data_list.append(dfResults)
       
    return (data_list)




def generating_data_set_consumption_times (Mouse_Date_FileName,df_list,condition):
    leng = len(Mouse_Date_FileName)
    df = pd.DataFrame()
    for i in range (leng):
        sessionInfo = Mouse_Date_FileName.iloc[i,:]
        mouse = sessionInfo["Mouse"] 
        date = sessionInfo["Date"]
    
        name = str(mouse)+"_"+str(date)
        
        session = pd.DataFrame(df_list[i][condition])
        session = session.rename(columns={condition: name})
        df = pd.concat([df,session],axis=1, sort=False)
    return (df)




"""
used in data_set_direction_consumption_licks
"""


def extract_data_set_consumption_times_std (Mouse_Date_FileName,
                                        Reward_NoReward_stay_right,
                                        Reward_NoReward_switch_right,
                                        Reward_NoReward_stay_left,
                                        Reward_NoReward_switch_left): 
    
    
    data_list = list()

    leng=len(Reward_NoReward_stay_right)
    
        
    for i in range (leng):
        
        dfResults = pd.DataFrame(columns = ["switchSide_switch","switchSide_Stay",
                                        "NOswitchSide_switch","NOswitchSide_Stay"])
        
        sessionInfo = Mouse_Date_FileName.iloc[i,:]
        
        cellType = sessionInfo["D"]
        sideOfStim = sessionInfo["SideOfStim"]        
       
        Reward_NoReward_stay_right_i_std = Reward_NoReward_stay_right[i].std(axis=1)
        Reward_NoReward_switch_right_i_std = Reward_NoReward_switch_right[i].std(axis=1)
        Reward_NoReward_stay_left_i_std = Reward_NoReward_stay_left[i].std(axis=1)
        Reward_NoReward_switch_left_i_std = Reward_NoReward_switch_left[i].std(axis=1)
        
    
        if cellType==1:
            
            if sideOfStim =="R":
                
                
                switchSide_switch_std = Reward_NoReward_switch_left_i_std
                switchSide_Stay_std = Reward_NoReward_stay_right_i_std
                NOswitchSide_switch_std = Reward_NoReward_switch_right_i_std
                NOswitchSide_Stay_std = Reward_NoReward_stay_left_i_std
                
                
      
            elif sideOfStim =="L":
                
                switchSide_switch_std = Reward_NoReward_switch_right_i_std
                switchSide_Stay_std = Reward_NoReward_stay_left_i_std
                NOswitchSide_switch_std = Reward_NoReward_switch_left_i_std
                NOswitchSide_Stay_std = Reward_NoReward_stay_right_i_std
                
                
            
        if cellType==2:
            
            if sideOfStim =="R":
                
                switchSide_switch_std = Reward_NoReward_switch_right_i_std
                switchSide_Stay_std = Reward_NoReward_stay_left_i_std
                NOswitchSide_switch_std = Reward_NoReward_switch_left_i_std
                NOswitchSide_Stay_std = Reward_NoReward_stay_right_i_std
                
            elif sideOfStim =="L":
            
                switchSide_switch_std = Reward_NoReward_switch_left_i_std
                switchSide_Stay_std = Reward_NoReward_stay_right_i_std
                NOswitchSide_switch_std = Reward_NoReward_switch_right_i_std
                NOswitchSide_Stay_std = Reward_NoReward_stay_left_i_std
                
        
        dfResults = pd.DataFrame({"switchSide_switch_std":switchSide_switch_std,
                                  "switchSide_Stay_std": switchSide_Stay_std,
                                  "NOswitchSide_switch_std":NOswitchSide_switch_std,
                                  "NOswitchSide_Stay_std":NOswitchSide_Stay_std})
        
        
        data_list.append(dfResults)
       
    return (data_list)


def generating_data_set_consumption_times_2 (Mouse_Date_FileName,df_list,condition,tag=''):
    leng = len(Mouse_Date_FileName)
    df = pd.DataFrame()
    for i in range (leng):
        sessionInfo = Mouse_Date_FileName.iloc[i,:]
        mouse = sessionInfo["Mouse"] 
        date = sessionInfo["Date"]
    
        name = str(mouse)+"_"+str(date)+tag
        
        session = pd.DataFrame(df_list[i][condition])
        session = session.rename(columns={condition: name})
        df = pd.concat([df,session],axis=1, sort=False)
    return (df)




def extract_data_set_consumption_directions (Mouse_Date_FileName,
                                        Reward_NoReward_stay_right_directions,
                                        Reward_NoReward_switch_right_directions,
                                        Reward_NoReward_stay_left_directions,
                                        Reward_NoReward_switch_left_directions): 
    
    
    data_list = list()

    leng=len(Reward_NoReward_stay_right_directions)
    
    
        
    for i in range (leng):
        
        dfResults = pd.DataFrame(columns = ["switchSide_switch","switchSide_Stay",
                                        "NOswitchSide_switch","NOswitchSide_Stay"])
        
        sessionInfo = Mouse_Date_FileName.iloc[i,:]
        
        cellType = sessionInfo["D"]
        sideOfStim = sessionInfo["SideOfStim"]        
       
        

        Reward_NoReward_stay_right_i_columns = list(Reward_NoReward_stay_right_directions[i].columns.values)
        Reward_NoReward_stay_right_i_r = (Reward_NoReward_stay_right_directions[i][Reward_NoReward_stay_right_i_columns]==2).sum(axis=1)
        Reward_NoReward_stay_right_i_l = (Reward_NoReward_stay_right_directions[i][Reward_NoReward_stay_right_i_columns]==1).sum(axis=1)
        
        

        Reward_NoReward_switch_right_i_columns = list(Reward_NoReward_switch_right_directions[i].columns.values)
        Reward_NoReward_switch_right_i_r = (Reward_NoReward_switch_right_directions[i][Reward_NoReward_switch_right_i_columns]==2).sum(axis=1)
        Reward_NoReward_switch_right_i_l = (Reward_NoReward_switch_right_directions[i][Reward_NoReward_switch_right_i_columns]==1).sum(axis=1)
        
        
        
        Reward_NoReward_stay_left_i_columns = list(Reward_NoReward_stay_left_directions[i].columns.values)
        Reward_NoReward_stay_left_i_r = (Reward_NoReward_stay_left_directions[i][Reward_NoReward_stay_left_i_columns]==2).sum(axis=1)
        Reward_NoReward_stay_left_i_l = (Reward_NoReward_stay_left_directions[i][Reward_NoReward_stay_left_i_columns]==1).sum(axis=1)
                
        
        
        Reward_NoReward_switch_left_i_columns = list(Reward_NoReward_switch_left_directions[i].columns.values)
        Reward_NoReward_switch_left_i_r = (Reward_NoReward_switch_left_directions[i][Reward_NoReward_switch_left_i_columns]==2).sum(axis=1)
        Reward_NoReward_switch_left_i_l = (Reward_NoReward_switch_left_directions[i][Reward_NoReward_switch_left_i_columns]==1).sum(axis=1)
          
        
        
        
    
        if cellType==1:
            
            if sideOfStim =="R":
                
                
                switchSide_switch_ipsi = Reward_NoReward_switch_left_i_r
                switchSide_switch_contra = Reward_NoReward_switch_left_i_l
                switchSide_switch_total = Reward_NoReward_switch_left_i_r+Reward_NoReward_switch_left_i_l
                switchSide_switch_ratio = Reward_NoReward_switch_left_i_r/switchSide_switch_total
                switchSide_Stay_ipsi = Reward_NoReward_stay_right_i_r
                switchSide_Stay_contra = Reward_NoReward_stay_right_i_l
                switchSide_Stay_total = Reward_NoReward_stay_right_i_r+Reward_NoReward_stay_right_i_l
                switchSide_Stay_ratio = Reward_NoReward_stay_right_i_r/switchSide_Stay_total

                
                NOswitchSide_switch_ipsi = Reward_NoReward_switch_right_i_r
                NOswitchSide_switch_contra = Reward_NoReward_switch_right_i_l
                NOswitchSide_switch_total =Reward_NoReward_switch_right_i_r+Reward_NoReward_switch_right_i_l
                NOswitchSide_switch_ratio =Reward_NoReward_switch_right_i_r/NOswitchSide_switch_total
                NOswitchSide_Stay_ipsi = Reward_NoReward_stay_left_i_r
                NOswitchSide_Stay_contra = Reward_NoReward_stay_left_i_l
                NOswitchSide_Stay_total = Reward_NoReward_stay_left_i_r+Reward_NoReward_stay_left_i_l
                NOswitchSide_Stay_ratio = Reward_NoReward_stay_left_i_r/NOswitchSide_Stay_total
                
                
      
            elif sideOfStim =="L":
                
                
                switchSide_switch_contra = Reward_NoReward_switch_right_i_r
                switchSide_switch_ipsi = Reward_NoReward_switch_right_i_l
                switchSide_switch_total = Reward_NoReward_switch_right_i_l+Reward_NoReward_switch_right_i_r
                switchSide_switch_ratio = Reward_NoReward_switch_right_i_l/switchSide_switch_total
                switchSide_Stay_contra = Reward_NoReward_stay_left_i_r
                switchSide_Stay_ipsi = Reward_NoReward_stay_left_i_l
                switchSide_Stay_total = Reward_NoReward_stay_left_i_l+Reward_NoReward_stay_left_i_r
                switchSide_Stay_ratio = Reward_NoReward_stay_left_i_l/switchSide_Stay_total
                
                NOswitchSide_switch_contra = Reward_NoReward_switch_left_i_r
                NOswitchSide_switch_ipsi = Reward_NoReward_switch_left_i_l
                NOswitchSide_switch_total = Reward_NoReward_switch_left_i_l+Reward_NoReward_switch_left_i_r
                NOswitchSide_switch_ratio = Reward_NoReward_switch_left_i_l/NOswitchSide_switch_total
                NOswitchSide_Stay_contra = Reward_NoReward_stay_right_i_r
                NOswitchSide_Stay_ipsi = Reward_NoReward_stay_right_i_l
                NOswitchSide_Stay_total = Reward_NoReward_stay_right_i_l+Reward_NoReward_stay_right_i_r
                NOswitchSide_Stay_ratio = Reward_NoReward_stay_right_i_l/NOswitchSide_Stay_total
                
            
        if cellType==2:
            
            if sideOfStim =="R":
                
                
                switchSide_switch_ipsi = Reward_NoReward_switch_right_i_r
                switchSide_switch_contra = Reward_NoReward_switch_right_i_l
                switchSide_switch_total = Reward_NoReward_switch_right_i_l+Reward_NoReward_switch_right_i_r
                switchSide_switch_ratio = Reward_NoReward_switch_right_i_l/switchSide_switch_total
                switchSide_Stay_ipsi = Reward_NoReward_stay_left_i_r
                switchSide_Stay_contra = Reward_NoReward_stay_left_i_l
                switchSide_Stay_total = Reward_NoReward_stay_left_i_l+Reward_NoReward_stay_left_i_r
                switchSide_Stay_ratio = Reward_NoReward_stay_left_i_l/switchSide_Stay_total
                
                NOswitchSide_switch_ipsi = Reward_NoReward_switch_left_i_r
                NOswitchSide_switch_contra = Reward_NoReward_switch_left_i_l
                NOswitchSide_switch_total = Reward_NoReward_switch_left_i_l+Reward_NoReward_switch_left_i_r
                NOswitchSide_switch_ratio = Reward_NoReward_switch_left_i_l/NOswitchSide_switch_total
                NOswitchSide_Stay_ipsi = Reward_NoReward_stay_right_i_r
                NOswitchSide_Stay_contra = Reward_NoReward_stay_right_i_l
                NOswitchSide_Stay_total = Reward_NoReward_stay_right_i_l+Reward_NoReward_stay_right_i_r
                NOswitchSide_Stay_ratio = Reward_NoReward_stay_right_i_l/NOswitchSide_Stay_total
                
            elif sideOfStim =="L":
                
                switchSide_switch_contra = Reward_NoReward_switch_left_i_r
                switchSide_switch_ipsi = Reward_NoReward_switch_left_i_l
                switchSide_switch_total = Reward_NoReward_switch_left_i_r+Reward_NoReward_switch_left_i_l
                switchSide_switch_ratio = Reward_NoReward_switch_left_i_r/switchSide_switch_total
                switchSide_Stay_contra = Reward_NoReward_stay_right_i_r
                switchSide_Stay_ipsi = Reward_NoReward_stay_right_i_l
                switchSide_Stay_total=Reward_NoReward_stay_right_i_r+Reward_NoReward_stay_right_i_l
                switchSide_Stay_ratio=Reward_NoReward_stay_right_i_r/switchSide_Stay_total
                
                NOswitchSide_switch_contra = Reward_NoReward_switch_right_i_r
                NOswitchSide_switch_ipsi = Reward_NoReward_switch_right_i_l
                NOswitchSide_switch_total = Reward_NoReward_switch_right_i_r+Reward_NoReward_switch_right_i_l
                NOswitchSide_switch_ratio = Reward_NoReward_switch_right_i_r/NOswitchSide_switch_total
                NOswitchSide_Stay_contra = Reward_NoReward_stay_left_i_r
                NOswitchSide_Stay_ipsi = Reward_NoReward_stay_left_i_l
                NOswitchSide_Stay_total = Reward_NoReward_stay_left_i_r+Reward_NoReward_stay_left_i_l
                NOswitchSide_Stay_ratio = Reward_NoReward_stay_left_i_r/NOswitchSide_Stay_total
                
        
        dfResults = pd.DataFrame({'switchSide_switch_ipsi': switchSide_switch_ipsi,
                                  'switchSide_switch_contra': switchSide_switch_contra,
                                  'switchSide_switch_total':switchSide_switch_total,
                                  'switchSide_switch_ratio':switchSide_switch_ratio,
                                  "switchSide_Stay_ipsi": switchSide_Stay_ipsi,
                                  "switchSide_Stay_contra":switchSide_Stay_contra,
                                  'switchSide_Stay_total':switchSide_Stay_total,
                                  "switchSide_Stay_ratio":switchSide_Stay_ratio,
                                  "NOswitchSide_switch_ipsi": NOswitchSide_switch_ipsi,
                                  "NOswitchSide_switch_contra": NOswitchSide_switch_contra,
                                  "NOswitchSide_switch_total":NOswitchSide_switch_total,
                                  "NOswitchSide_switch_ratio":NOswitchSide_switch_ratio,
                                  "NOswitchSide_Stay_ipsi": NOswitchSide_Stay_ipsi,
                                  "NOswitchSide_Stay_contra": NOswitchSide_Stay_contra,
                                  "NOswitchSide_Stay_total":NOswitchSide_Stay_total,
                                  "NOswitchSide_Stay_ratio":NOswitchSide_Stay_ratio})
        
        
        data_list.append(dfResults)
       
    return (data_list)















