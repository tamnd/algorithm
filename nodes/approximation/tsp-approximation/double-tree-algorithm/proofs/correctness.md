---
title: The double-tree algorithm returns a tour of cost at most 2(1 − 1/n) OPT
proves: [correctness]
status: full
---

The costs $c$ on the vertex set $V$, with $|V| = n \ge 2$, are symmetric, non-negative and satisfy the triangle inequality. For a walk $P = (p_0, p_1, \ldots, p_m)$ we write $c(P) = \sum_{i=1}^{m} c(p_{i-1}, p_i)$. For a tour $H = (h_1, \ldots, h_n)$, $c(H)$ includes the closing edge $c(h_n, h_1)$.

**Lemma 1 (the lower bound).** Each spanning tree $T$ of minimum cost satisfies $c(T) \le (1 - 1/n) \cdot \text{OPT}$.

*Proof.* Let $H^*$ be an optimal tour. It has $n$ edges of total cost OPT, so its most costly edge $e$ costs at least OPT$/n$. Delete $e$. The rest is a path through all $n$ vertices, so it is a spanning tree, and its cost is at most OPT $-$ OPT$/n$. A minimum spanning tree costs at most each spanning tree. $\square$

**Lemma 2 (the walk).** The multigraph $D$ of line L2 has an Euler circuit $W$, and $c(W) = 2\,c(T)$.

*Proof.* Each vertex $v$ has degree $2 \deg_T(v)$ in $D$, which is even. $D$ is connected, because $T$ is a spanning tree. By Euler's theorem, a connected multigraph with all degrees even has a closed walk that uses each edge exactly one time. $D$ has each edge of $T$ two times, so $c(W) = 2\,c(T)$. $\square$

**Lemma 3 (a shortcut).** For each walk $P = (p_0, \ldots, p_m)$, $c(p_0, p_m) \le c(P)$.

*Proof.* By induction on $m$. For $m = 0$, $c(p_0, p_0) = 0 = c(P)$; for $m = 1$ the two sides are equal. For $m \ge 2$, the triangle inequality gives $c(p_0, p_m) \le c(p_0, p_{m-1}) + c(p_{m-1}, p_m)$, and by induction $c(p_0, p_{m-1}) \le c(p_0, \ldots, p_{m-1})$. $\square$

**Lemma 4 (the loop).** Let $W = (w_0, w_1, \ldots, w_L)$ with $w_0 = w_L = r$. After the loop of line L5 has read $w_0, \ldots, w_j$, the list $H = (h_1, \ldots, h_k)$ holds the distinct vertices of $w_0, \ldots, w_j$ in the order of their first visit, $h_k$ is the last of these first visits, at an index $j' \le j$, and

$$c(h_1, \ldots, h_k) \le c(w_0, \ldots, w_{j'}).$$

*Proof.* After $w_0 = r$ is read, $H = (r)$ and both sides are 0. Assume the statement after $w_{j-1}$. If $w_j$ is in $H$, line L6 skips it, and $H$, $k$ and $j'$ do not change. If $w_j$ is not in $H$, line L7 appends it, so $h_{k+1} = w_j$ is a first visit, and the new $j'$ is $j$. The old $h_k$ is $w_{j'}$ for the old $j'$, so by Lemma 3 applied to the part $(w_{j'}, \ldots, w_j)$ of $W$,

$$c(h_1, \ldots, h_{k+1}) = c(h_1, \ldots, h_k) + c(w_{j'}, w_j) \le c(w_0, \ldots, w_{j'}) + c(w_{j'}, \ldots, w_j) = c(w_0, \ldots, w_j).$$

$\square$

**Theorem.** DOUBLE-TREE returns a tour $H$, and $c(H) \le 2\,c(T) \le 2(1 - 1/n) \cdot \text{OPT}$.

*Proof.* The walk $W$ visits each vertex, because it uses each edge of the spanning tree $T$. So by Lemma 4, at the end $H$ holds each vertex exactly one time, and $H$ is a tour. Let $h_n = w_{j'}$ be the last first visit. By Lemma 4, $c(h_1, \ldots, h_n) \le c(w_0, \ldots, w_{j'})$. By Lemma 3 on the rest $(w_{j'}, \ldots, w_L)$ of the walk, which ends at $w_L = r = h_1$, the closing edge satisfies $c(h_n, h_1) \le c(w_{j'}, \ldots, w_L)$. The sum gives $c(H) \le c(W)$. By Lemma 2, $c(W) = 2\,c(T)$, and by Lemma 1, $2\,c(T) \le 2(1 - 1/n) \cdot \text{OPT}$. $\blacksquare$

The bound holds for each instance, each minimum spanning tree and each Euler circuit. The wheel example on the page has ALG $= 2n - 2$ and OPT $= n$, so the factor $2(1 - 1/n)$ is reached for each even $n \ge 6$.
