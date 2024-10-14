# SynGen - Synthetic Data Generation
In the world of AI, data is moat. Unfortunately, finding enough high-quality data for downstream machine learning tasks(especially for problems where data scarcity is a big issue)can be a huge pain.Synthetic data generation using LLMs offers a powerful solution to provide high-quality, diverse, and privacy compliant data. That's what syngen tries to solve. I've tested synthetic data generation of a variety of models and for a variety of prompts. There are tweaks you can do to the complexity, variety, and length of real data, giving you a fine control over the data you want. Syngen also comes up with both a webapp and a cli tool, so use as you please.

## Models and Architecture Tested
3 classes of models were tested, Ollama(Llama3.2), HF(maybe some GPT2 style small model, or phi/Qwen), and commercially avaialble models(Cohere)

3 classes of prompts are testsed, these include prompts for diversity, language complexity, and text length. There is also a base prompt to compare against.

## Problem
Syngen, as the name suggests, generates synthetic data based on existing data. The synthetic data extends the existing data, and tries to adheres to the properties of it.

For the purpose of this project, we'll work with the "supplements" subset of Amazon reviews [dataset](https://amazon-reviews-2023.github.io/main.html), and try to augment the data.  

## What factors we considered?
Using Language Models to augment the dataset gives us fine control over the type to data we can generate - we can just prompt the LM to give exactly what kind of data we need for our use case. For the purpose of this study, we are going to test on three factos, namely - language complexity, divevrsity, and length. Let's try to understand what each of these factor imply

- **Language Complexity:** Language complexity, although difficult to define, basically refers how easily the comprehension of the sentence is. Given the real-world dataset, does the augmented data is similar in terms of language complexity?  

- **Language Diversity:** Language Diversity refers to the different ways in which the same sentence can be communicated. For our use case, we study does the augmented data is similar in terms of language diversity?

- **Text Length:** Most users when writing a review, prefer not to write too much, does LMs do that too, or they end up writing really long reviews - which can raise suspicion on the authenticity of the review.

## Assumptions

- For HF models, I are sticking our analysis to models which are around 1B parameters, I don't have the bandwidth to test larger models, so I chose smaller models.

- For commercial LLMS, I chose Cohere models cause their free tier works for my use case, and the command-r-plus model is actually really good.

- To test with completely local model, I chose Llama3.2, accessed by Ollama.

## Implementation details
First, let us see the directory structure.
```
- data
|_ product_asin.csv
|_ reviews_supplements.csv

- output
|_ cohere_XXX.csv
|_ hf_XXX.csv
|_ ollama_XXX.csv

- app.py
- main.py
- README.md
- requirements.txt
- .gitignore
```

To run the application from CLI(after installing and setting up environment variables), run the following command:
```
python main.py 
```
Additionally, you can pass these options:
- `--prompt_type`: Type of prompt to use for generating synthetic data. Valid choices are: 'base', 'diversity', 'lang_complexity', 'text_length'

- `--model`: Type of model to use for generating synthetic data. Valid choices are: 'hf', 'cohere', 'ollama'. In HF, "Qwen/Qwen2.5-1.5B-Instruct" is used based on our assumption.

- `--num_samples`: Number of synthetic samples to generate, defaults to 5.

Additionally, to run the web app, run the following command.

```
streamlit run app.py
```

## Results and Analysis

The generate CSV files from all the models on different types of prompts are in the `output` folder with the name format as:

```
suppl_{prompt_type}_{model}_{num_samples}_output.csv
```

Below mentioned is the analysis of the output(on 10 samples to understand where the output breaks)

### Base Prompt Analysis

1. Cohere Command R+ : 
**Rating:** The output seemed to infer from few shots that the rating were on 5 scale, and most products were rated either 2(1), 3(2), 4(3), 5(4).

**Title:** The title is relevant to the product review, with easy to understand language, and the sentiment is excited for most titles.

**Text:** Reviews are mostly one sentence, and easy to understand. Since the ratings are high, the sentiment is positive.

**Asin:** Asin follows the structure from the original data, and is consistent across all enteries.

**Parent_Asin:** Similar to Asin, these are also similar to one in the original dataset.

**User_ID:** The length of user_id is consistent, and unique for all enteries.

**Timestamp:** The timestamps are valid, and there is not too much discrepancy in year, month and day.

**Helpful_vote:** The synthetic data, like the real data has 1-2 helpful votes for the product.

**Time:** The timestamp and time entries are consistent with each other. The time is same as of original data(00:37, 19:15, 03:11)

2. Qwen1.5B :
**Rating:** The output seemed to infer from few shots that the rating were on 5 scale, and most products were rated 5(7), and few are 4(3).

**Title:** For most 5 star reviews, the title is "Five Stars" - so, not all titles are relevant to the product review.

**Text:** Reviews are one sentence. The reviews are in an easy to understand language, but the sentiment is neutral

**Asin:** Asin follows the structure from the original data, and is consistent across all enteries.

**Parent_Asin:** Similar to Asin, these are also similar to one in the original dataset.

**User_ID:** The length of user_id is consistent, but there are multiple same user_id enteries.

**Timestamp:** The timestamps are valid, and the date are different(2015-2017). Years range from 2009 to 2017.

**Helpful_vote:** Most reviews have 0 helpful votes, and some have 1 helpful votes.

**Time:** The timestamp and time entries are consistent with each other. The time is same as of original data(00:37, 19:15, 03:11)

3. Llama3.2 :
**Rating:** The output seemed to infer from few shots that the rating were on 5 scale, and most products were rated 3(3), 5(4), and few are 4(3).

**Title:** The titles are basically the product name, not completely relevant to the product review.

**Text:** Reviews are one sentence. The reviews are in an easy to understand language, but the sentiment is neutral

**Asin:** Asin follows the structure from the original data, but all are same for all enteries.

**Parent_Asin:** Similar to Asin, these are same for all enteries.

**User_ID:** The length of user_id is consistent, but there are multiple same user_id enteries(2 distinct user ids).

**Timestamp:** The timestamps are valid, and the date are different(2009-2015).

**Helpful_vote:** Most reviews have 0 helpful votes, and some have 1 helpful votes.

**Time:** The timestamp and time entries are consistent with each other. Most of the time is same as of original data(00:37, 19:15, 03:11)

### Diversity Prompt Analysis

1. Cohere Command R+:
**Rating:** The output seemed to infer from few shots that the rating were on 5 scale, and most products were rated either 4/5.

**Title:** The title is relevant to the product review, with easy to understand language.

**Text:** Reviews are mostly one sentence, and easy to understand - in a more converstional style. For the reviews with high ratings, the sentiment is positive and for low ratings the sentinent is negative.

**Asin:** Asin follows the structure from the original data, and is consistent across all enteries.

**Parent_Asin:** Similar to Asin, these are also similar to one in the original dataset.

**User_ID:** The length of user_id is consistent, and unique for all enteries.

**Timestamp:** The timestamps are valid, and there is not too much discrepancy in year, month and day. Years range from 2015-2023.

**Helpful_vote:** The synthetic data, like the real data has 1-2 helpful votes for the product.

**Time:** The timestamp and time entries are consistent with each other. The times are random.

2. Qwen1.5B :
**Note:** The model was unclear in understanding that the output was expected in csv format, and it gave it in markdown table format. Even after emphasis on diversity, the product reviews are same as the base prompt.

**Rating:** The output seemed to infer from few shots that the rating were on 5 scale, and most products were rated 5(7), and few are 4(3).

**Title:** For most 5 star reviews, the title is "Five Stars" - so, not all titles are relevant to the product review.

**Text:** Reviews are one sentence. The reviews are in an easy to understand language, but the sentiment is neutral

**Asin:** Asin follows the structure from the original data, and is consistent across all enteries.

**Parent_Asin:** Similar to Asin, these are also similar to one in the original dataset.

**User_ID:** The length of user_id is consistent, but there are multiple same user_id enteries.

**Timestamp:** The timestamps are valid, and the date are different(2015-2017). Years range from 2009 to 2017.

**Helpful_vote:** Most reviews have 0 helpful votes, and some have 1 helpful votes.

**Time:** The timestamp and time entries are consistent with each other. The time is same as of original data(00:37, 19:15, 03:11)

3. Llama3.2 :
**Rating:** The output could not infer from few shots that the rating were on 5 scale, and rated from 1-10(serially).

**Title:** The title are mostly one word, rating the product.

**Text:** Reviews are one sentence, to the point. However, For two products(first and last entry), the review is "Excellent Product Review".

**Asin:** Asin is same for all enteries, with the generic entry "1234567890".

**Parent_Asin:** Similar to Asin, these are also same for all enteries.

**User_ID:** The length of user_id is consistent, but all of the user ids are same.

**Timestamp:** The timestamps are valid, and the date are different(Years range from 2008 to 2018).

**Helpful_vote:** All reviews have 1 helpful votes.

**Time:** The timestamp and time entries are inconsistent with each other. Most time enteries are same as of original data(00:37, 19:15, 03:11).

### Language Complexity Prompt Analysis

1. Cohere Command R+:
**Rating:** The output seemed to infer from few shots that the rating were on 5 scale. Interestingly, some prducts were rated 4.5, 4.6, 4.7, 4.8 - which was not observed in base case.

**Title:** The title is relevant to the product review, with easy to understand language. The title encompassses a good summary of the review.

**Text:** Reviews are more than one sentence long, and relatively more complex than the base case. The tone of the reviews was converstational. Since most of the ratings are high, the sentiment of the review is positive.

**Asin:** Asin follows the structure from the original data, and is consistent across all enteries. All of them are distinct for all enteries.

**Parent_Asin:** Similar to Asin, these are also similar to one in the original dataset(all are same as Asin).

**User_ID:** The length of user_id is not consistent with the original dataset, and is of generic nature such as "A123456789" or "B987654321".

**Timestamp:** The timestamps are valid, and there is not too much discrepancy in year, month and day. Years range from 2022-2023.

**Helpful_vote:** Reviews have helpful vote ratings ranging from 1-4.

**Time:** The timestamp and time entries are consistent with each other. The times are random, and unlike the few-shot examples we used to prompt the model.

2. Qwen 1.5B :
**Rating:** The output seemed to infer from few shots that the rating were on 5 scale, and most products were rated 5(7), and few are 4(3).

**Title:** Unlike the previous case, the product title this time is the name of the supplement - which is relevant to the product review.

**Text:** Most reviews are one sentence. The reviews are in an easy to understand language, and the sentiment is positive.

**Asin:** Asin follows the structure from the original data, and is consistent across all enteries. However, some products share the same Asin id, even though they are different.

**Parent_Asin:** Similar to Asin, these are also similar to one in the original dataset.

**User_ID:** The length of user_id is consistent, but there are multiple same user_id enteries(only two distinct user_ids are there). 

**Timestamp:** The timestamps are valid, and the date are different. Years range from 2009 to 2015.

**Helpful_vote:** Most reviews have 0 helpful votes, and some have 1 helpful votes.

**Time:** The timestamp and time entries are consistent with each other. The time is nearly same as of original data(00:37, 19:15, 03:11) used to prompt the model.

3. Llama 3.2 :
**Note:** Even after prompting the model to only give the CSV enteries, it started the output as "Here are 10 synthetic example...". Other than that, the first entry is not a valid CSV entry, as the delimmeter "." is used instead of ","(however, none of them should have been there)  

**Rating:** The output could not infer from few shots that the rating were on 5 scale, and rated from 1-10(serially). 

**Title:** The title are mostly one word, and is the name of the supplement.

**Text:** Reviews are one sentence(compound), and to the point. The choice of words is complex as compared to the base case. 

**Asin:** Asin are distinct for all enteries, and the length is consistent with the original dataset.

**Parent_Asin:** Similar to Asin, these are also same as that of Asin.

**User_ID:** The length of user_id is consistent, with some repitition.

**Timestamp:** The timestamps are valid, and the date are different(Years range from 2018 to 2021).

**Helpful_vote:** All reviews have 1 helpful vote.

**Time:** The timestamp and time entries are inconsistent with each other. Most time enteries are distinct from the  few shot examples we used.

### Text Length Prompt Analysis

1. Cohere Command R+:
**Rating:** The output seemed to infer from few shots that the rating were on 5 scale. Half of the enteries were rated 4(5), and half 5(5). 

**Title:** The title is relevant to the product review, with easy to understand language. The title encompassses a good summary of the review.

**Text:** Some reviews are more than one sentence long, and relatively more complex than the base case. The tone of the reviews was converstational. The sentiment of the review is positive.

**Asin:** Asin follows the structure from the original data, and is consistent across all enteries. All of them are distinct for all enteries.

**Parent_Asin:** Similar to Asin, these are also similar to one in the original dataset(all are same as Asin).

**User_ID:** The length of user_id is consistent with the original dataset, and is of generic nature such as "A123456789EXAMPLE" or "A4444444444EXAMPLE".

**Timestamp:** The timestamps are valid, and there is not too much discrepancy in year, month and day. Years range from 2013-2022.

**Helpful_vote:** Reviews have helpful vote ranging from 0-2.

**Time:** The timestamp and time entries are consistent with each other. The times are random, and unlike the few-shot examples we used to prompt the model.

2. Qwen 1.5B :
**Note:** The model wa unclear in understanding that the output was expected in csv format, and it gave it in markdown table format. Also, even after telling the model to give only the CSV enteries, it started the answer with "Here are 10 additional rows..." . The "Data" column is also absent from the output generated.

**Rating:** The output seemed to infer from few shots that the rating were on 5 scale, and most products were rated 5(7), and few are 4(2). There were only 9 enteries, not 10.

**Title:** The product title is the name of the supplement - which is relevant to the product review, apart from the first entry which is titled "Great Product".

**Text:** Interestingly, apart from the first entry, which seems like a review, all other enteries basically explain what the supplement does - which is not something a review does.

**Asin:** All of the Asin id are same for all enteries(except the second entry).

**Parent_Asin:** Except the second entry, all Parent Asin ID are same.

**User_ID:** The length of user_id is consistent, but there are multiple same user_id enteries(apart from the second entry, all user_id are same). 

**Timestamp:** The timestamps are valid, and the date are different. The synthetic data only gave entry from the year 2015.

**Helpful_vote:** All enteries have 0 useful votes.

**Time:** Apart from the first and second entry(which also share the same timestamp(2015-01-04 03:11:26) ), all other enteries have the same timestamp(2015-09-27 19:15:33). 

3. Llama 3.2 :
**Note:** Even after prompting the model to only give the CSV enteries, it started the output as "Here are 10 synthetic example...". Other than that, 

**Rating:** The output infered that the rating were on 5 scale, and ratings it gave were 3(2), 4(4), 5(4). 

**Title:** The title are mostly one word, and is the name of the supplement.

**Text:** Reviews are one sentence, and have maximum of 4-5 words. The sentiment is neutral.

**Asin:** 4 pair of entries have the same Asin id, with only two being distinct. The length is consistent.

**Parent_Asin:** Similar to Asin column, these are also same as that of Asin.

**User_ID:** There are 4 distinct user_id in the data generated.

**Timestamp:** The timestamps are valid, and apart from the first and third entry(which have the year 2015), all other enteries have the year 2009. 

**Helpful_vote:** All reviews have 1 helpful vote.

**Time:** The timestamp and time entries are consistent with each other. Most time enteries are distinct from the  few shot examples we used.

## Questions
(Will add more questions as the project cycle continues)

1. **Concept/Category Drift:** Without any additional context, can the LM understand what product category we are talking about, and whether or not it sticks to it.

Ans. In my initial experiments, this was not the case. Many a times, the  model could not infer what exactly the reviews were about, so I explicitly chose to mention the category in the prompt.

2. **Accuracy num responses:** Given in the prompt how to many CSV enteries to generate, does the model generates the specified number of enteries?

Ans. Most of the time, it was the case. Qwen 1.5B however sometimes drifted away from this(mostly off by 1/2).

## Challenges Encountered

- Adjusting, and then using the correct prompt was really the difficult part. For testing, I tried with Cohere LLM, but then tested on all three versions of the models.

- Working with local models was really slow, and it was the bottleneck for slow iteration speed.

- Understanding the question and designing the experiment accordingly took a long time, but I focused on TDD, so the original idea went through many iterations.

### Result
Even though all models in some scenario gave inconsistent synthetic data ; could be due to many factors(such as temperature setting, random seed or other inference adjustable parameters), it is difficult to say which of the three strategies should be used to generate synthetic data. More experiments should be performed to give any conclusive results, but from this we can understand the tradeoffs and shortcomings of three different classes of models. A hybrid approach seems to be a good strategy to deploy moving forward.

Syngen is a work in progress, and will always accept contributions.

## Resources

1. [Synthetic Data Generation, OpenAI Cookbook](https://cookbook.openai.com/examples/sdg1)

2. [Cosmopedia Blog](https://huggingface.co/blog/cosmopedia)


### TODOs

- [X] Make at least the thing work with llama3.2 (using ollama)
- [X] work with the HF integration.
- [X] test different models(instruct from HF).
- [X] What metrics we are going to look at, and how to present it well.
- [X] Prompts for different metrics.
- [X] CLI support, Secrets are not injected into the script.
- [X] Documentation and comments.
- [X] Webapp. 
- [X] metrics testing/analysis(Completed).