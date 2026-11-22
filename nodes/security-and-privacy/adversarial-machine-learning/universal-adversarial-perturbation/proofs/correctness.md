---
title: The universal perturbation stays in the ball and reaches the best rate on a binary linear model
proves: [correctness]
status: full
---

Let the data be $x^1, \dots, x^n \in [0,1]^d$, let $\epsilon \ge 0$, and let $B = \{v : \lVert v \rVert_p \le \epsilon\}$ with $p \in \{2, \infty\}$. The map $P_B$ of line L6 is `project_ball`. The fooling rate of $v$ is the fraction of the $x^i$ whose label at $\operatorname{clip}(x^i + v)$ differs from the label at $x^i$.

**Lemma 1.** $P_B$ is the Euclidean projection onto $B$, so $P_B(u) \in B$ for every $u$.

*Proof.* For $p = 2$, `project_l2` keeps a point of the ball and moves any other point $u$ to $\epsilon u / \lVert u \rVert_2$, the nearest point of the sphere. For $p = \infty$, $B$ is the box $[-\epsilon, \epsilon]^d$, and clipping each coordinate gives the nearest point of a box. $\square$

**Theorem 1 (a valid output).** The returned $v$ satisfies $\lVert v \rVert_p \le \epsilon$, and the returned rate is the fooling rate of $v$ on the data.

*Proof.* Line L1 sets $v = 0 \in B$. The only other assignment to $v$ is line L6, whose result is in $B$ by Lemma 1. Line L7 computes the rate of the current $v$ after each pass, and $v$ does not change between line L7 and the return in line L9: line L8 breaks right after line L7, and otherwise the loop ends after line L7 of the last pass. If there are no passes, $v = 0$ and the rate is $0$, the rate of $0$. $\square$

**Theorem 2 (an upper bound for binary linear models).** Let the logits be $(0, f(u))$ with $f(u) = w^\top u + b$ and $w \ne 0$, so the label is $1$ when $f(u) > 0$ and $0$ otherwise. Let every $x^i$ have label $1$, and assume that no clip acts on the points that the algorithm visits. Then every $v \in B$ has fooling rate at most $R^\star = |\{i : f(x^i) \le \epsilon \lVert w \rVert_q\}| / n$, where $q = 2$ for $p = 2$ and $q = 1$ for $p = \infty$.

*Proof.* A point $x^i$ is fooled by $v$ when $f(x^i + v) = f(x^i) + w^\top v \le 0$. By Hölder's inequality, $w^\top v \ge -\lVert w \rVert_q \lVert v \rVert_p \ge -\epsilon \lVert w \rVert_q$. So a fooled point has $f(x^i) \le \epsilon \lVert w \rVert_q$. $\square$

**Theorem 3 (the $\ell_2$ rate is the best one).** Under the assumptions of Theorem 2 with $p = 2$, after one pass the fooling rate is $R^\star$, provided that no $f(x^i)$ is equal to $\epsilon \lVert w \rVert_2$.

*Proof.* For the logits $(0, f)$ and label $1$, the only other class is $0$, and its difference vector is $w_0 = \nabla z_0 - \nabla z_1 = -w$. So each DeepFool step of line L5 is a positive multiple of $-w$, and the projection of line L6 multiplies $v$ by a positive number. By induction, $v = -\tau\, w / \lVert w \rVert_2$ with $0 \le \tau \le \epsilon$ at all times, and $\tau$ never decreases: a step adds a positive amount to $\tau$ and the projection caps $\tau$ at $\epsilon$. The point $x^i$ is fooled by such a $v$ exactly when $f(x^i) \le \tau \lVert w \rVert_2$, so a point once fooled stays fooled. Take a point $x^i$ with $f(x^i) < \epsilon \lVert w \rVert_2$ that is not fooled when line L4 reaches it. On an affine model the inner DeepFool reaches the far side of the boundary at its first step (see the proof page of deepfool), so $v + r$ fools $x^i$. If the projection does not act, $v$ fools $x^i$ after line L6. If it acts, $\tau = \epsilon$ after line L6, and $f(x^i) < \epsilon \lVert w \rVert_2$ means $x^i$ is fooled. So at the end of the pass every point with $f(x^i) < \epsilon \lVert w \rVert_2$ is fooled, and no other point can be fooled by Theorem 2. $\blacksquare$

**What is not claimed.** For $p = \infty$ the iterates stay on the line of $w$ only until a projection clips some coordinates, so the $\ell_\infty$ result can be below $R^\star$; the test checks only the upper bound there. For a nonlinear model, the algorithm is a heuristic: the result depends on the order of the data, and no optimality holds. The fooling rate is a measurement on the given data, not a guarantee on new data.
