---
title: The partitioning greedy uses exactly as many resources as the depth
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The intervals $I[1], \ldots, I[n]$ are nonempty and of one type, with $I[j] = \langle l_j, r_j \rangle$. Say that an interval $\langle l', r' \rangle$ is *over by* $x$ when $r' \le x$ for half-open and open intervals and $r' < x$ for closed intervals. Line L4 tests whether the interval at the heap minimum is over by $I[j].l$. Let $d$ be the depth, the largest number of intervals that contain one point.

**Lemma 1 (over by means disjoint).** Let $A = \langle a, a' \rangle$ and $B = \langle b, b' \rangle$ with $a \le b$. Then $A \cap B = \emptyset$ if and only if $A$ is over by $b$.

*Proof.* For closed intervals, $A \cap B = \emptyset$ if and only if $a' < b$, since $a \le b$ and $B$ contains $b$. For half-open intervals, $B$ contains $b$ and the points just right of it, and $A$ contains every point of $[a, a')$, so they are disjoint if and only if $a' \le b$. For open intervals, $B$ contains the points just right of $b$, and $A$ contains every point of $(a, a')$; if $a' > b$, the points just right of $b$ and left of $a'$ are in both, since $a \le b$, and if $a' \le b$ every point of $A$ is less than $b$. $\square$

**Lemma 2 (two intervals through a point).** Under the same assumption $a \le b$, if $A$ is not over by $b$, then $A$ and $B$ both contain the point $z(b)$. Here $z(b) = b$ for closed and half-open intervals. For open intervals, $z(b)$ is a fixed point with $b < z(b)$ and no end point of any input interval in $(b, z(b)]$; it exists because there are finitely many end points.

*Proof.* For closed intervals, $a \le b \le a'$ and $b \le b'$, so $b \in A \cap B$. For half-open intervals, $a \le b < a'$ and $b < b'$, so $b \in A \cap B$. For open intervals, $a \le b < a'$ and $b < b'$. The end points $a'$ and $b'$ are greater than $b$, so $z(b) < \min(a', b')$, and $a \le b < z(b)$; so $z(b) \in A \cap B$. $\square$

**Invariant.** Let $D$ be the set of indices processed so far. Before each step of the loop of line L3:

> **(I)** The heap holds exactly one pair $(t, c)$ for each $c \in \{1, \ldots, k\}$, where $t$ is the right end of the interval $last(c)$, the interval of $D$ with label $c$ that was processed last. Two intervals of $D$ with the same label are disjoint.

*Initialization.* $D$ is empty, $k = 0$ and the heap is empty.

*Maintenance.* Let $j$ be the next index, $x = I[j].l$. Every interval of $D$ starts at or before $x$, by the order of line L1.

*Line L5 runs.* The minimum pair is $(t, c)$, and $last(c)$ is over by $x$. The intervals with label $c$, in processing order, are $A_1, \ldots, A_m = last(c)$, and $A_{i+1}$ took label $c$ when $A_i$ was over by $l(A_{i+1})$, so $r(A_i) \le l(A_{i+1}) \le r(A_{i+1})$. So every $A_i$ has $r(A_i) \le t$ and is over by $x$ whenever $last(c)$ is: if $r(A_i) \le t$ and $t \le x$ (or $t < x$), the same holds for $r(A_i)$. By Lemma 1, each $A_i$ is disjoint from $I[j]$. Line L7 gives $I[j]$ label $c$ and puts $(r_j, c)$ back, so (I) holds.

*Line L6 runs.* Then $I[j]$ gets the new label $k + 1$, which no other interval has, and line L7 adds its pair. (I) holds.

**Optimality.** Consider the step in which line L6 opens resource $k$, at $x = I[j].l$. If the heap is not empty, its minimum is not over by $x$, so no pair is: each $last(c)$ for $c < k$ has right end at least the minimum, so it is not over by $x$ either. Each $last(c)$ starts at or before $x$. By Lemma 2, applied to $last(c)$ and $I[j]$, each $last(c)$ and $I[j]$ contain the point $z(x)$, which depends only on $x$. So $k$ intervals contain one point, and $k \le d$. On the other side, the $d$ intervals through one point pairwise meet, so a valid labeling gives them $d$ different labels, and every valid labeling has at least $d$ labels. The final $k$ is the largest value opened, so $k = d$, and by (I) at the end the labeling is valid.

**Termination.** Line L1 sorts $n$ keys. The loop runs $n$ times, each with at most one EXTRACT-MIN and one INSERT on a heap of at most $n$ pairs. $\blacksquare$
