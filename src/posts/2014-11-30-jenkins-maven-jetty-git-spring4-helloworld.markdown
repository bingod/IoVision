---
layout: post
title: "java项目的自动化构建"
date: 2014-11-30 16:51 +0800
comments: true
categories:
---

Jenkins，之前叫做Hudson，是基于Java开发的一种持续集成工具，用于监控持续重复的工作，包括：持续的软件版本发布/测试项目。

<!-- more -->

maven,Maven是基于项目对象模型(POM)，可以通过一小段描述信息来管理项目的构建，报告和文档的软件项目管理工具。

spring4,我们都很熟悉，利用它来开发java web项目。

git,用于版本控制。
经过这两天的实验，发现java项目的自动化构建好处颇多。首先在eclips里建立java web程序（http://blog.csdn.net/smilevt/article/details/8215558），以前要集成spring4的时候，还要手动去下载jar。而现在由于建立的是maven程序，只要在pom.xml里填写程序依赖的很多框架，当启动mvn compile的时候，自动下载所依赖的一些开发框架。 当建立好程序的时候，我们去根目录启动程序（mvn compie ;mvn package;mvn test;mvn jetty:run;)这样就完成程序的开发流程。可是这还远远不够，设计到多人开发的时候，代码合并，项目总经理每次合并提交后都不断的测试，而微小的改变，对于大型的项目要运行起来就会特别费劲，每次测试所需要的时间也特别长。这时候jenkins出现了，jenkins可以替代我们完成很多工作。当我们把代码提交到github或者gitLab上，我们可以在另一台超级服务器部署jenkins，每一次构建，jenkins自动从github上clone最新版本代码，并自动完成java程序的编译，打包，运行。一个简单的helloworld web源代码地址：（https://github.com/bingod/webspring4）