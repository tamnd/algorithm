---
title: Shiloach-Vishkin merging computes the stable merge
proves: [correctness]
status: full
---

Let $C$ be the stable merge of the sorted arrays $A[0 \ldots m-1]$ and $B[0 \ldots n-1]$: the items in the strict order where $u$ comes before $v$ if $u$ has the smaller key, or the keys are equal and $u$ is in $A$ and $v$ in $B$, or both are in the same array and $u$ has the smaller index. A pair $(i, j)$ is a *split* if the first $i + j$ items of $C$ are $A[0 \ldots i-1]$ and $B[0 \ldots j-1]$.

## Lemma 1. The cuts are splits

*Proof.* Let $(i, j)$ be an A-cut, with $j$ the number of items of $B$ less than $A[i]$. The items before $A[i]$ in $C$ are $A[0 \ldots i-1]$, and the items $B[\ell]$ with $B[\ell] < A[i]$, which are $B[0 \ldots j-1]$ because $B$ is sorted. So $A[i]$ is at position $i + j$, and the first $i + j$ items are those. A B-cut $(i, j)$, with $i$ the number of items of $A$ at most $B[j]$, is the same with the roles swapped: the items before $B[j]$ are $B[0 \ldots j-1]$ and the items of $A$ at most $B[j]$, which are $A[0 \ldots i-1]$. The pairs $(0, 0)$ and $(m, n)$ are splits too. $\square$

## Lemma 2. Splits form a chain

If $(i, j)$ and $(i', j')$ are splits with $i + j \le i' + j'$, then $i \le i'$ and $j \le j'$. Two different splits have different sums $i + j$.

*Proof.* The first $i + j$ items of $C$ are a prefix of the first $i' + j'$ items, so $A[0 \ldots i-1]$ is part of $A[0 \ldots i'-1]$ and $B[0 \ldots j-1]$ of $B[0 \ldots j'-1]$. If $i + j = i' + j'$, the two prefixes are the same set, so $i = i'$ and $j = j'$. $\square$

## Lemma 3. Line L4 gives the order

Let $a = \lceil m/p \rceil$ and $b = \lceil n/p \rceil$. The number of B-cuts that come before the A-cut $(i, j)$ in the order of Lemma 2 is $\max(0, \lceil j/b \rceil - 1)$, and the number of A-cuts that come before the B-cut $(i, j)$ is $\max(0, \lceil i/a \rceil - 1)$. No A-cut equals a B-cut.

*Proof.* A B-cut with index $t b$ comes before the A-cut $(i, j)$ if and only if $B[t b]$ is among the first $i + j$ items of $C$, that is, if and only if $t b < j$ by Lemma 1. The number of integers $t \ge 1$ with $t b < j$ is $\max(0, \lceil j/b \rceil - 1)$, and all of them satisfy $t b < n$ and $t \le p - 1$, because $j \le n \le p b$. The count for a B-cut is the same with the roles swapped. If an A-cut and a B-cut were the same pair $(i, j)$, then $B[j]$ would not be less than $A[i]$ (because only $j$ items of $B$ are less than $A[i]$) and $A[i]$ would not be at most $B[j]$ (because only $i$ items of $A$ are at most $B[j]$), which is impossible. $\square$

So the place that line L4 gives to a cut is its index among the cuts of its own list plus the number of cuts of the other list before it, which is its index in the sorted order of all cuts. The places are distinct, and $S$ is the list of all splits in increasing order.

## Lemma 4. Each piece is a merge of two parts

Let $(i, j)$ and $(i', j')$ be consecutive in $S$. Then $C[i + j \ldots i' + j' - 1]$ is the stable merge of $A[i \ldots i'-1]$ and $B[j \ldots j'-1]$, and it holds at most $a$ items of $A$ and at most $b$ items of $B$.

*Proof.* By Lemma 2, $i \le i'$ and $j \le j'$. The first $i' + j'$ items of $C$ are $A[0 \ldots i'-1]$ and $B[0 \ldots j'-1]$, and the first $i + j$ are $A[0 \ldots i-1]$ and $B[0 \ldots j-1]$. So the items in between are $A[i \ldots i'-1]$ and $B[j \ldots j'-1]$, in the order of $C$, which on these items is their stable merge. If the part of $A$ had more than $a$ items, it would contain an index $t a$ with $i < t a < i'$ and $t a < m$, and then the A-cut $t$ would be a split strictly between the two consecutive splits, by Lemma 2. The same holds for $B$. $\square$

## Theorem

SV-MERGE writes the stable merge $C$ of $A$ and $B$.

*Proof.* By Lemma 3, $S$ lists $(0, 0)$, all cuts and $(m, n)$ in increasing order of $i + j$. The pieces between consecutive splits cover the positions $0, \ldots, m + n - 1$ of $C$ exactly once, and by Lemma 4 line L7 writes the correct items to each piece. $\square$
