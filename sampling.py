import argparse
import pandas as pd

def main():
    dat = pd.read_csv('./res/non_replies.csv')
    dat = dat.sample(n = args.number, random_state=0)

    dat.to_csv('./res/non_reply_samples.csv', index = False)
    print("Saved in ./res/non_reply_samples.csv")

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Enter the number of samples')
  parser.add_argument('-n',  '--number', default = 100, type=int)
  args = parser.parse_args()
  main()
