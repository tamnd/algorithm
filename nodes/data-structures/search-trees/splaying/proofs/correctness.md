---
title: Splaying keeps the binary search tree and ends with x at the root
proves: [correctness, termination]
status: full
---

Let $T$ be a binary search tree with parent pointers in which, for each node $v$, $v.left.p = v$ and $v.right.p = v$ when the children exist, and the root has no parent. Call this the link invariant.

**Lemma 1 (rotation).** If $x$ has a parent $y$, ROTATE$(x)$ keeps the link invariant and the in-order sequence, makes $y$ a child of $x$, and gives $x$ the old parent $z$ of $y$ (or no parent). The depth of $x$ drops by 1, and the subtree that $x$ now roots holds exactly the nodes of the old subtree of $y$.

*Proof.* Take $x = y.left$ (line L8); the other case is the mirror image. Let $\alpha, \beta$ be the subtrees of $x$ and $\gamma$ the right subtree of $y$, so the in-order sequence of the subtree of $y$ is $\alpha, x, \beta, y, \gamma$. After line L8, $y$ has children $\beta$ and $\gamma$, and $x$ has children $\alpha$ and $y$, so the sequence of the new subtree of $x$ is $\alpha, x, \beta, y, \gamma$, the same. The parent of the root of $\beta$ is set to $y$ in line L8, the parent of $y$ to $x$ and the parent of $x$ to $z$ in line L10, and the child pointer of $z$ that pointed to $y$ points to $x$ after line L11. All other links are unchanged. So the link invariant holds, and the in-order sequence of the whole tree is unchanged, since the subtree at that position has the same sequence. The keys of $\alpha, x, \beta, y, \gamma$ are in increasing order, so the BST property holds at $x$ and $y$; at every other node the set of keys in each subtree is unchanged. $\square$

**Lemma 2 (one round).** Assume $x.p \ne $ NIL at line L1. After the round, the link invariant and the in-order sequence still hold, and the depth of $x$ has dropped by 1 (line L3) or by 2 (lines L4 and L5).

*Proof.* Line L3 is one rotation of $x$. In line L4 the first rotation, ROTATE$(y)$, moves $y$ above $z$; by Lemma 1 the subtree of $y$ keeps $x$ as a child on the same side, so $x$ is still a child of $y$ and the second rotation is legal; it moves $x$ above $y$, and $x$ takes the old place of $z$, so its depth drops by 2. In line L5 the first rotation moves $x$ above $y$, and $x$ takes the place of $y$ as a child of $z$; the second moves $x$ above $z$. Each rotation keeps the invariant and the sequence by Lemma 1. $\square$

**Theorem.** SPLAY$(T, x)$ ends after $\lceil d/2 \rceil$ rounds and $d$ rotations, where $d$ is the depth of $x$, and then $T$ is a binary search tree with the same in-order sequence, the link invariant, and root $x$.

*Proof.* By Lemma 2 the depth of $x$ drops by 2 in each round while it is at least 2, and the last round is a zig exactly when the depth is 1. So the number of rounds is $\lceil d/2 \rceil$ and the number of rotations is $d$. The loop stops when $x.p = $ NIL, that is when $x$ is the root, and line L6 records it. The invariants hold after each round by Lemma 2. $\blacksquare$
