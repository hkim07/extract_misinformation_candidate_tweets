import preprocessor as p
p.set_options(p.OPT.MENTION, p.OPT.EMOJI, p.OPT.URL)

def twitter_preprocessing(x):
  tmp = p.clean(x)
  return tmp
  
  
from langdetect import detect
def detect_lang(_text):
    from langdetect import DetectorFactory
    DetectorFactory.seed = 0
    try:
        lang = detect(_text)
    except:
        lang = ''
    return lang