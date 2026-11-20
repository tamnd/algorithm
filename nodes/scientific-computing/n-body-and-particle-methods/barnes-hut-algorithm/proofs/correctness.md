---
title: The Barnes-Hut walk counts each body once, is exact for theta = 0, and has a bounded monopole error for small theta
proves: [correctness]
status: full
---

We use exact real arithmetic. The bodies have masses $m_j > 0$ and positions $\mathbf{x}_j \in \mathbb{R}^D$. A cell $C$ is a closed cube of side $s_C$; $B(C)$ is the set of bodies stored in the leaves below $C$, $M_C = \sum_{j \in B(C)} m_j$ and $\mathbf{z}_C = \frac{1}{M_C} \sum_{j \in B(C)} m_j \mathbf{x}_j$.

**Lemma 1 (the tree is a partition).** After lines L1 to L5, each body is stored in exactly one leaf, and the leaf cube contains the body. For each internal cell $C$, the sets $B(C')$ of its children $C'$ are disjoint and their union is $B(C)$.

*Proof.* Line L1 makes a cube that holds all bodies. An insertion at a cell either stores the body in a leaf at line L3, or passes it to exactly one child at line L5, chosen by comparing each coordinate with the middle of the cell, so the child cube contains the body. Line L4 moves the old bodies of a leaf to children by the same rule, and removes them from the leaf. So at each moment, each inserted body is in exactly one leaf, and on the path from the root to that leaf each cell contains it. The second statement follows, because the children of a cell are the only cells below it on these paths. $\square$

The depth limit of line L3 makes each insertion stop: a path has at most $\text{MAX-DEPTH} + 1$ cells. Bodies at the same point end in one leaf at the depth limit.

**Lemma 2 (the summaries).** After line L6, each cell has the mass $M_C$ and the center of mass $\mathbf{z}_C$ of $B(C)$.

*Proof.* By induction from the leaves up. A leaf sums its own bodies. An internal cell sums the masses of its children and takes the mass-weighted mean of their centers; by Lemma 1 and the induction hypothesis this is $\sum_{C'} \sum_{j \in B(C')} m_j = M_C$, and similarly for the first moment. $\square$

**Lemma 3 (each body is counted once).** For a target $\mathbf{x}_i$, let $\mathcal{A}$ be the set of cells accepted at line L8 and $\mathcal{L}$ the set of leaves reached at line L7. The sets $B(C)$ for $C \in \mathcal{A} \cup \mathcal{L}$ are pairwise disjoint, and their union is the set of all bodies.

*Proof.* The walk starts with the root. Each cell taken from the stack is either a leaf (line L7), accepted (line L8), or replaced by its children (line L9). By Lemma 1, replacing $C$ by its children keeps the sets $B$ of the stack and of the finished cells a partition of all bodies. The walk ends because the tree is finite, and then all cells are finished. $\square$

**Theorem 1 (exactness for theta = 0).** With $\theta = 0$ the walk returns the direct sum $\sum_{j \ne i} G m_j (\mathbf{x}_j - \mathbf{x}_i) / (|\mathbf{x}_j - \mathbf{x}_i|^2 + \epsilon^2)^{3/2}$.

*Proof.* The test $s_C < \theta d$ is false for $\theta = 0$, so no cell is accepted, $\mathcal{A}$ is empty, and by Lemma 3 every body is reached in exactly one leaf. Line L7 adds the pair term of each body $j \ne i$ of the leaf. $\square$

**Theorem 2 (monopole error of an accepted cell).** Let $C$ be a cell, $\mathbf{x}$ a point, $d = |\mathbf{x} - \mathbf{z}_C|$ and $b = \max_{j \in B(C)} |\mathbf{x}_j - \mathbf{z}_C|$, with $d > b$. Then, for $\epsilon = 0$,

$$\left| -G \sum_{j \in B(C)} \frac{m_j}{|\mathbf{x} - \mathbf{x}_j|} + \frac{G M_C}{d} \right| \le \frac{G M_C\, b^2}{d^2 (d - b)}.$$

*Proof.* Put the origin at $\mathbf{z}_C$ and let $\mathbf{y}_j = \mathbf{x}_j - \mathbf{z}_C$, so $|\mathbf{y}_j| \le b < d$. The Legendre series $\frac{1}{|\mathbf{x} - \mathbf{y}|} = \sum_{l \ge 0} \frac{|\mathbf{y}|^l}{d^{l+1}} P_l(\cos\gamma)$ converges absolutely. The term $l = 0$ summed over $B(C)$ is $M_C / d$. The term $l = 1$ is $\frac{1}{d^3} \mathbf{x} \cdot \sum_j m_j \mathbf{y}_j = 0$, because $\mathbf{z}_C$ is the center of mass. With $|P_l| \le 1$ and $m_j > 0$, the rest is at most $\sum_j m_j \sum_{l \ge 2} b^l / d^{l+1} = M_C \frac{b^2}{d^2 (d - b)}$. $\square$

**Corollary (a bound in terms of theta).** In dimension 3, the bodies of $C$ and their center of mass lie in the cube of $C$, so $b \le \sqrt{3}\, s_C$. If line L8 accepts $C$, then $s_C < \theta d$, so $b / d < \sqrt{3}\, \theta$. If $\sqrt{3}\, \theta < 1$, the relative error of the potential of the cell is less than $\frac{(\sqrt{3}\,\theta)^2}{1 - \sqrt{3}\,\theta}$; for $\theta = 0.3$ this is $0.56$, a loose worst case, and the error of a typical cell is much smaller. For $\theta \ge 1/\sqrt{3}$ there is no such bound in terms of $\theta$ alone: the bodies of the cell can be arbitrarily close to the target. The test "the target is not inside $C$" of line L8 removes the worst of these cases but does not give a bound. $\square$

**Cost of the walk.** Each cell is taken from the stack at most once per target, so one walk costs at most the number of cells times $2^D$. For bodies that are not all at one point, the depth limit bounds the number of cells by $N \cdot (\text{MAX-DEPTH} + 1)$. The $O(N \log N)$ cost for well-spread distributions is an estimate, discussed on the main page.
