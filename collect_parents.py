import argparse, os, time, json
import pandas as pd
import tweepy
import config # Twitter api app credential

def main():
    auth = tweepy.OAuthHandler(config.ckey, config.csec)
    auth.set_access_token(config.akey, config.asec)
    api = tweepy.API(auth, wait_on_rate_limit_notify = True, wait_on_rate_limit = True)

    folder = 'parents'
    if not os.path.exists(folder):
        os.makedirs(folder)
    filelist = os.listdir(folder)

    dat = pd.read_csv('./res/replies_with_sims.csv')
    dat = dat[:args.number]
    reply_ids = dat.id

    filelist = [x.split('.json')[0] for x in filelist]
    for ix, reply_id in enumerate(reply_ids):
        reply_id = reply_id[1:]
        if str(reply_id) in filelist:
            continue
        else:
            print("(%s out of %s) target ID: %s" % (ix+1, args.number, reply_id))
            thread = []
            try:
                tmp = api.get_status(id=reply_id, tweet_mode='extended')._json
                thread.append(tmp)
                parent_id = tmp['in_reply_to_status_id'];
                time.sleep(2.1)

                tmp = api.get_status(id=parent_id, tweet_mode='extended')._json
                thread.append(tmp)
                with open("./%s/%s.json" % (folder, reply_id), 'w') as f:
                    json.dump(thread, f)
            except:
                with open("./%s/%s.json" % (folder, reply_id), 'w') as f:
                    json.dump(thread, f) # save empty thread


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Enter the size of subset')
  parser.add_argument('-n',  '--number', default = 10, type=int)
  args = parser.parse_args()
  main()
