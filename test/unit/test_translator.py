from src.translator import translate_content

def basic_translate_content(content: str) -> tuple[bool, str]:
    if content == "这是一条中文消息":
        return False, "This is a Chinese message"
    if content == "Ceci est un message en français":
        return False, "This is a message in French"
    if content == "Esta es un mensaje en español":
        return False, "This is a Spanish message"
    if content == "Esta é uma mensagem em português":
        return False, "This is a Portuguese message"
    if content  == "これは日本語のメッセージです":
        return False, "This is a Japanese message"
    if content == "이것은 한국어 메시지입니다":
        return False, "This is a Korean message"
    if content == "Dies ist eine Nachricht auf Deutsch":
        return False, "This is a German message"
    if content == "Questo è un messaggio in italiano":
        return False, "This is an Italian message"
    if content == "Это сообщение на русском":
        return False, "This is a Russian message"
    if content == "هذه رسالة باللغة العربية":
        return False, "This is an Arabic message"
    if content == "यह हिंदी में संदेश है":
        return False, "This is a Hindi message"
    if content == "นี่คือข้อความภาษาไทย":
        return False, "This is a Thai message"
    if content == "Bu bir Türkçe mesajdır":
        return False, "This is a Turkish message"
    if content == "Đây là một tin nhắn bằng tiếng Việt":
        return False, "This is a Vietnamese message"
    if content == "Esto es un mensaje en catalán":
        return False, "This is a Catalan message"
    if content == "This is an English message":
        return True, "This is an English message"
    if content == "Hello":
        return True, "Hello"
    return True, content


def test_chinese():
    is_english, translated_content = translate_content("这是一条中文消息")
    assert is_english == False
    assert translated_content == "This is a Chinese message"

# def test_french():
#     is_english, translated_content = translate_content("Ceci est un message en français")
#     assert is_english == False
#     assert translated_content == "This is a French message"

# def test_french():
#     is_english, translated_content = translate_content("Ceci est un message en français")
#     assert is_english == False
#     assert translated_content == "This is a French message"

def test_llm_normal_response():
    test_text_list = ["这是一条中文消息", "Ceci est un message en français", "Esta es un mensaje en español", "Esta é uma mensagem em português", 
                "これは日本語のメッセージです", "이것은 한국어 메시지입니다", "Dies ist eine Nachricht auf Deutsch", "Questo è un messaggio in italiano", 
                "Это сообщение на русском", "هذه رسالة باللغة العربية", "यह हिंदी में संदेश है", "นี่คือข้อความภาษาไทย", "Bu bir Türkçe mesajdır", 
                "Đây là một tin nhắn bằng tiếng Việt", "Esto es un mensaje en catalán", "This is an English message", "Hello"]
    for test_text in test_text_list:
        is_english, translated_content = basic_translate_content(test_text)
        LLM1_is_english, LLM2_translation = translate_content(test_text)
        assert (is_english == LLM1_is_english)
        assert (translated_content == LLM2_translation)

def test_llm_gibberish_response():
    test_text_list = ["adfasf", "lkjsadhflkjashdflkjahf", "hellos,aj;dslf", "j;lkasjfd;al", "Conichi hola hi bonjour"]
    assumed_output = [(True, "adfasf"), (True, "lkjsadhflkjashdflkjahf"), (True, "hellos,aj;dslf"), (True, "j;lkasjfd;al"), 
                      (True, "Conichi hola hi bonjour"), (True, "Hows the duudly dumdum")]
    for i in range (len(test_text_list)):
        assert (assumed_output[i] == translate_content(test_text_list[i]))
        




