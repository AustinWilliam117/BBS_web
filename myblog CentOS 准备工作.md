#### myblog CentOS 准备工作 

``` shell 
wget https://www.python.org/ftp/python/3.4.3/Python-3.4.3.tgz
wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz
```

```shell 
yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel python-devel mysql-devel gcc make
```

```shell
./configure
make
make install
pip3.4 install --upgrade pip
```

```shell 
yum install mysql-server
```

```shell
pip install mysqlclient
```

您可能需要像这样安装Python和MySQL开发标头和库：

- `sudo apt-get install python-dev default-libmysqlclient-dev` ＃Debian / Ubuntu
- `sudo yum install python-devel mysql-devel` ＃Red Hat / CentOS
- `brew install mysql-client` ＃macOS（自制）

