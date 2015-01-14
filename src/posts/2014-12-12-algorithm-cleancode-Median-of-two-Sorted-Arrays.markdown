---
layout: post
title: "Median of Two Sorted Arrays"
date: 2014-12-12 16:51 +0800
comments: true
categories:
---

##quetions:

here are two sorted arrays A and B of size m and n respectively. Find the median of the two sorted arrays. The overall run time complexity should be O(log (m+n))

<!-- more -->

在追求问题解答的同时，追求极其简单精致的代码是以后努力的方向，好久没来leetcode了，当看到这题目的时候真心想不起来该怎么做，在要求log(m+n)的复杂度一定要想到二分法，以下代码具体普遍适用性，不仅可以求得中位数，还可以求得第K大的数，在求第K大的数的时候例如A={1,4,8,10,13,15,18},B= {2,5,7,9,20,21,29}我们在求第9大的数的时候，A[9/2 - 1] = 10, B[9 -(9/2) -1] =20,10 < 20,所以1，4，8，10都是比第9大的数还要小，所以直接减去这四个数，下次迭代求第5大的数。

<pre class = "prettyprint">
public class Solution {
    public double findKLarge(int[] A, int beginA, int[] B, int beginB, int k) {
        int lenA = A.length - beginA, lenB= B.length - beginB;
        if (lenA > lenB) return findKLarge(B, beginB, A, beginA, k);
        if (lenA == 0) return B[beginB + k -1];
        if (k == 1) return Math.min(A[beginA], B[beginB]);
        int p = Math.min(k/2, lenA);
        int pA = beginA + p, pB = beginB + k -p;
        if (A[pA -1] < B[pB - 1]) {
            return findKLarge(A, beginA +p, B, beginB, k - p);
        } else if (A[pA - 1] > B[pB - 1]) {
            return findKLarge(A, beginA, B, beginB + k - p, p);
        } else {
            return A[pA - 1];
        }
    }

    public double findMedianSortedArrays(int A[], int B[]) {
        int total = A.length + B.length;
        if (total % 2 == 1) {
            return findKLarge(A, 0, B, 0,total / 2 + 1);
        } else {
            return (findKLarge(A, 0, B, 0 ,total / 2)
                    + findKLarge(A, 0, B, 0,total / 2 + 1)) / 2;
        }

    }
}
</pre>
