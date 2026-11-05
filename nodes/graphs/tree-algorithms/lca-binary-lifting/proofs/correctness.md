---
title: LCA by binary lifting returns the lowest common ancestor
proves: [correctness, termination]
status: full
---

Let the tree have the vertices $0, \ldots, n-1$ and the root $r$. Write $depth(x)$ for the number of edges from $r$ to $x$, $p(x)$ for the parent of $x$ with $p(r) = r$, and $p^j(x)$ for $p$ applied $j$ times. For $0 \le j \le depth(x)$, $p^j(x)$ is the ancestor of $x$ at distance $j$; for $j > depth(x)$ it is $r$. A vertex is an ancestor of itself. For vertices $u, v$, $\mathrm{lca}(u, v)$ is the deepest common ancestor; it exists because $r$ is a common ancestor, and it is unique because the common ancestors of $u$ and $v$ all lie on the path from $u$ to $r$, which has at most one vertex at each depth.

**Lemma 1 (the table).** After PREPROCESS, $up[k][x] = p^{2^k}(x)$ for each $0 \le k < K$ and each vertex $x$.

*Proof.* Line L1 computes $p$ and $depth$ by BFS, which visits the vertices in order of distance from $r$ and sets the parent of each vertex to the vertex from which it is first reached, a vertex one level closer to $r$. Line L3 gives $up[0][x] = p(x) = p^1(x)$. For $k \ge 1$, the loop of line L4 runs after level $k - 1$ is complete, and by the induction hypothesis on $k$, $up[k][x] = p^{2^{k-1}}(p^{2^{k-1}}(x)) = p^{2^k}(x)$. $\square$

**Lemma 2 (lifting and the LCA).** (a) If $depth(u) \ge depth(v)$ and $d = depth(u) - depth(v)$, then $\mathrm{lca}(p^d(u), v) = \mathrm{lca}(u, v)$. (b) If $depth(u) = depth(v)$, then for each $j \ge 0$, $p^j(u) = p^j(v)$ if and only if $j \ge depth(u) - depth(\mathrm{lca}(u, v))$.

*Proof.* (a) The common ancestors of $u$ and $v$ have depth at most $depth(v)$, since each is an ancestor of $v$. The ancestors of $u$ with depth at most $depth(v)$ are exactly the ancestors of $p^d(u)$. So $u$ and $p^d(u)$ have the same common ancestors with $v$, and the same deepest one. (b) Let $\ell = \mathrm{lca}(u, v)$ and $t = depth(u) - depth(\ell)$. If $j \ge t$, both $p^j(u)$ and $p^j(v)$ are the ancestor of $\ell$ at distance $j - t$ (or $r$), so they are equal. If $j < t$ and $p^j(u) = p^j(v) = x$, then $x$ is a common ancestor of $u$ and $v$ with $depth(x) = depth(u) - j > depth(\ell)$, which contradicts the choice of $\ell$. $\square$

**Theorem.** LCA$(u, v)$ returns $\mathrm{lca}(u, v)$, after $O(K)$ steps.

*Proof.* Write $\ell = \mathrm{lca}(u, v)$ for the original pair. After line L5, $depth(u) \ge depth(v)$, and the pair is the same set, so $\ell$ is unchanged.

*Line L7.* Let $d = \sum_{k \in B} 2^k$, where $B$ is the set of one bits of $d$. Since $d \le n - 1 < 2^K$, $B \subseteq \{0, \ldots, K-1\}$. By Lemma 1 each jump applies $p^{2^k}$, and $p^a(p^b(x)) = p^{a+b}(x)$, so after line L7, $u$ is $p^d$ of the original $u$. By Lemma 2(a), $\mathrm{lca}(u, v) = \ell$ still, and now $depth(u) = depth(v)$.

*Line L8.* If $u = v$, then $u$ is an ancestor of both original vertices at the depth of $v$, and $\ell = \mathrm{lca}(u, u) = u$. The return is correct.

*Lines L9 and L10.* Now $u \ne v$ and $depth(u) = depth(v)$. Let $t = depth(u) - depth(\ell) \ge 1$, the distance from $u$ (and from $v$) up to $\ell$, and let $s = t - 1 \ge 0$. We claim this invariant before the step for $k$ (for $k = K - 1, \ldots, 0$), and after the step for $k = 0$ with $k = -1$:

> **(I)** $u \ne v$, $depth(u) = depth(v)$, $\mathrm{lca}(u, v) = \ell$, and $s < 2^{k+1}$.

*Initialization.* Before the step for $k = K - 1$: the first three parts hold as shown. Also $s < t \le depth(u) \le n - 1 < 2^K$.

*Maintenance.* Consider the step for $k$. By Lemma 1, $up[k][u] = p^{2^k}(u)$ and $up[k][v] = p^{2^k}(v)$. By Lemma 2(b), these differ if and only if $2^k < t$, that is $2^k \le s$.

If $2^k \le s$, line L10 sets $u \gets p^{2^k}(u)$ and $v \gets p^{2^k}(v)$. The new vertices differ, have equal depth, and are ancestors of the old ones below $\ell$ (their distance to $\ell$ is $t - 2^k \ge 1$), so $\ell$ is still their LCA by Lemma 2(b) applied to the old pair. The new $s$ is $s - 2^k < 2^{k+1} - 2^k = 2^k$.

If $2^k > s$, nothing changes, and $s < 2^k$ already.

In both cases (I) holds with $k - 1$ in place of $k$.

*Termination.* The loop has exactly $K$ steps. After the step for $k = 0$, (I) gives $s < 2^0 = 1$, so $s = 0$ and $t = 1$: $\ell$ is the parent of $u$. Line L11 returns $up[0][u] = p(u) = \ell$.

The number of steps is at most $K$ for line L7 and exactly $K$ for line L9, each of $O(1)$ work. $\blacksquare$
