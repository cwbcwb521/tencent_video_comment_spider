__author__ = 'slothgreed'

# video.coral.qq.com/varticle/2367268461/comment/v2?callback=_varticle2367268461commentv2&orinum=10&oriorder=o&pageflag=1&cursor=6360846676362179853&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=9&_=1516721543419
# video.coral.qq.com/varticle/2367268461/comment/v2?callback=_varticle2367268461commentv2&orinum=10&oriorder=o&pageflag=1&cursor=6360844620398243956&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=9&_=1516721543420
# video.coral.qq.com/varticle/2367268461/comment/v2?callback=_varticle2367268461commentv2&orinum=10&oriorder=o&pageflag=1&cursor=6360844620398243956

import urllib.request
import re
import http.cookiejar

# 设置视频编号
vid = 2367268461
# 设置起始评论id
comid = 6360813349059876569

headers={"Accept":"text/html,application/xthtml+xml,application/xml;q=0.9,*/*;q=0.8",
         "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
         "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
         "Connection":"keep-alive",
         "referer":"http://www.163.com/"}
cjar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
headall = []
for key,value in headers.items():
    item = (key,value)
    headall.append(item)
opener.addheaders = headall
urllib.request.install_opener(opener)

# 建立自定义函数craw(vid, comid), 实现自动爬取对应评论并返回
def craw(vid, comid):
    url = 'http://video.coral.qq.com/varticle/' + str(vid) + "/comment/v2?callback=_varticle" + str(vid) + 'commentv2&orinum=10&oriorder=o&pageflag=1&cursor=' + str(comid) + '&scorecursor=0&orirepnum=2&reporder=o&reppageflag=1&source=1'
    data = urllib.request.urlopen(url).read().decode('utf-8')
    return data

idpat = '"id":"(.*?)"'
userpat = '{"userid":"(.*?)","nick":"(.*?)"'
contpat = '"userid":"(.*?)","content":"(.*?)"'

# 过滤emoji
emoji_pattern = re.compile(
    u"(\ud83d[\ude00-\ude4f])|"  # emoticons
    u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
    u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
    u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
    u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
    "+", flags=re.UNICODE)

def remove_emoji(text):
    return emoji_pattern.sub(r'', text)

# 第一层循环，代表爬多少页
for i in range(1, 10):
    print("===================================")
    print("第 " +str(i)+ " 页评论内容：")
    data = craw(vid, comid)
    # 第二层循环，根据爬取结果提取并处理没调信息，一页10条评论
    idlist = re.compile(idpat, re.S).findall(data)
    userlist = re.compile(userpat, re.S).findall(data)
    contlist = re.compile(contpat, re.S).findall(data)
    for j in range(0, min(len(idlist), len(userlist), len(contlist))):
        for k in range(0, min(len(idlist), len(userlist), len(contlist))):
            try:
                if userlist[j][0] == contlist[k][0]:
                    print("用户名: " + remove_emoji(eval('u"' + userlist[j][1] + '"')))
                    print('内容为： ' + remove_emoji(eval('u"' + contlist[k][1] + '"')))
                    print('---------------------------------------------')
            except Exception as e:
                print(e)
                print("非法字符出现")
                pass
    # 将comid变为最后一条评论id，不断加载
    comid = idlist[9]