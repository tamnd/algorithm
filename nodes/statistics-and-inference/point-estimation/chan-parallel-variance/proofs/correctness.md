---
title: The merge formula is exact, associative and commutative
proves: [correctness]
status: full
---

The arithmetic is exact. A *summary* is a triple $(n, m, M)$ with $n > 0$. The summary of a nonempty finite list $x_1, \ldots, x_k$ is $\sigma(x) = (k, \bar x, \mathrm{SS})$ with $\bar x = \frac1k \sum_i x_i$ and $\mathrm{SS} = \sum_i (x_i - \bar x)^2$.

**Lemma 1 (weighted shift).** Let $w_1, \ldots, w_r > 0$, $W = \sum_j w_j$, real $y_1, \ldots, y_r$ and $\mu = \frac1W\sum_j w_j y_j$. Then for every real $c$,
$$\sum_{j=1}^r w_j (y_j - c)^2 = \sum_{j=1}^r w_j (y_j - \mu)^2 + W(\mu - c)^2.$$

*Proof.* Write $y_j - c = (y_j - \mu) + (\mu - c)$ and expand. The cross terms add up to $2(\mu - c)\sum_j w_j(y_j - \mu) = 2(\mu - c)(W\mu - W\mu) = 0$, and the last terms add up to $W(\mu - c)^2$. $\square$

**Lemma 2 (the merge in centred form).** For summaries $a = (n_a, m_a, M_a)$ and $b = (n_b, m_b, M_b)$, COMBINE (lines L1 to L5) returns $(n, m, M)$ with
$$n = n_a + n_b, \qquad m = \frac{n_a m_a + n_b m_b}{n}, \qquad M = M_a + M_b + n_a (m_a - m)^2 + n_b (m_b - m)^2.$$

*Proof.* Line L1 gives $n$. With $\delta = m_b - m_a$ (line L2), line L3 gives $m = m_a + \delta n_b/n = (n m_a + n_b m_b - n_b m_a)/n = (n_a m_a + n_b m_b)/n$. Then $m_a - m = -\delta n_b/n$ and $m_b - m = \delta n_a/n$, so
$$n_a(m_a - m)^2 + n_b(m_b - m)^2 = \frac{\delta^2 (n_a n_b^2 + n_b n_a^2)}{n^2} = \frac{\delta^2 n_a n_b (n_a + n_b)}{n^2} = \frac{\delta^2 n_a n_b}{n},$$
which is the term that line L4 adds to $M_a + M_b$. $\square$

**Theorem 1 (merge).** If $a = \sigma(x)$ and $b = \sigma(y)$ for nonempty lists $x$ and $y$, then COMBINE$(a, b) = \sigma(x \cdot y)$, the summary of the concatenation.

*Proof.* Let $(n, m, M)$ = COMBINE$(a, b)$. The list $x \cdot y$ has $n_a + n_b = n$ values with sum $n_a m_a + n_b m_b = n m$, so its mean is $m$ by Lemma 2. Its sum of squared deviations splits over the two parts:
$$\sum_{v \in x \cdot y}(v - m)^2 = \sum_{v \in x}(v - m)^2 + \sum_{v \in y}(v - m)^2 = M_a + n_a(m_a - m)^2 + M_b + n_b(m_b - m)^2,$$
by Lemma 1 with unit weights and $c = m$, once for $x$ (mean $m_a$, $\mathrm{SS} = M_a$) and once for $y$. By Lemma 2 this is $M$. $\square$

**Theorem 2 (associativity and commutativity).** COMBINE is commutative, and associative on all summaries, not only on summaries of data.

*Proof.* Lemma 2 is symmetric in $a$ and $b$, so COMBINE is commutative. For three summaries $a, b, c$, let $m_{ab}$ be the mean of COMBINE$(a, b)$ and $m$ the mean of the full merge, which is $\frac{1}{n_a + n_b + n_c}(n_a m_a + n_b m_b + n_c m_c)$ in either order. By Lemma 2 twice, the $M$ of COMBINE(COMBINE$(a, b), c)$ is
$$M_a + M_b + M_c + \big[n_a(m_a - m_{ab})^2 + n_b(m_b - m_{ab})^2 + (n_a + n_b)(m_{ab} - m)^2\big] + n_c(m_c - m)^2.$$
Lemma 1 with weights $n_a, n_b$, points $m_a, m_b$ (whose weighted mean is $m_{ab}$) and $c = m$ turns the bracket into $n_a(m_a - m)^2 + n_b(m_b - m)^2$. So
$$M = M_a + M_b + M_c + \sum_{i \in \{a, b, c\}} n_i (m_i - m)^2,$$
which is symmetric in $a, b, c$. The same expression results from COMBINE$(a$, COMBINE$(b, c))$, so the two are equal. $\square$

Hence the summaries with COMBINE form a commutative semigroup, and every tree of merges over a partition of the data into nonempty parts gives the same exact result $\sigma(x)$. Adding the triple $(0, 0, 0)$ as an identity, with the rule that COMBINE returns the other argument when one count is 0, makes it a commutative [monoid](/monoid/).

**Theorem 3 (PAIRWISE).** For $hi - lo \ge 1$, PAIRWISE$(x, lo, hi)$ returns $\sigma(x[lo \ldots hi-1])$.

*Proof.* By induction on $\ell = hi - lo$. For $\ell = 1$, line L6 returns $(1, x[lo], 0)$, the summary of one value. For $\ell \ge 2$, line L7 gives $lo < mid < hi$, since $1 \le \lfloor \ell/2 \rfloor < \ell$. Both calls of lines L8 and L9 have length between 1 and $\ell - 1$, so by induction they return $\sigma(x[lo \ldots mid-1])$ and $\sigma(x[mid \ldots hi-1])$. By Theorem 1, line L10 returns the summary of their concatenation, which is $x[lo \ldots hi-1]$. $\square$

**Corollary.** For $n \ge 2$, PAIRWISE-VARIANCE returns the mean, $\mathrm{SS}/(n - 1)$ and $\mathrm{SS}$ of $x_1, \ldots, x_n$. Each call on length $\ell \ge 2$ makes two calls on strictly shorter lengths, so the recursion terminates.

**Cost.** The recursion tree has $n$ leaves and $n - 1$ internal nodes, one COMBINE each. Counting the counts as integers, COMBINE does 10 floating-point operations: one subtraction in line L2; a multiplication, a division and an addition in line L3; and in line L4 the products $\delta \cdot \delta$, $\cdot\, n_a$, $\cdot\, n_b$, the division by $n$ and two additions. With the division of line L12 the total is $10(n - 1) + 1 = 10n - 9$. The recursion depth is $\lceil \log_2 n \rceil$, so the stack is $\Theta(\log n)$. The two calls of lines L8 and L9 are independent, so with them run in parallel the span satisfies $D(\ell) = D(\lceil \ell/2 \rceil) + O(1)$, which gives $D(n) = \Theta(\log n)$, with work $\Theta(n)$. $\square$
