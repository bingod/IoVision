---
layout: post
title: "First Missing Positive"
date: 2014-01-6 16:51 +0800
comments: true
categories:
---

##quetions:

Given an unsorted integer array, find the first missing positive integer.

For example:

Given [1,2,0] return 3,

and [3,4,-1,1] return 2.

Your algorithm should run in O(n) time and uses constant space.

<!-- more -->

这是我做leetcode真正值得我铭记的一条题目，当我拿到这条题目的时候，看到题目的条件真的无从下手，但是最后我还是想到了这个解法，这是唯一做过后不想去看别人代码的一条题目，所以第二次碰到后，真的很想把它留下来，这是看似简单的题目，隐藏下深刻的思想，思维跳跃，因为我们需要思维跳跃，来证明我们还没那么笨。

<pre class = "prettyprint">
public class Solution {
    public int firstMissingPositive(int[] A) {
        for (int i = 0; i < A.length; i++) {
            if (A[i] == 0) A[i] = -1;
        }
        for (int i = 0; i < A.length; i++) {
            int p = A[i];
            while (p > 0 && p <= A.length) {
                int t = A[p - 1];
                A[p -1] = 0;
                p = t;
            }
        }
        for (int i = 0; i < A.length;i++) {
            if (A[i] != 0) return i + 1;
        }
        return A.length + 1;
    }
}
</pre>
