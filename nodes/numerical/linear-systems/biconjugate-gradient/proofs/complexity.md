---
title: Cost per step of BiCG
proves: [time.worst, space.extra, matvecs.per_step, flops.per_step]
status: full
---

Count flops for one pass of L4 to L10, with $A$ stored with $z$ nonzeros.

- L4: the squared norm $r^T r$ costs $2 n - 1$ flops ($\|b\|_2$ is computed once).
- L5: $A p$ costs at most $2 z$ flops ($z$ multiplications, at most $z$ additions); $A^T \tilde p$ the same $2 z$, as a scatter over the same nonzeros; $\tilde p^T q$ costs $2 n - 1$.
- L6 and L9: two divisions and one inner product $\tilde r^T r$, $2 n + O(1)$.
- L7, L8, L10: five updates of the form $y \leftarrow y + c w$, $2 n$ each, $10 n$ in total.

Sum: $4 z + (2n) + (2n) + (2n) + 10 n + O(1) = 4 z + 16 n + O(1)$ flops, with exactly one product by $A$ and one by $A^T$, so 2 matvecs per step. For $k$ steps plus the initial residual ($2 z + n$) this is $O(k (z + n))$ time.

Space: the vectors $x, r, \tilde r, p, \tilde p, q, \tilde q$ are seven arrays of length $n$, reused across steps, plus $O(1)$ scalars: $\Theta(n)$ besides the matrix, for every $k$. $\blacksquare$
