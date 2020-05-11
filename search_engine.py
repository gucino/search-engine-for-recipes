# -*- coding: utf-8 -*-
"""
Created on Mon May 11 20:00:19 2020

@author: Tisana
"""

###############################
#import library
import json
import numpy as np
import string

with open('recipes.json') as json_file:
    data = json.load(json_file)
    

###############################
#remove duplicate recipes
#clean data set
title_list=[]
new_data=[]
for each_dict in data:
    if each_dict["title"] not in title_list:
        new_data.append(each_dict)
        title_list.append(each_dict["title"])
                
###############################
#Tokenisation
#input string query output list of string without punctuation and digits more than 3 letter

def Tokenisation(query):
    punctuation=string.punctuation
    digit=string.digits
    
    for each_punctuation in punctuation:
        query=query.replace(each_punctuation," ")
    for each_digit in digit:
        query=query.replace(each_digit," ")
        #print(each_punctuation)
    query_list=query.split()
    new_query_list=[]
    for each_word in query_list:
        #convert to lower case
      
        each_word=each_word.lower()
        if each_word not in punctuation and  each_word not in digit and len(each_word)>=3:
            
            #another check
            for each_punctuation in punctuation:
                each_word=each_word.replace(each_punctuation," ")
            for each_digit in digit:
                each_word=each_word.replace(each_digit," ")
            new_query_list.append(each_word)
    return new_query_list
    
###############################
#function to assign which feature(list) to be extract for each word when doing inverted index 

def list_to_append(each_dict,key):
    list=[]

    list.append(each_dict["title"])
    list.append(key) #where the item appear
    feature_list=["rating","ingredients","directions","calories","protein","fat"]
    
    for each_feature in feature_list:
        
        if each_feature in each_dict:
            if each_feature=="ingredients" or each_feature=="directions":
                list.append(len(each_dict[each_feature]))
            else:
                list.append(each_dict[each_feature])
        else:
            list.append("-")

    return list
#inverted index
#input data set, output inverted index format
#inverted index contain list which map the location (name of recipe,key at item appear,rating,len(ingredient),len(direction),cal,protrin,fat)
        
def inverted_index(data_set):

    inverted_index_dict={}
    
    for each_dict in data_set:
        for each,key in zip(each_dict.values(),each_dict):
            
            if type(each)==str:
                string_list=Tokenisation(each)
                for each_string in string_list:
                    each_string=each_string.lower()
                    if each_string in inverted_index_dict:                      
                        #inverted_index_dict[each_string].append([each_dict["title"],key,each_dict["rating"],len(each_dict["ingredients"]),len(each_dict["directions"])])
                      
                        inverted_index_dict[each_string].append(list_to_append(each_dict,key))
                    else:
                        #location recipe,key
                        
                        inverted_index_dict[each_string]=[list_to_append(each_dict,key)]
                        #inverted_index_dict[each_string]=[[each_dict["title"],key,each_dict["rating"],len(each_dict["ingredients"]),len(each_dict["directions"])]]
            elif type(each)!=int and type(each)!=float:
                #for list
                each_list=each
                for each_word in each_list:
                    each_word=Tokenisation(each_word)
                    for each_string in each_word:
                        each_string=each_string.lower()
                        if each_string in inverted_index_dict:
                            #location recipe,key
                          
                            inverted_index_dict[each_string].append(list_to_append(each_dict,key))
                            #inverted_index_dict[each_string].append([each_dict["title"],key,each_dict["rating"],len(each_dict["ingredients"]),len(each_dict["directions"])])
                         
                        else:
                            #location recipe,key
                        
                            inverted_index_dict[each_string]=[list_to_append(each_dict,key)]
                            #inverted_index_dict[each_string]=[[each_dict["title"],key,each_dict["rating"],len(each_dict["ingredients"]),len(each_dict["directions"])]] 


    return inverted_index_dict

###############################
#Search
#input the all word from dictionary and new_query_list (Tokenisation)
#output list of recipe(title) in which the query appera in and word assoicated with recipe

#to make sure that all word appear in that recipe
def find_recipe_in_commmon(check_all_word):
    result_set=set(check_all_word[0])
    for each_list in check_all_word[1:]:
        result_set.intersection_update(each_list)
    result_list=list(result_set)
    return result_list

def what_recipe_to_consider(dict,tokenisation_list):
    recipe_title_list=[]
    check_all_word=[]
    word_to_consider_list=[]
    for each_word in tokenisation_list:
        local_list=[]
        #check if "each word" in dictionary
        if each_word in dict:
            #print("for ",each_word," word")
            for each_list in dict[each_word]:
               
                if each_list[1]!="calories" and each_list[1]!="fat" and each_list[1]!="protein" and each_list[1]!="rating":
                    recipe_title_list.append(each_list) 
                    #print("found word ",each_word," in ",each_list[0])
                    local_list.append(each_list[0])
            word_to_consider_list.append(each_word)
        check_all_word.append(local_list)
    #print("check : ",check_all_word)
    recipe_to_consider_list=find_recipe_in_commmon(check_all_word)
    #print("consider only : ",recipe_to_consider_list)
    #print("_________")
    #build new final recipe list
    full_recipe_to_consider_list=[]
    for each_list in recipe_title_list:
        if each_list[0] in recipe_to_consider_list:
            full_recipe_to_consider_list.append(each_list)
            
    #print(full_recipe_to_consider_list)
    return full_recipe_to_consider_list,word_to_consider_list
###############################
#function tosort the list  assending or decending


'''
def sort(input_list,assending_or_decending):
    #list=input_list[:]
    sorted_list=[]
    while len(input_list)!=0:
        value_list=[]
        for each_list in input_list:
            value_list.append(each_list[1])
        if assending_or_decending=="decending":
            index_value=value_list.index(max(value_list))
        elif assending_or_decending=="assending":
            index_value=value_list.index(min(value_list))
            
        sorted_list.append(input_list[index_value])
        input_list.remove(input_list[index_value])
    return sorted_list 
'''
###############################
#order : calculate socre for each associated recipe
#input recipe list, keyword list (tokened query list),dict
#output list of recipe associated with score
def order(recipe_list,ordering):

    if ordering=="normal":
        scoring=[["title",8],["categories",4],["ingredients",2],["directions",1]]
        score_dic={}
        
        #number of qord to consider is 
        
        for each_list in recipe_list[0]:
            if each_list[0] not in score_dic:
                #create new score for this recipe
                #add rating core to each recipe
                if each_list[2]=="-":
                    rating=0
                else:
                    rating=each_list[2]
                #print("___________")
                #print("rating of ",each_list[0]," is ",rating)
                #score_dic[each_list[0]]=[0,num_word_to_consider*rating]
                #score_dic[each_list[0]]=[0,rating]
                score_dic[each_list[0]]=[rating]
            #assign score
      
            for each_scoring in scoring:
           
                if each_scoring[0]==each_list[1]:
                    #print("found the word at ",each_list[1])
                    score_gain=each_scoring[1]
                    #print("add ",score_gain ,"score")
            #find where to add score to  
            #score_dic[each_list[0]][0]+=score_gain
            score_dic[each_list[0]][0]+=score_gain
            #print(score_dic)
        '''
        #convert back to list
        score_list=[]
        for each_value,each_key in zip(score_dic.values(),score_dic):
            score_list.append([each_key,sum(each_value)])
        #print(score_list)
        #sort from max to min value
        sorted_score_list=sort(score_list,"decending")
        '''
        sorted_score_list=sorted(score_dic.items(),key=lambda x:x[1],reverse=True)
        return sorted_score_list           
                
    elif ordering=="simple":
        complexity_list=[]
        check_recipe_list=[]
        for each_recipe in recipe_list[0]:
            #if missing either ingredients or direction NOT appear in search
            if each_recipe[3]!="-" and each_recipe[4]!="-" and each_recipe[0] not in check_recipe_list and each_recipe[3]!=1 and each_recipe[4]!=1:
                check_recipe_list.append(each_recipe[0])
                #complexity=each_recipe[3]*each_recipe[4]
                #each_complexity_list=[each_recipe[0],each_recipe[3]*each_recipe[4]]
                complexity_list.append([each_recipe[0],each_recipe[3]*each_recipe[4]])
        '''
        sorted_complexity_list=sort(complexity_list,"assending") 
        '''
        sorted_complexity_list=sorted(complexity_list,key=lambda x:x[1])
        return sorted_complexity_list
    
    elif ordering=="healthy":
        cost_cuntion_list=[]
        check_recipe_list=[]
        for each_recipe in recipe_list[0]:
            #if missing either cal, protein or fat NOT appear in search
            if each_recipe[5]!="-" and each_recipe[6]!="-" and each_recipe[7]!="-" and each_recipe[0] not in check_recipe_list:
                check_recipe_list.append(each_recipe[0])
                
                #select n
                
                #cal=each_recipe[5]
                #protein=each_recipe[6]
                #fat=each_recipe[7]
                #n=1
                cost_function=(abs(each_recipe[5]-(510))/510)+(2*(abs(each_recipe[6]-(18))/18))+(4*(abs(each_recipe[7]-(150))/150))
                #each_cost_function_list=[each_recipe[0],cost_function]
                cost_cuntion_list.append([each_recipe[0],cost_function])
        
        #sorted_cost_function_list=sort(cost_cuntion_list,"assending")
        sorted_cost_function_list=sorted(cost_cuntion_list,key=lambda x:x[1])
        return sorted_cost_function_list
###############################
#count 
#funtion to cut ordered recipe list according to count (default 10)
'''
def count_cut(count,ordered_recipe_list):
    fianl_list=[]
    #ordered_recipe_list=ordered_recipe_list[:count]
    for each in ordered_recipe_list[:count]:
        #display oly title
        fianl_list.append(each[0])
    return fianl_list
'''
###############################

dict=inverted_index(new_data)
def search(query, ordering = 'normal', count = 10):
    #tokenisation_list=Tokenisation(query)
    
    #recipe_list=what_recipe_to_consider(dict,tokenisation_list)
    #ordered_recipe_list=order(recipe_list,ordering)
    #print_recipe_list=count_cut(count,ordered_recipe_list)
    
    print_recipe_list=order(what_recipe_to_consider(dict,Tokenisation(query)),ordering)
    #print_recipe_list=
    if len(print_recipe_list)==0:
        pass
    else:
        for each in print_recipe_list[:count]:
            print(each[0])
    return print_recipe_list