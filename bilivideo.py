import requests
import time
import random

'''
作者：pk哥
公众号：Python知识圈
日期：2018/10/02
代码解析详见公众号「Python知识圈」。

'''


def get_json(url):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    params = {
        'page_size': 10,
        'next_offset': str(num),
        'tag': '今日热门',
        'platform': 'pc'
    }
    try:
        html = requests.get(url, params=params, headers=headers)
        return html.json()
    except BaseException:
        print('request error')
        pass


def downloader(url, path):
    start = time.time()   # 开始时间
    size = 0
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/68.0.3440.106 Safari/537.36'}
    response = requests.get(url, headers=headers, stream=True)   # stream 属性必须带上
    chunk_size = 1024    # 每次下载的数据大小
    content_size = int(response.headers['content-length'])   # 总大小
    if response.status_code == 200:
        print('[文件大小]:%0.2f MB' % (content_size / chunk_size / 1024))   # 换算单位
        with open(path, 'wb') as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                size += len(data)   # 已下载的文件大小
                print('\r' + '[下载进度]:%s%.2f%%' % ('>' * int(size * 50 / content_size), float(size / content_size *
                                                                                             100)), end=" ")
    end = time.time()    # 结束时间
    print('\n' + '视频下载完成！用时%.2f秒' % (end - start))


if __name__ == '__main__':
    for i in range(10):
        url = 'http://api.vc.bilibili.com/board/v1/ranking/top?'
        num = i * 10 + 1
        html = get_json(url)
        infos = html['data']['items']
        for info in infos:
            title = info['item']['description']    # 小视频的标题
            video_url = info['item']['video_playurl']  # 小视频的下载链接
            print(title)
            # 为了防止有些视频没有提供下载链接的情况
            try:
                downloader(video_url, path='%s.mp4' % title)
                print('成功下载一个！')
            except BaseException:
                print('凉凉！下载失败')
                pass
        time.sleep(int(format(random.randint(2, 8))))   # 设置随机等待时间
