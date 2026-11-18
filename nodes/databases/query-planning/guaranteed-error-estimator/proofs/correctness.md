---
title: GEE stays within a factor sqrt(n/r) above and 1 + sqrt(n/r) below the number of distinct values, and no sampling estimator can do better than order sqrt(n/r)
proves: [correctness]
status: full
---

**Setting.** A column has $n$ rows and $D$ distinct values. A value $v$ occurs in $m_v \ge 1$ rows, so $\sum_v m_v = n$. The sample $S$ is a set of $r$ rows, $1 \le r \le n$, drawn uniformly at random without replacement (line L1). For $j \ge 1$, $f_j$ is the number of values that occur exactly $j$ times in $S$ (lines L2 and L3), and $d = \sum_{j \ge 1} f_j$ is the number of distinct values in $S$. Write $c = \sqrt{n/r} \ge 1$. Line L4 returns

$$G = c f_1 + \sum_{j \ge 2} f_j = d + (c - 1) f_1 .$$

The ratio error of an estimate $x > 0$ is $\max(x/D, D/x)$.

**Lemma 1 (deterministic range).** For every sample, $d \le G \le c\,d \le c\,D$.

*Proof.* $G - d = (c - 1) f_1 \ge 0$ because $c \ge 1$. Also $f_1 \le d$, so $G \le d + (c - 1) d = c\,d$. Each value of the sample is a value of the column, so $d \le D$. $\square$

So $G$ never overestimates by more than the factor $c$, on any sample. If $r = n$, then $c = 1$, the sample is the whole column, and $G = d = D$.

**Lemma 2 (a missed value is rarer than a value seen once).** Let $v$ be a value with $m = m_v$ rows. Then $\Pr[v \notin S] \le \frac{n}{r} \Pr[v \text{ occurs exactly once in } S]$.

*Proof.* There are $\binom{n}{r}$ equally likely samples. The sample misses $v$ in $\binom{n-m}{r}$ of them, and contains exactly one row of $v$ in $m \binom{n-m}{r-1}$ of them. If $\binom{n-m}{r} = 0$, the left side is 0 and there is nothing to prove. Otherwise $n - m \ge r$, and

$$\frac{m \binom{n-m}{r-1}}{\binom{n-m}{r}} = \frac{m\,r}{n - m - r + 1} \ge \frac{m\,r}{n} \ge \frac{r}{n},$$

because $n - m - r + 1 \le n$ and $m \ge 1$. $\square$

**Lemma 3 (expected underestimate).** $E[G] \ge D / (1 + c)$.

*Proof.* The number of values that the sample misses is $D - d$. By linearity of expectation and Lemma 2, summed over all values,

$$E[D - d] = \sum_v \Pr[v \notin S] \le \frac{n}{r} \sum_v \Pr[v \text{ once in } S] = c^2 E[f_1].$$

So $D \le E[d] + c^2 E[f_1]$. Also $E[f_1] \le E[d]$, because $f_1 \le d$. Then

$$(1 + c) E[G] = (1 + c) E[d] + (c^2 - 1) E[f_1] = E[d] + c^2 E[f_1] + \big(c\,E[d] - E[f_1]\big) \ge E[d] + c^2 E[f_1] \ge D,$$

where the middle step uses $c\,E[d] \ge E[d] \ge E[f_1]$. $\square$

**Theorem (correctness of GEE).** For every column and every sample size $r$, $G \le \sqrt{n/r}\,D$ on every sample, and $E[G] \ge D / (1 + \sqrt{n/r})$. So $\max(E[G]/D,\ D/E[G]) \le 1 + \sqrt{n/r}$.

*Proof.* Lemma 1 gives $G \le c D$ for every sample, so $E[G]/D \le c$. Lemma 3 gives $D/E[G] \le 1 + c$. $\blacksquare$

**A single estimate can be worse.** The theorem bounds the expected estimate, not the ratio error of each run. Take $k = n/r$ (an integer) and a column with one value in $n - k$ rows and $k$ other values in one row each, so $D = k + 1$. The sample misses all $k$ singletons with probability $\binom{n-k}{r} / \binom{n}{r}$, which tends to $e^{-1}$ when $n/r$ is fixed and $r$ grows (it is above $1/3$ for $n = 400$ and $r = 20$). On those samples $f_1 = 0$, $d = 1$ and $G = 1$, so the ratio error is $k + 1 = n/r + 1 = c^2 + 1$. The test file checks this case.

**Theorem (lower bound for every estimator).** Let $1 \le r < n$ and $e^{-r} \le \gamma < 1$, and let $K = \frac{n - r}{2r} \ln \frac{1}{\gamma}$. Let $E$ be any estimator that reads the values of at most $r$ rows, chosen in any adaptive way and with any random choices, and then outputs $x > 0$. Then there is a column of $n$ rows on which $E$ has ratio error at least $\sqrt{K}$ with probability at least $\gamma / (1 + \gamma)$. If $E$ is deterministic, the probability is 1.

*Proof.* Let $k = \lfloor K \rfloor$. Because $\ln(1/\gamma) \le r$, $K \le (n - r)/2$, so $k \le n - r$. Column A has the same value 0 in all $n$ rows, so $D_A = 1$. A column of type B has the value 0 in $n - k$ rows and $k$ distinct other values in the other $k$ rows, so $D_B = k + 1$. Let $s = \sqrt{k + 1}$; then $s > \sqrt{K}$.

Run $E$ on column A with its random choices $\omega$. It reads only zeros, so the rows it reads are a set $P(\omega)$ of at most $r$ positions fixed by $\omega$, and it outputs $x(\omega)$. Its ratio error on A is $x(\omega)$ if $x(\omega) \ge 1$. Let $p = \Pr[x \ge s]$ on A.

Now put the $k$ singletons of B at a set $Q$ of $k$ positions chosen uniformly at random, independently of $\omega$. If $Q$ misses $P(\omega)$, then $E$ with choices $\omega$ reads the same zeros on B as on A, so it reads the same rows and outputs the same $x(\omega)$. For each fixed $\omega$, $Q$ misses the at most $r$ positions of $P(\omega)$ with probability at least

$$q = \frac{\binom{n-k}{r}}{\binom{n}{r}} = \prod_{i=0}^{r-1} \Big(1 - \frac{k}{n - i}\Big) \ge \Big(1 - \frac{k}{n - r + 1}\Big)^r .$$

Let $t = \ln(1/\gamma) / (2r)$. Then $k/(n - r + 1) \le K/(n - r) = t$, and $t \le 1/2$ because $\gamma \ge e^{-r}$. On $[0, 1/2]$, $1 - t \ge e^{-2t}$: the function $1 - t - e^{-2t}$ is 0 at $t = 0$, concave, and positive at $t = 1/2$. So $q \ge e^{-2tr} = \gamma$.

If $x(\omega) < s$ and $Q$ misses $P(\omega)$, the ratio error on B is at least $D_B / x(\omega) > (k + 1)/s = s$. So, over $\omega$ and $Q$, the probability of ratio error at least $s$ on B is at least $q (1 - p) \ge \gamma (1 - p)$. This is an average over the choice of $Q$, so some fixed placement $Q_0$ gives a column B with at least this probability. On A the probability is $p$. If $p \ge \gamma/(1+\gamma)$, column A is the bad input. Otherwise $\gamma (1 - p) > \gamma \cdot \frac{1}{1 + \gamma}$, and column B with $Q_0$ is the bad input.

If $E$ is deterministic, $\omega$ is fixed and $p$ is 0 or 1. If $p = 1$, column A has ratio error at least $s$ always. If $p = 0$, put the singletons at $k$ positions outside $P$, which exist because $k \le n - r$; then $E$ outputs $x < s$ on B always. $\blacksquare$

**Comparison with the paper.** Charikar et al. state the lower bound with probability at least $\gamma$ for each $\gamma > e^{-r}$. The proof above uses the same pair of inputs and gives $\gamma/(1+\gamma)$ for randomized estimators, which is enough for the order of the bound: with $\gamma$ a constant, every estimator has ratio error of order $\sqrt{n/r}$ with constant probability on some input. GEE matches this order in the sense of the first theorem: its expected estimate is within a factor $1 + \sqrt{n/r}$ of $D$.

**Work.** Line L1 draws $r$ rows. Lines L2 and L3 count the values with a hash table, in $O(r)$ expected time and $O(r)$ space. Line L4 sums over the at most $r$ entries of the profile.
