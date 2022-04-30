from google.cloud import texttospeech
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io
import os

credential_path = r"C:\Users\Cspes\Downloads\Service-file.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

path = "Book"
if not os.path.exists(path):
    os.makedirs(path)

fp = open('Happiness.pdf', 'rb')
r_manager = PDFResourceManager()
r_string = io.StringIO()
converter = TextConverter(r_manager, r_string, laparams=LAParams())
interpreter = PDFPageInterpreter(r_manager, converter)
# Looping through pages and converting text to audio
page_num = 0
for pageNumber, page in enumerate(PDFPage.get_pages(fp)):
    if pageNumber == page_num:
        interpreter.process_page(page)
        data = r_string.getvalue()
        # Text to Speech Client
        client = texttospeech.TextToSpeechClient()
        synthesis_input = texttospeech.SynthesisInput(text=data)
        voice = texttospeech.VoiceSelectionParams(language_code="en-US",
                                                  ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
                                                  )
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        response = client.synthesize_speech(input=synthesis_input,
                                            voice=voice,
                                            audio_config=audio_config
                                            )
        with open(os.path.join(path, f'pdf page {page_num}.mp3'), 'wb') as file:
            file.write(response.audio_content)
        data = ''
        r_string.truncate(0)
        r_string.seek(0)
    page_num += 1
