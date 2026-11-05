---
title: The MinHash estimate is unbiased and concentrated around the Jaccard similarity
proves: [correctness]
status: full
---

We use the names of the pseudocode on the page. Fix two finite sets $A, B \subseteq U$, not both empty, and write $C = A \cup B$ and $J = |A \cap B| / |C|$.

**Assumption (R).** The functions $h_1, \ldots, h_k$ are independent. Each $h_i$ is injective on $C$, and the order that $h_i$ induces on $C$ is uniform over the $|C|!$ orders. A uniformly random permutation of a finite universe $U$ has this property for every $C$.

**Lemma 1 (the signature).** For each $i$, MINHASH-SIGNATURE sets $\mathrm{sig}[i] = \min_{a \in A} h_i(a)$, with $\min \emptyset = \infty$.

*Proof.* Fix $i$. Line L2 sets $\mathrm{sig}[i] = \infty$. Invariant of the loop of line L3: after the elements $a_1, \ldots, a_j$ of $A$ have been seen, $\mathrm{sig}[i] = \min(\infty, h_i(a_1), \ldots, h_i(a_j))$. It holds for $j = 0$, and line L4 keeps it, since $\min(\min(X), y) = \min(X \cup \{y\})$. At the end $j = |A|$. The loop over $i$ does not change $\mathrm{sig}[i']$ for $i' \ne i$. $\square$

**Lemma 2 (one position).** Let $X_i = 1$ if $\mathrm{sig}_A[i] = \mathrm{sig}_B[i]$ and $X_i = 0$ otherwise. Under (R), $\Pr[X_i = 1] = J$.

*Proof.* If one of the sets is empty, say $B$, then $J = 0$, $\mathrm{sig}_B[i] = \infty$ and $\mathrm{sig}_A[i]$ is finite, so $X_i = 0$. Now let both be nonempty. Let $u \in C$ be the element with the least value $h_i(u)$; it is unique since $h_i$ is injective on $C$. Under (R), each element of $C$ is first in a uniform order with the same probability, so $\Pr[u = c] = 1/|C|$ for each $c \in C$.

- If $u \in A \cap B$, then $h_i(u) \le h_i(a)$ for each $a \in A \subseteq C$, so by Lemma 1, $\mathrm{sig}_A[i] = h_i(u)$, and in the same way $\mathrm{sig}_B[i] = h_i(u)$. So $X_i = 1$.
- If $u \in A \setminus B$, then $\mathrm{sig}_A[i] = h_i(u)$. Each $b \in B$ is in $C$ and differs from $u$, so $h_i(b) > h_i(u)$ by injectivity, and $\mathrm{sig}_B[i] > h_i(u)$. So $X_i = 0$. The case $u \in B \setminus A$ is the same.

So $X_i = 1$ exactly when $u \in A \cap B$, which has probability $|A \cap B| / |C| = J$. $\square$

**Theorem.** Let $\hat J$ be the value that ESTIMATE returns for the signatures of $A$ and $B$. Under (R),

1. $\mathbb{E}[\hat J] = J$;
2. $\operatorname{Var}[\hat J] = J(1 - J)/k \le 1/(4k)$;
3. for each $\varepsilon > 0$, $\Pr[|\hat J - J| \ge \varepsilon] \le 2 e^{-2k\varepsilon^2}$.

*Proof.* Lines L6 to L8 count the positions with equal entries, so line L9 returns $\hat J = \frac{1}{k} \sum_{i=1}^{k} X_i$. Each $X_i$ depends only on $h_i$, so the $X_i$ are independent, and by Lemma 2 each is a Bernoulli variable with mean $J$.

1. By [linearity of expectation](/linearity-of-expectation/), $\mathbb{E}[\hat J] = \frac1k \sum_i \mathbb{E}[X_i] = J$.
2. A Bernoulli variable with mean $J$ has variance $J(1 - J)$. The variance of a sum of independent variables is the sum of their variances, so $\operatorname{Var}[\hat J] = \frac{1}{k^2} \cdot k J(1 - J) = J(1-J)/k$. Since $J(1 - J) \le 1/4$ for $0 \le J \le 1$, the bound follows.
3. The Hoeffding inequality for $k$ independent variables with values in $[0, 1]$ gives $\Pr[\frac1k \sum_i X_i - J \ge \varepsilon] \le e^{-2k\varepsilon^2}$, and the same bound for the lower tail. A union bound over the two tails gives the claim. $\blacksquare$

**Corollary.** For $0 < \delta < 1$ and $k \ge \ln(2/\delta) / (2\varepsilon^2)$, $\Pr[|\hat J - J| \ge \varepsilon] \le \delta$, since then $2 e^{-2k\varepsilon^2} \le 2 e^{-\ln(2/\delta)} = \delta$.

**Termination and cost.** The loops of lines L1, L3 and L7 run over finite ranges, $k$, $|A|$ and $k$ times, so both procedures stop after $k|A|$ and $k$ steps of $O(1)$ time on the word RAM.
