import youtube_dl
import io
from contextlib import redirect_stdout
from url_in_list import crawl
import sys

stdout = sys.stdout
sys.stdout = io.StringIO()

url = 'https://www.youtube.com/watch?v=Im4hOxukBQo&index=32&list=PLCQyA4-pzVUSRo3hLQd_ZXr0KwLHHrb7l'
# url = 'https://www.youtube.com/playlist?list=PLCQyA4-pzVUQaV0K8GeLtqy3Rk27kmGqE'
ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s', 'ignoreerrors': True})

with ydl:
        result = ydl.extract_info(
            url,
            download=False  # We just want to extract the info
        )

output = sys.stdout.getvalue().splitlines()
sys.stdout = stdout

videos = []

if 'entries' in result:
    # Can be a playlist or a list of videos
    videos = result['entries']
else:
    # Just a video
    video = result

wrong_idx = []

for idx, video in enumerate(videos):
    if video is not None:
        pass
        # print(idx, video['title'])
    else:
        # print(idx, 'None')
        wrong_idx.append(idx)


# wrong_idx = [76, 81, 179, 215, 235, 288, 302, 329, 344, 347, 357, 359, 383, 411, 427]
print('\nwrong idx: ', wrong_idx)
# urls = crawl(url)
#
# print('\nurls: ')
# for u in urls:
#     print(u)
#
# print('\nnumber of urls: ', len(urls))
# wrong_urls = [urls[i] for i in range(len(urls)) if i in wrong_idx]
# print('\n{} wrong urls: '.format(len(wrong_urls)))
#
result = []
# for u in wrong_urls:
#     print(u)
#     i = u.index('=')
#     result.append(u[i + 1:])
#
# for u in result:
#     print(u)
lines = []

for line in output:
    if line[:9] == '[youtube]':
        lines.append(line)

urls = None

for line in lines:
    words = line.split()
    if not urls:
        urls = [words[1]]
    if urls[-1] != words[1]:
        urls.append(words[1])

for i in wrong_idx:
    print(urls[i])
    result.append(urls[i])


with open('missing_urls.txt', "w") as file:
    for u in result:
        file.write(u)
        file.write('\n')
