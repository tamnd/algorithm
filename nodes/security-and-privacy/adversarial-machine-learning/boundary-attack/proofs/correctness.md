---
title: The boundary attack stays adversarial and never moves away from the input
proves: [correctness]
status: full
---

Let $x \in [0,1]^d$ have label $y$, and let the start $a^0 \in [0,1]^d$ have a label other than $y$. The attack sees only labels. We write $D(a) = \lVert a - x \rVert_2$ and $\Pi$ for the clip to $[0,1]^d$.

**Lemma 1 (the clip does not move points away from $x$).** For every $u \in \mathbb{R}^d$, $\lVert \Pi(u) - x \rVert_2 \le \lVert u - x \rVert_2$.

*Proof.* Since $x_i \in [0,1]$, clipping $u_i$ to $[0,1]$ moves it toward $x_i$ or leaves it in place, so $|\Pi(u)_i - x_i| \le |u_i - x_i|$ for each $i$. $\square$

**Lemma 2 (the two candidates).** Let $a \ne x$, $\alpha > 0$, $0 < \beta < 1$, and let the noise $\eta \ne 0$ be such that the moved point $m = a + \alpha D(a)\, \eta / \lVert \eta \rVert_2$ is not $x$. Then, before the clip, the orthogonal candidate $o$ has $D(o) = D(a)$, and the full candidate $c$ has $c - x = (1 - \beta)(o - x)$, so $D(c) = (1 - \beta) D(a)$. After the clip, $D(\Pi(c)) \le (1 - \beta) D(a)$.

*Proof.* In `candidate`, $o = x + (m - x) \cdot D(a) / \lVert m - x \rVert_2$, so $D(o) = D(a)$. Then $c = o + \beta(x - o)$, so $c - x = (1 - \beta)(o - x)$. The last claim follows from Lemma 1. $\square$

The case $m = x$ has probability $0$ for Gaussian noise, and the code does not guard against it.

**Theorem 1 (the invariant).** Assume $\alpha > 0$ and $0 < \beta < 1$ at the start. After every step $t$, the iterate $a^t$ lies in $[0,1]^d$, its label is not $y$, and $D(a^t) \le D(a^{t-1})$. When a full candidate is accepted, $D(a^t) \le (1 - \beta_t) D(a^{t-1})$. The attack uses at most $2T$ queries for $T$ steps.

*Proof.* Line L1 sets $a^0$ to the start, which satisfies the first two claims. The iterate changes only in line L6, and only to the clipped full candidate after a query has shown that its label is not $y$. That point lies in $[0,1]^d$, and Lemma 2 gives the bound on its distance. The rule of line L7 multiplies $\alpha$ and $\beta$ by $1.5$ or $1/1.5$ and caps $\beta$ at $0.9$, so $\alpha$ stays positive and $\beta$ stays in $(0, \max(\beta_0, 0.9)]$, which is inside $(0, 1)$. Each step makes one query in line L5 and at most one more in line L6. If the iterate reaches $x$ itself, line L2 stops, because then $x$ would have a label other than $y$, which does not happen. $\square$

**Corollary (a bound from below on linear models).** If the label is $1$ exactly when $w^\top u + b > 0$, then for every $t$, $D(a^t) \ge |w^\top x + b| / \lVert w \rVert_2$. So the distance of the output is between the true minimum distance and $D(a^0)$.

*Proof.* The iterate is on the other side of the hyperplane $w^\top u + b = 0$ (or on it), and the distance from $x$ to that closed half space is $|w^\top x + b| / \lVert w \rVert_2$. $\blacksquare$

**What is not claimed.** The proof shows that the distance never grows; it does not show that it reaches the minimum. The rate depends on the step sizes, the dimension and the shape of the boundary. In the seeded tests on random linear models in one to four dimensions, 120 steps gave a distance at most $1.066$ times the minimum (a measurement, not a theorem). The adaptation rule of line L7 is a simple version of the one in the paper by Brendel, Rauber and Bethge.
