---
title: Max-rate scheduling has the largest total rate in every slot, and the share and mean-rate formulas hold
proves: [correctness]
status: full
---

The users $k = 1, \ldots, K$, resources $n = 1, \ldots, N$, slots $t = 1, \ldots, T$ and rates $r_{k,n}(t) \ge 0$ are as on the page. An assignment of slot $t$ is a map $a : \{1, \ldots, N\} \to \{1, \ldots, K\}$, and its total is $V_t(a) = \sum_n r_{a(n), n}(t)$. Let $M_n(t) = \max_k r_{k,n}(t)$ and $B_n(t) = \{k : r_{k,n}(t) = M_n(t)\}$, the set of best users of resource $n$.

## Part 1: optimality

**Lemma 1 (the optimal assignments).** An assignment $a$ of slot $t$ maximizes $V_t$ if and only if $a(n) \in B_n(t)$ for every $n$. The largest value is $\sum_n M_n(t)$.

*Proof.* For every $a$, $V_t(a) = \sum_n M_n(t) - \sum_n \big(M_n(t) - r_{a(n),n}(t)\big)$, and each term $M_n(t) - r_{a(n),n}(t)$ is $\ge 0$, with equality exactly when $a(n) \in B_n(t)$. So $V_t(a) \le \sum_n M_n(t)$, and equality holds exactly when every term is $0$. Assignments with $a(n) \in B_n(t)$ for all $n$ exist, since each $B_n(t)$ is a nonempty subset of a finite set. $\square$

**Theorem 1 (one slot).** Lines L2 to L4 return the assignment $a^*$ with $a^*(n) = \min B_n(t)$. It maximizes $V_t$, and among all maximizers it is the first in the lexicographic order of $(a(1), \ldots, a(N))$.

*Proof.* Line L3 scans $k = 1, \ldots, K$ and keeps the current best index, replacing it only when a later rate is strictly larger. After the scan the kept index has rate $M_n(t)$, and no smaller index has rate $M_n(t)$, since the first index that reaches $M_n(t)$ is never replaced. So $a^*(n) = \min B_n(t)$, and by Lemma 1, $a^*$ is a maximizer. Let $a \ne a^*$ be another maximizer and $n_0$ the first place where they differ. By Lemma 1, $a(n_0) \in B_{n_0}(t)$, so $a(n_0) > \min B_{n_0}(t) = a^*(n_0)$, and $a^*$ comes first in lexicographic order. $\square$

**Theorem 2 (the horizon).** Let the rates of every slot be fixed in advance or revealed at the start of the slot, and let them not depend on the earlier choices. Then the schedule of the algorithm has the largest total $\sum_k S_k = \sum_t V_t(a_t)$ of all schedules, and the largest value is $\sum_t \sum_n M_n(t)$.

*Proof.* Every served bit of user $k$ is counted in exactly one slot and one resource, so $\sum_k S_k = \sum_t V_t(a_t)$, where line L5 adds $r_{a_t(n), n}(t)$ to $S_{a_t(n)}$ once for each $(t, n)$. For any schedule, by Lemma 1, $\sum_t V_t(a_t) \le \sum_t \sum_n M_n(t)$. The algorithm reaches $V_t(a^*_t) = \sum_n M_n(t)$ in every slot by Theorem 1, so it reaches the bound. Since the bound does not depend on the choices, no schedule, including one that knows the future rates, does better. $\square$

## Part 2: the formulas of the example

**Lemma 3 (share of slots).** Let $X_1, \ldots, X_K$ be independent, with $X_k$ exponential of rate $\lambda_k > 0$ (mean $1/\lambda_k$). Then

$$\Pr[X_i > X_j \text{ for all } j \ne i] = \sum_{S \subseteq \{j \ne i\}} (-1)^{|S|} \frac{\lambda_i}{\lambda_i + \sum_{j \in S} \lambda_j}.$$

*Proof.* Condition on $X_i = x$. By independence, the probability that all others are below $x$ is $\prod_{j \ne i} (1 - e^{-\lambda_j x})$, so the probability is $\int_0^\infty \lambda_i e^{-\lambda_i x} \prod_{j \ne i} (1 - e^{-\lambda_j x})\, dx$. Expanding the product gives $\sum_S (-1)^{|S|} e^{-x \sum_{j \in S} \lambda_j}$, a finite sum, so the integral can be taken term by term: $\int_0^\infty \lambda_i e^{-(\lambda_i + \Lambda_S) x}\, dx = \lambda_i / (\lambda_i + \Lambda_S)$ with $\Lambda_S = \sum_{j \in S} \lambda_j$. Ties have probability $0$, since the laws are continuous, so the tie rule does not change the share. $\square$

With equal rates, the $K$ events "user $i$ wins" have the same probability by symmetry, and they partition the sample space up to ties of probability $0$, so each has probability $1/K$. For two users, the formula gives $1 - \lambda_0 / (\lambda_0 + \lambda_1) = \lambda_1 / (\lambda_0 + \lambda_1) = m_0 / (m_0 + m_1)$.

**Lemma 4 (expectations of the largest gain).** Let $X = \max_k X_k$ for $K$ independent unit exponentials, and let $h$ be continuously differentiable on $[0, \infty)$ with $h'(x) \ge 0$ and $h'(x) \le c(1 + x)^m$ for some $c, m$. Then

$$\mathbb E[h(X)] = h(0) + \int_0^\infty h'(x) \big(1 - (1 - e^{-x})^K\big)\, dx.$$

*Proof.* $\Pr[X \le x] = \prod_k \Pr[X_k \le x] = (1 - e^{-x})^K$, so $\Pr[X > x] = 1 - (1 - e^{-x})^K \le K e^{-x}$ by the union bound. Write $h(X) - h(0) = \int_0^\infty h'(x) \mathbf 1[X > x]\, dx$. The integrand is nonnegative, so by Tonelli's theorem the expectation and the integral can be swapped, which gives the formula. It is finite because $h'(x) K e^{-x}$ is integrable. $\square$

**Corollary 5 ($\mathbb E[X] = H_K$).** With $h(x) = x$, $\mathbb E[X] = \int_0^\infty (1 - (1 - e^{-x})^K)\, dx$. Put $u = 1 - e^{-x}$, so $dx = du / (1 - u)$, and the integral is $\int_0^1 (1 - u^K)/(1 - u)\, du = \int_0^1 \sum_{j=0}^{K-1} u^j\, du = \sum_{j=1}^{K} 1/j = H_K$. $\square$

**Corollary 6 (mean rate).** With $h(x) = \log_2(1 + \gamma x)$ and $\gamma > 0$, $h'(x) = \gamma / ((1 + \gamma x) \ln 2)$, which is bounded, so Lemma 4 applies. The substitution $y = \ln(1 + \gamma x)$, $dy = \gamma\, dx / (1 + \gamma x)$, gives

$$\mathbb E[\log_2(1 + \gamma X)] = \frac{1}{\ln 2} \int_0^\infty \Pr\Big[X > \frac{e^y - 1}{\gamma}\Big]\, dy.$$

The code evaluates this integral by Simpson's rule on $[0, \ln(1 + \gamma (45 + \ln K))]$. Past the upper end, $\Pr[X > x] \le K e^{-x} \le e^{-45}$, and the integrand decays like $K \exp(-(e^y - 1)/\gamma)$, so the cut-off error is far below the test tolerance. Expanding $1 - (1 - e^{-x})^K = \sum_{m=1}^{K} (-1)^{m+1} \binom{K}{m} e^{-m x}$ and using $\int_0^\infty e^{-m x} \gamma / (1 + \gamma x)\, dx = e^{m/\gamma} E_1(m/\gamma)$ gives the closed form

$$\mathbb E[\log_2(1 + \gamma X)] = \frac{1}{\ln 2} \sum_{m=1}^{K} (-1)^{m+1} \binom{K}{m} e^{m/\gamma} E_1(m/\gamma),$$

which the tests use for small $K$. For $K = 1$ and $\gamma = 1$ it is $e\, E_1(1) / \ln 2 = 0.596347\ldots / \ln 2$. $\square$
