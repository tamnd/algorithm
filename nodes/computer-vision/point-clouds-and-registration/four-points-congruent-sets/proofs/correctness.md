---
title: A trial whose base lies in the overlap finds the image of the base
proves: [correctness]
status: full
---

We use the notation of the page and of the reference code. A trial picks a base $a, b, c, d$ from $P$. The lines $ab$ and $cd$ have closest points $e_1 = a + r_1 (b - a)$ and $e_2 = c + r_2 (d - c)$, with $0 < r_1, r_2 < 1$, and the base is accepted when the gap $\gamma = |e_1 - e_2|$ is at most $\delta$. Let $d_1 = |a - b|$ and $d_2 = |c - d|$. Line L4 collects the ordered pairs $(i, j)$ of $Q$ with $\big| |q_i - q_j| - d_1 \big| \le \delta$, and the same for $d_2$. Line L5 keeps a 4-tuple $(i, j, k, l)$ when $|(q_i + r_1 (q_j - q_i)) - (q_k + r_2 (q_l - q_k))| \le \delta$. Line L6 fits a rigid motion by the Kabsch method and drops the tuple if a base point is more than $2\delta$ from its partner after the fit. Line L7 scores the motion by the LCP.

## Lemma 1: the ratios are affine invariant

Let $A(x) = M x + t$ be an affine map with $M$ invertible. If $a, b, c, d$ are coplanar and the segments $ab$ and $cd$ meet at $e = a + r_1 (b - a) = c + r_2 (d - c)$, then the segments $A(a)A(b)$ and $A(c)A(d)$ meet at $A(e)$, with the same $r_1$ and $r_2$.

*Proof.* $A(a + r(b - a)) = A(a) + r (A(b) - A(a))$, because $A$ maps a weighted mean $(1 - r) a + r b$ to $(1 - r) A(a) + r A(b)$. So $A(e)$ lies on both image segments at the parameters $r_1$ and $r_2$. The image lines are not parallel, because $M$ is invertible and the lines $ab$ and $cd$ are not parallel, so they meet in one point, which is $A(e)$. $\square$

A rigid motion is an affine map, so the ratios are rigid invariants too. The ratios do not determine the base up to a rigid motion: any affine image of the base has the same ratios. This is why line L6 checks the rigid fit.

## Lemma 2: completeness of the extraction

Suppose $T$ is a rigid motion and $Q$ contains points $q_i, q_j, q_k, q_l$ with $|q_i - T a|$, $|q_j - T b|$, $|q_k - T c|$ and $|q_l - T d|$ all at most $\varepsilon$. If $2 \varepsilon + \gamma \le \delta$, then $(i, j, k, l)$ is among the tuples of line L5.

*Proof.* $T$ keeps distances, so $|T a - T b| = d_1$, and by the triangle inequality $\big| |q_i - q_j| - d_1 \big| \le 2 \varepsilon \le \delta$. So $(i, j)$ passes line L4; the same holds for $(k, l)$ with $d_2$. Next, $T$ is affine, so $T e_1 = (1 - r_1) T a + r_1 T b$, and

$$|(1 - r_1) q_i + r_1 q_j - T e_1| \le (1 - r_1) |q_i - T a| + r_1 |q_j - T b| \le \varepsilon .$$

In the same way the point of the pair $(k, l)$ is within $\varepsilon$ of $T e_2$. Since $|T e_1 - T e_2| = \gamma$, the two points are within $2 \varepsilon + \gamma \le \delta$ of each other, so line L5 keeps the tuple. $\square$

The reference code finds every such tuple, because the grid query of line L5 returns all stored points within $\delta$: a point within $\delta$ of the query lies in one of the 27 cubes of side $\delta$ around the cube of the query.

## Lemma 3: the true tuple passes the rigid check

Under the conditions of Lemma 2, the Kabsch fit $(\hat R, \hat t)$ from $(a, b, c, d)$ to $(q_i, q_j, q_k, q_l)$ has every residual at most $2 \varepsilon \le 2\delta$.

*Proof.* The Kabsch method returns a rigid motion that minimizes the sum of squared residuals over all rigid motions. The motion $T$ has sum at most $4 \varepsilon^2$. So the fit has sum at most $4 \varepsilon^2$, and each residual is at most $2 \varepsilon$. $\square$

If $a, b, c$ are not on one line, which the base selection ensures, then four exact correspondences determine the rigid motion, so for $\varepsilon = 0$ the fit equals $T$.

## Theorem

If in some trial the base lies in the overlap, in the sense of Lemma 2 with $2 \varepsilon + \gamma \le \delta$, then that trial scores a motion $\hat T$ whose residuals on the base are at most $2 \varepsilon$, and the result of 4PCS has an LCP score at least the score of $\hat T$.

*Proof.* Lemmas 2 and 3 show that the tuple is extracted and survives the check, so line L7 scores $\hat T$. The best score over all trials is kept. $\square$

## What this does not prove

- The theorem needs a trial whose base lies in the overlap. The base is random, so this holds only with some probability. If a fraction $f$ of the points of $P$ lie in the overlap and the base were four independent uniform picks, the chance per trial would be about $f^4$, and the number of trials for a success probability $p$ would follow the RANSAC bound. The reference code picks wide bases, which are not uniform, so this is a guide, not a bound.
- A motion with the best LCP need not be the true motion. A small $\delta$, a symmetric shape or a small overlap can make a wrong motion score higher.
- The motion $\hat T$ is fit to four points only, so its error grows with the noise and with a small base. A refinement such as ICP on all points is usual.
