#A DevOps Process for Machine Learning

## Requirements
To set up a controlled, safe E2E workflow for machine learning models, we will leverage 2 tools:
1.	Azure DevOps
2.	Azure Machine Learning

# Configure project
Create an Azure DevOps project to manage your source code, application builds and release pipelines.
In this project, put some scaffold code to represent the tasks you want to perform.
## Example Files
-	data.txt
-	extract.py
-	train.py
-	eval.py
-	conda.yml
-	score.py
-	pipeline.py (runs extract.py then train.py)

#Configure cloud compute resources
Leverage IaC to define environments, including networks, servers, and other compute resources, as a text file (script or definition) that is checked into version control and used as the base source for creating or updating those environments. 
For instance, adding a new server should be done by editing a text file and running the release pipeline, not by doing a remote connection into the environment and spinning up one manually.
Supporting to this lab we will make use of the Azure CLI and the Azure Machine Learning CLI extension to setup our resources.

## Resources to define:
-	ARM templates for AKS clusters (INT, PROD)
-	ARM template for AML workspace
## Resources to define (CLI script)
```
az group create -l westeurope -n dev
```
```
az ml workspace create -n amldev -g dev
```
```
az ml computetarget setup amlcompute -n cpu --autoscale-enabled --autoscale-max-nodes 4 --autoscale-min-nodes 1 -s STANDARD_D3_V2 -w amldev -g dev
```

#Set up training pipeline
Ensure your pipeline executes locally or in a hosted notebook environment (powered by Azure Notebooks). 

Once you have validated your pipeline works as expected, you can set up pipeline execution in Azure DevOps pipelines whenever a code change occurs.

## What happens on a code change
When a code change happens, the “pipeline.py” code will be executed via an authenticated Azure CLI. 

TODO (CLI) - you can submit a serialized pipeline.yml for execution as well as submit a request to a Published Pipeline.

This will take your code artifacts, validate they function as expected, and submit the pipeline for execution.

## Configure unit tests on code
Prior to automating your training flow, you should define unit tests to be run to ensure you aren’t wasting valuable time and compute in the training process.
Configure criteria for model evaluation once the training pipeline finishes.

# Determine when to register a model
Define an evaluation script which will check key metrics on the model in your pipeline-produced experiment. 
If the metrics check passes, go ahead and register the model.

#Define a release for when a new model is registered
Whenever a model or its score file changes, you want to determine if this registered model needs to be deployed, and where it needs to be deployed to. This is defined in Azure DevOps Pipelines as well.
Leveraging the Azure ML CLI, you can issue a series of commands to:
1.	package your model into a deployable service
2.	validate and profile your model to determine optimal compute & memory allocation
3.	deploy your model to production running on the Azure Kubernetes Service
Define phases, 1 INT, 1 PROD
Define a human approver as being required to move from INT to PROD


