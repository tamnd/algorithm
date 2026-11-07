---
title: Cost of IC(0) and of applying it
proves: [time.worst, space.extra, flops.solve, square_roots.worst]
status: full
---

Let $c$ bound the number of nonzeros in a row of the lower triangle of $A$, so each row of $L$ has at most $c$ entries.

**Factorization.** For row $i$ and each of its at most $c - 1$ off-diagonal positions $j$, L3 intersects the partial row $i$ (at most $c$ entries) with row $j$ (at most $c$ entries); iterating over the smaller one with constant time dictionary lookups costs $O(c)$. L4 is one division. L5 costs $O(c)$ and L7 one square root. So row $i$ costs $O(c^2)$, and the factorization $O(n c^2)$ time with exactly $n$ square roots when it succeeds (at most $n$ in any case).

**Storage.** The rows of $L$ hold $f$ entries; extracting the lower part of row $i$ takes $O(c)$ temporary space. So $\Theta(f)$ extra space.

**Applying $M^{-1}$.** The forward sweep with $L$ does one multiplication and one subtraction per off-diagonal entry and one division per row: $2(f - n) + n$ flops. The backward sweep with $L^T$ does the same: $2(f - n) + n$. Total $4 f - 2 n$ flops. $\blacksquare$
