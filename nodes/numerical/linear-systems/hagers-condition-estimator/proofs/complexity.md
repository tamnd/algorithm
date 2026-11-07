---
title: Cost of Hager's estimator
proves: [time.worst, space.extra, products.worst, flops.worst]
status: full
---

**Products.** Higham's form runs at most $t$ iterations, each with at most one product by $B$ (line L3) and one by $B^T$ (line L6), and line L10 adds one product by $B$. So at most $2 t + 1$ products.

**Flops per product with LU factors.** $B x = U^{-1}(L^{-1}(P x))$: the permutation costs no flops, the unit lower triangular solve $n(n - 1)$ flops and the upper triangular solve $n^2$ flops, so $2 n^2 - n$. The transposed product $B^T x = P^T L^{-T} U^{-T} x$ costs the same. So the products cost at most $(2 t + 1)(2 n^2 - n) \le 4 t n^2 + 2 n^2$ flops.

**Other work.** Per iteration, $\|y\|_1$, $\operatorname{sign}(y)$, the comparison of sign vectors, the index $j$ and $z^T x$ take $O(n)$ operations, and line L10 forms $b$ and its norm in $O(n)$. That is $O(t n)$ in total. Hence $4 t n^2 + 2 n^2 + O(t n)$ flops and $O(t n^2)$ time.

**Space.** The vectors $x$, $y$, the current and previous $\xi$, $z$ and $b$ are each of length $n$: $\Theta(n)$ besides the factors. $\blacksquare$
