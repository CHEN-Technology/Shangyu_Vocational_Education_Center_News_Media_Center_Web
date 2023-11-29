import datetime

import requests
import json
from bs4 import BeautifulSoup
import shutil

Cookie = '_clck=y19we1|1|fh2|0; ua_id=EYuE8BnEQMu0mujOAAAAAMq5M1RzAkX1bXDufU2kwLY=; wxuin=01053063693377; uuid=e0fc068b646902f5d4988324a0277ea0; rand_info=CAESIOHIyuYR86w9eS3n86dQ+Wf3Ys5rUSPaXsOwSxzzR5qY; slave_bizuin=3901605875; data_bizuin=3901605875; bizuin=3901605875; data_ticket=p6mz150EDGNVv0WCAdFsq0I5ld5+Nvh/hvNunZqXDNWbVa7EE7gIM/JHr3M2rFiW; slave_sid=U29OTTV4dWxOUTlTTUtaR3V3N2dEREp4ZFlWTjR2T01nUWxsNXFzWU12OVpBSk10c0hoWWhpdmhoMlphQmpBbDBJMjlyMjdKZWplS3BSOXRvb0ZlUkZ0UjhTS2ozQWJWZllJbUtYSGt5Um12Tm9MdGVtMWFsRGJxOGxvYWJ6SzFqZm4yQWxUWHhQUlJyZDhX; slave_user=gh_ad4fbe72fcc1; xid=c9152dc550a932d91bb7acb812e48280; mm_lang=zh_CN; token=235315890; _clsk=1ij6iwm|1701053072930|5|1|mp.weixin.qq.com/weheat-agent/payload/record'
url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
headers = {
  "Cookie": Cookie,
  "User-Agent": 'Mozilla/5.0 (Linux; Android 10; YAL-AL00 Build/HUAWEIYAL-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.64 HuaweiBrowser/10.0.1.335 Mobile Safari/537.36'
    }

keyword = 'zjzx'
token = '235315890'
search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&begin=0&count=5&query={}&token={}&lang=zh_CN&f=json&ajax=1'.format(keyword, token)

doc = requests.get(search_url,headers=headers).text
print(doc)
jstext = json.loads(doc)
fakeid = jstext['list'][0]['fakeid']

data = {
    "token": token,
    "lang": "zh_CN",
    "f": "json",
    "ajax": "1",
    "action": "list_ex",
    "begin": 0,
    "count": "5",
    "query": "",
    "fakeid": "MzI1OTIwNzc4OA==",
    "type": "9",
    }
response = requests.get(url, headers=headers, params=data).text
json_text = json.loads(response)
# print(json_text)

# 遍历 app_msg_list 数组中的每个元素
for item in json_text["app_msg_list"]:
    # 获取封面(cover)、创建时间(create_time)、标题(title)、链接(link)
    cover = item["cover"]
    create_time = item["create_time"]
    title = item["title"]
    link = item["link"]

    # 将创建时间转换为日期对象
    dt = datetime.datetime.fromtimestamp(create_time)

    # 将日期对象格式化为 "2005-12-25" 样式
    formatted_date = dt.strftime("%Y-%m-%d")

    # 打印结果
    # print("封面: ", cover)
    # print("创建时间: ", formatted_date)
    # print("标题: ", title)
    # print("链接: ", link)
    # print("---------------------------")

html_file_path = "/usr/share/nginx/html/index.html"  # 替换为实际的HTML文件路径
# html_file_path = "C:/Users/Administrator/Desktop/test/test.html"

with open(html_file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

# print(html_content)

# 将HTML文本加载到BeautifulSoup中
soup = BeautifulSoup(html_content, 'html.parser')

imgs_divs = soup.find_all('div', class_='imgs')

for imgs_div in imgs_divs:
    imgs_div.clear()

titles_divs = soup.find_all('div', class_='titles')

for titles_div in titles_divs:
    titles_div.clear()

# 遍历app_msg_list数组中的每个元素
for item in json_text["app_msg_list"]:
    # 获取封面(cover)、创建时间(create_time)、标题(title)、链接(link)
    cover = item["cover"]
    create_time = item["create_time"]
    title = item["title"]
    link = item["link"]

    # 将创建时间转换为日期对象
    dt = datetime.datetime.fromtimestamp(create_time)

    # 将日期对象格式化为 "2005-12-25" 样式
    formatted_date = dt.strftime("%Y-%m-%d")

    # 插入cover和link到class为imgs的div的子元素a的属性中
    imgs_div = soup.find('div', class_='imgs')
    a_element = soup.new_tag('a', href=link, target='_blank')
    img_element = soup.new_tag('img', src=cover)
    a_element.append(img_element)
    imgs_div.append(a_element)

    # 插入digest和formatted_date到class为titles的div的子元素a的子元素div的属性中
    titles_div = soup.find('div', class_='titles')
    a_element = soup.new_tag('a', href=link, target='_blank')
    div1_element = soup.new_tag('div', class_='title')
    div1_element.string = title
    div2_element = soup.new_tag('div', class_='title2')
    div2_element.string = formatted_date
    a_element.append(div1_element)
    a_element.append(div2_element)
    titles_div.append(a_element)

    a_elements_all = imgs_div.find_all('a')
    if len(a_elements_all) > 0:
        a_elements_all[0]['class'] = 'active'

    a_elements_all = titles_div.find_all('a')
    if len(a_elements_all) > 0:
        a_elements_all[0]['class'] = 'active'

# 获取修改后的HTML代码
modified_html = soup.prettify()

# 打印结果
# print(modified_html)

# 将修改后的HTML代码写入保存
output_file_path = "/usr/share/nginx/html/index.html"  # 替换为实际的输出文件路径
# output_file_path = "C:/Users/Administrator/Desktop/test/test.html"
with open(output_file_path, "w", encoding="utf-8") as file:
    file.write(modified_html)

# 打印保存成功的提示
print("Index保存成功！")

original_file_path = "/usr/share/nginx/html/index.html"
copy_file_path = "/usr/share/nginx/html/index_live.html"
shutil.copy(original_file_path, copy_file_path)

print("Index复制成功！")

# 读取复制的文件内容
with open(copy_file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

# 进行字符串替换
modified_html = html_content.replace('<script src="js/live.js">', '<script src="js/index_live.js">')

# 将修改后的HTML代码写回文件
with open(copy_file_path, "w", encoding="utf-8") as file:
    file.write(modified_html)

print("替换成功！")

with open(copy_file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "html.parser")

imgs_div = soup.find("div", class_="imgs")
titles_div = soup.find("div", class_="titles")

if imgs_div:
    first_a_element = imgs_div.find("a")
    if first_a_element:
        del first_a_element["class"]
        new_img_element = soup.new_tag("a", href="/html/live.html", target="_blank", class_="active")
        new_img_element.append(soup.new_tag("img", src="/img", alt=""))
        first_a_element.insert_before(new_img_element)

if titles_div:
    first_a_element = titles_div.find("a")
    if first_a_element:
        del first_a_element["class"]
        new_title_element = soup.new_tag("a", href="/html/live.html", target="_blank", class_="active")

        # 创建class为"title"的div并添加内容
        title_div = soup.new_tag("div", class_="title")
        title_div.string = "校园直播正在进行"
        new_title_element.append(title_div)

        new_title_element.append(soup.new_tag("div", class_="title2"))
        first_a_element.insert_before(new_title_element)

with open(copy_file_path, "w", encoding="utf-8") as file:
    file.write(str(soup))

print("插入成功！")

with open(copy_file_path, "r", encoding="utf-8") as file:
    html_content_fin = file.read()

# print(html_content_fin)

# 将HTML文本加载到BeautifulSoup中
soup_fin = BeautifulSoup(html_content_fin, 'html.parser')

# 选择包含class_属性的元素，并修改为class
elements = soup_fin.select('[class_]')
for element in elements:
    element['class'] = element['class_']
    del element['class_']

# 输出修改后的HTML
# print(soup_fin.prettify())

with open(copy_file_path, "w", encoding="utf-8") as file:
    file.write(str(soup_fin))

print("全部完成")
