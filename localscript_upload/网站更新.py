from threading import Thread
import requests
from io import BytesIO
from PIL import Image
import os
import pickle
import re
import time
import paramiko
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

requests.packages.urllib3.disable_warnings()

headers ={
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    'Referer': "https://mp.weixin.qq.com/",
    "Host": "mp.weixin.qq.com"
}

class showpng(Thread):
    def __init__(self, data):
        Thread.__init__(self)
        self.data = data

    def run(self):
        img = Image.open(BytesIO(self.data))
        img.show()

def islogin(session):
    try:
        session.cookies.load(ignore_discard=True)
    except Exception:
        pass
    loginurl = session.get("https://mp.weixin.qq.com/cgi-bin/scanloginqrcode?action=ask&token=&lang=zh_CN&f=json&ajax=1").json()
    if loginurl['base_resp']['ret'] == 0:
        print('Cookies值有效，无需扫码登录！')
        # print("loginurl:", loginurl)
        return session, True
    else:
        print('Cookies值已经失效，请重新扫码登录！')
        return session, False


# 公众号扫码登陆
def gzhlogin():

    session = requests.session()
    session.get('https://mp.weixin.qq.com/', headers=headers)
    session.post('https://mp.weixin.qq.com/cgi-bin/bizlogin?action=startlogin', data='userlang=zh_CN&redirect_url=&login_type=3&sessionid={}&token=&lang=zh_CN&f=json&ajax=1'.format(int(time.time() * 1000)), headers=headers)
    loginurl = session.get('https://mp.weixin.qq.com/cgi-bin/scanloginqrcode?action=getqrcode&random={}'.format(int(time.time() * 1000)))
    dateurl = 'https://mp.weixin.qq.com/cgi-bin/scanloginqrcode?action=ask&token=&lang=zh_CN&f=json&ajax=1'
    t = showpng(loginurl.content)
    t.start()
    while 1:
        date = session.get(dateurl).json()
        if date['status'] == 0:
            print('二维码未失效，请扫码！')
        elif date['status'] == 6:
            print('已扫码，请确认！')
        if date['status'] == 1:
            print('已确认，登录成功！')
            url = session.post('https://mp.weixin.qq.com/cgi-bin/bizlogin?action=login', data='userlang=zh_CN&redirect_url=&cookie_forbidden=0&cookie_cleaned=1&plugin_used=0&login_type=3&token=&lang=zh_CN&f=json&ajax=1', headers=headers).json()
            print("url:", url)
            # 获取token，并保存到cookies
            redirect_url = url["redirect_url"]

            token = redirect_url[redirect_url.rfind("=") + 1:len(redirect_url)]
            requests.utils.add_dict_to_cookiejar(session.cookies, {"token": token})
            break
        time.sleep(2)
    with open('gzhcookies.cookie', 'wb') as f:
        pickle.dump(session.cookies, f)
    return session

def checkSession():
    # 写入
    session = requests.session()
    if not os.path.exists('gzhcookies.cookie'):
        with open('gzhcookies.cookie', 'wb') as f:
            pickle.dump(session.cookies, f)
    # 读取
    session.cookies = pickle.load(open('gzhcookies.cookie', 'rb'))
    session, status = islogin(session)
    if not status:
        session = gzhlogin()

    return session

def gengxin():
    driver = webdriver.Edge()
    driver.maximize_window()

    # 全局变量用来存储提取到的 token 值
    global_tokens = set()

    # 打开网页
    driver.get("https://mp.weixin.qq.com/")

    # 以二进制模式读取保存的 cookie
    with open('gzhcookies.cookie', 'rb') as f:
        cookies = pickle.load(f)

    for cookie in cookies:
        # 删除不需要的属性
        del cookie._rest

        # 将 cookie 对象转换为可迭代的字典
        cookie_dict = cookie.__dict__

        # 添加 cookie 到浏览器
        driver.add_cookie(cookie_dict)

        # 刷新页面
        driver.refresh()

    # 等待页面加载完毕
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "new-creation__menu-item")))

    # 获取所有class为"new-creation__menu-item"的元素
    element = driver.find_element(By.CLASS_NAME, 'new-creation__menu-item')
    element.click()

    # 等待新标签页加载完毕
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))

    # 切换到新标签页
    driver.switch_to.window(driver.window_handles[-1])

    # 进行操作
    link = driver.find_element(By.ID, 'js_editor_insertlink')
    link.click()

    # 等待操作完成
    time.sleep(10)

    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'weui-desktop-btn')))
    button.click()

    # 找到所有具有相同类名的元素
    elements = driver.find_elements(By.CLASS_NAME, 'weui-desktop-form__input')

    # 确保至少有两个元素存在
    if len(elements) >= 2:
        # 选择第二个元素进行操作
        second_element = elements[1]
        second_element.send_keys("上虞区职业教育中心")
        second_element.send_keys(Keys.RETURN)
        list_item = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'inner_link_account_item')))
        list_item.click()
    else:
        print("无法找到第二个元素")

    # 通过执行 JavaScript 获取 fetch 或 XHR 资源的信息
    resources = driver.execute_script("return performance.getEntriesByType('resource')")

    # 用集合来存储唯一的 token 值
    unique_tokens = set()

    for resource in resources:
        if 'name' in resource.keys():
            resource_name = resource['name']
            # 使用正则表达式提取 token 字段的文本
            token_match = re.search(r"token=(\w+)", resource_name)
            if token_match:
                token = token_match.group(1)
                # 将 token 添加到集合中
                unique_tokens.add(token)
                # 将 token 添加到全局变量中
                global_tokens.add(token)

        # 打印唯一的 token 值
    for token in unique_tokens:
        print(token)

        # 获取请求标头中的Cookie
        cookie_str = driver.execute_script("return document.cookie;")
        cookie_str = "'{}'".format(cookie_str)
        print(cookie_str)

        formatted_tokens = str(global_tokens)
        formatted_tokens = formatted_tokens.strip('{}')
        print(formatted_tokens)

        directory = "./Temp"  # 替换为您想要创建的目录路径

        if not os.path.exists(directory):
            os.makedirs(directory)
            print("目录创建成功")

            # 远程服务器信息
            hostname = "10.1.10.111"
            port = 22
            username = "root"
            password = "syadmin"

            # 连接远程服务器
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname, port, username, password)

            # 执行命令来修改文件
            remote_file_path = "/home/sh/pythonProject/weixin.py"
            local_file_path = "./Temp/weixin.py"

            # 下载远程文件到本地
            sftp = ssh_client.open_sftp()
            sftp.get(remote_file_path, local_file_path)
            sftp.close()

            if os.path.exists(local_file_path):
                print("文件存在")
                # 打开文件并读取内容
                with open(local_file_path, 'r', encoding='utf-8') as file:
                    file_content = file.read()

                    # 替换文件内容中的 token 和 cookie
                    updated_text = re.sub(r"token = '.*'", f"token = {formatted_tokens}", file_content)
                    final_text = re.sub(r"Cookie = '.*'", f"Cookie = {cookie_str}", updated_text)

                # 将修改后的内容写回文件
                with open(local_file_path, 'w', encoding='utf-8') as file:
                    file.write(final_text)

                # 上传修改后的文件到远程服务器
                sftp = ssh_client.open_sftp()
                sftp.put(local_file_path, remote_file_path)
                sftp.close()

                # 关闭连接
                ssh_client.close()
                print('替换完成')

                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect('10.1.10.111', username='root', password='syadmin')

                stdin, stdout, stderr = ssh.exec_command('systemctl restart weixin.py')
                print("执行更新完成")
                ssh.close()
                driver.quit()
            else:
                print("文件不存在")
        else:
            print("目录已存在")

            # 远程服务器信息
            hostname = "10.1.10.111"
            port = 22
            username = "root"
            password = "syadmin"

            # 连接远程服务器
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname, port, username, password)

            # 执行命令来修改文件
            remote_file_path = "/home/sh/pythonProject/weixin.py"
            local_file_path = "./Temp/weixin.py"

            # 下载远程文件到本地
            sftp = ssh_client.open_sftp()
            sftp.get(remote_file_path, local_file_path)
            sftp.close()

            if os.path.exists(local_file_path):
                print("文件存在")
                # 打开文件并读取内容
                with open(local_file_path, 'r', encoding='utf-8') as file:
                    file_content = file.read()

                    # 替换文件内容中的 token 和 cookie
                    updated_text = re.sub(r"token = '.*'", f"token = {formatted_tokens}", file_content)
                    final_text = re.sub(r"Cookie = '.*'", f"Cookie = {cookie_str}", updated_text)

                # 将修改后的内容写回文件
                with open(local_file_path, 'w', encoding='utf-8') as file:
                    file.write(final_text)

                # 上传修改后的文件到远程服务器
                sftp = ssh_client.open_sftp()
                sftp.put(local_file_path, remote_file_path)
                sftp.close()

                # 关闭连接
                ssh_client.close()
                print('替换完成')

                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect('10.1.10.111', username='root', password='syadmin')

                stdin, stdout, stderr = ssh.exec_command('systemctl restart weixin.py')
                print("执行更新完成")
                ssh.close()
                driver.quit()


if __name__ == '__main__':
    session = checkSession()
    gengxin()
    input("按任意键退出程序...")
