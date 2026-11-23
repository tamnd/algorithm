---
title: PATE with the Laplace noisy max is 2 gamma Q-DP
proves: [correctness]
status: full
---

The private data is a sequence $D = (e_1, \ldots, e_n)$ of labeled examples with labels in $\{0, \ldots, m - 1\}$. The neighbor relation is replace: $D'$ has a different example at one position $i$, and the same examples at all other positions. The public points $x_1, \ldots, x_Q$ are fixed before the run and do not depend on $D$. The training rule of a teacher is any deterministic function from a sequence of examples to a classifier. Line L1 puts example $i$ into part $i \bmod k$, and line L2 trains teacher $j$ on part $j$. For a point $x$, $n_c(x)$ is the number of teachers that predict the class $c$. Line L5 outputs $\arg\max_c (n_c(x) + Z_c)$, where $Z_0, \ldots, Z_{m-1}$ are independent $\mathrm{Lap}(1/\gamma)$ variables. Ties among the noisy counts have probability zero, since the $Z_c$ have densities.

**Lemma 1 (one teacher changes).** If $D$ and $D'$ differ at position $i$, then the parts of lines L1 differ only in part $i \bmod k$, and only teacher $i \bmod k$ can change.

*Proof.* The part of each position depends only on the position, not on the data. So every part $j \ne i \bmod k$ holds the same examples in the same order under $D$ and $D'$, and line L2 trains the same teacher on it. $\square$

**Lemma 2 (one vote moves).** For every $x$, the vote vectors $n(x)$ under $D$ and $n'(x)$ under $D'$ satisfy $n' = n$ or $n' = n - \mathbf e_a + \mathbf e_b$ for two classes $a \ne b$. In both cases $|n_c - n'_c| \le 1$ for every $c$.

*Proof.* By Lemma 1 one teacher can change its prediction at $x$, from $a$ to $b$. All other votes stay. $\square$

**Lemma 3 (the Laplace tail).** Let $S(t) = \Pr[Z > t]$ for $Z \sim \mathrm{Lap}(1/\gamma)$. For all $t$ and $s \ge 0$, $S(t + s) \ge e^{-\gamma s} S(t)$.

*Proof.* $S(t) = \tfrac12 e^{-\gamma t}$ for $t \ge 0$ and $S(t) = 1 - \tfrac12 e^{\gamma t}$ for $t < 0$. The function $g = -\ln S$ is differentiable. For $t > 0$, $g'(t) = \gamma$. For $t < 0$, $g'(t) = \gamma\,\tfrac12 e^{\gamma t}/(1 - \tfrac12 e^{\gamma t}) \le \gamma$, since $\tfrac12 e^{\gamma t} \le \tfrac12 \le 1 - \tfrac12 e^{\gamma t}$. So $g(t + s) - g(t) \le \gamma s$. $\square$

**Lemma 4 (one answer).** If $|n_c - n'_c| \le 1$ for all $c$, then for every class $c$,

$$\Pr[\text{L5 outputs } c \text{ on } n] \le e^{2\gamma}\Pr[\text{L5 outputs } c \text{ on } n'].$$

*Proof.* Fix $c$ and fix the values $z_j$ of the other noises $Z_j$, $j \ne c$. Let $M = \max_{j \ne c}(n_j + z_j)$ and $M' = \max_{j \ne c}(n'_j + z_j)$; then $|M - M'| \le 1$. Up to an event of probability zero, $c$ wins on $n$ exactly when $Z_c > t = M - n_c$, and on $n'$ exactly when $Z_c > t' = M' - n'_c$. Now $t' \le t + 2$, so by Lemma 3 and since $S$ is decreasing,

$$S(t') \ge S(t + 2) \ge e^{-2\gamma} S(t).$$

$Z_c$ is independent of the other noises, so taking the expectation over them gives $\Pr[c \text{ on } n'] \ge e^{-2\gamma}\Pr[c \text{ on } n]$. $\square$

**Theorem (privacy).** The labels of lines L3 to L5 for $Q$ public points are $2\gamma Q$-DP under replace, and so is the student of line L6.

*Proof.* Fix the data $D$ and the public points. The $Q$ answers use independent noise, so the probability of a label sequence $(c_1, \ldots, c_Q)$ is the product of the $Q$ answer probabilities. By Lemma 2 each vote vector moves by at most one vote between $D$ and $D'$, and Lemma 4 bounds each factor by $e^{2\gamma}$. So the probability of every label sequence changes by at most the factor $e^{2\gamma Q}$, and summing over the sequences in an event gives the claim. Line L6 is a function of the public points and the labels only, so the student is $2\gamma Q$-DP by the post-processing theorem. $\square$

**Tightness.** With $m = 2$, let the votes be $(0, v)$ under $D$ and $(1, v - 1)$ under $D'$. Class 0 wins when $Z_1 - Z_0 < n_0 - n_1$, and $\Pr[Z_1 - Z_0 < -t] = \tfrac12 e^{-\gamma t}(1 + \gamma t/2)$ for $t \ge 0$. The ratio of this at $t = v - 2$ and at $t = v$ tends to $e^{2\gamma}$ as $v$ grows. So the factor $2\gamma$ of Lemma 4 cannot be lowered in general.

**What is not proved here.** The bound $2\gamma Q$ is a worst case over all data sets. Papernot et al. use the moments accountant with a bound that depends on the vote counts, which is much smaller when the teachers agree. That bound is a function of the private data, so publishing its value is not covered by the theorem above. The proof does not say anything about the accuracy of the student. The code samples from floats, so it follows the analysis only up to floating-point effects. $\blacksquare$
