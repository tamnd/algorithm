---
title: The queries of the fully indexable dictionary are correct
proves: [correctness]
status: full
---

Let $S \subseteq U = \{0, \ldots, u-1\}$ with $|S| = n$, and let $B$ be its characteristic vector. Write $s_1 < s_2 < \cdots < s_n$ for the elements of $S$. We assume that the primitives are correct: ACCESS$(x) = B[x]$, RANK1$(r) = |\{y < r : B[y] = 1\}|$, SELECT1$(i) = s_i$ and SELECT0$(k)$ is the $k$-th smallest element of $U \setminus S$. These are the queries of the [rank and select problem](/rank-select-problem/) on $B$.

**MEMBER, RANK, SELECT (lines L1 to L3).** $x \in S$ if and only if $B[x] = 1$, so line L1 is correct. $\text{RANK1}(r)$ counts the $y < r$ with $B[y] = 1$, which are the elements of $S$ less than $r$, so line L2 is correct. Line L3 returns $s_i$ by assumption.

**PRED (lines L4 to L6).** Let $0 \le x < u$ and $r = \text{RANK1}(x + 1) = |\{y \in S : y \le x\}|$. The elements of $S$ that are $\le x$ are exactly $s_1, \ldots, s_r$: they are the $r$ smallest elements of $S$, because if $s_i \le x$ then $s_{i'} \le x$ for each $i' < i$. If $r = 0$, no element is $\le x$, and line L5 returns none, which is right. If $r \ge 1$, the largest of them is $s_r$, and line L6 returns SELECT1$(r) = s_r$.

**SUCC (lines L7 to L9).** Let $r = \text{RANK1}(x) = |\{y \in S : y < x\}|$. By the same argument, the elements less than $x$ are $s_1, \ldots, s_r$, so the elements $\ge x$ are $s_{r+1}, \ldots, s_n$. If $r = n$, there is none, and line L8 returns none. Otherwise the smallest is $s_{r+1}$, which line L9 returns; SELECT1$(r + 1)$ is defined because $1 \le r + 1 \le n$.

**RANK-OUT (line L10).** Each $y$ with $0 \le y < r$ is in exactly one of $S$ and $U \setminus S$, so $|\{y \notin S : y < r\}| = r - |\{y \in S : y < r\}| = r - \text{RANK1}(r)$.

**SELECT-OUT (line L11).** The $k$-th smallest element of $U \setminus S$ is the position of the $k$-th 0 of $B$, which SELECT0$(k)$ returns by assumption.

**The primitives of the implementation.** The Python code keeps $B$ in packed words with the count $RS[q]$ of 1s before superblock $q$ of $8$ words. Its rank adds $RS[q]$, the counts of the full words of the superblock before word $\lfloor r/w \rfloor$, and the count of the low $r \bmod w$ bits of that word, which together cover $\{0, \ldots, r-1\}$ exactly. Its select first finds by binary search the last superblock $q$ with fewer than $j$ wanted bits before it. Such a $q$ exists since superblock 0 has none before it, and the wanted bit is in superblock $q$ or later; it is not later, because the next superblock already has at least $j$ wanted bits before it, or does not exist. It then scans words from the start of superblock $q$ as in the SELECT1 of the [bit vector](/bit-vector/), with the padding of the last word masked off for 0s. $\blacksquare$
