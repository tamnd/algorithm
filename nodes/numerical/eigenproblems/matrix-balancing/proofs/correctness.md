---
title: Balancing is an exact similarity, lowers the off-diagonal mass at every step, and terminates
proves: [correctness, termination]
status: full
---

Notation of the page: $B$ is the current matrix, $c_i = \sum_{j \ne i} |b_{ji}|$, $r_i = \sum_{j \ne i} |b_{ij}|$, $S(B) = \sum_{i \ne j} |b_{ij}|$, $\beta \ge 2$ the radix (an integer power of 2 in the implementation, so that it is the machine radix or a power of it), and $d_i = \beta^{e_i}$. Lemmas 2 to 5 use exact values of $c$ and $r$; the remark at the end covers their rounding.

**Lemma 1 (exact similarity).** Suppose no entry overflows or underflows. After any number of accepted steps, the stored matrix equals $D^{-1} A D$ exactly, with $D = \operatorname{diag}(d)$, and $\det(tI - B) = \det(tI - A)$.

*Proof.* Line L9 multiplies the entries of column $i$ by $f = \beta^m$ and divides those of row $i$ by $f$; the diagonal entry $b_{ii}$ is multiplied and divided, so it is unchanged. Multiplying a binary floating-point number by a power of 2 changes only its exponent, so in the absence of overflow and underflow every such product is exact. The step therefore replaces $B$ by $F^{-1} B F$ exactly, with $F = \operatorname{diag}(1, \dots, f, \dots, 1)$ in position $i$, and multiplies $d_i$ by $f$, again exactly. By induction the stored matrix is $D^{-1} A D$ with $D = \operatorname{diag}(d)$. Finally $\det(tI - D^{-1} A D) = \det(D^{-1} (tI - A) D) = \det(tI - A)$. $\square$

**Lemma 2 (the choice of f).** Let $c, r > 0$. Line L7 returns the power $f = \beta^m$ with $r / \beta \le c f^2 < r \beta$, and this $f$ minimizes $g(f) = c f + r / f$ over all integer powers of $\beta$.

*Proof.* Let $c_0 = c$. The first loop multiplies $f$ by $\beta$ and $c$ by $\beta^2$ while $c < r / \beta$, so at its end $c = c_0 f^2 \ge r / \beta$; if it ran at least once, the value before the last step was below $r / \beta$, so $c_0 f^2 < r \beta$. The second loop divides $f$ by $\beta$ and $c$ by $\beta^2$ while $c \ge r \beta$; if it runs, the first loop did not, and it stops at the first value below $r \beta$, which is at least $r \beta / \beta^2 = r / \beta$. Both loops stop after finitely many steps, since each multiplies $c$ by $\beta^{\pm 2}$. In all cases $r / \beta \le c_0 f^2 < r \beta$.

For optimality write $x = c_0 f^2 / r$, so $g(f) = (r / f)(x + 1) = \sqrt{c_0 r} \, h(x)$ with $h(x) = \sqrt x + 1 / \sqrt x$. The function $h$ is decreasing on $(0, 1]$, increasing on $[1, \infty)$ and satisfies $h(x) = h(1 / x)$, so $h(x) \le h(y)$ whenever $|\log x| \le |\log y|$. The other powers of $\beta$ give $y = x \beta^{2j}$ with $j \ne 0$. Since $|\log x| \le \log \beta$ and $|\log x + 2 j \log \beta| \ge 2 |j| \log\beta - |\log x| \ge \log \beta$, every other power gives a value at least $g(f)$. $\square$

**Lemma 3 (descent).** An accepted step at index $i$ lowers $S$ by more than $0.05 (c_i + r_i) > 0$.

*Proof.* The step changes only the off-diagonal entries of column $i$ (multiplied by $f$) and of row $i$ (divided by $f$); these sets are disjoint and their masses are $c_i$ and $r_i$. All other off-diagonal entries are unchanged. So $S$ changes by $(c_i f + r_i / f) - (c_i + r_i)$, which is below $-0.05 (c_i + r_i)$ by the test of line L8. Line L6 ensures $c_i, r_i > 0$. $\square$

**Theorem 4 (correctness).** When the algorithm returns, $B = D^{-1} A D$ exactly, $D$ has powers of $\beta$ on the diagonal, $\operatorname{spec}(B) = \operatorname{spec}(A)$ with multiplicities, $S(B) \le S(A)$, and if $y$ is an eigenvector of $B$ then $D y$ is an eigenvector of $A$ for the same eigenvalue. If it returns CONVERGED, then for every $i$ with $c_i r_i \ne 0$ and every integer $m$, $c_i \beta^m + r_i \beta^{-m} \ge 0.95 (c_i + r_i)$.

*Proof.* The first statements are Lemma 1 and Lemma 3. If $B y = \lambda y$ then $A (D y) = D B y = \lambda D y$, and $Dy \ne 0$. On CONVERGED the last sweep accepted no step, so the matrix did not change during it, and for every $i$ with $c_i r_i \ne 0$ the test of line L8 failed for the $f$ of line L7: $c_i f + r_i / f \ge 0.95 (c_i + r_i)$. By Lemma 2 every other power of $\beta$ gives a value at least as large. $\square$

**Theorem 5 (termination).** The algorithm returns after at most $\mathrm{maxsweeps}$ sweeps, each of which takes finitely many operations. If $A$ is irreducible, there is a finite number of sweeps after which it returns CONVERGED, independent of the cap.

*Proof.* The outer loop of line L2 runs at most $\mathrm{maxsweeps}$ times, and each sweep runs $n$ iterations of line L4, each finite by Lemma 2. Now let $A$ be irreducible. Every matrix that occurs is $B = D^{-1} A D$ with $b_{jk} = a_{jk} \beta^{e_k - e_j}$, so $B$ is determined by the integer differences $e_k - e_j$. For an edge $j \to k$ of the graph of $A$ ($a_{jk} \ne 0$, $j \ne k$), Lemma 3 gives $|a_{jk}| \beta^{e_k - e_j} \le S(B) \le S(A)$, so $e_k - e_j \le M_{jk} = \log_\beta (S(A) / |a_{jk}|)$. Since $A$ is irreducible, for any $j \ne k$ there are paths $j \to \dots \to k$ and $k \to \dots \to j$ in the graph, and summing the bounds along them bounds $e_k - e_j$ from above and from below by constants that depend only on $A$. So only finitely many matrices $B$ can occur. By Lemma 3, $S$ strictly decreases at each accepted step, so no matrix occurs twice, and the number of accepted steps is finite. After the last accepted step, the next full sweep accepts nothing and line L10 returns CONVERGED. $\square$

**Remark (rounding in the norms).** The implementation computes $c$ and $r$ in floating point, with relative errors at most $(n - 1) u$ to first order. The test of line L8 then holds for the computed values only if the exact values satisfy $c f + r / f < 0.95 \, (1 + 2 n u) / (1 - 2 n u) \, (c + r)$, which is still below $c + r$ for $n u < 0.01$, so Lemma 3 holds with $0.05$ replaced by a slightly smaller constant, and Theorem 5 is unaffected. Lemma 1 does not depend on the norms at all.
