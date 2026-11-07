---
title: Flop count of Gram-Schmidt
proves: [flops.worst, time.worst, space.extra]
status: full
---

Count additions, subtractions, multiplications and divisions; square roots are counted separately.

**MGS.** Pass $j$: line L2 is a squared norm of length $m$, $2m - 1$ flops, plus a square root; line L4 is $m$ divisions; for each of the $n - j$ values of $k$, line L6 is a dot product ($2m - 1$ flops) and line L7 a vector update ($2m$ flops). Summing over $j$:
$$\sum_{j=1}^{n} \bigl( 3m - 1 + (n - j)(4m - 1) \bigr) = n(3m - 1) + \frac{n(n - 1)}{2} (4m - 1) = 2 m n^2 + m n - \frac{n^2 + n}{2},$$
which is $2 m n^2 + O(m n)$, with $n$ square roots.

**CGS.** Column $j$ needs $j - 1$ dot products and $j - 1$ updates of length $m$, the same counts as MGS for the pairs $(i, j)$ with $i < j$, and the same norm and division. So the total is the same: $2 m n^2 + O(m n)$. CGS2 doubles the dot products and updates: $4 m n^2 + O(m n)$.

**Time and space.** Every flop takes constant time, so the time is $\Theta(m n^2)$. Besides $A$, which is overwritten by $Q$, the algorithm stores $R$: $n(n + 1)/2$ numbers, that is $\Theta(n^2)$. $\square$

$\blacksquare$
