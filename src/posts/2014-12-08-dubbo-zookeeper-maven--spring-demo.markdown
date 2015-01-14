---
layout: post
title: "dubbo框架的学习"
date: 2014-12-08 16:51 +0800
comments: true
categories:
---

Dubbo是阿里巴巴公司开源的一个高性能优秀的服务框架，使得应用可通过高性能的 RPC 实现服务的输出和输入功能，可以和Spring框架无缝集成

<!-- more -->

provider暴露服务方称之为“服务提供者”。

Consumer调用远程服务方称之为“服务消费者”。

Registry服务注册与发现的中心目录服务称之为“服务注册中心”。

Monitor统计服务的调用次调和调用时间的日志服务称之为“服务监控中心”。

该Demo的Registry由zookeeper承担，在本机安装zookeeper,具体的安装方法：http://jingyan.baidu.com/article/456c463b60bd380a5931446f.html

工程由maven创建： 服务方提供服务，并把服务注册到注册中心，消费着去注册中心订阅服务，注册中心把服务方的地址通知给消费者，消费者根据信息可以调用服务方的服务，原理就是这么简单。 Demo:https://github.com/bingod/dubbo-demo