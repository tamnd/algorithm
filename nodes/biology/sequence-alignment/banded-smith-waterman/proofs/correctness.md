---
title: Banded Smith-Waterman returns an optimal in-band local alignment
proves: [correctness]
status: full
---

Let $x = x_1 \cdots x_m$, $y = y_1 \cdots y_n$, a scoring matrix $s$, gap parameters $d \ge e \ge 0$ and a band $lo \le hi$ be given. Call a cell $(i, j)$ with $0 \le i \le m$, $0 \le j \le n$ a *band cell* when $lo \le j - i \le hi$. Line numbers refer to the pseudocode on the algorithm page.

**Paths and scores.** A local alignment of $x_{i_0+1} \cdots x_i$ with $y_{j_0+1} \cdots y_j$ is a sequence of columns $c_1, \ldots, c_k$; it visits the cells $(i_0, j_0)$, then the cell reached after each column, ending at $(i, j)$. A pair column moves by $(1, 1)$, an X-column $(a, -)$ by $(1, 0)$ and a Y-column $(-, b)$ by $(0, 1)$. The alignment is *in the band* when all the cells it visits are band cells. As in the proof for the [Gotoh algorithm](/gotoh-algorithm/), give column $c_t$ the contribution

$$\kappa(c_t \mid c_{t-1}) = \begin{cases} s(a, b) & \text{if } c_t = (a, b) \text{ is a pair column}, \\ -e & \text{if } c_t \text{ and } c_{t-1} \text{ are both X-columns or both Y-columns}, \\ -d & \text{otherwise}, \end{cases}$$

where $c_0$ is a dummy pair column. Then $S(A) = \sum_t \kappa(c_t \mid c_{t-1})$ is the affine score: a gap of length $L$ gets $-d$ for its first column and $-e$ for the others, including a gap that opens the alignment.

**Classes.** For a band cell $(i, j)$ let $\mathcal{A}(i, j)$ be the set of in-band local alignments that end at $(i, j)$. It contains the empty alignment that starts and ends at $(i, j)$, of score $0$. Split the nonempty ones by their last column into $\mathcal{M}(i, j)$, $\mathcal{X}(i, j)$ and $\mathcal{Y}(i, j)$, and let $M^*, X^*, Y^*$ be their maximum scores, with $\max \emptyset = -\infty$. Then $H^*(i, j) = \max\{0, M^*(i, j), X^*(i, j), Y^*(i, j)\}$ is the best score in $\mathcal{A}(i, j)$. For a cell that is not a band cell, or lies outside the grid, set all four values to $-\infty$.

**Lemma 1 (recurrences).** For every band cell $(i, j)$,

$$M^*(i, j) = H^*(i-1, j-1) + s(x_i, y_j), \quad X^*(i, j) = \max\{H^*(i-1, j) - d,\ X^*(i-1, j) - e\}, \quad Y^*(i, j) = \max\{H^*(i, j-1) - d,\ Y^*(i, j-1) - e\}.$$

*Proof.* Take $\mathcal{X}(i, j)$. Removing the last column $(x_i, -)$ of an alignment in it leaves an alignment that ends at $(i-1, j)$ and visits only band cells, so it lies in $\mathcal{A}(i-1, j)$. Conversely, appending $(x_i, -)$ to an alignment in $\mathcal{A}(i-1, j)$ gives an alignment in $\mathcal{X}(i, j)$, since $(i, j)$ is a band cell. So removal is a bijection. If $(i-1, j)$ is not a band cell or not in the grid, both sides are $-\infty$. Otherwise the removed column contributes $-e$ when the rest $A'$ ends with an X-column and $-d$ when $A'$ ends with a pair or a Y-column or is empty, so

$$X^*(i, j) = R = \max\bigl\{X^*(i-1, j) - e,\ M^*(i-1, j) - d,\ Y^*(i-1, j) - d,\ 0 - d\bigr\}.$$

The right side of the claim is $R' = \max\{H^*(i-1, j) - d,\ X^*(i-1, j) - e\} = \max\{R,\ X^*(i-1, j) - d\}$. As $d \ge e$, $X^*(i-1, j) - d \le X^*(i-1, j) - e \le R$, so $R' = R$. The $Y$ equation is symmetric. For $M^*$ the removed pair column contributes $s(x_i, y_j)$ whatever precedes it, and $(i-1, j-1)$ is on the same diagonal as $(i, j)$, so it is a band cell whenever it is in the grid. $\square$

**Lemma 2 (the tables).** After lines L1 to L8, every band cell holds $M = M^*$, $X = X^*$, $Y = Y^*$ and $H = H^*$, and $best = \max H^*$ over the band cells, attained at $(bi, bj)$.

*Proof.* Lines L2 and L3 visit exactly the band cells, in row-major order. The neighbours $(i-1, j-1)$, $(i-1, j)$ and $(i, j-1)$ come earlier in this order, so by induction they hold their true values if they are band cells, and $-\infty$ otherwise, as line L1 requires; this is also $-\infty$ in Lemma 1. So lines L4 to L6 compute the right sides of Lemma 1; when line L4 is skipped, $i = 0$ or $j = 0$, and $M$ keeps $-\infty = M^*$. Line L7 is the definition of $H^*$. Line L8 keeps the first maximum in visiting order, starting from $0$. $\square$

Every in-band local alignment lies in $\mathcal{A}(i, j)$ for its end cell, so $best$ is the optimal in-band local score. If $best = 0$, line L9 returns the empty alignment, which is optimal. Assume from now on $best > 0$.

**Lemma 3 (one traceback step).** Consider a pass of the loop of line L10 that starts at band cell $(i, j)$ with $state$ $q$, and let $T$ be the table named by $q$ ($T = H$ when $q$ is "any"). Assume $T[i][j]$ is finite, that $H[i][j] > 0$ if $q$ is "any", and, if $q$ is "any" and the column prepended just before is an X-column (a Y-column), that $X[i][j] < H[i][j]$ (that $Y[i][j] < H[i][j]$). Then the pass prepends one column $c$, moves to a cell $(i', j')$ with state $q'$ and table $T'$, and:

1. $T'[i'][j']$ is finite, so $(i', j')$ is a band cell;
2. $T[i][j] = T'[i'][j'] + \kappa(c \mid c')$, where $c'$ is the column the next pass prepends, or a dummy pair column if the next pass exits;
3. the assumption holds again at $(i', j', q')$, unless $q'$ is "any" and $H[i'][j'] = 0$.

*Proof.* If $q$ is "any", then $H[i][j] > 0$, so the $0$ of line L7 is not the maximum, and line L11 picks a table among $M, X, Y$ with value $H[i][j]$. By the assumption it does not pick $X$ right after an X-column, nor $Y$ right after a Y-column.

*Pair step, line L12.* $M[i][j]$ is finite, so $i, j \ge 1$ and $M[i][j] = H[i-1][j-1] + s(x_i, y_j)$ by line L4. The new state is "any", $\kappa(c \mid c') = s(x_i, y_j)$ for every $c'$, and the extra assumption is vacuous because $c$ is a pair column.

*X step, line L13.* $X[i][j]$ is finite, so line L5 gives $X[i][j] = \max\{H[i-1][j] - d, X[i-1][j] - e\}$ with a finite value. If $X[i][j] = X[i-1][j] - e$, the new state is $X$, the next pass prepends an X-column (it cannot exit, since exits happen only in state "any"), and $\kappa(c \mid c') = -e$. Otherwise $X[i][j] = H[i-1][j] - d > X[i-1][j] - e \ge X[i-1][j] - d$, so $X[i-1][j] < H[i-1][j]$, the new state is "any", and the next column is either absent or not an X-column, so $\kappa(c \mid c') = -d$. In both cases part 2 holds, and the followed value is finite as the difference of finite numbers. Only band cells hold finite values, so part 1 holds.

*Y step, line L14*, is symmetric. $\square$

**Theorem.** If $best > 0$, the algorithm returns $best$ and an in-band local alignment of score $best$ that ends at $(bi, bj)$.

*Proof.* Line L9 starts at $(bi, bj)$ in state "any" with $H = best > 0$ and no column prepended, so Lemma 3 applies. By part 3, it applies at every later pass until the loop exits, which happens exactly in state "any" at a cell with $H = 0$. Each pass decreases $i + j$, and the followed value stays finite, so the walk cannot leave the grid: at $(0, 0)$ the tables $M, X, Y$ hold $-\infty$ and $H$ holds $0$. So the loop exits at some band cell $(i_0, j_0)$ with $H[i_0][j_0] = 0$. Let $c_1, \ldots, c_k$ be the prepended columns from left to right. Summing part 2 over the passes, the values telescope:

$$best = H[i_0][j_0] + \sum_{t=1}^{k} \kappa(c_t \mid c_{t-1}) = 0 + S(c_1 \cdots c_k).$$

The columns spell $x_{i_0+1} \cdots x_{bi}$ over $y_{j_0+1} \cdots y_{bj}$, with no column of two spaces, and every visited cell is a band cell by part 1, so the result is an in-band local alignment of score $best$. By Lemma 2 this is optimal. $\square$

**What the band changes.** Only two points differ from the Gotoh proof: the classes contain only in-band alignments, which is why out-of-band neighbours must read $-\infty$ and not $0$ or a stale value, and each cell has the empty alignment, which gives the $0$ in line L7 and the exit test in line L11.
