---
title: Correctness of alpha-expansion
proves: [correctness]
status: full
---

The energy is $E(f) = \sum_p D_p(f_p) + \sum_{(p,q) \in \mathcal{N}} w_{pq} V(f_p, f_q)$ with weights $w_{pq} \ge 0$. We prove three facts: each move of lines L4 to L6 returns a labeling of least energy among all $\alpha$-expansions of $f$; the loop stops at a labeling $\hat f$ that no expansion move improves; and if $V$ is a metric and $D_p \ge 0$, then $E(\hat f) \le 2c\, E(f^*)$ for an optimal $f^*$, where $c = \max_{a \ne b} V(a,b) / \min_{a \ne b} V(a,b)$.

A metric here is a function with $V(a,b) = 0$ if and only if $a = b$, $V(a,b) = V(b,a) \ge 0$, and $V(a,b) \le V(a,c) + V(c,b)$.

## 1. Each move is optimal in its move space

An $\alpha$-expansion of $f$ is a labeling $g$ with $g_p \in \{f_p, \alpha\}$ for every $p$. Write $g = g(x)$ with $x_p = 1$ if $g_p = \alpha$ and $x_p = 0$ if $g_p = f_p$; when $f_p = \alpha$ both values give the same label. Line L4 builds the binary energy

$$B(x) = \sum_p U_p(x_p) + \sum_{(p,q) \in \mathcal{N}} \theta_{pq}(x_p, x_q),$$

with $U_p(0) = D_p(f_p)$, $U_p(1) = D_p(\alpha)$, and $\theta_{pq}(a, b) = w_{pq} V(\ell_p(a), \ell_q(b))$ where $\ell_p(0) = f_p$ and $\ell_p(1) = \alpha$. By construction $B(x) = E(g(x))$ for every $x$.

Each pairwise term is regular:

$$\theta_{pq}(0,0) + \theta_{pq}(1,1) = w_{pq}\,(V(f_p, f_q) + V(\alpha, \alpha)) \le w_{pq}\,(V(f_p, \alpha) + V(\alpha, f_q)) = \theta_{pq}(0,1) + \theta_{pq}(1,0),$$

by $V(\alpha, \alpha) = 0$ and the triangle inequality. So $B$ is in the class $\mathcal{F}^2$ and regular, and by the [Kolmogorov-Zabih theorem](/graph-representable-energies/) it is represented by the graph that the code builds: for each pair term, the edge $p \to q$ of capacity $\theta(0,1) + \theta(1,0) - \theta(0,0) - \theta(1,1) \ge 0$, and for the coefficient $\lambda_p$ of $x_p$ in the remaining linear part, an edge $s \to p$ of capacity $\lambda_p$ if $\lambda_p > 0$ or an edge $p \to t$ of capacity $-\lambda_p$ if $\lambda_p < 0$. A minimum cut gives a minimizer $x$ of $B$ with $x_p = 0$ on the source side (the last paragraph of the proof on the theorem page). Line L6 returns $g(x)$, which therefore has the least energy among all $\alpha$-expansions of $f$.

## 2. Termination and local optimality

Line L7 replaces $f$ only by a labeling of strictly smaller energy. There are $L^n$ labelings, so there are finitely many replacements, and some cycle of lines L3 to L7 has no replacement. Then line L8 stops. In that last cycle $f$ did not change, so for every label $\alpha$ the optimal $\alpha$-expansion of $f$ has energy at least $E(f)$. Since $f$ is itself an $\alpha$-expansion of $f$ (with $x = 0$), no $\alpha$-expansion has smaller energy than $f$, for any $\alpha$. With integer energies there are at most $E(f_0) - \min E + 1$ cycles.

## 3. The bound $E(\hat f) \le 2c\, E(f^*)$

Let $\hat f$ be the output and $f^*$ an optimal labeling. For a label $\alpha$ let $P_\alpha = \{p : f^*_p = \alpha\}$, and let $f^\alpha$ be the $\alpha$-expansion of $\hat f$ with $f^\alpha_p = \alpha$ for $p \in P_\alpha$ and $f^\alpha_p = \hat f_p$ otherwise. Split the pairs into $I_\alpha$ (both ends in $P_\alpha$), $B_\alpha$ (exactly one end in $P_\alpha$) and the rest. For a set $Q$ of sites and a set $M$ of pairs write $E^D_Q(f) = \sum_{p \in Q} D_p(f_p)$ and $E^V_M(f) = \sum_{(p,q) \in M} w_{pq} V(f_p, f_q)$.

By part 2, $E(\hat f) \le E(f^\alpha)$. The labelings $\hat f$ and $f^\alpha$ agree outside $P_\alpha$, so the terms of the sites outside $P_\alpha$ and of the pairs with no end in $P_\alpha$ cancel, and

$$E^D_{P_\alpha}(\hat f) + E^V_{I_\alpha \cup B_\alpha}(\hat f) \le E^D_{P_\alpha}(f^\alpha) + E^V_{I_\alpha}(f^\alpha) + E^V_{B_\alpha}(f^\alpha).$$

On $P_\alpha$, $f^\alpha = \alpha = f^*$, so the first two terms on the right equal $E^D_{P_\alpha}(f^*)$ and $E^V_{I_\alpha}(f^*)$. For a pair of $B_\alpha$ with $p \in P_\alpha$ and $q \notin P_\alpha$, we have $f^*_p = \alpha \ne f^*_q$, and $V(f^\alpha_p, f^\alpha_q) = V(\alpha, \hat f_q)$. If $\hat f_q = \alpha$ this is 0. Otherwise it is at most $\max_{a \ne b} V \le c \min_{a \ne b} V \le c\, V(\alpha, f^*_q) = c\, V(f^*_p, f^*_q)$. So

$$E^D_{P_\alpha}(\hat f) + E^V_{I_\alpha \cup B_\alpha}(\hat f) \le E^D_{P_\alpha}(f^*) + E^V_{I_\alpha}(f^*) + c\, E^V_{B_\alpha}(f^*).$$

Sum over all labels $\alpha$. The sets $P_\alpha$ partition the sites, so the data terms sum to $E_D(\hat f)$ and $E_D(f^*)$. A pair with $f^*_p = f^*_q$ is in exactly one $I_\alpha$ and in no $B_\alpha$; a pair with $f^*_p \ne f^*_q$ is in exactly two sets $B_\alpha$ and in no $I_\alpha$. On the left every pair appears at least once and $V \ge 0$, so the left sum is at least $E(\hat f)$. On the right the pairs of the first kind have $V(f^*_p, f^*_q) = 0$, and those of the second kind appear twice with the factor $c$. Hence

$$E(\hat f) \le E_D(f^*) + 2c\, E_V(f^*) \le 2c\, E(f^*),$$

where the last step uses $c \ge 1$ and $E_D(f^*) \ge 0$. For the Potts model $c = 1$ and the factor is 2. $\square$

The bound needs only that $\hat f$ is a local minimum for expansion moves, so it holds for any order of the labels and any start. It is Theorem 6.1 of Boykov, Veksler and Zabih (2001).
