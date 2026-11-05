---
title: NN-Descent keeps valid lists, terminates, and stops at a locally optimal graph
proves: [correctness]
status: full
---

We use the names of the pseudocode on the page. Fix $n \ge 2$ points, $1 \le k < n$, and the dissimilarity $\sigma$. For a point $v$ and $u \ne v$ write $\pi_v(u) = (\sigma(v, u), u)$, and order these pairs lexicographically. This is a strict total order on the $n - 1$ points $u \ne v$; let $\mathrm{rank}_v(u) \in \{1, \ldots, n - 1\}$ be the position of $u$ in it. Write $\max B[v]$ for the largest $\pi_v(u)$ with $u \in B[v]$.

**Lemma 1 (valid lists).** At all times each $B[v]$ holds $k$ distinct points other than $v$, each stored with $\sigma(v, u)$, and $\max B[v]$ never increases.

*Proof.* Line L1 picks $k$ distinct points $u \ne v$ and stores $\sigma(v, u)$. The lists change only in UPDATE$(B[u_1], u_2, l)$ with $l = \sigma(u_1, u_2)$ and $u_2 \ne u_1$ (line L8). It inserts only if $u_2 \notin B[u_1]$, so the points stay distinct and different from $u_1$, it replaces one entry, so the size stays $k$, and it stores the correct distance. It inserts only if $\pi_{u_1}(u_2) < \max B[u_1]$, and it removes the entry of that maximum. The other $k - 1$ entries are below the old maximum, and so is the new one, so the new maximum is smaller than the old one. $\square$

**Lemma 2 (termination).** Let $\Phi = \sum_v \sum_{u \in B[v]} \mathrm{rank}_v(u)$. Each update lowers $\Phi$ by at least 1, and $\Phi$ starts at most $n k (n - 1 - k)$ above its least possible value. So there are at most $n k (n - 1 - k)$ updates. With $\delta = 0$ there are at most $n k (n - 1 - k) + 1$ rounds, and with $\delta > 0$ at most $(n - 1 - k)/\delta + 1$.

*Proof.* An update of $B[u_1]$ replaces the entry of rank $\mathrm{rank}_{u_1}$ of the maximum by a point of smaller rank, so $\Phi$ drops by at least 1. For one list, the sum of $k$ distinct ranks in $\{1, \ldots, n - 1\}$ lies between $1 + \cdots + k$ and $(n - k) + \cdots + (n - 1)$, which differ by $k(n - 1 - k)$; summing over the $n$ lists bounds the total decrease, and so the number of updates. Every round except the last one has $c > \delta n k$ updates by line L11. With $\delta = 0$ that means at least one update, which gives the first bound on rounds. With $\delta > 0$, if there are $T$ rounds, then $(T - 1)\delta n k < n k (n - 1 - k)$, so $T < (n - 1 - k)/\delta + 1$. $\square$

For local optimality, assume no sampling ($s \ge$ every list size, so lines L4 and L7 take everything) and $\delta = 0$. Call an *entry* an occurrence of a point $u$ in a list $B[w]$, from the moment UPDATE or line L1 puts it there until it is removed. An entry is flagged new when it is created, and only line L4 changes its flag, to old.

**Lemma 3 (a compared pair stays settled).** Say that $(u_1, u_2)$ is *settled* when $u_2 \in B[u_1]$ or $\pi_{u_1}(u_2) > \max B[u_1]$. After line L10 compares $u_1$ and $u_2$, both $(u_1, u_2)$ and $(u_2, u_1)$ are settled, and they stay settled until the end.

*Proof.* Take $(u_1, u_2)$; the other pair is symmetric, since line L10 calls UPDATE in both directions. Right after UPDATE$(B[u_1], u_2, l)$, either $u_2 \in B[u_1]$ (it was there or it was inserted), or the insertion was refused with $u_2 \notin B[u_1]$ and $\pi_{u_1}(u_2) \ge \max B[u_1]$; the maximum is $\pi_{u_1}(w)$ for some $w \ne u_2$, so the inequality is strict. Now consider a later change of $B[u_1]$. If $u_2 \notin B[u_1]$, the maximum does not increase by Lemma 1, so the inequality stays. If $u_2 \in B[u_1]$ and it is not the removed entry, $u_2$ stays. If $u_2$ is removed, it was the maximum, the other $k - 1$ entries were below $\pi_{u_1}(u_2)$, and the new one is below it too, so afterwards $\pi_{u_1}(u_2) > \max B[u_1]$. $\square$

**Lemma 4 (every entry is joined once).** With no sampling, every entry that exists at the start of some round and is new then is flagged old in line L4 of that round; and every entry present at the end was new at the start of some round and has existed since then.

*Proof.* The first claim is line L4 with no sampling. For the second, take an entry present at the end. If line L1 made it, it was new at the start of round 1. Otherwise UPDATE made it during some round $r$. Round $r$ is not the last round, since the last round has $c = 0$ and so no update. So round $r + 1$ exists, and at its start the entry exists (it is present at the end, and an entry once removed is gone) and is still new, since only line L4 changes flags and line L4 of round $r$ ran before the entry existed. $\square$

**Theorem (local optimality).** With no sampling and $\delta = 0$, at the end, for every $v$ and all distinct $u_1, u_2 \in \bar N[v] = B[v] \cup R[v]$, the pair $(u_1, u_2)$ is settled.

*Proof.* Membership $u_i \in \bar N[v]$ is witnessed by an entry $e_i$: the entry of $u_i$ in $B[v]$, or the entry of $v$ in $B[u_i]$. Both entries are present at the end. By Lemma 4, $e_i$ was new at the start of some round $t_i$ and has existed since; let $t_i$ be that round. Rename so that $t_1 \le t_2$. Consider round $t_2$. At its start, $e_2$ is new, so in line L4 (if $e_2$ is in $B[v]$) or line L5 then L7 (if $e_2$ is the entry of $v$ in $B[u_2]$), $u_2$ joins $new[v]$. Also $e_1$ exists at the start of round $t_2$. If $t_1 = t_2$, it is new and $u_1$ joins $new[v]$ the same way. If $t_1 < t_2$, line L4 of round $t_1$ made it old and it has stayed old, so line L3 or lines L5 and L7 put $u_1$ in $old[v]$. Either way $u_2 \in new[v]$ and $u_1 \in new[v] \cup old[v]$ with $u_1 \ne u_2$, so line L8 compares them in round $t_2$, and by Lemma 3 the pair $(u_1, u_2)$ is settled from then to the end. $\square$

**Corollary.** With no sampling and $\delta = 0$, at the end, if $v \ne w$, $w \notin B[v]$, and $v, w \in \bar N[u]$ for some $u$, then $\pi_v(w) > \max B[v]$: no neighbor of a neighbor of $v$, in the graph of all lists, could enter $B[v]$.

*Proof.* Apply the theorem with center $u$, $u_1 = v$ and $u_2 = w$. Since $w \notin B[v]$, the pair is settled by the second clause. $\blacksquare$
