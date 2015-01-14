---
layout: post
title: "Wildcard Matching"
date: 2014-01-10 16:51 +0800
comments: true
categories:
---

##quetions:



'?' Matches any single character.

'*' Matches any sequence of characters (including the empty sequence).

The matching should cover the entire input string (not partial).

isMatch("aa", "a*") → true

isMatch("ab", "?*") → true

<!-- more -->

这条题目被狠狠的打击到了，看了tag,发现它是backtracking, dynamip program以及greedy,试着前面两种方法都超时间，最后想到了只要以p按*分段，每一段按顺序出现就是对的，除了开头和结尾特殊之外。可是还是不知道该如何写，看了看别人的代码。

递归算法：

<pre class = "prettyprint">
public class Solution {
    public boolean isMatch(String s, String p) {
        if (s.length() == 0 && p.length() == 0) return true;
        if (p.length() == 0) return false;
        if (s.length() == 0 && p.charAt(0) == '') return true;
        if (s.length() == 0 && p.length() != 0) return false;
        if (s.charAt(0) == p.charAt(0) || p.charAt(0) == '?') {
             return isMatch(s.substring(1), p.substring(1));
        }
        if(p.charAt(0) == '') {
            int i = 1;
            while(i < p.length() && p.charAt(i) == '*') i++;
            for (int j = 0; j <= s.length(); j++) {
                if (isMatch(s.substring(j), p.substring(i))) {
                    return true;
                }
            }
        }
        return false;
    }
}
</pre>

动态规划：

<pre class = "prettyprint">
public class Solution {
    public static boolean isMatch(String s, String p) {
        int m = s.length(), n = p.length();
        int k = Math.max(m, n) + 1;
        boolean[][] d = new boolean[k][k];
        for (int i = 0; i < d.length; i++)
            Arrays.fill(d[i], false);
        d[0][0] = true;
        for (int j = 1; j <= n; j++) {
            for (int i = 1; i <= m; i++) {
                if (p.charAt(j - 1) == '*' && (d[i - 1][j] || d[i][j-1])) {
                    d[i][j] = true;
                } else if ((p.charAt(j - 1)=='?' || p.charAt(j-1) == s.charAt(i - 1))
                && d[i - 1][j - 1]) {
                    d[i][j] = true;
                }
            }
        }
        return d[m][n];
    }
}
</pre>

贪婪算法，这是clean code的精髓，你领悟到了吗？
<pre class = "prettyprint">
public class Solution {
    public boolean isMatch(String s, String p) {
        int sp = 0, pp = 0, match = 0,startPre = -1;
        while(sp < s.length()) {
            if (pp < p.length() && (p.charAt(pp) == '?' ||s.charAt(sp) == p.charAt(pp))) {
                sp++;
                pp++;
            } else if (pp < p.length() && p.charAt(pp) == '') {
                startPre = pp;
                match = sp;
                pp++;
            } else if (startPre != -1) {
                pp = startPre + 1;
                match++;
                sp = match;
            } else {
                return false;
            }
        }
        while (pp < p.length() && p.charAt(pp) == '') pp++;
        return pp == p.length();
    }
}
</pre>
