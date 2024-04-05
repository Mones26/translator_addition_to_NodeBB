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

  try:
    classified_language = get_language(post)
  except:
    return (False, failure_text) # api failed
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
  try:
    translated = get_translation(post)
  except:
    return (False, failure_text) # couldn't translate

  # if something went wrong with translation, account for this
  if not translated or not isinstance(translated, str):
    return (False, failure_text)

  return (False, translated)
