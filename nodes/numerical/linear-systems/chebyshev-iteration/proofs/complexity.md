---
title: Cost of Chebyshev iteration
proves: [time.worst, space.extra, matvecs.worst, flops.per_step]
status: full
---

**Per step.** L5 is one matvec, at most $2 z$ flops. L6 and L7 are vector additions, $n$ flops each. L8 is $O(1)$. L9 computes $c_1 d + c_2 r$: $3 n$ flops ($2 n$ multiplications, $n$ additions). The squared norm in L4 costs $2 n - 1$ flops. Total $2 z + 7 n + O(1)$ flops.

**Number of steps.** By the corollary of the correctness proof, for symmetric $A$ with spectrum in $[\lambda_{\min}, \lambda_{\max}]$, after $k = \lceil (\sqrt\kappa/2) \ln(2/\varepsilon) \rceil$ steps $\|r_k\|_2 \le \varepsilon \|r_0\|_2$, so with $\mathrm{tol} \cdot \|b\|_2 = \varepsilon \|r_0\|_2$ the L4 test succeeds at the latest at that $k$. Each step is one matvec, so the matvec count is at most $\lceil (\sqrt\kappa/2) \ln(2/\varepsilon) \rceil$ (plus one for $r_0$), and the time is $O((z + n) \sqrt\kappa \ln(2/\varepsilon)) = O(z \sqrt\kappa \ln(2/\varepsilon))$ when every row has a nonzero ($z \ge n$).

**Space.** The vectors $x, r, d, w$ of length $n$ and $O(1)$ scalars: $\Theta(n)$. $\blacksquare$
