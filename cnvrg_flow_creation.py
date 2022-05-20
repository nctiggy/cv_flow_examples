#!/usr/bin/env python3

import yaml
import json
from copy import deepcopy
from cnvrgv2 import Cnvrg

# Auth with cnvrg and get current project
cnvrg = Cnvrg()
proj = cnvrg.projects.get("test")
flow = dict()

flow_name = "carvana_test"

data_path = "/data/test"

default_compute = ["carvana_AWS.medium"]

default_container_image = ("intel-optimized-tensorflow"
                           ":2.3.0-ubuntu-20.04-jupyter")

# Add tasks here
task_order = [
    {
        "type": "data",
        "dataset": "test",
        "title": "data_source"
    },
    {
        "type": "exec",
        "title": "data_prep",
        "input": "python ./src/models/census_data.py",
        "params": [
            {
                "key": "data_path",
                "type": "categorical",
                "value": f"{data_path}/adult.data"
            }
        ]
    },
    {
        "type": "exec",
        "title": "data_integrity",
        "input": ("export PYTHONPATH=$PYTHONPATH:/cnvrg; python "
                  "./src/models/check_census_data.py"),
        "params": [
            {
                "key": "data_path",
                "type": "categorical",
                "value": "/input/data_prep/output/output.pkl"
            },
        ]
    },
    {
        "type": "exec",
        "title": "train",
        "input": "python ./src/models/merged_tf.py",
        "params": [
            {
                "key": "data_path",
                "type": "categorical",
                "value": "/input/data_prep/output/output.pkl"
            },
            {
                "key": "epochs",
                "type": "discrete",
                "value": "4"
            }
        ]
     },
    {
        "type": "deploy",
        "title": "deploy_model",
        "endpoint_title": "deploymodel"
    }
]


# Initialize the new flow
flow['flow'] = flow_name
flow['recurring'] = ""
flow['tasks'] = []
flow['relations'] = []

data_template = {
    "title": "",
    "type": "",
    "dataset": ""
}

exec_template = {
    "title": "",
    "type": "",
    "input": "",
    "params": [
        {
            "key": "",
            "type": "",
            "values": [
                ""
            ]
        },
        {
            "key": "epochs",
            "type": "discrete",
            "values": [
                "4"
            ]
        }
    ],
    "output_dir": "output",
    "algorithm": "",
    "computes": default_compute,
    "image": default_container_image
}

deploy_template = {
    "endpoint_title": "",
    "type": "",
    "conditions": [],
    "title": ""
}

relation_template = {
    "from": "",
    "to": ""
}

# Create the tasks
for index, task in enumerate(task_order):
    template = f"{task['type']}_template"
    temp_task = deepcopy(eval(template))
    for k, v in task.items():
        temp_task[k] = v
    flow["tasks"].append(temp_task)
    if not index == 0:
        relationship = deepcopy(relation_template)
        relationship["from"] = task_order[index-1]["title"]
        relationship["to"] = task["title"]
        flow["relations"].append(relationship)

print(json.dumps(flow))

# Write the updated yaml to the filesystem
with open('data.yml', 'w') as outfile:
    yaml.dump(flow, outfile, default_flow_style=False)

# Push the new flow to cnvrg
flow = proj.flows.create(yaml_path='data.yml')

flow.run()
