---
title: The leaf weights, the split gain and the exact greedy split finder of XGBoost
proves: [correctness]
status: full
---

We use the pseudocode of the page. In round $t$, $\hat y_i$ is the prediction of example $i$ before the round, $g_i = \partial \ell(y_i, \hat y) / \partial \hat y$ and $h_i = \partial^2 \ell(y_i, \hat y) / \partial \hat y^2$ at $\hat y = \hat y_i$. We assume that the loss is convex in $\hat y$, so $h_i \ge 0$, and that $\lambda > 0$ or each leaf has $H_j > 0$, so that each denominator $H_j + \lambda$ is positive. A tree $f$ with $J$ leaves maps $x$ to the weight $w_{q(x)}$ of its leaf $q(x)$, and $\Omega(f) = \gamma J + \frac12 \lambda \sum_{j=1}^{J} w_j^2$.

### Claim 1: the second-order objective

Taylor's theorem in $\hat y$ gives $\ell(y_i, \hat y_i + f(x_i)) = \ell(y_i, \hat y_i) + g_i f(x_i) + \frac12 h_i f(x_i)^2 + o(f(x_i)^2)$. Dropping the remainder and the constant $\sum_i \ell(y_i, \hat y_i)$, round $t$ minimizes

$$\tilde{\mathcal L}(f) = \sum_{i=1}^{n} \left(g_i f(x_i) + \tfrac12 h_i f(x_i)^2\right) + \Omega(f).$$

For squared loss $\ell = \frac12 (y - \hat y)^2$ the remainder is zero, since $\ell$ is a quadratic in $\hat y$, so $\tilde{\mathcal L}$ is exact up to the constant. $\square$

### Claim 2: the best leaf weights and the structure score

Fix the structure $q$ and let $I_j = \{i : q(x_i) = j\}$, $G_j = \sum_{i \in I_j} g_i$ and $H_j = \sum_{i \in I_j} h_i$. Group the sum by leaves:

$$\tilde{\mathcal L} = \sum_{j=1}^{J} \left(G_j w_j + \tfrac12 (H_j + \lambda) w_j^2\right) + \gamma J.$$

The terms are independent, and each is a quadratic in $w_j$ with positive leading coefficient $\frac12(H_j + \lambda)$. Its derivative $G_j + (H_j + \lambda) w_j$ is zero at the unique minimizer

$$w_j^* = -\frac{G_j}{H_j + \lambda},$$

and the minimum value of the term is $G_j w_j^* + \frac12 (H_j + \lambda) (w_j^*)^2 = -\frac{G_j^2}{H_j + \lambda} + \frac{G_j^2}{2(H_j + \lambda)} = -\frac{G_j^2}{2(H_j + \lambda)}$. So the best objective of the structure $q$ is

$$\tilde{\mathcal L}^*(q) = -\frac12 \sum_{j=1}^{J} \frac{G_j^2}{H_j + \lambda} + \gamma J. \qquad \square$$

### Claim 3: the split gain

Replace one leaf with index set $I$ by two leaves $I_L$ and $I_R$ that partition it, and keep the other leaves. By Claim 2 the terms of the other leaves do not change. The term of $I$ was $-\frac{G^2}{2(H + \lambda)} + \gamma$ and the two new terms are $-\frac{G_L^2}{2(H_L + \lambda)} - \frac{G_R^2}{2(H_R + \lambda)} + 2\gamma$. So the decrease of $\tilde{\mathcal L}^*$ is

$$\mathcal L_{\text{split}} = \frac12\left(\frac{G_L^2}{H_L + \lambda} + \frac{G_R^2}{H_R + \lambda} - \frac{(G_L + G_R)^2}{H_L + H_R + \lambda}\right) - \gamma. \qquad \square$$

A split lowers the regularized objective exactly when $\mathcal L_{\text{split}} > 0$. With $a = H_L + \lambda$ and $b = H_R + \lambda$, a direct computation gives

$$\frac{G_L^2}{a} + \frac{G_R^2}{b} - \frac{(G_L + G_R)^2}{a + b} = \frac{(b G_L - a G_R)^2}{a b (a + b)} \ge 0.$$

When $\lambda = 0$, $a + b = H_L + H_R + \lambda$, so the bracket of $\mathcal L_{\text{split}}$ is never negative. When $\lambda > 0$, $H_L + H_R + \lambda = a + b - \lambda < a + b$, so the subtracted term is larger and the bracket can be negative. The example of the page has a split with bracket $-0.3214$. The penalty $\gamma$ then sets the least decrease that a split must give.

### Claim 4: the exact greedy finder returns a split of largest gain

Fix a node $I$ and a feature $k$. Let $P$ be the indices in $I$ whose value $x_{ik}$ is present, sorted by $x_{ik}$, and let $M = I \setminus P$, with sums $G_M$ and $H_M$. A threshold split with a default direction sends the present values $x_{ik} \le \theta$ left and the rest right, and sends all of $M$ to the side of the default direction. Up to the choice of $\theta$ inside a gap between two distinct present values, such a split is given by a number $j$ of leading elements of $P$ (with no cut between equal values) and a direction. The loop of line L11 visits each such $j$, from $0$ to $|P|$, and line L12 keeps $G_L$ and $H_L$ equal to the sums over the first $j$ elements of $P$, by induction on $j$. Line L14 adds $G_M$ and $H_M$ exactly when the missing values go left. So line L15 computes $\mathcal L_{\text{split}}$ of Claim 3 for each split of this form, and line L16 keeps the largest. Doing this for each feature $k$ covers every threshold split of the node with either default direction. $\square$

**The default direction rule.** For each cut, the finder tries both directions and keeps the one of larger gain. So the learned default direction of a node is the side that the missing values of the training set prefer under the objective, and a prediction sends a missing value there. When a feature has no missing values in the node, $G_M = H_M = 0$ and both directions give the same gain.

### Claim 5: why the sketch weights the points by $h_i$

When $h_i > 0$, completing the square gives $g_i f + \frac12 h_i f^2 = \frac12 h_i (f + g_i/h_i)^2 - g_i^2/(2h_i)$. So

$$\tilde{\mathcal L}(f) = \sum_{i=1}^{n} \tfrac12 h_i \left(f(x_i) - (-g_i / h_i)\right)^2 + \Omega(f) + \text{constant}.$$

This is a weighted squared loss with targets $-g_i/h_i$ and weights $h_i$. A candidate split that is good for the objective should therefore split the feature into parts of about equal total $h$, not of about equal count, which is what the weighted quantile sketch proposes. $\square$

### Termination

Each split makes two nonempty children, so each tree has at most $|I|$ leaves at a node of $|I|$ examples, and growth stops at depth $D$ or when no split has a positive gain. The outer loop runs $T$ times.
