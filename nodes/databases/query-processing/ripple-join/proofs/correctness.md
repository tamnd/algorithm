---
title: The ripple join estimate is unbiased at every step, with an exact variance formula, and it equals the answer when both inputs are read
proves: [correctness, termination, time.average]
status: full
---

We use the line numbers of the pseudocode. $R$ has $N$ tuples and $S$ has $M$ tuples, and each stored tuple is a distinct occurrence. For $r \in R$ and $s \in S$ let $v(r, s)$ be the value of the pair when the keys are equal and not NULL, and $v(r, s) = 0$ otherwise. The query asks for $\tau = \sum_{r \in R} \sum_{s \in S} v(r, s)$. COUNT is the case $v = 1$ on joining pairs. After step $t$ the algorithm has read the sets $R_t$ and $S_t$ of sizes $n = |R_t|$ and $m = |S_t|$. These sizes depend only on $t$, $N$, $M$ and the aspect ratio $(\beta_R, \beta_S)$, not on the random order. The estimate of line L5 is

$$\hat\tau_t = \frac{N M}{n m} \Sigma_t, \qquad \Sigma_t = \text{the running sum}.$$

**Lemma 1 (the running sum covers the rectangle).** After step $t$, $\Sigma_t = \sum_{r \in R_t} \sum_{s \in S_t} v(r, s)$.

*Proof.* Line L3 adds a tuple $r$ to $R_t$ and adds $v(r, s)$ for every $s$ already in $S_t$. Line L4 adds a tuple $s$ and adds $v(r, s)$ for every $r$ already in $R_t$, including the tuples of $R$ added in the same step. So each pair $(r, s)$ of $R_t \times S_t$ is added once, when the later of its two tuples is added, and no pair outside the rectangle is added. The hash form looks up only the tuples with the same key, which are exactly the pairs with $v(r, s)$ possibly nonzero, so both forms give the same sum. $\square$

**Theorem 1 (unbiased).** If the orders of $R$ and $S$ are independent and uniformly random, then $E[\hat\tau_t] = \tau$ at every step $t$ with $n, m \ge 1$.

*Proof.* A prefix of length $n$ of a uniformly random order of $R$ is a uniformly random subset of size $n$, so $P(r \in R_t) = n / N$ for each $r$, and in the same way $P(s \in S_t) = m / M$. The two orders are independent, so $P(r \in R_t \text{ and } s \in S_t) = n m / (N M)$. By Lemma 1 and [linearity of expectation](/linearity-of-expectation/),

$$E[\hat\tau_t] = \frac{N M}{n m} \sum_{r, s} v(r, s) \, P(r \in R_t, s \in S_t) = \sum_{r, s} v(r, s) = \tau. \qquad \blacksquare$$

The estimate of AVG is the ratio of the SUM and COUNT estimates. A ratio of unbiased estimates is not unbiased in general, so the AVG estimate is only consistent.

**Theorem 2 (exact variance).** Let $\mu = \tau / (N M)$, $a(r) = \frac{1}{M} \sum_s v(r, s)$, $b(s) = \frac{1}{N} \sum_r v(r, s)$ and $g(r, s) = v(r, s) - a(r) - b(s) + \mu$. Let $f_R = n / N$ and $f_S = m / M$, and let

$$S_a^2 = \frac{\sum_r (a(r) - \mu)^2}{N - 1}, \quad S_b^2 = \frac{\sum_s (b(s) - \mu)^2}{M - 1}, \quad S_g^2 = \frac{\sum_{r, s} g(r, s)^2}{(N - 1)(M - 1)}.$$

Then, with a term read as 0 when its factor $1 - f_R$ or $1 - f_S$ is 0,

$$\operatorname{Var}(\hat\tau_t) = N^2 M^2 \left( \frac{(1 - f_R) S_a^2}{n} + \frac{(1 - f_S) S_b^2}{m} + \frac{(1 - f_R)(1 - f_S) S_g^2}{n m} \right).$$

*Proof.* Write $v(r, s) = \mu + (a(r) - \mu) + (b(s) - \mu) + g(r, s)$ and sum over the rectangle. With $\bar a$ the mean of $a$ over $R_t$ and $\bar b$ the mean of $b$ over $S_t$,

$$\frac{\hat\tau_t}{N M} = \frac{\Sigma_t}{n m} = \mu + (\bar a - \mu) + (\bar b - \mu) + G, \qquad G = \frac{1}{n m} \sum_{r \in R_t} \sum_{s \in S_t} g(r, s).$$

The function $g$ has zero row sums and zero column sums: $\sum_s g(r, s) = M a(r) - M a(r) - M \mu + M \mu = 0$, and the same for columns.

*The three terms are uncorrelated.* $\bar a$ depends only on $R_t$ and $\bar b$ only on $S_t$, which are independent. Given $R_t$, each $s$ is in $S_t$ with probability $m / M$, so $E[G \mid R_t] = \frac{1}{n M} \sum_{r \in R_t} \sum_s g(r, s) = 0$. So $\operatorname{Cov}(\bar a, G) = E[(\bar a - \mu) E[G \mid R_t]] = 0$, and in the same way $\operatorname{Cov}(\bar b, G) = 0$.

*The first two terms.* $\bar a$ is the mean of a simple random sample of size $n$ without replacement from the $N$ values $a(r)$, so its variance is $(1 - f_R) S_a^2 / n$, and the same holds for $\bar b$.

*The third term.* $E[G] = 0$. For $r \ne r'$ in $R$, $P(r, r' \in R_t) = q_R = \frac{n(n - 1)}{N(N - 1)}$, and $P(r \in R_t) = p_R = n / N$; the same with $q_S$ and $p_S$ for $S$. Then

$$E[G^2] = \frac{1}{n^2 m^2} \sum_{r, r'} \sum_{s, s'} g(r, s) g(r', s') \, P(r, r' \in R_t) \, P(s, s' \in S_t).$$

For fixed $s, s'$, the sum over $r \ne r'$ of $g(r, s) g(r', s')$ equals $(\sum_r g(r, s))(\sum_{r'} g(r', s')) - \sum_r g(r, s) g(r, s') = -\sum_r g(r, s) g(r, s')$. So the sum over $r, r'$ is $(p_R - q_R) \sum_r g(r, s) g(r, s')$. Doing the same over $s, s'$ gives

$$E[G^2] = \frac{(p_R - q_R)(p_S - q_S)}{n^2 m^2} \sum_{r, s} g(r, s)^2.$$

Since $p_R - q_R = \frac{n}{N} \cdot \frac{N - n}{N - 1}$, this is $\frac{(1 - f_R)(1 - f_S)}{n m} S_g^2$. Adding the three variances and multiplying by $N^2 M^2$ gives the formula. When $N = 1$ the sample is all of $R$, $f_R = 1$, and the terms with $1 - f_R$ vanish. $\blacksquare$

The third term falls like $1 / (n m)$, faster than the first two, so for large samples the variance is close to the first two terms. The implementation estimates $S_a^2$ by the sample variance of $\frac{1}{m} \sum_{s \in S_t} v(r, s)$ over $r \in R_t$, and $S_b^2$ in the same way, and uses $\hat\tau_t \pm z \sqrt{\widehat{\operatorname{Var}}}$ as the interval. That the interval has coverage close to the nominal level rests on a [central limit theorem](/central-limit-theorem/) for large samples. It is an approximation, not a bound for a given $n$.

**Theorem 3 (the end is exact, and termination).** Each step reads at least one tuple while some tuple is unread, so after at most $N + M$ steps $R_t = R$ and $S_t = S$. Then $\hat\tau_t = \frac{N M}{N M} \tau = \tau$ by Lemma 1, and every term of the variance has a zero factor. $\blacksquare$

**Theorem 4 (work).** Let $j_t$ be the number of joining pairs in $R_t \times S_t$. With hash tables in expected $O(1)$ time per operation, the hash form does expected $O(n + m + j_t)$ work up to step $t$, plus $O(1)$ per step for the estimate if the sums $\sum_r A(r)^2$ and $\sum_s B(s)^2$ of the squared row and column sums are kept up to date. The nested-loops form does $\Theta(n m)$ comparisons.

*Proof.* Each read costs one insert and one lookup. Each joining pair is met once (Lemma 1) and changes one row sum $A(r)$ and one column sum $B(s)$ by $v$, and $\sum A(r)^2$ changes by $2 A(r) v + v^2$, computed in $O(1)$. The sample variances follow from these sums and $\Sigma_t$. The nested form compares each new tuple with every tuple read from the other input, which gives $n m$ comparisons for the rectangle. $\blacksquare$

The implementation recomputes the sample variances at each step in $O(n + m)$ time, which is simpler and does not change the results.
