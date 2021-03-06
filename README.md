# Optogenetics_analysis pipeline 

This package is the first (of many!) to support the analysis of a project in the Sabatini Lab at Harvard Medical School in which we try to better understand how the brain allows us to decide what to do next.

It uses jupyter noteboooks and each stage of the pipeline can be run stand-alone or as part of work flow controlled by one "master jupyter notebook" that uses the [papermill](https://papermill.readthedocs.io/en/latest/) library to control all the notebooks in the pipeline. 

This package is written to analyze optogenetics experiments but can also be used to analyze the mice behavior without optogenetic perturbations. The goal was to write a pipeline that allows for others in the lab to write there own notebooks and add them to the pipeline.  

The choice of notebook will determine what pipeline/analysis will be executed. If specific output data structures already exist based on previous runs of the pipeline the "master jupyter notebook" will recognize those data structures and only run what is needed to complete the new analyses. This saves lots of time and allows to efficiently explore the data.


The design of this behavioral task for mice was inspired by operant conditioning behavioral tasks. 
For more details see
[task description](https://github.com/gilmandelbaum/analysis-pipeline-for-optogenetics_ex/blob/master/task_description.md). 

## Getting started

The optogenetics_analysis pipeline was tested using python 3.7.3. 

It is recommended to install it in a separate conda environment. 

The papermill.execute function in the [optogenetics_Papermill.ipynb notebook](https://github.com/gilmandelbaum/analysis-pipeline-for-optogenetics_ex/tree/master/papermill_and_helper_functions) calls upon a specific kernel called optogenetics_env. 

Here are some simple commands you can run in the terminal to get going. 

```sh
cd github
git clone https://github.com/gilmandelbaum/analysis-pipeline-for-optogenetics_ex
conda create -n optogenetics_env python=3.7.3
conda activate optogenetics_env
cd analysis-pipeline-for-optogenetics_ex
pip install -r requirements.txt 
python -m ipykernel install --user --name optogenetics_env --display-name "optogenetics_env"
jupyter notebook
```

## For each session the stages of analysis are:

Nb stands for notebooks. The number refers to when the notebook will be exected in the pipeline. The x after each number stands for the version of the notebook. For example, one can run a seq of notebooks: 0a1a1d2a4a4b4c5a6a. 

[Nb_0x_pre_analysis](https://github.com/gilmandelbaum/analysis-pipeline-for-optogenetics_ex/tree/master/Nb_0x_pre_analysis)

[Nb_1x_define_trials_of_interest](https://github.com/gilmandelbaum/analysis-pipeline-for-optogenetics_ex/tree/master/Nb_1x_define_trials_of_interest)

[Nb_2x_import_lick_data](https://github.com/gilmandelbaum/analysis-pipeline-for-optogenetics_ex/tree/master/Nb_2x_import_lick_data)

[Nb_4x_assign_licks_to_behavioral_states](https://github.com/gilmandelbaum/analysis-pipeline-for-optogenetics_ex/tree/master/Nb_4x_assign_licks_to_behavioral_states)

[Nb_5x_form_one_structure_with_all_data](https://github.com/gilmandelbaum/analysis-pipeline-for-optogenetics_ex/tree/master/Nb_5x_form_one_structure_with_all_data)

[Nb_6x_extract_specific_information](https://github.com/gilmandelbaum/analysis-pipeline-for-optogenetics_ex/tree/master/Nb_6x_extract_specific_information)

[data analysis notebook(s)](https://github.com/gilmandelbaum/analysis-pipeline-for-optogenetics_ex/tree/master/Nb_data_set) run and combine data from all the sessions. 

all the notebooks run together using a [optogenetics_Papermill.ipynb notebook](https://github.com/gilmandelbaum/analysis-pipeline-for-optogenetics_ex/tree/master/papermill_and_helper_functions) or can be run stand alone. 

## Acknowledgments

This analysis package was written by Gil Mandelbaum and Maria Diaz Bobillo in the lab of [Bernardo Sabatini](https://sabatini.hms.harvard.edu/) at Harvard Medical School. 

