
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
        print (mouse+"/"+data_day)
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
        print (mouse+"/"+data_day)
        d = folder_name+"_"+seq_str+"/"+file_name+'.csv'
        
        data = pd.read_csv(root+d)
        data_list.append(data)
        
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
data_set_response_times
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
        print (sessionInfo)
        mouse = sessionInfo["Mouse"] 
        date = sessionInfo["Date"]
        cellType = sessionInfo["D"]
        sideOfStim = sessionInfo["SideOfStim"]        
        
        rt_stay_right = rt_stay_right[i]
        rt_switch_right = rt_switch_right[i]
        rt_stay_left = rt_stay_left[i]
        rt_switch_left = rt_switch_left[i]
    
        if cellType==1:
            
            if sideOfStim =="R":
                switchSide_switch = rt_switch_left.median()
                switchSide_Stay = rt_stay_right.median()
                
                NOswitchSide_switch = rt_switch_right.median()
                NOswitchSide_Stay = rt_stay_left.median()
                
            elif sideOfStim =="L":
                
                switchSide_switch = rt_switch_right.median()
                switchSide_Stay = rt_stay_left.median()
                
                NOswitchSide_switch = rt_switch_left.median()
                NOswitchSide_Stay = rt_stay_right.median()
                
        if cellType==2:
            
            if sideOfStim =="R":
                
                switchSide_switch = rt_switch_right.median()
                switchSide_Stay = rt_stay_left.median()
                
                NOswitchSide_switch = rt_switch_left.median()
                NOswitchSide_Stay = rt_stay_right.median()
                
            elif sideOfStim =="L":
            
                switchSide_switch = rt_switch_left.median()
                switchSide_Stay = rt_stay_right.median()
                
                NOswitchSide_switch = rt_switch_right.median()
                NOswitchSide_Stay = rt_stay_left.median()   
                
                
        dfResults.loc[i] = pd.Series({'mouse': mouse,"date": date,"D": cellType,
                                      "SideOfStim": sideOfStim,
                                      'switchSide_switch': switchSide_switch,
                                      "switchSide_Stay": switchSide_Stay, 
                                      "NOswitchSide_switch": NOswitchSide_switch, 
                                      "NOswitchSide_Stay": NOswitchSide_Stay})
        
    return (dfResults)
    