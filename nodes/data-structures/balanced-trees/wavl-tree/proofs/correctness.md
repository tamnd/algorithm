---
title: WAVL insertion and deletion keep the rank rules
proves: [correctness]
status: full
---

Each node $x$ has an integer rank $r(x)$, with $r(\text{nil}) = -1$. For a child $x$ of $p$, the *rank difference* is $\delta(x) = r(p) - r(x)$. A node whose children have rank differences $i$ and $j$ is an $i,j$ node. The tree is a *WAVL tree* when:

1. (W1) it is a binary search tree;
2. (W2) every rank difference is 1 or 2;
3. (W3) every leaf has rank 0.

A rotation keeps the in-order sequence of the keys and so keeps (W1); we only check (W2) and (W3) at the nodes whose children or ranks change. If a node $x$ takes the place of $p$ with the rank $p$ had, the rank difference of that place toward the parent of $p$ is unchanged. Two facts follow from the rules: a node that is not a leaf has rank at least 1, and a node with exactly one child has rank 1, with a leaf child (difference 1) and a nil child (difference 2).

## Insertion

Lines L1 to L6 first add a leaf $x$ of rank 0 as in a binary search tree. Before, its place held nil, with difference $r(p) + 1 \in \{1, 2\}$, so $r(p) \in \{0, 1\}$. If $r(p) = 1$, now $\delta(x) = 1$ and all rules hold. If $r(p) = 0$, then $\delta(x) = 0$.

**Invariant at line L2.** (W1) and (W3) hold, and (W2) holds except that $\delta(x)$ may be 0. If $\delta(x) = 0$, then either $x$ is a new leaf, whose parent was a leaf, or $x$ is a 1,2 node whose child of difference 1 is the previous $x$.

**Promotion (line L3).** Let $\delta(x) = 0$ and let $s$ be the sibling of $x$, with $\delta(s) = 1$. Promoting $p$ makes $\delta(x) = 1$ and $\delta(s) = 2$, so $p$ is a 1,2 node whose difference-1 child is $x$, and $p$ is not a leaf. Only $\delta(p)$ drops by one, to 0 or 1. So the invariant holds with $x \leftarrow p$. A new leaf $x$ always takes this case: its parent $p$ has rank 0, so $p$ was a leaf, $s$ is nil, and $\delta(s) = 0 - (-1) = 1$.

**Rotation (lines L4 and L5).** Let $\delta(x) = 0$ and $\delta(s) = 2$, so by the remark above $x$ is a 1,2 node, not a new leaf. Let $R = r(p) = r(x)$, so $r(s) = R - 2$. Let $x$ be the left child of $p$; the other case is the mirror image. Let $z = x.left$ (outer) and $y = x.right$ (inner).

- *Single rotation* when $\delta(y) = 2$: then $r(y) = R - 2$ and $r(z) = R - 1$. Rotate $x$ above $p$ and demote $p$ to $R - 1$. Now $x$, of rank $R$, has children $z$ and $p$, both of rank $R - 1$; $p$ has children $y$ and $s$, both of rank $R - 2$. All differences are 1. If $R = 1$, then $y$ and $s$ are nil and $p$ is a leaf of rank 0, as (W3) asks.
- *Double rotation* when $\delta(y) = 1$: then $r(y) = R - 1$, $r(z) = R - 2$, and $y$ is the previous $x$, a leaf or a 1,2 node, so its children $a$ (left) and $b$ (right) have ranks in $\{R - 2, R - 3\}$. Rotate $y$ above $x$ and then above $p$; promote $y$ to $R$ and demote $x$ and $p$ to $R - 1$. Now $y$ has children $x$ and $p$, with differences 1; $x$ has children $z$ (difference 1) and $a$ (1 or 2); $p$ has children $b$ (1 or 2) and $s$ (difference 1). If $R = 1$, all of $z$, $a$, $b$, $s$ are nil and $x$ and $p$ are leaves of rank 0.

In both cases the new top has rank $R$, the old rank of $p$, so all rules hold and the loop stops (line L6).

**Termination.** Each promotion moves $x$ up one level. The loop ends at the root, after a promotion that leaves $\delta(p) = 1$, or after one rotation case. At the end all rules hold. An insertion does at most two rotations.

## Deletion

Line L7 deletes as in a binary search tree. A node with two children takes the key of its successor, which has no left child, and that node is removed instead. So the removed node $z$ has at most one child; that child, or nil, takes its place as $x$, under $p$.

- If $z$ was a leaf with $\delta(z) = 1$, then $r(p) = 1$ and the new nil child has difference 2. If $p$ is now a leaf, it is a leaf of rank 1; line L8 demotes it to 0, which raises $\delta(p)$ to 2 or 3, and sets $x \leftarrow p$.
- If $z$ was a leaf with $\delta(z) = 2$, the nil child now has difference 3.
- If $z$ had one child, then $r(z) = 1$ and its child is a leaf $c$ of rank 0. Now $\delta(c) = \delta(z) + 1 \in \{2, 3\}$.

**Invariant at line L9.** (W1) and (W3) hold, and (W2) holds except that $\delta(x)$ may be 3.

Let $\delta(x) = 3$, $R = r(p)$, so $r(x) = R - 3$ and $R \ge 2$. Let $y$ be the sibling of $x$; since $\delta(y) \le 2$, $r(y) \ge 0$, so $y$ is a node. Let $x$ be the left child; the other case is the mirror image.

**Demote $p$ (line L10)** when $\delta(y) = 2$. Then $\delta(x) = 2$ and $\delta(y) = 1$, and $p$ still has the child $y$, so it is not a leaf. Only $\delta(p)$ grows, to 2 or 3. The invariant holds with $x \leftarrow p$.

**Demote $p$ and $y$ (line L11)** when $\delta(y) = 1$ and $y$ is a 2,2 node. Here $y$ has rank $R - 1$ and is not a leaf by (W3), so its children have rank $R - 3 \ge 0$ and are both nodes. After the demotions, $\delta(x) = 2$, $\delta(y) = 1$, and $y$ is a 1,1 node of rank $R - 2 \ge 1$. Only $\delta(p)$ grows, to 2 or 3. The invariant holds with $x \leftarrow p$.

**Single rotation (line L12)** when $\delta(y) = 1$, $y$ is not 2,2, and its outer child $z = y.right$ has $\delta(z) = 1$. So $r(y) = R - 1$, $r(z) = R - 2$, and the inner child $v = y.left$ has rank $R - 2$ or $R - 3$. Rotate $y$ above $p$, promote $y$ to $R$ and demote $p$ to $R - 1$. Now $y$ has children $p$ (difference 1) and $z$ (difference 2); $p$ has children $x$ (difference 2) and $v$ (1 or 2). If $p$ is now a leaf, then $x$ and $v$ are nil, $R = 2$, and $p$ has rank 1; it is demoted again to 0, and then $\delta(p) = 2$. All rules hold and the loop stops.

**Double rotation (line L13)** when $\delta(y) = 1$, $\delta(z) = 2$, and so, since $y$ is not 2,2, $\delta(v) = 1$. Then $r(y) = R - 1$, $r(z) = R - 3$, $r(v) = R - 2$, and the children $a$ (left) and $b$ (right) of $v$ have ranks in $\{R - 3, R - 4\}$. Rotate $v$ above $y$ and then above $p$; promote $v$ twice to $R$, demote $y$ to $R - 2$ and $p$ twice to $R - 2$. Now $v$ has children $p$ and $y$, both with difference 2; $p$ has children $x$ (difference 1) and $a$ (1 or 2); $y$ has children $b$ (1 or 2) and $z$ (difference 1). If $R = 2$, then $v$ was a leaf, $x$, $a$, $b$, $z$ are nil, and $p$ and $y$ are leaves of rank 0. All rules hold and the loop stops (line L14).

In both rotation cases the new top has rank $R$, so the difference toward the parent is unchanged.

**Termination.** Lines L10 and L11 move $x$ up one level. The loop ends at the root, when $\delta(x) \le 2$, or after one rotation case. A deletion does at most two rotations.

## Conclusion

**Theorem.** Starting from the empty tree, after any sequence of insertions and deletions the tree is a WAVL tree on exactly the keys inserted and not deleted, and each update does at most two rotations. The height is at most $2 \lg(n + 1) - 2$ for $n \ge 1$. If no deletion has been done, the tree is an AVL tree, and each rank is the height of its node.

*Proof.* The empty tree satisfies the rules, and the two parts above show that each update keeps them; the key sets change as in a binary search tree.

*Height.* Each rank difference is at least 1 and leaves have rank 0, so the height of a node is at most its rank. Let $m_k$ be the least number of nodes in a subtree whose root has rank $k$. Then $m_0 = 1$, $m_1 = 2$ (a node of rank 1 is not a leaf), and $m_k \ge 2 m_{k-2} + 1$, since both children have rank at least $k - 2$. By induction, $m_k \ge 2^{k/2 + 1} - 1$. So the root rank $k$ satisfies $k \le 2 \lg(n + 1) - 2$.

*Insertions only.* We show that insertions never create a 2,2 node. A new leaf is 1,1. A promotion raises one difference to 2, at the promoted node, whose other difference becomes 1. The rotations leave 1,1 and 1,2 nodes, as listed above. Every other change lowers a difference. So every node is 1,1 or 1,2, and by induction on the height, each rank is $1 + $ the larger rank of its children, which is the height. The differences of heights are then 1 or 2 at each node, which is the AVL rule. $\blacksquare$
