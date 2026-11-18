---
title: Vertex updates of one color commute, a line search makes the descent monotone, and fixed points are backward Euler steps
proves: [correctness]
status: full
---

We use the notation of the page, for a 2D mass-spring system. The free vertices have masses $m_i > 0$ and positions $\mathbf x_i$; pinned vertices are fixed. Spring $s = (a, b)$ has rest length $r_s > 0$, stiffness $k_s > 0$ and energy $E_s = \frac{k_s}{2}(|\mathbf x_a - \mathbf x_b| - r_s)^2$. With $\mathbf y = \mathbf x^n + \Delta t\mathbf v^n + \Delta t^2\mathbf g$ the objective of the step is

$$G(\mathbf x) = \sum_i \frac{m_i}{2\Delta t^2}|\mathbf x_i - \mathbf y_i|^2 + \sum_s E_s(\mathbf x).$$

For a free vertex $i$, let $\mathcal F_i$ be the set of springs that touch it, and let the local energy be $G_i(\mathbf z) = \frac{m_i}{2\Delta t^2}|\mathbf z - \mathbf y_i|^2 + \sum_{s \in \mathcal F_i} E_s(\mathbf x \text{ with } \mathbf x_i = \mathbf z)$.

## The local problem

**Lemma 1.** $G(\mathbf x) = G_i(\mathbf x_i) + c_i$, where $c_i$ does not depend on $\mathbf x_i$. So $\mathbf f_i = -\nabla G_i(\mathbf x_i) = -\nabla_i G(\mathbf x)$ and $H_i = \nabla^2 G_i(\mathbf x_i) = \nabla^2_{ii} G(\mathbf x)$, and for a spring with $\ell = |\mathbf x_i - \mathbf x_j| > 0$ and $\mathbf n = (\mathbf x_i - \mathbf x_j)/\ell$,

$$\nabla_i E_s = k_s(\ell - r_s)\,\mathbf n, \qquad \nabla_{ii}^2 E_s = k_s\Big(\mathbf n\mathbf n^T + \big(1 - \tfrac{r_s}{\ell}\big)(I - \mathbf n\mathbf n^T)\Big).$$

*Proof.* The terms of $G$ that contain $\mathbf x_i$ are the inertia term of $i$ and the springs of $\mathcal F_i$, which are exactly the terms of $G_i$. For the spring, $\nabla_i \ell = \mathbf n$ and $\nabla_i \mathbf n = (I - \mathbf n\mathbf n^T)/\ell$, so $\nabla_i E_s = k_s(\ell - r_s)\mathbf n$, and differentiating again gives $k_s\mathbf n\mathbf n^T + k_s(\ell - r_s)(I - \mathbf n\mathbf n^T)/\ell$. $\square$

These are equations (7) and (9) of Chen et al. (2024) for this energy, in 2D. The second term of the spring Hessian is negative when the spring is compressed ($\ell < r_s$), so $H_i$ can be indefinite or singular; the code skips the vertex when $|\det H_i| \le \varepsilon$.

## Colors

**Lemma 2 (updates of one color commute).** Let $i \ne j$ be free vertices that no spring joins. Then $G_i$ does not depend on $\mathbf x_j$, so the update of $i$ computed before or after the update of $j$ is the same. Hence, for a set of vertices of one color, computing all updates from the same state and then applying them gives the same result as applying them one after another, in any order.

*Proof.* $G_i$ contains $\mathbf x_j$ only through a spring of $\mathcal F_i$ with the other end $j$, and there is none. The update of $i$ is a function of $G_i$ only (the Newton step, the determinant test and the line search all use $G_i$), so it does not change when $\mathbf x_j$ changes. By induction over the order of the updates in the color, every update sees the same data as in the parallel version. $\square$

**Lemma 3.** The greedy coloring of the code is proper and uses at most $\Delta + 1$ colors, where $\Delta$ is the largest number of springs at a vertex.

*Proof.* Each vertex gets the smallest color that none of its colored neighbors has, so no spring joins two vertices of one color. A vertex has at most $\Delta$ neighbors, so one of the colors $0, \dots, \Delta$ is free. $\square$

## Descent

**Theorem 4 (monotone with a line search).** With the line search, no vertex update increases $G$. So $G$ never increases during a step.

*Proof.* The line search accepts a step $t\Delta\mathbf x_i$ only if $G_i(\mathbf x_i + t\Delta\mathbf x_i) \le G_i(\mathbf x_i)$, and otherwise returns zero. By Lemma 1, $G$ changes by the same amount as $G_i$. Within a color, Lemma 2 shows that the parallel updates equal the sequential ones, and each of those does not increase $G$. $\square$

**Lemma 5.** If $H_i$ is positive definite and $\mathbf f_i \ne 0$, the Newton step $\Delta\mathbf x_i = H_i^{-1}\mathbf f_i$ is a descent direction of $G_i$, and the backtracking line search accepts some $t = 2^{-q} > 0$ with a strict decrease, provided $G_i$ is smooth near $\mathbf x_i$.

*Proof.* $\nabla G_i \cdot \Delta\mathbf x_i = -\mathbf f_i^T H_i^{-1}\mathbf f_i < 0$. By Taylor's theorem $G_i(\mathbf x_i + t\Delta\mathbf x_i) < G_i(\mathbf x_i)$ for all small enough $t > 0$, and halving reaches such a $t$. $\square$

Without a line search there is no such guarantee: a full Newton step can overshoot, and with an indefinite $H_i$ it can point uphill. The paper notes that the Newton step does not guarantee a decrease and makes the line search optional. The page shows a crumpled start where one plain sweep raises $G$ by a factor of about $10^5$.

**Theorem 6 (fixed points).** Suppose that at $\mathbf x^*$ every $H_i$ satisfies $|\det H_i| > \varepsilon$. Then a sweep leaves $\mathbf x^*$ unchanged if and only if $\nabla G(\mathbf x^*) = 0$, that is, if $\mathbf x^*$ satisfies the backward Euler equation $M(\mathbf x^* - \mathbf y)/\Delta t^2 = -\nabla\sum_s E_s(\mathbf x^*)$ on the free vertices.

*Proof.* Without the line search, the update of $i$ is $H_i^{-1}\mathbf f_i$, which is zero exactly when $\mathbf f_i = 0$. With the line search, a zero update can also come from a failed search, but if $\mathbf f_i \ne 0$ and $H_i$ is positive definite, Lemma 5 rules this out; we state the theorem for the plain update and for this case. If $\nabla G(\mathbf x^*) = 0$, every $\mathbf f_i = 0$ by Lemma 1, so every update is zero. Conversely, if the sweep leaves $\mathbf x^*$ unchanged, the first update of each color is computed at $\mathbf x^*$ (Lemma 2), so every $\mathbf f_i(\mathbf x^*) = 0$, and $\nabla G(\mathbf x^*) = 0$. $\square$

The theorem does not say that the sweeps converge or how fast. Block coordinate descent converges linearly at best, and the page measures the rate.

**Corollary 7 (one spring).** For one free vertex joined to a pin at the origin by a spring of rest length $r$, with $\mathbf y_i = (y, 0)$, $y > 0$, and the start $\mathbf x_i = \mathbf y_i$, one update gives $\mathbf x_i = (\frac{m y + \Delta t^2 k r}{m + \Delta t^2 k}, 0)$, the backward Euler step.

*Proof.* Here $\mathbf n = (1, 0)$, $\mathbf f_i = (-k(y - r), 0)$ and $H_i$ is diagonal with first entry $m/\Delta t^2 + k$. So $\Delta\mathbf x_i = (-k(y - r)/(m/\Delta t^2 + k), 0)$, and $y + \Delta x = (m y + \Delta t^2 k r)/(m + \Delta t^2 k)$. At this point $\mathbf f_i = 0$: the second component is zero by symmetry, and the first is $-\frac{m}{\Delta t^2}(x - y) - k(x - r) = 0$ by the formula. $\square$

## Momentum

**Lemma 8.** With no pins and no gravity, every stationary point of $G$ satisfies $\sum_i m_i\mathbf x_i = \sum_i m_i\mathbf y_i$, so a converged step keeps the linear momentum. A finite number of sweeps does not keep it in general.

*Proof.* Each $E_s$ is invariant under a common translation of its two ends, so $\sum_i \nabla_i E_s = 0$. Summing $\nabla_i G = 0$ over $i$ gives $\sum_i m_i(\mathbf x_i - \mathbf y_i)/\Delta t^2 = 0$, and with $\mathbf y = \mathbf x^n + \Delta t\mathbf v^n$ and $\mathbf v^{n+1} = (\mathbf x - \mathbf x^n)/\Delta t$ this is $\sum m_i\mathbf v^{n+1}_i = \sum m_i \mathbf v^n_i$. A single vertex update changes $\sum m_j\mathbf x_j$ by $m_i\Delta\mathbf x_i$, which is not zero unless $\mathbf f_i = 0$, and nothing in a sweep cancels it exactly; the test measures a nonzero drift after 1 and 10 sweeps. $\square$

## Cost

**Lemma 9.** A sweep costs $\Theta(n + s)$ for $n$ free vertices and $s$ springs, and the memory is $\Theta(n + s)$.

*Proof.* The update of vertex $i$ costs $O(1 + |\mathcal F_i|)$ for the force, the $2 \times 2$ Hessian and the solve; the line search multiplies this by at most a constant number of trials. Summing over the vertices gives $\Theta(n + \sum_i|\mathcal F_i|) = \Theta(n + s)$, because each spring touches two vertices. The adjacency lists and the colors take $\Theta(n + s)$ memory. $\square$
