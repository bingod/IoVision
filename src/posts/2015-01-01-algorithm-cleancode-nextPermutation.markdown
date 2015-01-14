---
layout: post
title: "Next Permutation"
date: 2014-01-02 16:51 +0800
comments: true
categories:
---

##quetions:

Implement next permutation, which rearranges numbers into the lexicographically next greater permutation of numbers.

If such arrangement is not possible, it must rearrange it as the lowest possible order (ie, sorted in ascending order).

The replacement must be in-place, do not allocate extra memory.

Here are some examples. Inputs are in the left-hand column and its corresponding outputs are in the right-hand column.

<!-- more -->
于是可以有下面计算下一个排列的算法：

设P是1～n的一个全排列:p=p1p2......pn=p1p2......pj-1pjpj+1......pk-1pkpk+1......pn

1）从排列的右端开始，找出第一个比右边数字小的数字的序号j（j从左端开始计算），即 j=max{i|pi<pi+1}

2）在pj的右边的数字中，找出所有比pj大的数中最小的数字pk，即 k=max{i|pi>pj}（右边的数从右至左是递增的，因此k是所有大于pj的数字中序号最大者）

3）对换pi，pk

4）再将pj+1......pk-1pkpk+1......pn倒转得到排列p'=p1p2.....pj-1pjpn.....pk+1pkpk-1.....pj+1，这就是排列p的下一个排列。

<pre class = "prettyprint">
public class Solution {
    private void reverse(int[] num, int begin, int end) {
        while (begin < end) {
            int t = num[begin];
            num[begin] = num[end];
            num[end] = t;
            begin++; end--;
        }
    }
    public void nextPermutation(int[] num) {
        int firstLSR = Integer.MAX_VALUE; // first left small right
        for (int j = num.length -2; j >= 0; j--) {
            if (num[j] < num[j + 1]) {
                firstLSR = j; break;
            }
        }
        if (firstLSR == Integer.MAX_VALUE) {
            reverse(num, 0, num.length - 1);
            return;
        }
        int lfirstLSR = 0; // large than num[firstLSR] form right to left
        for (int j = num.length - 1; j > firstLSR; j--) {
            if (num[j] > num[firstLSR]) {
                lfirstLSR = j; break;
            }
        }
        int t = num[firstLSR];
        num[firstLSR] = num[lfirstLSR];
        num[lfirstLSR] = t;
        reverse(num, firstLSR + 1, num.length - 1);
    }
}
</pre>
