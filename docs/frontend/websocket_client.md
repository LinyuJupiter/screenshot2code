# websocket_client

## 概述

websocket_client 是一个基于websocket的客户端。在本前端项目中，它被用来向后端接口建立websocket连接，从而实现与后台的实时通信。

## 功能

- 支持websocket协议
- 拥有两个信号槽，分别为接收信息槽和中断连接槽
- 接受信息槽可以将接收到的信息发送给槽口
- 中断连接槽会在与服务器断开连接时发送信号给槽口
