# optogenetics_analysis


# Notebook 0:
define each trial

input: mouse_dataTrial_label.xlsx (each row is a trial). 

output: mouse_dateNotebook_0_a.pickle. The output is the same df as mouse_dataTrial_label with additional columns that will aid in the analysis. 

0_a: standard analysis 



# Notebook 1:
Each notebook 1 gives a different list of trial numbers with the same general structure of output: 
The number of trial: R/L, IPSI/CONTRA, TrialType. 

input: the output of notebook 0_a 

output: a list of lists called mouse_dateNotebook_1_label.pickle 
you can run "a" or "b" or "c" with "d" or with "e".

1_a: get all trials (with ENLp and with CUEp)

1_b: get no ENLp, no CUEp trials. 

1_c: get ENLp. 

1_d: is optogenetics stimulation trials. 
also takes TypeOfStim and Trials_filter that are set in the paper mill notebook. 
Trials_filter can be either 'allTrials' or 'noENLp' or 'onlyENLp'
TypeOfStim can be either 'ENLonly' or 'FullStim' or 'Consumption'
you can run 1_a or 1_b or 1_c together with 1_d.

1_e: is not optogenetics trials. 
see note for 1_d. 
you can run 1_a or 1_b or 1_c together with 1_e.

# Notebook 2:
To prepare the dataLick for analysis. 

input: dataLick. 

output: The output is the same df as dataLick_label with additional columns that will aid in the analysis. 

2_a: standard analysis 


# Notebook 3:
empty



# Notebook 4:
Flagging periods of interest in order to generate licks of specific interest. 
The goal is to assign licks to a specific trial and give each lick a tag. 

input: Notebook 2 

output: .pickle that has a data frame with two columns. The first column is the bin number and the second column is the trial number. 

4_a: Reward_NoReward_tag: consumption or no rewarded period. 

4_b: ENL_tag: enforced non lick period task. 

4_c: Sel_tag: response time.


# Notebook 5:

input: notebook 1 (list of trial types of interest), notebook 2 (data of all the licks). 
It also uses the flags that were generated in notebook 4s. 
Notebook 5 also needs [Tags] which are all set in the papermill notebook. 

output: A list of lists with the structure: [R/L][IPSI/CONTRA][trial type][period]. Each entry to the list is a df in which each lick in that condition is a row. A second output which is a list_of_tags in a csv file. 
 
5_a: splits as described above. 

# Notebook 6:
input: notebook 5 output 

output: extract a specific feature from the data on a session and save it in csv (if possible) and pickle format in a specific folder. The actual notebook output for notebook_6  can be empty. This is requiered in order for the papermill notebook not to re-run notebook that were already run. 

6_a: Each column is a trial and each entry is a lick time. Its runs on all the tags that have been generated. The data is stored in csv files in a folder called timeOfLicks. also pickled format of the list of lists called timeOfLicks.pickle. 

6_b: counts the number of licks in each trial type and each period. 

6_c: counts the number of licks (with direction) in each trial type and each period. 

6_d: some over lap with 6_a. Makes 

# Data Set Analysis notebooks: 

how_many_stim_success_rate: gives back a csv file with the number of trials stim that worked, did not work etc. 

how_many_Stim_vs_3rdTrial: how may stim trials compared to how many 3rd win trial that could have stim but were not. 

how_many_TO_NON_stim_trials: data_set_how_many_TO_NON_stim_trials.ipynb

how_many_TO_stim_trials: how many of the stim trials were time outs

lick_direction: gives back a csv with how much licks in each direction in various conditions. 

time_consumption_licks: timing of licks during stimulation

time_respose: response times in each condition. 

optogenetics_Papermill_data_set: to run all the notebooks above from one notebook. 

