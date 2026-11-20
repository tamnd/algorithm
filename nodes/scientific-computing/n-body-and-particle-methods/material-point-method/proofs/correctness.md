---
title: One MPM step moves all mass and momentum to the grid, conserves momentum without supports, reproduces rigid translation, and its interior force is the stress times a difference of cell volumes
proves: [correctness]
status: full
---

We use the pseudocode of the page and exact arithmetic, in 1D with the hats $N_i(x) = \max(0, 1 - |x - x_i| / \Delta x)$, $x_i = i \Delta x$. For a point at $x$ with $j = \lfloor x / \Delta x \rfloor$ and $w = x / \Delta x - j$, the code uses the two nodes $j$ and $j + 1$ with $N_j = 1 - w$, $N_{j+1} = w$, $N_j' = -1/\Delta x$ and $N_{j+1}' = 1/\Delta x$; all other nodes have $N_i(x) = N_i'(x) = 0$. So for every $x$:
$$\sum_i N_i(x) = 1, \qquad \sum_i N_i(x)\, x_i = x, \qquad \sum_i N_i'(x) = 0. \tag{P}$$
The first two follow from $(1 - w) + w = 1$ and $(1 - w) j \Delta x + w (j + 1) \Delta x = (j + w) \Delta x$.

We assume that every node $i$ with $N_i(x_p) \ne 0$ or $N_i'(x_p) \ne 0$ for some point $p$ has $m_i > 0$ after line L2. (This fails only when a point lies exactly on a node and the node to its right gets no mass from any point.)

**Claim 1 (transfer to the grid).** After line L2, $\sum_i m_i = \sum_p m_p$ and $\sum_i (mv)_i = \sum_p m_p v_p$.

*Proof.* Each point adds $N_i(x_p) m_p$ to $m_i$, and by (P) these add up over $i$ to $m_p$. The same holds for the momentum with $m_p v_p$ in place of $m_p$. $\square$

**Claim 2 (momentum).** If there are no fixed nodes, $\sum_p m_p v_p$ after line L7 equals $\sum_p m_p v_p$ before the step.

*Proof.* By (P), $\sum_i f_i = -\sum_p V_p \sigma_p \sum_i N_i'(x_p) = 0$. With no fixed nodes, line L5 gives $a_i = f_i / m_i$ for every node with mass. Line L7 changes the total by
$$h \sum_p m_p \sum_i N_i(x_p) a_i = h \sum_i a_i \sum_p N_i(x_p) m_p = h \sum_i a_i m_i = h \sum_i f_i = 0,$$
where the sum over $i$ runs over the nodes with mass, which by the assumption include every node where some $N_i(x_p) \ne 0$ or $f_i \ne 0$. $\square$

**Claim 3 (rigid translation).** If $v_p = u$ and $\sigma_p = 0$ for every point and no node is fixed, then after the step $v_p = u$, $x_p$ has moved by $h u$, and $F_p$ and $\sigma_p$ are unchanged.

*Proof.* Line L2 gives $(mv)_i = u\, m_i$, so line L4 gives $v_i = u$. Line L3 gives $f_i = 0$ since every $\sigma_p = 0$, so $v_i^{new} = u$ and $a_i = 0$. Line L7 leaves $v_p = u$. Line L8 adds $h \sum_i N_i(x_p) u = h u$ by (P). Line L9 gives $\dot\varepsilon_p = u \sum_i N_i'(x_p) = 0$ by (P), so lines L10 and L11 change nothing. $\square$

**Claim 4 (the interior force).** If every point has the same stress $\sigma$, then for every node $i$,
$$f_i = \frac{\sigma}{\Delta x} \Bigl(\sum_{p:\, x_p \in [x_i, x_{i+1})} V_p - \sum_{p:\, x_p \in [x_{i-1}, x_i)} V_p\Bigr).$$

*Proof.* A point in the cell $[x_{i-1}, x_i)$ has $j = i - 1$, so node $i$ is its right node with $N_i' = 1/\Delta x$, and it adds $-V_p \sigma / \Delta x$ to $f_i$. A point in $[x_i, x_{i+1})$ has $j = i$, so node $i$ is its left node with $N_i' = -1/\Delta x$, and it adds $+V_p \sigma / \Delta x$. No other point has $N_i'(x_p) \ne 0$. Adding up gives the formula. $\blacksquare$

So the internal force at an interior node is zero for a uniform stress exactly when the two cells next to the node hold the same particle volume, and it jumps by $\sigma V_p / \Delta x$ each time a point crosses the boundary of one of those cells.
