from googletrans import Translator
from django.core.cache import cache

translator = Translator()

def get_chosung(text):
    HANGUL_START = 44032
    HANGUL_END = 55203
    CHOSUNG_LIST = [
        'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
    ]

    def is_hangul(char):
        return HANGUL_START <= ord(char) <= HANGUL_END

    def get_chosung_char(char):
        if not is_hangul(char):
            return char
        return CHOSUNG_LIST[(ord(char) - HANGUL_START) // 588]

    return ''.join(get_chosung_char(char) for char in text)
  
# def get_english_variants(text):
#     # googletrans 라이브러리를 사용하여 한글을 영어로 번역
#     result = translator.translate(text, src='ko', dest='en')
#     result_no_spaces = result.text.replace(' ', '')  # 띄어쓰기 제거
#     return result_no_spaces

def get_english_variants(text):
    cache_key = f"translation_{text}"
    cached_translation = cache.get(cache_key)
    
    if cached_translation:
        return cached_translation
    
    result = translator.translate(text, src='ko', dest='en').text
    result_no_spaces = result.replace(' ', '')  # 띄어쓰기 제거
    cache.set(cache_key, result_no_spaces, timeout=60*60*24)  # 24시간 동안 캐시
    return result_no_spaces
