from flask import Flask, render_template, request
from prompt_generator import generate_advertisement

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        product_name = request.form["product"]
        organization_name = request.form["organization"]
        keywords = request.form["keywords"]

        tones = ["exciting", "informative", "persuasive"]

        prompts = generate_advertisement(product_name, keywords, tones, length="medium", organization_name=organization_name)

        prompts = [i for j in prompts for i in j]

        inputs = [prompts[0], prompts[1], prompts[2]]

        return render_template("index.html", inputs=enumerate(inputs))
    else:
        return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    selected_input = request.form["selected_input"]
    print("Selected input:", selected_input)

    file = open("response.txt", "a")
    file.write(str(selected_input) + ",")
    file.close()

    # Add selected input to list
    return "Selected input: " + str(selected_input)

if __name__ == "__main__":
    app.run(debug=True)