---
title: The expected CD-k update converges to the log likelihood gradient as k grows
proves: [correctness]
status: full
---

We use the pseudocode of the page. The RBM has visible units $v \in \{0,1\}^m$, hidden units $h \in \{0,1\}^n$, energy $E(v, h) = -a^\top v - b^\top h - v^\top W h$ and $p(v, h) = e^{-E(v, h)} / Z$. Write $\sigma(x) = 1/(1 + e^{-x})$ and $q(v) = \sigma(b + W^\top v) \in (0,1)^n$, with $\sigma$ applied to each entry. The data set is $D$, with empirical distribution $p_D$, and $\ell(\theta) = \frac{1}{|D|} \sum_{v \in D} \log p(v)$.

What is proved here: the line by line meaning of the algorithm (Lemmas 1 and 3), the exact gradient (Lemma 2), and that the expected update tends to the gradient geometrically in $k$ (Theorem). What is not claimed: that CD-k with a fixed $k$ follows the gradient of $\ell$ or of any other function. It does not in general, as the remark at the end says.

**Lemma 1 (factorized conditionals).** $p(h \mid v) = \prod_j p(h_j \mid v)$ with $p(h_j = 1 \mid v) = \sigma(b_j + \sum_i v_i W_{ij})$, and $p(v \mid h) = \prod_i p(v_i \mid h)$ with $p(v_i = 1 \mid h) = \sigma(a_i + \sum_j W_{ij} h_j)$.

*Proof.* For fixed $v$, $-E(v, h) = a^\top v + \sum_j h_j (b_j + \sum_i v_i W_{ij})$ is a sum of terms that each depend on one $h_j$. So $p(h \mid v) \propto \prod_j e^{h_j c_j}$ with $c_j = b_j + \sum_i v_i W_{ij}$, a product of independent Bernoulli laws with $p(h_j = 1 \mid v) = e^{c_j} / (1 + e^{c_j}) = \sigma(c_j)$. The visible side is the same with the roles of $v$ and $h$ exchanged. $\square$

So line L3 computes $q(v^0) = \mathbb{E}[h \mid v^0]$ exactly, and lines L4, L6 and L7 sample from or evaluate the exact conditionals.

**Lemma 2 (the gradient).** Let $s(v) = (v\, q(v)^\top,\ v,\ q(v))$, the statistics for $(W, a, b)$. Then

$$\nabla_\theta \ell = \mathbb{E}_{v \sim p_D}[s(v)] - \mathbb{E}_{v \sim p}[s(v)],$$

where $p$ is the marginal of the model on $v$.

*Proof.* Summing out $h$ with Lemma 1 gives $p(v) = e^{-F(v)} / Z$ with the free energy $F(v) = -a^\top v - \sum_j \log(1 + e^{c_j(v)})$. Differentiate: $\partial(-F) / \partial W_{ij} = v_i \sigma(c_j(v)) = v_i q_j(v)$, $\partial(-F)/\partial a_i = v_i$ and $\partial(-F)/\partial b_j = q_j(v)$; that is, $\nabla_\theta(-F(v)) = s(v)$. Also $Z = \sum_v e^{-F(v)}$, so $\nabla_\theta \log Z = \sum_v \frac{e^{-F(v)}}{Z} \nabla_\theta(-F(v)) = \mathbb{E}_p[s(v)]$. Then $\nabla_\theta \log p(v) = s(v) - \mathbb{E}_p[s]$, and averaging over $D$ gives the claim. $\square$

**Lemma 3 (the law of the chain).** Let $T(v, v') = \sum_h p(h \mid v)\, p(v' \mid h)$. In lines L4 to L8, after iteration $t$ of the loop, the vector $v$ has the law $T^t(v^0, \cdot)$, and $q$ in line L7 equals $q(v)$. Hence the expected update of lines L9 and L10, divided by $|V|$, is

$$G_k = \mathbb{E}_{v^0 \sim p_D}[s(v^0)] - \mathbb{E}_{v^0 \sim p_D}\, \mathbb{E}_{v \sim T^k(v^0, \cdot)}[s(v)]$$

when $V = D$, and its expectation over a uniformly drawn minibatch when $V \subset D$.

*Proof.* By induction on $t$. Before the loop, $h$ is drawn from $p(h \mid v^0)$ (line L4). In iteration $t$, line L6 draws $v$ from $p(\cdot \mid h)$, and line L8 draws the next $h$ from $p(\cdot \mid v)$ by Lemma 1. So each pass through lines L6 and L8 moves $v$ by one step of $T$, and after iteration $t$, $v \sim T^t(v^0, \cdot)$. Line L7 computes $q(v)$ by Lemma 1. The positive term $s(v^0)$ is deterministic given $v^0$. Taking expectations of lines L9 and L10 gives $G_k$. $\square$

Using $q(v)$ in the negative term in place of a sampled $h$ does not change the expectation, since $\mathbb{E}[v_i h_j \mid v] = v_i q_j(v)$; it only lowers the variance.

**Lemma 4 (the chain).** $T$ is a stochastic matrix on $\{0,1\}^m$ with all entries positive, and the model marginal $p$ is stationary: $\sum_v p(v) T(v, v') = p(v')$.

*Proof.* Every conditional probability in Lemma 1 is a product of values of $\sigma$, which lie in $(0, 1)$, so $T(v, v') > 0$, and $\sum_{v'} T(v, v') = \sum_h p(h \mid v) = 1$. For stationarity, $\sum_v p(v) p(h \mid v) = p(h)$, so $\sum_v p(v) T(v, v') = \sum_h p(h) p(v' \mid h) = \sum_h p(v', h) = p(v')$. $\square$

**Theorem.** Let $c_0 = \min_{v, v'} T(v, v') > 0$ and $c = 2^m c_0 \in (0, 1]$. Then every coordinate of the bias satisfies

$$\big| (G_k)_r - (\nabla_\theta \ell)_r \big| \le (1 - c)^k .$$

In particular $G_k \to \nabla_\theta \ell$ as $k \to \infty$.

*Proof.* Let $U$ be the matrix whose rows are all the uniform distribution on the $2^m$ states. Since $T(v, v') \ge c_0 = c\, U(v, v')$, we can write $T = c\, U + (1 - c) R$ with $R$ stochastic (if $c = 1$, $T = U$ and the claim is trivial). For two distributions $\mu$ and $\nu$, $\mu U = \nu U$, so $\mu T - \nu T = (1 - c)(\mu - \nu) R$ and

$$\lVert \mu T - \nu T \rVert_{TV} \le (1 - c) \lVert \mu - \nu \rVert_{TV},$$

because a stochastic matrix does not increase the total variation distance $\lVert \mu - \nu \rVert_{TV} = \frac12 \sum_v |\mu(v) - \nu(v)|$. Take $\mu = \delta_{v^0}$ and $\nu = p$, which is stationary by Lemma 4. By induction, $\lVert T^k(v^0, \cdot) - p \rVert_{TV} \le (1 - c)^k \lVert \delta_{v^0} - p \rVert_{TV} \le (1 - c)^k$.

Each coordinate $f = s_r$ of the statistics takes values in $[0, 1]$, since $v_i \in \{0, 1\}$ and $q_j \in (0, 1)$. For such $f$ and distributions $\mu, \nu$, $|\mathbb{E}_\mu f - \mathbb{E}_\nu f| = |\sum_v (\mu(v) - \nu(v))(f(v) - \tfrac12)| \le \tfrac12 \sum_v |\mu(v) - \nu(v)| = \lVert \mu - \nu \rVert_{TV}$. By Lemmas 2 and 3,

$$(G_k)_r - (\nabla_\theta \ell)_r = \mathbb{E}_{v^0 \sim p_D}\big[ \mathbb{E}_p[s_r] - \mathbb{E}_{T^k(v^0, \cdot)}[s_r] \big],$$

and each inner difference is at most $(1 - c)^k$ in absolute value. $\square$

**Remark (what fails for finite k).** The bound is useless in practice for large $m$: $c$ can be tiny when the weights are large, and the chain mixes slowly. For fixed $k$, $G_k$ is a biased estimate, and the field $\theta \mapsto G_k(\theta)$ need not be the gradient of any function: a gradient field has a symmetric Jacobian, and for CD-1 the Jacobian of $G_1$ is not symmetric in general (Sutskever and Tieleman 2010). The tests of the implementation find an asymmetry above $10^{-3}$ for a model with 3 visible and 2 hidden units, while the Jacobian of the exact gradient is symmetric up to rounding. The fixed points of CD-1 can also differ from the maximum likelihood estimate (Carreira-Perpiñán and Hinton 2005).
