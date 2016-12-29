import http.client
import json
from picture import get_picture_url

result = list()


def request_api(text):
    conn = http.client.HTTPConnection("api.bosonnlp.com")

    headers = {
        'content-type': "application/json",
        'accept': "application/json",
        'x-token': "D4kzWL2C.10867.LravVg7ReFAI"
    }

    conn.request("POST", "/tag/analysis?space_mode=0&oov_level=3&t2s=0&=&special_char_conv=0", text.encode('utf-8'),
                 headers)

    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))

    return data[0]


def main():
    print("捕获关键词大约需要2至3分钟，请倒杯茶等待")
    f = open('test_text.txt', 'r', encoding='utf-8')
    text_list = f.read().split('\n')
    text_list = filter(lambda x: x != '', text_list)
    for item in text_list:
        text = "\"" + item + "\""
        progress(text)
    print("总共捕获%s个关键词，即将获取图片，该过程时间视网络情况而定，一般非常缓慢，请倒杯茶等待" % len(result))
    for item in result:
        print(item['m'] * get_picture_url(item['n']))


def progress(text):
    result_raw = list()
    data = request_api(text)
    for i, item in enumerate(data['tag']):
        if item == 'm':
            result_raw.append(obtain_m_q_n(data, i))
    # 原本试图删除数组中的元素 发现index会乱 现在改用filter 勿忘
    result_raw = filter(lambda x: m_str_to_m_int(x['m']) is not False, result_raw)
    result_raw = list(result_raw)
    for item in result_raw:
        item['m'] = int(m_str_to_m_int(item['m']))  # 把文字表示的m词装换成int
    for item in result_raw:
        if 'q' in item and (item['q'] == '对' or item['q'] == '双' or item['q'] == '对'):
            item['m'] = item['m'] * 2
        if 'q' in item:
            del item['q']
    result_raw = filter(lambda x: x['n'] != '', result_raw)
    for item in result_raw:
        result.append(item)
        # print(item['n'])
    print('捕捉到%s个关键词' % len(result))


def obtain_m_q_n(data, index):  # 常见关键词为mqn(n)结构（数词、量词、名词）
    index_inner = index
    result_temp = dict()
    if data['word'][index_inner] == '一个':  # 分词发现一个bug 把'一个'这种词分成m而不是mq 所以进行处理 '二个'就没有这个问题
        result_temp['m'] = '一'
        result_temp['q'] = '个'
    else:
        result_temp['m'] = data['word'][index_inner]
    index_inner += 1
    if data['tag'][index_inner] == 'q':
        result_temp['q'] = data['word'][index_inner]
        result_temp['n'] = mining(data, index_inner)
    else:
        result_temp['n'] = mining(data, index_inner - 1)
    return result_temp


def mining(data, index):  # 向后挖掘名词
    index_inner = index
    text_temp = ""
    while True:
        index_inner += 1
        if data['tag'][index_inner][0] == 'n':
            text_temp += data['word'][index_inner]
        elif data['tag'][index_inner][0] == 'w':  # 不放心 为了防止死循环 遇到标点符号强制停止
            break
        elif data['tag'][index_inner] != 'a' and data['tag'][index_inner][0] != 'n' and data['tag'][
            index_inner] != 'z' and \
                        data['tag'][index_inner][0] != 'u':  # 排除一些定语的成分后 如形容词a 状态词z 以及助词u 视为该mqn结构结束
            break
    return text_temp


def m_str_to_m_int(m_str):
    dict_test_list_1 = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17',
                        '18', '19', '20']
    dict_test_list_2 = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十',
                        '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十']
    dict_test_list_3 = ['壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖', '拾', '拾壹', '拾贰', '拾叁', '拾肆',
                        '拾伍', '拾陆', '拾柒', '拾捌', '拾玖', '贰拾']

    if m_str == '两':  # 特例
        return 2
    if m_str in dict_test_list_1:
        return int(dict_test_list_1.index(m_str) + 1)
    elif m_str in dict_test_list_2:
        return int(dict_test_list_2.index(m_str) + 1)
    elif m_str in dict_test_list_3:
        return int(dict_test_list_3.index(m_str) + 1)
    else:
        return False


main()
