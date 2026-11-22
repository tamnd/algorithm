---
title: Interval bound propagation gives sound bounds, and a certificate rules out every label change in the box
proves: [correctness]
status: full
---

A network is a list of affine layers $(W_1, b_1), \dots, (W_K, b_K)$, with a ReLU after every layer except the last. We write $f(v)$ for the output of layer $K$ at the input $v$, and we compare vectors coordinate by coordinate. Arithmetic is exact.

**Lemma 1 (an affine layer).** Let $\mu, r$ be vectors with $r \ge 0$, and let $v$ satisfy $|v_t - \mu_t| \le r_t$ for every $t$. Then for every row $i$,
$$(W\mu + b)_i - (|W| r)_i \le (Wv + b)_i \le (W\mu + b)_i + (|W| r)_i.$$
Both ends are reached: the upper one at $v_t = \mu_t + \operatorname{sign}(W_{it}) r_t$, the lower one at $v_t = \mu_t - \operatorname{sign}(W_{it}) r_t$.

*Proof.* $(Wv + b)_i - (W\mu + b)_i = \sum_t W_{it}(v_t - \mu_t)$. By the triangle inequality, $|\sum_t W_{it}(v_t - \mu_t)| \le \sum_t |W_{it}|\,|v_t - \mu_t| \le \sum_t |W_{it}| r_t$. At the given points every term $W_{it}(v_t - \mu_t)$ equals $\pm |W_{it}| r_t$ with the same sign for all $t$, so the bound is an equality. $\square$

**Lemma 2 (a ReLU).** If $l \le a \le u$, then $\max(l, 0) \le \max(a, 0) \le \max(u, 0)$, and both ends are reached on $[l, u]$.

*Proof.* The function $t \mapsto \max(t, 0)$ is nondecreasing, which gives the inequalities. It is continuous, so by the intermediate value theorem it takes every value between $\max(l, 0)$ and $\max(u, 0)$ on $[l, u]$; in particular it takes the two ends, at $t = l$ and $t = u$. $\square$

**Theorem 1 (soundness of IBP).** Let $l \le u$ be the input box of line L1, and let $(l^{(k)}, u^{(k)})$ be the box after layer $k$ in the loop of lines L2 to L8. For every input $v$ with $l \le v \le u$, the activation $a^{(k)}(v)$ of layer $k$ (after its ReLU when $k < K$) satisfies $l^{(k)} \le a^{(k)}(v) \le u^{(k)}$. In particular the pair $(l', u')$ of line L9 bounds $f(v)$.

*Proof.* By induction on $k$. For $k = 0$ the claim is the hypothesis $l \le v \le u$. Assume the claim for $k - 1$. Line L3 sets $\mu = (u^{(k-1)} + l^{(k-1)})/2$ and $r = (u^{(k-1)} - l^{(k-1)})/2 \ge 0$, so $l^{(k-1)} \le a \le u^{(k-1)}$ is the same as $|a_t - \mu_t| \le r_t$ for every $t$. By Lemma 1, the pre-activation $W_k a + b_k$ lies between the vectors of line L6. If $k < K$, Lemma 2 applied to each coordinate shows that the activation lies between the vectors of line L8. If $k = K$, there is no ReLU and the claim is the bound of line L6. Each box keeps $l^{(k)} \le u^{(k)}$, because $r \ge 0$ and the ReLU is nondecreasing, so the induction can go on. $\square$

**Theorem 2 (the certificate).** Let $x \in [0,1]^d$, $\epsilon \ge 0$ and $y$ be a label. If CERTIFY-IBP returns true, then for every $x' \in S = B_\infty(x, \epsilon) \cap [0,1]^d$ and every $j \ne y$, $z_y(x') > z_j(x')$, so $y$ is the only argmax of $z(x')$.

*Proof.* Line L10 gives $l_i = \max(x_i - \epsilon, 0)$ and $u_i = \min(x_i + \epsilon, 1)$. A point $x'$ is in $S$ if and only if $l \le x' \le u$, since the two interval conditions on each coordinate intersect to $[l_i, u_i]$. Line L11 changes only the last layer: its output number $j$ is now $(W_K[y] - W_K[j]) a + b_K[y] - b_K[j] = z_y - z_j$, where $a$ is the last hidden activation. The hidden layers are the same, so this new network computes the vector of margins. By Theorem 1, every $x' \in S$ has $z_y(x') - z_j(x') \ge l'_j$. Line L13 returns true only when every $l'_j > 0$, so every margin is positive on $S$. $\square$

**Theorem 3 (one layer is tight).** If $K = 1$, each bound of line L9 is reached at a corner of the input box, so the output box is the smallest box that contains the image of the input box.

*Proof.* With $K = 1$ the loop runs once with no ReLU. Line L3 gives the center and radius of the input box, and Lemma 1 shows that the end $l'_i$ is reached at the corner $v_t = \mu_t - \operatorname{sign}(W_{it}) r_t$ and the end $u'_i$ at $v_t = \mu_t + \operatorname{sign}(W_{it}) r_t$; both corners are in the box. So no smaller interval contains all the values of output $i$, for each $i$. With hidden layers this fails in general, because Lemma 1 treats the coordinates of the activation as independent, while they all depend on the same input; the worked example on the page has the bound $-1.25$ against the true minimum $1$. $\blacksquare$
