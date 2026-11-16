---
title: Why the chi-square gate has the stated probability, why the augmented matrix gives an optimal partial matching, and why GNN is never worse than the greedy rule
proves: [correctness]
status: full
---

Notation as on the page. There are $n$ tracks and $m$ measurements. The gated cost is $c_{ij} = d^2_{ij}$ if $d^2_{ij} \le \gamma$ and $c_{ij} = \infty$ otherwise. A partial matching $M$ is a set of pairs $(i, j)$ with finite $c_{ij}$ in which no track and no measurement appears twice. Its cost is $J(M) = \sum_{(i, j) \in M} c_{ij} + c_{\text{miss}} (n - |M|) + c_{\text{new}} (m - |M|)$, with $c_{\text{miss}}, c_{\text{new}} \ge 0$ finite. The claims are about one frame.

## Claim 1: the probability of the gate

Let $\nu = z - \hat z$ be Gaussian with mean 0 and a positive definite covariance $S$ in $\mathbb{R}^p$. Then $d^2 = \nu^{\mathsf T} S^{-1} \nu$ has the chi-square distribution with $p$ degrees of freedom. For $p = 2$, $\Pr(d^2 \le \gamma) = 1 - e^{-\gamma/2}$.

*Proof.* Let $S = L L^{\mathsf T}$ be the Cholesky factorization and $w = L^{-1} \nu$. Then $w$ is Gaussian with covariance $L^{-1} S L^{-\mathsf T} = I$, so its components are independent standard normal numbers. Also $\nu^{\mathsf T} S^{-1} \nu = \nu^{\mathsf T} L^{-\mathsf T} L^{-1} \nu = w^{\mathsf T} w = \sum_k w_k^2$, a sum of $p$ squares of independent standard normal numbers, which is the definition of the chi-square distribution with $p$ degrees of freedom. For $p = 2$ its density is $\tfrac12 e^{-x/2}$ on $x \ge 0$, and the integral from 0 to $\gamma$ is $1 - e^{-\gamma/2}$. $\square$

For $\gamma = 9.21$ this is $1 - e^{-4.605} = 0.9900$, and for $\gamma = 5.991$ it is $0.9500$. The claim needs the Gaussian model. With a wrong model, for example a maneuver that the motion model does not allow, the true measurement leaves the gate more often.

## Claim 2: the augmented matrix

Let $A$ be the $(n + m) \times (n + m)$ matrix of line L5. Rows $1, \ldots, n$ are the tracks, rows $n + 1, \ldots, n + m$ are dummy rows of the measurements. Columns $1, \ldots, m$ are the measurements, columns $m + 1, \ldots, m + n$ are dummy columns of the tracks. The entries are $A_{ij} = c_{ij}$ for a track and a measurement, $A_{i, m+i} = c_{\text{miss}}$ and $A_{i, m+k} = \infty$ for $k \ne i$, $A_{n+j, j} = c_{\text{new}}$ and $A_{n+j, k} = \infty$ for a measurement column $k \ne j$, and $A_{n+j, m+i} = 0$.

(a) Every partial matching $M$ gives a permutation $\sigma$ with $\sum_r A_{r \sigma(r)} = J(M)$.

(b) Every permutation $\sigma$ of finite cost gives the partial matching $M_\sigma = \{(i, \sigma(i)) : i \le n, \sigma(i) \le m\}$ with $J(M_\sigma) = \sum_r A_{r \sigma(r)}$.

(c) So if $\sigma$ is an optimal permutation, $M_\sigma$ is an optimal partial matching, and the two optimal costs are equal.

*Proof of (a).* Let $|M| = k$. Send each matched track $i$ to its measurement $j$, at cost $c_{ij}$. Send each unmatched track $i$ to its dummy column $m + i$, at cost $c_{\text{miss}}$. Send the dummy row of each unmatched measurement $j$ to column $j$, at cost $c_{\text{new}}$. So far the rows used are the $n$ track rows and the $m - k$ dummy rows of unmatched measurements, and the columns used are the $k$ matched measurement columns, the $n - k$ dummy columns of unmatched tracks, and the $m - k$ unmatched measurement columns. What is left is $k$ dummy rows of the matched measurements and $k$ dummy columns of the matched tracks. Pair them in any order, at cost 0 each, since the lower right block is all zero. Every row and every column is used once, so $\sigma$ is a permutation, and its cost is $\sum_{M} c_{ij} + (n - k) c_{\text{miss}} + (m - k) c_{\text{new}} = J(M)$.

*Proof of (b).* Since the cost is finite, no entry $\infty$ is used. Track row $i$ goes either to a measurement column $j$ with $c_{ij}$ finite, or to its own dummy column $m + i$. The pairs of the first kind form $M_\sigma$, and since $\sigma$ is a permutation, no measurement appears twice, so $M_\sigma$ is a partial matching. Let $k = |M_\sigma|$. The other $n - k$ tracks each pay $c_{\text{miss}}$. A measurement column $j$ is used by exactly one row. If $j$ is in $M_\sigma$, that row is a track row. Otherwise it is a dummy row, and the only finite entry of a dummy row in a measurement column is $A_{n+j, j}$, so the row is the dummy row of $j$, at cost $c_{\text{new}}$. That gives $m - k$ costs $c_{\text{new}}$. The remaining dummy rows go to dummy columns at cost 0. The total is $J(M_\sigma)$.

*Proof of (c).* By (a), the least permutation cost is at most $\min_M J(M)$. By (b), the cost of an optimal $\sigma$ equals $J(M_\sigma) \ge \min_M J(M)$. So the two minima are equal and $M_\sigma$ attains it. $\square$

The empty matching has the finite cost $n c_{\text{miss}} + m c_{\text{new}}$, so by (a) $A$ always has a permutation of finite cost and the solver of line L6 always returns one. The Hungarian algorithm with potentials returns a permutation of least cost on any matrix whose entries are finite or $\infty$ with at least one finite permutation; its correctness is proved on the [Hungarian algorithm](/hungarian-algorithm/) page. The code reports infeasibility when every unvisited column has reduced cost $\infty$, which cannot happen here.

## Claim 3: gated pairs are used

If $c_{ij} < c_{\text{miss}} + c_{\text{new}}$, then no optimal matching leaves both track $i$ and measurement $j$ unmatched.

*Proof.* Let $M$ leave both unmatched. Then $M' = M \cup \{(i, j)\}$ is a partial matching, and $J(M') = J(M) + c_{ij} - c_{\text{miss}} - c_{\text{new}} < J(M)$. So $M$ is not optimal. $\square$

With the default $c_{\text{miss}} = c_{\text{new}} = \gamma / 2$ the condition is $d^2_{ij} < \gamma$, which holds for every gated pair except those on the boundary of the gate.

## Claim 4: never worse than the greedy rule

Let $G$ be the matching of the greedy rule, which repeatedly takes the gated pair of least distance among unused tracks and measurements. Then the GNN cost is at most $J(G)$.

*Proof.* $G$ uses only gated pairs and never uses a track or a measurement twice, so it is a partial matching. By Claim 2 the GNN matching has the least $J$ over all partial matchings, so its cost is at most $J(G)$. $\square$

The example on the page has $J(G) = 14.455$ and a GNN cost of $8.295$, so the inequality can be strict.
