---
title: Tree sort writes a sorted permutation of the input, stably
proves: [correctness]
status: full
---

We call a binary tree whose nodes hold items *ordered* when for each node $v$, each item in the left subtree of $v$ is less than $v.key$, and no item in the right subtree of $v$ is less than $v.key$.

**Lemma 1 (insert).** If $T$ is ordered, then after INSERT$(T, x)$ the tree is ordered and holds the items of $T$ and $x$.

*Proof.* INSERT does not change the existing nodes or links; it adds one leaf. Let $v_0, v_1, \ldots, v_d$ be the nodes on the path from the root, where the new leaf $u$ becomes a child of $v_d$. At each $v_j$, the walk goes left when $x < v_j.key$ and right otherwise. So for each $j$, $u$ is in the left subtree of $v_j$ exactly when $x < v_j.key$, which is the condition for $v_j$. The nodes that are not on the path do not have $u$ in their subtrees. So each node still meets the condition. $\square$

**Lemma 2 (inorder).** The inorder traversal of an ordered tree lists its items in non-decreasing order.

*Proof.* By induction on the number of nodes. The empty tree gives an empty list. For a root $r$ with subtrees $L$ and $R$, both are ordered, so by the hypothesis the traversal lists $L$ in order, then $r$, then $R$ in order. Each item of $L$ is less than $r.key$, and no item of $R$ is less than $r.key$. So the full list is non-decreasing. $\square$

**Theorem 1.** After TREE-SORT$(A)$, the array $A$ holds the items of the input in non-decreasing order.

*Proof.* The empty tree is ordered. By Lemma 1 and induction on $i$, after the loop of lines L2 and L3 the tree is ordered and holds each item of the input once. By Lemma 2, lines L5 and L6 visit its $n$ items in non-decreasing order and write them into $A[0 \ldots n-1]$. $\blacksquare$

**Theorem 2 (stability).** If $A[i]$ and $A[j]$ have equal keys and $i < j$, then $A[i]$ is written before $A[j]$.

*Proof.* The node of $A[j]$ is added after the node of $A[i]$, as a new leaf, and nodes are never moved. So the node of $A[j]$ is not an ancestor of the node of $A[i]$. There are two cases.

If the node of $A[i]$ is an ancestor of the node of $A[j]$, the walk of $A[j]$ passed it. There $A[j] < A[i]$ is false, because the keys are equal, so the walk went right. So $A[j]$ is in the right subtree of $A[i]$, which inorder visits after $A[i]$.

Otherwise, let $w$ be the lowest common ancestor of the two nodes; it is a third node, and the two items are in different subtrees of $w$. But both walks passed $w$, and the test $x < w.key$ has the same result for two items with equal keys, so both went to the same side. This is a contradiction, so this case does not occur. $\blacksquare$

**Termination.** Each insert walks down a path of a finite tree and stops at an empty place, and the traversal visits each of the $n$ nodes once.
