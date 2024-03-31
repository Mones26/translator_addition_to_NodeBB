from typing import Callable

from google.colab import auth
from google.cloud import aiplatform

PROJECT_ID = "nodebb-416919" # TODO: Replace with your GCP Project ID

# Set the project id
! gcloud config set project {PROJECT_ID}

auth.authenticate_user()

aiplatform.init(
    # your Google Cloud Project ID or number
    # environment default used is not set
    project=PROJECT_ID,

    # the Vertex AI region you will use
    # defaults to us-central1
    location='us-central1',
)
from vertexai.language_models import ChatModel, InputOutputTextPair

chat_model = ChatModel.from_pretrained("chat-bison@001")

def get_translation(post: str) -> str:
    parameters = {
        "temperature": 0.7,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
    }

    chat = chat_model.start_chat(context=post)
    response = chat.send_message(post, **parameters)
    return response.text

def get_language(post: str) -> str:
    parameters = {
        "temperature": 0.7,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
    }
    chat = chat_model.start_chat(context=post)
    response = chat.send_message(post, **parameters)
    return response.text

def query_llm(post: str) -> tuple[bool, str]:
  # use zero-shot prompting, due to fairly strong empirical results

  classified_language = get_language(post)
  # if the post is in english to begin with, return the original content
  if "english" in classified_language.lower():
    return (True, post)
  # if the post seems malformed, make this known
  if "malformed" in classified_language.lower():
    return (False, "Malformed")
  # otherwise, translate the sentence to english, and return
  translated = get_translation(post)
  return (False, translated)

def translate_content(content: str) -> tuple[bool, str]:
    return query_llm(content)
    # if content == "这是一条中文消息":
    #     return False, "This is a Chinese message"
    # if content == "Ceci est un message en français":
    #     return False, "This is a French message"
    # if content == "Esta es un mensaje en español":
    #     return False, "This is a Spanish message"
    # if content == "Esta é uma mensagem em português":
    #     return False, "This is a Portuguese message"
    # if content  == "これは日本語のメッセージです":
    #     return False, "This is a Japanese message"
    # if content == "이것은 한국어 메시지입니다":
    #     return False, "This is a Korean message"
    # if content == "Dies ist eine Nachricht auf Deutsch":
    #     return False, "This is a German message"
    # if content == "Questo è un messaggio in italiano":
    #     return False, "This is an Italian message"
    # if content == "Это сообщение на русском":
    #     return False, "This is a Russian message"
    # if content == "هذه رسالة باللغة العربية":
    #     return False, "This is an Arabic message"
    # if content == "यह हिंदी में संदेश है":
    #     return False, "This is a Hindi message"
    # if content == "นี่คือข้อความภาษาไทย":
    #     return False, "This is a Thai message"
    # if content == "Bu bir Türkçe mesajdır":
    #     return False, "This is a Turkish message"
    # if content == "Đây là một tin nhắn bằng tiếng Việt":
    #     return False, "This is a Vietnamese message"
    # if content == "Esto es un mensaje en catalán":
    #     return False, "This is a Catalan message"
    # if content == "This is an English message":
    #     return True, "This is an English message"
    # return True, content
