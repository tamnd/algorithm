---
title: The one-pass LRU stack gives the hits of the LRU cache of every size
proves: [correctness]
status: full
---

We prove the claim for the LRU rule: $\mathrm{PRI}(a, b)$ is true when the last use of $a$ is later than the last use of $b$. Line L6 records the time of the last use. For the OPT rule the page refers to Mattson, Gecsei, Slutz and Traiger, and the tests check that case against one MIN simulation per size.

Let $S_t$ be the list $S$ after request $t$, and let $U_t$ be the set of distinct items in $\sigma_1 \cdots \sigma_t$. Let $\mathrm{last}_t(z)$ be the time of the last request for $z$ up to $t$.

**Lemma 1 (the stack is the recency order).** For each $t \ge 0$, $S_t$ lists each item of $U_t$ exactly once, ordered by $\mathrm{last}_t$, latest first.

*Proof.* By induction on $t$. For $t = 0$, $S_0$ and $U_0$ are empty. Assume the claim for $t - 1$, and let $S_{t-1} = s_1, \ldots, s_m$, so $\mathrm{last}_{t-1}(s_1) > \cdots > \mathrm{last}_{t-1}(s_m)$. Let $y = \sigma_t$. The new order by $\mathrm{last}_t$ is $y$ followed by the items of $S_{t-1}$ other than $y$, in their old order, because only the last use of $y$ changes and it becomes $t$, the latest.

If line L7 applies, $y = s_1$ and this order is $S_{t-1}$, which the algorithm keeps. If line L8 applies, $m = 0$ and the new list is $y$. Otherwise, line L9 puts $y$ at position 1 and carries $c = s_1$. Let $e = d - 1$ if $y = s_d$, and $e = m$ if $y \notin S_{t-1}$. We claim that just before the step $i$ of line L10, with $2 \le i \le e$, the carried item is $c = s_{i-1}$ and position $i$ still holds $s_i$. This is true for $i = 2$. At step $i$, $c = s_{i-1}$ was used later than $s_i$, so $\mathrm{PRI}(s_i, c)$ is false, and line L11 swaps: position $i$ gets $s_{i-1}$ and the carried item becomes $s_i$. Position $i + 1$ is not touched, so it still holds $s_{i+1}$. After the loop, $c = s_e$. Line L12 puts it at position $d$, the old place of $y$, or appends it if $y$ is new. The result is $y, s_1, \ldots, s_e, s_{d+1}, \ldots, s_m$ if $y = s_d$, or $y, s_1, \ldots, s_m$ if $y$ is new. In both cases this is the new recency order, and it lists each item of $U_t = U_{t-1} \cup \{y\}$ once. $\square$

**Lemma 2 (the LRU cache is the top of the stack).** Let $L_t(k)$ be the content of an LRU cache of size $k$ after request $t$, from an empty start. Then $L_t(k)$ is the set of the first $\min(k, |U_t|)$ items of $S_t$.

*Proof.* By induction on $t$. For $t = 0$ both sets are empty. Assume the claim for $t - 1$, and write $T_{t-1}$ for the first $\min(k, |U_{t-1}|)$ items of $S_{t-1}$. Let $y = \sigma_t$.

- If $y \in L_{t-1}(k)$, LRU hits and the content does not change. By Lemma 1, $S_t$ moves $y$ to the top and keeps the order of the others. The first $\min(k, |U_t|)$ items of $S_t$ are $y$ and the other items of $T_{t-1}$, because $y$ was among them and $|U_t| = |U_{t-1}|$. This is $L_{t-1}(k) = L_t(k)$.
- If $y \notin L_{t-1}(k)$ and $|L_{t-1}(k)| < k$, LRU loads $y$ without an eviction. Then $T_{t-1} = U_{t-1}$, so $y$ is new, $|U_t| = |U_{t-1}| + 1 \le k$, and the first $|U_t|$ items of $S_t$ are all of $U_t = L_{t-1}(k) \cup \{y\}$.
- If $y \notin L_{t-1}(k)$ and $|L_{t-1}(k)| = k$, LRU evicts the least recently used item of $L_{t-1}(k)$, which by Lemma 1 is $s_k$, and loads $y$. Since $y$ is at depth more than $k$ in $S_{t-1}$ or is new, the first $k$ items of $S_t$ are $y, s_1, \ldots, s_{k-1}$. This is $L_{t-1}(k) \setminus \{s_k\} \cup \{y\} = L_t(k)$. $\square$

**Theorem.** For each $k \ge 1$, the value $H(k)$ of line L13 equals the number of hits of the LRU cache of size $k$ on $\sigma$.

*Proof.* Request $t$ hits in the LRU cache of size $k$ exactly when $y = \sigma_t \in L_{t-1}(k)$. By Lemma 2, this holds exactly when $y$ is among the first $k$ items of $S_{t-1}$, that is, when the depth $d$ found by line L4 satisfies $d \le k$. If $y \notin S_{t-1}$, then $d = \infty$ and the request misses for every $k$. Line L5 counts request $t$ in $\mathrm{hist}[d]$, so $\mathrm{hist}[1] + \cdots + \mathrm{hist}[k]$ is the number of requests with $d \le k$, which is the number of hits with size $k$. $\square$

As a consequence, $L_t(k) \subseteq L_t(k + 1)$ for all $t$ and $k$, so LRU has the inclusion property, and its hits never decrease as $k$ grows.
