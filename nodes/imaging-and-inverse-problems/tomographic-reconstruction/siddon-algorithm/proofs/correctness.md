---
title: Correctness of Siddon's algorithm
proves: [correctness]
status: full
---

We use the conventions of the page. The image is $n \times n$ on $Q = [-1, 1]^2$ with $h = 2/n$. Pixel $(i, j)$ is the closed square $P_{ij} = [-1 + jh, -1 + (j+1)h] \times [1 - (i+1)h, 1 - ih]$. The ray is $p(\alpha) = p_0 + \alpha d$ with $d = p_1 - p_0 = (d_x, d_y) \ne 0$, $0 \le \alpha \le 1$, and $D = |d|$. We work in exact arithmetic. A vertical grid line is a line $x = -1 + kh$ and a horizontal grid line is a line $y = -1 + kh$, for an integer $k$ with $0 \le k \le n$.

We prove that SIDDON returns, for each pixel $P_{ij}$ whose intersection with the segment has positive length, exactly one triple $(i, j, \ell)$ with $\ell$ that length, and no other triple. For a ray that lies on a grid line, the length goes to one of the two pixels that share that line, as the page says.

**Lemma 1 (clipping, line L2).** Let $I = \{\alpha \in [0, 1] : p(\alpha) \in Q\}$. If $I$ has positive length, line L2 sets $[\alpha_{\min}, \alpha_{\max}] = I$. If $I$ is empty or one point, line L3 returns the empty list, which is correct.

*Proof.* $p(\alpha) \in Q$ if and only if $-1 \le x_0 + \alpha d_x \le 1$ and $-1 \le y_0 + \alpha d_y \le 1$. For $d_x \ne 0$, the first condition is $\alpha$ between $(-1 - x_0)/d_x$ and $(1 - x_0)/d_x$, a closed interval, and line L2 intersects $[0, 1]$ with it. For $d_x = 0$ the condition does not depend on $\alpha$: it holds for all $\alpha$ or for none. The same holds for $y$. An intersection of closed intervals is a closed interval, so $I = [\alpha_{\min}, \alpha_{\max}]$ when it is not empty. A segment of zero length meets no pixel with positive length. $\square$

The code tests $-1 \le c_0 < 1$ when $d_c = 0$, not $c_0 \le 1$. A ray on the line $x = 1$ touches only the border of $Q$, and the rule of line L9 would give it to column $n$, which does not exist. So the code drops it. This changes only rays on the border of $Q$.

**Lemma 2 (the crossing lists, lines L4 and L5).** Suppose $d_x \ne 0$. Line L4 returns, in increasing order, exactly the values $\alpha \in (\alpha_{\min}, \alpha_{\max})$ at which $x(\alpha) = x_0 + \alpha d_x$ is on a vertical grid line. The same holds for line L5 and the horizontal lines.

*Proof.* Put $u(\alpha) = n(x(\alpha) + 1)/2$. Then $x(\alpha) = -1 + kh$ if and only if $u(\alpha) = k$. The function $u$ is affine and strictly monotone, so it maps $(\alpha_{\min}, \alpha_{\max})$ onto the open interval between $u(\alpha_{\min})$ and $u(\alpha_{\max})$. Call its ends $u_- < u_+$. The integers in $(u_-, u_+)$ are $k = \lfloor u_- \rfloor + 1, \ldots, \lceil u_+ \rceil - 1$, which is the range that the code builds. Each such $k$ gives exactly one $\alpha = (-1 + kh - x_0)/d_x$ in the open interval. Because $x(\alpha) \in [-1, 1]$ on $I$, we have $u \in [0, n]$, so each $k$ is a real grid line. If $d_x > 0$, then $\alpha$ increases with $k$ and the code lists $k$ upward. If $d_x < 0$, then $\alpha$ decreases with $k$ and the code lists $k$ downward. So the list is increasing in both cases. $\square$

If $d_x = 0$, line L4 returns the empty list. That is correct too: then $x$ is constant, and either it is not on a grid line, or it is on one for every $\alpha$, which is the case of a ray on a grid line that we treat at the end.

**Lemma 3 (merge, line L6).** $S$ is the increasing list of $\alpha_{\min}$, all values of Lemma 2 for both axes, and $\alpha_{\max}$. Equal values from the two lists stay as two equal neighbors.

*Proof.* $A_x$ and $A_y$ are increasing by Lemma 2. MERGE of two increasing lists is the increasing list of all their elements, with repetitions, by the standard invariant of the merge step of merge sort: the output so far is increasing and holds the smallest elements. All values are in $(\alpha_{\min}, \alpha_{\max})$, so putting $\alpha_{\min}$ in front and $\alpha_{\max}$ at the end keeps the list increasing. $\square$

Let $\beta_0 < \beta_1 < \cdots < \beta_m$ be the distinct values of $S$. These are the pairs that the loop of line L7 keeps, because it skips the pairs of equal neighbors. Put $J_r = (\beta_{r-1}, \beta_r)$ for $r = 1, \ldots, m$.

**Lemma 4 (one piece, one pixel).** Assume the ray is not on a grid line. For each $r$, the open piece $p(J_r)$ lies in the interior of one pixel $P_{ij}$, and lines L8 and L9 compute this $(i, j)$.

*Proof.* Take $\alpha \in J_r$. By Lemmas 2 and 3, no value of $J_r$ puts $x(\alpha)$ or $y(\alpha)$ on a grid line. Also $p(\alpha)$ is in $Q$, by Lemma 1. Consider $x$. If $d_x \ne 0$, the continuous function $x(\alpha)$ on the interval $J_r$ never meets a grid line, so it stays in one open interval $(-1 + jh, -1 + (j+1)h)$. If $d_x = 0$, then $x$ is constant and, by the assumption, not on a grid line, so it is in one such interval as well. The same holds for $y$ and an interval $(1 - (i+1)h, 1 - ih)$. So $p(J_r)$ is in the interior of $P_{ij}$. The midpoint $(x_m, y_m)$ of line L8 is in $p(J_r)$. From $-1 + jh < x_m < -1 + (j+1)h$ we get $j < (x_m + 1)/h < j + 1$, so $\lfloor (x_m + 1)/h \rfloor = j$. From $1 - (i+1)h < y_m < 1 - ih$ we get $i < (1 - y_m)/h < i + 1$, so $\lfloor (1 - y_m)/h \rfloor = i$. The clamp to $[0, n-1]$ does not change these values. $\square$

**Lemma 5 (length, line L10).** The length of $p(J_r)$ is $(\beta_r - \beta_{r-1})D$.

*Proof.* $|p(\alpha) - p(\alpha')| = |\alpha - \alpha'|\,|d| = |\alpha - \alpha'| D$. $\square$

**Theorem.** Assume the ray is not on a grid line. Then SIDDON returns each pixel $P_{ij}$ whose intersection with the segment has positive length exactly once, with the length of that intersection, and no other pixel.

*Proof.* The segment inside $Q$ is $p(I)$ by Lemma 1, and $I$ is the union of the pieces $J_r$ and the finite set $\{\beta_0, \ldots, \beta_m\}$. A finite set of points has length 0. So the length of $p(I) \cap P_{ij}$ is the sum of the lengths of the pieces $p(J_r)$ that lie in $P_{ij}$. By Lemma 4, every piece lies in exactly one pixel and in the interior of it.

It remains to show that no two pieces lie in the same pixel. Take $r < r'$ with both pieces in $P_{ij}$. Then $\beta_r$ is in $(\alpha_{\min}, \alpha_{\max})$ and is a value of $A_x$ or $A_y$, so $p(\beta_r)$ is on a grid line, say $x = -1 + kh$, and $d_x \ne 0$. On $J_r$ the value of $x$ is on one side of this line, and on $J_{r'}$ it is on the other side, because $x(\alpha)$ is strictly monotone. Both sides cannot meet the interior of $P_{ij}$, because the interior of a pixel lies on one side of each grid line. This is a contradiction.

So each pixel with positive length gets exactly one triple, with its full length by Lemma 5. A pixel with zero length gets no piece, so it gets no triple. $\square$

**A ray on a grid line.** Suppose $d_x = 0$ and $x_0 = -1 + kh$ with $0 \le k < n$. Then the segment touches columns $k - 1$ and $k$ (or only column $k$ when $k = 0$), and the closed intersection with a pixel of each column has positive length. Lemmas 1 to 3 and 5 hold as before. In the proof of Lemma 4, $y$ still stays in one open row interval, and the midpoint gives $(x_m + 1)/h = k$, so line L9 returns column $k$. So the code returns the pixels of column $k$ with their full lengths, and none of column $k - 1$. This is the convention of the page: the length goes to the pixel on the right of a vertical line, and below a horizontal line by the same argument with $\lfloor (1 - y_m)/h \rfloor$. The sum of all lengths is still the length of $p(I)$, so a projection of an image that is constant across the line is still exact.

**Exactness with rationals.** All the operations of lines L2 to L9 are additions, subtractions, products, quotients, floors and ceilings of the input coordinates and the integers $k$ and $n$. So with rational input, every $\alpha$ is rational and computed exactly, and all comparisons in Lemma 2, Lemma 3 and line L7 are exact. The only square root is $D$. If $D$ is rational, as for the directions $(3, 4)$ or $(5, 12)$, every output length is exact. This is the setting of the test that compares the output with a brute-force clip of the segment against each pixel.

**Projection and back projection.** Let $A$ be the matrix with $A_{r, in + j} = \ell$ for each output triple $(i, j, \ell)$ of ray $r$. The projector computes $(Ax)_r = \sum \ell\, x_{ij}$ over the triples of ray $r$, and the back projector adds $\ell\, y_r$ to pixel $(i, j)$ for the same triples, which is $(A^T y)_{in+j}$. So $\langle Ax, y\rangle = \sum_r \sum_{(i,j,\ell)} \ell\, x_{ij}\, y_r = \langle x, A^T y\rangle$ for all $x$ and $y$. By the theorem, for a piecewise constant image $f = \sum x_{ij}\chi_{P_{ij}}$, $(Ax)_r$ is the exact integral of $f$ along the segment of ray $r$.
