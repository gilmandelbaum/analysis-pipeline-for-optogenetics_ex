# optogenetics_analysis pipeline 

This package is the first (of many!) to support the analysis of a project in the Sabatini Lab at Harvard Medical School in which we try to better understand how the brain allows us to decide what to do next.

This package analyzes optogenetics experiments.

It uses jupyter noteboooks and each stage of the pipeline can be run stand-alone or as part of work flow controlled by a "master notebook" that uses papermill.

The choice of notebook list determines what pipeline will be executed. If specific output data structures already exist based on previous runs the "master notebook" will recognize the data structures that already exist and only run what is needed to complete the new analyses. This saves lots of time and allows to efficiently explore the data.

The design of this behavioral task for mice was inspired by operant conditioning behavioral tasks. In such tasks, animals are required to make their “next” choice based on their “previous” actions and the corresponding outcomes of that action. For more details about the behavioral task see 

This analysis package was written by Gil Mandelbaum and Maria Diaz Bobillo.

## Getting Started

The optogenetics_analysis pipeline was tested using python 3.7.3. 

It is recommended to install in a separate conda environment. 

The papermill.execute function calls upon a specific kernel called optogenetics_env. 

Here are some simple commands you can run in the terminal to get going.

```sh
cd github
git clone https://github.com/gilmandelbaum/analysis-pipeline-for-optogenetics_ex
conda create -n optogenetics_env python=3.7.3
conda activate optogenetics_env
cd analysis-pipeline-for-optogenetics_ex
pip install -r requirements.txt 
python -m ipykernel install --user --name optogenetics_env --display-name "optogenetics_env"
```





# optogenetics_analysis
This package is the first (of many!) to support the analysis of a project in the Sabatini Lab at Harvard Medical School in which we try to better understand how the brain allows us to decide what to do next. 

This package analyzes optogenetics experiments. 

It uses jupyter noteboooks and each stage of the pipeline can be run stand-alone or as part of work flow controlled by a "master notebook" that uses papermill. 

The choice of notebook list determines what analysis is done (see list of notebooks below). If specific output data structures already exist based on previous runs the "master notebook" will recognize the data structures that already exist and only run what is needed to complete the new analyses. This saves lots of time and allows to efficiently explore the data.

The notebooks were tested and run using python 3.7.3. (details about env soon to come!)

The design of this behavioral task for mice was inspired by operant conditioning behavioral tasks. 
In such tasks, animals are required to make their “next” choice based on their “previous” actions and the corresponding outcomes of that action.



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
