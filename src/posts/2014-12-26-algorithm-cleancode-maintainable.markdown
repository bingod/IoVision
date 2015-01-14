---
layout: post
title: "Valid Parenthese"
date: 2014-12-26 16:51 +0800
comments: true
categories:
---

##quetions:

Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

The brackets must close in the correct order, "()" and "()[]{}" are all valid but "(]" and "([)]" are not.

<!-- more -->

当我们拿到这条题目的时候我们都有想法，无非就是借助一个栈来操作，当进来左括号进栈，右括号时，弹出，但是正常的思维我们都要作出很多的判断语句，当要增加别的括号的时候，造成代码非常混乱，我们可以借助一个字典，写出可维护代码！！！

<pre class = "prettyprint">
public class Solution {
    private Map map = new HashMap() {
    {
        put('(', ')');
        put('[', ']');
        put('{', '}');
    }};

    public boolean isValid(String s) {
        Stack stack = new Stack();
        for (Character c : s.toCharArray()) {
            if (map.containsKey(c)) {
                stack.push(c);
            } else if (stack.isEmpty() || map.get(stack.pop()) != c) {
                return false;
            }
        }
        return stack.isEmpty();
    }
}
</pre>
