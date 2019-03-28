import csv
import os
import time
import pandas as pd, numpy as np, os, gc

class mapper:
    def _init_(self):
        self.x = [];
        self.y = [];
        # To tell whether the encoding is allowed or not. 0 for YES, 1 for NO
        self.flag = 0;


#Get "path+filename"s from the root file
def filename(file_dir):
    L = []
    for root,dirs,files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.csv':
                L.append(os.path.join(root,file))

    return L

#Get the whole training dataset, not working yet
def conbination(list,k):
    df_head = pd.read_csv(list[0],chunksize=100)
    for i in range(1,k):
        df_now = pd.read_csv(list[i],chunksize=100)
        df_head = df_head.append(df_now)
        #df_head = pd.concat([df_head,df_now],axis=0)
    return df_head

#Count missing value for each attribute. Put them in a same csv
def MVstastic(list):
    df = pd.read_csv('MissingValueDistribution2.csv')
    for i in range(1, len(list)):
        df0 = pd.read_csv(list[i])
        df1 = df0.isnull().sum()
        df = pd.concat([df,df1],axis=1)
        df.to_csv('MissingValueDistribution2.csv',mode = 'a')
    return 0

#Get the unique value of an Attribute(col)
def GetUnicate(col,L):
    t0 = time.time()
    A = mapper()
    #Get the whole data of an Attribute(col)
    for i in range(0,len(L)):
        df = pd.read_csv(L[i], usecols=[col])
        if i == 0:
            df.to_csv('unique\\' + str(col) + '.csv', mode='a')
        else:
            df.to_csv('unique\\' + str(col)+ '.csv',mode = 'a',header=0)
    #Lable encode
    df0 = pd.read_csv('unique\\' + str(col) + '.csv',usecols=[1])
    if df.isnull().any().sum() > 0:
        A.flag = 1
    else:
        cat = pd.Categorical(df0[col],categories=df0[col].unique(),ordered=True)
        cate = cat.codes
        A.x = df0[col].unique()
        A.y = cate
        A.flag = 0
    t1 = time.time()-t0
    print(t1)

    return A


if __name__=="__main__":
    L = filename('D:\\常用\\创新设计\\Detection\\temp')
    temp = {}

    #print (filename('D:\\常用\\创新设计\\Detection\\temp'))
    #print(L[1])
    """df = pd.read_csv(L[1])#or len(L)
    print('The dimensuion of this dataset is:'+ '\n')
    print(df.shape )
    print('\n' + 'Description:'+ '\n' )
    print(df.describe())
    print('Missing value distribution:' + '\n')
    print(df.isnull().sum())
    df2 = df.isnull().sum(axis=1)
    df2.to_csv('MissingValueDistribution_row.csv')
    #print(df.isnull().sum(axis=1))
    #MVstastic(L)"""

    FE = ['EngineVersion', 'AppVersion', 'AvSigVersion', 'Census_OSVersion']
    # LOAD AND ONE-HOT-ENCODE
    OHE = ['AVProductStatesIdentifier',
           'AVProductsInstalled',
           'CountryIdentifier',
           'CityIdentifier',
           'GeoNameIdentifier',
           'LocaleEnglishNameIdentifier',
           'OsBuild',
           'OsSuite',
           'SmartScreen',
           'Census_MDC2FormFactor',
           'Census_OEMNameIdentifier',
           'Census_ProcessorCoreCount',
           'Census_ProcessorModelIdentifier',
           'Census_PrimaryDiskTotalCapacity',
           'Census_PrimaryDiskTypeName',
           'Census_TotalPhysicalRAM',
           'Census_ChassisTypeName',
           'Census_InternalPrimaryDiagonalDisplaySizeInInches',
           'Census_InternalPrimaryDisplayResolutionHorizontal',
           'Census_InternalPrimaryDisplayResolutionVertical',
           'Census_PowerPlatformRoleName',
           'Census_InternalBatteryType',
           'Census_InternalBatteryNumberOfCharges',
           'Census_OSEdition',
           'Census_OSInstallLanguageIdentifier',
           'Census_GenuineStateName',
           'Census_ActivationChannel',
           'Census_FirmwareManufacturerIdentifier',
           'Census_IsTouchEnabled',
           'Wdft_IsGamer',
           'Wdft_RegionIdentifier']

    cols = FE + OHE
    for i in range(0,len(cols)):
        test = GetUnicate(cols[i],L)
        if test.flag == 1:
            print('Sorry,but there is missing data in the attribute' + str(cols[i]))
        else:
            temp.update({cols[i]:test.y})
            print(test.x)
            print(len(test.x))
            print(test.y)
            print(len(test.y))
    df = pd.DataFrame(temp)
    df.to_csv("total.csv",index=False,sep=',')