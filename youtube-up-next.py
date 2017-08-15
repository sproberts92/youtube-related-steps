import json
import random
from pprint import pprint

import requests

base_url = 'https://www.googleapis.com/youtube/v3'
target_artist = ''
start_id = ''


def main():
    api_key = json.load(open('api-key.json', 'r'))['key']

    visted = []

    while True:
        id_ = start_id

        # Request the related videos
        params = {'relatedToVideoId': id_, 'key': api_key, 'type': 'video',
                  'part': ','.join(['id', 'snippet'])}
        data = requests.get(base_url + '/search', params=params).json()

        # Extract the ids of the related vidoes
        ids = {vid['id']['videoId']:vid['snippet']['title']  for vid in data['items']}

        # Request info on the related vidoes
        params = {'id': ','.join(ids), 'key': api_key, 'part': 'statistics,snippet'}
        vid_stats = requests.get(base_url + '/videos', params=params).json()

        # Extract the views/likes from each of the related vids
        counts = [(vid['id'], int(vid['statistics']['viewCount']), int(vid['statistics']['likeCount'])/(int(vid['statistics']['likeCount']) + int(vid['statistics']['dislikeCount'])), vid['snippet']['categoryId']) for vid in vid_stats['items']]
        counts = [c for c in counts if c[3] == '10']

        # Filter out the ids already visited
        unvisted = [v for v in counts if v[0] not in visted]

        # Either choose the most viewed or liked or choose one randomly
        if unvisted and random.randrange(1):
            most_played = max(unvisted, key=lambda x: x[1])
        else:
            most_played = counts[random.randrange(len(counts))]


        # Append the selected vid to the visited list
        try:
            id_ = most_played[0]
            visted.append(id_)
        except Exception as e:
            print(e)

        # Trim the visited list
        if len(visted) > 15:
            del visted[0]

        # Look for the target artist in the title
        vid_title = ids[most_played[0]]
        print(most_played, vid_title)
        if target_artist in vid_title.lower().split('-')[-1]:
            return

if __name__ == '__main__':
    main()
