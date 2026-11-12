---
title: The Gotoh algorithm returns an optimal affine gap alignment
proves: [correctness]
status: full
---

Let $x = x_1 \cdots x_m$, $y = y_1 \cdots y_n$, a scoring matrix $s$ and $d \ge e \ge 0$ be given. For an alignment $A$ write $S(A)$ for its affine score: the sum of $s(a, b)$ over pair columns minus $d + (L-1)e$ for each gap of length $L$. Line numbers refer to the pseudocode on the algorithm page.

**Column costs.** Call a column $(a, b)$ with $a, b$ letters a *pair column*, a column $(a, -)$ an *X-column* and a column $(-, b)$ a *Y-column*. Give the $t$-th column $c_t$ of $A$ the contribution

$$\kappa(c_t \mid c_{t-1}) = \begin{cases} s(a, b) & \text{if } c_t = (a, b) \text{ is a pair column}, \\ -e & \text{if } c_t \text{ and } c_{t-1} \text{ are both X-columns or both Y-columns}, \\ -d & \text{otherwise}, \end{cases}$$

where $c_0$ is a dummy pair column. A gap of length $L$ gets $-d$ for its first column and $-e$ for each other one, so $S(A) = \sum_t \kappa(c_t \mid c_{t-1})$.

**Classes.** For $0 \le i \le m$, $0 \le j \le n$ let $\mathcal{A}(i, j)$ be the set of alignments of $x_1 \cdots x_i$ with $y_1 \cdots y_j$. Split the nonempty ones by their last column: $\mathcal{M}(i, j)$ ends with $(x_i, y_j)$, $\mathcal{X}(i, j)$ ends with $(x_i, -)$, $\mathcal{Y}(i, j)$ ends with $(-, y_j)$. Define

$$M^*(i, j) = \max_{A \in \mathcal{M}(i, j)} S(A), \quad X^*(i, j) = \max_{A \in \mathcal{X}(i, j)} S(A), \quad Y^*(i, j) = \max_{A \in \mathcal{Y}(i, j)} S(A),$$

with $\max \emptyset = -\infty$, and $H^*(i, j) = \max_{A \in \mathcal{A}(i, j)} S(A)$. So $H^*(0, 0) = 0$ (the empty alignment) and $H^*(i, j) = \max\{M^*, X^*, Y^*\}(i, j)$ otherwise.

**Lemma 1 (recurrences).** For $(i, j) \ne (0, 0)$,

$$M^*(i, j) = H^*(i-1, j-1) + s(x_i, y_j) \quad (i, j \ge 1),$$
$$X^*(i, j) = \max\{H^*(i-1, j) - d,\ X^*(i-1, j) - e\} \quad (i \ge 1),$$
$$Y^*(i, j) = \max\{H^*(i, j-1) - d,\ Y^*(i, j-1) - e\} \quad (j \ge 1),$$

and a class whose last column would need $x_0$ or $y_0$ is empty, with value $-\infty$.

*Proof.* Removing the last column is a bijection from $\mathcal{M}(i, j)$ onto $\mathcal{A}(i-1, j-1)$, and the removed pair column contributes $s(x_i, y_j)$ whatever precedes it. This gives the first equation.

Removing the last column is a bijection from $\mathcal{X}(i, j)$ onto $\mathcal{A}(i-1, j)$. The removed X-column contributes $-e$ if the remaining alignment $A'$ is in $\mathcal{X}(i-1, j)$ and $-d$ otherwise, that is, if $A'$ is in $\mathcal{M}(i-1, j)$ or $\mathcal{Y}(i-1, j)$ or is empty. So $X^*(i, j) = R$ with

$$R = \max\bigl\{ X^*(i-1, j) - e,\ M^*(i-1, j) - d,\ Y^*(i-1, j) - d,\ E - d \bigr\},$$

where $E = 0$ if $(i-1, j) = (0, 0)$ and $E = -\infty$ otherwise. The claimed value is $R' = \max\{H^*(i-1, j) - d, X^*(i-1, j) - e\}$. Since $H^*(i-1, j) = \max\{M^*, X^*, Y^*, E\}$ at $(i-1, j)$, we get $R' = \max\{R, X^*(i-1, j) - d\}$. As $d \ge e$, $X^*(i-1, j) - d \le X^*(i-1, j) - e \le R$, so $R' = R$. The third equation is symmetric. $\square$

**Lemma 2 (the tables).** After lines L1 to L8, $M[i][j] = M^*(i, j)$, $X[i][j] = X^*(i, j)$, $Y[i][j] = Y^*(i, j)$ and $H[i][j] = H^*(i, j)$ for all cells.

*Proof.* Induction over the cells in row-major order, the order of lines L2 and L3. Line L1 sets cell $(0, 0)$ correctly: $\mathcal{M}, \mathcal{X}, \mathcal{Y}$ are empty there and $H^* = 0$. For another cell, lines L5 to L7 evaluate the right sides of Lemma 1 from cells that come earlier in row-major order, which hold the true values by induction. An entry that line L5, L6 or L7 skips keeps $-\infty$ from line L1, the value of an empty class. Line L8 then gives $H^*$. $\square$

So $H[m][n] = H^*(m, n)$ is the optimal score, and it is finite because $x$ and $y$ always have an alignment.

**Lemma 3 (one traceback step).** Consider a pass of the loop of line L10 that starts at $(i, j)$ with $state$ $q$, and let $T$ be the table named by $q$ ($T = H$ when $q$ is "any"). Assume $T[i][j]$ is finite, and, if $q$ is "any" and the column prepended just before this pass is an X-column (a Y-column), that $X[i][j] < H[i][j]$ (that $Y[i][j] < H[i][j]$). Then the pass prepends one column $c$, moves to a cell $(i', j')$ with state $q'$ and table $T'$, and:

1. $T'[i'][j']$ is finite and $T[i][j] = T'[i'][j'] + \kappa(c \mid c')$, where $c'$ is the column the next pass prepends, or a dummy pair column if $(i', j') = (0, 0)$;
2. the assumption holds again at $(i', j', q')$.

*Proof.* If $q$ is "any", line L11 picks a table among $M, X, Y$ with value $H[i][j]$, which exists by line L8 since $(i, j) \ne (0, 0)$. By the assumption it does not pick $X$ right after an X-column, nor $Y$ right after a Y-column. Call the picked table $T$ again; its value is $H[i][j]$.

*Pair step, line L12.* $M[i][j]$ is finite, so $i, j \ge 1$, and $M[i][j] = H[i-1][j-1] + s(x_i, y_j)$ by line L5. The new state is "any", $T' = H$, and $\kappa(c \mid c') = s(x_i, y_j)$ for every $c'$. The assumption at the new cell is vacuous, since $c$ is a pair column.

*X step, lines L13 and L14.* $X[i][j]$ is finite, so $i \ge 1$. If $X[i][j] = X[i-1][j] - e$, the new state is $X$, so the next pass prepends an X-column $c'$ and $\kappa(c \mid c') = -e$. Otherwise line L6 gives $X[i][j] = H[i-1][j] - d > X[i-1][j] - e$, and the new state is "any" with $T' = H$. Then $H[i-1][j] - d > X[i-1][j] - e \ge X[i-1][j] - d$, so $X[i-1][j] < H[i-1][j]$, which is the assumption at the new cell. By that assumption the next column $c'$ is not an X-column, so $\kappa(c \mid c') = -d$. In both cases $T[i][j] = T'[i-1][j] + \kappa(c \mid c')$, and $T'[i-1][j]$ is finite as the difference of finite numbers.

*Y step, line L15*, is symmetric. $\square$

**Theorem.** The algorithm returns $H^*(m, n)$ and an alignment of $x$ and $y$ with that score.

*Proof.* At line L9 the state is "any", $H[m][n]$ is finite, and no column has been prepended, so Lemma 3 applies. By induction it applies to every pass. Each pass decreases $i + j$ by 1 or 2, so the loop stops at $(0, 0)$. The state at $(0, 0)$ is "any": a pair step always sets "any", and a state $X$ or $Y$ would follow $X[0][0] = -\infty$ or $Y[0][0] = -\infty$, while Lemma 3 keeps the followed value finite. So the final value is $H[0][0] = 0$. Let the prepended columns be $c_1, \ldots, c_k$ from left to right. Summing part 1 of Lemma 3 over the passes, the values telescope:

$$H[m][n] = 0 + \sum_{t=1}^{k} \kappa(c_t \mid c_{t-1}) = S(c_1 \cdots c_k).$$

Each pass prepends exactly the letters whose indices it decreases, so the top row spells $x$ and the bottom row spells $y$, and no column holds two spaces. By Lemma 2, line L16 returns $H[m][n] = H^*(m, n)$ together with an alignment of that score. $\square$

**Where $d \ge e$ is used.** Only in Lemma 1. Without it, the term $X^*(i-1, j) - d$ in $R'$ can exceed $R$, and the tables can hold a score that no alignment has.
