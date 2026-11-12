---
title: Ancestral sampling draws from the joint, and rejection draws from the posterior
proves: [correctness]
status: full
---

Let the network have the variables $X_1, \ldots, X_m$, numbered in the topological order $\pi$ of line L1. So each parent of $X_i$ has an index less than $i$. Write $f_i(x) = P(x_i \mid x_{\mathrm{Pa}(i)})$ for the table entry of $X_i$. Each row of a table is a probability distribution: $\sum_{x_i} f_i(x) = 1$ for each fixed value of the parents. The joint is $P(x) = \prod_{i=1}^{m} f_i(x)$.

**Lemma 1 (the draw).** If $u$ is uniform on $[0, 1)$ and $(p_0, \ldots, p_{c-1})$ is a row, the draw returns $x$ with probability $p_x$.

*Proof.* Let $S_x = p_0 + \cdots + p_x$ and $S_{-1} = 0$. The draw returns $x$ exactly when $S_{x-1} \le u < S_x$. This interval has length $p_x$, and $u$ is uniform, so the probability is $p_x$. Since $S_{c-1} = 1$, each $u \in [0, 1)$ gives a value. $\square$

**Lemma 2 (prefix marginals).** For each $j$ with $0 \le j \le m$ and each $(x_1, \ldots, x_j)$,
$$P(x_1, \ldots, x_j) = \prod_{i=1}^{j} f_i(x).$$
The right side depends only on $x_1, \ldots, x_j$, because the parents of $X_i$ have smaller indices.

*Proof.* By downward induction on $j$. For $j = m$ the statement is the definition of the joint. Assume it for $j \ge 1$. Then
$$P(x_1, \ldots, x_{j-1}) = \sum_{x_j} P(x_1, \ldots, x_j) = \prod_{i=1}^{j-1} f_i(x) \cdot \sum_{x_j} f_j(x).$$
The factor $f_i$ for $i < j$ does not depend on $x_j$: $x_j$ is not $x_i$, and $X_j$ is not a parent of $X_i$ because $j > i$. So these factors move out of the sum. The last sum is the sum of one row of the table of $X_j$, which is 1. $\square$

**Theorem 1.** ANCESTRAL-SAMPLE returns $x$ with probability $P(x)$, for each assignment $x$.

*Proof.* We show by induction on $j$ that after $j$ passes of the loop of line L2, the drawn values $(x_1, \ldots, x_j)$ have the probability $\prod_{i \le j} f_i(x)$. For $j = 0$ the product is empty and equals 1. In pass $j$, line L3 reads the parent values of $X_j$; they are drawn, since they have smaller indices. Line L4 draws $x_j$ from the row $f_j(\cdot)$ for these values, with a fresh uniform number. By Lemma 1 the conditional probability of $x_j$ given the earlier draws is $f_j(x)$. The probability of the prefix of length $j$ is then the probability of the prefix of length $j - 1$ times $f_j(x)$, which is the claim. For $j = m$ the probability is $\prod_{i=1}^{m} f_i(x) = P(x)$. Lemma 2 shows that every prefix also has the right marginal. $\square$

**Theorem 2.** In REJECTION-QUERY, the number $K$ of kept samples is Binomial$(s, P(e))$. Given $K = k \ge 1$, the kept samples are i.i.d. with the distribution $P(x \mid e)$, so each returned frequency is an unbiased estimate of $P(Q = q \mid e)$ given $K = k$, with variance $P(q \mid e)(1 - P(q \mid e)) / k$.

*Proof.* The $s$ calls of line L8 use disjoint uniform numbers, so by Theorem 1 their outputs are i.i.d. with the distribution $P$. Line L9 keeps a sample $x$ when $x$ agrees with $e$. This has probability $\sum_{x \text{ agrees with } e} P(x) = P(e)$ for each call, independently, so $K$ is Binomial$(s, P(e))$. For a kept sample,
$$\Pr[x \mid \text{kept}] = \frac{P(x)\,[x \text{ agrees with } e]}{P(e)} = P(x \mid e).$$
Given the set of kept indices, the kept samples are independent, since the calls are. The count of $Q = q$ among $k$ such samples is Binomial$(k, P(q \mid e))$, which gives the mean and the variance. $\square$

**Relation to general rejection sampling.** Take the target $g(x) = P(x \mid e)$ and the proposal $P(x)$. Then $g(x) \le P(x) / P(e)$, so the envelope constant is $M = 1 / P(e)$, and the acceptance probability $g(x) / (M P(x)) = [x \text{ agrees with } e]$ is 0 or 1. The expected number of proposals per accepted sample is $M = 1 / P(e)$.
