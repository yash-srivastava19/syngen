import io
import os
import streamlit as st
from dotenv import load_dotenv
from transformers import pipeline

load_dotenv()

## Generate an app where we can generate synthetic dataset based on CSV data. Ability to adjust parameters for adjusting dialogue length, topic, diversity, and language m=complexity should also be there.
st.title("Synthetic Data Generation App")
st.write("This app generates synthetic data based on CSV data. You can adjust parameters for dialogue length, topic, diversity, and language complexity.")

st.write("Upload a CSV file to get started.")
uploaded_file = st.file_uploader("Choose a file")

# Options to steer data generated(how do we use these params?)
topic = st.text_input("Topic", "Health Supplements")

# Options to tweak the synthetic data generated
num_options = st.slider("Number of synthetic data entries to generate", 1, 10, 5)

# Select for the type of prompt to use
prompt_type = st.selectbox("Select Prompt Type", ["Base", "Diversity", "Language Complexity", "Text Length"])



if uploaded_file is not None:
    # If the file is not noe, we sample randomly 3 enteries from the dataset(including the header), and make a custom prompt
    import pandas as pd
    df = pd.read_csv(uploaded_file)
    with open("text_review.txt", "w") as f:
        for i in range(3):
            print(df.iloc[i], file=f, sep = ",")
    
    ## Read from any three random enteries from the dataset, and then create a subset of the dataset in the prompt_base
    if prompt_type == "Text Length":
        prompt = f"""
        I have the following CSV data for health supplements:
        
        {df.iloc[0]}
        {df.iloc[1]}
        {df.iloc[2]}
    
        I would like you to generate {num_options} more examples of synthetic data with a dialouge length similar to the example given.Give only the CSV entries(with column names as well), nothing else.

        """
    elif prompt_type == "Diversity":
        prompt = f"""
        I have the following CSV data for health supplements:
        
        {df.iloc[0]}
        {df.iloc[1]}
        {df.iloc[2]}
        
        I would like you to generate {num_options} more examples of synthetic data with a high level of diversity.Give only the CSV entries(with column names as well), nothing else.
        
        """
    elif prompt_type == "Language Complexity":
        prompt = f"""
        I have the following CSV data for health supplements:

        {df.iloc[0]}
        {df.iloc[1]}
        {df.iloc[2]}

        I would like you to generate {num_options} more examples of synthetic data with a high level of language complexity.Give only the CSV entries(with column names as well), nothing else.

        """
    elif prompt_type == "Base":
        prompt = f"""
        I have the following CSV data for health supplements:
        
        {df.iloc[0]}
        {df.iloc[1]}
        {df.iloc[2]}
    
        I would like you to generate {num_options} more examples of synthetic data based on this input. Give only the CSV entries(with column names as well), nothing else.
        
        """
    else:
        st.write("Please select a prompt type to proceed.")

    
    ## Now, we can generate synthetic data based on the prompt_base, give user the ability to select the model.
    model = st.selectbox("Select Model", ["Cohere", "Qwen2.5-1.5B-Instruct", "Llama3.2"])
    if model == "Cohere":
        import cohere
        co = cohere.ClientV2(os.environ["COHERE_API_KEY"])
        response = co.chat(
            model="command-r-plus",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        import io 
        # Debug: print(response.message.content[0].text)
        with st.spinner("Generating synthetic data..."):
            try:
                df = pd.read_csv(io.StringIO(response.message.content[0].text), sep=",")
                st.write(df)
            except Exception as e:
                st.write(response.message.content[0].text)

    elif model == "Qwen2.5-1.5B-Instruct":
        generator = pipeline('text-generation', model='Qwen/Qwen2.5-1.5B-Instruct')
        response = generator(prompt, max_new_tokens=700)
        
        # Debug: print(response[0]['generated_text'])
        with st.spinner("Generating synthetic data..."):
            try:
                df = pd.read_csv(io.StringIO(response[0]['generated_text']), sep=",")
                st.write(df)
            except Exception as e:
                st.write(response[0]['generated_text'])

    
    elif model == "Llama3.2":
        import ollama
        response = ollama.chat(model='llama3.2', messages=[
          {
            'role': 'user',
            'content': prompt,
          },
        ])

        # Debug: print(response['message']['content'])
        with st.spinner("Generating synthetic data..."):
            try:
                df = pd.read_csv(io.StringIO(response['message']['content']), sep=",")
                st.write(df)
            except Exception as e:
                st.write(response['message']['content'])

    else:
        st.write("Please select a model to proceed.")
else:
    st.write("Please upload a file to proceed.")