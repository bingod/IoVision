---
layout: post
title: "java nio中的Selector"
date: 2014-11-19 16:51 +0800
comments: true
categories:
---

Selector（选择器）是Java NIO中能够检测一到多个NIO通道，并能够知晓通道是否为诸如读写事件做好准备的组件。这样，一个单独的线程可以管理多个channel，从而 管理多个网络连接。以前socketserver都会生成多个线程来对应不同的连接，由于产生大量的线程，线程切换又占有很大的计算机资源，而用到nio就可以避免这个问题
<!-- more -->

注意register()方法的第二个参数。这是一个“interest集合”，意思是在通过Selector监听Channel时对什么事件感兴趣。可以监听四种不同类型的事件：

SelectionKey.OP_READ = 1;

SelectionKey.OP_WRITE = 4;

SelectionKey.OP_CONNECT = 8;

SelectionKey.OP_ACCEPT = 16;

通道触发了一个事件意思是该事件已经就绪。所以，某个channel成功连接到另一个服务器称为“连接就绪”。一个server socket channel准备好接收新进入的连接称为“接 收就绪”。一个有数据可读的通道可以说是“读就绪”。等待写数据的通道可以说是“写就绪”

下面我们看看一个例子:

<pre class="prettyprint">
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.SelectionKey;
import java.nio.channels.Selector;
import java.nio.channels.SocketChannel;
import java.util.Iterator;
/**
 * 多个SocketChannel注册Selector。
 *
 */
public class SocketChannelSelector {
  public static SocketChannel createSocketChannel(String hostName, int port)
      throws IOException {
    SocketChannel sChannel = SocketChannel.open();
    sChannel.configureBlocking(false);//如果为 false，则此通道将被置于非阻塞模式
    sChannel.connect(new InetSocketAddress(hostName, port));
    return sChannel;
  }
  // 2个连接注册的选择器关键字
  static SelectionKey key1;
  static SelectionKey key2;
  public static void main(String[] args) {
    // 1个选择器，注册2个Socket 通道
    Selector selector = null;
    try {
      // 创建选择器
      selector = Selector.open();
      // 创建2个通道
      SocketChannel sChannel1 = createSocketChannel("mail.bupt.edu.cn", 25);
      SocketChannel sChannel2 = createSocketChannel("mail.csdn.net", 25);
      // 注册选择器，侦听所有的事件
      key1 = sChannel1.register(selector, sChannel1.validOps());
      key2 = sChannel2.register(selector, sChannel2.validOps());
    } catch (IOException e) {
    }
    // 等待事件的循环
    while (true) {
      try {
        // 等待
        selector.select();//阻塞到至少有一个通道在你注册的事件上就绪了
      } catch (IOException e) {
        break;
      }
      // 所有事件列表
      Iterator it = selector.selectedKeys().iterator();
      // 处理每一个事件
     while (it.hasNext()) {
        // 得到关键字
        SelectionKey selKey = it.next();
        // 删除已经处理的关键字
        it.remove();
        try {
          // 处理事件
          processSelectionKey(selKey);
        } catch (IOException e) {
          // 处理异常
          selKey.cancel();
        }
      }
    }
  }
  public static void processSelectionKey(SelectionKey selKey) throws IOException {
    ByteBuffer buf = ByteBuffer.allocateDirect(1024);
    // 确认连接正常
    if (selKey.isValid() && selKey.isConnectable()) {
      // 得到通道
      SocketChannel sChannel = (SocketChannel) selKey.channel();
      // 是否连接完毕？
      boolean success = sChannel.finishConnect();
      if (!success) {
        // 异常
        selKey.cancel();
      }
    }
    // 如果可以读取数据
    if (selKey.isValid() && selKey.isReadable()) {
      // 得到通道
      SocketChannel sChannel = (SocketChannel) selKey.channel();
      if (sChannel.read(buf) > 0) {
        // 转到最开始
        buf.flip();
        while (buf.remaining() > 0) {
          System.out.print((char) buf.get());
        }
        // 也可以转化为字符串，不过需要借助第三个变量了。
        // buf.get(buff, 0, numBytesRead);
        // System.out.println(new String(buff, 0, numBytesRead, "UTF-8"));
        // 复位，清空
        buf.clear();
      }
    }
// 如果可以写入数据
    if (selKey.isValid() && selKey.isWritable()) {
      // 得到通道
      SocketChannel sChannel = (SocketChannel) selKey.channel();
      // 区分2个侦听器的关键字
      // 我这里只写一次数据。
      if (!s1 && key1.equals(selKey)) {
        System.out.println("channel1 write data..");
        buf.clear();
        buf.put("HELO localhost\n".getBytes());
        buf.flip();
        sChannel.write(buf);
        s1 = true;
      } else if (!s2 && key2.equals(selKey)) {
        System.out.println("channel2 write data..");
        buf.clear();
        buf.put("HELO localhost\n".getBytes());
        buf.flip();
        sChannel.write(buf);
        s2 = true;
      }
    }
  }
  // 判断已经写过数据的标志
  static boolean s1 = false;
  static boolean s2 = false;
}
</pre>

该例子主要用selector管理两个通道，一个是连接北邮邮箱的SocketChannel，另一个是连接csdn的邮箱，连接成功后，读取返回的数据，并向通道写入数据，接受返回的结>果。可以打开cmd:输入telnet mail.bupt.edu.cn 25测试看看，是否能连接。由于该例子比较通俗明了，是分析selector特别好的例子。其实选择器类似于指挥员，而每一次指挥员指挥一组人员>（规定10个左右）而人员来自于几个通道A,B,C，他们又有不同的目的，而指挥员可以监听他们的想法，假如A通道的人现在已经人满十个了，它就会告诉指挥员这组人数已经 够，你赶快带我们走吧，指挥人员听到消息马上去处理。所以要和selector使用的通道必须是非阻塞的通道。附有同步，异步和阻塞，非阻塞（阻塞非阻塞：是指某执行函数 、过程是否立刻返回。也就是程序调用某个函数是否立刻返回。同步异步是站在程序的视角看的，同步是有次序不可随意划分颠倒的，异步次序不是固定的）