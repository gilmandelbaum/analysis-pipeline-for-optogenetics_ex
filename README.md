# optogenetics_analysis
This analysis package was written to support the analyis of optogenetic experiments done in the Sabatini Lab at harvard medical school. 

It uses jupyter noteboooks (More details soon to come). 

The notebooks were tested and run using python 3.7.3. 

The design of this behavioral task for mice was inspired by operant conditioning behavioral tasks. 
In such tasks, animals are required to make their “next” choice based on their “previous” actions and the corresponding outcomes of that action.

Here, mice were head-restrained and indicated one of two choices by licking to one of two lick-ports (‘‘lick left/lick right’’) after hearing a “go” cue. In this task, the computer selected one port as the “correct” (i.e. rewarded) port and maintained this designation before switching at random to the other port after 4 to 8 trials were rewarded. The first lick after the go cue was used to select a port and water was only delivered on the offset of this lick, motivating the animal to lick again to test if a reward was delivered (and subsequently continue licking to collect reward, if present). The optimal strategy in this task is to implement win-->repeat and lose-->switch behaviors and to avoid executing win-->switch and lose-->repeat behaviors on two consecutive trials. 

This task was designed by Gil Mandelbaum and Zengcai Guo in the Sabatini Lab at Harvard Medical School and Svobda Lab at Janelia Farms Research Campus.

This analysis package was written by Gil Mandelbaum and Maria Diaz Bobillo.


# for each session the stages of analysis are:

pre analysis Nb_0x

define trials of interest Nb_1x

Import lick data Nb_2x

assign licks to behavioral states Nb_4x

form one structure with all the licks of interest Nb_5x

extract specific licks or data about specific licks per session Nb_6x

data analysis notebook(s) that runs on all the sessions. 

all the notebooks are run together using a optogenetics_Papermill.ipynb notebook. 

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

output: A list of lists with the structure: [R/L][IPSI/CONTRA][trial type]{period}. Each entry to the list is a df in which each lick in that condition is a row. A second output which is a list_of_tags in a csv file. 
 
5_a: splits as described above. 

# Notebook 6:
input: notebook 5 output 

output: extract a specific feature from the data on a session and save it in csv (if possible) and pickle format in a specific folder. The actual notebook output for notebook_6  can be empty. This is requiered in order for the papermill notebook not to re-run notebook that were already run. 

6_a: Each column is a trial and each entry is a lick time. Its runs on all the tags that have been generated. The data is stored in csv files in a folder called timeOfLicks. also pickled format of the list of lists called timeOfLicks.pickle. 

6_b: counts the number of licks in each trial type and each period. 

6_c: counts the number of licks (with direction) in each trial type and each period. 


# Data Set Analysis notebooks: 

how_many_stim_success_rate: gives back a csv file with the number of trials stim that worked, did not work etc. 

how_many_Stim_vs_3rdTrial: how may stim trials compared to how many 3rd win trial that could have stim but were not.This notebook imports the data_trial_label and does the analysis based on that. 

how_many_TO_NON_stim_trials: data_set_how_many_TO_NON_stim_trials.ipynb

how_many_TO_stim_trials: how many of the stim trials were time outs

lick_direction: gives back a csv with how much licks in each direction in various conditions. 

time_consumption_licks: timing of licks during stimulation

time_respose: response times in each condition. 

optogenetics_Papermill_data_set: to run all the notebooks above from one notebook. 

