---
title: Good-Turing estimation gives a proper distribution, and the Turing formula is unbiased for the mass of each count class
proves: [correctness]
status: full
---

We write $c(x) \ge 1$ for the count of a seen type $x$, $N = \sum_x c(x) \ge 1$, and $N_r$ for the number of seen types $x$ with $c(x) = r$.

**Theorem 1 (a proper distribution).** The output of GOOD-TURING satisfies $p(x) \ge 0$ for every seen type, $0 \le P_0 \le 1$, and $P_0 + \sum_x p(x) = 1$. If $P_0 < 1$, then $p(x) > 0$ for every seen type.

*Proof.* Line L2 gives $0 \le P_0 = N_1 / N \le 1$, since $N_1 \le N$. For each $r$ with $N_r > 0$, line L4 sets $r^* = (r+1) N_{r+1} / N_r$ only when $N_{r+1} > 0$, so $r^* > 0$, and line L5 sets $r^* = r \ge 1$. So every $r^*$ is positive. There is at least one seen type, so $S = \sum_r N_r r^* > 0$ in line L6, and line L7 is defined. Then $p(x) = (1 - P_0) r^*_{c(x)} / S \ge 0$, with $p(x) > 0$ when $P_0 < 1$. Group the seen types by their count:

$$\sum_x p(x) = \frac{1 - P_0}{S} \sum_r N_r r^* = 1 - P_0. \qquad \square$$

**Lemma 2 (the mass of the formula alone).** Let $\tilde r = (r+1) N_{r+1} / N_r$ for every $r$ with $N_r > 0$, and $\tilde p(x) = \tilde r_{c(x)} / N$. Then

$$\sum_x \tilde p(x) = \frac{1}{N} \sum_{s \ge 2,\; N_{s-1} > 0} s N_s .$$

So $N_1 / N + \sum_x \tilde p(x) = 1$ if and only if $N_{s-1} > 0$ for every $s \ge 2$ with $N_s > 0$.

*Proof.* $\sum_x \tilde p(x) = \frac1N \sum_{r:\, N_r > 0} N_r \tilde r = \frac1N \sum_{r:\, N_r > 0} (r+1) N_{r+1}$. Put $s = r + 1$. The sum runs over the $s \ge 2$ with $N_{s-1} > 0$, and the terms with $N_s = 0$ are zero. Since $N = N_1 + \sum_{s \ge 2} s N_s$, the total with $N_1 / N$ is 1 exactly when no term $s N_s > 0$ is left out. $\square$

This is why line L5 keeps $r^* = r$ and line L7 scales: the formula alone loses the mass of every count $s$ with $N_{s-1} = 0$, and it always gives $\tilde r = 0$ to the largest count.

**Theorem 3 (Good's identity).** Let $X_1, \ldots, X_N$ be independent draws from a distribution $q$ on a countable set of types. Let $N_r^{(M)}$ be the number of types seen exactly $r$ times in the first $M$ draws, and let

$$M_r = \sum_x q_x \,[\, x \text{ is seen exactly } r \text{ times in } X_1, \ldots, X_N \,]$$

be the total probability of the types seen $r$ times. Then for every $r \ge 0$,

$$\mathbb{E}[M_r] = \frac{r+1}{N+1}\, \mathbb{E}\bigl[N_{r+1}^{(N+1)}\bigr].$$

*Proof.* The count of type $x$ in $N$ draws has the binomial distribution with parameters $N$ and $q_x$. By linearity of expectation, and since all terms are nonnegative so that the sums may be reordered,

$$\mathbb{E}[M_r] = \sum_x q_x \binom{N}{r} q_x^{r} (1 - q_x)^{N-r} = \binom{N}{r} \sum_x q_x^{r+1} (1 - q_x)^{N-r}.$$

In the same way, the count of $x$ in $N + 1$ draws is binomial with parameters $N + 1$ and $q_x$, so

$$\mathbb{E}\bigl[N_{r+1}^{(N+1)}\bigr] = \binom{N+1}{r+1} \sum_x q_x^{r+1} (1 - q_x)^{N-r}.$$

The two sums are the same. The identity follows from

$$\binom{N}{r} = \frac{N!}{r!\,(N-r)!} = \frac{r+1}{N+1} \cdot \frac{(N+1)!}{(r+1)!\,(N-r)!} = \frac{r+1}{N+1} \binom{N+1}{r+1}. \qquad \blacksquare$$

**What the identity gives.** For $r = 0$, the unseen mass has $\mathbb{E}[M_0] = \mathbb{E}[N_1^{(N+1)}] / (N + 1)$. The observed $N_1 / N$ estimates it, and its bias is small. From the binomial sums above,

$$\frac{\mathbb{E}[N_1^{(N)}]}{N} - \mathbb{E}[M_0] = \sum_x q_x (1 - q_x)^{N-1} - \sum_x q_x (1 - q_x)^{N} = \sum_x q_x^2 (1 - q_x)^{N-1} = \frac{\mathbb{E}[M_1]}{N},$$

which lies in $[0, 1/N]$ because $0 \le M_1 \le 1$. For $r \ge 1$, replace $\mathbb{E}[N_{r+1}^{(N+1)}] / (N+1)$ by the observed $N_{r+1} / N$ and share $M_r$ equally among the $N_r$ types seen $r$ times. Each gets $(r+1) N_{r+1} / (N N_r) = r^* / N$, which is the estimate of line L4 before the scaling of line L7. The identity holds for every $q$, so the estimator makes no assumption on the shape of the distribution, only on the independence of the draws.
