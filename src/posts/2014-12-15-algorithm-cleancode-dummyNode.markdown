---
layout: post
title: "Add Two Numbers"
date: 2014-12-15 16:51 +0800
comments: true
categories:
---

##quetions:

You are given two linked lists representing two non-negative numbers. The digits are stored in reverse order and each of their nodes contain a single digit. Add the two numbers and return it as a linked list.

Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)

Output: 7 -> 0 -> 8


<!-- more -->

这个题目并没有什么难度，主要是在追求精致的代码这类题目一个共同点，都是增加一个伪头结点，如Merge Two Sorted List题目。在涉及到链表的操作时候，我们必须首先想到这个方法，它减少了好多判断。还有在设计到两个链表的时候，我们减少多个循环，因为每一个循环体内代码都是类似的，我们可以合并起来不是吗？

改前：

<pre class = "prettyprint">
public class Solution {
    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        ListNode head=new ListNode(0);
        ListNode cur=head,cur1=l1,cur2=l2;
        int carry=0;
        while(cur1!=null&&cur2!=null){
            ListNode tmp=new ListNode((cur1.val+cur2.val+carry)%10);
            carry=(cur1.val+cur2.val+carry)/10;
            cur.next=tmp;
            cur=cur.next;
            cur1=cur1.next;
            cur2=cur2.next;
        }
        while(cur1!=null){
            ListNode tmp=new ListNode((cur1.val+carry)%10);
            carry=(cur1.val+carry)/10;
            cur.next=tmp;
            cur1=cur1.next;
            cur=cur.next;
        }
        while(cur2!=null){
            ListNode tmp=new ListNode((cur2.val+carry)%10);
            carry=(cur2.val+carry)/10;
            cur.next=tmp;
            cur2=cur2.next;
            cur=cur.next;
        }
        if(carry!=0)
        {
            ListNode tmp=new ListNode(carry);
            cur.next=tmp;
        }
        return head.next;

    }
};
</pre>

改后:
<pre class = "prettyprint">
public class Solution {
    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        ListNode dummyNode = new ListNode(0);
        ListNode p1 = l1, p2 = l2, cur = dummyNode;
        int carry = 0;
        while (p1 != null || p2 !=null) {
            int x = (p1 == null) ? 0 : p1.val;
            int y = (p2 == null) ? 0 : p2.val;
            int val = (x + y +carry);
            carry = val / 10;
            cur.next = new ListNode(val % 10);
            p1 = (p1 == null) ? p1 : p1.next;
            p2 = (p2 == null) ? p2 : p2.next;
            cur = cur.next;
        }
        if (carry > 0) cur.next = new ListNode(carry);
        return dummyNode.next;
    }
}
</pre>
