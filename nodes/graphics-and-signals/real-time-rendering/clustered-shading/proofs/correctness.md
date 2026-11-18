---
title: Clustered light assignment never drops a light that reaches a pixel
proves: [correctness]
status: full
---

**Setting.** The conventions are those of the tiled shading page: the camera is at the origin and looks along $-z$, the view depth is $d = -z > 0$, the pixel $(i, j)$ at depth $d$ has the position $P = d\,(u(i + 1/2), v(j + 1/2), -1)$, and a light with center $c$ and radius $r$ reaches $P$ only if $\lVert P - c \rVert < r$, with a contribution of exactly 0 otherwise. The screen has $S_y$ tiles in $y$, the vertical field of view is $2\theta$, the near plane is at depth $n_0 > 0$, and $q = 1 + 2 \tan\theta / S_y > 1$. Slice $k$ covers the depths $[n_k, n_{k+1})$ with $n_k = n_0 q^k$ (Equation 1 of Olsson, Billeter and Assarsson). A pixel at depth $d \ge n_0$ gets the key (tile $i$, tile $j$, slice $k$) with $k = \lfloor \log(d / n_0) / \log q \rfloor$ (Equation 2). The light list of an occupied cluster keeps a light unless the sphere is fully outside one of the four side planes of the tile, or $-c_z + r < n_k$, or $-c_z - r > n_{k+1}$. The claims are in exact arithmetic.

**Lemma 1 (the slice of a depth).** For $d \ge n_0$, the index $k$ of Equation 2 satisfies $n_k \le d < n_{k+1}$, and it is the only integer that does.

*Proof.* Since $\log q > 0$, $k \le \log(d / n_0) / \log q < k + 1$ is the same as $q^k \le d / n_0 < q^{k + 1}$, which is $n_k \le d < n_{k+1}$. The intervals $[n_k, n_{k+1})$ are disjoint, because $n_k$ is increasing in $k$. $\square$

In floating point, the logarithms can put a depth that lies very close to $n_k$ one slice off. The code corrects $k$ with one comparison against $n_k$ and $n_{k+1}$ in each direction, so Lemma 1 holds for the computed index with the computed slice bounds.

**Lemma 2 (self-similar slices).** The depth extent of slice $k$ equals the height of one tile at the depth $n_k$.

*Proof.* At depth $x$, the view frustum is $2 x \tan\theta$ high, so one of the $S_y$ tiles is $2 x \tan\theta / S_y$ high. The extent of slice $k$ is $n_{k+1} - n_k = n_k (q - 1) = n_k \cdot 2 \tan\theta / S_y$, which is this height at $x = n_k$. $\square$

So the near face of each cluster is a square in view space if the tiles are square in view space, and the cluster is as deep as it is high. The far face is larger by the factor $q$.

**Theorem 1 (no miss).** If a light reaches the position $P$ of a pixel, then the light is in the list of the cluster of that pixel.

*Proof.* Let the pixel be in tile $\tau$ and slice $k$. By Lemma 1 of the tiled shading proof, $m \cdot P \ge 0$ for each of the four inward unit normals $m$ of $\tau$, so with $\delta = \lVert P - c \rVert < r$ we get $m \cdot c \ge m \cdot P - \delta > -r$, and no plane rejects the light. By Lemma 1 above, $n_k \le d < n_{k+1}$, where $d = -P_z$. Also $|(-c_z) - d| \le \delta < r$. Hence $-c_z + r > d \ge n_k$ and $-c_z - r < d < n_{k+1}$, and the depth test keeps the light. $\square$

**Theorem 2 (the image is the brute-force image).** If the lists hold every light that reaches a pixel of the cluster and are visited in increasing index order, the clustered image equals the brute-force image value for value, also in floating point.

*Proof.* As for tiled shading: each light that is not in the list contributes exactly $+0$ to the brute-force sum, and adding $+0$ to a sum that is $\ge 0$ does not change it, so both sums perform the same nonzero additions in the same order. $\square$

**Theorem 3 (cost).** Let $p$ be the number of pixels, $l$ the number of lights and $t$ the number of occupied clusters. The keys cost $O(p)$, finding the occupied clusters costs $O(p)$ expected time with hashing or $O(p \log p)$ with sorting, the light assignment by testing every light against every occupied cluster costs $O(t l)$, and $t \le p$. With $S_x S_y$ tiles and the depth range $[n_0, f]$, also $t \le S_x S_y \lceil \log(f / n_0) / \log q \rceil$.

*Proof.* Each pixel computes one key in $O(1)$. The set of distinct keys is built with one insertion per pixel. Each pair of an occupied cluster and a light costs one test of $O(1)$. A cluster is occupied only if at least one pixel has its key, so $t \le p$. The slice index of a depth in $[n_0, f]$ is at most $\log(f / n_0) / \log q$, which bounds the number of slices. $\square$

**What is not claimed.** Clusters remove the false positives of a large depth range in a tile, but the list of a cluster is not always a subset of the list of its tile, because the slab of the slice can reach past the nearest or farthest pixel of the tile. The gain over tiled shading in the tests is a measurement on one scene. The radius of a light, the tile size and the slice ratio are tuning.
