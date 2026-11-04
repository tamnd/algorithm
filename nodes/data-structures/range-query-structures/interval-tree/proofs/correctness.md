---
title: SEARCH and REPORT of the interval tree are correct, and REPORT visits O((k + 1) h) nodes
proves: [correctness, complexity]
status: full
---

The tree $T$ is a binary search tree of closed intervals ordered by the left end $lo$: every interval in the left subtree of $x$ has $lo \le x.lo$, and every interval in the right subtree has $lo \ge x.lo$. Each node has $x.\mathit{max}$ equal to the largest right end in its subtree, and $\mathit{nil}.\mathit{max} = -\infty$. Intervals $[lo, hi]$ and $[a, b]$ overlap iff $lo \le b$ and $a \le hi$. Let $h$ be the height of $T$ (the number of nodes on a longest path from the root).

**Lemma 1.** Let $x$ be a node, and suppose $x.\mathit{left} \ne \mathit{nil}$ and $x.\mathit{left}.\mathit{max} \ge a$. If no interval of the left subtree overlaps $[a, b]$, then no interval of the right subtree overlaps $[a, b]$.

*Proof.* Some interval $[lo', hi']$ of the left subtree has $hi' = x.\mathit{left}.\mathit{max} \ge a$. It does not overlap, so $lo' > b$. Every interval $[lo'', hi'']$ of the right subtree has $lo'' \ge x.lo \ge lo' > b$, so it does not overlap either. $\square$

**Lemma 2.** If $x.\mathit{left} = \mathit{nil}$ or $x.\mathit{left}.\mathit{max} < a$, then no interval of the left subtree overlaps $[a, b]$.

*Proof.* Each of them has $hi \le x.\mathit{left}.\mathit{max} < a$. $\square$

**Theorem 1 (SEARCH).** SEARCH$(T, a, b)$ returns an interval that overlaps $[a, b]$ if one exists, and nil otherwise, after at most $h$ passes of the loop.

*Proof.* Invariant: if some interval of $T$ overlaps $[a, b]$, then one lies in the subtree of $x$ (with the subtree of nil empty). It holds at the start with $x$ the root. Suppose it holds and the loop runs, so $x$ does not overlap. If line L3 moves to the left child and the left subtree holds no overlapping interval, then by Lemma 1 the right subtree holds none, and $x$ itself does not overlap, so no interval of the subtree of $x$ overlaps, and by the invariant none of $T$ does; the invariant holds for the left child, vacuously or not. If line L4 moves right, by Lemma 2 the left subtree has no overlap and $x$ has none, so an overlapping interval of the subtree of $x$ is in the right subtree. Each pass goes one level down, so the loop stops after at most $h$ passes. If it stops at a node, the loop test says that node overlaps. If it stops at nil, the subtree of nil is empty, so by the invariant no interval overlaps. $\square$

**Theorem 2 (REPORT).** REPORT$(x, a, b, out)$ appends exactly the intervals of the subtree of $x$ that overlap $[a, b]$, each once.

*Proof.* By induction on the size of the subtree. For nil nothing is appended, which is right. If $x.\mathit{max} < a$, every interval of the subtree ends before $a$, and nothing is right. Otherwise line L7 appends the overlapping intervals of the left subtree, by the induction hypothesis, and line L8 appends $x$ iff it overlaps. If $x.lo \le b$, line L9 appends those of the right subtree. If $x.lo > b$, every interval of the right subtree has $lo \ge x.lo > b$, and none overlaps. The three parts are disjoint. $\square$

**Theorem 3 (cost of REPORT).** If REPORT$(T.\mathit{root}, a, b)$ outputs $k$ intervals, at most $(k + 1) h$ of its calls pass line L6, and it makes at most $\min(2 (k + 1) h + 1, 2n + 1)$ calls in total.

*Proof.* Let $P$ be the search path of $b$: start at the root, and at a node $y$ go right if $y.lo \le b$ and left otherwise. Call a node *expanded* if a call on it passes line L6.

Let $x$ be expanded. By line L9, every right turn on the path from the root to $x$ is at a node $y$ with $y.lo \le b$. Suppose the path also turns left at some $y$ with $y.lo \le b$. Then every interval below $x$ has $lo \le y.lo \le b$. Since $x$ passes line L6, an interval below $x$ (or $x$ itself) has $hi = x.\mathit{max} \ge a$, so it overlaps $[a, b]$, and by Theorem 2 it is output; so $x$ lies on the path from the root to an output. Otherwise every left turn is at a $y$ with $y.lo > b$ and every right turn at a $y$ with $y.lo \le b$, so $x$ lies on $P$.

So the expanded nodes lie on the union of $P$ and the $k$ root paths of the outputs, which has at most $(k + 1) h$ nodes. Each call is on the root or on a child of an expanded node, so there are at most $2 (k + 1) h + 1$ calls. Each node is called at most once, and the calls on nil are at most $n + 1$, so there are at most $2n + 1$ calls. $\square$
