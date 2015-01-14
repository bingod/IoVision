---
layout: post
title: "java并发编程基础"
date: 2014-11-10 16:51 +0800
comments: true
categories:
---
对于java多线程的基础代码，我们常常会看到每个对象都自带有wait(),nodify()方法，所以这些方法是在基础类里面的，也就是说每个对象都有。它不属于Thread类里面的。 wait():如果对象调用了这个函数，会迫使持有该对象的线程把对象的控制权交出去，然后该线程处于等待状态（该线程等待拿到对象的控制权），这种等待是被动的，你需要别人来唤醒

<!-- more -->

sleep():如果线程调用了这个函数，是线程本身调用，这是主动睡眠，时间一到，立马醒来

nodify():如果对象调用了这个函数，就会通知某个正在等待该对象的控制权的线程，使被通知的线程立马醒过来，继续工作，而通知线程继续往下执行。

下面我们看看常见的生产者和消费者模式。



<pre class="prettyprint">
public class WaitNotify {
    public static void main(String[] args) {
        Q q = new Q();
        Producer p = new Producer(q);
        Consumer c = new Consumer(q);
        new Thread(p).start();
        new Thread(c).start();
    }
}
class Producer implements Runnable {
    Q q = null;
    public Producer(Q q) {
        this.q = q;
    }
    @Override
    public void run() {
        int i = 0;
        while(i<5) {
            q.put(i++);
        }
    }
}
class Consumer implements Runnable {
    Q q = null;
    public Consumer(Q q) {
        this.q = q;
    }
    @Override
    public void run() {
        while(q.get()<5){
        }
    }
}
class Q {
    int n;
    boolean valueSet = false;
    public synchronized int get() {
        if(!valueSet) {     // if valueSet == false,wait else try to got value
            try {
                this.wait();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        System.out.println("Get n : " + n);
        valueSet = false;
        this.notify();
        return n;
    }
    public synchronized void put(int n) {
        if(valueSet) {      // if valueSet == true,already have value so wait fetch,else put
            try {
                System.out.println("wait释放的控制权马上生效：");
                this.wait();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
        this.n = n;
        System.out.println("Put n : " + n);
        valueSet = true;
        notify();
        try {
        Thread.sleep(1000);
        System.out.println("肯定先打印出这条语句，然后再印消费者读到的数据,这说明notify释放的控制权不是马上有效，而是等到synchronized语句执行完");
        Thread.sleep(1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
</pre>

程序输出：

Put n : 0

肯定先打印出这条语句，然后再印消费者读到的数据,这说明notify释放的控制权不是马上有效，而是等到synchronized语句执行完

wait释放的控制权马上生效：

Get n : 0

Put n : 1

肯定先打印出这条语句，然后再印消费者读到的数据,这说明notify释放的控制权不是马上有效，而是等到synchronized语句执行完

wait释放的控制权马上生效：

Get n : 1

生产者和消费者进程都轮流占有q对象的控制权，一个对它写，一个对他读，当消费者进程执行对象的get函数，如果valueSet==false,还没设置值，则消费者进程把该对象的控制权交出去，继续等待，生产者从而获得q对象的控制权，它发现valueSet==false,则它设置值，并唤醒因为对象q而等待的消费者进程，同时生产者继续往下执行，如果消费者进程还没来得及读取数据，则生产者先睡吧。还有要注意的就是控制权释放的时候生效的时间的问题，当你要释放控制权，去唤醒他人的时候，这一段时间间隔你必须执行完自己的东西，synchronized修饰的语句某一个时刻时能有一个进程执行，你不执行完，万一下面你还要对该对象操作，而控制权已经交出去那不完蛋了。而wait不同，一旦wait原来的进程就真睡了，什么也不做，所以立即生效可以理解，不会造成冲突。