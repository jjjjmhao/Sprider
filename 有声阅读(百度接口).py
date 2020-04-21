import re
from aip import AipSpeech

app_id = '14975947'
api_key = 'X9f3qewZCohppMHxlunznUbi'
secret_key = 'LupWgIIFzZ9kTVNZSH5G0guNGZIqqTom'

client = AipSpeech(app_id,api_key,secret_key)

with open('read.txt','r') as a:
    text = a.readlines()

for cut in text:
    #以1000个字节的长度进行分割
    text_cut = re.findall('.{1000}', cut)
    text_cut.append(cut[(len(text_cut) * 1000):])
    #在分割后的字符串中间插入"---"
    text_final = '---'.join(text_cut)
#计算文本中有多少个"---"标志
times = text_final.count('---')
for n in range(0,times+1):
    name = text_final.split('---')[n]
    result = client.synthesis(name, 'zh', '1',
                              {"vol": 9,
                               "spd": 4,
                               "pit": 9,
                               "per": 3,
                               })

    with open('test/' + str(n + 1) + '.mp3', "wb") as d:
        print('正在生成第' + str(n + 1) + '段语音......')
        d.write(result)