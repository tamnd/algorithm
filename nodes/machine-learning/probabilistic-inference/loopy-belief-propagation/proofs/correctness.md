---
title: Loopy BP is exact on trees, and its fixed points are the Bethe stationary points
proves: [correctness]
status: full
---

We use the factor graph, the messages and the pseudocode of the page. All factors are positive. Write $d_i = |N(i)|$, and write $\propto$ for equality up to a positive factor that does not depend on the argument. A *fixed point* is a set of positive normalized messages $\mu_{a \to i}$ with $\mu = F(\mu)$, where $F$ is lines L3 and L4: first $\nu_{i \to a} \propto \prod_{c \in N(i) \setminus a} \mu_{c \to i}$, then $\mu'_{a \to i} \propto \sum_{x_a \setminus x_i} f_a \prod_{j \in N(a) \setminus i} \nu_{j \to a}$.

**Lemma 1 (damping keeps the fixed points).** For $0 \le \lambda < 1$, the damped map $G(\mu) = \mathrm{normalize}((1 - \lambda) F(\mu) + \lambda \mu)$ has the same fixed points as $F$.

*Proof.* If $F(\mu) = \mu$, then $(1 - \lambda)\mu + \lambda \mu = \mu$, which is already normalized. Conversely, if $G(\mu) = \mu$, then, since $F(\mu)$ and $\mu$ both sum to 1 on each edge, $(1 - \lambda) F(\mu) + \lambda \mu$ also sums to 1, so the normalization does nothing and $(1 - \lambda) F(\mu) + \lambda \mu = \mu$. As $\lambda < 1$, this gives $F(\mu) = \mu$. $\square$

**Lemma 2 (exact on trees).** Let the factor graph be a tree and $\lambda = 0$. For an edge $(a, i)$, removing the edge splits the tree in two; let $T_{a \to i}$ be the part that contains $a$, and define its height by $h(a \to i) = 1 + \max\{h(c \to j) : j \in N(a) \setminus i,\ c \in N(j) \setminus a\}$, with the maximum of the empty set equal to 0. Then after round $t \ge h(a \to i)$,

$$\mu_{a \to i}(x_i) \propto \sum_{x_{T_{a \to i}} \setminus x_i} \ \prod_{c \in T_{a \to i}} f_c(x_c) =: M_{a \to i}(x_i),$$

where the sum is over all variables of $T_{a \to i}$ other than $x_i$. Also the fixed point of $F$ is unique and equal to these messages.

*Proof.* By induction on $h = h(a \to i)$. The parts $T_{c \to j}$ for $j \in N(a) \setminus i$ and $c \in N(j) \setminus a$ are disjoint, and with factor $a$ and the variables $j$ they make up $T_{a \to i}$, because the graph is a tree. So the sum that defines $M_{a \to i}$ factors as

$$M_{a \to i}(x_i) = \sum_{x_a \setminus x_i} f_a(x_a) \prod_{j \in N(a) \setminus i} \ \prod_{c \in N(j) \setminus a} M_{c \to j}(x_j).$$

If $h = 1$, the products are empty, and line L4 of round 1 gives $\mu_{a \to i} \propto \sum_{x_a \setminus x_i} f_a$, which is $M_{a \to i}$; nothing changes in later rounds. If $h > 1$ and $t \ge h$, then in round $t$ line L3 uses the messages $\mu_{c \to j}$ from the end of round $t - 1 \ge h(c \to j)$, which are $\propto M_{c \to j}$ by induction; so line L4 gives $\mu_{a \to i} \propto M_{a \to i}$ by the display. The same argument, with "after round $t$" replaced by "at a fixed point", shows that every fixed point has $\mu_{a \to i} \propto M_{a \to i}$, so the fixed point is unique. $\square$

**Corollary.** On a tree, the beliefs at the fixed point are the exact marginals. Removing variable $i$ splits the tree into the parts $T_{a \to i}$, $a \in N(i)$, which hold every factor once. So $p(x_i) \propto \sum_{x \setminus x_i} \prod_c f_c = \prod_{a \in N(i)} M_{a \to i}(x_i) \propto b_i(x_i)$. In the same way, removing factor $a$ splits the tree into $a$ and the parts $T_{c \to j}$, so $p(x_a) \propto f_a \prod_{j} \prod_{c \in N(j) \setminus a} M_{c \to j}(x_j) \propto b_a(x_a)$. By Lemma 1, damping does not change this fixed point.

**Lemma 3 (local consistency).** At a fixed point, $\sum_{x_a \setminus x_i} b_a(x_a) = b_i(x_i)$ for every edge $(a, i)$, where $b_a \propto f_a \prod_{j \in N(a)} \nu_{j \to a}$ and $b_i \propto \prod_{c \in N(i)} \mu_{c \to i}$ are normalized.

*Proof.* $\sum_{x_a \setminus x_i} f_a \prod_{j \in N(a)} \nu_{j \to a} = \nu_{i \to a}(x_i) \sum_{x_a \setminus x_i} f_a \prod_{j \ne i} \nu_{j \to a} \propto \nu_{i \to a}(x_i)\, \mu_{a \to i}(x_i) \propto \prod_{c \in N(i)} \mu_{c \to i}(x_i)$, using line L4 and then line L3 at the fixed point. Both sides sum to 1 over $x_i$, so they are equal. $\square$

**Theorem (Yedidia, Freeman and Weiss).** Let

$$F_{\mathrm{Bethe}}(b) = \sum_a \sum_{x_a} b_a(x_a) \log \frac{b_a(x_a)}{f_a(x_a)} - \sum_i (d_i - 1) \sum_{x_i} b_i(x_i) \log b_i(x_i)$$

on the local polytope $\mathcal{L}$: $b_a, b_i \ge 0$, $\sum_{x_i} b_i = 1$, $\sum_{x_a} b_a = 1$, and $\sum_{x_a \setminus x_i} b_a = b_i$ for every edge. Then the beliefs of every fixed point are a stationary point of $F_{\mathrm{Bethe}}$ on $\mathcal{L}$, and every stationary point with all $b > 0$ is the set of beliefs of a fixed point.

*Proof.* The constraints are affine, so a point with $b > 0$ is stationary on $\mathcal{L}$ if and only if there are multipliers $\lambda_{ai}(x_i)$, $\gamma_a$, $\gamma_i$ such that the gradient of

$$F_{\mathrm{Bethe}} + \sum_{(a, i)} \sum_{x_i} \lambda_{ai}(x_i) \Big( b_i(x_i) - \sum_{x_a \setminus x_i} b_a(x_a) \Big) + \sum_a \gamma_a \Big( \sum_{x_a} b_a - 1 \Big) + \sum_i \gamma_i \Big( \sum_{x_i} b_i - 1 \Big)$$

is 0. The derivatives in $b_a(x_a)$ and $b_i(x_i)$ give the conditions

$$\text{(A)}\ \ b_a(x_a) \propto f_a(x_a) \exp\Big( \sum_{i \in N(a)} \lambda_{ai}(x_i) \Big), \qquad \text{(B)}\ \ (d_i - 1) \log b_i(x_i) = \sum_{a \in N(i)} \lambda_{ai}(x_i) + \mathrm{const}_i,$$

since $\partial_{b_a} = \log b_a - \log f_a + 1 - \sum_i \lambda_{ai}(x_i) + \gamma_a$ and $\partial_{b_i} = -(d_i - 1)(\log b_i + 1) + \sum_a \lambda_{ai}(x_i) + \gamma_i$. Conversely, (A) and (B) give such multipliers, with $\gamma_a, \gamma_i$ chosen to absorb the constants.

*From a fixed point.* Let $\lambda_{ai} = \log \nu_{i \to a}$. Then (A) is the definition of $b_a$. For (B), $\sum_{a \in N(i)} \log \nu_{i \to a} = \sum_a \sum_{c \ne a} \log \mu_{c \to i} + \mathrm{const} = (d_i - 1) \sum_c \log \mu_{c \to i} + \mathrm{const} = (d_i - 1) \log b_i + \mathrm{const}$, because each $c$ appears for the $d_i - 1$ choices of $a \ne c$. The beliefs are positive and in $\mathcal{L}$ by Lemma 3. So they are a stationary point.

*To a fixed point.* Let $b > 0$ be stationary with multipliers $\lambda$. Define $\nu_{i \to a} \propto \exp(\lambda_{ai})$ and $\mu_{a \to i} \propto b_i / \nu_{i \to a}$, both normalized and positive. By (B), $\prod_{c \in N(i)} \nu_{i \to c} \propto b_i^{d_i - 1}$. Then:

- Line L3: $\prod_{c \in N(i) \setminus a} \mu_{c \to i} \propto b_i^{d_i - 1} \big/ \prod_{c \ne a} \nu_{i \to c} \propto b_i^{d_i - 1}\, \nu_{i \to a} / b_i^{d_i - 1} = \nu_{i \to a}$.
- Line L4: $\sum_{x_a \setminus x_i} f_a \prod_{j \ne i} \nu_{j \to a} = \nu_{i \to a}(x_i)^{-1} \sum_{x_a \setminus x_i} f_a \prod_{j} \nu_{j \to a} \propto \nu_{i \to a}(x_i)^{-1} \sum_{x_a \setminus x_i} b_a \propto b_i / \nu_{i \to a} \propto \mu_{a \to i}$, by (A) and the marginal constraint.

So the messages are a fixed point. Their beliefs are $\prod_c \mu_{c \to i} \propto b_i^{d_i} / b_i^{d_i - 1} = b_i$ and $f_a \prod_j \nu_{j \to a} \propto b_a$ by (A). If $d_i = 1$, then (B) says that $\lambda_{ai}$ is constant, so $\nu_{i \to a}$ is uniform, which is the empty product of line L3; the steps above still hold. $\blacksquare$

**Remarks.** On a tree, $F_{\mathrm{Bethe}}$ at the exact marginals equals $-\log Z$, which is proved on the Bethe free energy page. The theorem says nothing about convergence: the frustrated $K_4$ of the page has a fixed point (damping finds it) but the undamped iteration does not reach it. For convergence, the Mooij-Kappen condition is a sufficient condition; its proof uses a contraction argument in a suitable norm on the log messages and is in the paper.
