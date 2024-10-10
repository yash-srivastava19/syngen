# SynGen - Synthetic Data Generation
Data scarcity is a big issue, syngen tries to solve it. Generate synthetic data, with similar language complexity, diversity, and length.

## Models and Architecture Tested
3 classes of models were tested, Ollama(Llama3.2), HF(maybe some GPT2 style small model, or phi/Qwen), and commercially avaialble models(Cohere)

## Problem
For starters, we will try to generate sythetic reviews. There are 3 prompts based on the three things we mentioned.

## What factors we considered?
Let's see. Will update later.

- For HF models, we are sticking our analysis to models which are around 1B parameters, so that our implementation doesn't take too much space. This also gives an idea on sigal/noise ratio for small models.


## Metrics
1. **Concept/Category Drift:** Without any additional context, can the LM understand what product category we are talking about, and whether or not it sticks to it.

2. **Accuracy num responses:** Given in the prompt how to many CSV enteries to generate, does the model generates the specified number of enteries?

3. **Similarity to Original Dataset:** How similar the generated synthetic data is to original dataset. Are there any discrepancies?

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
- [] metrics testing.
- [] understand why things work that way, efficacies if you will.