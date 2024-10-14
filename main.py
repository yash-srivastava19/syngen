# Imports
import os 
import cohere
import ollama
import argparse
from dotenv import load_dotenv
from transformers import pipeline

env = load_dotenv() # Load secrets from .env file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate synthetic data based on CSV entries.')
    parser.add_argument('--prompt_type', type=str, default='base', help='Type of prompt to use for generating synthetic data.', choices=['base', 'diversity', 'lang_complexity', 'text_length'])
    parser.add_argument('--model', type=str, default='ollama', help='Type of model to use for generating synthetic data.', choices=['hf', 'cohere', 'ollama'])
    parser.add_argument('--num_samples', type=int, default=5, help='Number of synthetic samples to generate.')
    args = parser.parse_args()
    
    ##Now, we will test these on three classes of prompts - diversity, language complexity, and text length.

    prompt_base = f"""
    I have the following CSV data for health supplements:

    rating, title, text, asin, parent_asin, user_id, timestamp, helpful_vote, verified_purchase, data, time
    4,B Complex in gel cap form,I bought this along with Vit C in gel cap form...,B00012ND5G,B00012ND5G,AGDVFFLJWAQ3ULNNKF4LXID2RVSQ,2009-12-11 00:37:33,1,True,2009-12-11,00:37
    5,Five Stars,great product,B00013Z0ZQ,B00013Z0ZQ,AG3BSKXHDGP6E3EGQD2SXCK6KFQQ,2015-01-04 03:11:26,0,True,2015-01-04,03:11
    5,Five Stars,Came as expectedly,B00013Z0ZQ,B00013Z0ZQ,AHG2WKFD4LXPC46WWC6JMQGX52JA,2015-09-27 19:15:33,0,True,2015-09-27,19:15

    I would like you to generate {int(args.num_samples)} more examples of synthetic data based on this input. Give only the CSV entries(with column names as well), nothing else.
    """

    diversity_prompt = f"""
    I have the following CSV data for health supplements:

    rating, title, text, asin, parent_asin, user_id, timestamp, helpful_vote, verified_purchase, data, time
    4,B Complex in gel cap form,I bought this along with Vit C in gel cap form...,B00012ND5G,B00012ND5G,AGDVFFLJWAQ3ULNNKF4LXID2RVSQ,2009-12-11 00:37:33,1,True,2009-12-11,00:37
    5,Five Stars,great product,B00013Z0ZQ,B00013Z0ZQ,AG3BSKXHDGP6E3EGQD2SXCK6KFQQ,2015-01-04 03:11:26,0,True,2015-01-04,03:11
    5,Five Stars,Came as expectedly,B00013Z0ZQ,B00013Z0ZQ,AHG2WKFD4LXPC46WWC6JMQGX52JA,2015-09-27 19:15:33,0,True,2015-09-27,19:15

    I would like you to generate {int(args.num_samples)} more examples of synthetic data with a high level of diversity.Give only the CSV entries(with column names as well), nothing else.

    """

    language_complexity_prompt = f"""
    I have the following CSV data for health supplements:

    rating, title, text, asin, parent_asin, user_id, timestamp, helpful_vote, verified_purchase, data, time
    4,B Complex in gel cap form,I bought this along with Vit C in gel cap form...,B00012ND5G,B00012ND5G,AGDVFFLJWAQ3ULNNKF4LXID2RVSQ,2009-12-11 00:37:33,1,True,2009-12-11,00:37
    5,Five Stars,great product,B00013Z0ZQ,B00013Z0ZQ,AG3BSKXHDGP6E3EGQD2SXCK6KFQQ,2015-01-04 03:11:26,0,True,2015-01-04,03:11
    5,Five Stars,Came as expectedly,B00013Z0ZQ,B00013Z0ZQ,AHG2WKFD4LXPC46WWC6JMQGX52JA,2015-09-27 19:15:33,0,True,2015-09-27,19:15

    I would like you to generate {int(args.num_samples)} more examples of synthetic data with a high level of language complexity.Give only the CSV entries(with column names as well), nothing else.

    """

    dialouge_length_prompt = f"""
    I have the following CSV data for health supplements:

    rating, title, text, asin, parent_asin, user_id, timestamp, helpful_vote, verified_purchase, data, time
    4,B Complex in gel cap form,I bought this along with Vit C in gel cap form...,B00012ND5G,B00012ND5G,AGDVFFLJWAQ3ULNNKF4LXID2RVSQ,2009-12-11 00:37:33,1,True,2009-12-11,00:37
    5,Five Stars,great product,B00013Z0ZQ,B00013Z0ZQ,AG3BSKXHDGP6E3EGQD2SXCK6KFQQ,2015-01-04 03:11:26,0,True,2015-01-04,03:11
    5,Five Stars,Came as expectedly,B00013Z0ZQ,B00013Z0ZQ,AHG2WKFD4LXPC46WWC6JMQGX52JA,2015-09-27 19:15:33,0,True,2015-09-27,19:15

    I would like you to generate {int(args.num_samples)} more examples of synthetic data with a dialouge length similar to the example given.Give only the CSV entries(with column names as well), nothing else.

    """

    if args.prompt_type == 'base':
        prompt = prompt_base

    elif args.prompt_type == 'diversity':
        prompt = diversity_prompt

    elif args.prompt_type == 'lang_complexity':
        prompt = language_complexity_prompt

    elif args.prompt_type == 'text_length':
        prompt = dialouge_length_prompt

    else:
        print("Invalid prompt type. Please choose from base, diversity, lang_complexity, or text_length.")

    ##Now, we will test these on three classes of models. HFs, Cohere, and OLlama.
    
    if args.model == 'hf':
        # Update: Got the chat template stuff working.
        model_name = 'Qwen/Qwen2.5-1.5B-Instruct'
        print(f"------- Using {model_name} Model for now ---------")
        generator = pipeline('text-generation', model=model_name, trust_remote_code=True)
        response = generator([{"role": "user", "content": prompt}], do_sample=True, max_new_tokens=1000)
        
        # Save stuff to a file.
        with open(f"output/suppl_{args.prompt_type}_hf_qwen_{args.num_samples}_output.csv", "w") as f:
            print(response[0]['generated_text'][1]['content'], file=f)
        
        print(response[0]['generated_text'][1]['content'])
    
    elif args.model == 'cohere':
        model_name = "command-r-plus"
        # api_key = 
        co = cohere.ClientV2(os.environ["COHERE_API_KEY"])
        response = co.chat(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        # Save stuff to a file.
        with open(f"output/suppl_{args.prompt_type}_cohere_{model_name}_{args.num_samples}_output.csv", "w") as f:
            print(response.message.content[0].text, file=f)

        print(response.message.content[0].text)
    
    elif args.model == 'ollama':
        response = ollama.chat(model='llama3.2', messages=[
            {
                'role': 'user',
                'content': prompt,
            },

        ])

        # Save stuff to a file.
        with open(f"output/suppl_{args.prompt_type}_ollama_llama3.2_{args.num_samples}_output.csv", "w") as f:
            print(response['message']['content'], file=f)

        print(response['message']['content'])
    
    else:
        print("Invalid model type. Please choose from hf, cohere, or ollama.")