---
title: Proof of the Schoenberg-Whitney theorem
proves: [statement]
status: full
---

We use the notation of the statement. $N_{i,q}$ is the B-spline of degree $q$ on the knots $t_i, \ldots, t_{i+q+1}$, from the Cox-de Boor recursion with half-open spans and the rule that a term with a zero denominator is $0$. It depends only on these $q + 2$ knots. We use these facts from the B-spline page.

- **(F1) Support.** $N_{i,q}(x) = 0$ for $x \notin [t_i, t_{i+q+1})$.
- **(F2) Positivity.** $N_{i,q}(x) > 0$ for $t_i < x < t_{i+q+1}$.
- **(F3) Continuity.** On each nonempty knot span $N_{i,q}$ is a polynomial, and at a knot of multiplicity $m \le q$ among its own knots it is $C^{q-m}$. A value in $(t_i, t_{i+q+1})$ occurs at most $q$ times among $t_{i+1}, \ldots, t_{i+q}$. So for $q \ge 1$, $N_{i,q}$ is continuous everywhere except possibly at $t_i$, when $t_i = t_{i+q}$, and at $t_{i+q+1}$, when $t_{i+1} = t_{i+q+1}$.
- **(F4) Derivative.** On each open knot span, $N_{i,q}' = \frac{q}{t_{i+q} - t_i} N_{i,q-1} - \frac{q}{t_{i+q+1} - t_{i+1}} N_{i+1,q-1}$, with the same zero rule.

A piecewise polynomial $g$ has one-sided limits $g(x^-)$ and $g(x^+)$ at every point, and $g(x^+) = g(x)$ for a combination of B-splines.

## Lemma 1 (the value at the start of the support)

*Let $q \ge 0$ and $t_i < t_{i+q+1}$. Then $N_{i,q}(t_i) \ne 0$ if and only if $t_i = t_{i+q}$, and then $N_{i,q}(t_i) = 1$.*

*Proof.* Write $u = t_i$. First let $u < t_{i+r}$ for some $r \ge 1$; we show $N_{i,r}(u) = 0$ by induction on $r$. In the recursion $N_{i,r}(u) = \omega \, N_{i,r-1}(u) + (1 - \omega') N_{i+1,r-1}(u)$ the left weight is $\omega = (u - t_i)/(t_{i+r} - t_i) = 0$. For $r = 1$, $N_{i+1,0}(u) = 0$ because $u < t_{i+1}$. For $r \ge 2$, either $u < t_{i+1}$, and $N_{i+1,r-1}(u) = 0$ by (F1), or $t_{i+1} = u < t_{(i+1)+(r-1)}$, and $N_{i+1,r-1}(u) = 0$ by the induction hypothesis. So if $t_i < t_{i+q}$, then $N_{i,q}(t_i) = 0$ (for $q = 0$ this case does not occur).

Now let $t_i = t_{i+q} < t_{i+q+1}$ and put $\mu = i + q$, so $t_\mu \le u < t_{\mu+1}$. On this span $N_{\mu-r,r-1}$ is $0$ by (F1), so the recursion gives $N_{\mu-r,r}(u) = \frac{t_{\mu+1} - u}{t_{\mu+1} - t_{\mu-r+1}} N_{\mu-r+1,r-1}(u)$ for $1 \le r \le q$, and $N_{\mu,0}(u) = 1$. At $u = t_i$ every factor is $1$, because $t_{\mu-r+1} = t_i$ for $1 \le r \le q$. So $N_{i,q}(t_i) = N_{\mu-q,q}(t_i) = 1$. $\square$

**Part 2 of the theorem** follows: $N_i(\tau) \ne 0$ needs $t_i \le \tau < t_{i+p+1}$ by (F1); inside, $N_i(\tau) > 0$ by (F2); and at $\tau = t_i$, Lemma 1 applies.

## Necessity

Suppose $N_k(\tau_k) = 0$ for some $k$. By part 2, either $\tau_k \ge t_{k+p+1}$, or $\tau_k < t_k$, or $\tau_k = t_k < t_{k+p}$.

*Case $\tau_k \ge t_{k+p+1}$.* For $j \le k$ and $i \ge k$, $\tau_i \ge \tau_k \ge t_{k+p+1} \ge t_{j+p+1}$, so $A_{ij} = N_j(\tau_i) = 0$ by (F1). The $k + 1$ columns $0, \ldots, k$ have their nonzero entries only in the $k$ rows $0, \ldots, k - 1$. So they are $k + 1$ vectors in a space of dimension $k$, they are dependent, and $A$ is singular.

*Case $\tau_k \le t_k$ and $N_k(\tau_k) = 0$.* Let $i \le k$ and $j \ge k$. Then $\tau_i \le \tau_k \le t_k \le t_j$. If $\tau_i < t_j$, then $N_j(\tau_i) = 0$ by (F1). If $\tau_i = t_j$, then all these numbers are equal: $i = k$ because the sites are distinct, and $t_k = t_j$. For $j = k$, $N_k(\tau_k) = 0$ by assumption. For $j > k$, if $N_j(t_j) \ne 0$ then $t_j = t_{j+p}$ by Lemma 1, so $t_k = t_{k+1} = \cdots = t_{j+p}$, which contains $t_k = t_{k+p+1}$; this is excluded by the hypothesis $t_k < t_{k+p+1}$. So $N_j(\tau_i) = 0$ in all cases. The $k + 1$ rows $0, \ldots, k$ have their nonzero entries only in the $k$ columns $0, \ldots, k - 1$, and $A$ is singular.

## Lemma 2 (a weak Rolle theorem)

*Let $\alpha < \beta$ and let $g$ be continuous on $[\alpha, \beta]$ and a polynomial on each of finitely many subintervals, with $g(\alpha) = g(\beta) = 0$. Then there is a $\rho \in (\alpha, \beta)$ whose one-sided derivatives satisfy $g'_-(\rho) \, g'_+(\rho) \le 0$.*

*Proof.* If $g = 0$ on $[\alpha, \beta]$, every $\rho$ works. Otherwise $|g|$ has its maximum at a point $\rho \in (\alpha, \beta)$ with $g(\rho) \ne 0$. If $g(\rho) > 0$ is the maximum of $g$, then $g'_+(\rho) \le 0 \le g'_-(\rho)$. If $g(\rho) < 0$ is the minimum, then $g'_+(\rho) \ge 0 \ge g'_-(\rho)$. The one-sided derivatives exist because $g$ is a polynomial on each side of $\rho$ near $\rho$. $\square$

## The key lemma

Say that $g$ **changes sign weakly** at $\sigma$ if $g(\sigma^-) \, g(\sigma^+) \le 0$. If $g$ is continuous at $\sigma$, this means $g(\sigma) = 0$.

**Lemma 3.** *Let $q \ge 0$, $m \ge 0$, and knots $t_0 \le \cdots \le t_{m+q+1}$ with $t_k < t_{k+q+1}$ for all $k$. Let $\sigma_0 < \cdots < \sigma_m$ with $t_k < \sigma_k < t_{k+q+1}$ for all $k$. If $g = \sum_{k=0}^{m} d_k N_{k,q}$ changes sign weakly at every $\sigma_k$, then $d_0 = \cdots = d_m = 0$.*

*Proof.* By induction on $q$, and for fixed $q$ by induction on $m$.

*$q = 0$.* The spans $[t_k, t_{k+1})$ are disjoint and $\sigma_k$ is inside the span of $N_{k,0}$, so $g = d_k$ on both sides of $\sigma_k$. Then $d_k^2 \le 0$ and $d_k = 0$.

*$q \ge 1$, splitting on the left.* Suppose $\sigma_{i-1} < t_i$ for some $1 \le i \le m$. Near each $\sigma_k$ with $k \le i - 1$, on both sides, the functions $N_{j,q}$ with $j \ge i$ are $0$, because $\sigma_k < t_i \le t_j$. So $g_1 = \sum_{k<i} d_k N_{k,q}$ has the same one-sided limits as $g$ at $\sigma_0, \ldots, \sigma_{i-1}$. This is an instance of the lemma with $i - 1 < m$ in place of $m$, on the knots $t_0, \ldots, t_{i+q}$, so $d_0 = \cdots = d_{i-1} = 0$. Then $g = \sum_{k \ge i} d_k N_{k,q}$, an instance with $m - i < m$ on the knots $t_i, \ldots, t_{m+q+1}$, and the rest of the $d_k$ are $0$.

*$q \ge 1$, splitting on the right.* Suppose $\sigma_i > t_{i+q}$ for some $1 \le i \le m$. Near each $\sigma_k$ with $k \ge i$ the functions $N_{j,q}$ with $j \le i - 1$ are $0$, because their supports end at $t_{j+q+1} \le t_{i+q} < \sigma_k$. As before, first $d_i = \cdots = d_m = 0$, and then $d_0 = \cdots = d_{i-1} = 0$.

*$q \ge 1$, no split.* Now for every $1 \le i \le m$,
$$t_i \le \sigma_{i-1} \quad \text{and} \quad \sigma_i \le t_{i+q}. \tag{NS}$$

(a) *Continuity.* We show that every $N_{j,q}$, $0 \le j \le m$, is continuous on the open interval $(t_0, t_{m+q+1})$. By (F3) a jump can occur only at $t_j$ when $t_j = t_{j+q}$, or at $t_{j+q+1}$ when $t_{j+1} = t_{j+q+1}$. For $j = 0$ the first point is $t_0$, and for $j = m$ the second is $t_{m+q+1}$, both outside the open interval. For $1 \le j \le m$, (NS) and the hypothesis give $t_j \le \sigma_{j-1} < t_{j+q}$, so $t_j \ne t_{j+q}$. For $0 \le j \le m - 1$, they give $t_{j+1} < \sigma_{j+1} \le t_{j+q+1}$, so $t_{j+1} \ne t_{j+q+1}$. So $g$ is continuous on $(t_0, t_{m+q+1})$, and $g(\sigma_k) = 0$ for every $k$.

(b) *The derivative.* On each open knot span, by (F4),
$$g' = h := \sum_{k=0}^{m+1} e_k N_{k,q-1}, \qquad e_k = \frac{q \, (d_k - d_{k-1})}{t_{k+q} - t_k}, \quad d_{-1} = d_{m+1} = 0,$$
where a term with $t_{k+q} = t_k$ is left out; its function $N_{k,q-1}$ is $0$. At a point $\rho$ where $g$ is continuous, the right derivative of $g$ is the derivative at $\rho$ of the polynomial piece to the right of $\rho$, which is $h(\rho^+)$; in the same way the left derivative is $h(\rho^-)$.

(c) *Points for the derivative.* For $1 \le k \le m$, Lemma 2 on $[\sigma_{k-1}, \sigma_k]$ gives $\rho_k \in (\sigma_{k-1}, \sigma_k)$ at which $h$ changes sign weakly. By (NS) and the hypothesis,
$$t_k \le \sigma_{k-1} < \rho_k < \sigma_k \le t_{k+q}, \qquad \text{so } t_k < \rho_k < t_{k+q}.$$
At the left end there are two cases. If $\sigma_0 \ge t_q$, all $\rho_k$ lie to the right of $t_q$, and $N_{0,q-1}$, with support in $[t_0, t_q)$, is $0$ near every $\rho_k$; put $k_0 = 1$. If $\sigma_0 < t_q$, then $t_0 < \sigma_0 < t_q$, so no $N_{j,q}$ jumps at $t_0$ (for $j = 0$ because $t_0 < t_q$, for $j \ge 1$ because $t_j = t_{j+q}$ would put this value at least at $t_{q+1} > \sigma_0$), and no support ends at $t_0$, because $t_{j+q+1} \ge t_{q+1} > t_0$. With (a), $g$ is continuous on $[t_0, \sigma_0]$, $g(t_0) = 0$ because $g = 0$ to the left of $t_0$, and $g(\sigma_0) = 0$. Lemma 2 gives $\rho_0 \in (t_0, \sigma_0) \subset (t_0, t_q)$ where $h$ changes sign weakly; put $k_0 = 0$. The right end is the mirror image: if $\sigma_m \le t_{m+1}$, $N_{m+1,q-1}$ is $0$ near every $\rho_k$ and $k_1 = m$; if $\sigma_m > t_{m+1}$, then $t_{m+1} < \sigma_m < t_{m+q+1}$, no $N_{j,q}$ jumps at $t_{m+q+1}$ (by (F3) a jump of $N_{j,q}$ there would need $t_j$ or $t_{j+1}$ to be equal to $t_{m+q+1}$, but both are at most $t_{m+1} < t_{m+q+1}$), so $g$ is continuous on $[\sigma_m, t_{m+q+1}]$ with $g = 0$ at both ends, Lemma 2 gives $\rho_{m+1} \in (\sigma_m, t_{m+q+1}) \subset (t_{m+1}, t_{m+q+1})$, and $k_1 = m + 1$.

(d) *Induction.* The points $\rho_{k_0} < \cdots < \rho_{k_1}$ are increasing, because they are separated by the $\sigma_k$. For $k_0 \le k \le k_1$ we have $t_k < \rho_k < t_{k+q}$, so $N_{k,q-1}$ is not identically $0$. Near each $\rho_k$ the terms of $h$ with indices outside $k_0, \ldots, k_1$ are $0$, so $\sum_{k=k_0}^{k_1} e_k N_{k,q-1}$ changes sign weakly at every $\rho_k$. This is an instance of the lemma for the degree $q - 1$ on the knots $t_{k_0}, \ldots, t_{k_1+q}$. By the induction hypothesis $e_k = 0$ for $k_0 \le k \le k_1$, in particular for $1 \le k \le m$. Since $t_{k+q} > t_k$ for these $k$, $d_0 = d_1 = \cdots = d_m$.

(e) *End.* So $g = d_0 \sum_{j=0}^{m} N_{j,q}$ and $0 = g(\sigma_0) = d_0 \sum_j N_{j,q}(\sigma_0)$. Every term is nonnegative and $N_{0,q}(\sigma_0) > 0$ by (F2), so $d_0 = 0$. (For $m = 0$ steps (c) and (d) are not needed.) $\square$

## Sufficiency

Let $N_i(\tau_i) \ne 0$ for every $i$. We prove that $A$ is nonsingular by induction on $n$.

*A site at a knot of multiplicity $p + 1$.* Suppose $\tau_i = t_i$ for some $i$. By Lemma 1, $t_i = t_{i+p} < t_{i+p+1}$. For $j < i$, the support of $N_j$ ends at $t_{j+p+1} \le t_{i+p} = t_i$, so $N_j = 0$ at $t_i$ and at every site $\tau_k \ge t_i$, that is, for $k \ge i$. For $j > i$, $N_j$ is $0$ at every site $\tau_k < t_i$, that is, for $k < i$, and also at $\tau_i = t_i$: if $t_j > t_i$ by (F1), and if $t_j = t_i$ by Lemma 1, since $t_j = t_{j+p}$ would give $t_i = t_{i+p+1}$. So, with the rows and columns in their order, row $i$ is the unit row $e_i$, the rows $k < i$ are $0$ in the columns $j \ge i$, and the rows $k > i$ are $0$ in the columns $j < i$. Hence
$$\det A = \det A_1 \cdot 1 \cdot \det A_2,$$
where $A_1$ is the collocation matrix of $N_0, \ldots, N_{i-1}$ at $\tau_0, \ldots, \tau_{i-1}$ and $A_2$ that of $N_{i+1}, \ldots, N_n$ at $\tau_{i+1}, \ldots, \tau_n$. These are the B-splines of the knot vectors $t_0, \ldots, t_{i+p}$ and $t_{i+1}, \ldots, t_{n+p+1}$, the diagonal entries are the same as in $A$, and $i < n + 1$ and $n - i < n + 1$, so both determinants are nonzero by the induction hypothesis. An empty block has determinant $1$.

*All sites inside the supports.* Otherwise $t_i < \tau_i < t_{i+p+1}$ for every $i$, by part 2. If $A c = 0$, then $g = \sum_j c_j N_j$ is $0$ at every $\tau_i$, and since $g$ is continuous from the right, $g(\tau_i^+) = 0$ and $g$ changes sign weakly at every $\tau_i$. Lemma 3 with $q = p$, $m = n$ and $\sigma_i = \tau_i$ gives $c = 0$. So $A$ is nonsingular.

This proves part 1.

## The closing rule (part 3)

Let $b = t_{n+1} = t_{n+p+1}$ and $\tau_n = b$, with the limits from the left in row $n$. The hypothesis $t_n < t_{n+p+1}$ gives $t_n < b$, so $[t_n, b)$ is the last nonempty span. Adding $p$ knots below $t_0$ does not change $N_0, \ldots, N_n$, because each B-spline depends only on its own knots, so we may assume that the functions $N_{n-p}, \ldots, N_{n-1}$ exist.

On $[t_n, b)$ the function $N_{n+1,r-1}$ is $0$ by (F1), so the recursion gives $N_{n,r}(x) = \frac{x - t_n}{t_{n+r} - t_n} N_{n,r-1}(x)$ for $1 \le r \le p$, and $N_{n,p}(x) = \prod_{r=1}^{p} \frac{x - t_n}{t_{n+r} - t_n}$. Since $t_{n+r} = b$ for $1 \le r \le p$, the limit from the left at $b$ is $1$. On the same span $\sum_{i=n-p}^{n} N_{i,p}(x) = 1$, by the partition of unity on a nonempty span (the coefficient of $y^p$ in Marsden's identity on the Curry-Schoenberg proof page). All terms are nonnegative, so the limits from the left of $N_j$, $j < n$, at $b$ are $0$. Hence row $n$ is the unit row $e_n$ and $N_n(\tau_n) = 1$. The other sites satisfy $\tau_k < t_{n+1}$, so their rows are unchanged, and $\det A$ equals the determinant of the collocation matrix of $N_0, \ldots, N_{n-1}$ at $\tau_0, \ldots, \tau_{n-1}$, which is the case $n - 1$ of part 1 on the knots $t_0, \ldots, t_{n+p}$ and has the same diagonal. $\blacksquare$
