---
title: MORRIS-INORDER visits the nodes in inorder, terminates, and restores the tree
proves: [correctness, termination]
status: full
---

Fix a binary tree with the original pointers $\mathrm{left}_0$ and $\mathrm{right}_0$. For a node $x$, let $T(x)$ be its subtree in the original tree, let $|T(x)|$ be its number of nodes, and let $\mathrm{last}(x)$ be the last node of $T(x)$ in inorder. The node $\mathrm{last}(x)$ is reached from $x$ by following $\mathrm{right}_0$ pointers until one is NIL, so $\mathrm{right}_0[\mathrm{last}(x)] = \mathrm{NIL}$. The algorithm never writes $\mathrm{left}$, so $\mathrm{left} = \mathrm{left}_0$ at all times.

Say that $T(x)$ is *clean with exit $s$* if every node $y$ of $T(x)$ has $\mathrm{right}[y] = \mathrm{right}_0[y]$, except that $\mathrm{right}[\mathrm{last}(x)] = s$, where $s$ is NIL or a node outside $T(x)$.

**Lemma 1.** Suppose that at the start of an iteration of line L2 the current node is $x$, and $T(x)$ is clean with exit $s$. Then after finitely many iterations, the current node is $s$, the visits made in between are the nodes of $T(x)$ in inorder, $T(x)$ is again clean with exit $s$, and no right pointer outside $T(x)$ was read or written in between.

*Proof.* By strong induction on $|T(x)|$. Let $L = \mathrm{left}[x]$ and $R = \mathrm{right}_0[x]$.

*Case 1: $L = \mathrm{NIL}$.* Line L4 visits $x$ and sets the current node to $\mathrm{right}[x]$.

- If $R = \mathrm{NIL}$, then $T(x) = \{x\}$, $\mathrm{last}(x) = x$ and $\mathrm{right}[x] = s$. So the current node is $s$ after one iteration, the only visit is $x$, which is the inorder of $T(x)$, and nothing was written.
- If $R \ne \mathrm{NIL}$, then $x \ne \mathrm{last}(x)$, so $\mathrm{right}[x] = R$ and the current node becomes $R$. The subtree $T(R)$ has $\mathrm{last}(R) = \mathrm{last}(x)$, and it is clean with exit $s$, because $T(R) \subset T(x)$ and $s \notin T(x)$. It is smaller than $T(x)$, so by the induction hypothesis the walk visits $T(R)$ in inorder, arrives at $s$, and leaves $T(R)$ clean with exit $s$. The visits are $x$ followed by the inorder of $T(R)$, which is the inorder of $T(x)$ since $T(x)$ has no left subtree.

*Case 2: $L \ne \mathrm{NIL}$.* Let $p^* = \mathrm{last}(L)$, the inorder predecessor of $x$. It is in $T(L)$, so $p^* \ne \mathrm{last}(x)$ (which is $x$ or in $T(R)$), and $\mathrm{right}[p^*] = \mathrm{right}_0[p^*] = \mathrm{NIL}$.

*First visit.* Line L5 starts at $p = L$ and follows right pointers. Every node on the path from $L$ to $p^*$ along $\mathrm{right}_0$ is in $T(L)$ and is not $\mathrm{last}(x)$, so its right pointer is original. For each such node before $p^*$, the right pointer is a node of $T(L)$, so it is neither NIL nor $x$, and the loop goes on. At $p^*$ the right pointer is NIL, and the loop stops with $p = p^*$. Line L6 sets $\mathrm{right}[p^*] = x$ and moves to $L$. Now $T(L)$ is clean with exit $x$, and $x \notin T(L)$. Only right pointers in $T(L)$ were read, and only $\mathrm{right}[p^*]$ was written.

*The left subtree.* $|T(L)| < |T(x)|$, so by the induction hypothesis the walk visits $T(L)$ in inorder and arrives at $x$, with $T(L)$ clean with exit $x$, and touches no right pointer outside $T(L)$. So the rest of $T(x)$, in particular $\mathrm{right}[x]$ and the pointers in $T(R)$, is as it was before the first visit.

*Second visit.* Line L5 again walks from $L$ along the right pointers. As before, the nodes before $p^*$ have original pointers into $T(L)$, so the loop reaches $p^*$, and it stops there because $\mathrm{right}[p^*] = x$. Line L6 does not apply, and line L7 sets $\mathrm{right}[p^*] = \mathrm{NIL}$, visits $x$ and sets the current node to $\mathrm{right}[x]$. Now every right pointer in $T(L)$ is original. The rest is as in Case 1: if $R = \mathrm{NIL}$, then $x = \mathrm{last}(x)$ and $\mathrm{right}[x] = s$, so the walk arrives at $s$; else $\mathrm{right}[x] = R$, and the induction hypothesis on $T(R)$, which is clean with exit $s$, gives the inorder of $T(R)$ and the arrival at $s$.

The visits are the inorder of $T(L)$, then $x$, then the inorder of $T(R)$, which is the inorder of $T(x)$. At the end, the pointers in $T(L)$ and at $x$ are original and $T(R)$ is clean with exit $s$, so $T(x)$ is clean with exit $s$. Only right pointers in $T(x)$ were read or written. Each part takes finitely many iterations, by the induction hypothesis. $\square$

**Theorem.** MORRIS-INORDER terminates, visits every node of the tree exactly once and in inorder, and at the end every pointer has its original value.

*Proof.* If the root is NIL, the loop does not run, nothing is visited, and nothing is written. Otherwise, at the start, all pointers are original. The tree $T(\mathrm{root})$ is then clean with exit NIL, because $\mathrm{right}_0[\mathrm{last}(\mathrm{root})] = \mathrm{NIL}$. By Lemma 1, after finitely many iterations the current node is NIL, the visits are the inorder of the whole tree, and the tree is clean with exit NIL, which means that all right pointers are original. At that moment the test of line L2 fails, and the algorithm stops. $\blacksquare$
