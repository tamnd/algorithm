---
title: A scalable Bloom filter has no false negatives and a bounded rate
proves: [correctness, invariant, termination]
status: full
---

Fix the sequence of operations. Each operation does a constant number of steps for each part of each slice it reads, so it ends. Write $l$ for the number of slices after the operations, and $K_i$ for the multiset of keys inserted into slice $i$.

**Lemma 1 (invariant (S)).** After each operation, every slice except the last has count $\kappa_i$, the last has count between 1 and $\kappa_{l-1}$, the count of slice $i$ is $|K_i|$, and $P_{i,j}[p] = 1$ exactly when some $y \in K_i$ has $h_{i,j}(y) = p$.

*Proof.* By induction over the operations. A QUERY changes nothing. Consider INSERT$(x)$. If there is no slice, or the last slice has count $\kappa_{l-1}$, line L4 appends slice $l$ with count 0 and all bits 0; the old last slice now has count exactly $\kappa_{l-1}$, as required for a slice that is not last. Note $\kappa_i \ge 1$, since $b_i \ge 2$ gives $(b_i - 1)\ln 2 \ge 0.69$, and the code takes $\kappa_i = 1$ in the case $b_i = 2$. Now the last slice has count below its capacity. Lines L5 and L6 add $x$ to $K_{l-1}$, set exactly the bits $P_{l-1,j}[h_{l-1,j}(x)]$, and add 1 to the count, which then is between 1 and $\kappa_{l-1}$. No other slice and no other bit changes, and no bit is set to 0. $\square$

**Theorem 1 (no false negatives).** If $x$ was inserted, QUERY$(x)$ returns true.

*Proof.* Let $i$ be a slice with $x \in K_i$. By Lemma 1, $P_{i,j}[h_{i,j}(x)] = 1$ for each $j \le k_i$, so line L8 returns true when the loop reaches slice $i$, unless it returned true before. $\square$

**Model.** For Theorem 2 assume ideal hashing: the values $h_{i,j}(y)$ for all slices $i$, parts $j$ and keys $y$ are independent, and $h_{i,j}(y)$ is uniform on $\{0, \ldots, b_i - 1\}$. Fix the sequence of inserted keys. Since INSERT does not read any hash value to decide where a key goes, the multisets $K_i$ do not depend on the hash values. Let $x$ be a key that is not inserted.

**Lemma 2.** If $c \le (b - 1)\ln 2$ and $b \ge 2$, then $(1 - 1/b)^c \ge 1/2$.

*Proof.* For $t = 1/(b - 1) \in (0, 1]$ we have $1 - 1/b = 1/(1 + t) \ge e^{-t}$, since $e^t \ge 1 + t$. So $(1 - 1/b)^c \ge e^{-c/(b - 1)} \ge e^{-\ln 2} = 1/2$. $\square$

**Theorem 2 (rate).** Slice $i$ accepts $x$ with probability at most $2^{-k_i} \le \varepsilon_0 r^i$, and QUERY$(x)$ returns true with probability at most $\sum_{i < l} \varepsilon_0 r^i < \varepsilon_0/(1 - r)$.

*Proof.* Fix $i$ and let $D$ be the set of distinct keys of $K_i$, so $|D| \le \kappa_i$ by Lemma 1. For part $j$ let $X_j$ be the number of 1 bits of $P_{i,j}$. By Lemma 1, $X_j$ is a function of the values $h_{i,j}(y)$ for $y \in D$ only. So $X_1, \ldots, X_{k_i}$ are independent, and they are independent of the values $h_{i,j}(x)$, since $x \notin D$. Given the $X_j$, slice $i$ accepts $x$ with probability $\prod_j X_j/b_i$. Hence
$$ \Pr[\text{slice } i \text{ accepts } x] = \mathbb{E}\Big[\prod_j \frac{X_j}{b_i}\Big] = \prod_j \frac{\mathbb{E}[X_j]}{b_i}. $$
Each bit of $P_{i,j}$ is 0 with probability $(1 - 1/b_i)^{|D|} \ge (1 - 1/b_i)^{\kappa_i} \ge 1/2$ by Lemma 2, since $\kappa_i \le (b_i - 1)\ln 2$ when $b_i \ge 3$, and for $b_i = 2$ the capacity 1 gives the fraction $1/2$ directly. So $\mathbb{E}[X_j]/b_i \le 1/2$, and the product is at most $2^{-k_i}$. By the choice $k_i = \lceil \log_2(1/(\varepsilon_0 r^i)) \rceil$, $2^{-k_i} \le \varepsilon_0 r^i$.

QUERY$(x)$ returns true only if some slice accepts $x$. The union bound over the $l$ slices and the sum of the geometric series give
$$ \Pr[\text{QUERY}(x) = \text{true}] \le \sum_{i=0}^{l-1} \varepsilon_0 r^i = \varepsilon_0 \frac{1 - r^l}{1 - r} < \frac{\varepsilon_0}{1 - r}. \quad \blacksquare $$
