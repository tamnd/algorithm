---
title: The occupancy grid operations keep the invariant, and the traversal returns exactly the cells a segment crosses
proves: [correctness, termination]
status: full
---

We use the names of the pseudocode. The grid has the origin $(o_x, o_y)$, the cell side $s > 0$ and $W \times H$ cells. Cell $(i, j)$ is the half-open square $Q_{ij} = [o_x + i s, o_x + (i + 1) s) \times [o_y + j s, o_y + (j + 1) s)$, and its open square is $Q^\circ_{ij} = (o_x + i s, o_x + (i + 1) s) \times (o_y + j s, o_y + (j + 1) s)$. These definitions make sense for all integers $i, j$; the grid is the part with $0 \le i < W$ and $0 \le j < H$. The invariant (G) asks: (1) the array $l$ has $W H$ entries; (2) each entry is in $[l_{\min}, l_{\max}]$; (3) the entry of cell $(i, j)$ is the value obtained from $l_0$ by the updates of that cell, in order, each by line L4. We assume exact arithmetic; the remark at the end treats rounding.

**Lemma 1 (index).** For a real $x$, the integer $i = \lfloor (x - o_x)/s \rfloor$ is the only integer with $o_x + i s \le x < o_x + (i + 1) s$. *Proof.* The floor $i$ of $u = (x - o_x)/s$ is the only integer with $i \le u < i + 1$; multiply by $s > 0$ and add $o_x$. $\square$

So line L1 gives the only cell $(i, j)$ of the infinite lattice with $(x, y) \in Q_{ij}$, and line L2 returns it exactly when it is a cell of the grid. INDEX changes nothing.

**Lemma 2 (update).** UPDATE keeps (G). *Proof.* Line L3 maps $(i, j)$ with $0 \le i < W$, $0 \le j < H$ to $k = j W + i$, and this map is a bijection onto $\{0, \ldots, W H - 1\}$: $i = k \bmod W$ and $j = \lfloor k / W \rfloor$. So line L4 changes the entry of cell $(i, j)$ and no other entry, and part 1 and part 3 for the other cells hold. Line L4 applies the update rule to the old value, so part 3 holds for cell $(i, j)$, and the clamp puts the new value in $[l_{\min}, l_{\max}]$, so part 2 holds. $\square$

Without clamping ($l_{\min} = -\infty$, $l_{\max} = +\infty$), induction on the number of updates with Lemma 2 gives the closed form $l_{ij} = l_0 + \sum_k (l_k - l_0)$ over the updates $l_k$ of cell $(i, j)$. PROBABILITY returns $1 - 1/(1 + e^{l}) = e^l / (1 + e^l)$, which is the inverse of $p \mapsto \log(p / (1 - p))$, so it returns the probability that the log odds encode.

**The traversal.** Let $a \ne b$ be two points, $d = b - a$ and $p(t) = a + t d$ for $t \in [0, 1]$. Let $(i_a, j_a)$ and $(i_b, j_b)$ be their cells. Call the segment *generic* if no $p(t)$ with $t \in [0, 1]$ lies on a vertical and a horizontal cell edge at once (it passes through no corner), and $a$ and $b$ lie on no cell edge.

**Lemma 3 (crossings).** Let $d_x > 0$. The times $t \in (0, 1]$ at which $p(t)$ lies on a vertical edge $x = o_x + k s$ are $\tau_k = (o_x + k s - a_x) / d_x$ for $k = i_a + 1, \ldots, i_b$, and there are $i_b - i_a$ of them, in increasing order. For $d_x < 0$ the same holds with $k = i_a, i_a - 1, \ldots, i_b + 1$, and there are $i_a - i_b$ of them. For $d_x = 0$ there is none, and $i_a = i_b$. *Proof.* For $d_x > 0$, $x(t)$ increases from $a_x$ to $b_x$, so it meets the edge $o_x + k s$ exactly when $a_x < o_x + k s \le b_x$. By Lemma 1, $o_x + i_a s \le a_x < o_x + (i_a + 1) s$ and the same for $b$, so these are the $k$ with $i_a + 1 \le k \le i_b$. The case $d_x < 0$ is symmetric (in a generic segment $a$ is on no edge, so the edge $o_x + i_a s < a_x$ is met), and $d_x = 0$ is clear. $\square$

**Claim.** For a generic segment, CELLS-ON-SEGMENT ends after $n = |i_b - i_a| + |j_b - j_a|$ steps, returns $n + 1$ distinct cells $c_0, \ldots, c_n$ with $c_0 = (i_a, j_a)$ and $c_n = (i_b, j_b)$, each step moves to a cell that shares an edge with the previous one, and $\{c_0, \ldots, c_n\}$ is exactly the set of cells whose open square meets the segment.

*Proof.* By Lemma 3, the $|i_b - i_a|$ vertical crossing times and the $|j_b - j_a|$ horizontal crossing times are all in $(0, 1)$ (generic: $b$ is on no edge), and no vertical crossing time equals a horizontal one (no corner). Merge them into one increasing list $0 < \sigma_1 < \cdots < \sigma_n < 1$, and set $\sigma_0 = 0$, $\sigma_{n+1} = 1$.

On each open interval $(\sigma_m, \sigma_{m+1})$, $p(t)$ is on no edge, so it stays in one open square $Q^\circ_{c}$; call this cell $e_m$. At $\sigma_{m+1}$ the point crosses one edge, vertical or horizontal, so $e_{m+1}$ differs from $e_m$ by $\pm 1$ in one index: by $\operatorname{sign}(d_x)$ in $i$ at a vertical crossing, and by $\operatorname{sign}(d_y)$ in $j$ at a horizontal one. Also $e_0 = (i_a, j_a)$, since $a$ lies in the interior of its cell.

Invariant of the loop, before step $m + 1$ (for $m = 0, \ldots, n$): the current cell is $(i, j) = e_m$, the cells $e_0, \ldots, e_m$ have been output, $t_x$ is the first vertical crossing time after $\sigma_m$ (or $+\infty$ if none is left), and $t_y$ is the first horizontal one.

*Initialization.* Line L6 sets $(i, j) = (i_a, j_a) = e_0$, line L8 outputs it, and line L7 sets $t_x$ to the time of the next vertical edge in the direction of $d_x$, which is $\tau_{i_a + 1}$ (or $\tau_{i_a}$ for $d_x < 0$), the first vertical crossing; the same for $t_y$.

*Maintenance.* The next crossing time $\sigma_{m+1}$ is $\min(t_x, t_y)$. If $i = i_b$, all vertical crossings are done, because each of them moves $i$ one step from $i_a$ towards $i_b$; then the next crossing is horizontal. If $j = j_b$, it is vertical. If neither holds, both kinds remain, and the smaller of $t_x$ and $t_y$ is the next one; they are not equal (no corner). So line L10 or line L11 makes the same move as the crossing at $\sigma_{m+1}$, and $(i, j)$ becomes $e_{m+1}$. Consecutive crossing times of one kind differ by exactly $s / |d_x|$ (or $s / |d_y|$), because consecutive edges are $s$ apart, so adding $\Delta t_x$ (or $\Delta t_y$) gives the next crossing time of that kind. Line L12 outputs $e_{m+1}$.

*Termination.* The loop runs exactly $n$ times, and then $(i, j) = e_n$, the cell of the last interval $(\sigma_n, 1)$, which holds the points just before $b$; since $b$ is in the interior of its cell, $e_n = (i_b, j_b)$.

Each step changes one index by $\pm 1$ in a fixed direction per axis, so the indices are monotone, and no cell is output twice. Each output cell $e_m$ contains $p(t)$ for $t$ in the open interval $(\sigma_m, \sigma_{m+1})$, so its open square meets the segment. Conversely, if $Q^\circ_c$ meets the segment at $p(t)$, then $t$ is no crossing time (a point of an open square is on no edge), so $t$ lies in some interval $(\sigma_m, \sigma_{m+1})$, or $t \in \{0, 1\}$ inside $e_0$ or $e_n$, and $c = e_m$. $\square$

**INSERT-RAY.** It calls UPDATE on cells of the grid only (the tests of lines L13 and L14), so by Lemma 2 it keeps (G). By the claim, it updates each cell that the beam crosses once: with $l_{\mathrm{free}}$ for the cells before the end cell, and with $l_{\mathrm{occ}}$ or $l_{\mathrm{free}}$ for the cell of the end point.

**Non-generic segments and rounding.** If the segment passes through a corner, then at that time $t_x = t_y$, and line L10 steps in $y$ first; the extra cell meets the segment only at the corner. All other parts of the proof hold. In floating-point arithmetic, $t_x$ and $t_y$ carry rounding errors, so for two crossings that are very close, the order can swap and the output can contain a corner cell instead of its neighbor. The tests $j = j_b$ and $i \ne i_b$ of line L10 still force exactly $|i_b - i_a|$ steps in $i$ and $|j_b - j_a|$ steps in $j$, so the output always starts at the cell of $a$, ends at the cell of $b$, moves by edge neighbors, and the loop always stops after $n$ steps. $\blacksquare$
