---
title: The piercing greedy places the fewest points
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The intervals $I[1], \ldots, I[n]$ are nonempty and of one type, with $I[k] = \langle l_k, r_k \rangle$. Let $k_1, k_2, \ldots, k_n$ be the order of line L1, so $r_{k_1} \le r_{k_2} \le \cdots \le r_{k_n}$. For half-open and open intervals line L4 tests $l \ge p$ in place of $l > p$.

**Claim.** PIERCE stops after $n$ steps. For closed intervals it returns a set of points that pierces every interval, of the least possible size. For half-open and open intervals the same holds after each $p$ is replaced by the real point of its group described below.

**Openers and groups.** Call $I[k]$ an *opener* if line L5 runs in its step, and let $J_1, \ldots, J_m$ be the openers in order, with right ends $q_1 \le q_2 \le \cdots \le q_m$. The *group* $G_i$ is $J_i$ together with the intervals read after $J_i$ and before $J_{i+1}$; in their steps $p = q_i$.

**Lemma 1 (each group has a common point).** Every interval of $G_i$ meets the point $q_i$ in the sense of its type. That is, an interval $\langle l, r \rangle \in G_i$ has $l \le q_i \le r$ for closed intervals, and $l < q_i \le r$ for half-open and open intervals.

*Proof.* Each interval of $G_i$ comes at or after $J_i$ in the order, so $r \ge q_i$. For $J_i$ itself, $l \le r = q_i$, and $l < r = q_i$ for half-open and open intervals, which are nonempty. For any other interval of $G_i$ the test of line L4 failed, so $l \le q_i$ for closed intervals and $l < q_i$ for the other types. $\square$

**Real points.** For closed intervals the point is $q_i$, which lies in every interval of $G_i$ by Lemma 1. For half-open and open intervals let $m_i$ be the largest left end in $G_i$, so $m_i < q_i$ by Lemma 1. For half-open intervals, $m_i$ lies in every $[l, r) \in G_i$, since $l \le m_i < q_i \le r$. For open intervals, the midpoint $(m_i + q_i)/2$ lies in every $(l, r) \in G_i$, since $l \le m_i < (m_i + q_i)/2 < q_i \le r$. So in each case one point pierces the whole group, and the groups together contain all $n$ intervals. Hence the output pierces every interval and has $m$ points.

**Lemma 2 (the openers are pairwise disjoint).** For $i < j$, $J_i \cap J_j = \emptyset$.

*Proof.* When $J_{i+1}$ is read, $p = q_i$ and the test of line L4 holds: $l(J_{i+1}) > q_i$ for closed intervals, and $l(J_{i+1}) \ge q_i$ for the other types. For $j > i$, the openers come in order, so $l(J_j) > q_{j-1} \ge q_i$ in the closed case and $l(J_j) \ge q_{j-1} \ge q_i$ otherwise. Every point of $J_i$ is at most $q_i$, and less than $q_i$ for half-open and open intervals; every point of $J_j$ is at least $l(J_j)$, and greater than it for open intervals. In each case every point of $J_i$ is less than every point of $J_j$. $\square$

**Optimality.** Let $P$ be any set of points that pierces every interval. Each opener contains a point of $P$, and by Lemma 2 no point lies in two openers. So $|P| \ge m$, and the output, with $m$ points, is optimal.

**Termination.** Line L1 sorts $n$ keys, and the loop of line L3 does one step of $O(1)$ work for each index. The real points need one more value per group, the running maximum $m_i$, which is updated in $O(1)$ time per step. $\blacksquare$
