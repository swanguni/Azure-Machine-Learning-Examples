from azureml.core import Workspace
from azureml.core.model import Model
from azureml.core import Run

#workspace_name ="aidemosdevaml"
#resource_group="aidemosdev"
#subscription_id = "bc69d98c-7d2b-4542-88a4-f86eb4aea4a5"

# Get workspace
#ws = Workspace.get(name = workspace_name,
#                             subscription_id = subscription_id,
#                             resource_group = resource_group)

# Download Model to Project root directory
#model_name= 'blah.pkl'

run = Run.get_context()
model = run.register_model(model_name = "pi_estimate", model_path = "outputs/pi_estimate.txt")

#model = Model.register(model_path = model_name, # this points to a local file
#                       model_name = model_name, # this is the name the model is registered as
#                       tags = {'area': "diabetes", 'type': "regression", 'run_id' : run_id},
#                       description="Regression model for diabetes dataset",
#                       workspace = ws)

print('Model registered: {} \nModel Description: {} \nModel Version: {}'.format(model.name, model.description, model.version))