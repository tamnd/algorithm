---
title: The affine coordinates are invariant, the true basis gets every vote, and a returned match is verified
proves: [correctness]
status: full
---

We use the notation of the page and of the reference code. A basis is an ordered triple $(o, a, b)$ of points of the plane that are not on one line. For such a basis, every point $p$ has unique affine coordinates $(\alpha, \beta)$ with $p = o + \alpha (a - o) + \beta (b - o)$, because $a - o$ and $b - o$ are linearly independent. The bin of $(\alpha, \beta)$ is $(\lfloor \alpha / s \rfloor, \lfloor \beta / s \rfloor)$ for the bin size $s$. Lines L1 to L3 store the entry (model, basis) in the bin of each other model point, for every model and every basis of its points. Line L5 computes the coordinates of each scene point that is not in the scene basis, and line L6 adds one vote to each entry found in its bin or in the 8 bins around it.

## Lemma 1: affine coordinates are invariant

Let $T(x) = A x + t$ with $A$ invertible. If $p$ has the coordinates $(\alpha, \beta)$ in the basis $(o, a, b)$, then $T(p)$ has the same coordinates in the basis $(T o, T a, T b)$, and $(T o, T a, T b)$ is a basis.

*Proof.* $T(p) - T(o) = A (p - o) = \alpha A (a - o) + \beta A (b - o) = \alpha (T a - T o) + \beta (T b - T o)$. Since $A$ is invertible, $A(a - o)$ and $A(b - o)$ are linearly independent, so the new triple is a basis and the coordinates are unique. $\square$

## Lemma 2: the true basis gets every vote

Let a model have $m$ points $y_1, \ldots, y_m$ in general position, and suppose the scene contains points $z_1, \ldots, z_m$ (in any order among other points) such that, for the basis $(y_i, y_j, y_k)$ and the scene basis $(z_i, z_j, z_k)$, the coordinates of each $z_l$ differ from those of $y_l$ by less than $s$ in each component. Then line L6 gives the entry (model, $(i, j, k)$) at least $m - 3$ votes when the scene basis is $(z_i, z_j, z_k)$.

*Proof.* For real numbers $x$ and $y$ with $|x - y| < s$, the integers $\lfloor x / s \rfloor$ and $\lfloor y / s \rfloor$ differ by at most 1, since $|x/s - y/s| < 1$. So for each $l \notin \{i, j, k\}$, the bin of $z_l$ is the bin of $y_l$ or one of its 8 neighbours. Line L3 stored (model, $(i, j, k)$) in the bin of $y_l$, so line L6 finds it and adds one vote for $z_l$. The $m - 3$ points $z_l$ are distinct scene points, and each gives the entry one vote. $\square$

In the exact case, $z_l = T(y_l)$ for an invertible affine map $T$, and by Lemma 1 the coordinates are equal, so the condition of Lemma 2 holds for every $s > 0$.

## Lemma 3: the verification accepts the true hypothesis in the exact case

If $z_l = T(y_l)$ for all $l$, the affine map that `fit_affine` computes from $(y_i, y_j, y_k)$ to $(z_i, z_j, z_k)$ is $T$, and `verify` counts all $m$ model points for any tolerance $\tau \ge 0$.

*Proof.* An affine map of the plane has 6 unknowns, and the three point pairs give 6 linear equations. With $u = y_j - y_i$ and $v = y_k - y_i$ independent, the linear part must send $u$ to $z_j - z_i$ and $v$ to $z_k - z_i$, which fixes it as $[z_j - z_i, z_k - z_i][u, v]^{-1}$; the shift then follows from $y_i \mapsto z_i$. $T$ satisfies these equations, so the solution is $T$. Then each model point $y_l$ maps to $z_l$, a scene point at distance $0 \le \tau$. $\square$

## Theorem

1. **Soundness.** If `recognize` returns a model and a map $(A, t)$, then at least `min_fit` model points (by default all $m$) land within $\tau$ of scene points under $(A, t)$.
2. **Completeness of one trial.** In the exact case of Lemma 3, with `min_votes` at most $m - 3$, a trial whose random scene basis is $(T y_i, T y_j, T y_k)$ for some basis $(y_i, y_j, y_k)$ of the model returns a match.

*Proof.* (1) Line L8 returns only a hypothesis for which `verify` counted at least the required number of points. (2) By Lemmas 1 and 2 the entry (model, $(i, j, k)$) has at least $m - 3 \ge$ `min_votes` votes, so line L7 does not stop before it. The hypotheses are tried in order of votes; either an earlier one passes the verification, and the trial returns it, or this one is reached and passes by Lemma 3. $\square$

If the scene has $n$ points, of which $k$ are the images of model points with no three on one line, then a random ordered triple of distinct scene points is the image of a stored basis with probability $k(k-1)(k-2) / (n(n-1)(n-2))$, since every ordered triple of model points that are not on one line is stored. The number of trials then follows the same bound as [RANSAC](/ransac-iteration-bound/).

## What this does not prove

- **Noise.** With noise, the coordinates change by an amount that grows as the basis gets thin or small, because $[u, v]^{-1}$ grows. The condition of Lemma 2 can then fail, and the true entry gets fewer votes. Grimson and Huttenlocher (1990) studied this effect and showed that the method degrades quickly with noise and clutter.
- **Mirror images and symmetry.** An affine map with a negative determinant is a reflection. The reference code accepts it, so a model and its mirror image are not told apart. A symmetric model gets votes for several bases, each with a valid match.
- **Wrong models.** A verification with a loose tolerance and a cluttered scene can accept a wrong model. The theorem says only that the accepted points do fit.
