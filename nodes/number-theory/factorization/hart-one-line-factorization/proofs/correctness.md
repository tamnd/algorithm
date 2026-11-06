---
title: Correctness of Hart's one line factoring algorithm
proves: [correctness, termination]
status: full
---

Let $N \ge 2$, $M \ge 1$ and $K \ge 1$ be integers. For an iteration $i$, write $x = MNi$, $s = \lceil \sqrt x \rceil$ and $m = s^2 - x$, as in lines L2 and L3.

**Termination.** Each pass of the loop of line L1 does a fixed number of operations, and there are at most $K$ passes. So the algorithm stops, at line L2, L5 or L6.

**Lemma 1 (the size of $m$).** $0 \le m \le 2s - 2$, and $s \ge 2$.

*Proof.* $s^2 \ge x$ by the choice of $s$, so $m \ge 0$. Since $s$ is the smallest integer with $s^2 \ge x$, we have $(s - 1)^2 < x$, so $m = s^2 - x < s^2 - (s - 1)^2 = 2s - 1$, and $m \le 2s - 2$ because both sides are integers. Finally $x \ge 2$, so $s \ge 2$. $\square$

**Lemma 2 (a returned value is a proper factor).** Suppose line L5 runs at iteration $i$, so $2s - 1 < N$ and $m = t^2$ with an integer $t \ge 0$. Then $g = \gcd(N, s - t)$ satisfies $1 < g < N$ and $g \mid N$.

*Proof.* From Lemma 1, $t^2 = m \le 2s - 2 < s^2$, because $s^2 - 2s + 2 = (s - 1)^2 + 1 > 0$. So $0 \le t < s$, and $t \le s - 1$. Then
$$(s - t)(s + t) = s^2 - t^2 = s^2 - m = x = MNi,$$
so $N$ divides $(s - t)(s + t)$. Here $1 \le s - t \le s + t \le 2s - 1 < N$.

The value $g$ divides $N$ by definition. If $g = N$, then $N \mid s - t$ with $0 < s - t < N$, which is impossible. If $g = 1$, then $N$ is coprime to $s - t$, and since $N$ divides $(s - t)(s + t)$, it divides $s + t$. But $0 < s + t < N$, which is again impossible. So $1 < g < N$. $\square$

**Corollary 3 (primes and failures).** If $N$ is prime, the algorithm returns $1$. For every $N$, the output is $1$ or a proper factor of $N$.

*Proof.* The algorithm returns only at lines L2 and L6, with the value $1$, or at line L5. By Lemma 2, a return at line L5 gives a proper factor of $N$. A prime has no proper factor, so for a prime $N$ line L5 never runs, and the output is $1$. $\square$

**Lemma 4 (when an iteration succeeds).** Suppose $MNi = AB$ with integers $1 \le A < B$ of the same parity, $(\sqrt B - \sqrt A)^2 < 2$, and $A + B < N$. Then, if the loop reaches iteration $i$, it stops there at line L5 with $s = (A + B)/2$ and $t = (B - A)/2$.

*Proof.* Put $a = (A + B)/2$ and $b = (B - A)/2$, integers because $A$ and $B$ have the same parity. Then $a^2 - b^2 = AB = x$, so $a^2 \ge x$ and $a \ge \sqrt x$. Also
$$a - \sqrt x = \frac{A + B}{2} - \sqrt{AB} = \frac{(\sqrt B - \sqrt A)^2}{2} < 1,$$
so $a - 1 < \sqrt x \le a$, and $a = \lceil \sqrt x \rceil = s$. Then $m = s^2 - x = b^2$ is a square, and the square root found at line L4 is $t = b$. The range test of line L2 passes because $2s - 1 = A + B - 1 < N$. So the algorithm reaches line L5 at iteration $i$. $\square$

Lemma 4 explains the example of the main page: $8 \cdot 200633 = 1252 \cdot 1282$ with $(\sqrt{1282} - \sqrt{1252})^2 \approx 0.18$, so iteration $8$ gives $s = 1267$ and $t = 15$.

**Theorem 5 (the full factorization).** Let $N \ge 2$, let $c = \lfloor N^{1/3} \rfloor + 1$, and suppose that trial division by every $d \le c$ with $d^2 \le R$ divides out all such factors from $N$, with $R$ the part left at the end. Then $R$ is $1$, a prime, the square of a prime, or a product of two distinct primes. Splitting $R$ by a primality test, a square test, OLF and, if OLF fails, trial division up to $\sqrt R$, gives the prime factorization of $N$.

*Proof.* The trial division loop stops either because $d > c$ or because $d^2 > R$. Every prime factor of $R$ is larger than every $d$ that was tried, since those were divided out.

If the loop stopped because $d^2 > R$, then every prime factor of $R$ is at least $d > \sqrt R$, so $R$ has at most one prime factor counted with multiplicity: $R$ is $1$ or a prime.

If it stopped because $d > c$, then every prime factor of $R$ is larger than $c > N^{1/3} \ge R^{1/3}$. If $R$ had three prime factors counted with multiplicity, their product would be larger than $R$, a contradiction. So $R$ is $1$, a prime $p$, a square $p^2$, or a product $pq$ of two distinct primes.

A primality test settles the cases $1$ and $p$. The case $p^2$ is a perfect square, and the integer square root gives $p$. In the case $pq$, $R$ is composite and not a square; OLF returns a proper factor $g$ or $1$ by Corollary 3. A proper factor of $pq$ is $p$ or $q$, so $R = g \cdot (R/g)$ is the factorization into two primes. If OLF fails, trial division by odd numbers from the last $d$ finds the smaller prime $p \le \sqrt R$, since $R$ is composite. In each case the factors found, together with those removed by trial division, are primes whose product is $N$. $\blacksquare$
