# NC(net_chat)网络通讯工具 By: Majjcom

本工具***安全快速***，提供相对***安全***的网络通讯环境

## 简介

还在担心自己的通讯数据**被监控**么，这里提供了一个*全新*的通讯工具

你可以部署自己的通讯环境，支持**局域网**和**广域网**通讯

配合其他工具可擦除***激情的火花***

## 使用

### 1.服务端

使用**Python3**运行`chat_server`中的`main.py`启动服务器(记得打开5555端口)

### 2.客户端

在Windows端可用Release中的NC来连接

**NC支持使用域名连接服务器**

在输入server时输入**域名**或**IP**按下<kbd>Enter</kbd>连接

输入服务的端口*(默认5555)*

随后输入**房间**和**对应秘钥**

进入房间后，按下<kbd>Alt</kbd>来进入输入模式，输入内容后按下<kbd>Enter</kbd>可发送

在输入时以\@开头可以运行指令(下方有指令列表)

当登录用户为Sys时，可运行所有指令

**注意，请下载对应服务器提供的公钥**

## 获取

Windows端可下载[NC_v1.5.1_Win_amd64.tar.gz](https://github.com/Majjcom/net_chat/releases/download/v1.5.1/NC_v1.5.1_Win_amd64.tar.gz)

*本版本仅支持Windows10 amd64*

## 指令列表

|指令  |     功能         |权限  |
|:---- |     :----:       |:----:|
|ADDR  |查看连接信息      |ALL   |
|LOGOUT|登出当前房间      |ALL   |
|CLEAR |清理屏幕          |ALL   |
|EXIT  |退出程序          |ALL   |
|PING  |发送PING指令给主机|ALL   |
|CREAT |创建房间          |Sys   |
|PASSWD|修改指定房间密钥  |Sys   |
|GETALL|接收房间所有信息  |Sys   |
