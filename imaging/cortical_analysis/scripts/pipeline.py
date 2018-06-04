import os, sys

import numpy as np
from os.path import join
import pandas as pd

root = os.path.dirname(__file__)


if __name__ == '__main__':
    # Set parameters
    dataset_folder = '/input'
    out_folder = '/output'
    csv_data = '/group/groupfile.csv'

    bin_dir = join(root, 'bin')

    # Cast variables
    dsf = os.path.normpath(dataset_folder)

    # Add environment variable
    os.environ['SUBJECTS_DIR'] = dsf
    print('[  INFO  ] New SUBJECTS_DIR: ', os.environ['SUBJECTS_DIR'], '\n\n')

    # Load dataset: df
    df = pd.read_csv(csv_data)

    # Parameters for features output
    thick_data = []
    index = []

    for subject in df['subj'][:4]:
        sdir = os.path.join(dataset_folder, subject)
        out_f = os.path.join(out_folder, subject)
        print('\n[  INFO  ] Processing subject: ', subject)

        # Create a folder
        try:
            os.mkdir(out_f)
        except FileExistsError:
            print('[  WARNING  ] Looks like folder %s already exists.' % out_f)

        # Define the pipeline (list of commands): pipeline_cmd
        pipeline_cmd = {}
    
        hemispheres = ['lh', 'rh']
        surface_file_ext = ['', '.vtk', '.obj', '.m', '.m', '.m']
        files_orig = ['.white', '.sphere.reg']

        files_target = []
        for f in files_orig:
            for ext in surface_file_ext:
                files_target.append(f + ext)

        for h in hemispheres:
            pipeline_cmd[h] = [
                'mris_convert ' + join(sdir, 'surf', h + files_target[0]) + ' ' + join(out_f, h + files_target[1]),
                'java -jar ' + join(bin_dir, 'ShapeTranslator.jar') + ' -input ' + join(out_f, h + files_target[1]) + ' -output ' + join(out_f, h + files_target[2]) + ' -obj',
                join(bin_dir, 'ccbbm') + ' -obj2mesh ' + join(out_f, h + files_target[2]) + ' ' + join(out_f, h + files_target[3]),
                join(bin_dir, 'ccbbm') + ' -enforce_manifold_topology ' + join(out_f, h + files_target[3]) + ' ' + join(out_f, h + files_target[4]),
                join(bin_dir, 'ccbbm') + ' -close_boundaries ' + join(out_f, h + files_target[3]) + ' ' + join(out_f, h + files_target[4]),

                'mris_convert ' + join(sdir, 'surf', h + files_target[6]) + ' ' + join(out_f, h + files_target[7]),
                'java -jar ' + join(bin_dir, 'ShapeTranslator.jar') + ' -input ' + join(out_f, h + files_target[7]) + ' -output ' + join(out_f, h + files_target[8]) + ' -obj',
                join(bin_dir, 'ccbbm') + ' -obj2mesh ' + join(out_f, h + files_target[8]) + ' ' + join(out_f, h + files_target[9]),
                join(bin_dir, 'ccbbm') + ' -enforce_manifold_topology ' + join(out_f, h + files_target[9]) + ' ' + join(out_f, h + files_target[10]),
                join(bin_dir, 'ccbbm') + ' -close_boundaries ' + join(out_f, h + files_target[10]) + ' ' + join(out_f, h + files_target[11]),

                join(bin_dir, 'ccbbm') + ' -transform ' + join(out_f, h + files_target[11]) + ' ' + join(bin_dir, 'one_hundredth.txt') + ' ' + join(out_f, h + files_target[11]),

                'mris_convert -c ' + join(sdir, 'surf', h + '.thickness') + ' ' + join(sdir, 'surf', h + '.white') + ' ' + join(out_f, h + '_thick.asc'),
                join(bin_dir, 'FSthick2raw') + ' ' + join(out_f, h + '_thick.asc') + ' ' + join(out_f, h + '_thick.raw'),

                # 14 - 15
                join(bin_dir, 'ccbbm') + ' -gausssmooth_attribute3 256 ' + join(out_f, h + '.sphere.reg.m') + ' ' + join(out_f, h + '_thick.raw') + ' 2e-4 ' + join(out_f, h + '_thick_2e-4.raw'),
                join(bin_dir, 'ccbbm') + ' -fastsampling ' + join(out_f, h + '.sphere.reg.m') + \
                ' ' + join(bin_dir, 'FreeSurfer_IC7.m') + ' ' + join(out_f, h + '.white.sampled.m') + ' -tmp_atts ' + \
                join(out_f, h + '_thick_2e-4.raw') + ' -tar_atts ' + join(out_f, h + '_thick_2e-4_sampled.raw')

            ]

        for hemi, commands in pipeline_cmd.items():
            if hemi is 'lh':
                print('\n[  INFO  ] Processing Left hemisphere:')
            elif hemi is 'rh':
                print('\n[  INFO  ] Processing Right hemisphere:')

            # Execute pipeline
            for cmd in commands:
                print(cmd)
                os.system(cmd)

        # Concatenate hemisphere results
        lh_tk = np.fromfile(join(out_f, 'lh' + '_thick_2e-4.raw'))
        rh_tk = np.fromfile(join(out_f, 'rh' + '_thick_2e-4.raw'))
        thick_data.append(np.append(lh_tk, rh_tk))
        index.append(subject)

        print('[  INFO  ] Number of vertex: LH - ', np.shape(lh_tk), ' \ RH - ', np.shape(rh_tk))

    # Column names
    cols = []
    for i in range(len(thick_data[0])):
        # For lh
        if i <= len(lh_tk):
            cols.append('lh_thick_2e-4_' + str(i))
        else:
            cols.append('rh_thick_2e-4_' + str(i - len(lh_tk)))

    print('[  INFO  ] Number of vertex extracted: ', len(cols), 'Concatenated', len(lh_tk))
    # Create DataFrame
    thick_df = pd.DataFrame(index=index, columns=cols, data=thick_data)

    print(thick_df.head())
