#!/usr/bin/env python
from dipy.workflows.reconst import ReconstMAPMRIFlow
import json
import os.path

with open('config.json') as config_json:
    config = json.load(config_json)

    # Paths to data
    data_file = str(config['dwi'])
    data_bval = str(config['bvals'])
    data_bvec = str(config['bvecs'])
    lap = bool(config['lap'])
    pos = bool(config['pos'])
    lap_weighting = float(config['laplacian_weighting'])
    small_delta = float(config['small_delta'])
    big_delta = float(config['big_delta'])

    path = os.getcwd()
    mmri_flow = ReconstMAPMRIFlow()
    save_metrics = ['rtop', 'msd', 'qiv', 'rtap', 'rtpp', 'ng', 'perng', 'parng']
    mmri_flow.run(data_file=data_file, data_bval=data_bval, data_bvec=data_bvec,
                  small_delta=small_delta, big_delta=big_delta,
                  out_dir=path, laplacian=lap, positivity=pos, save_metrics=save_metrics,
                  lap_weighting=lap_weighting)