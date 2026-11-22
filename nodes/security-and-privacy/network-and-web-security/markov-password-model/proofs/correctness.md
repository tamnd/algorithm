---
title: The Markov password model is a distribution, and its guess numbers and Monte Carlo estimates are exact or unbiased
proves: [correctness, complexity]
status: full
---

We use the pseudocode MARKOV-SCORE of the page. The alphabet is $\Sigma$, the order is $k \ge 0$, and $\sigma = |\Sigma| + 1$ counts the characters and the end symbol $\dashv$. For a context $c$ (a string of $k$ symbols over $\Sigma$ and the start symbol) and a symbol $a \in \Sigma \cup \{\dashv\}$, the trained model has counts $N(c, a)$ and $N(c) = \sum_a N(c, a)$, and

$$ P(a \mid c) = \frac{N(c, a) + \delta}{N(c) + \delta\sigma}. $$

For a string $w = w_1 \cdots w_n$ let $w_{n+1} = \dashv$ and let $c_i$ be the last $k$ symbols of $\triangleright^k w_1 \cdots w_{i-1}$, where $\triangleright$ is the start symbol.

**Claim 1 (the score).** MARKOV-SCORE returns $-\log_2 P(w)$ with $P(w) = \prod_{i=1}^{n+1} P(w_i \mid c_i)$.

*Proof.* The loop of line L2 keeps the invariant: before the iteration for $i$, $c = c_i$ and $p = \prod_{j < i} P(w_j \mid c_j)$. Line L1 makes it true for $i = 1$, since $c_1 = \triangleright^k$ and the empty product is 1. Line L3 picks $w_i$, line L4 multiplies $p$ by $P(w_i \mid c_i)$, and line L5 sets $c$ to the last $k$ symbols of $c_i w_i$, which is $c_{i+1}$. After the iteration for $i = n + 1$, $p = P(w)$, and line L6 returns $-\log_2 p$. $\square$

**Claim 2 (a distribution).** For each context $c$, $\sum_a P(a \mid c) = 1$ when the denominator is positive. If $\delta > 0$, then $\sum_w P(w) = 1$ over all finite strings $w$ over $\Sigma$.

*Proof.* The first part is $\sum_a (N(c, a) + \delta) = N(c) + \delta\sigma$. For the second, let $Q(u) = \prod_{i=1}^{|u|} P(u_i \mid c_i)$ be the probability of the prefix $u$ without the end symbol, so $P(u) = Q(u) P(\dashv \mid c_{|u|+1})$ and $Q(u) = \sum_{a \in \Sigma \cup \{\dashv\}}$ of $Q(u) P(a \mid c_{|u|+1})$. We show by induction on $L$ that

$$ \sum_{|w| \le L} P(w) + \sum_{|u| = L + 1} Q(u) = 1. $$

For $L = -1$ the first sum is empty and the second is $Q(\varepsilon) = 1$. To go from $L - 1$ to $L$, split each $Q(u)$ with $|u| = L$ by its next symbol: the end symbol gives $P(u)$, a character $a$ gives $Q(ua)$. This is the identity that the test checks with exact fractions.

There are finitely many contexts, so $\varepsilon = \min_c P(\dashv \mid c) > 0$ when $\delta > 0$, since then $P(\dashv \mid c) \ge \delta / (N(c) + \delta\sigma)$. Each step that is not the end has probability at most $1 - \varepsilon$ in total, so $\sum_{|u| = L+1} Q(u) \le (1 - \varepsilon)^{L+1}$, which tends to 0. $\square$

With $\delta = 0$ and a context never seen in training, the denominator is 0 and the code gives probability 0. Then the mass can be less than 1, and a string with an unseen transition has strength $+\infty$.

**Claim 3 (maximum likelihood).** With $\delta = 0$, the values $P(a \mid c) = N(c, a) / N(c)$ maximize the likelihood of the training list among all order-$k$ models.

*Proof.* The log likelihood of the list is $\sum_c \sum_a N(c, a) \log P(a \mid c)$. The terms for different contexts are independent. For one context with $N(c) > 0$ and empirical distribution $\hat p(a) = N(c, a)/N(c)$, the term is $N(c) \sum_a \hat p(a) \log P(a \mid c)$, and by Gibbs' inequality this is largest exactly when $P(\cdot \mid c) = \hat p$. $\square$

**Claim 4 (guess numbers).** GUESS-NUMBER$(w, M)$ of the code returns $1 + |\{v : |v| \le M,\ P(v) > P(w)\}|$.

*Proof.* Each factor is at most 1, so for each prefix $u$ and each $v$ that extends it, $P(v) \le Q(u)$. The search starts at the empty prefix and skips the subtree of $u$ when $Q(u) \le P(w)$; no string in that subtree can have $P(v) > P(w)$. Each other prefix $u$ is visited once, counted when $P(u) = Q(u) P(\dashv \mid c) > P(w)$, and extended by each character while $|u| < M$. So each string of length at most $M$ with $P(v) > P(w)$ is counted once, and no other string is. $\square$

**Claim 5 (the Monte Carlo estimate).** Let $S_1, \ldots, S_m$ be independent draws from the model and $t$ a threshold. Then

$$ \hat G = \sum_{j=1}^{m} \frac{[P(S_j) > t]}{m\, P(S_j)} $$

has expectation $|\{v : P(v) > t\}|$.

*Proof.* By linearity, $\mathbb{E}[\hat G] = \mathbb{E}\big[[P(S) > t] / P(S)\big] = \sum_{v : P(v) > 0} P(v) [P(v) > t] / P(v) = |\{v : P(v) > t\}|$. This set is finite for $t > 0$, since $P(v) \le (1 - \varepsilon)^{|v|}$. When the draws are cut at length $M$, as in the code, the same computation gives the count of strings of length at most $M$. $\square$

The estimate of the guess number of $w$ is $1 + \hat G$ with $t = P(w)$. Its variance is not bounded by this argument, and the test only checks that it is near the exact count on one small model.

**Cost.** Line L4 does one lookup of a context of $k$ symbols in a hash table, so MARKOV-SCORE takes $\Theta(nk)$ time for $n = |w|$ on the word-RAM, or $\Theta(n)$ when $k$ is a constant, and $O(k)$ extra space. Training reads each of the $T$ symbols of the padded list once and does one lookup for each, so it takes $O(Tk)$ time, and the tables hold at most $T$ contexts of $k$ symbols. $\blacksquare$
