import os
from os.path import join, dirname

import numpy as np
import pandas as pd


def mkdir(folder):
    try:
        os.mkdir(folder)
    except Exception as e:
        print('[  WARNING  ] Looks like folder %s already exists.' % folder)
        print('[  WARNING  ] Exception: {}'.format(e))


if __name__ == '__main__':
    os.system('clear')
    #   - File containing the main components 
    # resulting from the experiment: comp_file
    #   - File containing feature_data: f_file
    #   - ENIGMA Shape folder: eshape_f
    #   - Output folder: out_f
    home = os.environ['HOME']
    comp_file = join(home, 'Documents/temp/PCA_results/data_simulation/PCA.npy')
    f_file = join(home, 'Documents/temp/PCA_results/data_simulation/center_1/output/groupfile_features.csv')
    e_shape_f = join(home, 'Documents/Docker/meta-imagen/imaging/eshape/enigma_shape/')
    out_f = join(dirname(comp_file), 'surfaces')

    # key folders an programs
    ccbbm = join(e_shape_f, 'MedialDemonsShared/bin/ccbbm')
    atlas_f = join(e_shape_f, 'MedialDemonsShared/atlas')

    # Create output folder if not exist
    mkdir(out_f)

    # Load components file: data
    # Load features_file: feats_df
    data = np.load(comp_file)
    feats = pd.read_csv(f_file, index_col=0, nrows=1).columns.tolist()
    print('[  INFO  ] Total number of features: %d' % len(feats))

    # Get regions: rois
    rois = set([i.split('_')[1] for i in feats])

    # Feature names: f_names
    f_names = ['thick', 'LogJacs']

    # Create DataFrame from components
    df = pd.DataFrame(data=data.T, columns=feats)

    # Do the magic!
    print(df.head())
    for roi in rois:
        for f_name in f_names:
            # Load thickness and LogJacs from the roi
            name = f_name + '_' + roi
            sel = [name in col for col in df.columns]
            roi_data = df.loc[:, sel]
            
            # Create folder per region and feature type: roi_folder
            roi_folder = join(out_f, name)
            mkdir(roi_folder)
            
            # Load per component
            print('[  INFO  ] ROI: %s' % name)
            for i, c in roi_data.iterrows():
                # # Save RAW
                txt_file = join(roi_folder, name + '.txt')
                raw_file = join(roi_folder, name + '.raw')
                # c.values.tofile(raw_file)
                if roi == '11':
                    np.savetxt(txt_file, c.values)

                # Map it to mesh
                atlas_file = join(atlas_f, 'atlas_%s.m' % roi)
                out_file = raw_file = join(roi_folder, name + '.m')
                min_cut = c.min()
                max_cut = c.max()

                cmd = ccbbm + ' -color_attribute2 %s %s %s %f %f' %  (atlas_file, raw_file, out_file, min_cut, max_cut)
                
                print(cmd)
                # os.system(cmd)
