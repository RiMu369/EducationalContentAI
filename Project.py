from boltiotai import openai
import os
from flask import Flask, render_template_string, request

openai.api_key = os.environ['OPENAI_API_KEY']

def generate_tutorial(course):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": "You are a helpful assistant that creates educational content"
            }, {
                "role": "user",
                "content": f"Give the objectives, sample syllabus, details of 3 measureable outcomes (Knowledge, Comprehension, Application), Assessment Methods, and recommended readings for a course titled: {course}. The output should be in markdown format, and according to the following template: \n# Course Title: \n\n## Objectives: \n\n## Sample Syllabus: \n\n## Measureable Outcomes: \n\n## Assessment Methods: \n\n##Recommeded readings: \n. The output should align with Bloom's Taxonomy levels."
            }])
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error during OpenAI API call: {e}")
        return "Error generating content. Please try again."


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello():
    output = ""
    if request.method == 'POST':
        course = request.form['course']
        output = generate_tutorial(course)
    return render_template_string('''

<!DOCTYPE html>
<html>
    <head>
        <title>Infinite Project Generator</title>
        <link
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css"
          rel="stylesheet"
        />
	<style>
	  .btn-primary:active, .btn-secondary:active{
  		background-color: #3e8e41;
		box-shadow: 0px 2px #666;
  		transform: translateY(2px);
	  }
	  .btn-primary, .btn-secondary {
	    padding: 5px 10px;
	    text-align: center;
	    cursor: pointer;
	    outline: none;
	    color: #fff;
  	    background-color: #04AA6D;
	    border: none;
	    border-radius: 15px;
	    box-shadow: 0px 4px #999;
	  }
	</style>
    <script>
      async function generateTutorial() {
        const course = document.querySelector("#course").value;
        const gen = document.querySelector("#gen");
        gen.style.display = "block";
        const response = await fetch("/generate", {
         method: "POST",
         body: new FormData(document.querySelector("#tutorial-form")),
        });
        const newOutput = await response.text();
        output.textContent = newOutput;
        gen.style.display = "none";
      }
      function copyToClipboard() {
        const output = document.querySelector("#output");
        const textarea = document.createElement("textarea");
        textarea.value = output.textContent;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand("copy");
        document.body.removeChild(textarea);
        alert("Copied to clipboard");
      }
    </script>
    </head>
    <body>
        <div class="container">
          <h1 class="my-4" style="color:#007BFF;">EduGenie: AI-Powered Educational Content Creator</h1>
          <form
            id="tutorial-form"
            onsubmit="event.preventDefault(); generateTutorial();"
            class="mb-3"
          >
            <div class="mb-3">
              <label for="course" class="form-label">
		Course Title:
	      </label>
              <input
                type="text"
                class="form-control"
                id="course"
                name="course"
                placeholder="Enter the course title"
                required
              />
            </div>
            <button type="submit" class="btn-primary" style = "background-color:black;border: solid 2px #363636;">
              Generate Content  
            </button>
          </form>
	  <div id="gen" style="display:none">
		Generating content, please wait...
	  </div><br>
          <div class="card">
            <div
              class="card-header d-flex justify-content-between align-items-center"
	      style = "background-color:#007BFF;color:white;"
            >
              Output:
              <button class="btn-secondary" onclick="copyToClipboard()">
                Copy
              </button>
            </div>
            <div class="card-body">
              <pre id="output" class="mb-0" style="white-space: pre-wrap; color:black;">
              {{ output }}
              </pre>
            </div>
          </div>
	  <br>
	  <div class="Data_privacy" style="background-color:#CFF4FC;color:#00738D;border:solid 2px #B8F0FA;border-radius:7px;padding:10px;">
	    Data Privacy Notice: Your input data is used only to generate educational content and is not stored or logged
	  </div>
        </div>
    </body>
</html>
''',
        output=output)


@app.route('/generate', methods=['POST'])
def generate():
    course = request.form['course']
    return generate_tutorial(course)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)