---
title: The Kahn order of the upwind graph solves every cell with known inflow, a cycle is detected exactly, the converged sweep balances and stays positive, and a grid has i plus j plus 1 wavefront levels
proves: [correctness]
status: full
---

We assume exact arithmetic. The mesh, the faces $(a, b, n, A)$ and the lines L1 to L7 are those of the page. Every cell has a volume $V_c > 0$ and $\Sigma_{t,c} > 0$. For a face with the unit normal $n$ out of cell $a$, write $g = (\Omega\cdot n)A$. The upwind graph $G_\Omega$ has an edge $a \to b$ when $g > 0$ and an edge $b \to a$ when $g < 0$, for every interior face. A face with $g = 0$ gives no edge. The cell equation of the step scheme is
$$\Sigma_{t,c}V_c\,\psi_c + \sum_{f \in \mathrm{out}(c)} g_f\,\psi_c - \sum_{f \in \mathrm{in}(c)} |g_f|\,\psi_{\mathrm{up}(f)} = q_c V_c, \tag{1}$$
where $g_f$ is taken with the normal out of $c$, $\mathrm{out}(c)$ are the faces of $c$ with $g_f > 0$, $\mathrm{in}(c)$ those with $g_f < 0$, and $\psi_{\mathrm{up}(f)}$ is the value of the cell on the other side, or the given inflow value on a boundary face.

**Lemma 1 (the order).** Lines L1 to L6 output a cell only after all its upstream cells in $G_\Omega$. They output every cell if and only if $G_\Omega$ has no directed cycle. Otherwise the cells they do not output are exactly the cells that lie on a cycle or can be reached from one.

*Proof.* Line L2 sets $\mathrm{indeg}(c)$ to the number of edges into $c$. Line L6 lowers it by one when an upstream cell is output, and a cell enters the queue only when it reaches 0, that is after all its upstream cells. This is Kahn's algorithm for [topological sort](/topological-sort/).

If $G_\Omega$ has a cycle, no cell of the cycle can be output first among the cells of the cycle, because its predecessor on the cycle must come before it. So no cell of a cycle is output, and by the first part no cell that can be reached from one is output. Conversely, let $c$ be a cell that is not output. Then at the end $\mathrm{indeg}(c) > 0$, so $c$ has an upstream cell $c'$ that is not output. Repeat with $c'$. The mesh is finite, so the chain $c \leftarrow c' \leftarrow c'' \leftarrow \cdots$ repeats a cell, which gives a cycle from which $c$ can be reached. $\square$

So line L7 raises an error exactly when the mesh has a cycle for $\Omega$, and the implementation names the blocked cells.

**Theorem 2 (one sweep solves the direction).** If $G_\Omega$ has no cycle, the system (1) for all cells has exactly one solution, and line L5 computes it.

*Proof.* When line L5 solves cell $c$, every term $\psi_{\mathrm{up}(f)}$ with $f \in \mathrm{in}(c)$ is known: it is boundary data, or the value of an upstream cell, which Lemma 1 has output earlier. Then (1) is one linear equation in $\psi_c$ with the coefficient $\Sigma_{t,c}V_c + \sum_{\mathrm{out}(c)} g_f > 0$, so $\psi_c$ is unique and line L5 gives it. Ordered in the sweep order, the matrix of (1) is lower triangular with a positive diagonal, so the whole system has exactly one solution. $\square$

**Theorem 3 (balance).** The values of Theorem 2 satisfy
$$\sum_c \Sigma_{t,c}V_c\,\psi_c + J^{\mathrm{out}} = \sum_c q_c V_c + J^{\mathrm{in}},$$
where $J^{\mathrm{out}} = \sum g_f \psi_c$ over the boundary faces with $g_f > 0$ and $J^{\mathrm{in}} = \sum |g_f|\,\psi_{\mathrm{in}}$ over the boundary faces with $g_f < 0$.

*Proof.* Add (1) over all cells. An interior face $f$ with $g_f \ne 0$ appears in two equations: with $+|g_f|\psi_{\mathrm{up}}$ in the equation of its upstream cell, where it is an out face, and with $-|g_f|\psi_{\mathrm{up}}$ in the equation of its downstream cell, where it is an in face. These cancel. What remains are the boundary faces. $\square$

**Theorem 4 (positivity).** If $q_c \ge 0$ for every cell and the inflow values are not negative, then every $\psi_c \ge 0$. If moreover each cell is closed, $\sum_{f} n_f A_f = 0$, then a constant $\psi_0$ with $q = \Sigma_t\psi_0$ and the inflow $\psi_0$ is reproduced exactly.

*Proof.* By induction in the sweep order, the numerator of line L5 is a sum of terms that are not negative, and the denominator is positive. For the second part, closure gives $\sum_{\mathrm{out}(c)} g_f = \sum_{\mathrm{in}(c)} |g_f|$, so $\psi_c = \psi_0$ satisfies (1) in every cell, and Theorem 2 makes it the solution. $\square$

**Theorem 5 (wavefronts on a grid).** On an $n_x$ by $n_y$ grid of rectangles with $\Omega_x > 0$ and $\Omega_y > 0$, the level of cell $(i, j)$, counted from 0, is $i + j + 1$, so there are $n_x + n_y - 1$ levels. Cells with the same level have no edge between them. If $\Omega_y = 0$, there are $n_x$ levels.

*Proof.* The edges of $G_\Omega$ are $(i, j) \to (i + 1, j)$ and $(i, j) \to (i, j + 1)$. Cell $(0, 0)$ has no upstream cell and level 1. By induction on $i + j$, the upstream cells of $(i, j)$ are $(i - 1, j)$ and $(i, j - 1)$ when they exist, both with level $i + j$, so $(i, j)$ has level $i + j + 1$. Every edge raises the level by exactly 1, so it never joins two cells of one level. If $\Omega_y = 0$, the faces between rows have $g = 0$, only the edges in $x$ remain, and the level of $(i, j)$ is $i + 1$. $\square$

So the cells of one level can be solved at the same time, and a grid sweep has at most $\min(n_x, n_y)$ cells at the same level.

**Theorem 6 (the diamond difference sweep on a grid).** For a direction $(\mu, \eta)$ with $\mu \ne 0$ and $\eta \ne 0$, and every cell $(i, j)$, the equations
$$|\mu|\frac{\psi_R - \psi_L}{\Delta x_i} + |\eta|\frac{\psi_T - \psi_B}{\Delta y_j} + \Sigma_t\psi_c = q, \qquad \psi_c = \frac{\psi_L + \psi_R}{2} = \frac{\psi_B + \psi_T}{2},$$
with the incoming values $\psi_L$ and $\psi_B$ known, have exactly one solution, $\psi_c = (q + a\psi_L + b\psi_B)/(\Sigma_t + a + b)$ with $a = 2|\mu|/\Delta x_i$ and $b = 2|\eta|/\Delta y_j$, and $\psi_R = 2\psi_c - \psi_L$, $\psi_T = 2\psi_c - \psi_B$. The loop of the implementation, rows in the direction of $\eta$ and cells in a row in the direction of $\mu$, solves all cells.

*Proof.* The two diamond relations give $\psi_R - \psi_L = 2(\psi_c - \psi_L)$ and $\psi_T - \psi_B = 2(\psi_c - \psi_B)$. Put them into the balance: $(\Sigma_t + a + b)\psi_c = q + a\psi_L + b\psi_B$, with a positive factor on the left. The row by row order is a topological order of the grid graph of Theorem 5, so the argument of Theorem 2 applies. $\square$

With $q = 0$ and $\psi_L = \psi_B = 1$, both outgoing values are $2\psi_c - 1 = (a + b - \Sigma_t)/(\Sigma_t + a + b)$, which is negative when $\Sigma_t > a + b$. The page shows the case $\mu = \eta = 0.1$, $\Delta x = \Delta y = 1$, $\Sigma_t = 1$, which gives $-3/7$.
