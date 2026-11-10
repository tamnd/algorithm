---
title: The Hochbaum-Shmoys scheme returns a schedule of makespan at most (1 + 1/k) OPT
proves: [correctness, time.worst]
status: full
---

**Statement.** Let $p_1, \ldots, p_n$ be positive integers, $m \ge 1$ and $k \ge 1$ integers. (a) If DUAL-TEST$(p, m, T, k)$ returns a schedule, its makespan is at most $(1 + 1/k) T$. (b) If $\mathrm{OPT} \le T$, DUAL-TEST does not return NO. (c) HS-PTAS returns a schedule of makespan at most $(1 + 1/k)\,\mathrm{OPT}$. (d) HS-PTAS runs in time $O\bigl((n+1)^{d}(k+1)^{d} d \log P\bigr)$ with $d \le k^2 - k + 1$ and $P = \sum_j p_j$.

**Setup.** We use the pseudocode of the page, with $u = T/k^2$. For a large job $j$ we have $p_j > T/k = k u$. The rounded size is $r_j = \lfloor p_j/u \rfloor u$, so $p_j - u < r_j \le p_j$, and $r_j \ge k u$ because $p_j / u > k$ and $k$ is an integer. A *rounded multiset* is a vector $v = (v_1, \ldots, v_d)$ that counts the rounded large jobs of each size $s_i$. A machine *holds* $v$ if $\sum_i v_i s_i \le T$.

**Lemma 1 (few large jobs per machine).** A machine that holds a non-empty rounded multiset $c$ has $\sum_i c_i \le k$.

*Proof.* Each rounded size is at least $k u = T/k$. So $\bigl(\sum_i c_i\bigr) T/k \le \sum_i c_i s_i \le T$, and $\sum_i c_i \le k$. $\square$

**Lemma 2 (the table).** For each $v$ with $0 \le v \le (n_1, \ldots, n_d)$, the value $M[v]$ of line L6 is the least number of machines into which the rounded multiset $v$ can be split so that each machine holds its part.

*Proof.* By induction on $\sum_i v_i$. For $v = 0$, zero machines suffice and $M[0] = 0$. Let $v \ne 0$. Each vector $v - c$ in the minimum of L6 is smaller than $v$ in lexicographic order, because $c \ne 0$ and $c \ge 0$; so its entry is already computed when L6 reaches $v$. The minimum is not empty: the vector $c = e_i$ with one job of a size $s_i$ present in $v$ is a configuration, since $s_i \le r_j \le p_j \le T$ by line L1. *Upper bound.* For a configuration $c \le v$, put $c$ on one machine and split $v - c$ with $M[v - c]$ machines, by the induction hypothesis; this uses $1 + M[v - c]$ machines. *Lower bound.* Take a split of $v$ into $q$ machines, each holding its part, with $q$ least. Some part $c$ is non-empty (as $v \ne 0$), so it is a configuration with $c \le v$, and the other $q - 1$ parts split $v - c$. By the induction hypothesis $q - 1 \ge M[v - c]$, so $q \ge 1 + M[v - c] \ge M[v]$. $\square$

**Proof of (a).** Suppose DUAL-TEST returns a schedule. By Lemma 2 and line L7, line L8 uses $M[n] \le m$ machines, and machine $i$ gets the jobs of a configuration $c^{(i)}$. Its true load of large jobs is
$$\sum_{j \text{ on } i} p_j < \sum_{j \text{ on } i} (r_j + u) = \sum_t c^{(i)}_t s_t + u \sum_t c^{(i)}_t \le T + k u = T + T/k,$$
by Lemma 1. So each machine has load at most $(1 + 1/k) T$ after line L8. In line L9 a small job $j$ goes only to a machine $i$ with load at most $T$, and $p_j \le T/k$, so the new load is at most $(1 + 1/k) T$. A load that is already at most $(1 + 1/k) T$ does not change when other machines get jobs. So at line L10 every load is at most $(1 + 1/k) T$. $\square$

**Proof of (b).** Suppose a schedule $\sigma$ has makespan at most $T$. Then $p_j \le T$ for each $j$, so line L1 does not return NO. For a machine $i$ of $\sigma$, let $c^{(i)}$ count its large jobs by rounded size. Since $r_j \le p_j$, its rounded load is at most its true load, which is at most $T$. So the non-empty vectors $c^{(i)}$ split $(n_1, \ldots, n_d)$ into at most $m$ parts, each held by one machine, and Lemma 2 gives $M[n] \le m$. Line L7 does not return NO. Now consider a small job $j$ in line L9. The jobs placed so far do not include $j$, so their total load is at most $P - p_j$. And $P \le m T$, because $\sigma$ has $m$ loads of at most $T$. Since $p_j > 0$, the total placed load is less than $mT$, and the least load is less than $T$. So line L9 does not return NO. $\square$

**Proof of (c).** All loads and $\mathrm{OPT}$ are integers. We show that the loop of lines B3 to B5 keeps the invariant: $\mathrm{OPT} > lo$, and $S$ is a schedule with makespan at most $(1 + 1/k)\,hi$.

- *Initialization.* $\mathrm{OPT} \ge \max_j p_j$, and $\mathrm{OPT} \ge \sum_j p_j / m$ because some machine has at least the average load; as $\mathrm{OPT}$ is an integer, $\mathrm{OPT} \ge LB > lo$. A greedy schedule that puts each job on a least loaded machine has makespan at most $\sum_j p_j / m + \max_j p_j \le 2 LB$: when the last job $j$ of the fullest machine was placed, that machine had the least load, so its load was at most $(\sum_j p_j - p_j)/m$. So $\mathrm{OPT} \le 2LB = hi$, and by (b) DUAL-TEST$(p, m, hi, k)$ returns a schedule $S$, which by (a) has makespan at most $(1 + 1/k)\,hi$.
- *Maintenance.* If the test at $mid$ returns NO, then by (b) $\mathrm{OPT} > mid$, so $lo \leftarrow mid$ keeps the first part. If it returns a schedule, by (a) its makespan is at most $(1 + 1/k)\,mid$, so $hi \leftarrow mid$ and $S \leftarrow S'$ keep the second part.
- *Termination.* While $hi - lo > 1$ we have $lo < mid < hi$, so $hi - lo$ drops by at least 1 in each step and becomes 1.

At the end $hi = lo + 1$ and $\mathrm{OPT} > lo$, so $\mathrm{OPT} \ge hi$ because both are integers. The returned $S$ has makespan at most $(1 + 1/k)\,hi \le (1 + 1/k)\,\mathrm{OPT}$. $\square$

**Proof of (d).** The rounded sizes are the multiples $a u$ with $k \le a \le k^2$, because $k u \le r_j \le p_j \le T = k^2 u$. So $d \le k^2 - k + 1$. The table of L6 has $\prod_i (n_i + 1) \le (n+1)^d$ entries. By Lemma 1 a configuration has $c_i \le k$ for each $i$, so there are at most $(k+1)^d$ configurations, and each entry of L6 costs $O((k+1)^d d)$. Lines L1 to L5, L8 and L9 cost $O(n m + (k+1)^d d)$, or $O(n \log m)$ for L9 with a heap. In the search, $hi - lo$ starts at $LB + 1$ and the update keeps at most $\lceil (hi - lo)/2 \rceil$, so after $\lceil \log_2(LB + 1) \rceil$ steps it is 1. As $LB \le P$, there are $O(\log P)$ calls. $\blacksquare$
