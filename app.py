from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from deepgram import Deepgram
import asyncio
import re


app = Flask(__name__)

# Your OpenAI and Deepgram API keys should be set as environment variables
# It is not safe to hardcode them in your source code
client=OpenAI(api_key="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")
DEEPGRAM_API_KEY = '60acc7ddc93281435ea12246d71e5278c7cca930'
dg_client = Deepgram(DEEPGRAM_API_KEY)

@app.route('/security')
def security():
    return render_template('security.html')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/')
def index():
    # A simple form to upload an audio file
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>ChronoLingua</title>
        <link rel="icon" href="/static/css/images/ICON.png">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

        <style>
            .align-with-form {
                display: flex;
                align-items: center;
                justify-content: space-around;
            }
            body, html {
                height: 100%; /* full height of the viewport */
                margin: 0;
                display: flex; /* enables flexbox */
                flex-direction: column; /* stack children vertically */
                justify-content: space-between; /* push header and footer to the ends */
                background-color: #f5f5f5;
                background-image: url('/static/css/images/background.png');
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
                background-position: center;
            }


            .form-container {
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100%;
            }
            .form-box {
                width: 100%; /* Or your preferred width */
                padding: 2em;
                background: #333;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                margin: auto;
                color: #fff; /* Ensure text is white if needed */
            }

            .title {
                margin-bottom: 0.4rem;
                font-family: 'Montserrat', sans-serif;
                font-weight: 700;
                color: #A020F0;
            }
            .subtitle {
                color: #FFFFFF;
            }
            .circle {
                width: 330px;
                height: 330px;
                background-color: transparent; /* Make background transparent */
                border: 2px solid white; /* White border, adjust thickness as needed */
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                color: white;
            }
            .file {
                display: flex;
                align-items: center;
                width: 100%;
            }

            .file-cta {
                line-height: normal; /* Reset line-height to default to match button height */
                padding: 10px 16px;

            }

            .file-name {
                display: inline-block;
                vertical-align: middle;
                margin-right: 10px; /* If you want space to the right */
                border: 1px solid #ccc; /* Add a border */
                border-radius: 4px; /* Optional: rounded corners */
                padding: 0.5em 1em; /* Add padding inside the 'No file uploaded' box */
                min-width: 200px; /* Set a minimum width */
                text-align: center; /* Center the text inside the box */
            }

            .button {
                width: calc(100% - 10px); /* Adjust width to account for margin */
                cursor: pointer;
                margin-top: 1em; /* Space above the button */
                margin-bottom: 1em; /* Space below the button */
                /* If you want horizontal spacing between side-by-side buttons */
                margin-right: 5px; /* Space to the right of the button */
                margin-left: 5px; /* Space to the left of the button */
            }
            .navbar {
                background-color: transparent !important; /* Make navbar transparent */
                border: none;
                box-shadow: none;
            }
            .navbar-item{
                color: #A020F0;
            }
            .navbar-link{
                color: #A020F0;
            }
            #progressBar {
                display: none;
            }
            .main-content {
                flex: 1; /* grows to fill available space */
                /* Other styles as necessary */
            }
            .footer {
                background-color: transparent;
                color: #fff; /* Adjust the text color as needed */
                /* ...other styles... */
            }
            .footertext {
                color: #A020F0;
            } 

            /* General styling for all icons */
            .fa {
                color: white;            /* Sets icon color to white */
                background-color: blue;  /* Sets background color to blue */
                padding: 20px;           /* Adds padding around the icon */
                border-radius: 100%;      /* Makes the background circular */
                text-align: center;      /* Centers the icon within the background */
                text-decoration: none;   /* Removes underline from the icon links */
            }

            /* Specific styling for Facebook icon */
            .fa-facebook {
                background-color: #3b5998; /* Facebook's brand color for background */
            }

            /* Specific styling for Twitter icon */
            .fa-twitter {
                background-color: #1DA1F2; /* Twitter's brand color for background */
            }
            .fa-instagram {
                background-color: #d62976
            }

            
        </style>
    </head>
    <body>
    <div class="main-content">

        <nav class="navbar" role="navigation" aria-label="main navigation">
        <div class="navbar-brand">
            <a class="navbar-item" href="/">
            <img src="/static/css/images/ICON.png" width="30" height="30">
            </a>

            <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
            </a>
        </div>

        <div id="navbarBasicExample" class="navbar-menu">

            <a class="navbar-item" href="https://forms.gle/YBL75rAdt4M3bj1E8 ">
                Feedback
            </a>

            <a class="navbar-item" href="/security">
                Security
            </a>

            <div class="navbar-end">
            <div class="navbar-item">
            </div>
            </div>
        </div>
        </nav>

            <section class="section">
                <div class="container">
                    <h1 class="title">ChronoLingua</h1>
                    <p class="subtitle">Artificial Intelligent Stuttering Detection</p>
                </div>
            </section>
            <div class="align-with-form">
                <div class="circle">
                    ChronoLingua uses Artificial Intelligence to analyze spoken language, offering insights for speech therapists and actors. It detects stutters, provides feedback, and aids in refining verbal communication.
                </div>
                
                <div class="form-container">
                    <div class="form-box">
                        <h1 class="title has-text-centered">Upload new Audio File</h1>
                        <form action="/upload" method="POST" enctype="multipart/form-data">
                            <label class="file-label">
                                <input class="file-input" type="file" name="audio_file">
                                <span class="file-cta">
                                    <span class="file-icon">
                                        <i class="fas fa-upload"></i>
                                    </span>
                                    <span class="file-label">
                                        Choose a file…
                                    </span>
                                </span>
                                <span class="file-name">
                                    No file uploaded
                                </span>
                            </label>
                            <button id="submitButton" class="button is-light" type="submit">Submit</button>
                            <progress id="progressBar" class="progress is-medium is-dark" max="100">45%</progress>

                        </form>
                    </div>
                </div>
            </div>
            </div>
        </body>
        <footer class="footer">
        <div class="content has-text-centered">
            <p class = "footertext">
            <strong>ChronoLingua</strong> by Diego Gonzalez <a href="mailto:diego.gaf28@gmail.com">(email)</a>. Contact support for problems: 
            <a href="mailto:chronolingua@gmail.com">(email). <br> </a>
            </p>
            <a href="https://www.facebook.com/chronolingua" class="fa fa-facebook"></a>
            <a href="https://www.x.com/chronolingua" class="fa fa-twitter"></a>
            <a href="https://www.instagram.com/chronolingua/" class="fa fa-instagram"></a>

        </div>
        </footer>

        <script>

            document.getElementById('submitButton').addEventListener('click', function() {
            document.getElementById('progressBar').style.display = 'block';
            });

            const fileInput = document.querySelector('.file-input');
            const fileLabel = document.querySelector('.file-name');
            const form = document.querySelector('form');

            fileInput.addEventListener('change', function() {
                const fileName = fileInput.files.length > 0 
                    ? fileInput.files[0].name 
                    : 'No file uploaded';
                fileLabel.textContent = fileName;
                form.submit();
            });
        </script>
    </html>


'''



@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No audio file part'}), 400

    file = request.files['audio_file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        audio_data = file.read()
        source = {'buffer': audio_data, 'mimetype': 'audio/wav'}
        options = {"punctuate": True, "utterances": True}

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            response = loop.run_until_complete(dg_client.transcription.prerecorded(source, options))
            all_word_details = extract_word_details(response)
            formatted_details = format_word_details_for_gpt(all_word_details)
            
            # Interact with ChatGPT for analysis of detected blocks
            chatgpt_response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Analyze the provided transcript to identify the top five instances of blockage stutters."},
                        {"role": "user", "content": formatted_details},
                        {"role": "user", "content": "Context: I am providing you with a transcript of an audio file. The transcript includes each word spoken, its starting and ending times, and the confidence scores of these words being correctly identified."},
                        {"role": "user", "content": "Your Goal: Your task is to analyze the transcript and identify the top five words that are most likely to be blockage stutters."},
                        {"role": "user", "content": "Timing Analysis: Focus on the timing between the starting time of the word and the ending time of the word before the word being analyzed. Look for unusually long pauses that don't align with normal speech patterns or the context of the conversation."},
                        {"role": "user", "content": "Confidence Scores: Consider the confidence scores of each word. A low-confidence word followed by an unusually long pause may indicate a stutter."},
                        {"role": "user", "content": "Providing Results: For each identified blockage stutter, provide the following: The word. Its starting and ending times. The confidence score. A brief explanation of why this word was identified as a stutter (focusing on the timing gap and context)."},
                        {"role": "user", "content": "Contextual Sensitivity: Be mindful of the overall context of the speech. Not all pauses are stutters - some may be natural pauses for breath or punctuation. Report Format: List your findings in a clear, organized manner."}
                ],
                temperature = 0.0
            )
            
            chatgpt_text_response = chatgpt_response.choices[0].message.content

            # Split the response by number followed by a period and space to get each item
            response_items = re.split(r'(\d+\.) ', chatgpt_text_response)[1:]  # Ignore the first empty split
            response_items = [f'{num} {text.strip()}' for num, text in zip(response_items[0::2], response_items[1::2])]

            gpt_response_word_analysis = client.chat.completions.create(
                    model="gpt-4",  
                    messages=[
                        {"role": "system", "content": "You are analyzing words for pronunciation challenges specific to native English speakers who stutter, particularly due to vocal cord stress from certain letters or letter combinations."},
                        {"role": "user", "content": chatgpt_text_response},
                        {"role": "user", "content": "From the previous response, identify words that might pose pronunciation challenges for native English speakers who stutter. We are specifically looking for words that have letters or letter combinations that could be stressful on the vocal cords. Do not focus on non-native speaker challenges; our emphasis is on stuttering and vocal cord stress."}
                    ],
                    temperature = 0.0
                )

            analysis_text = gpt_response_word_analysis.choices[0].message.content
            formatted_analysis = f'<p>{analysis_text}</p>'


            # Wrap each item in paragraph tags
            formatted_response = ''.join([f'<p>{item}</p>' for item in response_items])
            combined_content = formatted_response + formatted_analysis
            html_content = f'<html><body>{combined_content}</body></html>'


            full_html_response = f'''
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
                <link rel="icon" href="/static/css/images/ICON.png">
            </head>
            <body>
                <div class="tile is-ancestor">
                    <div class="tile is-4 is-vertical is-parent">
                        <div class="tile is-child box">
                        <p class="title">ChronoLingua</p>
                        <p>Our AI detected a few blockage-type stutters and have given analysis based on your individual difficulty with the word's pronunciation </p>
                        </div>
                        <div class="tile is-child box">
                        <p class="title">Pronunciation</p>
                        {formatted_analysis}
                        </div>
                    </div>
                    <div class="tile is-parent">
                        <div class="tile is-child box">
                        <p class="title">Blockage Stutters</p>
                        {formatted_response}
                        </div>
                    </div>
            </div>
                <!-- Additional scripts or content here -->
            <div class="tile">
                <a href="/" class="button is-light">
                    Back to Home
                </a>
            </div>
            </body>
            </html>
            '''

            return full_html_response
            
            # Return the response from ChatGPT
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            loop.close()

    return jsonify({'error': 'File type not allowed'}), 400

def allowed_file(filename):
    # This function checks for allowed file extensions
    ALLOWED_EXTENSIONS = {'wav', 'mp3'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_word_details(response):
    # Assuming 'response' is the JSON response from Deepgram
    # Adapt this function based on the actual response structure from Deepgram
    all_word_details = []
    for utterance in response['results']['utterances']:
        for word in utterance['words']:
            all_word_details.append({
                "word": word['word'],
                "start": word['start'],
                "end": word['end'],
                "confidence": word.get('confidence', 0)
            })
    return all_word_details

def format_word_details_for_gpt(all_word_details):
    formatted_details = [
        f"{detail['word']}({detail['start']}s-{detail['end']}s, confidence: {detail.get('confidence', 'N/A')})"
        for detail in all_word_details
    ]
    return ', '.join(formatted_details)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
