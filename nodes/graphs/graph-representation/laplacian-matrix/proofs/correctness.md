---
title: The Laplacian operations keep the degree invariant and compute Lx and the quadratic form
proves: [correctness]
status: full
---

We use the pseudocode of the page. The graph has the vertices $0, \ldots, n - 1$ and a multiset $E$ of edges $\{u, v\}$ with $u \ne v$ and weights $w > 0$. Let $W_{uv}$ be the sum of the weights of the edges between $u$ and $v$ (so $W_{uu} = 0$), let $D_{uu} = \sum_v W_{uv}$, and let $L = D - W$. The invariant is:

> **(I)** For each vertex $u$, `deg[u]` $= D_{uu}$, and `adj[u]` holds exactly one pair $(v, w)$ for each edge of $E$ with ends $u$ and $v$ and weight $w$.

**Initialization.** With $E$ empty, `deg` is all zeros and every list is empty, so (I) holds.

**ADD-EDGE.** Let the new edge be $\{u, v\}$ with weight $w$. Line L1 adds $w$ to `deg[u]` and to `deg[v]`, which is the change of $D_{uu}$ and $D_{vv}$; no other degree changes, because the edge has no other end. Lines L2 and L3 add the pair $(v, w)$ to `adj[u]` and $(u, w)$ to `adj[v]`, one pair at each end and nothing else. So (I) holds for $E \cup \{\{u, v\}\}$.

**Reading the matrix.** By (I), for $u \ne v$ the sum of $w$ over the pairs $(v, w)$ of `adj[u]` is $W_{uv}$, so $L_{uv} = -W_{uv}$ is this sum negated, and $L_{uu} = D_{uu} - W_{uu} = $ `deg[u]`. This is what ENTRY returns.

**MULTIPLY.** Fix $u$. Line L5 sets $y_u = D_{uu} x_u$. Lines L6 and L7 then subtract $w x_v$ once for each pair of `adj[u]`, which by (I) subtracts $\sum_v W_{uv} x_v$. So after the inner loop $y_u = D_{uu} x_u - \sum_v W_{uv} x_v = \sum_v L_{uv} x_v = (Lx)_u$. The outer loop of line L4 does this for each $u$, and line L8 returns $y = Lx$.

**QUADRATIC-FORM.** By (I), each edge $e = \{u, v\}$ gives one pair in `adj[u]` and one in `adj[v]`, and the test $u < v$ of line L11 keeps exactly one of them. So line L13 returns $s = \sum_{e \in E} w(e) (x_u - x_v)^2$. Expanding the square,

$$s = \sum_{e} w(e) (x_u^2 + x_v^2) - 2 \sum_{e} w(e) x_u x_v = \sum_u D_{uu} x_u^2 - \sum_{u, v} W_{uv} x_u x_v = x^T L x,$$

because each edge adds $w(e)$ to the squares of its two ends, and the double sum over ordered pairs counts each edge twice.

**Consequences.** Since $s \ge 0$, $L$ is positive semidefinite. If $Lx = 0$ then $x^T L x = 0$, so $x_u = x_v$ for every edge, as all weights are positive, and $x$ is constant on each connected component. Conversely, if $x$ is constant on each component then each term of $(Lx)_u = \sum_v W_{uv}(x_u - x_v)$ is zero. So the kernel of $L$ is spanned by the indicator vectors of the $c$ components, which are linearly independent, and $\operatorname{rank} L = n - c$. This is what `components` computes by exact elimination.

**Cost.** ADD-EDGE does $O(1)$ amortized work. MULTIPLY and QUADRATIC-FORM read each of the $n$ degrees once and each of the $2|E|$ pairs once, so they take $\Theta(n + m)$ time. $\blacksquare$
