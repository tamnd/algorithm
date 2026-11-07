---
title: The number of Jacobi sweeps for a diagonally dominant matrix
proves: [sweeps.worst, time.worst]
status: full
---

Exact arithmetic. Assume $A$ is strictly row diagonally dominant, so $q = \|G_J\|_\infty < 1$ (Theorem 3 of the correctness proof), and let $0 < \varepsilon < 1$.

**Claim.** After $k^\ast = \lceil \ln(1/\varepsilon) / \ln(1/q) \rceil$ sweeps, $\|e_{k^\ast}\|_\infty \le \varepsilon \|e_0\|_\infty$. (If $q = 0$, one sweep gives $e_1 = 0$.)

*Proof.* By Theorem 3, $\|e_k\|_\infty \le q^k \|e_0\|_\infty$. For $0 < q < 1$, $q^k \le \varepsilon$ is equivalent to $k \ln(1/q) \ge \ln(1/\varepsilon)$, which holds for $k = k^\ast$. $\square$

**Cost per sweep.** For each row $i$ with $z_i$ nonzeros (diagonal included), line L3 does $z_i - 1$ multiplications and $z_i - 2$ additions, line L4 two subtractions and a multiplication, and line L8 a subtraction and a division. That is $2 z_i + 3$ flops, so $2z + 3n = O(z)$ per sweep since $z \ge n$, plus $n$ comparisons for the norm in line L5. Each nonzero of $A$ is read once per sweep. With $k^\ast$ sweeps the time is $O(z \ln(1/\varepsilon) / \ln(1/q))$. The extra storage is the vectors $s$ and $r$, that is $\Theta(n)$. $\square$

$\blacksquare$
