---
title: Operation count of GMRES
proves: [time.worst, time.restarted, space.extra, space.restarted, matvecs.worst, flops.worst]
status: full
---

Count flops (one addition or multiplication each) for $k$ Arnoldi steps on an $n \times n$ matrix with $z$ nonzeros, with the dense helpers replaced by CSR products as in the implementation.

**Step $j$ (L4 to L8).** L4 is one matvec: $z$ multiplications and at most $z$ additions, so $2 z$ flops. L5 performs $j$ inner products ($2 n - 1$ flops each) and $j$ updates $w \leftarrow w - h v$ ($2 n$ flops each): $j(4 n - 1)$ flops. L6 is a norm and a scaling, $3 n + O(1)$ flops and one square root. L7 applies $j - 1$ rotations to a column and forms one, $6 j + O(1)$ flops, independent of $n$. Total for step $j$: $2 z + 4 j n + O(n + j)$.

**Full GMRES, $k$ steps.** Summing, $\sum_{j=1}^{k} (2 z + 4 j n + O(n)) = 2 k z + 2 k(k+1) n + O(k n) = 2 k z + 2 k^2 n + O(k n)$ flops. L9 adds $k^2$ flops for the triangular solve and $2 k n$ for $V_k y$, and L1 a matvec and $O(n)$. So the flop count is $2 k z + 2 k^2 n + O(k n)$, the number of matvecs is $k$ (plus one per restart for $r_0$), and the time is $O(k z + k^2 n)$.

**Restarted, GMRES($m$).** Each cycle has at most $m$ steps, and in step $j \le m$ the Gram-Schmidt cost is $4 j n \le 4 m n$; so $k$ steps in total cost at most $2 k z + 4 k m n + O(k n)$ flops, which is $O(k z + k m n)$, plus $\lceil k/m \rceil$ extra matvecs for the restarts.

**Space.** The basis $v_1, \dots, v_{j+1}$ takes $(j + 1) n$ words, $H$ and the rotations $O(j^2)$, and $x$, $r$, $w$ another $3 n$. With $j \le k$ this is $\Theta(k n)$ for $k \le n$ (the basis is stored in full, so the bound is attained), and with $j \le m$ it is $\Theta(m n)$. $\blacksquare$
