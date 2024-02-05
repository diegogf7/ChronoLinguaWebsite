import request
from openai import OpenAI
from deepgram import Deepgram
import asyncio
import re


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
