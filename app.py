import streamlit as st

## Generate an app where we can generate synthetic dataset based on CSV data. Ability to adjust parameters for adjusting dialogue length, topic, diversity, and language m=complexity should also be there.
st.title("Synthetic Data Generation App")
st.write("This app generates synthetic data based on CSV data. You can adjust parameters for dialogue length, topic, diversity, and language complexity.")

st.write("Upload a CSV file to get started.")
uploaded_file = st.file_uploader("Choose a file")

# Options to steer data generated(how do we use these params?)
num_options = st.slider("Number of synthetic data entries to generate", 1, 10, 5)
dialogue_length = st.slider("Dialogue Length", 50, 500, 100)
topic = st.text_input("Topic", "Health Supplements")
diversity = st.slider("Diversity", 0, 1, 0.5)
language_complexity = st.slider("Language Complexity", 0, 1, 0.5)


if uploaded_file is not None:
    # If the file is not noe, we sample randomly 3 enteries from the dataset(including the header), and make a custom prompt
    import pandas as pd
    df = pd.read_csv(uploaded_file)
    with open("text_review.txt", "w") as f:
        for i in range(3):
            print(df.iloc[i], file=f, sep = ",")
    
    ## Read from any three random enteries from the dataset, and then create a subset of the dataset in the prompt_base

    prompt_base = f"""
    I have the following CSV data: 
    {df.iloc[0]}
    {df.iloc[1]}
    {df.iloc[2]}
    Generate a synthetic dataset based on this input. Produce me {num_options} more examples of the data formatted for CSV to augment dataset. Give only the CSV entries.
    """

    ## Now, we can generate synthetic data based on the prompt_base, give user the ability to select the model.
    model = st.selectbox("Select Model", ["Cohere", "Microsoft Phi-3.5-mini-instruct", "Llama3.2"])
    if model == "Cohere":
        import cohere
        co = cohere.ClientV2("5mG9Baoklq9rOXkTSpTvXZ5J6XG4RMGWTHM7p2sp")
        response = co.chat(
            model="command-r-plus",
            messages=[
                {
                    "role": "user",
                    "content": prompt_base
                }
            ]
        )
        st.write(response.message.content[0].text)
    elif model == "Microsoft Phi-3.5-mini-instruct":
        from transformers import pipeline
        generator = pipeline('text-generation', model='microsoft/Phi-3.5-mini-instruct')
        response = generator(prompt_base, max_new_tokens=dialogue_length)
        st.write(response[0]['generated_text'])
    elif model == "Llama3.2":
        import ollama
        response = ollama.chat(model='llama3.2', messages=[
          {
            'role': 'user',
            'content': prompt_base,
          },
        ])
        st.write(response['message']['content'])
    else:
        st.write("Please select a model to proceed.")
else:
    st.write("Please upload a file to proceed.")

