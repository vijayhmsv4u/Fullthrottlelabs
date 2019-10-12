from django.shortcuts import render
from rest_framework import response, status, decorators
from django.conf import settings
import os
import pandas as pd

# Create your views here.
@decorators.api_view(['GET'])
def search(request):
    word= request.GET.get("word",None)
    if not os.path.isfile(settings.UNIGRAM_PATH):
        return response.Response({
                    "data": None,
                    "message":"Unigram File Not Found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
    if not word.isalpha():
        return response.Response({
                    "data": None,
                    "message":"Input should not have special characters"
                },
                status=status.HTTP_404_NOT_FOUND
            )

    if word:
        filter_unigrams={}
        unigram_data= pd.read_csv(settings.UNIGRAM_PATH, index_col=0)
        unigram_data.dropna(inplace=True)
        for unigram,unigram_value in unigram_data.to_dict()["count"].items():
            if type(unigram)==str and word in unigram:
                if unigram.find(word) not in filter_unigrams.keys():
                    filter_unigrams[unigram.find(word)]={}
                if unigram_value not in filter_unigrams[unigram.find(word)].keys():
                    filter_unigrams[unigram.find(word)][unigram_value]=[]
                filter_unigrams[unigram.find(word)][unigram_value].append(unigram)

        sorted_unigrams=[]
        count=0
        
        for index,filtered_unigram in filter_unigrams.items():
            unigrams_count=list(filtered_unigram.keys())
            unigrams_count.sort(reverse=True)
            for unigram in unigrams_count:
                for uni in filtered_unigram[unigram]:
                    if count<25:
                        sorted_unigrams.append(uni)
                        count+=1
                    else:
                        break
        sorted_unigrams.sort(key=len)
        if word in sorted_unigrams:
            sorted_unigrams.remove(word)
            sorted_unigrams.insert(0, word)
        return response.Response({
                    "data": sorted_unigrams,
                    "message":"Data Retrieved SuccessFully"
                },
                status=status.HTTP_200_OK
            )    
    else:
        return response.Response({
                    "data": None,
                    "message":"Enter Valid Input"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
