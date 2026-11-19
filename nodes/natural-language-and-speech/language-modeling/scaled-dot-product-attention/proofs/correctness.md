---
title: Scaled dot-product attention returns the masked row softmax times V, its output rows are convex combinations of the visible values, it is permutation equivariant, and unit-variance inputs give scores of variance d_k before scaling
proves: [correctness]
status: full
---

We use the notation of the page. $Q$ is $n \times d_k$, $K$ is $m \times d_k$, $V$ is $m \times d_v$ and $M$ is an $n \times m$ mask. Write $J_i = \{ j : M_{ij} \}$ for the keys that query $i$ sees, and assume $J_i \ne \emptyset$ for every $i$. The target is

$$O_i = \sum_{j \in J_i} \pi_{ij} V_j, \qquad \pi_{ij} = \frac{\exp(a_{ij})}{\sum_{j' \in J_i} \exp(a_{ij'})}, \qquad a_{ij} = \frac{Q_i \cdot K_j}{\sqrt{d_k}},$$

with $\pi_{ij} = 0$ for $j \notin J_i$. We work in the real RAM with $e^{-\infty} = 0$.

**Lemma 1 (the scores).** After the loop of lines L2 to L4 for query $i$, $s_j = a_{ij}$ for $j \in J_i$ and $s_j = -\infty$ for $j \notin J_i$.

*Proof.* Line L3 sets $s_j = a_{ij}$ for every $j$, and line L4 replaces it by $-\infty$ exactly when $M_{ij}$ is false. $\square$

**Lemma 2 (the softmax).** After line L7, $p_j = \pi_{ij}$ for every $j$.

*Proof.* Since $J_i$ is not empty, Lemma 1 gives $\mu = \max_{j \in J_i} a_{ij}$, a finite number. Line L6 sets $p_j = e^{a_{ij} - \mu}$ for $j \in J_i$ and $p_j = e^{-\infty} = 0$ otherwise. Every $a_{ij} - \mu \le 0$, and it equals 0 for some $j$, so $1 \le Z \le |J_i|$; in particular $Z > 0$ and the division at line L7 is defined. For $j \in J_i$,

$$\frac{p_j}{Z} = \frac{e^{a_{ij}} e^{-\mu}}{e^{-\mu} \sum_{j' \in J_i} e^{a_{ij'}}} = \pi_{ij},$$

and for $j \notin J_i$ the value is $0 = \pi_{ij}$. $\square$

**Theorem 3 (correctness).** ATTENTION returns $O$.

*Proof.* The iterations of line L1 do not share state, so it suffices to look at one $i$. By Lemma 2, line L8 sets $O_i = \sum_j \pi_{ij} V_j = \sum_{j \in J_i} \pi_{ij} V_j$, the target row. Line L9 returns all $n$ rows. The loops are finite, so the algorithm stops. $\square$

**Corollary 4 (convex output).** Each $O_i$ is a convex combination of $\{ V_j : j \in J_i \}$, so each coordinate $O_{ic}$ lies between the smallest and largest $V_{jc}$ over $j \in J_i$.

*Proof.* By Lemma 2 the weights $\pi_{ij}$ are non-negative, zero outside $J_i$, and $\sum_j \pi_{ij} = \sum_j p_j / Z = 1$. $\square$

**Theorem 5 (permutation equivariance).** Take no mask. Let $\sigma$ be a permutation of $\{1, \ldots, n\}$ and $\tau$ one of $\{1, \ldots, m\}$, and let $Q'_i = Q_{\sigma(i)}$, $K'_j = K_{\tau(j)}$ and $V'_j = V_{\tau(j)}$. Then the output $O'$ on $(Q', K', V')$ satisfies $O'_i = O_{\sigma(i)}$.

*Proof.* The score of query $i$ and key $j$ on the new input is $a'_{ij} = Q_{\sigma(i)} \cdot K_{\tau(j)} / \sqrt{d_k} = a_{\sigma(i) \tau(j)}$. The denominator $\sum_{j} e^{a'_{ij}} = \sum_j e^{a_{\sigma(i) \tau(j)}}$ is a sum over all keys in another order, so it equals the denominator of row $\sigma(i)$. Hence $\pi'_{ij} = \pi_{\sigma(i) \tau(j)}$ and

$$O'_i = \sum_j \pi_{\sigma(i) \tau(j)} V_{\tau(j)} = \sum_{j'} \pi_{\sigma(i) j'} V_{j'} = O_{\sigma(i)},$$

by the change of index $j' = \tau(j)$. $\square$

With a causal mask Theorem 5 does not hold for general $\sigma$, because the mask is tied to the positions. Instead, by Lemma 1 the row of query $i$ depends only on $K_j$ and $V_j$ with $j \le i + (m - n)$, so changing later keys or values does not change it.

**Lemma 6 (the variance of a dot product).** Let $q_1, \ldots, q_{d}, k_1, \ldots, k_{d}$ be independent random variables with mean 0 and variance 1. Then $q \cdot k$ has mean 0 and variance $d$, and $q \cdot k / \sqrt{d}$ has variance 1.

*Proof.* For each $t$, $q_t$ and $k_t$ are independent, so $\mathbb{E}[q_t k_t] = \mathbb{E}[q_t]\, \mathbb{E}[k_t] = 0$ and $\mathbb{E}[(q_t k_t)^2] = \mathbb{E}[q_t^2]\, \mathbb{E}[k_t^2] = 1$. So $\operatorname{Var}(q_t k_t) = 1$. For $t \ne u$ the products $q_t k_t$ and $q_u k_u$ are functions of disjoint sets of independent variables, so they are independent and their covariance is 0. The variance of the sum is the sum of the variances, $d$, and its mean is 0. Dividing by $\sqrt{d}$ divides the variance by $d$. $\blacksquare$

Lemma 6 is about the inputs at the start of training. It does not say that the scores of a trained network have variance 1; the factor $1/\sqrt{d_k}$ is a choice made so that the softmax starts in a region where its gradient is not small.
