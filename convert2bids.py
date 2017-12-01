import pandas as pd
import os.path as osp

import numpy as np

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
    :return: (from_path, to_path, new_id)
    """

    df_path = pd.DataFrame(columns=['FROM_PATH', 'TO_PATH', 'OLD_SUB_ID', 'NEW_SUB_ID'], index=range(len(sub_info)))

    for i, row in sub_info.iterrows():
        site = row['SITE_ID']
        subj = str(row['SUB_ID'])

        if row['ABIDE'] == 1:
            subj = subj.zfill(7)  # they have two leading zeros in ABIDE_I
        from_path = osp.join(data_dir, site, )

        df_path.loc[i] = df_path({'FROM_PATH'})




def transfer_data(pheno_file):
    pass



if __name__ == '__main__':

    data_dir = "/data_remote/ABIDE/"
    pheno_file = "Phenotypic"
    sub_info = get_subjectinfo(data_dir, pheno_file)

    construct_paths(data_dir, sub_info)