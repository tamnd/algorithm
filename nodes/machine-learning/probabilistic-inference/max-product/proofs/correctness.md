---
title: On a factor tree max-product with backtracking returns a MAP assignment
proves: [correctness]
status: full
---

We use the pseudocode MAX-PRODUCT of the page. As for [belief propagation](/belief-propagation/), we may treat one tree of the forest at a time: the trees share no variable and no factor, so the maximum of the product over all the variables is the product of the maxima over the trees, and line L4 multiplies them. So let the factor graph be a tree with root variable $r$. All the tables are nonnegative. Let $\lambda_x$ be the evidence indicator of $x$, and
$$\tilde p(x) = \prod_v \lambda_v(x_v) \prod_f f(x_f).$$
An assignment agrees with the evidence exactly when its $\tilde p$ value can be positive, and a MAP assignment is one that maximizes $\tilde p$.

**Two rules.** For nonnegative numbers, $a \cdot \max(b, c) = \max(ab, ac)$, and the maximum over two independent groups of a product of nonnegative functions, one on each group, is the product of the two maxima. These replace the rule that the product distributes over the sum. In log space the rules are $a + \max(b, c) = \max(a + b, a + c)$ and the sum of maxima, true for all reals and $-\infty$.

**Sides.** For a node $u$ with parent $w$, let $T_u$ be the part of the tree that holds $u$ when the edge $\{u, w\}$ is removed, and $\Pi_u$ the product of the factors and indicators in it. Let $x_w$ stand for the variable of the edge.

**Claim 1 (collect messages).** After line L2, for each node $u$ with parent $w$,
$$\mu_{u \to w}(x) = \max \{\Pi_u(y) : y \text{ an assignment of the variables of } T_u \text{ with } y_{\text{edge}} = x\}.$$

*Proof.* The same induction as for belief propagation, with max in place of the sum, using the two rules. A variable $u$ sends $\lambda_u(x) \prod_g \mu_{g \to u}(x)$ over its child factors $g$, whose sides are disjoint and meet only in $u$; with $u$ fixed the maxima over the sides are independent, so their product is the maximum of the product. A factor $u = f$ sends to its parent variable $w$ the maximum over the other variables $z$ of the scope of $f(x_f) \prod_z \mu_{z \to f}(x_z)$ (line L3); by induction each $\mu_{z \to f}(x_z)$ is the maximum over the side of $z$ with $z$ fixed, these sides are disjoint, and with $x_f$ fixed they are independent. $\blacksquare$

At the root, the sides of the factors of $r$ are disjoint, meet only in $r$, and cover the tree. So $b_r(x) = \lambda_r(x) \prod_g \mu_{g \to r}(x)$ is the maximum of $\tilde p$ with $X_r = x$, and $\max_x b_r(x) = M$, the maximum of $\tilde p$. This is the value of line L4.

**Claim 2 (backtracking).** Let $x^*$ be the assignment built by lines L4 to L7, with any choice among tied maximizers. For each variable $y \ne r$ with parent factor $f$, the value of $\Pi_y$ at $x^*$ is $\mu_{y \to f}(x^*_y)$. For each factor $g$ with parent variable $p$, the value of $\Pi_g$ at $x^*$ is $\mu_{g \to p}(x^*_p)$.

*Proof.* Lines L5 to L7 visit the factors in breadth-first order, so when the factor $g$ is visited, its parent $p$ already has its value, and the variables below $g$ get theirs now; every variable gets exactly one value, from its parent factor or at the root. We prove the claim by induction from the leaves upward.

For a factor $g$ with parent $p$: line L6 picks the row $a$ of $g$ with $a_p = x^*_p$ that maximizes $g(a) \prod_z \mu_{z \to g}(a_z)$ over the child variables $z$, and line L7 sets $x^*_z = a_z$. So, by Claim 1 for line L3, $g(a) \prod_z \mu_{z \to g}(x^*_z) = \mu_{g \to p}(x^*_p)$. By induction, the value of $\Pi_z$ at $x^*$ is $\mu_{z \to g}(x^*_z)$, and $\Pi_g = g \prod_z \Pi_z$, which gives the claim for $g$.

For a variable $y$ with parent factor $f$: $\Pi_y = \lambda_y \prod_g \Pi_g$ over the child factors $g$ of $y$. By induction each $\Pi_g$ has the value $\mu_{g \to y}(x^*_y)$ at $x^*$, so $\Pi_y(x^*) = \lambda_y(x^*_y) \prod_g \mu_{g \to y}(x^*_y) = \mu_{y \to f}(x^*_y)$, by the variable update of line L2. $\blacksquare$

**Theorem.** $\tilde p(x^*) = M$, so $x^*$ is a MAP assignment. If $M > 0$, it agrees with the evidence.

*Proof.* $\tilde p = \lambda_r \prod_g \Pi_g$ over the factors $g$ of the root. By Claim 2, $\tilde p(x^*) = \lambda_r(x^*_r) \prod_g \mu_{g \to r}(x^*_r) = b_r(x^*_r)$, and line L4 chose $x^*_r$ to maximize $b_r$, so $\tilde p(x^*) = M$. If $M > 0$, every indicator is 1 at $x^*$. $\blacksquare$

**Max-marginals.** After the distribute pass, the argument of belief propagation with max in place of the sum shows that $\lambda_x(x) \prod_{f \in N(x)} \mu_{f \to x}(x)$ is the maximum of $\tilde p$ with $X = x$, for every variable.

**Why backtracking and not the max-marginals alone.** Each value that maximizes its own max-marginal is part of some MAP assignment, but when there are ties, the values chosen at different variables can come from different MAP assignments. For the factor $f(x, y) = [x \ne y]$, both max-marginals are $(1, 1)$, and the choice $(0, 0)$ has value 0. Backtracking avoids this, because each choice is made with the values of the parent fixed. Without ties, the maximizer of each max-marginal is unique and the two methods agree. $\blacksquare$
