---
title: The Clopper-Pearson interval is well defined and has coverage at least 1 - alpha for every p
proves: [correctness]
status: full
---

Let $X \sim \text{Binomial}(n, p)$ with $n \ge 1$, and let $0 < \alpha < 1$. Write $G_p(x) = P_p(X \ge x)$ and $F_p(x) = P_p(X \le x)$. The interval of the page is $[L(x), U(x)]$ with $L(0) = 0$, $U(n) = 1$, and otherwise

$$G_{L(x)}(x) = \alpha/2 \quad (1 \le x \le n), \qquad F_{U(x)}(x) = \alpha/2 \quad (0 \le x \le n - 1).$$

**Lemma 1 (the tail is a Beta integral).** For $1 \le x \le n$ and $0 \le p \le 1$,

$$G_p(x) = \frac{n!}{(x-1)!\,(n-x)!} \int_0^p t^{x-1} (1 - t)^{n-x} \, dt = I_p(x, n - x + 1).$$

*Proof.* Both sides are $0$ at $p = 0$. Differentiate the sum $G_p(x) = \sum_{k=x}^{n} \binom{n}{k} p^k (1-p)^{n-k}$ term by term. Using $k \binom{n}{k} = n \binom{n-1}{k-1}$ and $(n - k)\binom{n}{k} = n \binom{n-1}{k}$,

$$\frac{d}{dp} G_p(x) = n \sum_{k=x}^{n} \Big[\tbinom{n-1}{k-1} p^{k-1}(1-p)^{n-k} - \tbinom{n-1}{k} p^{k}(1-p)^{n-k-1}\Big],$$

with the convention $\binom{n-1}{n} = 0$. The sum telescopes to its first term, $n \binom{n-1}{x-1} p^{x-1} (1-p)^{n-x}$, which is the integrand. $\square$

**Lemma 2 (the endpoints exist, are unique and are ordered).** For $1 \le x \le n$, the map $p \mapsto G_p(x)$ is continuous and strictly increasing on $[0, 1]$, from $0$ to $1$, because its derivative in Lemma 1 is positive on $(0, 1)$. So $L(x)$ exists, is unique and lies in $(0, 1)$. For $0 \le x \le n - 1$, $F_p(x) = 1 - G_p(x + 1)$ is continuous and strictly decreasing from $1$ to $0$, so $U(x)$ exists, is unique and lies in $(0, 1)$. Moreover:

- $p < L(x)$ if and only if $G_p(x) < \alpha/2$, and $p > U(x)$ if and only if $F_p(x) < \alpha/2$, by strict monotonicity.
- $L(x) < U(x)$. At $p = L(x)$ with $x < n$, $F_p(x) = 1 - G_p(x) + P_p(X = x) > 1 - \alpha/2 > \alpha/2$, so $L(x) < U(x)$ by the previous item. The cases $x = 0$ and $x = n$ are clear.
- $L$ and $U$ are strictly increasing in $x$, because $G_p(x)$ is strictly decreasing in $x$ for fixed $p \in (0, 1)$, and so is $F_p(x)$ as a function of $-x$.

By Lemma 1, $L(x)$ is the $\alpha/2$ quantile of $\text{Beta}(x, n - x + 1)$. By the same lemma applied to $G_p(x + 1)$, $U(x)$ is the $1 - \alpha/2$ quantile of $\text{Beta}(x + 1, n - x)$. $\square$

**Theorem (conservative coverage).** For every $p \in [0, 1]$, $P_p\big(L(X) \le p \le U(X)\big) \ge 1 - \alpha$.

*Proof.* The interval misses $p$ when $L(X) > p$ or $U(X) < p$. These events are disjoint, because $L(X) < U(X)$. If $p = 0$ then $L(X) > 0$ requires $X \ge 1$, which has probability $0$, and $U(X) < 0$ is impossible; the case $p = 1$ is symmetric. So let $0 < p < 1$.

By Lemma 2, $\{x : L(x) > p\} = \{x \ge 1 : G_p(x) < \alpha/2\}$; for $x = 0$, $L(0) = 0 \le p$. The set $A = \{x : G_p(x) < \alpha/2\}$ is an upper set of the integers $0, \ldots, n$, because $G_p(x)$ is decreasing in $x$. If $A$ is empty, the event has probability $0$. Otherwise let $x^*$ be its smallest element. Then $P_p(X \in A) = P_p(X \ge x^*) = G_p(x^*) < \alpha/2$.

In the same way, $\{x : U(x) < p\} = \{x \le n - 1 : F_p(x) < \alpha/2\}$ is a lower set with largest element $x^{**}$ when it is not empty, and its probability is $F_p(x^{**}) < \alpha/2$.

So the probability of a miss is less than $\alpha/2 + \alpha/2 = \alpha$, and the coverage is greater than $1 - \alpha$. $\square$

The inequality is strict for each $p$ in $(0, 1)$, but the infimum of the coverage over $p$ can approach $1 - \alpha$ for large $n$. The coverage is not continuous in $p$: it jumps at each endpoint $L(x)$ and $U(x)$.

**Duality.** By Lemma 2, $p_0 \in (L(x), U(x))$ if and only if $G_{p_0}(x) > \alpha/2$ and $F_{p_0}(x) > \alpha/2$, that is, if and only if neither one-sided exact [binomial test](/binomial-test/) rejects at level $\alpha/2$. This is the doubling rule of the two-sided test, and the theorem above is the general [test-interval duality](/test-interval-duality/) for it.

**The algorithm.** Lines L1 and L3 set the fixed endpoints. Lines L2 and L4 find the unique roots of Lemma 2 by bisection on $[0, 1]$. Bisection keeps a bracket $[lo, hi]$ with $f(lo) < $ target $\le f(hi)$ for the increasing function $f$, so the root stays in the bracket, and the loop stops when the midpoint equals an end of the bracket, that is, when the bracket is two adjacent floating point numbers. Each step evaluates one binomial tail of at most $n + 1$ terms. $\square$
