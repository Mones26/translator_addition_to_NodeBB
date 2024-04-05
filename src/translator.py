import pathlib
import textwrap
import os
from tqdm import tqdm

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown
import pdb

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

genai.configure(api_key=os.environ['API_KEY']) # the api key should be saved as an env var via export API_KEY = ...

model = genai.GenerativeModel('gemini-pro')

def get_translation(post: str) -> str:
    response = model.generate_content("Please translate this to english: " + post)
    return response.text

def get_language(post: str) -> str:
    response = model.generate_content("What language is this? If it is not written in a recognizable language, please say 'Impossible': " + post)
    return response.text

def translate_content(post: str) -> tuple[bool, str]:
  failure_text = "Sorry - we failed to properly parse and translate your post! Something may be wrong with our backend :/"

  classified_language = get_language(post)
  # if something went wrong with classification, account for this
  error_keywords = ["understand", "didn't", "sorry"]
  for word in error_keywords:
    if word in classified_language:
      return (False, failure_text)
  if not classified_language or not isinstance(classified_language, str):
    return (False, failure_text)

  # if the post is in english to begin with, return the original content
  if "english" in classified_language.lower():
    return (True, post)
  # if the post seems malformed, make this known
  if "impossible" in classified_language.lower():
    return (False, "Malformed")
  # otherwise, translate the sentence to english, and return
  translated = get_translation(post)

  # if something went wrong with translation, account for this
  if not translated or not isinstance(translated, str):
    return (False, failure_text)

  return (False, translated)










# # def translate_content(content: str) -> tuple[bool, str]:
# #     # return query_llm(content)
# #     if content == "这是一条中文消息":
# #         return False, "This is a Chinese message"
# #     if content == "Ceci est un message en français":
# #         return False, "This is a French message"
# #     if content == "Esta es un mensaje en español":
# #         return False, "This is a Spanish message"
# #     if content == "Esta é uma mensagem em português":
# #         return False, "This is a Portuguese message"
# #     if content  == "これは日本語のメッセージです":
# #         return False, "This is a Japanese message"
# #     if content == "이것은 한국어 메시지입니다":
# #         return False, "This is a Korean message"
# #     if content == "Dies ist eine Nachricht auf Deutsch":
# #         return False, "This is a German message"
# #     if content == "Questo è un messaggio in italiano":
# #         return False, "This is an Italian message"
# #     if content == "Это сообщение на русском":
# #         return False, "This is a Russian message"
# #     if content == "هذه رسالة باللغة العربية":
# #         return False, "This is an Arabic message"
# #     if content == "यह हिंदी में संदेश है":
# #         return False, "This is a Hindi message"
# #     if content == "นี่คือข้อความภาษาไทย":
# #         return False, "This is a Thai message"
# #     if content == "Bu bir Türkçe mesajdır":
# #         return False, "This is a Turkish message"
# #     if content == "Đây là một tin nhắn bằng tiếng Việt":
# #         return False, "This is a Vietnamese message"
# #     if content == "Esto es un mensaje en catalán":
# #         return False, "This is a Catalan message"
# #     if content == "This is an English message":
# #         return True, "This is an English message"
# #     return True, content
