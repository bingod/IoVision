---
layout: post
title: "mina简易教程"
date: 2014-11-19 16:51 +0800
comments: true
categories:
---

Apache MINA是一个网络应用程序框架，用来帮助用户简单地开发高性能和高可扩展性的网络应用程序。它提供了一个通过Java NIO在不同的传输例如TCP/IP和UDP/IP上抽象的事件驱动的异步API

<!-- more -->

I/O 服务：I/O 服务用来执行实际的 I/O 操作。 IoAccepter 相当于网络应用程序中的服务器端 IoConnector 相当于客户端

I/O 处理器：I/O 处理器用来执行具体的业务逻辑。对接收到的消息执行特定的处理。 IoHandler 业务处理逻辑

I/O 过滤器：I/O 服务能够传输的是字节流，而上层应用需要的是特定的对象与数据结构。I/O 过滤器用来完成这两者之间的转换。I/O 过滤器的另外一个重要作用是对输入输出的数据进行处理，满足横切的需求。多个 I/O 过滤器串联起来，形成 I/O 过滤器链。 IoFilter 过滤器用于悬接通讯层接口与业务层接口

IoSession 当前客户端到服务器端的一个连接实例

IoService->IoProcessor->IoFilter->IoFilter...->IoHandler

IoService<-IoProcessor<-IoFilter<-IoFilter...<-IoHandler

IoService 便是应用程序的入口，IoAccepter 便是 IoService 的一个扩展接口。IoService 接口可以用来添加多个 IoFilter，这些 IoFilter 符合责任链模式并由 IoProcessor 线程负责调用。 IoHandler，这便是业务处理模块。在业务处理类中不需要去关心实际的通讯细节，只管处理客户端传输过来的信息即可。编写 Handler 类就是使用 MINA 开发网络应用程序的重心所在，相当于 MINA 已经帮你处理了所有的通讯方面的细节问题

<pre class="prettyprint">
public class CalculatorServer {
    private static final int PORT = 10010;

    private static final Logger LOGGER = LoggerFactory
        .getLogger(CalculatorServer.class);

    public static void main(String[] args) throws IOException {
        IoAcceptor acceptor = new NioSocketAcceptor();

        acceptor.getFilterChain().addLast("logger", new LoggingFilter());
        acceptor.getFilterChain().addLast(
            "codec",
            new ProtocolCodecFilter(new TextLineCodecFactory(Charset
                .forName("UTF-8"))));

        acceptor.setHandler(new CalculatorHandler());
        acceptor.bind(new InetSocketAddress(PORT));
        LOGGER.info("计算器服务已启动，端口是" + PORT);
    }
 }
</pre>

<pre class="prettyprint">
 public class CalculatorHandler extends IoHandlerAdapter {
    private static final Logger LOGGER = LoggerFactory
        .getLogger(CalculatorHandler.class);

    private ScriptEngine jsEngine = null; //

    public CalculatorHandler() {
        ScriptEngineManager sfm = new ScriptEngineManager();
        jsEngine = sfm.getEngineByName("JavaScript");
        if (jsEngine == null) {
            throw new RuntimeException("找不到 JavaScript 引擎。");
        }
    }

    public void exceptionCaught(IoSession session, Throwable cause)
        throws Exception {
        LOGGER.warn(cause.getMessage(), cause);
    }
    //消息来到的时候处罚该方法,message为接受到的信息
    @Override
    public void messageReceived(IoSession session, Object message)
        throws Exception {
        String expression = message.toString();
        if ("quit".equalsIgnoreCase(expression.trim())) {
            session.close(true);
            return;
        }
        try {
            Object result = jsEngine.eval(expression);
            session.write(result.toString());
        } catch (ScriptException e) {
            LOGGER.warn(e.getMessage(), e);
            session.write("Wrong expression, try again.");
        }
    }
    //message的值为要发送给客户端的信息。
    @Override
    public void messageSent(IoSession session, Object message) {
        System.out.println("当信息已经传送给客户端后触发此方法" + message.toString());
    }
    @Override
    public void sessionClosed(IoSession session) {
        System.out.println("客户端关闭连接时候出发此方法");
    }
    @Override
    public void sessionIdle(IoSession session, IdleStatus status) {
        System.out.println("连接空闲的时候触发此方法：" + status);

    }
 }
</pre>