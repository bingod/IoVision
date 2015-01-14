---
layout: post
title: "java nio中的Buffer"
date: 2014-11-18 16:51 +0800
comments: true
categories:
---
java NIO中的Buffer用于和NIO通道进行交互。如你所知，数据是从通道读入缓冲区，从缓冲区写入到通道中的。 缓冲区本质上是一块可以写入数据，然后可以从中读取数据的内存。这块内存被包装成NIO Buffer对象，并提供了一组方法，用来方便的访问该块内存。 为了理解Buffer的工作原理，需要熟悉它的三个属性：
<!-- more -->

capacity 申请的时候固定大小。

position 当你写数据到Buffer中时，position表示当前的位置。初始的position值为0.当一个byte、long等数据写到Buffer后， position会向前移动到下一个可插入数据的Buffer单>元。position最大可为capacity - 1. 当读取数据时，也是从某个特定位置读。当将Buffer从写模式切换到读模式，position会被重置为0. 当从Buffer的position处读取数据时，position向前移动到下一个可读> 的位置。

limit 在写模式下，Buffer的limit表示你最多能往Buffer里写多少数据。 写模式下，limit等于Buffer的capacity。 当切换Buffer到读模式时， limit表示你最多能读到多少数据。因此，当切换Buffer到读模式时，limit会被设置成写模式下的position值。换句话说，你能读到之前写入的> 所有数据（limit被设置成已写数据的数量，这个值在写模式下就是position）

下面我们看看一个例子:

<pre class="prettyprint">
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
public class CopyFile {
    public static void main(String[] args) throws Exception {
        String infile = "." + File.separator + "ck.txt";
        String outfile = "." + File.separator+ "cy.txt";
        String logfile = "." + File.separator + "log.txt";
        // 获取源文件和目标文件的输入输出流
        FileInputStream fin = new FileInputStream(infile);
        FileOutputStream fout = new FileOutputStream(outfile);
        FileOutputStream flog = new FileOutputStream(logfile);
        // 获取输入输出通道
        FileChannel fcin = fin.getChannel();
        FileChannel fcout = fout.getChannel();
        FileChannel fclog = flog.getChannel();
        // 创建缓冲区
        ByteBuffer buffer = ByteBuffer.allocate(8);
        while (true) {
            // clear方法重设缓冲区，使它可以接受读入的数据
            buffer.clear();  //把position设置为0，把limit设置为capacity,limit为第一个不可读写的数，并不是清空数据而是修改索引而已啊
            // 读入数据到buffer,流或通道中的数据读出来，并放到 byte[] 或者 ByteBuffer 中去 ，read隐藏调用buffer里的put方法
            int r = fcin.read(buffer);
            System.out.println(buffer.remaining());//remain剩余的空间，就是position到limit的空间。
           /* while(buffer.hasRemaining()){
                System.out.println("buffer get:" + (char)buffer.get() + buffer.position()); // read 1 byte at a time
           }//这种相对读取position是要移动的，类似绝对读取，buffer.get(1)position是不会移动的。
            // read方法返回读取的字节数，可能为零，如果该通道已到达流的末尾，则返回-1
            if (r == -1) {
                break;
            }
            // flip方法让缓冲区可以将新读入的数据写入另一个通道 ,主要是通过修改buffer里的position和limit值 :使limit=position,position=0
            buffer.flip();
            // 写出buffer里的数据，write 可以理解为将 byte[] 或者 ByteBuffer 中的数据写到流或通道中去,write隐藏调用buffer里的get方法
            fcout.write(buffer);
            buffer.rewind();//把position = 0, limit = limit,重新写一次，写到日志文件。
            fclog.write(buffer);
        }
    }
}
</pre>
该例子主要实现复制一个文件到另一个文件，并备份一份，把ck.txt复制到cy.txt,并在log.txt产生一样的数据。主要引起注意的是当相对读写缓冲区的时候，position是要向后移动的，而绝对读写的时候，position不动。