import unittest
import pytest
import pandas as pd
import numpy as np
import math
import matplotlib as mp
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from project07 import extract_mz, mz_datastd, met_pca

@pytest.mark.parametrize('csv_file',[('metabolites.csv')])
def test_extract_mz(csv_file: str):
    df = extract_mz(csv_file)
    assert len(df.columns) == 488
    assert df.shape == (12, 488)
        
@pytest.mark.parametrize('csv_file',[('metabolites.csv')])
def test_mz_datastd(csv_file: str):
    df = extract_mz(csv_file)
    test_xvals, testdatastd_df = mz_datastd(df)
    np_empty = np.empty(2)
    assert testdatastd_df.shape == (12, 487)
    assert print(type(test_xvals)) == print(type(np_empty))

@pytest.mark.parametrize('csv_file,num_comp',[('metabolites.csv',5)])    
def test_met_pca(csv_file: str, num_comp: int):
    df = extract_mz(csv_file)
    test_xvals, testdatastd_df = mz_datastd(df)
    pca_df, PC = met_pca(df, test_xvals, num_comp)
    assert len(pca_df.columns)-1 == 5
    assert pca_df.shape == (12,6)