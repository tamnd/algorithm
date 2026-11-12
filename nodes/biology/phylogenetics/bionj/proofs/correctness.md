---
title: BIONJ returns the tree of an additive distance matrix, and its weight minimizes the model variance
proves: [correctness]
status: full
---

We prove two things about BIONJ: (1) on the leaf metric of a binary tree with positive edge lengths it returns that tree with its edge lengths, for every value of $\lambda$ in line L7; (2) the $\lambda$ of line L7 minimizes the model variance of the new distances over $[0, 1]$.

**Part 1: exactness.** Let $T$ be an unrooted binary tree with leaf set $X$, $|X| = r \ge 2$, positive edge lengths $w$, and leaf metric $D$. We use induction on $r$, with the hypothesis that BIONJ returns $T$ for every symmetric matrix $V$ that it carries along.

For $r = 2$, line L11 adds the one edge of $T$ with length $D_{ab}$.

For $r \ge 3$, lines L3 and L4 read only $D$, and they are the lines L3 and L4 of [neighbor-joining](/neighbor-joining/). By Lemma 4 of the neighbor-joining proof, every pair that minimizes $Q$ is a cherry $(i, j)$ of $T$, with a common neighbor $p$. By Lemma 5 of the same proof, line L5 gives $\delta_{iu} = w(i, p)$ and $\delta_{ju} = w(j, p)$. For a leaf $k \ne i, j$ the path from $i$ to $k$ and the path from $j$ to $k$ pass through $p$, so
$$D_{ik} - \delta_{iu} = d(p, k) = D_{jk} - \delta_{ju}.$$
Line L8 then gives $D_{uk} = \lambda\, d(p, k) + (1 - \lambda)\, d(p, k) = d(p, k)$, whatever $\lambda$ is. So after line L10 the matrix on the active nodes is the leaf metric of $T'$, the tree $T$ with $i$ and $j$ removed and $p$ renamed $u$. In $T'$ the vertex $p$ has degree 1, the other degrees do not change, and all edge lengths stay positive, so $T'$ is a tree of the same kind with $r - 1$ leaves. The rest of the run is BIONJ on that matrix with some matrix $V$, and by the induction hypothesis it returns $T'$. Adding the edges $(i, p)$ and $(j, p)$ of line L6 gives $T$. $\square$

**Part 2: the weight.** Fix the pair $(i, j)$, the other active nodes $K = A \setminus \{i, j\}$ with $|K| = r - 2$, and write $a_k = V_{ik}$, $b_k = V_{jk}$, $c = V_{ij}$. The model variance of the $r - 2$ new distances is
$$f(\lambda) = \sum_{k \in K} \Big(\lambda^2 a_k + (1 - \lambda)^2 b_k + \lambda (1 - \lambda)(a_k + b_k - c)\Big),$$
where $\frac{1}{2}(a_k + b_k - c)$ is the model covariance of $D_{ik}$ and $D_{jk}$. Expand one term: the coefficient of $\lambda^2$ is $a_k + b_k - (a_k + b_k - c) = c$, the coefficient of $\lambda$ is $-2 b_k + (a_k + b_k - c) = a_k - b_k - c$, and the constant is $b_k$. So
$$f(\lambda) = (r - 2)\, c\, \lambda^2 + \Big(\sum_{k} (a_k - b_k) - (r - 2) c\Big) \lambda + \sum_k b_k.$$

If $c = 0$, $f$ is linear and line L7 takes $\lambda = 1/2$; the algorithm does not claim optimality in this case. If $c > 0$, $f$ is a parabola that opens upward, and its minimum over the real line is at
$$\lambda^* = \frac{(r - 2) c - \sum_k (a_k - b_k)}{2 (r - 2) c} = \frac{1}{2} + \frac{\sum_{k \in K} (V_{jk} - V_{ik})}{2 (r - 2) V_{ij}},$$
which is the formula of line L7. A convex function of one variable decreases up to its minimum and increases after it, so the minimum over $[0, 1]$ is at $\lambda^*$ clipped to $[0, 1]$, which is what line L7 returns.

Finally, the value of line L9 is the term of $f$ for $k$: $\lambda^2 a_k + (1 - \lambda)^2 b_k + \lambda(1 - \lambda)(a_k + b_k - c) = \lambda a_k (\lambda + 1 - \lambda) + (1 - \lambda) b_k (1 - \lambda + \lambda) - \lambda (1 - \lambda) c = \lambda a_k + (1 - \lambda) b_k - \lambda (1 - \lambda) c$. So $V_{uk}$ is the model variance of the new distance $D_{uk}$. $\blacksquare$
