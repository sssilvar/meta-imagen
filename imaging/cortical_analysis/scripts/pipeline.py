from __future__ import print_function

import os
import sys
import argparse

import numpy as np
from os.path import join, isfile
import pandas as pd

root = os.path.dirname(os.path.realpath(__file__))


def parse_args():
    subjects_dir_def = '/input'
    out_folder_def = '/output'
    groupfile_def = '/group/groupfile.csv'

    parser = argparse.ArgumentParser(description='Cortical feature extraction')
    parser.add_argument('-sd', metavar='--subjects-dir',
                        help='$SUBJECTS_DIR path.',
                        default=subjects_dir_def)
    parser.add_argument('-gf', metavar='--groupfile',
                        help='Path to CSV containing subjects (groupfile.csv)',
                        default=groupfile_def)
    parser.add_argument('-out', metavar='--output',
                        help='Output folder where features are gonna be saved (RECOMMENDED: Same than ENIGMA\'s)',
                        default=out_folder_def)
    return parser.parse_args()



if __name__ == '__main__':
    # Parse arguments
    args = parse_args()

    # Set parameters
    dataset_folder = args.sd
    out_folder = args.out
    csv_data = args.gf

    # Print some info
    print('========== CORTICAL FEATURE EXTRACTION ==========')
    print('\t- FreeSurfer subjects folder: %s' % dataset_folder)
    print('\t- Groupfile CSV: %s' % csv_data)
    print('\t- Output folder: %s' % out_folder)

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

    for subject in df['subj']:
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

        # List directory
        ls = os.listdir(out_f)
        if ('lh_thick_2e-4_sampled.raw' not in ls) and ('rh_thick_2e-4_sampled.raw' not in ls):
            for hemi, commands in pipeline_cmd.items():
                if hemi is 'lh':
                    print('\n\n[  INFO  ] Processing Left hemisphere:')
                elif hemi is 'rh':
                    print('\n\n[  INFO  ] Processing Right hemisphere:')

                # Execute pipeline
                # TODO: Remove index (:15) from 'commands'. 
                for i, cmd in enumerate(commands[:15]):
                    print('[  CMD  ] %d\n %s \n' % (i + 1, cmd))
                    os.system(cmd)
        else:
            print('[  WARNING  ] Skipping %s' % subject)

        # Clean output, leave only .raw
        os.system('rm $(ls %s/* | grep -v "thick_2e-4_sampled.raw")' % out_f)
        
        # Concatenate hemisphere results
        # Thickness
        try:
            lh_tk = np.fromfile(join(out_f, 'lh_thick_2e-4_sampled.raw'))
        except IOError:
            np.empty_like(thick_data[-1])
        
        try:
            rh_tk = np.fromfile(join(out_f, 'rh_thick_2e-4_sampled.raw'))
        except IOError:
            np.empty_like(thick_data[-1])
        
        thick_data.append(np.append(lh_tk, rh_tk))

        # # log Jacobians (orig)
        # lh_log_jac = np.fromfile(join(out_f, 'lh_LogJac_2e-4.raw'))
        # rh_log_jac = np.fromfile(join(out_f, 'rh_LogJac_2e-4.raw'))
        # log_jac_data.append(np.append(lh_log_jac, rh_log_jac))

        # # log Jacobians (normalized)
        # lh_log_eq_jac = np.fromfile(join(out_f, 'lh_LogJac_eq_2e-4.raw'))
        # rh_log_eq_jac = np.fromfile(join(out_f, 'rh_LogJac_eq_2e-4.raw'))
        # log_jac_eq_data.append(np.append(lh_log_eq_jac, rh_log_eq_jac))

        index.append(subject)

        print('[  INFO  ] Number of vertex: LH - ', np.shape(lh_tk), ' \ RH - ', np.shape(rh_tk))

    # ===== SAVE CORTICAL RESULTS =====
    tk_cols = []
    lj_cols = []
    lj_eq_cols = []

    # Thickness data
    for i in range(len(thick_data[0])):
        # For lh
        if i < len(lh_tk):
            tk_cols.append('lt_' + str(i))
        else:
            tk_cols.append('rt_' + str(i - len(lh_tk)))

    # for i in range(len(log_jac_data[0])):
    #     # For lh
    #     if i < len(lh_log_jac):
    #         lj_cols.append('lL_' + str(i))
    #     else:
    #         lj_cols.append('rL_' + str(i))

    # for i in range(len(log_jac_eq_data[0])):
    #     # For lh
    #     if i < len(lh_log_eq_jac):
    #         lj_eq_cols.append('lLe_' + str(i))
    #     else:
    #         lj_eq_cols.append('rLe_' + str(i))

    # Create DataFrame
    print('\n\n[  INFO  ] Data dimensionality')
    print('\t\t- Thickness: ', np.shape(thick_data), ' | Mean: ', np.mean(thick_data))
    # print('\t\t- Log. Jacobians: ', np.shape(log_jac_data), ' | Mean: ', np.mean(log_jac_data))
    # print('\t\t- Log jacobians Normalized: ', np.shape(log_jac_eq_data), ' | Mean: ', np.max(log_jac_eq_data))

    # TODO: Include LogJacobians
    cortical_df = pd.DataFrame(index=index, columns=tk_cols, data=thick_data)  # Creates a DataFrame from cortical thickness info
    cortical_df.to_csv(join(out_folder, 'groupfile_cortical_thickness.csv'))

    # whole_data = np.hstack((thick_data, log_jac_data, log_jac_eq_data))
    # cortical_df = pd.DataFrame(index=index, columns=column_names, data=whole_data)
    # cortical_df = pd.DataFrame(index=index, columns=column_names[:len(log_jac_eq_data[0])], data=log_jac_eq_data)

    # Load ENIGMA SHAPE data
    sub_tk_csv = join(out_folder, 'groupfile_thick.csv')
    sub_lj_csv = join(out_folder, 'groupfile_LogJacs.csv')

    # Join with ENIGMA Shape data
    if isfile(sub_tk_csv) and isfile(sub_lj_csv):
        df_eshape = pd.read_csv(join(out_folder, 'groupfile_thick.csv'), index_col=0)
        df_eshape = df_eshape.join(pd.read_csv(join(out_folder, 'groupfile_LogJacs.csv'), index_col=0))

        # Join features in a single matrix and save groupfile.csv
        df_all = cortical_df.join(df_eshape)
        df_all.to_csv(join(out_folder, 'groupfile_features.csv'))
    else:
        print('[  ERROR  ] Subcortical data was not found')
