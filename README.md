# 上虞区职业教育中心新闻媒体中心网页源代码

本项目是上虞区职业教育中心新闻媒体中心的网页源代码，网页错误请提交至 Issues 中。

注意：本项目为纯静态网页，由 JS 侦测直播流的有效性来控制网站首页的重定向，网页内容则通过 Python 脚本进行定时更新。

## 使用

使用以下命令拉取文件至 Web 服务器中即可。

    git clone https://github.com/CHEN-Technology/Shangyu_Vocational_Education_Center_News_Media_Center_Web.git

## 轮播图更新

轮播图是通过 Python 对微信公众平台进行内容的爬取，再通过多个 Python 脚本进行文件的更新。

serverfile_updatescript 中的是服务器端更新网页文件的脚本，需放置在服务器中并使用 timer 计时器等方式定时执行。

localscript_upload 中的是进行微信 cookie 的更新，自动运行浏览器获取公众号数据并远程连接服务器进行 weixin.py 脚本的更新的脚本。

localscript_upload 中的脚本在 cookie 无效时运行会请求扫码登录，请使用注册了微信公众号的微信号进行登录，登录后重新运行脚本即可运行浏览器自动化获取数据进行后续操作。

#### 注：推荐将脚本打包使用，省去脚本环境配置步骤。
