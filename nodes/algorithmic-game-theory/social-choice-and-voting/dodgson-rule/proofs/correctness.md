---
title: Correctness and properties of the Dodgson score algorithm
proves: [correctness]
status: full
---

Let $A = \{0, \ldots, m - 1\}$ with $m \ge 2$, let $P = (r_1, \ldots, r_n)$ be a profile of $n \ge 1$ rankings, let $N(x, y)$ be the number of voters who rank $x$ above $y$, and let $q = \lfloor n/2 \rfloor + 1$. Candidate $c$ is a Condorcet winner of a profile exactly when $N(c, b) \ge q$ for every $b \ne c$. For a ballot $r$ where $c$ is in place $\ell$ and $0 \le k \le \ell$, let $\mathrm{up}_k(r)$ be $r$ with $c$ moved up $k$ places; it costs $k$ swaps, and $c$ passes the $k$ candidates just above it. The distance between two profiles is the least number of swaps that turns one into the other; for two rankings it is the number of pairs they order differently, so for profiles it is the sum of these numbers over the ballots.

**Claim 1 (moving up is enough).** $\mathrm{sc}(c)$ equals the least $\sum_i k_i$ over the choices $0 \le k_i \le \ell_i$ for which $c$ is a Condorcet winner of $(\mathrm{up}_{k_1}(r_1), \ldots, \mathrm{up}_{k_n}(r_n))$.

*Proof.* Each such profile is reached by $\sum_i k_i$ swaps, so $\mathrm{sc}(c)$ is at most the least sum. For the other direction, let $Q = (s_1, \ldots, s_n)$ be a profile where $c$ is a Condorcet winner, reached from $P$ with $\mathrm{sc}(c)$ swaps; so the distance from $P$ to $Q$ is at most $\mathrm{sc}(c)$. On ballot $i$, let $U_i$ be the set of candidates above $c$ in $r_i$ and below $c$ in $s_i$. If $U_i$ is empty, let $k_i = 0$. Otherwise let $u$ be the member of $U_i$ highest in $r_i$, and let $k_i$ be the number of candidates from $u$ down to just above $c$ in $r_i$, $u$ included. Every such candidate $v$ gives a pair that $r_i$ and $s_i$ order differently: if $v$ is below $c$ in $s_i$, the pair $\{v, c\}$; otherwise $v$ is above $c$ and so above $u$ in $s_i$, while $u$ is above $v$ in $r_i$, and the pair is $\{u, v\}$. These pairs are distinct, so the distance between $r_i$ and $s_i$ is at least $k_i$, and $\sum_i k_i \le \mathrm{sc}(c)$. Moving $c$ up $k_i$ places in $r_i$ passes a superset of $U_i$. So in $Q' = (\mathrm{up}_{k_i}(r_i))_i$, for each $b \ne c$, $c$ is above $b$ on every ballot where it is above $b$ in $Q$: either $c$ was above $b$ in $r_i$, and moving $c$ up keeps this, or $b \in U_i$. So $N_{Q'}(c, b) \ge N_Q(c, b) \ge q$, and $c$ is a Condorcet winner of $Q'$.

**Claim 2 (invariant).** For a choice of $k_1, \ldots, k_i$ on the first $i$ ballots, let its deficit vector be $d[b] = \max(0, q - N(c, b) - g_b)$, where $g_b$ is the number of ballots $j \le i$ on which $b$ is among the $k_j$ candidates just above $c$. After line L9 has run for the first $i$ ballots, $F$ maps exactly the deficit vectors of such choices, each to the least $\sum_{j \le i} k_j$ that gives it.

*Proof.* By induction on $i$. For $i = 0$ the only choice is empty, its deficit vector is the one of line L2, and its cost is 0, as set by line L3. Assume the claim after $i - 1$ ballots. A choice for $i$ ballots is a choice for $i - 1$ ballots followed by a $k_i$, and the new deficit vector depends only on the old one and $k_i$: each candidate passed on ballot $i$ has its deficit lowered by 1, not below 0, which is line L7. So the vectors reachable after $i$ ballots are those of line L7 applied to the keys of $F$. For a vector $d'$, a cheapest choice that reaches it ends with some $k_i$ after a choice with some vector $d$. Replacing that first part by a cheapest choice with vector $d$ gives the same $d'$ at no larger cost. So the least cost of $d'$ is the least $F[d] + k_i$ over the pairs $(d, k_i)$ that lead to $d'$, which is what lines L6 and L8 compute.

**Claim 3 (correctness).** DODGSON-SCORE returns $\mathrm{sc}(c)$, and line L11 returns the Dodgson winner with the smallest index.

*Proof.* The choice $k_i = \ell_i$ for all $i$ puts $c$ on top of every ballot, so $N(c, b) = n \ge q$ and the zero vector is reached; line L10 finds a key. A choice has deficit vector zero exactly when $c$ is a Condorcet winner of the resulting profile. By Claim 2, line L10 returns the least $\sum_i k_i$ among those choices, which is $\mathrm{sc}(c)$ by Claim 1. Line L11 compares the scores of all candidates.

**Claim 4 (Condorcet consistency).** $\mathrm{sc}(c) = 0$ exactly when $c$ is a Condorcet winner of $P$, so a Condorcet winner is the unique winner.

*Proof.* Zero swaps leave $P$ unchanged. Every other candidate has a positive score, since there is at most one Condorcet winner.

**Claim 5 (Pareto).** If every voter ranks $a$ above $b$, then $\mathrm{sc}(a) < \mathrm{sc}(b)$.

*Proof.* By Claim 1, take $k_i$ with sum $\mathrm{sc}(b)$ such that $b$ is a Condorcet winner of $Q = (\mathrm{up}_{k_i}(r_i))_i$, where the moves are of $b$. Not all $k_i$ are 0, because $b$ loses to $a$ in $P$. On ballot $i$, let $\delta_i \ge 1$ be the number of places between $a$ and $b$, so $a$ is $\delta_i$ places above $b$. Move $a$ up $k'_i = \max(0, k_i - \delta_i)$ places instead. Then $k'_i \le k_i$, with $k'_i < k_i$ when $k_i > 0$, so $\sum_i k'_i < \mathrm{sc}(b)$. In the new ballot, $a$ is above every $x \ne a$ that $b$ is above in $\mathrm{up}_{k_i}(r_i)$: such an $x$ is below $b$ in $r_i$, or between $a$ and $b$, or above $a$ and passed by $b$, and then it is passed by $a$ too, because $b$ passes the $k_i - \delta_i$ candidates just above $a$ after it passes $a$. So in the new profile $N(a, x) \ge N_Q(b, x) \ge q$ for every $x \ne a, b$, and $N(a, b) = n \ge q$. So $a$ is a Condorcet winner after fewer than $\mathrm{sc}(b)$ swaps.

**Claim 6 (anonymity and neutrality).** Reordering the voters does not change any score. Renaming the candidates by a permutation $\pi$ maps the score of $c$ to the score of $\pi(c)$.

*Proof.* A swap sequence for one profile becomes, by reordering the ballots or by renaming the candidates, a swap sequence of the same length for the other, and being a Condorcet winner is kept by both changes.

**Claim 7 (time).** DODGSON-SCORE runs in $O(m^2 n (n/2 + 2)^{m - 1})$ time and $O(m (n/2 + 2)^{m - 1})$ space.

*Proof.* Each of the $m - 1$ deficits lies in $\{0, \ldots, q\}$ with $q \le n/2 + 1$, so $F$ and $G$ have at most $(n/2 + 2)^{m - 1}$ keys of $m - 1$ entries each. Line L1 takes $O(n m^2)$ time. For each of the $n$ ballots, lines L6 to L8 try at most $m$ values of $k$ for each key, and each value takes $O(m)$ time to build and look up the new vector. Line L11 calls DODGSON-SCORE $m$ times. $\blacksquare$
