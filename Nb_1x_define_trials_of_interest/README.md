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
