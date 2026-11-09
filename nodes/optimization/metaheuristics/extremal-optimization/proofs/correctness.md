---
title: Extremal optimization returns the best solution it saw, and with a finite tau it sees a ground state with probability tending to 1
proves: [correctness]
status: full
---

We use the pseudocode of the page for the $\pm J$ spin glass. There are $n$ spins $s_i \in \{-1, +1\}$, symmetric couplings $J_{ij} = J_{ji}$ with $J_{ii} = 0$, the energy $E(s) = -\sum_{i<j} J_{ij} s_i s_j$ and the local fitness $\lambda_i(s) = s_i \sum_{j \ne i} J_{ij} s_j$. We write $s^{(t)}$ for the spins after step $t$, with $s^{(0)}$ the start.

**Claim 1 (the returned solution).** After step $t$, $best \in \{s^{(0)}, \dots, s^{(t)}\}$ and $E(best) = \min\{E(s^{(0)}), \dots, E(s^{(t)})\}$.

*Proof.* By induction on $t$. Line L1 gives the claim for $t = 0$. At step $t$, line L6 always sets a new $s^{(t)}$, and line L7 replaces $best$ by it exactly when $E(s^{(t)}) < E(best)$, which is the old minimum. So the new $E(best)$ is the minimum including $E(s^{(t)})$, and $best$ is a visited state. $\square$

**Claim 2 (the energy and one flip).** $E(s) = -\tfrac{1}{2}\sum_i \lambda_i(s)$, and if $s'$ is $s$ with spin $i$ flipped, then $E(s') - E(s) = 2\lambda_i(s)$.

*Proof.* $\sum_i \lambda_i(s) = \sum_i \sum_{j \ne i} J_{ij} s_i s_j$ counts each unordered pair $\{i, j\}$ twice, once as $(i, j)$ and once as $(j, i)$, with the same value since $J_{ij} = J_{ji}$. So it equals $2\sum_{i<j} J_{ij} s_i s_j = -2E(s)$. For the flip, the terms of $E$ that do not contain $i$ do not change, and each term $-J_{ij} s_i s_j$ with $j \ne i$ changes sign. So $E(s') - E(s) = 2\sum_{j \ne i} J_{ij} s_i s_j = 2\lambda_i(s)$. $\square$

**Claim 3 (every spin can be flipped).** Let $\tau < \infty$ and $p = n^{-\tau}/\sum_{m=1}^n m^{-\tau}$. At each step, given the whole past, each spin $i$ is flipped with probability at least $p$.

*Proof.* Line L4 gives a permutation $\pi$ of the spins that depends only on the current state, so spin $i$ has a unique rank $r$ with $\pi(r) = i$. Line L5 draws $k = r$ with probability $r^{-\tau}/\sum_m m^{-\tau}$, using a fresh random number. Since $r \le n$ and $\tau \ge 0$, $r^{-\tau} \ge n^{-\tau}$, and this probability is at least $p$. Line L6 then flips spin $\pi(k) = i$. $\square$

**Claim 4 (a ground state is seen with probability tending to 1).** Let $g$ be a ground state. For $\tau < \infty$ and any start, the probability that none of $s^{(0)}, \dots, s^{(K)}$ equals $g$ is at most $(1 - p^n)^{\lfloor K/n \rfloor}$. So $E(best) = \min E$ with probability at least $1 - (1 - p^n)^{\lfloor K/n \rfloor}$.

*Proof.* Fix a block of $n$ consecutive steps, starting from a state $s$. Let $D$ be the set of spins where $s$ and $g$ differ, with $|D| = d \le n$, and list them as $i_1, \dots, i_d$. If the first $d$ steps of the block flip $i_1, \dots, i_d$ in this order, then after them the state is $g$. By Claim 3 and the chain rule, this happens with probability at least $p^d \ge p^n$, whatever $s$ is, since $p \le 1$. So, given everything before the block, the block misses $g$ with probability at most $1 - p^n$. The $\lfloor K/n \rfloor$ disjoint blocks inside the first $K$ steps give the product bound by the chain rule. If $g$ is visited, Claim 1 gives $E(best) = E(g)$. $\square$

**Remarks.** Claim 4 holds for any walk that can flip each spin with probability at least $p$, including a random walk, so it says nothing about why EO works well. The bound is very weak: for $n = 12$ and $\tau = 1.4$, $p \approx 0.014$ and $p^{12} \approx 10^{-22}$. For $\tau = \infty$ (basic EO), Claim 3 fails, since only rank 1 is ever drawn, and the walk is a deterministic map on a finite set once ties are fixed, so it ends in a cycle that may contain no ground state. The tests check Claim 2 on 50 random states, the law of line L5 within 0.01 on 100000 draws, Claim 1 on 10 runs, and that seed 0 with $\tau = 1 + 1/\ln 12$ reaches the ground energy $-28$ of the instance with 12 spins.
