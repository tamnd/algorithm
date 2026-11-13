---
title: Each step of GrabCut minimizes the energy over one group of variables, so the energy never rises and the loop stops
proves: [correctness]
status: full
---

Write $D_\varepsilon(a, c, \theta, z) = D(a, c, \theta, z) + \tfrac{\varepsilon}{2} \operatorname{tr} \Sigma(a, c)^{-1}$ for the data cost of the implementation, with $D$ as on the main page and $\varepsilon \ge 0$, and $E = \sum_n D_\varepsilon(\alpha_n, k_n, \theta, z_n) + V(\alpha, z)$. A component with weight 0 has cost $+\infty$ and is never chosen. The argument is in exact arithmetic.

**Lemma 1 (line L4).** For fixed $\alpha$ and $\theta$, choosing each $k_n$ as a component of least cost $D_\varepsilon(\alpha_n, k_n, \theta, z_n)$ minimizes $E$ over $k$.

*Proof.* $V$ does not depend on $k$, and the data term is a sum of terms each of which depends on one $k_n$ only. $\square$

**Lemma 2 (line L5).** For fixed $\alpha$ and $k$, LEARN minimizes $E$ over $\theta$.

*Proof.* Only the data term depends on $\theta$, and it splits into one sum per label $a$. If no pixel has label $a$, the sum is empty and any model for $a$, in particular the old one, is optimal. Otherwise let $M$ be the number of pixels with label $a$, and let $m_c = |F(a, c)|$, so $\sum_c m_c = M$. The sum is

$$-\sum_c m_c \log \pi_c + \sum_{c : m_c > 0} \; \sum_{n \in F(a, c)} \Bigl( \tfrac{1}{2} \log \det \Sigma_c + \tfrac{1}{2} (z_n - \mu_c)^\top \Sigma_c^{-1} (z_n - \mu_c) + \tfrac{\varepsilon}{2} \operatorname{tr} \Sigma_c^{-1} \Bigr).$$

*Weights.* Under $\sum_c \pi_c = 1$, $-\sum_c m_c \log \pi_c - \bigl(-\sum_c m_c \log (m_c / M)\bigr) = M \sum_c \frac{m_c}{M} \log \frac{m_c / M}{\pi_c} \ge 0$ by Gibbs' inequality, with equality at $\pi_c = m_c / M$. A component with $m_c = 0$ gets $\pi_c = 0$.

*Means.* For any positive definite $\Sigma_c$ and the sample mean $\bar z$ of $F(a, c)$,

$$\sum_{n} (z_n - \mu_c)^\top \Sigma_c^{-1} (z_n - \mu_c) = \sum_{n} (z_n - \bar z)^\top \Sigma_c^{-1} (z_n - \bar z) + m_c (\bar z - \mu_c)^\top \Sigma_c^{-1} (\bar z - \mu_c),$$

since the cross terms add up to 0. The last term is non-negative and is 0 at $\mu_c = \bar z$.

*Covariances.* With $\mu_c = \bar z$, let $S = \frac{1}{m_c} \sum_n (z_n - \bar z)(z_n - \bar z)^\top$ and $A = S + \varepsilon I$. Using $x^\top P x = \operatorname{tr}(P x x^\top)$ and writing $P = \Sigma_c^{-1}$, the terms of component $c$ are $\frac{m_c}{2} g(P)$ with $g(P) = -\log \det P + \operatorname{tr}(P A)$. Let $\lambda_1, \dots, \lambda_d > 0$ be the eigenvalues of $A^{1/2} P A^{1/2}$ (here $\varepsilon > 0$, or $S$ nonsingular, so $A$ is positive definite). Then

$$g(P) - g(A^{-1}) = \sum_i (\lambda_i - 1 - \log \lambda_i) \ge 0,$$

because $\lambda - 1 - \log \lambda \ge 0$ for $\lambda > 0$, with equality only at $\lambda = 1$. So $\Sigma_c = A = S + \varepsilon I$, which LEARN computes, is the unique minimizer. $\square$

**Lemma 3 (line L6).** For fixed $\theta$, let $\hat E(\alpha) = \min_k E(\alpha, k, \theta, z) = \sum_n \min_c D_\varepsilon(\alpha_n, c, \theta, z_n) + V(\alpha, z)$, over labelings $\alpha$ that agree with the trimap on $T_B$ and $T_F$. The labeling of line L6 minimizes $\hat E$.

*Proof.* Write $u_n(a) = \min_c D_\varepsilon(a, c, \theta, z_n)$. Every $s$-$t$ cut $(S, \bar S)$ of the graph gives the labeling $\alpha_n = 1$ for $n \in S \cap T_U$, $\alpha_n = 0$ for $n \in \bar S \cap T_U$, and the fixed values elsewhere, and every allowed labeling arises from exactly one cut. Count the capacity of the edges from $S$ to $\bar S$:

- the edge $s \to n$ is cut exactly when $\alpha_n = 0$, and $n \to t$ exactly when $\alpha_n = 1$, so the unary edges of $n$ contribute $u_n(\alpha_n) - \min(u_n(0), u_n(1))$ plus the pair weights moved onto them;
- for two neighbors $m, n \in T_U$, one of the two directed edges between them is cut exactly when $\alpha_m \ne \alpha_n$, and it carries the pair weight;
- a pair with one fixed pixel $m$ and $n \in T_U$ has its weight on the unary edge of $n$ for the label $1 - \alpha_m$, which is cut exactly when $\alpha_n \ne \alpha_m$.

Pairs of two fixed pixels and the terms $u_n$ of fixed pixels do not depend on the cut. So the capacity of every cut is $\hat E(\alpha) - \kappa$ for one constant $\kappa$. When Edmonds-Karp stops, there is no augmenting path, and by the [max-flow min-cut theorem](/max-flow-min-cut-theorem/) the set $S$ of nodes reachable from $s$ in the residual graph is a minimum cut. Its labeling therefore minimizes $\hat E$. $\square$

**Theorem.** Let $E_0$ be the energy after line L2 and $E_r$ the energy computed at line L7 of round $r$. Within each round the energy does not rise from step to step, and $E_r \le E_{r-1}$. The loop ends after finitely many rounds, and at its end a whole round of lines L4 to L6 did not lower the energy.

*Proof.* Let $(\alpha, k, \theta)$ be the state at the start of round $r$, with energy $E_{r-1}$ (the state after line L2 or after line L7 of the round before). Line L4 gives $k'$ with $E(\alpha, k', \theta) \le E(\alpha, k, \theta)$ by Lemma 1. Line L5 gives $\theta'$ with $E(\alpha, k', \theta') \le E(\alpha, k', \theta)$ by Lemma 2. Line L6 gives $\alpha'$ with $\hat E(\alpha') \le \hat E(\alpha) \le E(\alpha, k', \theta')$ by Lemma 3, where $\hat E$ uses $\theta'$, and line L7 picks $k''$ with $E(\alpha', k'', \theta') = \hat E(\alpha')$. So $E_r \le E_{r-1}$.

The value $E_r$ is fixed by $\alpha$, $k'$ and $\alpha'$, because $\theta'$ is computed from $\alpha$ and $k'$ (and from the old model only for a label with no pixels, which does not change the energy). There are finitely many such triples. While the loop runs, $E_1 > E_2 > \dots$ strictly, so no value repeats and the loop ends after finitely many rounds. It ends when $E_r \ge E_{r-1}$, that is $E_r = E_{r-1}$, and then each of the three steps of that round left the energy unchanged. $\square$

With floating point numbers the inequalities hold up to rounding, which is why the implementation compares with a small tolerance and caps the number of rounds. With $\varepsilon = 0$ and nonsingular sample covariances, the energy is the one of the paper, and the same proof is the monotone convergence argument of its Section 3.2.
