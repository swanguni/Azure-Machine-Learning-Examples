# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license.

import argparse
import os
from azureml.core import Run

from sklearn.datasets import load_diabetes
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib

print("In train.py")
print("As a data scientist, this is where I use my training code.")

parser = argparse.ArgumentParser("train")

parser.add_argument("--input_data", type=str, help="input data")
parser.add_argument("--output_train", type=str, help="output_train directory")

args = parser.parse_args()

print("Argument 1: %s" % args.input_data)
print("Argument 2: %s" % args.output_train)

if not (args.output_train is None):
    os.makedirs(args.output_train, exist_ok=True)
    print("%s created" % args.output_train)


run = Run.get_context()

X, y = load_diabetes(return_X_y = True)
columns = ['age', 'gender', 'bmi', 'bp', 's1', 's2', 's3', 's4', 's5', 's6']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
data = {
    "train":{"X": X_train, "y": y_train},        
    "test":{"X": X_test, "y": y_test}
}

print('Running train.py')

# Randomly pic alpha
alphas = np.arange(0.0, 1.0, 0.05)
alpha=alphas[np.random.choice(alphas.shape[0], 1, replace=False)][0]
print(alpha)
run.log('alpha', alpha)
reg = Ridge(alpha = alpha)
reg.fit(data['train']['X'], data['train']['y'])
preds = reg.predict(data['test']['X'])
run.log('mse', mean_squared_error(preds, data['test']['y']))

# Save model as part of the run history
model_name = "sklearn_regression_model.pkl"
# model_name = "."

with open(model_name, "wb") as file:
    joblib.dump(value = reg, filename = model_name)

# upload the model file explicitly into artifacts 
run.upload_file(name = './outputs/'+ model_name, path_or_stream = model_name)
print('Uploaded the model {} to experiment {}'.format(model_name, run.experiment.name))
dirpath = os.getcwd()
print(dirpath)

print('Following files are uploaded ')
print(run.get_file_names())