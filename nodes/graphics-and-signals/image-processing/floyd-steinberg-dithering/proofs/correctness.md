---
title: Floyd-Steinberg dithering conserves the error exactly, up to the part pushed off the image, and keeps every error within half a step
proves: [correctness]
status: full
---

Let $v(x, y)$ be the input, $q(x, y)$ the output, $v'(x, y)$ the value of line L4 when pixel $(x, y)$ is visited, and $e(x, y) = v'(x, y) - q(x, y)$ the error of line L5. Write $N = \{(1, 0, 7/16), (-1, 1, 3/16), (0, 1, 5/16), (1, 1, 1/16)\}$ for the weights of line L6, with $dx$ negated on the rows that run right to left in the serpentine order. The weights add up to $\frac{7 + 3 + 5 + 1}{16} = 1$.

Every target $(x + dx, y + dy)$ of line L6 comes after $(x, y)$ in the visiting order: either it is the next pixel in the same row in the direction of the scan, or it is in the next row. So when a pixel is visited, it has received all the error it will ever receive, and

$$
v'(x, y) = v(x, y) + r(x, y), \qquad r(x, y) = \sum_{(x_0, y_0) \to (x, y)} w\, e(x_0, y_0), \tag{1}
$$

where the sum runs over the earlier pixels whose line L7 adds a share to $(x, y)$, with weight $w$.

**Claim 1 (conservation).** $\displaystyle \sum_{x, y} v(x, y) - \sum_{x, y} q(x, y) = \text{lost}$, where lost is the sum of the shares of line L8.

*Proof.* Each pixel sends shares $w\, e(x, y)$ with $\sum w = 1$, so the shares of one pixel add up to $e(x, y)$. Each share goes to a pixel inside the image, where it is a term of $r$ in (1), or it goes to line L8. Adding over all pixels,

$$
\sum_{x, y} e(x, y) = \sum_{x, y} r(x, y) + \text{lost}.
$$

By (1) and the definition of $e$, $\sum (q + e) = \sum v' = \sum v + \sum r$. Subtracting the two equations gives $\sum q = \sum v - \text{lost}$. The argument does not depend on how line L4 chooses the level or on the scan order, and it is exact in rational arithmetic. $\square$

**Claim 2 (bounded error).** Let the levels be $0, 1/m, 2/m, \ldots, 1$ for some $m \ge 1$, with $m = 1$ for black and white, and let every $v(x, y) \in [0, 1]$. Then for every pixel, $|e(x, y)| \le 1/(2m)$ and $v'(x, y) \in [-1/(2m), 1 + 1/(2m)]$.

*Proof.* By induction in the visiting order. Suppose every earlier pixel has $|e| \le 1/(2m)$. The pixel $(x, y)$ receives shares from at most four earlier pixels, each with a different weight of $N$, so

$$
|r(x, y)| \le \sum w\, |e(x_0, y_0)| \le \frac{1}{2m} \sum_{N} w = \frac{1}{2m}.
$$

By (1), $v' \in [-1/(2m), 1 + 1/(2m)]$. Line L4 picks the nearest level. If $v' \in [0, 1]$, the nearest of the levels spaced $1/m$ apart is within half a spacing, so $|e| \le 1/(2m)$. If $v' < 0$, the nearest level is 0 and $|e| = |v'| \le 1/(2m)$. If $v' > 1$, the nearest level is 1 and $e = v' - 1 \le 1/(2m)$. The first pixel has $r = 0$, which starts the induction. $\square$

**Consequence (constant gray).** Let $v \equiv g$ and the levels be $\{0, 1\}$, so that $\sum q$ is the number of ones. A pixel sends a share off the image only if it is in the last row (the three shares below) or in the first or the last column of its row (the shares behind and ahead). There are at most $W + 2H$ such pixels, and the shares that one pixel sends off add up to at most $|e| \le 1/2$ in absolute value. By Claim 1,

$$
\Big| \sum q - g W H \Big| = |\text{lost}| \le \frac{W + 2H}{2}.
$$

So the fraction of ones is $g$ up to $O(1/W + 1/H)$, and the error of the mean over the image goes to 0 as the image grows.
