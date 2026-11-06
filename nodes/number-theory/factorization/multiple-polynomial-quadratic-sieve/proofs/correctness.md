---
title: Correctness of the multiple polynomial quadratic sieve
proves: [correctness, termination]
status: full
---

Throughout, $N \ge 3$ is odd and not a perfect square, and $F$ is the factor base of line L1: $-1$, $2$, and the odd primes $p \le B$ with $(N/p) = 1$, each with $t_p^2 \equiv N \pmod p$.

**Lemma 1 (enough primes $q$).** There are infinitely many primes $q$ with $(N/q) = 1$. So the search of line L3 always stops.

*Proof.* First, infinitely many primes divide some value $x^2 - N$ with $x$ an integer. If not, let $p_1, \dots, p_k$ be all of them and $P = p_1 \cdots p_k$. Then $(NP)^2 - N = N(NP^2 - 1)$, and $NP^2 - 1 \ge N - 1 \ge 2$ is coprime to $P$, so it has a prime factor that is not among the $p_i$ but divides the value at $x = NP$, a contradiction. Now take such a prime $q$ with $q \nmid 2N$; all but finitely many qualify. Then $x^2 \equiv N \not\equiv 0 \pmod q$ for some $x$, so $N$ is a nonzero square modulo the odd prime $q$, that is, $(N/q) = 1$. $\square$

**Lemma 2 (the polynomial).** Let $q$ be an odd prime with $(N/q) = 1$, $a = q^2$, and $b_0$ with $b_0^2 \equiv N \pmod q$, $0 < b_0 < q$. Let $k = \frac{N - b_0^2}{q} \cdot (2b_0)^{-1} \bmod q$ and $b = b_0 + kq$, replaced by $a - b$ if $2b > a$. Then $b^2 \equiv N \pmod a$, $0 < b \le a/2$, $c = (b^2 - N)/a$ is an integer, $b^2 - ac = N$, and for every integer $x$
$$a f(x) = (ax + b)^2 - N \ne 0, \qquad f(x) = ax^2 + 2bx + c.$$

*Proof.* Since $(N/q) = 1$, $q \nmid N$, so $q \nmid b_0$, and $q$ is odd, so $2b_0$ is invertible modulo $q$ and $k$ is defined. The quotient $(N - b_0^2)/q$ is an integer as $q \mid N - b_0^2$. Then
$$b^2 = b_0^2 + 2b_0kq + k^2q^2 \equiv b_0^2 + 2b_0kq \pmod{q^2},$$
and $2b_0k \equiv (N - b_0^2)/q \pmod q$ gives $2b_0kq \equiv N - b_0^2 \pmod{q^2}$, so $b^2 \equiv N \pmod{q^2}$. Also $(a - b)^2 = a^2 - 2ab + b^2 \equiv b^2 \pmod a$, so the replacement keeps the congruence. Before it, $1 \le b_0 \le b \le (q - 1) + (q - 1)q < a$, so $0 < b < a$, and after it $0 < b \le a/2$. The congruence makes $c$ an integer, and $ac = b^2 - N$ is $b^2 - ac = N$. Expanding, $(ax + b)^2 - N = a^2x^2 + 2abx + b^2 - N = a^2x^2 + 2abx + ac = af(x)$. This is not $0$, since $N$ is not a perfect square. $\square$

**Lemma 3 (the root classes).** Let $f$ be as in Lemma 2 with $q > B$. For an odd $p \in F$, the two classes $x \equiv (\pm t_p - b)a^{-1} \pmod p$ are distinct, and $p \mid f(x)$ if and only if $x$ is in one of them. Also $2 \mid f(x)$ if and only if $x \equiv c \pmod 2$.

*Proof.* Let $p \in F$ be odd. Then $p \le B < q$, so $p \nmid a = q^2$ and $a^{-1} \bmod p$ exists. Also $(N/p) = 1$ gives $p \nmid N$, so $t_p \not\equiv -t_p \pmod p$, since otherwise $p \mid 2t_p$, so $p \mid t_p$ and $p \mid t_p^2$, and then $t_p^2 \equiv N$ gives $p \mid N$; so the two classes are distinct. As $p \nmid a$, $p \mid f(x)$ if and only if $p \mid af(x) = (ax + b)^2 - N$, which is $(ax + b)^2 \equiv t_p^2$, that is, $(ax + b - t_p)(ax + b + t_p) \equiv 0 \pmod p$. Since $p$ is prime, this holds if and only if $ax + b \equiv \pm t_p$, that is, $x \equiv (\pm t_p - b)a^{-1} \pmod p$. For $p = 2$: $a$ is odd and $x^2 \equiv x \pmod 2$, so $f(x) = ax^2 + 2bx + c \equiv x + c \pmod 2$. $\square$

**Lemma 4 (the sieve).** After line L5, for every $x \in [-M, M)$, $S[x]$ is the sum of $\log p$ over the distinct primes $p \in F$, $p > 0$, that divide $f(x)$.

*Proof.* Line L5 starts with $S[x] = 0$ and adds $\log p$ once for each root class of $p$ that contains $x$. By Lemma 3, an odd $p$ has two distinct classes and $x$ lies in one of them exactly when $p \mid f(x)$, so $\log p$ is added once if $p \mid f(x)$ and never otherwise. For $p = 2$ the single class $x \equiv c$ gives the same. $\square$

**Lemma 5 (relations).** Every relation $(r, v)$ appended at line L6 satisfies $r^2 \equiv \prod_{p \in F} p^{v_p} \pmod N$, with $p = -1$ included.

*Proof.* Line L6 appends $(r, v)$ only when trial division shows $f(x) = \prod_{p \in F} p^{v_p}$, with $v_{-1} = 1$ exactly when $f(x) < 0$. Here $r \equiv (ax + b)q^{-1} \pmod N$, where $q^{-1}$ exists because $q \nmid N$. By Lemma 2, $(ax + b)^2 = N + af(x) \equiv q^2 f(x) \pmod N$, so $r^2 \equiv q^2 f(x) q^{-2} = f(x) \pmod N$. $\square$

**Lemma 6 (the elimination).** Let $v_1, \dots, v_m$ be the exponent vectors mod 2, as bit masks over the $|F|$ coordinates of $F$. Gaussian elimination that records, for each reduced row, the set $h$ of original rows added into it, produces for each row that reduces to $0$ a nonempty set $h$ with $\bigoplus_{l \in h} v_l = 0$. If $m > |F|$, at least $m - |F|$ such sets are found.

*Proof.* Row $j$ starts with $u = v_j$ and $h = \{j\}$. Each reduction adds a stored pivot pair $(u', h')$ with $u' = \bigoplus_{l \in h'} v_l$ to $(u, h)$ by $\oplus$ in both parts, so $u = \bigoplus_{l \in h} v_l$ stays true. The stored pairs come from earlier rows, so $j \notin h'$ and $j$ stays in $h$, which is therefore nonempty. Each reduction clears the leading bit of $u$ and changes only lower bits, so the row either reduces to $0$ or becomes a pivot with a new leading bit. There are $|F|$ coordinates, so at most $|F|$ pivots, and at least $m - |F|$ rows reduce to $0$. $\square$

**Theorem.** MPQS stops, and it returns $1$ or a proper factor $g$ of $N$. Each subset $T$ tried at line L7 satisfies $X^2 \equiv Y^2 \pmod N$. If the loop ends with $|R| \ge |F| + E$, at least $E$ subsets are tried.

*Proof.* *Termination.* Each pass of the loop of line L2 uses one more polynomial, and the loop stops after at most $P$ of them. In each pass, line L3 stops by Lemma 1, lines L4 and L5 do finitely many steps for the finitely many primes of $F$ on an interval of $2M$ values, and trial division of the nonzero integer $f(x)$ (Lemma 2) by primes stops. Line L7 runs over finitely many subsets.

*Congruence of squares.* Let $T$ be a subset from Lemma 6 and $e = \sum_{(r, v) \in T} v$ over the integers. Every $e_p$ is even, including $e_{-1}$. By Lemma 5,
$$X^2 \equiv \prod_{(r, v) \in T} r^2 \equiv \prod_{p \in F} p^{e_p} = (-1)^{e_{-1}} \prod_{p > 0} \big(p^{e_p/2}\big)^2 \equiv Y^2 \pmod N,$$
since $(-1)^{e_{-1}} = 1$. The relations of $T$ may come from different polynomials, since each satisfies Lemma 5 over the same $F$. The count of subsets is Lemma 6 with $m = |R|$.

*Correctness.* The only return other than line L8 is in line L7, which returns $g = \gcd(X - Y, N)$ only if $1 < g < N$. A gcd with $N$ divides $N$, so $g$ is a proper factor. A prime $N$ has none, so for a prime $N$ the output is $1$. The threshold $\tau$ of line L6 decides only which values are tried by trial division, and keeping only one relation for each value of $\pm r$ only removes relations, so neither affects these statements. $\blacksquare$
