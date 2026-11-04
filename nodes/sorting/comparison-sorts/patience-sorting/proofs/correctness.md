---
title: Patience sorting sorts stably, and its piles count the longest non-decreasing subsequence
proves: [correctness]
status: full
---

We call a list of piles *valid* when each pile, read from the top down, is strictly increasing, and the tops are non-decreasing from left to right.

**Lemma 1 (one deal step).** If the piles are valid before line L3, they are valid after line L5, and line L3 finds the least index $i$ with $x < \text{top}(P[i])$.

*Proof.* The tops are non-decreasing, so the predicate "$x < \text{top}(P[j])$" is false for a prefix of the indices and true for the rest. A binary search for the first index where it is true is therefore correct, and returns $|P|$ when it is true nowhere. If $i < |P|$, the new top is $x < \text{top}(P[i])$, so the pile stays strictly increasing from the top. The left neighbour, if any, has $\text{top}(P[i-1]) \le x$ by the choice of $i$, and the right neighbour has a top at least the old top of $P[i]$, which is greater than $x$. So the tops stay non-decreasing. If $i = |P|$, the new pile holds only $x$, and the last old top is at most $x$. $\square$

**Theorem 1.** PATIENCE-SORT$(A)$ writes the items of $A$ in non-decreasing order.

*Proof.* The empty list of piles is valid, so by Lemma 1 the piles are valid after the deal, and they hold each item once. During the merge, the item at the top of each pile is the least item of that pile. The heap root is a pile whose top is least among all tops, so line L8 outputs the least of the remaining items. By induction on $t$, $A[0 \ldots t]$ holds the $t + 1$ least items in non-decreasing order. After $n$ steps all items are output. $\blacksquare$

**Theorem 2 (stability).** If $y$ and $z$ have equal keys and $y$ comes before $z$ in $A$, then $y$ is output before $z$.

*Proof.* Let $y$ be on pile $p_y$. When $z$ is dealt, the top of $p_y$ is $y$ or an item placed on it later, which is less than $y$; in both cases it is at most $z$. The tops of the piles left of $p_y$ are at most that top. So the binary search does not choose a pile with index at most $p_y$, and $z$ goes to a pile $p_z > p_y$. In particular, two equal items never share a pile.

Suppose that $z$ is output while $y$ is still on its pile. Then $z$ is the top of $p_z$, and it is least among the tops. The top $t$ of $p_y$ is $y$ or an item above $y$; an item above $y$ is less than $y$ and so less than $z$, which is impossible. So $t = y$, the two tops are equal, and the heap breaks the tie for the lower index $p_y < p_z$. So $y$ is at the root, not $z$. This is a contradiction. $\blacksquare$

**Theorem 3 (the number of piles).** The number $k$ of piles after the deal equals the length of the longest non-decreasing subsequence of $A$.

*Proof.* Let $y$ come before $z$ with $y \le z$. When $z$ is dealt, the top of the pile of $y$ is at most $y \le z$, so as in Theorem 2, $z$ goes to a pile further right. So the items of a non-decreasing subsequence lie on piles with increasing indices, and its length is at most $k$.

Conversely, when an item $x$ goes on pile $i > 0$, let $\text{link}(x)$ be the top of pile $i - 1$ at that moment. By the choice of $i$, $\text{link}(x) \le x$, and it was dealt before $x$. Start with any item of pile $k - 1$ and follow the links $k - 1$ times: each step goes to pile one to the left, to an item that comes earlier and is at most the current one. Read in reverse, these $k$ items form a non-decreasing subsequence. $\blacksquare$

**Termination.** The deal handles each item once, and each binary search halves its range. The merge removes one item in each of $n$ steps.
