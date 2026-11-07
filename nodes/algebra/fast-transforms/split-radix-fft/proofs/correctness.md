---
title: SPLIT-RADIX-FFT computes the DFT of length 2^m with n lg n additions and (n/2) lg n − n + 1 multiplications
proves: [correctness, complexity]
status: full
---

**Statement.** Let $R$ be a commutative ring, $n = 2^m$ with $m \ge 0$, and $\omega \in R$ with $\omega^{n/2} = -1$ if $n \ge 2$ (any $\omega$ if $n = 1$). For every $x \in R^n$, SPLIT-RADIX-FFT$(x, \omega)$ returns $X$ with $X_k = \sum_{j=0}^{n-1} x_j \omega^{jk}$ for $0 \le k < n$. It does exactly $A(n) = n \lg n$ additions and subtractions and exactly

$$T(n) = \tfrac13 n \lg n - \tfrac89 n + 1 - \tfrac19 (-1)^m, \qquad G(n) = \tfrac16 n \lg n - \tfrac19 n + \tfrac19 (-1)^m$$

multiplications by twiddle factors (line L8) and by $J$ (line L9), so $T(n) + G(n) = \frac n2 \lg n - n + 1$ multiplications in all.

**The hypothesis is inherited.** If $n \ge 2$ then $\omega^n = (\omega^{n/2})^2 = 1$. If $n \ge 4$, the call at line L3 has length $n/2$ and root $\omega^2$, and $(\omega^2)^{(n/2)/2} = \omega^{n/2} = -1$; the calls at lines L4 and L5 have length $n/4$ and root $\omega^4$, and if $n/4 \ge 2$ then $(\omega^4)^{(n/4)/2} = \omega^{n/2} = -1$. So every recursive call satisfies the hypothesis of the statement.

**Lemma 1 (the splitting).** Let $n \ge 4$, $q = n/4$, and let $U_k = \sum_{j<2q} x_{2j} \omega^{2jk}$, $Z_k = \sum_{j<q} x_{4j+1} \omega^{4jk}$ and $Z'_k = \sum_{j<q} x_{4j+3} \omega^{4jk}$, defined for all integers $k \ge 0$. Then for every $k \ge 0$,

$$X_k = U_k + \omega^k Z_k + \omega^{3k} Z'_k,$$

and $U$ has period $2q$ and $Z, Z'$ have period $q$ in $k$.

*Proof.* Each $j \in [0, n)$ is even, or $1$ or $3$ modulo $4$, and in exactly one way of the form $2j'$, $4j' + 1$ or $4j' + 3$. So $X_k$ is the sum of $\sum_{j'} x_{2j'} \omega^{2j'k}$, $\sum_{j'} x_{4j'+1} \omega^{(4j'+1)k} = \omega^k Z_k$ and $\sum_{j'} x_{4j'+3} \omega^{(4j'+3)k} = \omega^{3k} Z'_k$. The periods follow from $\omega^{2 \cdot 2q} = \omega^n = 1$ and $\omega^{4q} = \omega^n = 1$. $\square$

**Lemma 2 (the L-shaped butterfly).** With $J = \omega^{q}$ and $0 \le k < q$, put $a = \omega^k Z_k$, $b = \omega^{3k} Z'_k$, $s = a + b$ and $d = J(a - b)$. Then

$$X_k = U_k + s, \quad X_{k + 2q} = U_k - s, \quad X_{k+q} = U_{k+q} + d, \quad X_{k+3q} = U_{k+q} - d.$$

*Proof.* We have $J^2 = \omega^{n/2} = -1$, so $J^3 = -J$ and $J^4 = 1$. Apply Lemma 1 at $k + rq$ for $r = 0, 1, 2, 3$. By the periods, $Z_{k + rq} = Z_k$ and $Z'_{k+rq} = Z'_k$, and $U_{k + 2q} = U_k$, $U_{k + 3q} = U_{k+q}$. The twiddle factors are $\omega^{k + rq} = J^r \omega^k$ and $\omega^{3(k + rq)} = J^{3r} \omega^{3k}$. For $r = 0$ this gives $X_k = U_k + a + b$. For $r = 2$, $J^2 = J^6 = -1$, so $X_{k+2q} = U_k - a - b$. For $r = 1$, $J^3 = -J$, so $X_{k+q} = U_{k+q} + J a - J b = U_{k+q} + d$. For $r = 3$, $J^3 = -J$ and $J^9 = J$, so $X_{k+3q} = U_{k+q} - J a + J b = U_{k+q} - d$. $\square$

**Correctness.** By induction on $m$. For $n = 1$, line L1 returns $x$, and $X_0 = x_0$. For $n = 2$, $\omega = \omega^{n/2} = -1$, so $X_0 = x_0 + x_1$ and $X_1 = x_0 - x_1$, which line L2 returns. Let $n \ge 4$. The recursive calls satisfy the hypothesis and are on shorter inputs, so by induction lines L3, L4 and L5 compute the sequences $U$ (for $0 \le k < 2q$), $Z$ and $Z'$ (for $0 \le k < q$) of Lemma 1: line L3 gets the DFT of $(x_{2j})$ with root $\omega^2$, and lines L4 and L5 get those of $(x_{4j+1})$ and $(x_{4j+3})$ with root $\omega^4$. Line L6 sets $J = \omega^q$. At $k = 0$ the factors $\omega^0$ are $1$, so line L8 sets $a = Z_0$ and $b = Z'_0$ without a product, which are the values of Lemma 2. By Lemma 2, lines L9 to L11 write the correct values to positions $k, k + q, k + 2q, k + 3q$. As $k$ runs over $[0, q)$ and $r$ over $\{0, 1, 2, 3\}$, $k + rq$ runs over $[0, n)$ exactly once (division by $q$). So line L12 returns $X$.

**Inverse.** If $n$ is a unit and $\omega$ is a principal $n$-th root of unity (for example, $R$ a field, where $\omega$ has order exactly $n$ because $\omega^{n/2} = -1 \ne 1$), then $\omega^{-1}$ also satisfies $(\omega^{-1})^{n/2} = -1$, and the procedure with $\omega^{-1}$ followed by division by $n$ inverts the DFT, as shown on the page of the [inverse discrete Fourier transform](/inverse-discrete-fourier-transform/).

**Operation count.** For $n \ge 4$ each iteration of lines L7 to L11 does $6$ additions and subtractions ($a + b$, $a - b$ and four at lines L10 and L11), one product by $J$, and two twiddle products unless $k = 0$. With $q = n/4$ iterations, the recurrences are

$$A(n) = A(n/2) + 2A(n/4) + \tfrac32 n, \quad T(n) = T(n/2) + 2T(n/4) + \tfrac n2 - 2, \quad G(n) = G(n/2) + 2 G(n/4) + \tfrac n4,$$

for $n \ge 4$, with $A(1) = 0$, $A(2) = 2$, and $T$ and $G$ zero at $n = 1, 2$, since lines L1 and L2 do no multiplications. Each recurrence determines its function from its two initial values, so it suffices to check that the claimed formulas take these values and satisfy the recurrences. Write $\epsilon = (-1)^m$, so $(-1)^{m-1} = -\epsilon$ and $(-1)^{m-2} = \epsilon$.

- $A$: $n \lg n$ is $0$ at $n = 1$ and $2$ at $n = 2$, and $\frac n2 (m - 1) + 2 \cdot \frac n4 (m - 2) + \frac32 n = nm - \frac n2 - n + \frac32 n = nm$.
- $T$: at $n = 1$, $0 - \frac89 + 1 - \frac19 = 0$; at $n = 2$, $\frac23 - \frac{16}{9} + 1 + \frac19 = 0$. And $T(n/2) + 2T(n/4) = \frac16 n (m-1) - \frac49 n + 1 + \frac19 \epsilon + \frac16 n (m - 2) - \frac49 n + 2 - \frac29 \epsilon = \frac13 nm - \frac12 n - \frac89 n + 3 - \frac19 \epsilon$; adding $\frac n2 - 2$ gives $T(n)$.
- $G$: at $n = 1$, $0 - \frac19 + \frac19 = 0$; at $n = 2$, $\frac13 - \frac29 - \frac19 = 0$. And $G(n/2) + 2G(n/4) = \frac1{12} n(m - 1) - \frac1{18} n - \frac19 \epsilon + \frac1{12} n (m - 2) - \frac1{18} n + \frac29 \epsilon = \frac16 nm - \frac14 n - \frac19 n + \frac19 \epsilon$; adding $\frac n4$ gives $G(n)$.

Adding, $T(n) + G(n) = \frac12 n \lg n - n + 1$.

**Time and space.** Each call does $O(1)$ work besides its counted operations and its loop, and the number of calls $C(n) = 1 + C(n/2) + 2C(n/4)$ with $C(1) = C(2) = 1$ is $O(n)$ (by induction, $C(n) \le 2n - 1$, since $1 + (n - 1) + 2(\frac n2 - 1) = 2n - 2$). So the time is $\Theta(n \log n)$. A call of length $n$ holds its three partial results and its output, $O(n)$ entries, while it runs; along a root-to-leaf path the lengths at least halve, so the live storage is $O(n + n/2 + \ldots) = O(n)$, plus the table of $n$ powers and a recursion stack of depth $\lg n$. The extra space is $\Theta(n)$. $\blacksquare$
