---
title: BUILD makes the table of top-left sums, and RECT-SUM and BOX-MEAN return the sum and the mean over the asked rectangle
proves: [correctness]
status: full
---

Let $f$ have $W$ columns and $H$ rows. For $0 \le x \le W$ and $0 \le y \le H$ put

$$P(x, y) = \sum_{j=0}^{y-1} \sum_{i=0}^{x-1} f[j][i],$$

the sum over the top-left block of $y$ rows and $x$ columns; an empty sum is $0$.

**Lemma 1 (BUILD).** After BUILD, $S[y][x] = P(x, y)$ for all $0 \le x \le W$, $0 \le y \le H$.

*Proof.* Row $0$ and column $0$ are set to zero at line L1 and never written again, since line L6 writes only indices $y + 1 \ge 1$ and $x + 1 \ge 1$. Their values are right because $P(x, 0) = P(0, y) = 0$.

For the other entries we use induction on the image row $y$. The hypothesis for $y$ is that row $y$ of the table holds $S[y][x] = P(x, y)$ for all $x$, which holds for $y = 0$. Fix $y$ and run the inner loop of lines L4 to L6. By a second induction on $x$, after line L5 we have $\mathrm{run} = \sum_{i=0}^{x} f[y][i]$: line L3 starts at $0$, and line L5 adds $f[y][x]$. Line L6 then sets

$$S[y+1][x+1] = S[y][x+1] + \mathrm{run} = P(x+1, y) + \sum_{i=0}^{x} f[y][i] = P(x+1, y+1),$$

where the middle step uses the outer hypothesis, which line L6 may use because it reads only row $y$, finished in the previous outer step. So row $y + 1$ is right for every column $1 \le x + 1 \le W$, and with column $0$ for all of them. The loops run over finite ranges, so BUILD terminates. $\square$

**Lemma 2 (RECT-SUM).** For $0 \le x_0 \le x_1 \le W$ and $0 \le y_0 \le y_1 \le H$, line L8 returns $\sum_{y_0 \le j < y_1} \sum_{x_0 \le i < x_1} f[j][i]$.

*Proof.* By Lemma 1, line L8 returns $P(x_1, y_1) - P(x_1, y_0) - P(x_0, y_1) + P(x_0, y_0)$. Count how often a pixel $(i, j)$ appears in this signed sum. It appears in $P(a, b)$ exactly when $i < a$ and $j < b$. Let $\alpha = [i < x_1] - [i < x_0]$ and $\beta = [j < y_1] - [j < y_0]$, with $[\cdot]$ equal to $1$ when the condition holds and $0$ otherwise. The coefficient of $f[j][i]$ is

$$[i < x_1][j < y_1] - [i < x_1][j < y_0] - [i < x_0][j < y_1] + [i < x_0][j < y_0] = \alpha \beta.$$

Because $x_0 \le x_1$, $\alpha = 1$ when $x_0 \le i < x_1$ and $\alpha = 0$ otherwise; the same holds for $\beta$ and the rows. So the coefficient is $1$ for the pixels of the rectangle and $0$ for all others. $\square$

**Lemma 3 (BOX-MEAN).** For a pixel $(x, y)$ of the image and $r \ge 0$, lines L9 and L10 return the mean of $f$ over the pixels $(i, j)$ of the image with $|i - x| \le r$ and $|j - y| \le r$.

*Proof.* The set of such pixels is $[x_0, x_1) \times [y_0, y_1)$ with the bounds of line L9, the intersection of the window $[x - r, x + r + 1) \times [y - r, y + r + 1)$ with $[0, W) \times [0, H)$. Since $0 \le x < W$, we have $x_0 \le x < x_0 + 1 \le x_1$, so the rectangle meets the precondition of Lemma 2 and is not empty; the same holds for the rows. By Lemma 2 the call returns the sum over this set, and line L10 divides by its size $(x_1 - x_0)(y_1 - y_0) \ge 1$. $\square$

**Lemma 4 (modular entries).** If every table entry and every result is kept modulo $m$, then RECT-SUM returns the true sum whenever the true sum lies in $\{0, \dots, m-1\}$.

*Proof.* Reduction modulo $m$ commutes with addition and subtraction, so the reduced table holds $P(x, y) \bmod m$, and the reduced result of line L8 is the true rectangle sum modulo $m$, which is the true sum when it lies in $\{0, \dots, m - 1\}$. $\square$

Together, Lemmas 1 to 3 prove that each operation returns the value the abstract type promises, and Lemma 4 justifies the use of wrapping machine words. $\blacksquare$
