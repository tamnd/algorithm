---
title: MOGA ranks keep dominance, and its fitness assignment keeps the total of each rank
proves: [correctness]
status: full
---

All objectives are minimized, $N$ is the population size, and line numbers refer to the `pseudo id=main` block of the MOGA page. MOGA is a heuristic. The statements below are about the fitness that it assigns and the sizes that it keeps; none of them says that MOGA reaches the Pareto front.

## The rank

Let $r(x) = 1 + \lvert D(x) \rvert$, where $D(x)$ is the set of members $z$ with $f(z) \prec f(x)$.

**Lemma 1.** (a) $r(x) = 1$ if and only if no member dominates $x$. (b) If $f(z) \prec f(x)$, then $r(z) < r(x)$.

*Proof.* (a) is the definition. (b) If $w \in D(z)$, then $f(w) \prec f(z) \prec f(x)$, so $w \in D(x)$ by transitivity. So $D(z) \subseteq D(x)$. Also $z \in D(x)$, and $z \notin D(z)$ because dominance is irreflexive. So $\lvert D(x) \rvert \ge \lvert D(z) \rvert + 1$. $\square$

## The averaged fitness

Line L4 sorts the members by rank and gives the member at position $k = 1, \ldots, N$ the raw value $N - k + 1$. Line L5 replaces the value of each member by the mean over the members of the same rank.

**Lemma 2.** (a) The values after line L5 sum to $N(N+1)/2$, and each rank keeps the sum of its raw values. (b) Members of equal rank get equal values. (c) If $r(x) < r(x')$, then the value of $x$ is larger than the value of $x'$.

*Proof.* (a) and (b): replacing the values of a group by their mean keeps the group sum, and the raw values are a permutation of $1, \ldots, N$. (c) The sort puts the members of each rank in one block of consecutive positions, and the block of the smaller rank comes first. Each raw value in the first block is larger than each raw value in the second block, so the mean of the first block is larger than the mean of the second. $\square$

The order of members inside a block does not matter after line L5, so the result does not depend on how the sort breaks ties.

## Sharing and scaling

Line L6 computes the niche count $m(x) = \sum_{z : r(z) = r(x)} \mathrm{sh}(d(x, z))$ with $\mathrm{sh}(d) = 1 - d/\sigma$ for $d < \sigma$ and $0$ otherwise. Line L7 sets $\varphi(x) = c_r\, F(x)/m(x)$, where $F$ is the value from line L5 and the factor $c_r$ for rank $r$ makes the sum of $\varphi$ over rank $r$ equal to the sum of $F$ over rank $r$.

**Lemma 3.** (a) $m(x) \ge 1$, so line L7 is well defined and $\varphi(x) > 0$. (b) The total of $\varphi$ over each rank equals the total of $F$ over that rank. (c) Inside one rank, $\varphi(x) > \varphi(x')$ if and only if $m(x) < m(x')$.

*Proof.* (a) The sum for $m(x)$ contains $z = x$ with $d = 0$ and $\mathrm{sh}(0) = 1$, and the other terms are non-negative. The values $F$ are positive, so the sum of $F/m$ over a rank is positive and $c_r$ exists and is positive. (b) is the choice of $c_r$. (c) Inside a rank, $F$ is constant by Lemma 2(b), so $\varphi = c_r F / m$ decreases as $m$ grows. $\square$

## Selection and population size

**Theorem 4.** Let the parents of line L8 be drawn by proportional selection or by stochastic universal sampling on $\varphi$. Then the expected number of parents with rank $r$ is

$$\frac{N \sum_{x : r(x) = r} F(x)}{N(N+1)/2},$$

which does not depend on $\sigma$. In particular, if $k$ members have rank 1, the expected number of parents of rank 1 is $\frac{2}{N+1} \sum_{j=0}^{k-1} (N - j)$.

*Proof.* Both selection schemes give member $x$ an expected count of $N \varphi(x) / \sum_z \varphi(z)$. By Lemma 3(b) and Lemma 2(a), the total over all members is $N(N+1)/2$, and the total over rank $r$ is the sum of $F$ over rank $r$. Sum the expected counts over the rank. The members of rank 1 take positions $1, \ldots, k$ in line L4, so their raw values are $N, N-1, \ldots, N-k+1$. $\square$

So sharing moves the expected share between members of one rank, toward members in less crowded regions of the objective space, and does not move it between ranks.

**Lemma 5.** Each generation keeps $\lvert P \rvert = N$, and line L10 returns a nonempty set of mutually non-dominated members of the last population.

*Proof.* Line L8 draws $N$ parents, and line L9 makes one offspring for each parent. The output is the set of rank-1 members, which is nonempty because a finite set with a strict partial order has a minimal element, and two rank-1 members do not dominate each other by Lemma 1(a). $\square$
