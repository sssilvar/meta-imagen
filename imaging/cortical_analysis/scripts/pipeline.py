from __future__ import print_function

import os, sys

import numpy as np
from os.path import join
import pandas as pd

root = os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__':
    # Set parameters
    center_main_folder = ''
    dataset_folder = center_main_folder + '/input'
    out_folder = center_main_folder + '/output'
    csv_data = center_main_folder + '/group/groupfile.csv'

    # Set bin folder and add execution permission
    bin_dir = join(root, 'bin')
    os.system('chmod -R +x ' + bin_dir)
    
    # Software variables
    ccbbm = join(bin_dir, 'ccbbm')
    raw_operations = join(bin_dir, 'raw_operations')
    shape_translator = join(bin_dir, 'ShapeTranslator.jar')

    # Cast variables
    dsf = os.path.normpath(dataset_folder)

    # Add environment variable
    os.environ['SUBJECTS_DIR'] = dsf
    print('[  INFO  ] New SUBJECTS_DIR: ', os.environ['SUBJECTS_DIR'], '\n\n')

    # Load dataset: df
    df = pd.read_csv(csv_data)

    # Parameters for features output
    thick_data = []
    log_jac_data = []
    log_jac_eq_data = []
    index = []

    for subject in df['subj'][:2]:
        sdir = os.path.join(dataset_folder, subject)
        out_f = os.path.join(out_folder, subject)
        print('\n[  INFO  ] Processing subject: ', subject)

        # Create a folder
        try:
            os.mkdir(out_f)
        except Exception as e:
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
            if h is 'rh':
                ic_file = join(bin_dir, 'FreeSurfer_IC7_RH_sym.m')
            else:
                ic_file = join(bin_dir, 'FreeSurfer_IC7.m')

            # Create list of commands (pipeline)
            pipeline_cmd[h] = [
                'mris_convert ' + join(sdir, 'surf', h + files_target[0]) + ' ' + join(out_f, h + files_target[1]),
                'java -jar ' + shape_translator + ' -input ' + join(out_f, h + files_target[1]) + ' -output ' + join(out_f, h + files_target[2]) + ' -obj',
                ccbbm + ' -obj2mesh ' + join(out_f, h + files_target[2]) + ' ' + join(out_f, h + files_target[3]),
                ccbbm + ' -enforce_manifold_topology ' + join(out_f, h + files_target[3]) + ' ' + join(out_f, h + files_target[4]),
                ccbbm + ' -close_boundaries ' + join(out_f, h + files_target[3]) + ' ' + join(out_f, h + files_target[4]),

                'mris_convert ' + join(sdir, 'surf', h + files_target[6]) + ' ' + join(out_f, h + files_target[7]),
                'java -jar ' + shape_translator + ' -input ' + join(out_f, h + files_target[7]) + ' -output ' + join(out_f, h + files_target[8]) + ' -obj',
                ccbbm + ' -obj2mesh ' + join(out_f, h + files_target[8]) + ' ' + join(out_f, h + files_target[9]),
                ccbbm + ' -enforce_manifold_topology ' + join(out_f, h + files_target[9]) + ' ' + join(out_f, h + files_target[10]),
                ccbbm + ' -close_boundaries ' + join(out_f, h + files_target[10]) + ' ' + join(out_f, h + files_target[11]),

                ccbbm + ' -transform ' + join(out_f, h + files_target[11]) + ' ' + join(bin_dir, 'one_hundredth.txt') + ' ' + join(out_f, h + files_target[11]),

                # 12
                'mris_convert -c ' + \
                join(sdir, 'surf', h + '.thickness') + ' ' + \
                join(sdir, 'surf', h + '.white') + ' ' + \
                join(out_f, h + '_thick.asc'),

                # 13
                join(bin_dir, 'FSthick2raw') + ' ' + \
                join(out_f, h + '_thick.asc') + ' ' + \
                join(out_f, h + '_thick.raw'),

                # 14
                ccbbm + ' -gausssmooth_attribute3 256 ' + \
                join(out_f, h + '.sphere.reg.m') + ' ' + \
                join(out_f, h + '_thick.raw') + ' 2e-4 ' + \
                join(out_f, h + '_thick_2e-4.raw'),

                # 15
                ccbbm + ' -fastsampling ' + \
                join(out_f, h + '.sphere.reg.m') + ' ' + \
                ic_file + ' ' + \
                join(out_f, h + '.white.m') + ' ' + \
                join(out_f, h + '.white.sampled.m') + \
                ' -tmp_atts ' + join(out_f, h + '_thick_2e-4.raw') + \
                ' -tar_atts ' + join(out_f, h + '_thick_2e-4_sampled.raw'),

                # 16 - LogJacobians
                ccbbm + ' -store_att_area ' + \
                join(out_f, h + '.white.sampled.m') + ' ' + \
                join(out_f, h + '.white.area.raw'),

                # 17
                raw_operations + ' -divide -float ' + \
                join(out_f, h + '.white.area.raw') + ' ' + \
                join(bin_dir,  h.upper() + '_mean_area.raw') + ' ' + \
                join(out_f, h + '.jac.raw'),

                # 18
                raw_operations + ' -log -float ' + join(out_f, h + '.jac.raw') + ' ' + join(out_f, h + '_LogJac.raw'),

                # 19
                ccbbm + ' -laplacian_smooth_attribute ' + \
                join(out_f, h + '.white.sampled.m') + ' ' + \
                join(out_f, h + '_LogJac.raw') + ' ' + \
                join(out_f, h + '_LogJac.raw') + ' 20',

                # 20
                ccbbm + ' -gausssmooth_attribute3 256 ' + \
                ic_file + ' ' + \
                join(out_f, h + '_LogJac.raw') + ' 2e-4 ' + \
                join(out_f, h + '_LogJac_2e-4.raw'),

                # 21
                ccbbm + ' -equalizearea ' + \
                join(bin_dir,  h.upper() + '_200_mean.m') + ' ' + \
                join(out_f, h + '.white.sampled.m') + ' ' + \
                join(out_f, h + '.white.normed_area.m'),

                # 22
                ccbbm + ' -store_att_area ' + \
                join(out_f, h + '.white.normed_area.m') + ' ' + \
                join(out_f, h + '.white.normed_area.area.raw'),

                # 23
                raw_operations + ' -divide -float ' + \
                join(out_f, h + '.white.normed_area.area.raw') + ' ' + \
                join(bin_dir, h.upper() + '_mean_area_equalized.raw') + ' ' + \
                join(out_f, h + '.jac_eq.raw'),

                # 24
                raw_operations + ' -log -float ' + \
                join(out_f, h + '.jac_eq.raw') + ' ' + \
                join(out_f, h + '_LogJac_eq.raw'),

                # 25
                ccbbm + ' -laplacian_smooth_attribute ' + \
                join(out_f, h + '.white.sampled.m') + ' ' + \
                join(out_f, h + '_LogJac_eq.raw') + ' ' + \
                join(out_f, h + '_LogJac_eq.raw') + ' 20',

                # 26
                ccbbm + ' -gausssmooth_attribute3 256 ' + ic_file + ' ' + \
                join(out_f, h + '_LogJac_eq.raw') + ' 2e-4 ' + \
                join(out_f, h + '_LogJac_eq_2e-4.raw')
            ]

        for hemi, commands in pipeline_cmd.items():
            if hemi is 'lh':
                print('\n\n[  INFO  ] Processing Left hemisphere:')
            elif hemi is 'rh':
                print('\n\n[  INFO  ] Processing Right hemisphere:')

            # Execute pipeline
            for i, cmd in enumerate(commands):
                print('[  CMD  ] %d\n %s \n' % (i + 1, cmd))
                # os.system(cmd)

        # Concatenate hemisphere results
        # Thickness
        lh_tk = np.fromfile(join(out_f, 'lh' + '_thick_2e-4_sampled.raw'))
        rh_tk = np.fromfile(join(out_f, 'rh' + '_thick_2e-4_sampled.raw'))
        thick_data.append(np.append(lh_tk, rh_tk))

        # # log Jacobians (orig)
        lh_log_jac = np.fromfile(join(out_f, 'lh_LogJac_2e-4.raw'))
        rh_log_jac = np.fromfile(join(out_f, 'rh_LogJac_2e-4.raw'))
        log_jac_data.append(np.append(lh_log_jac, rh_log_jac))

        # log Jacobians (normalized)
        lh_log_eq_jac = np.fromfile(join(out_f, 'lh_LogJac_eq_2e-4.raw'))
        rh_log_eq_jac = np.fromfile(join(out_f, 'rh_LogJac_eq_2e-4.raw'))
        log_jac_eq_data.append(np.append(lh_log_eq_jac, rh_log_eq_jac))

        index.append(subject)

        print('[  INFO  ] Number of vertex: LH - ', np.shape(lh_tk), ' \ RH - ', np.shape(rh_tk))

    # ===== SAVE CORTICAL RESULTS =====
    column_names = []

    # Thickness data
    for i in range(len(thick_data[0])):
        # For lh
        if i < len(lh_tk):
            column_names.append('lh_tk_' + str(i))
        else:
            column_names.append('rh_tk_' + str(i - len(lh_tk)))

    for i in range(len(log_jac_data[0])):
        # For lh
        if i < len(lh_log_jac):
            column_names.append('lh_LJ_' + str(i))
        else:
            column_names.append('rh_LJ_' + str(i))

    for i in range(len(log_jac_eq_data[0])):
        # For lh
        if i < len(lh_log_eq_jac):
            column_names.append('lh_LJ_eq_' + str(i))
        else:
            column_names.append('rh_LJ_eq_' + str(i))

    # Create DataFrame
    print('\n\n[  INFO  ] Data dimensionality')
    print('\t\t- Thickness: ', np.shape(thick_data), ' | Mean: ', np.mean(thick_data))
    print('\t\t- Log. Jacobians: ', np.shape(log_jac_data), ' | Mean: ', np.mean(log_jac_data))
    print('\t\t- Log jacobians Normalized: ', np.shape(log_jac_eq_data), ' | Mean: ', np.max(log_jac_eq_data))

    whole_data = np.hstack((thick_data, log_jac_data, log_jac_eq_data))
    cortical_df = pd.DataFrame(index=index, columns=column_names, data=whole_data)
    # cortical_df = pd.DataFrame(index=index, columns=column_names[:len(log_jac_eq_data[0])], data=log_jac_eq_data)

    # Load ENIGMA SHAPE data
    df_eshape = pd.read_csv(join(out_folder, 'groupfile_thick.csv'), index_col=0)
    df_eshape = df_eshape.join(pd.read_csv(join(out_folder, 'groupfile_LogJacs.csv'), index_col=0))

    # Join features in a single matrix
    df_all = cortical_df.join(df_eshape)

    # for col in df_all.columns:
    #     number_of_nan = df_all[col].isnull().sum()

    #     if number_of_nan > 0:
    #         print('[  WARNING  ] Not a Number (NaN) found: ', number_of_nan)

    # Save Data
    # df_all.to_hdf(join(out_folder, 'groupfile_features.h5'), key='features', format='table', mode='w')
    df_all.to_csv(join(out_folder, 'groupfile_features.csv'))
