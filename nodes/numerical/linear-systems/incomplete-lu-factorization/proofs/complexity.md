---
title: Cost of ILU and of applying it
proves: [time.worst, space.extra, flops.solve]
status: full
---

Let $c$ bound the number of entries of any working row $w$ (for ILU(0), the number of nonzeros in a row of $A$, since no fill is created).

**Factorization.** Row $i$: building $w$ and its heap costs $O(c)$. At most $c$ columns are popped, each pop $O(\log c)$. Each processed multiplier $k$ costs one division (L3) and one pass over the stored row $U_k$, which has at most $c$ entries (it was a working row), with $O(1)$ work per entry including the dictionary lookup in L5 and L6. So row $i$ costs $O(c \log c + c \cdot c) = O(c^2)$ and the whole factorization $O(n c^2)$. L7 costs $O(c)$ per row.

**Storage.** The kept rows of $L$ and $U$ hold $f$ entries plus levels for $U$, and the working row $O(c) \le O(f)$: $\Theta(f)$ extra space.

**Applying $M^{-1}$.** The forward sweep does one multiplication and one subtraction per stored entry of $L$: $2 \operatorname{nnz}(L)$ flops. The backward sweep does the same for the off-diagonal entries of $U$ and one division per row: $2(\operatorname{nnz}(U) - n) + n$. Total $2(\operatorname{nnz}(L) + \operatorname{nnz}(U)) - n = 2 f - n$ flops. $\blacksquare$
