---
title: Correctness of Dixon's random squares algorithm
proves: [correctness, termination]
status: full
---

Write $U$ for the group of units modulo $N$, that is, the residues in $[1, N - 1]$ prime to $N$, and $v(z)$ for the exponent vector of $z^2 \bmod N$ over $F$ when it exists.

**Lemma 1 (the elimination).** Let $v_1, \dots, v_m$ be the exponent vectors mod 2, as bit masks. When row $j$ reduces to $0$, the subset $h$ it carries is nonempty and $\bigoplus_{l \in h} v_l = 0$, where $\oplus$ is the sum mod 2. If $m > K$, at least $m - K$ subsets are found.

*Proof.* Row $j$ starts with $u = v_j$ and $h = \{j\}$. Each reduction adds a stored pivot pair $(u', h')$ with $u' = \bigoplus_{l \in h'} v_l$ to $(u, h)$ by $\oplus$ in both parts, so $u = \bigoplus_{l \in h} v_l$ stays true. The stored pairs come from rows $l < j$, so $j \notin h'$ and $j$ stays in $h$; thus $h \ne \emptyset$. Each reduction clears the leading bit of $u$ and changes only lower bits, so a row either reduces to $0$ or becomes a pivot with a leading bit that no other pivot has. There are $K$ bit positions, so at most $K$ pivots, and at least $m - K$ rows reduce to $0$. $\square$

**Lemma 2 (the congruence).** For every subset $T$ tried at line L7, $X^2 \equiv Y^2 \pmod N$.

*Proof.* Each relation $(z, v)$ has $z^2 \equiv \prod_{p \in F} p^{v_p} \pmod N$ by line L5. Let $e = \sum_{(z, v) \in T} v$. By Lemma 1 every $e_p$ is even, so $X^2 \equiv \prod_{(z, v) \in T} z^2 \equiv \prod_{p \in F} p^{e_p} = \big(\prod_{p \in F} p^{e_p/2}\big)^2 \equiv Y^2 \pmod N$. $\square$

**Lemma 3 (square roots).** Let $N$ be odd with exactly $r$ distinct prime factors, and let $\phi: U \to U$ be $z \mapsto z^2 \bmod N$. Each nonempty fiber $\phi^{-1}(s)$ is a coset $wH$ of the kernel $H = \{h \in U : h^2 \equiv 1\}$, and $|H| = 2^r$. For units $X, Y$ with $X^2 \equiv Y^2$, $\gcd(X - Y, N)$ is a proper factor of $N$ if and only if $X \not\equiv \pm Y \pmod N$.

*Proof.* $\phi$ is a homomorphism of the abelian group $U$, so its fibers are the cosets of its kernel $H$. By the Chinese remainder theorem, $H$ is the product of the groups $\{h \bmod p^j : h^2 \equiv 1\}$ over the prime powers $p^j \parallel N$. For odd $p$, the group of units modulo $p^j$ is cyclic of even order, so it has exactly two elements with square $1$, namely $\pm 1$. Hence $|H| = 2^r$.

For the second claim, $N \mid (X - Y)(X + Y)$. If $X \equiv Y$, the gcd is $N$. If $X \equiv -Y$, then $X - Y \equiv -2Y$ is a unit because $N$ is odd, so the gcd is $1$. Conversely, if the gcd is $N$ then $X \equiv Y$. If the gcd is $1$, then $N \mid X + Y$, so $X \equiv -Y$. In all other cases $1 < \gcd(X - Y, N) < N$. $\square$

**Theorem.** The algorithm stops and returns $1$ or a proper factor of $N$. Suppose $N$ is odd with $r \ge 2$ distinct prime factors. Then, conditioned on the event that the run reaches line L6, each subset $T$ that line L6 produces gives a proper factor at line L8 with probability at least $1 - 2^{1-r} \ge 1/2$.

*Proof.* *Termination.* The loop of lines L2 to L5 makes at most $I$ draws. Each smoothness test divides a positive integer by primes, so it stops. Line L6 runs Lemma 1 on finitely many rows, and lines L7 and L8 run once per subset.

*Correctness.* At line L4, $1 \le z \le N - 1$, so $g = \gcd(z, N) \le z < N$, and $g > 1$ is tested; so $g$ is a proper factor. Line L8 returns $g = \gcd(X - Y, N)$ only if $1 < g < N$. Otherwise line L9 returns $1$. So the output is always $1$ or a proper factor. A prime $N$ has no proper factor, so the output is $1$.

*Probability.* The run reaches line L6 exactly when no draw had $\gcd(z, N) > 1$. Conditioned on this, the draws $z_1, z_2, \dots$ are independent and uniform on $U$. Condition further on the values $s_t = z_t^2 \bmod N$. By Lemma 3, each $z_t$ is then uniform on the coset $\phi^{-1}(s_t) = w_t H$, and the $z_t$ stay independent, because the fibers of $\phi$ all have size $2^r$ and the draws were independent. Every choice of the algorithm before line L8 depends only on the values $s_t$: the number of draws, the smoothness test, the vectors, the subsets of Lemma 1 and the value $Y$. So, given the $s_t$, the subset $T$ and $Y$ are fixed. Also $Y$ is a unit: if a prime $p \in F$ divides $N$, it does not divide $s_t$, because $s_t \equiv z_t^2 \pmod p$ with $p \nmid z_t$, so $e_p = 0$.

Pick one relation $j_0 \in T$ and write $X = z_{j_0} C$, where $C$ is the product of the other $z$ in $T$ modulo $N$ and is independent of $z_{j_0}$. Given $C$, $X$ is uniform on the coset $w_{j_0} C H$, which has $2^r$ elements. By Lemma 2, $X^2 \equiv Y^2$, so $\pm Y$ lie in this coset too, and they are two distinct elements since $N$ is odd and $Y$ is a unit. So $X \equiv \pm Y$ has probability $2/2^r = 2^{1-r}$. By Lemma 3, line L8 finds a proper factor in every other case. Since this holds for every value of the conditions, it holds after removing them. $\blacksquare$
