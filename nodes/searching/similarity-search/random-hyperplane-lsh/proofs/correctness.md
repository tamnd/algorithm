---
title: Random hyperplanes collide with probability 1 − θ/π, and the L-table query succeeds with probability at least 1 − 1/e − 1/3
proves: [correctness]
status: full
---

We use the names of the pseudocode on the page. All vectors are nonzero, and $\theta(x, y) \in [0, \pi]$ is the angle between $x$ and $y$.

**Lemma 1 (one hyperplane).** Let $r \in \mathbb{R}^d$ have independent $N(0, 1)$ coordinates, and let $b_r(x) = 1$ if $r \cdot x \ge 0$ and $0$ otherwise. Then $\Pr[b_r(x) = b_r(y)] = 1 - \theta(x, y)/\pi$.

*Proof.* If $x$ and $y$ are parallel, then either $y = \lambda x$ with $\lambda > 0$, the angle is 0 and the bits are always equal, or $\lambda < 0$, the angle is $\pi$, and the bits differ unless $r \cdot x = 0$, an event of probability 0. Otherwise $x$ and $y$ span a plane $W$. Write $r = s + t$ with $s \in W$ and $t \perp W$; then $r \cdot x = s \cdot x$ and $r \cdot y = s \cdot y$. The standard Gaussian is invariant under orthogonal maps, so in an orthonormal basis of $W$ the two coordinates of $s$ are independent $N(0,1)$, and the direction of $s$ is uniform on the unit circle of $W$, and $s \ne 0$ with probability 1. Let $\phi$ be that direction. Then $s \cdot x \ge 0$ exactly when $\phi$ lies in the closed half circle centered at the direction of $x$, and the same for $y$. The two half circles are centered at directions an angle $\theta$ apart, so their symmetric difference is two arcs of length $\theta$ each, of total measure $2\theta$ out of $2\pi$. The bits differ exactly when $\phi$ lies in this symmetric difference (up to the endpoints, of measure 0). So $\Pr[b_r(x) \ne b_r(y)] = 2\theta/(2\pi) = \theta/\pi$. $\square$

**Lemma 2 (one table).** For one table $\ell$, with $k$ hyperplanes drawn independently in line L3, $\Pr[\mathrm{HASH}(x, R_\ell) = \mathrm{HASH}(y, R_\ell)] = (1 - \theta(x,y)/\pi)^k$.

*Proof.* By line L1 the keys are equal exactly when all $k$ bits agree. The bits use independent vectors $r_1, \ldots, r_k$, so the events are independent, and each has probability $1 - \theta/\pi$ by Lemma 1. $\square$

**Lemma 3 (soundness).** Whatever the random choices, QUERY returns either "none" or a vector $x \in P$ with $\theta(q, x) \le \theta_2$.

*Proof.* Every bucket holds only vectors of $P$, inserted in line L4. The only line that returns a vector is L8, and it tests $\theta(q, x) \le \theta_2$ first. $\square$

**Theorem.** Let $0 < \theta_1 < \theta_2 < \pi$, $p_1 = 1 - \theta_1/\pi$, $p_2 = 1 - \theta_2/\pi$, $\rho = \ln(1/p_1)/\ln(1/p_2)$, $k = \lceil \log_{1/p_2} n \rceil$ and $L = \lceil n^{\rho}/p_1 \rceil$, with $n = |P| \ge 2$. If some $p^* \in P$ has $\theta(q, p^*) \le \theta_1$, then QUERY returns a vector within angle $\theta_2$ of $q$ with probability at least $1 - 1/e - 1/3$.

*Proof.* Define two events over the random hyperplanes.

$E_1$: for every $\ell$, $p^*$ is not in the bucket $T_\ell[\mathrm{HASH}(q, R_\ell)]$. Since $1 - \theta/\pi$ decreases in $\theta$ and $\theta(q, p^*) \le \theta_1$, Lemma 2 gives a collision probability of at least $p_1^k$ in each table, and the tables are independent, so $\Pr[E_1] \le (1 - p_1^k)^L \le e^{-L p_1^k}$. Now $k \le \log_{1/p_2} n + 1$, so $p_1^k \ge p_1 \cdot p_1^{\log_{1/p_2} n} = p_1 \cdot n^{-\ln(1/p_1)/\ln(1/p_2)} = p_1 n^{-\rho}$. With $L \ge n^{\rho}/p_1$ this gives $L p_1^k \ge 1$ and $\Pr[E_1] \le 1/e$.

$E_2$: the number $F$ of pairs $(\ell, x)$ with $x$ in the bucket of $q$ in table $\ell$ and $\theta(q, x) > \theta_2$ is at least $3L$. For each such $x$ and $\ell$, Lemma 2 gives a probability at most $p_2^k \le p_2^{\log_{1/p_2} n} = 1/n$. There are at most $n$ such $x$ and $L$ tables, so by linearity of expectation $\mathbb{E}[F] \le L$. By Markov's inequality, $\Pr[E_2] = \Pr[F \ge 3L] \le L/(3L) = 1/3$.

Assume neither event happens. Each execution of line L9 follows a failed test in line L8, so it counts a pair $(\ell, x)$ with $x$ in the bucket of $q$ in table $\ell$ and $\theta(q, x) > \theta_2$, and different executions count different pairs. Since $F < 3L$, the counter $c$ stays below $3L$, and line L10 never returns. So the loops run until line L8 returns a vector, or until every bucket of $q$ has been scanned. Since $E_1$ fails, $p^*$ is in one of these buckets, and line L8 returns when it reaches $p^*$, if not earlier. So QUERY returns a vector, and by Lemma 3 it is within $\theta_2$. By the union bound the probability of $E_1 \cup E_2$ is at most $1/e + 1/3$, so QUERY succeeds with probability at least $1 - 1/e - 1/3 \approx 0.2988$. $\blacksquare$
