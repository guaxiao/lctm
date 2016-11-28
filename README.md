# lctm

# 使用方法
- 安装并开启 redis-server (注意一定要关闭 redis 的远程登录, 否则你的服务器会因为 redis 的安全漏洞被干掉, 几乎是一定的)
- 用 app.py 文件末尾的命令运行程序

## Vagrant
假设你
1. vagrant 已经安装完毕，
2. hyper-v 已禁用，
3. vt-x 在 bios 中已经开启，
4. 且有一个 ss 在 1080 端口监听。

打开一个 `powershell`， `cmd` 自己搜怎么设环境变量。
``` powershell
git clone https://github.com/guaxiao/lctm
$env:http_proxy="127.0.0.1:1080"
$env:https_proxy="127.0.0.1:1080"
vagrant plugin install vagrant-proxyconf
vagrant up
vagrant ssh -- -R 1080:localhost:1080
gunicorn wsgi --worker-class=gevent -t 4 -b 0.0.0.0:8000
```
然后打开 `127.0.0.1:8080`

如果不想开代理，则注释掉 `.Vagrantfile` 10-14行，且不带参数的运行 `vagrant ssh`

## windows 开发
*放弃 windows*


1. 下载虚拟机(vbox,vmware), 运行Linux, 比如 ubuntu
2. 安装redis (apt-get install redis-server)
3. git clone 项目
4. 安装依赖 (项目使用Python 3，所以使用 pip3 install.具体需要的包 使用 python3 app.py runserver 运行程序会出现提示)
5. 初始化数据库

    ```
    # python app.py shell
    >>> from models import db
    >>> db.create_all()
    ```
6. 用 app.py 文件末尾的命令运行程序
