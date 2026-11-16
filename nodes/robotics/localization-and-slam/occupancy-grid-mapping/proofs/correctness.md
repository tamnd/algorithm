---
title: The log odds update gives the posterior of each cell under the independence assumption
proves: [correctness]
status: full
---

**Setting.** Fix one cell $m_i$ of the grid. It is occupied ($m_i = 1$) or free ($m_i = 0$), and its prior is $p(m_i = 1) = p_0$ with $0 < p_0 < 1$. The poses $x_1, \ldots, x_T$ are known and fixed in advance, and $z_t$ is the scan taken at $x_t$. Write $\operatorname{odds}(p) = p / (1 - p)$ and $\operatorname{lo}(p) = \log \operatorname{odds}(p)$, so that $l_0 = \operatorname{lo}(p_0)$. Write $\mathrm{ism}_t = $ INVERSE-SENSOR-MODEL$(m_i, x_t, z_t)$.

**Assumptions.**

- (I) Given the state of the cell and the poses, a scan is independent of the earlier scans: $p(z_t \mid m_i, z_{1:t-1}, x_{1:t}) = p(z_t \mid m_i, x_t)$.
- (S) The inverse model gives the log odds of the posterior of the cell from one scan: $\mathrm{ism}_t = \operatorname{lo}(p(m_i = 1 \mid z_t, x_t))$, and this probability is in $(0, 1)$.
- (K) A pose alone carries no information about the map: $p(m_i \mid x_t) = p(m_i)$ and $p(m_i \mid z_{1:t-1}, x_{1:t}) = p(m_i \mid z_{1:t-1}, x_{1:t-1})$. This holds because the poses are fixed in advance and do not depend on the map.

**Claim.** Let $l_{0,i} = l_0$, and let $l_{t,i}$ be the value of the cell after OCCUPANCY-GRID-MAPPING has processed $z_1, \ldots, z_t$. Then for every $t \ge 0$,

$$l_{t,i} = \operatorname{lo}\big(p(m_i = 1 \mid z_{1:t}, x_{1:t})\big) = l_0 + \sum_{s=1}^{t} (\mathrm{ism}_s - l_0).$$

*Proof.* First, the algorithm computes the sum on the right. Line L3 adds $\mathrm{ism}_t - l_0$ to $l_i$. Line L4 leaves $l_i$ unchanged, and line L2 sends a cell to line L4 only when it is outside the perceptual field, where the inverse model returns $l_0$ (line L9), so that the term $\mathrm{ism}_t - l_0$ is zero. So in both branches the value grows by $\mathrm{ism}_t - l_0$, and induction on $t$ gives the sum.

Next, the sum is the posterior log odds. By induction on $t$. For $t = 0$ both sides are $l_0$. Let $t \ge 1$. For $v \in \{0, 1\}$, Bayes' rule gives

$$p(m_i = v \mid z_{1:t}, x_{1:t}) = \frac{p(z_t \mid m_i = v, z_{1:t-1}, x_{1:t})\, p(m_i = v \mid z_{1:t-1}, x_{1:t})}{p(z_t \mid z_{1:t-1}, x_{1:t})}.$$

By (I) the first factor is $p(z_t \mid m_i = v, x_t)$, and by (K) the second is $p(m_i = v \mid z_{1:t-1}, x_{1:t-1})$. The denominator does not depend on $v$. Divide the equation for $v = 1$ by the equation for $v = 0$:

$$\operatorname{odds}_t = \frac{p(z_t \mid m_i = 1, x_t)}{p(z_t \mid m_i = 0, x_t)}\, \operatorname{odds}_{t-1},$$

where $\operatorname{odds}_t$ is the odds of $m_i = 1$ given $z_{1:t}, x_{1:t}$. Bayes' rule once more, with (K), gives $p(z_t \mid m_i = v, x_t) = p(m_i = v \mid z_t, x_t)\, p(z_t \mid x_t) / p(m_i = v)$. In the ratio, $p(z_t \mid x_t)$ cancels, and

$$\frac{p(z_t \mid m_i = 1, x_t)}{p(z_t \mid m_i = 0, x_t)} = \frac{\operatorname{odds}(p(m_i = 1 \mid z_t, x_t))}{\operatorname{odds}(p_0)}.$$

Take logarithms and use (S): $\log \operatorname{odds}_t = \log \operatorname{odds}_{t-1} + \mathrm{ism}_t - l_0$. With the induction hypothesis, $\log \operatorname{odds}_t = l_0 + \sum_{s=1}^{t} (\mathrm{ism}_s - l_0)$. All odds are positive and finite, because (S) puts every probability in $(0, 1)$, so each step is defined. $\square$

**The cells that the implementation skips.** The implementation calls the inverse model only for the cells that `Grid.cells_within` returns for the radius $z_{\max} + \alpha$. Let $a = (x - z_{\max} - \alpha - o_x)/s$, where $o_x$ is the grid origin and $s$ the cell side. A cell whose center $o_x + (i + 1/2) s$ is at least $x - z_{\max} - \alpha$ has $i \ge \lceil a - 1/2 \rceil \ge \lfloor a \rfloor$, and the same holds at the upper end and for $y$. So every cell whose center lies in the square of half side $z_{\max} + \alpha$ around the robot is visited. A cell that is not visited has its center outside this square, so its distance $r$ to the robot is more than $z_{\max}$, and line L9 returns $l_0$. Skipping it is the same as line L4.

**Order of the scans.** The sum does not depend on the order of its terms, so any order of the scans gives the same map. In floating-point arithmetic the results of two orders differ only by rounding.

**Termination.** One scan does one call of the inverse model for each of the at most $g$ cells, and each call ends after a search over $b$ beams. So a scan ends after $O(g b)$ steps.

**What the assumptions mean.** The claim is about one cell at a time. Assumption (I) is false for real scans: a reading depends on all cells along the beam, not only on $m_i$, so the readings are dependent given $m_i$ alone. The product of the per-cell results is therefore not the joint posterior over maps; it is the approximation of independent cells. Assumption (S) holds only for an inverse model that is learned from the forward model. The fixed values $0.7$ and $0.4$ of the implementation are rules of thumb, so the output is the result of a consistent update rule, with the exact sum above, and not a calibrated probability.
