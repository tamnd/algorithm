---
tag: VYC79B
kind: theorem
slug: walds-equation
name: Wald's equation
aliases:
- Wald's identity
area: foundations/probabilistic-analysis
level: advanced
summary: For i.i.d. X_i with finite mean and a stopping time N with finite mean, the expected sum of the first N terms is E[N] E[X_1].
prereqs: [expected-value, independent-random-variables, linearity-of-expectation, martingale]
see_also: [optional-stopping-theorem, rejection-sampling, las-vegas-algorithm, geometric-distribution, markov-inequality, monte-carlo-algorithm]
sources:
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 13, Section 13.3, Wald's Equation (statement, proof as a corollary of the martingale stopping theorem, and examples)
  - paper: doi:10.1214/aoms/1177731235
    title: Abraham Wald, On cumulative sums of random variables, Annals of Mathematical Statistics 15(3), 1944, pages 283 to 296
    locator: the identity for the expected value of a sum stopped at a random time
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Chapter 4, Tail Inequalities, Section 4.4, Martingales (stopping times and Wald's equation)
  - book: isbn:9780521406055
    title: David Williams, Probability with Martingales, Cambridge University Press, 1991
    locator: Chapter 10, Martingales (Theorem 10.10, the optional stopping theorem used in the second proof)
---

Wald's equation says that if $X_1, X_2, \ldots$ are independent copies of a random variable with finite mean $\mu$, and $N$ is a [stopping time](/optional-stopping-theorem/) with $\mathbb E[N] < \infty$, then $\mathbb E[X_1 + \cdots + X_N] = \mathbb E[N]\,\mu$. It is [linearity of expectation](/linearity-of-expectation/) for a sum whose number of terms is random and may depend on the terms already seen. In algorithm analysis it gives the expected total cost of repeated independent trials, as in [rejection sampling](/rejection-sampling/) and the restarts of a [Las Vegas algorithm](/las-vegas-algorithm/). The equation fails when $N$ looks into the future, and when $\mathbb E[N] = \infty$.

## Statement

Let $(\mathcal F_n)_{n \ge 0}$ be a filtration, and let $X_1, X_2, \ldots$ be random variables such that, for each $n \ge 1$, $X_n$ is $\mathcal F_n$-measurable and independent of $\mathcal F_{n-1}$, and all $X_n$ have the same distribution with $\mathbb E|X_1| < \infty$. Let $\mu = \mathbb E[X_1]$ and $S_n = X_1 + \cdots + X_n$, with $S_0 = 0$. Let $N$ be a stopping time with values in $\{0, 1, 2, \ldots\}$: $\{N = n\} \in \mathcal F_n$ for each $n$.

**Theorem (Wald's equation).** If $\mathbb E[N] < \infty$, then $S_N$ is integrable and
$$ \mathbb E[S_N] = \mathbb E[N]\,\mu. $$
If $X_n \ge 0$ almost surely, the equation holds in $[0, \infty]$ without the hypothesis $\mathbb E[N] < \infty$, with the convention $0 \cdot \infty = 0$.

**Theorem (Wald's second identity).** If in addition $\mu = 0$ and $\sigma^2 = \mathbb E[X_1^2] < \infty$, and $\mathbb E[N] < \infty$, then $\mathbb E[S_N^2] = \sigma^2\,\mathbb E[N]$. Applied to $X_n - \mu$, this gives $\mathbb E[(S_N - N\mu)^2] = \sigma^2\,\mathbb E[N]$ when $\sigma^2 = \operatorname{Var}(X_1)$.

Two special cases are the usual forms.

- *$N$ is a stopping time of the sequence.* The $X_n$ are independent and identically distributed, $\mathcal F_n = \sigma(X_1, \ldots, X_n)$, and the decision to stop after $n$ terms depends only on $X_1, \ldots, X_n$. The filtration may also contain extra randomness that is independent of $X_{n+1}, X_{n+2}, \ldots$.
- *$N$ is independent of the sequence.* The $X_n$ are i.i.d., $N$ is independent of $(X_n)$, and $\mathcal F_n = \sigma(N, X_1, \ldots, X_n)$. Then $\{N = n\} \in \mathcal F_0$, and $X_n$ is independent of $\mathcal F_{n-1} = \sigma(N, X_1, \ldots, X_{n-1})$.

The proof uses the identical distribution only through $\mathbb E[X_n] = \mu$ and $\mathbb E|X_n| = \mathbb E|X_1|$. So the equation holds for independent $X_n$ with a common mean $\mu$ and $\sup_n \mathbb E|X_n| < \infty$, with the same proof.

## In plain words

You repeat an experiment, and each repetition gives a random amount, for example the time it took. The repetitions are independent and alike. After each one you decide, from what you have seen so far, whether to go on. The theorem says that the expected total is the expected number of repetitions times the expected amount of one repetition.

This looks like plain averaging, but it is not obvious, because the number of repetitions depends on the amounts. If you stop after a large amount, the last amount tends to be large. The theorem says that this bias cancels out, as long as you decide to stop from the past only and the expected number of repetitions is finite.

If the rule to stop may peek at the next result, the equation fails. If the expected number of repetitions is infinite, it can fail too.

## Proof

**Step 1 (the event of the $i$-th term is decided before it).** For $i \ge 1$, $\{N \ge i\} = \Omega \setminus \{N \le i - 1\}$, and $\{N \le i - 1\} = \bigcup_{j \le i-1}\{N = j\} \in \mathcal F_{i-1}$. So $\{N \ge i\} \in \mathcal F_{i-1}$, and it is independent of $X_i$.

**Step 2 (the sum as a series).** Since $\mathbb E[N] < \infty$, $N < \infty$ almost surely, and
$$ S_N = \sum_{i=1}^{\infty} X_i\,1_{\{N \ge i\}}, $$
where for each outcome only the first $N$ terms are not zero.

**Step 3 (absolute convergence).** By Step 1 and independence, $\mathbb E\big[|X_i|\,1_{\{N \ge i\}}\big] = \mathbb E|X_i|\,\Pr(N \ge i) = \mathbb E|X_1|\,\Pr(N \ge i)$. The terms are not negative, so by the monotone convergence theorem
$$ \mathbb E\Big[\sum_{i \ge 1}|X_i|\,1_{\{N \ge i\}}\Big] = \mathbb E|X_1|\sum_{i \ge 1}\Pr(N \ge i) = \mathbb E|X_1|\,\mathbb E[N] < \infty, $$
using the tail sum formula $\mathbb E[N] = \sum_{i \ge 1}\Pr(N \ge i)$ for the [expected value](/expected-value/) of a variable with values in $\{0, 1, 2, \ldots\}$.

**Step 4 (exchange of sum and expectation).** By Step 3, $Y = \sum_i |X_i|\,1_{\{N \ge i\}}$ is integrable, and $|S_N| \le Y$, so $S_N$ is integrable. The partial sums $\sum_{i \le n} X_i 1_{\{N \ge i\}} = S_{N \wedge n}$ are bounded by $Y$ and tend to $S_N$, so the dominated convergence theorem allows the exchange:
$$ \mathbb E[S_N] = \sum_{i \ge 1}\mathbb E\big[X_i\,1_{\{N \ge i\}}\big] = \sum_{i \ge 1}\mu\,\Pr(N \ge i) = \mu\,\mathbb E[N], $$
where the middle equality is again Step 1 and independence. $\square$

If $X_n \ge 0$, Steps 1 to 3 with $X_i$ in place of $|X_i|$ give $\mathbb E[S_N] = \mu\,\mathbb E[N]$ in $[0, \infty]$ without the assumption $\mathbb E[N] < \infty$; on the event $\{N = \infty\}$ the series is the infinite sum, and if $\mu = 0$ then all $X_i = 0$ almost surely and both sides are 0.

**Second proof, by optional stopping.** Let $M_n = S_n - n\mu$. Since $X_{n+1}$ is independent of $\mathcal F_n$, $\mathbb E[M_{n+1} - M_n \mid \mathcal F_n] = \mathbb E[X_{n+1}] - \mu = 0$, so $(M_n)$ is a [martingale](/martingale/), and $\mathbb E\big[|M_{n+1} - M_n| \,\big|\, \mathcal F_n\big] = \mathbb E|X_1 - \mu| \le 2\,\mathbb E|X_1|$, a constant. With $\mathbb E[N] < \infty$, case (b) of the [optional stopping theorem](/optional-stopping-theorem/) gives $\mathbb E[M_N] = M_0 = 0$, that is, $\mathbb E[S_N - N\mu] = 0$. Since $\mathbb E[N\mu]$ is finite, $\mathbb E[S_N] = \mu\,\mathbb E[N]$. $\square$

**Proof of the second identity.** Let $\mu = 0$. For $0 \le n < m$, $S_{N \wedge m} - S_{N \wedge n} = \sum_{i=n+1}^{m} X_i\,1_{\{N \ge i\}}$. Square and take expectations.

- *Diagonal terms.* By Step 1, $\mathbb E[X_i^2\,1_{\{N \ge i\}}] = \sigma^2\,\Pr(N \ge i)$.
- *Cross terms.* For $j < k$, the variable $X_j 1_{\{N \ge j\}} 1_{\{N \ge k\}}$ is $\mathcal F_{k-1}$-measurable and integrable, and $X_k$ is independent of $\mathcal F_{k-1}$ with mean 0. So $\mathbb E[X_j 1_{\{N \ge j\}}\,X_k 1_{\{N \ge k\}}] = 0$.

Hence $\mathbb E[(S_{N \wedge m} - S_{N \wedge n})^2] = \sigma^2\sum_{i=n+1}^m \Pr(N \ge i)$. The series $\sum_i \Pr(N \ge i) = \mathbb E[N]$ converges, so $(S_{N \wedge n})_n$ is a Cauchy sequence in $L^2$. It converges in $L^2$ to some $S'$, and a subsequence converges to $S'$ almost surely. But $S_{N \wedge n} \to S_N$ almost surely, so $S' = S_N$. Convergence in $L^2$ gives convergence of the second moments, and the case $n = 0$ of the computation gives
$$ \mathbb E[S_N^2] = \lim_{m \to \infty}\mathbb E[S_{N \wedge m}^2] = \lim_{m \to \infty}\sigma^2\sum_{i=1}^m \Pr(N \ge i) = \sigma^2\,\mathbb E[N]. \qquad \square $$

## Consequences

**Rolling a die until a 6.** Roll a fair die until the first 6, and add all the rolls, the 6 included. The number of rolls $N$ has the [geometric distribution](/geometric-distribution/) with parameter $\frac16$, so $\mathbb E[N] = 6$, and $N$ is a stopping time: the decision to stop after a roll depends on that roll and the earlier ones. Wald's equation gives $\mathbb E[S_N] = 6 \cdot 3.5 = 21$. A direct check: given $N$, each roll before the last is uniform on $\{1, \ldots, 5\}$ with mean 3, so $\mathbb E[S_N] = 3(\mathbb E[N] - 1) + 6 = 15 + 6 = 21$. Here the rolls that are counted are not a sample of the die with mean $3.5$: the last one is always 6, the others have mean 3. Wald's equation still holds, because the stopping rule does not look ahead.

**Rejection sampling with early rejection.** To draw a uniform integer in $\{0, 1, 2, 3, 4\}$ from fair random bits, draw 3 bits as a number in $\{0, \ldots, 7\}$ and accept if it is below 5; else start again. Each trial accepts with probability $5/8$, so the number of trials is geometric with mean $8/5$, and by Wald's equation the expected number of bits is $3 \cdot 8/5 = 4.8$. A better trial reads the bits from the most significant one and rejects as soon as the prefix shows the value is at least 5: the prefix 11 (values 6 and 7, probability $\frac14$) is rejected after 2 bits, and every other trial uses 3 bits. Now the cost $C_i$ of a trial depends on its outcome. The pairs (cost, outcome) of the trials are i.i.d., the number of trials $N$ is a stopping time for them, and $\mathbb E[C_i] = \frac14 \cdot 2 + \frac34 \cdot 3 = 2.75$. Wald's equation gives $\mathbb E[\text{bits}] = 2.75 \cdot 8/5 = 4.4$. The first step analysis $E = 2.75 + \frac38 E$ gives the same value $E = 4.4$.

**Las Vegas restarts.** Let a [Las Vegas algorithm](/las-vegas-algorithm/) have running time $T = 2^K$, where $\Pr(K = j) = 2^{-j}$ for $j \ge 1$. Then $\mathbb E[T] = \sum_j 2^j 2^{-j} = \infty$. Run it with a cutoff $2^k$: if a run has not finished after $2^k$ steps, stop it and start a new independent run. A run costs $\min(T, 2^k)$, with mean $\sum_{j=1}^k 2^j 2^{-j} + 2^k \cdot 2^{-k} = k + 1$, and succeeds with probability $1 - 2^{-k}$. The index of the first successful run is a stopping time with mean $1/(1 - 2^{-k})$, so by Wald's equation the expected total time is $(k + 1)/(1 - 2^{-k})$.

| cutoff $2^k$ | 2 | 4 | 8 | 16 | 32 | 64 | 128 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| expected total time | 4 | 4 | 4.571 | 5.333 | 6.194 | 7.111 | 8.063 |

Restarts turn an infinite expected time into the finite value 4. The same argument with [Markov's inequality](/markov-inequality/) bounds any Las Vegas algorithm with $\mathbb E[T] = t$ cut off at $2t$: each run costs at most $2t$ and succeeds with probability at least $\frac12$, so the expected total is at most $4t$.

**The duration of the gambler's ruin.** For the fair walk stopped on hitting $-a$ or $b$, the stopping time $N$ has finite mean (see the [optional stopping theorem](/optional-stopping-theorem/)). The second identity with $\sigma^2 = 1$ gives $\mathbb E[N] = \mathbb E[S_N^2] = a^2\frac{b}{a+b} + b^2\frac{a}{a+b} = ab$. For $a = 3$ and $b = 7$ this is 21.

## Tightness

**$N$ must not look ahead.** Let $N' = N - 1$ be the number of rolls before the first 6. Then $\mathbb E[N'] = 5$, and the naive product is $5 \cdot 3.5 = 17.5$, but the true expected sum of these rolls is $5 \cdot 3 = 15$. Here $\{N' \ge i\} = \{X_1 \ne 6, \ldots, X_i \ne 6\}$ depends on $X_i$, so Step 1 fails, and $N'$ is not a stopping time: to stop after roll $n$ one must know that roll $n + 1$ is a 6.

**$\mathbb E[N] < \infty$ is needed.** Let $X_i = \pm 1$ with probability $\frac12$ each, and let $N$ be the first $n$ with $S_n = 1$. Then $N < \infty$ almost surely and $\mu = 0$, but $S_N = 1$, so $\mathbb E[S_N] = 1 \ne 0 = \mu\,\mathbb E[N]$ under any convention. By the theorem, this forces $\mathbb E[N] = \infty$, which is the case. The nonnegative case shows that for $X_i \ge 0$ the hypothesis can be dropped.

**The average is not unbiased.** Wald's equation is about the sum, not about the mean of the sample. Let $X_i \in \{0, 1\}$ be fair coin flips, and stop after one flip if it is 1, else after two flips. Then $\mathbb E[N] = \frac32$ and $\mathbb E[S_N] = \frac34 = \frac12 \cdot \frac32$, as Wald's equation says. But $\mathbb E[S_N/N] = \frac12 \cdot 1 + \frac12 \cdot \frac14 = \frac58 \ne \frac12$. A stopping rule can bias the sample average even though it cannot bias the sum.

### Pitfalls

- **Independence of $N$ and the $X_i$ is not required.** The usual mistake goes the other way: a writer assumes that $N$ must be independent of the $X_i$, and does not use the equation where it applies, for example for the bits of rejection sampling where the cost and the decision to stop come from the same trial.
- **The variance is not $\sigma^2\,\mathbb E[N]$.** For $\mu \ne 0$, the second identity is about $S_N - N\mu$, not about $S_N$. If $N$ is independent of the $X_i$, then $\operatorname{Var}(S_N) = \sigma^2\,\mathbb E[N] + \mu^2 \operatorname{Var}(N)$, which is larger.
- **Each term needs the same mean.** If the cost of trial $i$ has a mean that changes with $i$, for example because the algorithm doubles a budget at each restart, the equation in this form does not apply. Use $\mathbb E[S_N] = \sum_i \mathbb E[X_i]\Pr(N \ge i)$, which the proof gives when each $X_i$ is independent of $\mathcal F_{i-1}$ and $\sum_i \mathbb E|X_i|\Pr(N \ge i) < \infty$.

## History

Wald published the identity in 1944, in a paper on cumulative sums of random variables written for his work on sequential analysis, where a test takes observations until a stopping rule ends it. Mitzenmacher and Upfal, Section 13.3, prove it as a corollary of the martingale stopping theorem and apply it to algorithms.

## References
