# optogenetics_analysis
This package is the first (of many!) to support the analysis of a project in the Sabatini Lab at Harvard Medical School in which we try to better understand how the brain allows us to decide what to do next. 

This package analyzes optogenetics experiments. 

It uses jupyter noteboooks and each stage of the pipeline can be run stand-alone or as part of work flow controlled by a "master notebook" that uses papermill. 

The choice of notebook list determines what analysis is done (see list of notebooks below). If specific output data structures already exist based on previous runs the "master notebook" will recognize the data structures that already exist and only run what is needed to complete the new analyses. This saves lots of time and allows to efficiently explore the data.

The notebooks were tested and run using python 3.7.3. (details about env soon to come!)

The design of this behavioral task for mice was inspired by operant conditioning behavioral tasks. 
In such tasks, animals are required to make their “next” choice based on their “previous” actions and the corresponding outcomes of that action.

Here, mice were head-restrained and indicated one of two choices by licking to one of two lick-ports (‘‘lick left/lick right’’) after hearing a “go” cue. In this task, the computer selected one port as the “correct” (i.e. rewarded) port and maintained this designation before switching at random to the other port after 4 to 8 trials were rewarded. The first lick after the go cue was used to select a port and water was only delivered on the offset of this lick, motivating the animal to lick again to test if a reward was delivered (and subsequently continue licking to collect reward, if present). The optimal strategy in this task is to implement win-->repeat and lose-->switch behaviors and to avoid executing win-->switch and lose-->repeat behaviors on two consecutive trials. 

This task was designed by Gil Mandelbaum and Zengcai Guo in the Sabatini Lab at Harvard Medical School and Svobda Lab at Janelia Farms Research Campus.

This analysis package was written by Gil Mandelbaum and Maria Diaz Bobillo.


# for each session the stages of analysis are:

Nb_0x_pre_analysis

Nb_1x_define_trials_of_interest

Nb_2x_import_lick_data

Nb_4x_assign_licks_to_behavioral_states

Nb_5x_form_one_structure_with_all_data

Nb_6x_extract_specific_information

data analysis notebook(s) run and combine data from all the sessions. 

all the notebooks are run together using a optogenetics_Papermill.ipynb notebook. 
