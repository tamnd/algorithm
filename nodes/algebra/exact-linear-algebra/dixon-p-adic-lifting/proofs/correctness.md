---
title: Dixon lifting returns the rational solution
proves: [correctness, termination]
status: full
---

Let $A$ be an $n \times n$ integer matrix with columns $a_1, \dots, a_n$, let $b \in \mathbb{Z}^n$, and let $\|v\|$ be the Euclidean norm. Put $H = \prod_j \|a_j\|$, $D = \lfloor H \rfloor + 1$ and $N = \lfloor H \|b\| \rfloor + 1$, the bounds of line L2. The case $n = 0$ is trivial (the empty vector), so let $n \ge 1$.

**Claim.** If $\det A \ne 0$ and line L1 finds a prime $p$ with $p \nmid \det A$, then DIXON$(A, b)$ stops and returns the unique $x \in \mathbb{Q}^n$ with $Ax = b$. If line L1 finds that $\det A \equiv 0$ modulo primes whose product exceeds $D$, then $\det A = 0$ and the answer NONE is correct.

**Line L1.** Over the field $\mathbb{Z}/p\mathbb{Z}$, the matrix $A \bmod p$ is invertible exactly when $\det A \not\equiv 0 \pmod p$, so Gauss-Jordan elimination modulo $p$ either returns $C$ with $CA \equiv AC \equiv I \pmod p$ or reports that $p \mid \det A$. By the Hadamard bound, $|\det A| \le H < D$. If distinct primes $q_1, \dots, q_s$ all divide $\det A$ and $q_1 \cdots q_s > D$, then their product divides $\det A$ and exceeds $|\det A|$, so $\det A = 0$. Conversely, if $\det A \ne 0$, it has finitely many prime factors, so the search over an infinite set of primes stops.

**Termination.** Line L3 picks the least $k$ with $p^k > 2ND$, which exists since $p \ge 2$. The loops of lines L5 and L9 have $k$ and $n$ steps, and the Euclidean algorithm inside line L10 stops because the remainders decrease.

**Lifting invariant.** Let $r_0 = b$, let $y_i$ and $r_{i+1}$ be the values computed in step $i$, and let $\bar{x}_i = \sum_{t < i} y_t p^t$, the value of $\bar{x}$ before step $i$. Then for $0 \le i \le k$, $r_i$ is an integer vector and

$$
A \bar{x}_i + p^i r_i = b. \qquad (\ast)
$$

For $i = 0$ this reads $0 + r_0 = b$. Assume $(\ast)$ for $i$. Line L6 sets $y_i \equiv C r_i \pmod p$, so $A y_i \equiv A C r_i \equiv r_i \pmod p$. Hence $r_i - A y_i$ is divisible by $p$ in every entry, and line L8 gives an integer vector $r_{i+1}$ with $p\, r_{i+1} = r_i - A y_i$. Then

$$
A \bar{x}_{i+1} + p^{i+1} r_{i+1} = A \bar{x}_i + p^i A y_i + p^i (r_i - A y_i) = A \bar{x}_i + p^i r_i = b.
$$

At the end, with $\bar{x} = \bar{x}_k$, $(\ast)$ gives $A \bar{x} \equiv b \pmod{p^k}$.

**The residues are those of the solution.** Let $d = \det A \ne 0$ and let $x$ be the rational solution. By [Cramer's rule](/cramers-rule/), $x_j = \det A_j(b) / d$, where $A_j(b)$ is $A$ with column $j$ replaced by $b$. By the Hadamard bound applied to the columns of $A_j(b)$, $|\det A_j(b)| \le \|b\| \prod_{i \ne j} \|a_i\| \le H \|b\| < N$; the middle step uses $\|a_j\| \ge 1$, which holds because a zero column would make $d = 0$. Write $x_j = s_j / t_j$ in lowest terms with $t_j > 0$. Then $t_j \mid d$, so $|s_j| < N$ and $0 < t_j \le |d| < D$. Since $p \nmid d$, $d$ and $t_j$ are units modulo $p^k$. Multiply $A \bar{x} \equiv b$ by $\operatorname{adj}(A)$: $d \bar{x} \equiv \operatorname{adj}(A) b = d x \pmod{p^k}$, so $\bar{x}_j \equiv \det A_j(b) d^{-1} \equiv s_j t_j^{-1}$, that is,

$$
s_j \equiv t_j \bar{x}_j \pmod{p^k}, \qquad |s_j| \le N, \quad 0 < t_j \le D, \quad 2ND < p^k. \qquad (\ast\ast)
$$

**Rational reconstruction.** Fix $j$ and write $m = p^k$ and $u = \bar{x}_j \bmod m$. The extended Euclidean algorithm on $(m, u)$ produces $r_0 = m$, $r_1 = u$, $t_0 = 0$, $t_1 = 1$ (and $\sigma_0 = 1$, $\sigma_1 = 0$), and $r_{i+1} = r_{i-1} - q_i r_i$, $t_{i+1} = t_{i-1} - q_i t_i$, $\sigma_{i+1} = \sigma_{i-1} - q_i \sigma_i$ with $q_i = \lfloor r_{i-1} / r_i \rfloor$, until $r_\ell = 0$. Standard facts, each by induction on $i$:

- (a) $\sigma_i m + t_i u = r_i$.
- (b) $\sigma_i t_{i+1} - \sigma_{i+1} t_i = \pm 1$.
- (c) For $i \ge 1$ the $t_i$ alternate in sign, and $1 = |t_1| \le |t_2| \le \cdots$. Indeed $t_{i+1} = t_{i-1} - q_i t_i$ with $q_i \ge 1$, and if $t_{i-1}$ and $t_i$ have opposite signs (or $t_{i-1} = 0$), then $|t_{i+1}| = |t_{i-1}| + q_i |t_i| \ge |t_i|$ with the sign opposite to $t_i$.

*Lemma.* Let $\sigma, t$ be integers with $t \ne 0$, and let $j \ge 1$ be the largest index with $|t_j| \le |t|$. Then $|\sigma m + t u| \ge r_j$.

*Proof.* If $j = \ell$, then $r_j = 0$ and there is nothing to prove. Otherwise $|t_{j+1}| > |t|$. By (b), the integer matrix with rows $(\sigma_j, t_j)$ and $(\sigma_{j+1}, t_{j+1})$ has determinant $\pm 1$, so $(\sigma, t) = \alpha (\sigma_j, t_j) + \beta (\sigma_{j+1}, t_{j+1})$ for integers $\alpha, \beta$, and by (a), $\sigma m + t u = \alpha r_j + \beta r_{j+1}$. If $\alpha = 0$, then $t = \beta t_{j+1}$ with $\beta \ne 0$, so $|t| \ge |t_{j+1}|$, which is false. If $\alpha$ and $\beta$ are both nonzero with opposite signs, then $\alpha t_j$ and $\beta t_{j+1}$ have the same sign by (c), so $|t| = |\alpha| |t_j| + |\beta| |t_{j+1}| \ge |t_{j+1}|$, false again. So $\alpha \ne 0$, and $\beta$ is $0$ or has the sign of $\alpha$. Since $r_j, r_{j+1} \ge 0$, $|\alpha r_j + \beta r_{j+1}| = |\alpha| r_j + |\beta| r_{j+1} \ge r_j$. $\square$

Now apply the lemma to $(\ast\ast)$: $s_j = \sigma m + t_j u$ for some integer $\sigma$, so with $J$ the largest index such that $|t_J| \le t_j$, we get $r_J \le |s_j| \le N$. Line L10 stops at the first index $i$ with $r_i \le N$. Since $r_0 = m > 2ND \ge N$, $i \ge 1$, and since $r_J \le N$, $i \le J$. By (c), $1 \le |t_i| \le |t_J| \le t_j \le D$, so the test $|t_i| \le D$ passes. Finally, by (a), $r_i \equiv t_i u$ and $s_j \equiv t_j u \pmod m$, so

$$
s_j t_i - t_j r_i \equiv t_j u\, t_i - t_j t_i u = 0 \pmod m, \qquad |s_j t_i - t_j r_i| \le N D + D N = 2ND < m.
$$

So $s_j t_i = t_j r_i$, and the returned fraction $r_i / t_i$ equals $s_j / t_j = x_j$.

**End.** Line L10 recovers every $x_j$, so line L11 returns the solution $x$, which is unique because $\det A \ne 0$. $\blacksquare$

**Remark.** The bounds $N$ and $D$ in the proof are the only place where the size of the answer enters. Any valid bounds work; smaller ones shorten the lifting, and the early-termination variant replaces them by a check $A x = b$.
