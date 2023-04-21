import openai
import random

# Set up the OpenAI API credentials
openai.api_key = "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"

all_tones = ["persuasive", "excited", "informative", "authoritative", "urgent"]

# Function to generate advertisement prompts
def generate_advertisement(product_service_name, keywords, tone, length="medium", organization_name=None):
    # Select two random tones from the list
    random_tones_1 = random.sample(all_tones, 2)
    random_tones_3 = random.sample(all_tones, 2)

    prompt1_tones = random_tones_1
    prompt3_tones = random_tones_3
    prompt_tones = [prompt1_tones, tone, prompt3_tones]

    model = "text-davinci-002"
    temperature = 0.5

    if length == "short":
        max_tokens = 240
    elif length == "long":
        max_tokens = 720
    else:
        max_tokens = 480

    prompts = []
    for tone in prompt_tones:
        # Set the parameters for the OpenAI API call
        prompt = f"Generate an advertisement prompt for {product_service_name}. Keywords to include are {', '.join(keywords[:20])}. The tone should be {', '.join(tone[:5])}. The length should be {length if length else 'medium'}."
        if organization_name:
            prompt += f" This advertisement is for {organization_name}."

        # Call the OpenAI API to generate the advertisement prompts
        response = openai.Completion.create(  
            engine=model,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Extract the generated prompts from the response
        prompt_choices = [choice.text.strip() for choice in response.choices]
        prompts.append(prompt_choices)

    return prompts




