import os

with open('libs'+os.sep+'genres'+os.sep+'raw.txt', 'rb') as f:
    raw_text = ' '.join([a.strip() for a in f.readlines()])

    subreddits = filter(lambda a: (a[:3] == '/r/' and str.isalnum(a[3:])), raw_text.split())
    subreddits = map(lambda x: x[3:].lower(), subreddits)
    print subreddits

with open('libs'+os.sep+'genres'+os.sep+'subs.txt', 'wb') as f:
    f.write(str(subreddits))

