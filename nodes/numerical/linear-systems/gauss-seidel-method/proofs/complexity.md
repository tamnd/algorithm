---
title: The number of Gauss-Seidel sweeps for a diagonally dominant matrix
proves: [sweeps.worst, time.worst]
status: full
---

Exact arithmetic, strictly row diagonally dominant $A$, $q = \|G_J\|_\infty < 1$ and $0 < \varepsilon < 1$.

**Claim.** After $k^\ast = \lceil \ln(1/\varepsilon) / \ln(1/q) \rceil$ sweeps, $\|e_{k^\ast}\|_\infty \le \varepsilon \|e_0\|_\infty$. (If $q = 0$, $A$ is diagonal and one sweep gives $e_1 = 0$.)

*Proof.* Theorem 4 of the correctness proof gives $\|e_k\|_\infty \le \eta^k \|e_0\|_\infty \le q^k \|e_0\|_\infty$, and $q^{k^\ast} \le \varepsilon$ as in the Jacobi count. $\square$

**Cost.** A sweep (lines L5 to L7) does, for row $i$ with $z_i$ nonzeros, $z_i - 1$ multiplications, at most $z_i - 2$ additions, one subtraction and one division: $2 z_i$ flops, $2z$ in total. Line L2 does $2z$ more and line L3 does $n$ comparisons. So each pass of the outer loop costs $O(z)$ (as $z \ge n$), and $k^\ast$ of them cost $O(z \ln(1/\varepsilon) / \ln(1/q))$. The only extra storage is the residual $r$, $\Theta(n)$. $\square$

$\blacksquare$
