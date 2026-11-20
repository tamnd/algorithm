---
title: The Foschini-Miljanic iteration converges to the least feasible powers exactly when the spectral radius is below 1
proves: [correctness]
status: full
---

There are $K$ links with gains $G_{ij} \ge 0$, $G_{ii} > 0$, noise powers $\sigma_i > 0$ and targets $\gamma_i > 0$. Put $F_{ij} = \gamma_i G_{ij} / G_{ii}$ for $j \ne i$, $F_{ii} = 0$ and $u_i = \gamma_i \sigma_i / G_{ii}$. Then $F \ge 0$ and $u > 0$ entrywise. For $p \ge 0$,

$$\mathrm{SINR}_i(p) \ge \gamma_i \iff G_{ii} p_i \ge \gamma_i \Big(\sum_{j \ne i} G_{ij} p_j + \sigma_i\Big) \iff p_i \ge (Fp + u)_i, \tag{1}$$

and the same holds with equality on both sides. So $p$ meets all targets exactly when $p \ge Fp + u$; such a $p$ is *feasible*. For $\beta \in (0, 1]$, lines L2 to L4 compute $p(t+1) = T(p(t))$ with

$$T(p) = (1 - \beta)\, p + \beta\, (F p + u) = C p + \beta u, \qquad C = (1 - \beta) I + \beta F. \tag{2}$$

All inequalities between vectors are entrywise. $\rho(\cdot)$ is the spectral radius.

**Lemma 1 (monotone map).** $C \ge 0$, so $p \le q$ implies $T(p) \le T(q)$.

*Proof.* $1 - \beta \ge 0$ and $\beta F \ge 0$, so every entry of $C$ is nonnegative, and $T(q) - T(p) = C(q - p) \ge 0$. $\square$

**Lemma 2 (fixed points).** A vector $p$ is a fixed point of $T$ exactly when $p = Fp + u$, that is, by (1), when $p \ge 0$ meets every target with equality.

*Proof.* $T(p) = p$ means $\beta (Fp + u - p) = 0$, and $\beta > 0$. $\square$

**Theorem 1 (feasible case).** Let $\rho(F) < 1$. Then:

1. $p^* = (I - F)^{-1} u$ exists, $p^* \ge u > 0$, and $p^*$ meets every target with equality.
2. Every feasible $p$ satisfies $p \ge p^*$.
3. For every $p(0) \in \mathbb{R}^K$, $p(t) \to p^*$. For every $r$ with $\rho(C) < r$ there is a constant $c$ with $\|p(t) - p^*\| \le c\, r^t \|p(0) - p^*\|$, and $\rho(C) \le (1 - \beta) + \beta \rho(F) < 1$.

*Proof.* (1) Since $\rho(F) < 1$, the Neumann series $\sum_{k \ge 0} F^k$ converges and equals $(I - F)^{-1}$. Every term is nonnegative, so $p^* = \sum_k F^k u \ge F^0 u = u > 0$. From $(I - F) p^* = u$ we get $p^* = F p^* + u$, and Lemma 2 gives equality in every target.

(2) Let $p$ be feasible, so $p \ge u + Fp$. Since $F \ge 0$, we may multiply this by $F$ and keep the order: $Fp \ge Fu + F^2 p$. By induction on $n$,

$$p \ge \sum_{k=0}^{n-1} F^k u + F^n p \ge \sum_{k=0}^{n-1} F^k u,$$

where the last step uses $F^n p \ge 0$ (a feasible $p$ is $\ge u > 0$). Let $n \to \infty$: $p \ge p^*$.

(3) Put $e(t) = p(t) - p^*$. Since $T(p^*) = p^*$, $e(t+1) = T(p(t)) - T(p^*) = C e(t)$, so $e(t) = C^t e(0)$. Each eigenvalue of $C$ is $\mu = (1 - \beta) + \beta \lambda$ for an eigenvalue $\lambda$ of $F$, so $|\mu| \le (1 - \beta) + \beta |\lambda| \le (1 - \beta) + \beta \rho(F)$, which is below 1 because $\beta > 0$ and $\rho(F) < 1$. By Gelfand's formula $\|C^t\|^{1/t} \to \rho(C)$, so for $r > \rho(C)$ there is $c$ with $\|C^t\| \le c\, r^t$ for all $t$. Pick $r < 1$; then $\|e(t)\| \le c\, r^t \|e(0)\| \to 0$. $\square$

**Theorem 2 (infeasible case).** Let $\rho(F) \ge 1$. Then no feasible vector exists, and the iterates from $p(0) = 0$ increase in every entry and $\sum_i p_i(t) \to \infty$.

*Proof.* By the Perron-Frobenius theorem for nonnegative matrices, applied to $F^T$, there is $y \ge 0$, $y \ne 0$, with $y^T F = \rho(F)\, y^T$. Suppose $p$ is feasible. Then $p \ge 0$ and

$$y^T p \ge y^T F p + y^T u = \rho(F)\, y^T p + y^T u,$$

so $(1 - \rho(F))\, y^T p \ge y^T u$. The right side is positive, since $y \ge 0$, $y \ne 0$ and $u > 0$. The left side is at most $0$, since $\rho(F) \ge 1$ and $y^T p \ge 0$. This is a contradiction, so no feasible vector exists.

Now start at $p(0) = 0$. Then $p(1) = \beta u \ge p(0)$, and if $p(t) \ge p(t-1)$, Lemma 1 gives $p(t+1) = T(p(t)) \ge T(p(t-1)) = p(t)$. So the sequence increases in every entry. If it were bounded, it would converge to a finite limit $\bar p \ge 0$, and since $T$ is continuous, $T(\bar p) = \bar p$. By Lemma 2, $\bar p$ would meet every target, so it would be feasible, which we have just ruled out. Hence the sequence is unbounded, and since it is nonnegative and increasing, $\sum_i p_i(t) \to \infty$. $\square$

**Corollary (monotone convergence).** Let $\rho(F) < 1$. From $p(0) = 0$ the iterates increase to $p^*$ and stay below it; from a feasible $p(0)$ they decrease to $p^*$ and stay feasible.

*Proof.* From $0 \le p^*$ and Lemma 1, $p(t) = T^t(0) \le T^t(p^*) = p^*$, and the increase follows as in Theorem 2. If $p(0)$ is feasible, then $p(0) \ge Fp(0) + u$, so $T(p(0)) = (1 - \beta) p(0) + \beta (F p(0) + u) \le p(0)$; Lemma 1 and induction give $p(t+1) \le p(t)$. Also $T(p) \ge Fp + u$ whenever $p \ge Fp + u$, because $T(p)$ is a convex combination of $p$ and $Fp + u$, both $\ge Fp + u$; and then $F T(p) + u \le Fp + u \le T(p)$ by $T(p) \le p$ and $F \ge 0$. So each iterate is feasible. Theorem 1 gives the limit. $\square$

**The algorithm.** Lines L1 to L4 compute $p(t+1) = T(p(t))$, because line L3 computes $I_i = (\sum_{j \ne i} G_{ij} p_j(t) + \sigma_i)$ and line L4 sets $p_i(t+1) = (1 - \beta) p_i(t) + \beta \gamma_i I_i / G_{ii} = (1 - \beta) p_i(t) + \beta (F p(t) + u)_i$. Line L5 returns an iterate once the change in one round is at most $\epsilon$ times the largest power, and line L6 returns $p(T)$. By Theorem 1, when $\rho(F) < 1$ the returned vector tends to $p^*$ as $\epsilon \to 0$ and $T \to \infty$: near the fixed point the error is at most the change in one round divided by $1 - r$ in a norm in which $C$ contracts by $r < 1$. By Theorem 2, when $\rho(F) \ge 1$ no returned vector meets every target, and from $p(0) = 0$ the powers grow without bound.
