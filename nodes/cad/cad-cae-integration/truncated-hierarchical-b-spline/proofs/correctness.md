---
title: The truncated basis is nonnegative, a partition of unity, preserves coefficients, spans the hierarchical space and is linearly independent
proves: [correctness]
status: full
---

We use the notation of the page. $\mathcal{B}^k$ is the set of tensor B-splines of level $k$, and "$\gamma \subseteq \Omega$" means that every support cell of $\gamma$ lies in $\Omega$. The domains satisfy $\Omega^0 = [0, n_0]^2$, $\Omega^{k+1} \subseteq \Omega^k$, each $\Omega^k$ is a union of cells of level $k - 1$, and $\Omega^L = \emptyset$. $H^\ell$ is Kraft's selection of level $\ell$: the $\beta \in \mathcal{B}^\ell$ with $\beta \subseteq \Omega^\ell$ and $\beta \not\subseteq \Omega^{\ell+1}$. $S^k$ is the span of $\mathcal{B}^k$, and $S^0 \subseteq S^1 \subseteq \cdots$. For $s \in S^k$, $c^k_\gamma(s)$ is its coefficient on $\gamma \in \mathcal{B}^k$; these coefficients are unique because $\mathcal{B}^k$ is a basis of $S^k$.

We use two facts from [the hierarchical B-spline proof](/hierarchical-b-spline/): (two-scale) each $\beta \in \mathcal{B}^k$ is $\sum_\gamma r_{\beta\gamma} \gamma$ over $\gamma \in \mathcal{B}^{k+1}$ with $r_{\beta\gamma} \ge 0$, and $r_{\beta\gamma} \ne 0$ only if the support of $\gamma$ lies in that of $\beta$; and (span) every $\beta \in \mathcal{B}^\ell$ with $\beta \subseteq \Omega^\ell$ lies in the span of $H = \bigcup_\ell H^\ell$, which is linearly independent.

For $s \in S^{k-1}$, $\operatorname{trunc}^k s = \sum_{\gamma \in \mathcal{B}^k, \gamma \not\subseteq \Omega^k} c^k_\gamma(s) \gamma$. This map is linear. Lines L2 to L5 compute $\tau(\beta) = \operatorname{trunc}^{L-1} \cdots \operatorname{trunc}^{\ell+1} \beta$ for $\beta \in H^\ell$, and line L6 writes it in the finest level by the two-scale relation; an empty product means $\tau(\beta) = \beta$.

**Lemma 1 (nonnegativity).** For $\beta \in H^\ell$ and each $k \ge \ell$, the coefficients of the partial truncation $\operatorname{trunc}^{k} \cdots \operatorname{trunc}^{\ell+1} \beta$ on $\mathcal{B}^k$ are nonnegative, and so are the coefficients of $\tau(\beta)$ on the finest level. Hence $\tau(\beta) \ge 0$.

*Proof.* At $k = \ell$ the coefficients are a unit vector. A lift multiplies nonnegative coefficients by the nonnegative two-scale coefficients and adds, and the truncation sets some coefficients to zero. So every step keeps the coefficients nonnegative, and so does the final lift in line L6. B-splines are nonnegative, so $\tau(\beta) \ge 0$. $\square$

**Theorem 1 (preservation of coefficients).** For every $s \in S^0$,

$$s = \sum_{\ell = 0}^{L-1} \sum_{\beta \in H^\ell} c^\ell_\beta(s)\, \tau(\beta).$$

*Proof.* For $0 \le k \le L - 1$ let

$$g_k = \sum_{\ell < k} \sum_{\beta \in H^\ell} c^\ell_\beta(s)\, \operatorname{trunc}^{k} \cdots \operatorname{trunc}^{\ell+1} \beta.$$

We prove by induction on $k$ the two claims (a) $g_k = \sum_{\gamma \in \mathcal{B}^k, \gamma \not\subseteq \Omega^k} c^k_\gamma(s) \gamma$ and (b) $s = g_k + \sum_{\gamma \in \mathcal{B}^k, \gamma \subseteq \Omega^k} c^k_\gamma(s) \gamma$. Claim (b) follows from (a) because $s = \sum_{\gamma \in \mathcal{B}^k} c^k_\gamma(s) \gamma$.

For $k = 0$, $g_0 = 0$ and every $\gamma \in \mathcal{B}^0$ lies in $\Omega^0$, so (a) holds.

Assume (a) and (b) for some $k < L - 1$. Split the B-splines of level $k$ in $\Omega^k$ into $H^k$ and $D^k = \{\gamma \in \mathcal{B}^k : \gamma \subseteq \Omega^{k+1}\}$. Then (b) reads $s = u + v$ with

$$u = g_k + \sum_{\beta \in H^k} c^k_\beta(s) \beta, \qquad v = \sum_{\gamma \in D^k} c^k_\gamma(s) \gamma.$$

By the two-scale fact, $v$ is a combination of B-splines $\eta \in \mathcal{B}^{k+1}$ whose supports lie in the supports of members of $D^k$, so in $\Omega^{k+1}$. Hence for every $\eta \in \mathcal{B}^{k+1}$ with $\eta \not\subseteq \Omega^{k+1}$, $c^{k+1}_\eta(v) = 0$ and $c^{k+1}_\eta(u) = c^{k+1}_\eta(s)$ by linearity and uniqueness of coefficients. So

$$\operatorname{trunc}^{k+1} u = \sum_{\eta \not\subseteq \Omega^{k+1}} c^{k+1}_\eta(s)\, \eta.$$

By linearity of $\operatorname{trunc}^{k+1}$, $\operatorname{trunc}^{k+1} u = g_{k+1}$, since $\operatorname{trunc}^{k+1}$ applied to the terms of $g_k$ adds one more truncation and $\operatorname{trunc}^{k+1} \beta$ is the partial truncation of $\beta \in H^k$. This is (a) for $k + 1$.

At $k = L - 1$, $\Omega^L = \emptyset$, so no $\gamma \in \mathcal{B}^{L-1}$ lies in $\Omega^L$ and the $\gamma \subseteq \Omega^{L-1}$ are exactly $H^{L-1}$. For these, $\tau(\gamma) = \gamma$. Claim (b) is then

$$s = g_{L-1} + \sum_{\beta \in H^{L-1}} c^{L-1}_\beta(s) \beta = \sum_{\ell} \sum_{\beta \in H^\ell} c^\ell_\beta(s)\, \tau(\beta). \qquad \square$$

**Corollary 1 (partition of unity).** $\sum_{(\ell, \beta) \in H} \tau(\beta) = 1$.

*Proof.* The constant 1 lies in $S^0$, and by the [partition of unity](/partition-of-unity/) of B-splines on an open knot vector, $1 = \sum_{\gamma \in \mathcal{B}^k} \gamma$ in every level, so $c^\ell_\beta(1) = 1$ for all $\beta$. Apply Theorem 1. $\square$

**Lemma 2 (triangular form).** For $\beta \in H^\ell$, $\tau(\beta) - \beta$ is a combination of B-splines $\gamma$ of levels $k > \ell$ with $\gamma \subseteq \Omega^k$.

*Proof.* Write $t_\ell = \beta$ and $t_k = \operatorname{trunc}^k t_{k-1}$. Then $t_{k-1} - t_k = \sum_{\gamma \in \mathcal{B}^k, \gamma \subseteq \Omega^k} c^k_\gamma(t_{k-1}) \gamma$, and $\tau(\beta) - \beta = -\sum_{k = \ell+1}^{L-1} (t_{k-1} - t_k)$. $\square$

**Theorem 2 (same span, linear independence).** The functions $\tau(\beta)$, $(\ell, \beta) \in H$, are linearly independent and span the same space as $H$.

*Proof.* By Lemma 2 and the span fact, each $\gamma$ of level $k$ with $\gamma \subseteq \Omega^k$ lies in the span of $H^k \cup H^{k+1} \cup \cdots$, so $\tau(\beta) - \beta$ lies in the span of $\bigcup_{k > \ell} H^k$ for $\beta \in H^\ell$. Order $H$ by level from the finest down. In the basis $H$ of $\operatorname{span} H$, the matrix that maps $H$ to $\{\tau(\beta)\}$ has ones on the diagonal and nonzero entries off the diagonal only from a level to finer levels, so it is unit triangular and invertible. Hence $\{\tau(\beta)\}$ is a basis of $\operatorname{span} H$. $\square$

**Corollary 2 (nested spaces).** If $\hat\Omega^\ell \supseteq \Omega^\ell$ for every level, the truncated basis for $\hat\Omega$ spans a space that contains the span of the truncated basis for $\Omega$.

*Proof.* By Theorem 2 both spans equal the hierarchical spans, which are nested by the nesting theorem of the hierarchical B-spline proof. $\square$

**Correctness of the operations.** Line L1 is Kraft's selection. Lines L2 to L5 compute $\operatorname{trunc}^{k} \cdots \operatorname{trunc}^{\ell+1} \beta$ for $k = \ell + 1, \ldots, L - 1$: line L4 lifts by the two-scale matrices, which give the unique coefficients on $\mathcal{B}^k$, and line L5 drops exactly the terms with $\gamma \subseteq \Omega^k$. Line L6 lifts the result to the finest level without change of the function. Lines L7 to L10 sum the coefficients times the finest tensor B-splines, computed by the Cox-de Boor recursion. So BASIS returns $\tau(\beta)$ for each $\beta \in H$, and Lemma 1, Theorem 1, Corollary 1, Theorem 2 and Corollary 2 hold for its output. The tests check each of them exactly with fractions. $\blacksquare$
