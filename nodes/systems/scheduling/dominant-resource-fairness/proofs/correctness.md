---
title: Progressive filling gives a feasible, Pareto efficient, envy-free allocation with the sharing incentive, and it is the leximin optimum of the dominant shares
proves: [correctness, termination]
status: full
---

The capacities are $C_r > 0$ and one task of user $i$ needs $D_{ir} \ge 0$, with some $D_{ir} > 0$. Let $d_i = \max_r D_{ir}/C_r > 0$. An allocation gives $x_i \ge 0$ tasks to user $i$, with dominant share $s_i = x_i d_i$. Note that $D_{ir} \le d_i C_r$ for every $r$. Say that user $i$ *needs* resource $r$ if $D_{ir} > 0$, and that $r$ is *full* if $\sum_i x_i D_{ir} = C_r$.

**Lemma 1 (one pass).** At the start of each pass every resource is used at most to its capacity, the level $s$ chosen at line L4 is at least the level of the pass before, and after the pass the resources in $R^*$ are full and at least one more user is frozen.

*Proof.* At level $s$, with $x_i = s / d_i$ for the active users, the use of resource $r$ is $u_r(s) = \sum_{\text{frozen}} x_i D_{ir} + s \sum_{\text{active}} D_{ir}/d_i$, which is linear and does not fall in $s$. A resource with rate 0 has a fixed use, and it was at most $C_r$ before. For a resource with a positive rate, $s_r$ of line L3 is the level with $u_r(s_r) = C_r$. At the previous level $s'$ (or $0$ in the first pass) the use is at most $C_r$, so $s_r \ge s'$. Line L4 takes $s = \min_r s_r$, so $u_r(s) \le C_r$ for every $r$, with equality for $r \in R^*$. A resource in $R^*$ has a positive rate, so some active user needs it, and line L6 freezes that user. $\square$

**Termination.** Each pass freezes at least one user (Lemma 1), so there are at most $n$ passes. The final allocation is feasible by Lemma 1. A frozen user keeps its tasks, so its dominant share $s_i$ is the level of the pass in which it was frozen, and these levels do not fall from pass to pass.

**Lemma 2 (bottleneck).** Every user $i$ needs a resource $b(i)$ that is full at the end, and every user $j$ that needs $b(i)$ has $s_j \le s_i$.

*Proof.* Let user $i$ be frozen in the pass that makes $b(i) \in R^*$ full. After this pass, every user that needs $b(i)$ is frozen (line L6 freezes the active ones, and the others were frozen before), so the use of $b(i)$ never changes again and $b(i)$ stays full. A user $j$ that needs $b(i)$ was frozen in this pass or an earlier one, so its level is at most the level of $i$. $\square$

**Theorem 1 (sharing incentive).** $s_i \ge 1/n$ for every user $i$. An equal split, which gives every user $C_r/n$ of each resource, gives user $i$ exactly $\min_r C_r/(n D_{ir}) = 1/(n d_i)$ tasks, which is a dominant share of $1/n$; so DRF gives each user at least what the equal split gives it.

*Proof.* In the first pass every user is active, and $s_r = C_r / \sum_i D_{ir}/d_i \ge C_r / (n C_r) = 1/n$, because $D_{ir}/d_i \le C_r$. So the first level is at least $1/n$, and the levels do not fall. $\square$

**Theorem 2 (Pareto efficiency).** No feasible allocation $y$ has $y_i \ge x_i$ for every $i$ and $y_k > x_k$ for some $k$.

*Proof.* Let $b = b(k)$ from Lemma 2. Then $\sum_i y_i D_{ib} \ge \sum_i x_i D_{ib} + (y_k - x_k) D_{kb} > C_b$, because $b$ is full under $x$ and $D_{kb} > 0$. So $y$ is not feasible. $\square$

**Theorem 3 (envy-freeness).** For all users $i \ne j$, the bundle of $j$ lets user $i$ run at most $x_i$ tasks: $\min_{r : D_{ir} > 0} x_j D_{jr} / D_{ir} \le x_i$.

*Proof.* Let $b = b(i)$. If $D_{jb} = 0$, the term for $r = b$ is 0. Otherwise $j$ needs $b$, so $s_j \le s_i$ by Lemma 2. Let $r_i$ be the dominant resource of $i$, so $D_{ir_i} = d_i C_{r_i} > 0$. Then the term for $r = r_i$ is $x_j D_{jr_i} / (d_i C_{r_i}) \le x_j d_j / d_i = s_j / d_i \le s_i / d_i = x_i$. $\square$

**Theorem 4 (max-min property).** Let $y$ be any feasible allocation with dominant shares $t_i = y_i d_i$. If $t_i > s_i$, then some user $j$ has $s_j \le s_i$ and $t_j < s_j$.

*Proof.* Let $b = b(i)$. Since $\sum_j y_j D_{jb} \le C_b = \sum_j x_j D_{jb}$, and $y_i D_{ib} > x_i D_{ib}$, some user $j$ with $D_{jb} > 0$ has $y_j < x_j$, so $t_j < s_j$. By Lemma 2, $s_j \le s_i$. $\square$

**Corollary (leximin).** For every feasible $y$ with $t \ne s$, the sorted vector of $t$ is smaller than the sorted vector of $s$ in lexicographic order. So DRF maximizes the smallest dominant share, and its dominant shares are the unique leximin optimum.

*Proof.* Let $L = \{ k : t_k \ne s_k \}$ and $\sigma = \min_{k \in L} s_k$. Some $k \in L$ has $s_k = \sigma$ and $t_k < \sigma$: take any $k \in L$ with $s_k = \sigma$; if $t_k > s_k$, Theorem 4 gives $j$ with $s_j \le \sigma$ and $t_j < s_j$, so $j \in L$, $s_j = \sigma$, and we take $j$. Now let $u = \min_{k \in L} t_k < \sigma$. Outside $L$ the two vectors agree. Inside $L$, all entries of $s$ are at least $\sigma > u$, and all entries of $t$ are at least $u$, with at least one equal to $u$. So both vectors have the same entries below $u$, but $t$ has more entries equal to $u$ than $s$. Thus at the first position where the sorted vectors differ, $t$ has the value $u$ and $s$ has a larger value. $\square$

**Not proved here.** The paper also proves strategy-proofness: no user can get more tasks by reporting a demand vector other than its true one. The tests check Lemma 1, Theorems 1 to 4 and the corollary on random instances, the corollary against a brute force over a grid of dominant shares, and the paper's example. $\blacksquare$
