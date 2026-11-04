---
title: The merge sort tree answers counting and k-th queries correctly
proves: [correctness, complexity]
status: full
---

Let $A[0 \ldots n-1]$ be an array over a totally ordered set, $N$ the least power of two with $N \ge n$, and number the nodes $1 \ldots 2N - 1$ as in the page: node $v < N$ has the children $2v$ and $2v + 1$, and the leaf $N + i$ is position $i$. Node $v$ at depth $d$ covers $I_v = [j 2^{K-d}, (j+1) 2^{K-d})$, where $K = \lg N$ and $v = 2^d + j$.

**Lemma 1 (build).** After BUILD, each $S_v$ is the sorted list of the multiset $M_v = \{A[k] : k \in I_v, k < n\}$.

*Proof.* By induction on $v$ from $2N - 1$ down to $1$. A leaf $N + i$ holds $[A[i]]$ if $i < n$ (line L7) and the empty list otherwise, which is $M_{N+i}$ sorted. For $v < N$, $I_v$ is the disjoint union of $I_{2v}$ and $I_{2v+1}$, so $M_v = M_{2v} \uplus M_{2v+1}$, and the merge of two sorted lists (line L8) is the sorted list of the union of their multisets. $\square$

**Lemma 2 (canonical nodes).** For $0 \le l \le r \le N$, the nodes at which lines L3 and L4 call LOWER have pairwise disjoint ranges whose union is $[l, r)$, and there are at most two of them per level.

*Proof.* Write $l', r'$ for the variables after line L1. We keep the invariant: the nodes used so far cover $[l, r)$ minus the union $U$ of $I_u$ for $l' \le u < r'$, where $u$ ranges over the nodes of the current level, and the used nodes are disjoint from $U$. At the start nothing is used and $U$ is the union of the leaves $N + l, \ldots, N + r - 1$, which is $[l, r)$. In one round, if $l'$ is odd, node $l'$ is the right child of its parent, so the node $l'$ is moved from $U$ to the used set and $l'$ becomes even; the same holds for $r'$ odd with $r' - 1$. Now $l'$ and $r'$ are even, so the nodes $l', \ldots, r' - 1$ pair up into the children of $l'/2, \ldots, r'/2 - 1$, and line L5 keeps $U$ the same. The loop stops when $l' \ge r'$, so $U$ is empty, and each round uses at most two nodes of one level. $\square$

**Theorem 1 (count).** COUNT$(l, r, x)$ returns $\#\{k \in [l, r) : A[k] < x\}$.

*Proof.* By Lemma 2 the positions of $[l, r)$ with $k < n$ are split among the used nodes, each in exactly one, and by Lemma 1 LOWER$(S_v, x)$ is the number of those positions $k \in I_v$ with $A[k] < x$. Summing gives the claim. The same proof with an upper-bound search gives the count of $A[k] \le x$. $\square$

**Theorem 2 (k-th).** For $1 \le k \le r - l$, KTH$(l, r, k)$ returns the $k$-th smallest item of $A[l \ldots r-1]$.

*Proof.* Let $c(v) = \#\{j \in [l, r) : A[j] \le v\}$; it is non-decreasing in $v$. Let $y$ be the $k$-th smallest item of the range. Then $c(y) \ge k$, and $c(v) < k$ for every $v < y$. The root list $S_1$ is $A$ sorted (Lemma 1), so it contains $y$, and the predicate $P(m) = [c(S_1[m]) \ge k]$ is monotone in $m$ and true at the last index $n - 1$, since $c(S_1[n-1]) = r - l \ge k$. Lines L9 to L12 are a binary search for the least $m$ with $P(m)$, kept by the invariant that $P(hi)$ holds and $P(m')$ fails for all $m' < lo$. At the least such $m$, $S_1[m] \ge y$ since $P$ fails below $y$, and $S_1[m] \le y$ since $y$ occurs in $S_1$ at some index where $P$ holds. So $S_1[m] = y$. $\square$

**Theorem 3 (cost).** BUILD takes $O(n \log n)$ time and the lists have $n (K + 1)$ items. COUNT takes $O(\log^2 n)$ time and KTH takes $O(\log^3 n)$.

*Proof.* The lists of one level hold each of the $n$ items once, so the merges of one level take $O(n + N)$ time, and there are $K + 1 = O(\log n)$ levels. By Lemma 2 COUNT does at most $2K$ binary searches on lists of at most $n$ items, $O(\log n)$ each. KTH does $\lceil \lg n \rceil$ rounds of the outer search, each one count. Termination: COUNT halves $r' - l'$ at least every round, so it runs at most $K + 1$ rounds, and the outer search halves $hi - lo$. $\square$
