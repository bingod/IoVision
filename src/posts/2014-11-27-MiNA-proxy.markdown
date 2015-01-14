---
layout: post
title: "mina写一个简易的代理服务器"
date: 2014-11-20 16:51 +0800
comments: true
categories:
---

在分析MINA框架的过程中，分析一个代理服务器的代码，为了使自己后面不忘记，也写下了几行注释，希望自己能够爱上代码吧，嘿嘿！
<!-- more -->
可以用上一篇文章写的代码充当服务器的角色，并修改代码里面的端口

<pre class="prettyprint">
public abstract class AbstractProxyIoHandler extends IoHandlerAdapter {
    private static final Charset CHARSET = Charset.forName("UTF-8");
    public static final String OTHER_IO_SESSION = AbstractProxyIoHandler.class.getName()+".OtherIoSession";

    private final Logger logger = LoggerFactory.getLogger(getClass());

    @Override
    public void sessionCreated(IoSession session) throws Exception {
        session.suspendRead();
        session.suspendWrite();
    }

    @Override
    public void sessionClosed(IoSession session) throws Exception {
        if (session.getAttribute( OTHER_IO_SESSION ) != null) {
            IoSession sess = (IoSession) session.getAttribute(OTHER_IO_SESSION);//获得另一个会话
            sess.setAttribute(OTHER_IO_SESSION, null);
            sess.close(false);
            session.setAttribute(OTHER_IO_SESSION, null);//注意顺序如果把自己的会话首先删除了，就没法关闭相对的会话
        }
    }

    @Override
    public void messageReceived(IoSession session, Object message)
            throws Exception {

        IoBuffer rb = (IoBuffer) message;
        System.out.println(rb.getChar(2));
        IoBuffer wb = IoBuffer.allocate(rb.remaining());
        rb.mark();
        wb.put(rb);
        wb.flip();
        //把接收的数据转发给另一个会话
        ((IoSession) session.getAttribute(OTHER_IO_SESSION)).write(wb);
        rb.reset();
        logger.info(rb.getString(CHARSET.newDecoder()));
    }
}
</pre>

<pre class="prettyprint">
public class ClientToProxyIoHandler extends AbstractProxyIoHandler {

    private final ServerToProxyIoHandler connectorHandler = new ServerToProxyIoHandler();
    private final IoConnector connector;

    private final SocketAddress remoteAddress;

    public ClientToProxyIoHandler(IoConnector connector,
            SocketAddress remoteAddress) {
        this.connector = connector;
        this.remoteAddress = remoteAddress;//服务器的地址:端口
        connector.setHandler(connectorHandler);//设置连接器的业务处理函数
    }

    //当客户端连接到代理服务时候（新的连接打开的时候），触发该方法
    @Override
    public void sessionOpened(final IoSession session) throws Exception {

        connector.connect(remoteAddress).addListener(new IoFutureListener() {
            public void operationComplete(ConnectFuture future) {
                try {
                    future.getSession().setAttribute(OTHER_IO_SESSION, session);
                    System.out.println("1:"+session);
                    //(0x00000001: nio socket, server, /127.0.0.1:51292 => /127.0.0.1:8474)
                    session.setAttribute(OTHER_IO_SESSION, future.getSession());

                    System.out.println("2:"+future.getSession());
                    //2:(0x00000002: nio socket, client, /10.108.115.121:42706 => /10.108.115.108:8989)
                    IoSession session2 = future.getSession();
                    session2.resumeRead();
                    session2.resumeWrite();
                } catch (RuntimeIoException e) {
                    session.close(true);
                } finally {
                    session.resumeRead();
                    session.resumeWrite();
                }
            }
        });
    }
}
</pre>

<pre class="prettyprint">
public class ServerToProxyIoHandler extends AbstractProxyIoHandler {
}
</pre>

<pre class="prettyprint">
public class Main {

    public static void main(String[] args) throws Exception {

        // Create TCP/IP acceptor.
        NioSocketAcceptor acceptor = new NioSocketAcceptor();//代理服务器的接收器，接受本地的请求连接

        // Create TCP/IP connector.
        IoConnector connector = new NioSocketConnector();//代理服务器连接器，要连到服务器，它也应该有一个handler

        // Set connect timeout.
        connector.setConnectTimeoutMillis(30*1000L);

        ClientToProxyIoHandler handler = new ClientToProxyIoHandler(connector,
                new InetSocketAddress("10.108.115.108", 8989));

        // Start proxy.
        acceptor.setHandler(handler);

        acceptor.setReuseAddress(true);

        acceptor.bind(new InetSocketAddress(8474));

    }
}
</pre>