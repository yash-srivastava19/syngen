## First, let's see what kind of data we have.
import pandas as pd

df1 = pd.read_csv("data/reviews_supplements.csv")
with open("text_review_1.txt", "w") as f:
    for i in range(4):
        pass
        # print(df1.iloc[i], sep = ",")

df2 = pd.read_csv("data/product_asin.csv")
with open("text_review_2.txt", "w") as f:
    for i in range(4):
        pass
        # print(df2.iloc[i], sep = ",")    

## Now, let's try to see what kind of prompts we should use to generate synthetic data based on csv enteries.

## We have generated 3 prompts, one is base, one is for diversity, one is for language complexity, and one is for dialouge length.
prompt_base = """
I have the following CSV data for health supplements:

rating, title, text, asin, parent_asin, user_id, timestamp, helpful_vote, verified_purchase, data, time
4,B Complex in gel cap form,I bought this along with Vit C in gel cap form...,B00012ND5G,B00012ND5G,AGDVFFLJWAQ3ULNNKF4LXID2RVSQ,2009-12-11 00:37:33,1,True,2009-12-11,00:37
5,Five Stars,great product,B00013Z0ZQ,B00013Z0ZQ,AG3BSKXHDGP6E3EGQD2SXCK6KFQQ,2015-01-04 03:11:26,0,True,2015-01-04,03:11
5,Five Stars,Came as expectedly,B00013Z0ZQ,B00013Z0ZQ,AHG2WKFD4LXPC46WWC6JMQGX52JA,2015-09-27 19:15:33,0,True,2015-09-27,19:15

I would like you to generate synthetic data based on this input. Produce me 5 more examples of the data formatted for CSV to augment dataset. Give only the CSV entries.
"""

diversity_prompt = """
I have the following CSV data for health supplements:

rating, title, text, asin, parent_asin, user_id, timestamp, helpful_vote, verified_purchase, data, time
4,B Complex in gel cap form,I bought this along with Vit C in gel cap form...,B00012ND5G,B00012ND5G,AGDVFFLJWAQ3ULNNKF4LXID2RVSQ,2009-12-11 00:37:33,1,True,2009-12-11,00:37
5,Five Stars,great product,B00013Z0ZQ,B00013Z0ZQ,AG3BSKXHDGP6E3EGQD2SXCK6KFQQ,2015-01-04 03:11:26,0,True,2015-01-04,03:11
5,Five Stars,Came as expectedly,B00013Z0ZQ,B00013Z0ZQ,AHG2WKFD4LXPC46WWC6JMQGX52JA,2015-09-27 19:15:33,0,True,2015-09-27,19:15

I would like you to generate 5 more examples of synthetic data with a high level of diversity.Give only the CSV entries.

"""

language_complexity_prompt = """
I have the following CSV data for health supplements:

rating, title, text, asin, parent_asin, user_id, timestamp, helpful_vote, verified_purchase, data, time
4,B Complex in gel cap form,I bought this along with Vit C in gel cap form...,B00012ND5G,B00012ND5G,AGDVFFLJWAQ3ULNNKF4LXID2RVSQ,2009-12-11 00:37:33,1,True,2009-12-11,00:37
5,Five Stars,great product,B00013Z0ZQ,B00013Z0ZQ,AG3BSKXHDGP6E3EGQD2SXCK6KFQQ,2015-01-04 03:11:26,0,True,2015-01-04,03:11
5,Five Stars,Came as expectedly,B00013Z0ZQ,B00013Z0ZQ,AHG2WKFD4LXPC46WWC6JMQGX52JA,2015-09-27 19:15:33,0,True,2015-09-27,19:15

I would like you to generate 5 more examples of synthetic data with a high level of language complexity.Give only the CSV entries.

"""

dialouge_length_prompt = """
I have the following CSV data for health supplements:

rating, title, text, asin, parent_asin, user_id, timestamp, helpful_vote, verified_purchase, data, time
4,B Complex in gel cap form,I bought this along with Vit C in gel cap form...,B00012ND5G,B00012ND5G,AGDVFFLJWAQ3ULNNKF4LXID2RVSQ,2009-12-11 00:37:33,1,True,2009-12-11,00:37
5,Five Stars,great product,B00013Z0ZQ,B00013Z0ZQ,AG3BSKXHDGP6E3EGQD2SXCK6KFQQ,2015-01-04 03:11:26,0,True,2015-01-04,03:11
5,Five Stars,Came as expectedly,B00013Z0ZQ,B00013Z0ZQ,AHG2WKFD4LXPC46WWC6JMQGX52JA,2015-09-27 19:15:33,0,True,2015-09-27,19:15

I would like you to generate 5 more examples of synthetic data with a dialouge length similar to the example given.Give only the CSV entries.

"""

##Now, we will test these on three classes of models. HFs, Cohere, and OLlama.

## This is working, will test further.

# import ollama
# response = ollama.chat(model='llama3.2', messages=[
#   {
#     'role': 'user',
#     'content': prompt_base,
#   },

# ])
# print("From Llama3.2")
# print(response['message']['content'])

##  Works, but the models are too big. Will try with smaller models.
# from transformers import pipeline
# generator = pipeline('text-generation', model='microsoft/Phi-3.5-mini-instruct')
# response = generator(prompt_base, max_new_tokens=700)
# print(response[0]['generated_text'])

## Let's try with commercial model - Cohere.

## Private.
import cohere
co = cohere.ClientV2("5mG9Baoklq9rOXkTSpTvXZ5J6XG4RMGWTHM7p2sp")

response = co.chat(
    model="command-r-plus",
    messages=[
        {
            "role": "user",
            "content": language_complexity_prompt
        }
    ]
)

print(response.message.content[0].text)

