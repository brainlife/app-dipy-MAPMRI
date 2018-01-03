from dipy.workflows.reconst import ReconstMAPMRILaplacian, ReconstMAPMRIBoth, ReconstMAPMRIPositivity
import json
import os.path


def main():
    with open('config.json') as config_json:
        config = json.load(config_json)

        # Paths to data
        data_file = str(config['dwi'])
        data_bval = str(config['bvals'])
        data_bvec = str(config['bvecs'])
        model_type = str(config['model_type'])

    if model_type is 'both':
        mmri_flow = ReconstMAPMRIBoth
    elif model_type is 'laplacian':
        mmri_flow = ReconstMAPMRILaplacian
    elif model_type is 'positivity':
        mmri_flow = ReconstMAPMRIPositivity

    path = os.getcwd()
    path = os.path.join(path, 'output')

    mmri_flow.run(data_file=data_file, data_bval=data_bval, data_bvec=data_bvec, out_dir=path)

main()