from azureml.pipeline.core import Pipeline, PipelineData, StepSequence
from azureml.pipeline.steps import PythonScriptStep
from azureml.pipeline.steps import DataTransferStep
from azureml.pipeline.core import PublishedPipeline
from azureml.pipeline.core.graph import PipelineParameter

from azureml.core import Workspace, Run, Experiment, Datastore
from azureml.core.compute import AmlCompute

aml_compute_target = "cpu"

workspace_name ="aidemosdevaml"
resource_group="aidemosdev"
subscription_id = "bc69d98c-7d2b-4542-88a4-f86eb4aea4a5"
project_folder = "."

ws = Workspace.get(name = workspace_name,
                             subscription_id = subscription_id,
                             resource_group = resource_group)



# Runconfig
from azureml.core.runconfig import CondaDependencies, RunConfiguration
cd = CondaDependencies.create(pip_packages=["sklearn", "azureml-defaults"])
amlcompute_run_config = RunConfiguration(conda_dependencies=cd)

# Make sure the compute target exists
try:
    aml_compute = AmlCompute(ws, aml_compute_target)
    print("found existing compute target.")
except:
    print("compute target not found. exiting")

# each step has its dependencies declared as a runconfig (if it needs extra packages)
step1 = PythonScriptStep(name="train_step",
                         script_name="train.py", 
                         compute_target=aml_compute, 
                         source_directory=project_folder,
                         runconfig = amlcompute_run_config,
                         allow_reuse=False)

step2 = PythonScriptStep(name="compare_step",
                         script_name="compare.py", 
                         compute_target=aml_compute, 
                         source_directory=project_folder)

step3 = PythonScriptStep(name="extract_step",
                         script_name="extract.py", 
                         compute_target=aml_compute, 
                         source_directory=project_folder)

step4 = PythonScriptStep(name="register_step",
                         script_name="register.py", 
                         compute_target=aml_compute, 
                         source_directory=project_folder)

# list of steps to run
steps = [step1,step2,step3,step4]
print("Step lists created")

pipeline1 = Pipeline(workspace=ws, steps=steps)
print ("Pipeline is built")

pipeline1.validate()
print("Pipeline validation complete")

pipeline_run1 = Experiment(ws, 'devopsdemo').submit(pipeline1, regenerate_outputs=True)
print("Pipeline is submitted for execution")