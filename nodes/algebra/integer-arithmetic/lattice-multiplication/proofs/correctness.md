---
title: Lattice multiplication computes the exact product
proves: [correctness, termination]
status: full
---

Let $\beta \ge 2$, and let $a = [a_0, \ldots, a_{m-1}]$ and $b = [b_0, \ldots, b_{n-1}]$ be digit arrays with $0 \le a_i, b_j \le \beta - 1$, of values $A = \sum_i a_i\beta^i$ and $B = \sum_j b_j\beta^j$.

**Theorem.** LATTICE-MUL$(a, b)$ terminates and returns digits $c_0, \ldots, c_{m+n-1}$ in $[0, \beta - 1]$ with $\sum_k c_k\beta^k = AB$.

*Proof.* All loops have fixed bounds, so the procedure terminates.

*Step 1: the grid.* Line L2 uses division with remainder by $\beta$, so $a_i b_j = h_{ij}\beta + l_{ij}$ with $0 \le l_{ij} \le \beta - 1$ and $h_{ij} \ge 0$.

*Step 2: the lanes.* After lines L3 to L5, for each $k$ with $0 \le k \le m + n - 1$,

$$s_k = \sum_{i + j = k} l_{ij} + \sum_{i + j = k - 1} h_{ij} ,$$

where the sums run over $0 \le i < m$ and $0 \le j < n$. The index $i + j + 1$ of line L5 is at most $(m - 1) + (n - 1) + 1 = m + n - 1$, so it is inside the array. Hence

$$\sum_{k=0}^{m+n-1} s_k\beta^k = \sum_{i,j} l_{ij}\beta^{i+j} + \sum_{i,j} h_{ij}\beta^{i+j+1} = \sum_{i,j} (h_{ij}\beta + l_{ij})\beta^{i+j} = \sum_{i,j} a_i b_j \beta^{i+j} = AB .$$

*Step 3: the carry pass.* We show the invariant

> **(C)** before the step with index $k$ of line L7, $c_0, \ldots, c_{k-1}$ are digits in $[0, \beta - 1]$, $\text{carry} \ge 0$, and $\sum_{k'<k} c_{k'}\beta^{k'} + \text{carry}\cdot\beta^k = \sum_{k'<k} s_{k'}\beta^{k'}$.

For $k = 0$, line L6 sets carry to 0, and both sides are 0. In the step with index $k$, line L8 forms $t = s_k + \text{carry} \ge 0$, and line L9 writes $t = c_k + \text{carry}'\beta$ with $0 \le c_k \le \beta - 1$ and $\text{carry}' = \lfloor t/\beta \rfloor \ge 0$. Then

$$\sum_{k' \le k} c_{k'}\beta^{k'} + \text{carry}'\beta^{k+1} = \sum_{k'<k} c_{k'}\beta^{k'} + t\beta^k = \sum_{k'<k} c_{k'}\beta^{k'} + \text{carry}\cdot\beta^k + s_k\beta^k = \sum_{k' \le k} s_{k'}\beta^{k'} ,$$

by (C) for $k$. So (C) holds for $k + 1$.

*Step 4: the end.* After the step with $k = m + n - 1$, (C) and Step 2 give $\sum_{k} c_k\beta^k + \text{carry}\cdot\beta^{m+n} = AB$. Since $AB \le (\beta^m - 1)(\beta^n - 1) < \beta^{m+n}$ and $\sum_k c_k \beta^k \ge 0$, the final carry is less than 1, so it is 0, and $\sum_k c_k\beta^k = AB$. $\blacksquare$

**The size of the lane sums.** Each $l_{ij} \le \beta - 1$, and each $h_{ij} \le \lfloor (\beta - 1)^2/\beta \rfloor = \beta - 2$, because $(\beta - 1)^2 = (\beta - 2)\beta + 1$. Lane $k$ has at most $\min(m, n)$ cells with $i + j = k$, and at most $\min(m, n)$ with $i + j = k - 1$, since for fixed $k$ the index $i$ determines $j$, and both $i < m$ and $j < n$. So $s_k \le 2\min(m, n)(\beta - 1)$. Write $p = \min(m, n)$. If $\text{carry} \le 2p - 1$ before a step, then $t \le 2p(\beta - 1) + 2p - 1 = 2p\beta - 1$, and $\text{carry}' = \lfloor t/\beta \rfloor \le 2p - 1$. Since the first carry is 0, every carry is at most $2p - 1$, which gives the bound on the extra bits stated on the page.
