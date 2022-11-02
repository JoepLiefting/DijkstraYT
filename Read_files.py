import pandas as pd

import numpy as np

import copy

def read_D(what, K):

    D_path = "C:/Intermodal/Case study/Preferences/D_EGS - 10r.xlsx"

    D_origin_barge = pd.read_excel(D_path, 'Barge')

    D_origin_train = pd.read_excel(D_path, 'Train')

    D_origin_truck = pd.read_excel(D_path, 'Truck')



    D_origin_barge = D_origin_barge.set_index('N')

    D_origin_train = D_origin_train.set_index('N')

    D_origin_truck = D_origin_truck.set_index('N')



    D_origin_barge = D_origin_barge.values

    D_origin_train = D_origin_train.values

    D_origin_truck = D_origin_truck.values



    D = {}

    for k in range(len(K)):

        if K[k, 5] == 1:

            D[k] = D_origin_barge.copy()

        else:

            if K[k, 5] == 2:

                D[k] = D_origin_train.copy()

            else:

                D[k] = D_origin_truck.copy()

    if what == 'D':

        return D

    D_origin_All = pd.read_excel(D_path, 'All')

    D_origin_All = D_origin_All.set_index('N')

    D_origin_All = D_origin_All.values

    if what == 'D_All':

        return D, D_origin_All

    if what == 'all':

        return D, D_origin_All, D_origin_barge, D_origin_train, D_origin_truck



def read_R_K(request_number_in_R, what='all'):

    Data = pd.ExcelFile(data_path)

    if what == 'K' or what == 'revert_K':

        K = pd.read_excel(Data, 'K')

        K = K.set_index('K')

        if what == 'revert_K':

            revert_K = dict(zip(K.index, range(len(K))))

            return revert_K

        K = K.values

        return K

    if what == 'all' or 'noR_pool':

        R = pd.read_excel(Data, 'R_' + str(request_number_in_R))

        revert_r = R['p'][0]



        if isinstance(revert_r, str):

            names = revert_names('str')

        else:

            names = revert_names('int')

        R['p'] = R['p'].map(names).fillna(R['p'])

        R['d'] = R['d'].map(names).fillna(R['d'])

        R.insert(7, 'r', range(len(R)))

        R = R.values

        # change name of r to -carrier00request_number

        for index in range(len(R)):

            R[index, 7] = R[index, 7] + 100000 * parallel_number



        c_delay_list = []

        for request_number in R[:, 7]:

            index_r = list(R[:, 7]).index(request_number)

            if R[index_r, 5] - R[index_r, 2] < 30:

                c_delay_list.append(100)

            else:

                if R[index_r, 5] - R[index_r, 2] < 54:

                    c_delay_list.append(70)



                else:

                    c_delay_list.append(50)

        # R['c_delay'] = c_delay_list

        R = np.append(R, np.c_[c_delay_list], axis=1)

        R_info = -1



        R_pool = R.copy()

        K = pd.read_excel(Data, 'K')

        K = K.set_index('K')

        K = K.values

        if what == 'noR_pool':

            return R, R_info, K

        if what == 'all':

            return R, R_info, K, R_pool





def revert_names(type='str'):

    if type == 'str':

        return {'Delta': 0, 'Euromax': 1, 'HOME': 2, 'Moerdijk': 3, 'Venlo': 4, 'Duisburg': 5,

                'Willebroek': 6, 'Neuss': 7, 'Dortmund': 8, 'Nuremberg': 9}

    else:

        return {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9}



def read_no_route():

    # please change it to your own data path

    Barge_no_land_path = "C:/Intermodal/Case study/Barge_no_land.xlsx"

    no_route_barge = pd.read_excel(Barge_no_land_path, 'Barge')

    no_route_truck = pd.read_excel(Barge_no_land_path, 'Truck')

    names = revert_names()

    no_route_barge['O'] = no_route_barge['O'].map(names).fillna(no_route_barge['O'])

    no_route_barge['D'] = no_route_barge['D'].map(names).fillna(no_route_barge['D'])

    no_route_barge = no_route_barge.values

    no_route_truck = no_route_truck.values

    return no_route_barge, no_route_truck



parallel_number = 1



#please change it to your own data path

data_path = "C:/Intermodal/Case study/vs. Wenjing/instances/Intermodal_EGS_data_all.xlsx"



#read routes that are unsuitable to barges and trucks

no_route_barge, no_route_truck = read_no_route()



Data = pd.ExcelFile(data_path)



#number of requests, it can be 5, 10, 20, 30, 50, 100 ...

request_number_in_R = 10



#terminals

N = pd.read_excel(Data, 'N')

N = N.values

#change names of terminals to numbers

names = revert_names()



#read depots

o = pd.read_excel(Data, 'o')

o = o.set_index('K')

o['o'] = o['o'].map(names).fillna(o['o'])

o['o2'] = o['o2'].map(names).fillna(o['o2'])

o = o.values



#transshipment terminals

T = pd.read_excel(Data, 'T')

T['T'] = T['T'].map(names).fillna(T['T'])

T = list(T['T'])



#requests, inforation of requests, vehicles, requests pool

R, R_info, K, R_pool = read_R_K(request_number_in_R)

#distance between terminals of all vehicles, distance between terminals of trucks

D, D_origin_All = read_D('D_All', K)