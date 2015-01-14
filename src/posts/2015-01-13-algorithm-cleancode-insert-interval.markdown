---
layout: post
title: "Insert Interval"
date: 2014-01-13 16:51 +0800
comments: true
categories:
---

##quetions:

Given a set of non-overlapping intervals, insert a new interval into the intervals (merge if necessary).

You may assume that the intervals were initially sorted according to their start times.

Example 1:

Given intervals [1,3],[6,9], insert and merge [2,5] in as [1,5],[6,9].

Example 2:

Given [1,2],[3,5],[6,7],[8,10],[12,16], insert and merge [4,9] in as [1,2],[3,10],[12,16].

This is because the new interval [4,9] overlaps with [3,5],[6,7],[8,10].

<!-- more -->

题目并没有难度，可是就是比较难以处理，都有思想，就是如何减少比较次数，如果能够做到clean code确实有难度

<pre class = "prettyprint">
public class Solution {
    public List insert(List intervals, Interval newInterval) {
        List list = new LinkedList();
        for (int i = 0; i < intervals.size(); i++) {
            if (newInterval.start > intervals.get(i).end) {
                list.add(intervals.get(i));
            } else if (newInterval.end < intervals.get(i).start) {
                list.add(newInterval);
                newInterval = intervals.get(i);
            } else {
                newInterval.start = Math.min(newInterval.start, intervals.get(i).start);
                newInterval.end = Math.max(newInterval.end, intervals.get(i).end);
            }
        }
        list.add(newInterval);
        return list;
    }
}
</pre>