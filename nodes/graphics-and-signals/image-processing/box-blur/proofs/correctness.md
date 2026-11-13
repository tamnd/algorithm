---
title: The two passes of running sums give the direct 2D box sum with the same border rule
proves: [correctness]
status: full
---

Let $f$ have $W \ge 1$ columns and $H \ge 1$ rows, and let $r \ge 0$. For an axis of length $n$ the border rule is a map $\mathrm{ext}(\cdot, n)$ from the integers to $\{0, \dots, n-1\} \cup \{\bot\}$ with $\mathrm{ext}(i, n) = i$ for $0 \le i < n$; the symbol $\bot$ means no pixel. For a row $a$ of length $n$ write $\hat a(i) = a[\mathrm{ext}(i, n)]$, read as $0$ when the index is $\bot$. The extended image is $\tilde f(i, j) = f[\mathrm{ext}(j, H)][\mathrm{ext}(i, W)]$, read as $0$ when either index is $\bot$. The claim is that BOX-BLUR returns

$$h(x, y) = \frac{1}{(2r+1)^2} \sum_{v=-r}^{r} \sum_{u=-r}^{r} \tilde f(x+u, y+v) \quad \text{for } 0 \le x < W,\ 0 \le y < H.$$

**Lemma 1 (one running pass).** Let $a$ be a row of length $n \ge 1$. The loop of lines L2 to L6, applied to $a$, stores $g[x] = \sum_{u=-r}^{r} \hat a(x+u)$ for every $0 \le x < n$.

*Proof.* By induction on $x$, with the invariant $s = \sum_{u=-r}^{r} \hat a(x+u)$ when line L6 (or L3 for $x = 0$) stores $s$. Base: line L2 sets $s = \sum_{u=-r}^{r} \hat a(u)$, the claim for $x = 0$, and line L3 stores it. Step: assume $s = \sum_{i=x-1-r}^{x-1+r} \hat a(i)$ before line L5 for some $x \ge 1$. The index set $\{x - r, \dots, x + r\}$ equals $\{x - 1 - r, \dots, x - 1 + r\}$ with $x - r - 1$ removed and $x + r$ added, and these two indices differ because $2r + 1 \ge 1$. So the new value $s + \hat a(x + r) - \hat a(x - r - 1)$ of line L5 is $\sum_{i=x-r}^{x+r} \hat a(i)$, which line L6 stores. Termination: the loop of line L4 runs over the finite range $1 \le x \le n - 1$. $\square$

**Lemma 2 (the horizontal pass).** After lines L1 to L6, $g[y][x] = \sum_{u=-r}^{r} f[y][\mathrm{ext}(x+u, W)]$ for $0 \le y < H$, $0 \le x < W$.

*Proof.* Lemma 1 applied to each row $a = f[y]$. $\square$

**Lemma 3 (the extended rows of $g$).** For every integer $j$ and every $0 \le x < W$,

$$g[\mathrm{ext}(j, H)][x] = \sum_{u=-r}^{r} \tilde f(x + u, j),$$

with the left side read as $0$ when $\mathrm{ext}(j, H) = \bot$.

*Proof.* If $\mathrm{ext}(j, H) = \bot$, then every term $\tilde f(x+u, j)$ is $0$ by definition, and both sides are $0$. Otherwise $y' = \mathrm{ext}(j, H)$ is a row of the image, and by Lemma 2 the left side is $\sum_u f[y'][\mathrm{ext}(x+u, W)]$, which is $\sum_u \tilde f(x+u, j)$ term by term, the zero terms included. $\square$

This is the step that needs the border rule to act on each axis on its own, as clamp, mirror, wrap and zero do.

**Theorem.** BOX-BLUR returns $h$ as in the claim.

*Proof.* Lines L7 to L12 are Lemma 1 applied to each column $c_x = (g[0][x], \dots, g[H-1][x])$, so after line L12

$$h[y][x] = \sum_{v=-r}^{r} \hat c_x(y + v) = \sum_{v=-r}^{r} g[\mathrm{ext}(y+v, H)][x] = \sum_{v=-r}^{r} \sum_{u=-r}^{r} \tilde f(x+u, y+v)$$

by Lemma 3. Line L13 divides each entry by $(2r+1)^2$. Both passes and the division run over finite ranges, so the algorithm terminates. $\blacksquare$
