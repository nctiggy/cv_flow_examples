#!/usr/bin/env python3

import yaml
from copy import deepcopy
from cnvrgv2 import Cnvrg

# Auth with cnvrg and get current project
cnvrg = Cnvrg()
proj = cnvrg.projects.get("test")
flow = dict()

# Open existing flow file
#with open('/root/test/flow.yaml', 'r') as file:
#    cnvrg_yaml = yaml.safe_load(file)

# Initialize the new flow
flow['flow'] = 'auto_build'
flow['recurring'] = ""
flow['tasks'] = []
flow['relations'] = []

dataset_template = {
    "title": "census_data_source",
    "top": 100,
    "left": 100,
    "type": "data",
    "dataset": "test"
}

task_template = {
    "title": "custom_task",
    "type": "exec",
    "input": "python ./src/models/census_data.py",
    "params": [
        {
            "key": "data_path",
            "type": "categorical",
            "values": [
                "/data/test/adult.data"
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
    "computes": ["carvana_AWS.medium"],
    "image": "intel-optimized-tensorflow:2.3.0-ubuntu-20.04-jupyter",
    "top": "100",
    "left": "300"
}

relation_template = {
    "from": "census_data_source",
    "to": "custom_task"
}


flow['tasks'].append(deepcopy(dataset_template))
flow['tasks'].append(deepcopy(task_template))
flow['relations'].append(deepcopy(relation_template))

print(flow)

# Write the updated yaml to the filesystem
with open('/root/test/data.yml', 'w') as outfile:
    yaml.dump(flow, outfile, default_flow_style=False)

# Push the new flow to cnvrg
flow = proj.flows.create(yaml_path='/root/test/data.yml')

# Run the flow we just created!
flow.run()
