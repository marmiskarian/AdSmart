# AdSmart
*Spice up your ads with smart and creative prompts from AdSmart.*

AdSmart is a powerful tool that generates advertisement prompts based on the keywords you provide. With AdSmart, you can easily create targeted and effective advertisements that will help you reach your audience. Whether you need a slogan for your product, a headline for your blog post, or a tagline for your social media campaign, AdSmart can help you find the best words to attract your audience.


## How it works
AdSmart takes as an input your `product/service information`, a list of `keywords` that describe your product or service, additionally, specific information such as the `tone` and `length` of the prompts. Our advanced algorithm based on the `Chat GPT python API` will generate a list of advertisement prompts for you to choose from. You can explore one of the prompts and get a new list of options. Finally, you can select the one that best fits your needs, do your own customization (editing) and and start advertising smarter with AdSmart.


## How to use it
To use AdSmart, you need to install the required dependencies and run the main script. You can also use the web interface to interact with the project.


### *Installation*
To install AdSmart, clone this repository and run the following command:

```
pip install -r requirements.txt
```


### *Running the script*
To run the main script, use the following command:
```
python adsmart.py --keywords KEYWORDS --tone TONE --length LENGTH
```
where KEYWORDS is a comma-separated list of keywords that describe your product or service, TONE is one of the following options: positive, negative, neutral, funny, serious, formal, informal, and LENGTH is an integer that specifies the maximum number of words for each prompt.


### *Web interface*
You can also use the web interface to generate advertisement prompts. To launch the web interface, run the following command:
```
streamlit run app.py
```
Then open your browser and go to http://localhost:????. You will see a form where you can enter your keywords and other parameters. After clicking the generate button, you will see a list of advertisement prompts.

How is the website going to look like? Rough mockup of the website: [link](https://zaruhipoghosyan01.wixsite.com/adsmart)

The input page can be found in the `General` section that can be found on the right corner of the `Home` introductory page.


## Project Information
This project was done by students from the American University of Armenia (AUA), and the project owners are Maria Miskaryan, Hrayr Muradyan, Narine Marutyan and Zaruhi Poghosyan.

ClickUp: [link](https://app.clickup.com/9007102928/v/li/900701227902)

© 2023 by AdSmart. This project is open source and free for personal and educational use. If you want to use this project for commercial purposes, please contact the project owners for permission.