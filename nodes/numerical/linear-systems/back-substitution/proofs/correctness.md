---
title: Back substitution is correct and backward stable
proves: [correctness, termination]
status: full
---

We use the notation of the page: $U$ is $n \times n$ upper triangular, $u$ is the unit roundoff and $\gamma_k = k u / (1 - k u)$ for $k u < 1$.

**Termination.** Line L1 runs $n$ times and line L4 runs $n - i$ times for each $i$, so the algorithm stops after $n^2$ flops or after it returns at line L2.

**Theorem 1 (exact arithmetic).** If each $u_{ii} \neq 0$, BACK-SUBSTITUTION returns the unique $x$ with $U x = b$. If some $u_{ii} = 0$, it returns SINGULAR, and $U$ is singular.

*Proof.* If some $u_{ii} = 0$ then $\det U = \prod_i u_{ii} = 0$, and line L2 returns SINGULAR at the largest such $i$ (the loop reaches it before any smaller index). Now assume each $u_{ii} \neq 0$ and let $x^*$ be the solution, which exists because $\det U \ne 0$. We show by downward induction on $i$ the claim $P(i)$: after the pass of line L1 for $i$, $x_k = x^*_k$ for $k = i, \ldots, n$.

*Base and step together.* Assume $P(i + 1)$, or nothing when $i = n$. Lines L3 to L5 give $s = b_i - \sum_{j=i+1}^n u_{ij} x_j = b_i - \sum_{j=i+1}^n u_{ij} x^*_j$ by the hypothesis. Row $i$ of $U x^* = b$ is $u_{ii} x^*_i + \sum_{j > i} u_{ij} x^*_j = b_i$, because $u_{ij} = 0$ for $j < i$. So $s = u_{ii} x^*_i$ and line L6 sets $x_i = x^*_i$. With $P(i + 1)$ this gives $P(i)$.

$P(1)$ is the claim. $\square$

**Lemma 2 (Higham, Lemma 3.1).** If $|\delta_k| \le u$ and $\sigma_k \in \{1, -1\}$ for $k = 1, \ldots, m$, and $m u < 1$, then $\prod_{k=1}^m (1 + \delta_k)^{\sigma_k} = 1 + \theta_m$ with $|\theta_m| \le \gamma_m$.

*Proof.* By induction on $m$, the product lies between $(1 - u)^m$ and $(1 - u)^{-m}$, since each factor lies in $[1 - u, 1/(1 - u)]$: for $1 + \delta$ this follows from $1 + u \le 1/(1 - u)$, and for $1/(1 + \delta)$ from $1/(1 + u) \ge 1 - u$. Bernoulli's inequality gives $(1 - u)^m \ge 1 - m u \ge 1 - \gamma_m$. For the upper end, $(1 - u)^{-m} \le (1 - m u)^{-1} = 1 + \gamma_m$, again by $(1 - u)^m \ge 1 - m u$. $\square$

**Theorem 3 (floating point).** Assume the [standard model](/floating-point-model/): each operation returns $\mathrm{fl}(a \circ b) = (a \circ b)(1 + \delta)$ with $|\delta| \le u$, no underflow or overflow happens, and $n u < 1$. If BACK-SUBSTITUTION runs to the end, its output $\hat x$ satisfies $(U + \Delta U)\hat x = b$ with $|\Delta u_{ij}| \le \gamma_{n - i + 1} |u_{ij}| \le \gamma_n |u_{ij}|$ for all $i, j$.

*Proof.* Fix a row $i$ and let $k = n - i$. Write $p_j = \mathrm{fl}(u_{ij} \hat x_j) = u_{ij} \hat x_j (1 + \alpha_j)$ for $j = i + 1, \ldots, n$. Line L5 computes $s_{i} = b_i$ and $s_j = \mathrm{fl}(s_{j-1} - p_j) = (s_{j-1} - p_j)(1 + \beta_j)$, where we index $s$ by the last $j$ used. Line L6 computes $\hat x_i = (s_n / u_{ii})(1 + \delta)$, so $u_{ii} \hat x_i (1 + \delta)^{-1} = s_n$.

Unroll the recursion for $s$:
$$s_n = b_i \prod_{l = i+1}^{n} (1 + \beta_l) - \sum_{j = i+1}^{n} u_{ij} \hat x_j (1 + \alpha_j) \prod_{l = j}^{n} (1 + \beta_l).$$
Divide both sides by $\prod_{l=i+1}^n (1 + \beta_l)$ and put the result into $u_{ii} \hat x_i (1 + \delta)^{-1} = s_n$:
$$u_{ii} \hat x_i (1 + \delta)^{-1} \prod_{l = i+1}^{n} (1 + \beta_l)^{-1} + \sum_{j = i+1}^{n} u_{ij} \hat x_j (1 + \alpha_j) \prod_{l = i+1}^{j-1} (1 + \beta_l)^{-1} = b_i.$$
The factor of $u_{ii}$ is a product of $k + 1$ terms of the form $(1 + \delta)^{\pm 1}$, and the factor of $u_{ij}$ is a product of $1 + (j - i - 1) \le k$ such terms. By Lemma 2 each factor is $1 + \theta$ with $|\theta| \le \gamma_{k+1} = \gamma_{n - i + 1}$, since $\gamma_m$ grows with $m$. Set $\Delta u_{ij} = \theta_{ij} u_{ij}$ for $j \ge i$ and $\Delta u_{ij} = 0$ for $j < i$. Then row $i$ of $(U + \Delta U)\hat x = b$ holds exactly, with $|\Delta u_{ij}| \le \gamma_{n - i + 1} |u_{ij}|$. This holds for each row, and $\gamma_{n - i + 1} \le \gamma_n$. $\blacksquare$

**Remarks.** Forward substitution has the same proof with the rows taken in the order $1, \ldots, n$; row $i$ then has $i - 1$ products, so its bound is $\gamma_i$. A different order of the sum in line L5 changes which factors appear in which term, but each term still has at most $k + 1$ factors, so the bound $\gamma_n$ is the same (Higham, Theorem 8.5).
