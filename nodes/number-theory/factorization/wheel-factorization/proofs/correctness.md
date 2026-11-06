---
title: Correctness of wheel factorization
proves: [correctness, termination]
status: full
---

Let $N \ge 1$, let $p_1 < \cdots < p_k$ be the first $k$ primes, $W = p_1 \cdots p_k$ (with $W = 1$ for $k = 0$), and let $s$ be the least integer greater than $1$ with $\gcd(s, W) = 1$.

**Lemma 1 (the wheel lists the right numbers).** The values that $d$ takes at line L5 are exactly the integers $t \ge s$ with $\gcd(t, W) = 1$, in increasing order.

*Proof.* Since $\gcd(t, W) = \gcd(t \bmod W, W)$, the set $C = \{t \ge s : \gcd(t, W) = 1\}$ is invariant under $t \mapsto t + W$. Its elements in $[s, s + W)$ are $r_0 = s < r_1 < \cdots < r_{\varphi - 1}$, where $\varphi = \varphi(W)$. So the elements of $C$ in increasing order are $r_0, r_1, \dots, r_{\varphi - 1}, r_0 + W, r_1 + W, \dots$, and the gap from each to the next is $g_j = r_{j+1} - r_j$ for $j < \varphi - 1$ and $g_{\varphi - 1} = r_0 + W - r_{\varphi - 1}$ at the end of a period. Line L4 sets $d = r_0$, $i = 0$, and line L7 adds $g_i$ and advances $i$ modulo $\varphi$; by induction, after $t$ steps $d$ is the $t$-th element of $C$ (counted from $0$) and $i = t \bmod \varphi$. $\square$

**Lemma 2.** Every prime $q$ that is not a wheel prime is in $C$, and every prime less than $s$ is a wheel prime.

*Proof.* A prime $q$ that is not among $p_1, \dots, p_k$ does not divide $W$, so $\gcd(q, W) = 1$. As $q > 1$, the minimality of $s$ gives $q \ge s$, so $q \in C$. The second claim is the contrapositive. $\square$

**Invariant.** Each time line L5 is reached: (a) $N = (\prod F) \cdot m$; (b) $F$ is a list of primes in non-decreasing order, each less than $d$; (c) no prime less than $d$ divides $m$.

*Initialization.* After lines L1 to L3, $F$ holds each wheel prime as often as it divides $N$, in increasing order, and $m = N / \prod F$, so (a) holds and $m$ has no wheel prime as a factor. Line L4 sets $d = s$. Each wheel prime is less than $s$ (it divides $W$, so it is not coprime to $W$, and the primes are less than $p_{k+1} = s$ when the basis is the first $k$ primes). So (b) holds. Every prime less than $s$ is a wheel prime by Lemma 2, so (c) holds.

*Maintenance.* Suppose the invariant holds and $d^2 \le m$. First, if $d \mid m$, then $d$ is prime: $d \ge s \ge 2$, and a prime factor $q$ of $d$ divides $m$, so $q \ge d$ by (c), which forces $q = d$. The inner loop of line L6 divides $m$ by $d$ while possible and appends $d$ each time, which keeps (a), keeps the order in (b) because every earlier entry is less than $d$, and leaves $d \nmid m$. Line L7 moves $d$ to $d'$, the next element of $C$ (Lemma 1). The entries of $F$ are at most $d < d'$, so (b) holds. For (c), let $q < d'$ be a prime. If $q$ is a wheel prime, it does not divide $m$ (it was removed in lines L2 and L3, and $m$ only shrinks by other factors). Otherwise $q \in C$ by Lemma 2, and $q < d'$ means $q \le d$ since no element of $C$ lies strictly between $d$ and $d'$. If $q < d$, (c) before the step gives $q \nmid m$; if $q = d$, line L6 removed it. Dividing $m$ never adds prime factors, so (c) holds for the new $m$.

**Termination.** Each pass of the outer loop increases $d$ by a positive gap, and $m$ never grows. So after finitely many passes $d^2 > m$. Each inner loop of line L6 ends, because $d \ge 2$ and $m$ is a positive integer that shrinks with each division.

**Correctness.** When the loop stops, $d^2 > m$. If $m > 1$ were composite, it would have a prime factor $q \le \sqrt m < d$, against (c). So $m = 1$ or $m$ is a prime with $m \ge d$ by (c); in the second case line L8 appends $m$, which is at least every entry of $F$. By (a), the product of the returned list is $N$, and every entry is prime and in non-decreasing order. By the [fundamental theorem of arithmetic](/fundamental-theorem-of-arithmetic/) this is the factorization of $N$. $\blacksquare$
