---
title: Supersampling computes the sample mean, its ordered grid error is at most the number of cut cells over k squared, and jittering is unbiased
proves: [correctness]
status: full
---

Fix a pixel $(i, j)$, the square $Q = [i, i+1] \times [j, j+1]$. Split $Q$ into the $k^2$ closed cells $Q_{a,b} = [i + a/k, i + (a+1)/k] \times [j + b/k, j + (b+1)/k]$ for $0 \le a, b < k$. Each cell has area $1/k^2$, and the ordered grid sample of the cell is its center $s_{a,b}$.

The scene is $n$ triangles in priority order with colors in $[0, 1]$ per channel, over a background color. For a point $p$, let $g(p)$ be the color that the algorithm assigns at $p$: the color of the last triangle in the list that contains $p$, or the background. Let $B$ be the union of the edges of all triangles of positive area, a set of $s = 3n$ segments or fewer. The exact box-filtered value is $\bar g = \iint_Q g$; it is well defined because $g$ is constant on each connected part of the plane minus $B$, and $B$ has area zero.

**Lemma 1 (what the algorithm computes).** SSAA writes $P[i, j] = k^{-2} \sum_{a,b} g(s_{a,b})$ for the ordered grid.

*Proof.* Line L2 sets the sum to zero. Lines L3 to L6 run once for each pair $(a, b)$, and line L4 sets the point to $s_{a,b} = (i + (a + 1/2)/k, j + (b + 1/2)/k)$. Line L5 scans the triangles from the last to the first and returns the first one that contains the point, which is the last one in priority order, so line L6 adds $g(s_{a,b})$. Line L7 divides by $k^2$. Lines L1 and L8 do this for every pixel and return the image. $\square$

**Lemma 2.** If the interior of a cell does not meet $B$, then $g$ is constant on the interior of the cell, and $g(s_{a,b}) = k^2 \iint_{Q_{a,b}} g$.

*Proof.* The interior of the cell is connected, and it meets no edge of any triangle. A triangle's closed set is bounded by its edges, so a connected set that misses the edges lies entirely inside or entirely outside each triangle. Hence the set of triangles that contain a point is the same for all points of the interior, and $g$ is constant there. The center $s_{a,b}$ lies in the interior. The boundary of the cell has area zero, so the integral of $g$ over the cell is $1/k^2$ times that constant. $\square$

**Lemma 3.** A segment $e$ meets the interiors of at most $2k - 1$ cells of $Q$.

*Proof.* The interior grid lines of $Q$ are the $k - 1$ vertical lines $x = i + a/k$ and the $k - 1$ horizontal lines $y = j + b/k$ for $1 \le a, b \le k - 1$. If $e$ lies on one of these lines, it meets no cell interior. Otherwise $e$ meets each of these lines in at most one point, because a segment that meets a line in two points lies on it. Let $e' = e \cap Q$, a segment or empty. Remove from $e'$ its points on the interior grid lines: at most $2k - 2$ points, so at most $2k - 1$ open pieces remain. Each piece is connected and misses every interior grid line, so it lies in the interior of one cell or on the boundary of $Q$. The removed points lie on grid lines, which are not in any cell interior. So the cell interiors that $e$ meets number at most $2k - 1$. $\square$

**Theorem 1 (ordered grid error).** Let $m$ be the number of cells of $Q$ whose interior meets $B$. Then, per channel, $|P[i, j] - \bar g| \le m / k^2 \le s(2k-1)/k^2$. For one triangle, $s = 3$; for one straight edge crossing the pixel, the bound is $(2k-1)/k^2 < 2/k$.

*Proof.* By Lemma 1, $P[i, j] - \bar g = \sum_{a,b} \big(k^{-2} g(s_{a,b}) - \iint_{Q_{a,b}} g\big)$. By Lemma 2, the terms of the cells whose interior misses $B$ are zero. For each other cell, both $k^{-2} g(s_{a,b})$ and $\iint_{Q_{a,b}} g$ lie in $[0, 1/k^2]$ per channel, so the term has absolute value at most $1/k^2$. There are $m$ such cells, which gives the first bound. Each cell counted in $m$ has its interior met by some edge, and by Lemma 3 each of the $s$ edges meets at most $2k-1$ cell interiors, so $m \le s(2k-1)$. $\square$

**Tightness.** Let the pixel $Q = [0, 1]^2$ be black below the horizontal line $y = (r + 1/2)/k - \varepsilon$ for an integer $0 \le r < k$ and a small $\varepsilon > 0$, and white above it. The samples with $b < r$ are black and the others are white, so $P = r/k$ while $\bar g = (r + 1/2)/k - \varepsilon$. The error is $1/(2k) - \varepsilon$. So the worst case error for one edge is $\Theta(1/k) = \Theta(N^{-1/2})$ with $N = k^2$ samples.

**Theorem 2 (jittered samples).** Replace $s_{a,b}$ by a point $X_{a,b}$ drawn uniformly from the cell $Q_{a,b}$, independently for all cells. Then $\mathbb{E}[P[i, j]] = \bar g$. If the scene is one triangle of color 1 on background 0, then $\operatorname{Var}(P[i, j]) \le m/(4k^4) \le 3(2k-1)/(4k^4)$.

*Proof.* For one cell, $\mathbb{E}[g(X_{a,b})] = k^2 \iint_{Q_{a,b}} g$, because the density of $X_{a,b}$ is $k^2$ on the cell. By linearity, $\mathbb{E}[P] = k^{-2} \sum_{a,b} k^2 \iint_{Q_{a,b}} g = \bar g$. For one triangle on a black background, $g(X_{a,b})$ is a Bernoulli variable with mean $q_{a,b}$, the covered fraction of the cell, so its variance is $q_{a,b}(1 - q_{a,b}) \le 1/4$. If the interior of the cell misses $B$, then $q_{a,b} \in \{0, 1\}$ and the variance is zero. The cells are independent, so $\operatorname{Var}(P) = k^{-4} \sum_{a,b} q_{a,b}(1 - q_{a,b}) \le m/(4k^4)$, and $m \le 3(2k-1)$ by Lemma 3. $\square$

With $N = k^2$, the variance bound is below $3 N^{-3/2}/2$ for one triangle, so the RMS error is $O(N^{-3/4})$. With $N$ independent uniform samples in the whole pixel, the variance is $\bar g (1 - \bar g)/N$, which is of order $N^{-1}$ when $\bar g$ is not close to 0 or 1.

**The implementation.** The program draws each offset from a lattice of $M \times M$ points inside the cell (the parameter `jitter_steps`) instead of the continuous uniform law. Then $\mathbb{E}[g(X_{a,b})]$ is the mean of $g$ over those $M^2$ lattice points, so the expectation of the jittered estimate equals the ordered grid estimate with $kM \times kM$ samples. By Theorem 1 applied with $kM$, it differs from $\bar g$ by at most $s(2kM - 1)/(kM)^2$, which is below $2s/(kM)$. The variance bound of Theorem 2 holds for the lattice law as well, since only the Bernoulli argument was used, with $q_{a,b}$ the fraction of covered lattice points. $\blacksquare$
