---
title: Cost per step of BiCGSTAB
proves: [time.worst, space.extra, matvecs.per_step, flops.per_step]
status: full
---

One pass of L3 to L11, with $A$ stored with $z$ nonzeros:

- Products: $v = A p$ (L4) and $t = A s$ (L7), each at most $2 z$ flops: $4 z$, so 2 matvecs.
- Inner products and squared norms, each $2 n - 1$ flops: $r^T r$ (L3 test), $\hat r^T v$ (L4), $s^T s$ (L6), $t^T s$ and $t^T t$ (L8), $\hat r^T r$ (L10): six, $12 n - 6$.
- Updates: $s = r - \alpha v$ ($2n$), $x \leftarrow x + \alpha p + \omega s$ ($4 n$), $r = s - \omega t$ ($2 n$), $p = r + \beta(p - \omega v)$ ($4 n$): $12 n$.
- Scalars: $O(1)$.

Total $4 z + 24 n + O(1)$ flops. Over $k$ passes plus the initial residual, $O(k (z + n))$ time. Storage: $x, r, \hat r, p, v, s, t$, seven vectors of length $n$ reused at every pass, so $\Theta(n)$ extra space. $\blacksquare$
