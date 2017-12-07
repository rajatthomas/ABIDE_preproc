import os
import os.path as osp
import shutil

import numpy as np
import pandas as pd

def get_subjectinfo(data_dir, file):
    """
    :param file: csv file containing subject information
    :return: dictionary with relevant key/value pairs
    """

    COI_ABIDEI = ['SITE_ID', 'SUB_ID', 'DX_GROUP', 'AGE_AT_SCAN', 'SEX']
    COI_ABIDEII = ['SITE_ID', 'SUB_ID', 'DX_GROUP', 'AGE_AT_SCAN ', 'SEX'] # Notice space after AGE_AT_SCAN

    pheno_file = file + "_ABIDE_I.csv"
    pheno_ABIDEI = pd.read_csv(osp.join(data_dir, pheno_file))[COI_ABIDEI]
    pheno_ABIDEI['ABIDE'] = pd.Series(np.ones(len(pheno_ABIDEI)))

    pheno_file = file + "_ABIDE_II.csv"
    pheno_ABIDEII = pd.read_csv(osp.join(data_dir, pheno_file), encoding='cp1252')[COI_ABIDEII]
    pheno_ABIDEII['ABIDE'] = pd.Series(2*np.ones(len(pheno_ABIDEII)))

    pheno = pd.concat([pheno_ABIDEI, pheno_ABIDEII], ignore_index=True)

    return pheno


def construct_paths(data_dir, sub_info):
    """
    E.G o/p path: /data/subject_control01/anat/ and /data/subject_control01/func
    :param data_dir: primary data directory
    :param sub_info: SITE_ID, SUB_ID and DX, info to construct path
    :return: df_path -> from_path, to_path, odl_id, new_id
    """

    df_path = pd.DataFrame(columns=['FROM_PATH_ANAT', 'TO_PATH_ANAT', 'FROM_PATH_REST', 'TO_PATH_REST',
                                    'OLD_SUB_ID', 'NEW_SUB_ID', 'ABIDE'], index=range(len(sub_info)))

    new_id = 0
    for i, row in sub_info.iterrows():
        site = row['SITE_ID']
        subj = str(row['SUB_ID'])

        if row['ABIDE'] == 1:
            subj = subj.zfill(7)  # they have two leading zeros in ABIDE_I

        if row['DX_GROUP'] == 1:
            new_subj = 'subject_ASD_' + str(new_id).zfill(4)

        if row['DX_GROUP'] == 2:
            new_subj = 'subject_CON_' + str(new_id).zfill(4)

        from_path = osp.join(data_dir, site, subj, 'session_1')
        to_path = osp.join(data_dir, 'data', new_subj)

        from_path_anat = osp.join(from_path, 'anat_1')
        from_path_rest = osp.join(from_path, 'rest_1')

        to_path_rest = osp.join(to_path, 'rest')
        to_path_anat = osp.join(to_path, 'anat')

        df_path.loc[new_id] = pd.Series({'FROM_PATH_ANAT': from_path_anat, 'TO_PATH_ANAT': to_path_anat,
                                         'FROM_PATH_REST': from_path_rest, 'TO_PATH_REST': to_path_rest,
                                         'OLD_SUB_ID': subj, 'NEW_SUB_ID': str(new_id).zfill(4), 'ABIDE': row['ABIDE']})

        new_id += 1

    return df_path

def transfer_data(path_info):

    for i in range(len(path_info)):

        if path_info.iloc[i]['ABIDE'] == 1:
            from_file_anat = osp.join(path_info.iloc[i]['FROM_PATH_ANAT'], 'mprage.nii.gz')
        else:
            from_file_anat = osp.join(path_info.iloc[i]['FROM_PATH_ANAT'], 'anat.nii.gz')

        from_file_rest = osp.join(path_info.iloc[i]['FROM_PATH_REST'], 'rest.nii.gz');

        to_file_anat = osp.join(path_info.iloc[i]['TO_PATH_ANAT'], 'anat.nii.gz')
        to_file_rest = osp.join(path_info.iloc[i]['TO_PATH_REST'], 'rest.nii.gz')

        os.makedirs(path_info.iloc[i]['TO_PATH_ANAT'], exist_ok=True)
        os.makedirs(path_info.iloc[i]['TO_PATH_REST'], exist_ok=True)

        shutil.copyfile(from_file_anat, to_file_anat)
        shutil.copyfile(from_file_rest, to_file_rest)

        print('copied {0} of {1} files'.format(i, len(path_info)))

if __name__ == '__main__':

    data_dir = "/data_remote/ABIDE/"
    pheno_file = "Phenotypic"
    sub_info = get_subjectinfo(data_dir, pheno_file)

    path_info = construct_paths(data_dir, sub_info)
    transfer_data(path_info)