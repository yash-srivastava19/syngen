# SynGen - Synthetic Data Generation
In the world of AI, data is moat. Unfortunately, finding enough high-quality data for downstream machine learning tasks(especially for problems where data scarcity is a big issue)can be a huge pain. That's what syngen tries to solve. I've tested synthetic data generation of a variety of models and for a variety of prompts. There are tweaks you can do to the complexity, variety, and length of real data, giving you a fine control over the data you want. Syngen also comes up with both a webapp and a cli tool, so use as you please.

## Models and Architecture Tested
3 classes of models were tested, Ollama(Llama3.2), HF(maybe some GPT2 style small model, or phi/Qwen), and commercially avaialble models(Cohere)

3 classes of prompts are testsed, these include prompts for diversity, language complexity, and text length. There is also a base prompt to compare against.

## Problem
Syngen, as the name suggests, generates synthetic data based on existing data. The synthetic data extends the existing data, and tries to adheres to the properties of it.

For the purpose of this project, we'll work with a "supplements" subset of Amazon reviews [dataset](https://amazon-reviews-2023.github.io/main.html), and try to augment the data.  

## What factors we considered?
Using Language Models to augment the dataset gives us fine control over the type to data we can generate - we can just prompt the LM to give exactly what kind of data we need for our use case. For the purpose of this study, we are going to test on three factos, namely - language complexity, divevrsity, and length. Let's try to understand what each of these factor imply

- **Language Complexity:** Language complexity, although difficult to define, basically refers how easily the comprehension of the sentence is. Given the real-world dataset, does the augmented data is similar in terms of language complexity?  

- **Language Diversity:** Language Diversity refers to the different ways in which the same sentence can be communicated. For our use case, we study does the augmented data is similar in terms of language diversity?

- **Text Length:** Most users when writing a review, prefer not to write too much, does LMs do that too, or they end up writing really long reviews - which can raise suspicion on the authenticity of the review.

## Assumptions

- For HF models, I are sticking our analysis to models which are around 1B parameters, I don't have the bandwidth to test larger models, so I chose smaller models.

- For commercial LLMS, I chose Cohere models cause their free tier works for my use case, and the command-r-plus model is actually really good.

- To test with completely local model, I chose Llama3.2, accessed by Ollama.

## Metrics
1. **Concept/Category Drift:** Without any additional context, can the LM understand what product category we are talking about, and whether or not it sticks to it.

2. **Accuracy num responses:** Given in the prompt how to many CSV enteries to generate, does the model generates the specified number of enteries?

3. **Similarity to Original Dataset:** How similar the generated synthetic data is to original dataset. Are there any discrepancies?

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


## Additional Caveats

- Adjusting the prompt was really the difficult part. For testing, I tried with Cohere LLM, but then tested on all three versions of the models.

## Challenges Encountered.

- Will update later.

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
- [] metrics testing/analysis.
- [] understand why things work that way, efficacies if you will.