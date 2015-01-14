---
layout: post
title: "Jump Game II"
date: 2014-01-11 16:51 +0800
comments: true
categories:
---

##quetions:

quetions:

Given an array of non-negative integers, you are initially positioned at the first index of the array.

Each element in the array represents your maximum jump length at that position.

Your goal is to reach the last index in the minimum number of jumps.

For example:

Given array A = [2,3,1,1,4]

The minimum number of jumps to reach the last index is 2. (Jump 1 step from index 0 to 1, then 3 steps to the last index.)

<!-- more -->

贪心算法（又称贪婪算法）是指，在对问题求解时，总是做出在当前看来是最好的选择。也就是说，不从整体最优上加以考虑，他所做出的仅是在某种意义上的局部最优解。贪心算法不是对所有问题都能得到整体最优解，但对范围相当广泛的许多问题他能产生整体最优解或者是整体最优解的近似解。该题目就是从头开始，跳跃一步所能到最远的距离，跳两步能走的最远距离……以此类推

递归算法：

<pre class = "prettyprint">
public class Solution {
    public int jump(int[] A) {
        int maxJump = 0, i = 0;
        int step = 0;
        while (maxJump < A.length - 1) {//当maxJump能够着末尾就不用跳了
            int preMax = -1;
            while (i <= maxJump) {
                preMax = Math.max(preMax, i + A[i]);
                i++;
            }
            maxJump = preMax;
            step++;
        }
        return step;
    }
}
</pre>