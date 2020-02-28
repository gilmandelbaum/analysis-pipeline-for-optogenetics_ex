
from pathlib import Path
import pickle


def loadSession (Mouse_Date_FileName,data_dir_output,HowManyBack,seq_str): 

    data_list = list()

    for row in Mouse_Date_FileName.iterrows():
        
        dfPerSession = row[1]
        mouse = dfPerSession["Mouse"]
        date = dfPerSession["Date"]
        
        __mouse = "__"+mouse
        data_day= '20'+str(date)[:2]+'_'+str(date)[2:4]+'_'+str(date)[4:6]
        version = str(seq_str[-1])
        
        root = Path(data_dir_output+"/"+mouse+"/"+data_day+__mouse+'/'+str(HowManyBack)+"_Back")
        d = mouse+"_"+data_day+'Notebook_5_'+version+'_seq'+seq_str+'.pickle'
        print (d)
        
        my_path = root / d 
        # open a file, where you stored the pickled data
        fileToOpen = open(my_path, 'rb')
        #print (fileToOpen)
        # dump information to that file
        LickCount_perTrial_df = pickle.load(fileToOpen)
        
        
        data_list.append(LickCount_perTrial_df)
        
    return (data_list)

