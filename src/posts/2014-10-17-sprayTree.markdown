---
layout: post
title: "伸展树"
date: 2014-10-17 16:51 +0800
comments: true
categories:
---

##自顶向下的伸展树：

在自底向上的伸展树中，我们需要求一个节点的父节点和祖父节点，因此这种伸展树难以实现。因此，我们可以构建自顶向下的伸展树。 当我们沿着树向下搜索某个节点X的时候，我们将搜索路径上的节点及其子树移走。我们构建两棵临时的树──左树和右树。没有被移走的节点构成的树称作中树。在伸展操作的过程中：

1、当前节点X是中树的根。

2、左树L保存小于X的节点。

3、右树R保存大于X的节点。

开始时候，X是树T的根，左右树L和R都是空的。和前面的自下而上相同，自上而下也分三种情况： 将中树的左右子树分别连接到左树的右子树和右树的左子树上。将左右树作为X的左右子树。重新最成了一所查找的节点为根的树。 下面给出伪代码：

右连接：将当前根及其右子树连接到右树上。左子结点作为新根。

左连接：将当前根及其左子树连接到左树上。右子结点作为新根。

<!-- more -->

<pre class="prettyprint">
Function Top-Down-Splay
           Do
              If X 小于 T Then
                   If X 小于 T 的左孩子 Then
                     T的左子节点绕T右旋
                   EndIf

                右连接
              Else If X大于 T Then
                   If X 大于 T 的右孩子 Then
                     T的右子节点绕T左旋
                   EndIf
               左连接
             EndIf
           While  !(找到 X或遇到空节点)
           组合左中右树
         EndFuntion
</pre>

<pre class="prettyprint">

8 int size;  /* number of nodes in the tree */
  9            /* Not actually needed for any of the operations */
 10 typedef struct tree_node Tree;
 11  struct tree_node
 12 {
 13     Tree * left, * right;
 14     int item;
 15 };
 16
 17 Tree * splay (int i, Tree * t)
 18 {
 19  /* Simple top down splay, not requiring i to be in the tree t.  */
 20  /* What it does is described above.                             */
 21     Tree N, *l, *r, *y;
 22     if (t == NULL)
 23         return t;
 24     N.left = N.right = NULL;
 25     l = r = &N;
 26     for (;;)
 27     {
 28         if (i < t->item)
 29         {
 30             if (t->left == NULL)
 31             {
 32                 break;
 33             }
 34             if (i < t->left->item)
 35             {
 36                 y = t->left;                           /* rotate right */
 37                 t->left = y->right;
 38                 y->right = t;
 39                 t = y;
 40                 if (t->left == NULL)
 41                 {
 42                     break;
 43                 }
 44             }
 45             r->left = t;                               /* link right */
 46             r = t;
 47             t = t->left;
 48         }
 49         else if (i > t->item)
 50         {
 51             if (t->right == NULL)
 52             {
 53                 break;
 54             }
 55             if (i > t->right->item)
 56             {
 57                 y = t->right;                          /* rotate left */
 58                 t->right = y->left;
 59                 y->left = t;
 60                 t = y;
 61                 if (t->right == NULL)
 62                 {
 63                     break;
 64                 }
 65             }
 66             l->right = t;                              /* link left */
 67             l = t;
 68             t = t->right;
 69         }
 70         else
 71         {
 72             break;
 73         }
 74     }
 75     l->right = t->left;                                /* assemble */
 76     r->left = t->right;
 77     t->left = N.right;
 78     t->right = N.left;
 79     return t;
 80 }
</pre>

这主要是在查找伸展结点的时候，把找到到结点放到根结点中，因为这是最近访问的结点，后面很可能再次访问到！
