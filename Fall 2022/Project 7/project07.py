


import pandas as pd
import numpy as np
import math
import matplotlib as mp
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def extract_mz(file_path:str) -> 'pandas.core.frame.DataFrame':
    """
     Given a file path or file name of a csv file in the active working directory, extract_mz will return a
     DataFrame organized with mz being the set of features
    Args:
        file path: The path or file name to the `.csv` file.

    Returns:
        A sorted (by ascending mz values) DataFrame organized with mz as the columns and Samples as the rows being the set of features.
    
    Ultimately this script uses a for loop which indexes a row and column of a data frame of zeros of a predetermined size and replaces each value 
    with the corresponding value of each data point from the data frame that contains the metabolite data. The final data frame consists of the 
    organized data with the mz values as column headers and a new samples column with the name of the samples as the first column.
    
    """
    
    df = pd.read_csv(file_path)
    df = df.sort_values(by='mz', ascending= True, ignore_index = True) #sorts the data according to ascending mz values
    cols = list(df['mz']) #converts sorted mz values into a list
    df = df.drop(columns = 'mz') #drops the 'mz' values column
    new_cols = pd.DataFrame({'Samples': df.columns}) #dummy data frame to acquire dimensions
    col_len = len(cols) #calculates the length of the new column headers or the 'mz' column of the original dataset
    row_len = len(df.columns) #calculates the length of rows for the new dataframe
    new_df = pd.DataFrame(np.zeros((row_len, col_len)), columns = cols) #generates a data frame of zeros in the dimensions of the new dataframe with 'mz' values as headers
    
    #the for loops below index the row of the new data frame and fill in the values as necessary
    for j in list(range(0, row_len)):
        for i in list(range(0, col_len)):
            new_df.iloc[j, i] = df.iloc[i,j]
            
    new_df = pd.concat([new_df, new_cols], axis = 1) #vertically concatenates Samples columns
    first = new_df.pop('Samples') #removes Samples column from dataframe and stores in in this variable
    newer_df = new_df.insert(0, 'Samples', first) #inserts removed samples column as the first column
        

        
    return new_df #should return a data frame with columns that equal the length of the sample columns and columns that equal the length of the column headers 




def mz_datastd(dataframe):
    """
     Uses a Data Frame organized using function mz_extract.
    Args:
        dataframe: a data frame of organized metabolomics data

    Returns:
        mz_datastd returns 3 outputs
        x_val: standardized data using x components
        y_val: standardized data using y components
        new_df: data fram containing all standardized data organized by mz values as column headers
    
    This functions allows extracted mass spectral metabolomics data from a data frame to be prepared for PCA processing.
    Prior to principal component analysis (PCA), the data must be mean centered and standardized. This function standardizes
    the data and out puts the x and y standardized data and a data frame which consists of only the x components since that
    is what we are interested in at the moment.
    """
    samples = [dataframe['Samples']]
    dataframe = dataframe.drop(columns = 'Samples')
    x_val = dataframe.loc[:, dataframe.columns].values
    #y_val = dataframe.loc[:, samples].values
    x_val = StandardScaler().fit_transform(x_val)
    #y_val = StandardScaler().fit_transform(y_val)
    new_df = pd.DataFrame(data = x_val, columns = dataframe.columns)

    return x_val, new_df



    
    
def met_pca(dataframe, std_data, num_comp):
    """
     Uses a Data Frame organized using function mz_extract.
    Args:
        dataframe: dataframe that contains standardized data.
        std_data: standardized data.
        num_comp: number of components
    Returns:
        met_pca returns 3 outputs
        comp_df: data frame with labeled pca scatter matrix data.
        PC: numpy array with pca scatter matrix data.
        plot: plotted pc data with interactiveplot.
        
    This functions takes the standardized data, performs PCA, and plots the PCA components. The num_comp input
    allows the users to define how many principal components they want to plot using the plotly express library.
    The plotly express library was chosen to provide the user with an interactive plot that would allows them to
    exlude samples they deem uninteresting and/or have control of the axes for better perspectives of the separated
    features.
    
    
    """
    
    pc_colnames = []
    met_pca = PCA(n_components = num_comp)
    count = 0
    pc_count = 1
    while count < num_comp:
        pc_colnames.append('PC ' + str(pc_count + count))
        count += 1
        
    PC = met_pca.fit_transform(std_data)
    pc_df = pd.DataFrame(data = PC, columns = pc_colnames)
    comp_df = pd.concat([pc_df, dataframe[['Samples']]], axis = 1)
    fig = px.scatter_matrix(PC, dimensions=range(2), color = dataframe['Samples'],
                       )
#fig.update_traces(diagonal_visible=False)
    fig.show()
    return comp_df, PC