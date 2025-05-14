from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os

def initialize_speech_to_text(api_key, service_url):
    """Initialize IBM Watson Speech to Text service."""
    authenticator = IAMAuthenticator(api_key)
    stt_service = SpeechToTextV1(authenticator=authenticator)
    stt_service.set_service_url(service_url)
    return stt_service

def transcribe_audio(stt_service, audio_path):
    """Transcribe audio file using IBM Watson Speech to Text."""
    with open(audio_path, 'rb') as audio_file:
        response = stt_service.recognize(
            audio=audio_file,
            content_type='audio/wav',
            model='en-US_BroadbandModel',
            timestamps=True,
            word_confidence=True
        ).get_result()
    
    transcripts = [alt['transcript']
                  for result in response['results']
                  for alt in result['alternatives']]
    return " ".join(transcripts).strip()
