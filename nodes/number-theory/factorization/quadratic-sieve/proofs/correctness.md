---
title: Correctness of the quadratic sieve
proves: [correctness, termination]
status: full
---

Let $s = \lfloor \sqrt N \rfloor$ and $f(t) = (s + t)^2 - N$. Since $N$ is not a perfect square, $f(t) \ne 0$ for every integer $t$, so $\log |f(t)|$ at line L5 is defined.

**Lemma 1 (the root classes).** Let $p$ be an odd prime with $p \nmid N$ and $(N/p) = 1$, and let $r_p^2 \equiv N \pmod p$. Then $r_p \not\equiv -r_p \pmod p$, and for every integer $x$, $p \mid x^2 - N$ if and only if $x \equiv r_p$ or $x \equiv -r_p \pmod p$. Also $2 \mid x^2 - N$ if and only if $x$ is odd.

*Proof.* If $r_p \equiv -r_p$, then $p \mid 2r_p$, so $p \mid r_p$ and $p \mid N$, which is excluded. Next, $x^2 - N \equiv x^2 - r_p^2 = (x - r_p)(x + r_p) \pmod p$, and since $p$ is prime, $p$ divides the product if and only if it divides one factor. For $p = 2$: $N$ is odd, so $x^2 - N$ is even if and only if $x^2$ is odd, that is, $x$ is odd. $\square$

**Lemma 2 (the sieve).** After line L4 runs on a block $W$, for each $t \in W$, $S[t] = \sum \log p$ over the distinct primes $p \in F$, $p > 0$, that divide $f(t)$.

*Proof.* Line L4 sets $S[t] = 0$ and then, for each prime $p$ of $F$ and each of its root classes $c$, adds $\log p$ to exactly the entries $t \in W$ with $s + t \equiv c \pmod p$. By Lemma 1, the root classes of an odd $p$ are two distinct classes, and $p \mid f(t)$ exactly when $s + t$ lies in one of them; so $\log p$ is added once if $p \mid f(t)$ and never otherwise. For $p = 2$ the one class $c = 1$ gives the same. Every odd $p \in F$ has $(N/p) = 1$, which implies $p \nmid N$, so Lemma 1 applies to it. $\square$

**Lemma 3 (relations).** Every relation $(x, v)$ in $R$ satisfies $x^2 \equiv \prod_{p \in F} p^{v_p} \pmod N$, with $p = -1$ included. No two relations have the same $x$.

*Proof.* Line L6 appends $(s + t, v)$ only when trial division shows $f(t) = \prod_{p \in F} p^{v_p}$, with $v_{-1} = 1$ exactly when $f(t) < 0$. Then $x^2 = (s + t)^2 = N + f(t) \equiv f(t) \pmod N$. The blocks of line L3 are disjoint intervals of $t$: the right blocks $[jM, (j + 1)M)$ cover $t \ge 0$ and the left blocks $[-(j + 1)M, -jM)$ cover $t < 0$, each cut to $s + t \ge 1$. So each $t$, hence each $x = s + t$, is looked at once. $\square$

**Lemma 4 (the elimination).** Let $v_1, \dots, v_m$ be the exponent vectors mod 2, as bit masks over the $K + 1$ coordinates of $F$. Gaussian elimination that records, for each reduced row, the set $h$ of original rows added into it, produces for each row that reduces to $0$ a nonempty set $h$ with $\bigoplus_{l \in h} v_l = 0$. If $m > |F|$, at least $m - |F|$ such sets are found.

*Proof.* Row $j$ starts with $u = v_j$ and $h = \{j\}$. Each reduction adds a stored pivot pair $(u', h')$ with $u' = \bigoplus_{l \in h'} v_l$ to $(u, h)$ by $\oplus$ in both parts, so $u = \bigoplus_{l \in h} v_l$ stays true. The stored pairs come from earlier rows, so $j \notin h'$, and $j$ stays in $h$. Each reduction clears the leading bit of $u$ and changes only lower bits, so the row either reduces to $0$ or becomes a pivot with a new leading bit. There are $|F|$ coordinates, so at most $|F|$ pivots, and at least $m - |F|$ rows reduce to $0$. $\square$

**Theorem.** QS stops, and it returns $1$ or a proper factor $g$ of $N$. Each subset $T$ tried at line L8 satisfies $X^2 \equiv Y^2 \pmod N$. If the loop ends with $|R| \ge |F| + E$, at least $E$ subsets are tried.

*Proof.* *Termination.* Each pass of the loop of line L2 increases $j$ at line L7, and the loop stops when $j \ge J$. Each pass sieves two blocks of at most $M$ values with finitely many primes, and trial division of a nonzero integer by primes stops. Line L8 runs over finitely many subsets.

*Congruence of squares.* Let $T$ be a subset from Lemma 4 and $e = \sum_{(x, v) \in T} v$ over the integers. Every $e_p$ is even, including $e_{-1}$. By Lemma 3, $X^2 \equiv \prod_{(x, v) \in T} x^2 \equiv \prod_{p \in F} p^{e_p} = (-1)^{e_{-1}} \prod_{p > 0} \big(p^{e_p/2}\big)^2 \equiv Y^2 \pmod N$, since $(-1)^{e_{-1}} = 1$. The count of subsets is Lemma 4 with $m = |R|$.

*Correctness.* The only return other than line L9 is in line L8, which returns $g = \gcd(X - Y, N)$ only if $1 < g < N$. A gcd with $N$ divides $N$, so $g$ is a proper factor. A prime $N$ has none, so for a prime the output is $1$. The threshold of line L5 decides only which values are tried by trial division, so it does not affect any of these statements. $\blacksquare$
