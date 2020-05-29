
# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
# get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])
import json
import requests_with_caching
import sys
sys.setExecutionLimit(40000)
def get_movies_from_tastedive(str1):
    baseurl='https://tastedive.com/api/similar'
    params_diction={}
    params_diction['q']=str1
    params_diction['type']='movies'
    params_diction['limit']='5'
    resp = requests_with_caching.get(baseurl, params=params_diction)
    str1_ds=resp.json()
    return str1_ds
    
def extract_movie_titles(lst):
    name_arr=[]
    for d in range(len(lst['Similar']['Results'])):
        name_arr.append(lst['Similar']['Results'][d]['Name'])
    return name_arr

def get_related_titles(lst):
    new_lst=[]
    for ele in lst:
        new_lst.append(extract_movie_titles(get_movies_from_tastedive(ele)))
    final_lst=[]
    for i in range(len(new_lst)):
        for j in new_lst[i]:
            if j not in final_lst:
                final_lst.append(j)
    return final_lst

def get_movie_data(s):
    baseurl='http://www.omdbapi.com/'
    params_diction={}
    params_diction['t']=s
    params_diction['r']='json'
    resp=requests_with_caching.get(baseurl,params=params_diction)
    s_ds=resp.json()
    return s_ds

def get_movie_rating(dic):
    rating=0
    l=dic['Ratings']
    for i in range(len(l)):
        #print(l[i]['Source'])
        if l[i]['Source']=='Rotten Tomatoes':
            st=l[i]['Value'].replace('%','')
            t=int((st))
            rating+=t
    return rating       

def get_sorted_recommendations(lst):
    rs=get_related_titles(lst)
    rs.sort()
    #print(rs)
    rate_lst=[]
    for i in range(len(rs)):
        rate_lst.append(get_movie_rating(get_movie_data(rs[i])))
    sorted_lst=[]
    #rate_lst.sort()
    dd=dict((i, rate_lst.count(i)) for i in rate_lst)
    #print(dd)
    s_dict=list(zip(rs,rate_lst)) 
    So=sorted(s_dict,key = lambda x: x[1],reverse=True)
    for i in So:
        sorted_lst.append(i[0])
    return sorted_lst      
print(get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"]))
