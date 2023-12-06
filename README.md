# 上虞区职业教育中心新闻媒体中心网页源代码

Shangyu_Vocational_Education_Center_News_Media_Center_Web

## 使用

使用以下命令拉取文件至 Web 服务器中即可。

    git clone https://github.com/CHEN-Technology/Shangyu_Vocational_Education_Center_News_Media_Center_Web.git

## 更新

serverfile_updatescript 中的是服务器端更新网页文件的脚本，需放置在服务器中并使用 timer 计时器等方式定时执行。

localscript_upload 中的是进行微信 cookie 的更新，自动运行浏览器获取公众号数据并远程连接服务器进行 weixin,py 脚本的更新的脚本。

网站更新.py 在 cookie 无效时运行会请求扫码登录，请使用注册了微信公众号的微信号进行登录，登录后重新运行脚本即可运行浏览器自动化获取数据进行后续操作。

##### 注：推荐将网站更新.py 打包，省去脚本环境配置步骤。
