import preprocessor as p
p.set_options(p.OPT.MENTION, p.OPT.EMOJI, p.OPT.URL)

def twitter_preprocessing(x):
  tmp = p.clean(x)
  return tmp