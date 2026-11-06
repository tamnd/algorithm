---
title: Correctness of Lehman's factorization method
proves: [correctness, termination]
status: full
---

Let $N \ge 22$, and write $t = N^{1/3}$, a real number with $t > 2.8$.

**Termination.** Line L1 is a finite loop. For each $k$, the value $a^2 - 4kN$ grows with $a$ without bound, so the loop of line L4 ends; the loop of line L2 has $\lfloor t \rfloor + 1$ passes. So the algorithm stops.

**Lemma 1 (a returned gcd is a proper factor).** Suppose line L5 returns for some $k \le t + 1$ and some $a$ with $a^2 - 4kN = b^2$, $b \ge 0$, and $(a^2 - 4kN)^3 < N^2$. Then $d = \gcd(a + b, N)$ satisfies $1 < d < N$.

*Proof.* From $b^6 < N^2$ we get $b < t$. From $a^2 = 4kN + b^2 < 4(t + 1)t^3 + t^2 = t^2(2t + 1)^2$, we get $a < t(2t + 1)$. So $a + b < 2t^2 + 2t$. The inequality $2t^2 + 2t < t^3$ is $t^2 - 2t - 2 > 0$, which holds for $t > 1 + \sqrt 3 \approx 2.73$, so for $N > 20.4$. Hence $a + b < N$. Also $a^2 - b^2 = 4kN > 0$ with $a, b \ge 0$, so $a > b$ and $a - b \ge 1$.

$N$ divides $4kN = (a + b)(a - b)$. If $d = N$, then $N \mid a + b$ with $0 < a + b < N$, which is impossible. If $d = 1$, then $N \mid a - b$, and $0 < a - b < a + b < N$, which is impossible. So $1 < d < N$. $\square$

**Lemma 2 (Dirichlet).** Let $\xi$ be a real number and $B > 1$ a real number. There are integers $u$ and $v$ with $1 \le v \le B$ and $|v\xi - u| < 1/B$.

*Proof.* Let $M = \lfloor B \rfloor \ge 1$. The $M + 2$ numbers $0, 1$ and $\{j\xi\} = j\xi - \lfloor j\xi \rfloor$ for $j = 1, \dots, M$ lie in $[0, 1]$. Split $[0, 1]$ into the $M + 1$ closed intervals $[i/(M + 1), (i + 1)/(M + 1)]$. Two of the $M + 2$ numbers lie in the same interval, so they differ by at most $1/(M + 1)$. Each of the numbers has the form $j\xi - u_j$ with $0 \le j \le M$ (with $0 = 0\xi - 0$ and $1 = 0\xi + 1$), and the two chosen numbers cannot both have $j = 0$, because $0$ and $1$ differ by $1 > 1/(M + 1)$. Their difference is $v\xi - u$ with $1 \le |v| \le M$; replacing $(v, u)$ by $(-v, -u)$ if needed, $1 \le v \le M \le B$, and $|v\xi - u| \le 1/(M + 1) < 1/B$ since $M + 1 > B$. $\square$

**Lemma 3 (a good multiplier exists).** Let $N = pq$ with primes $t < p \le q$. Then there are integers $u, v \ge 1$ such that $k = uv$ satisfies $1 \le k < t + 1$, and $a = uq + vp$, $b = |uq - vp|$ satisfy $a^2 - b^2 = 4kN$, $a \ge \sqrt{4kN}$ and $b < t$.

*Proof.* Let $B = N^{1/6}\sqrt{q/p}$. Since $q \ge p$ and $N > 1$, $B > 1$. Apply Lemma 2 with $\xi = p/q$: there are $u, v$ with $1 \le v \le B$ and $|vp/q - u| < 1/B$. Multiply by $q$: $|vp - uq| < q/B = \sqrt{pq}/N^{1/6} = N^{1/2 - 1/6} = t$. So $b < t$.

If $u \le 0$, then $|vp - uq| \ge vp \ge p > t$, a contradiction; so $u \ge 1$. Next, $u < vp/q + 1/B$, so $k = uv < v^2 p/q + v/B \le B^2 p/q + 1 = N^{1/3} + 1 = t + 1$, using $v \le B$.

Finally, $a^2 - b^2 = (uq + vp)^2 - (uq - vp)^2 = 4uv\,pq = 4kN$, and by the inequality of the means $a = uq + vp \ge 2\sqrt{uq \cdot vp} = 2\sqrt{kN}$. $\square$

**Theorem.** LEHMAN($N$) returns a divisor $d$ of $N$ with $1 < d < N$ if $N$ is composite, and returns $N$ if $N$ is prime.

*Proof.* If line L1 returns $d$, then $2 \le d \le t < N$ and $d \mid N$. If line L5 returns, then Lemma 1 applies, since the loop of line L2 only uses $k \le \lfloor t \rfloor + 1 \le t + 1$ and line L4 checks $(a^2 - 4kN)^3 < N^2$. So every value returned on lines L1 or L5 is a proper divisor; in particular, for prime $N$ neither line returns, and line L7 returns $N$.

Let $N$ be composite, and suppose line L1 returns nothing. Then $N$ has no prime factor at most $t$. If $N$ had three prime factors (with multiplicity), their product would exceed $t^3 = N$. So $N = pq$ with primes $t < p \le q$. Take $u, v, k, a, b$ from Lemma 3. Since $k$ is an integer with $1 \le k < t + 1$, it satisfies $k \le \lfloor t \rfloor + 1$, so the loop of line L2 reaches $k$ unless it returned earlier. For this $k$, line L3 starts at $\lceil \sqrt{4kN} \rceil \le a$, and $a^2 - 4kN = b^2$ with $b^6 < t^6 = N^2$. The value $a'^2 - 4kN$ increases with $a'$, so every $a'$ from $\lceil \sqrt{4kN} \rceil$ to $a$ passes the test of line L4, and the loop reaches $a$ unless line L5 returned earlier. At $a$, line L5 finds the square $b^2$ and returns. So for composite $N$ the algorithm always returns on line L1 or L5, never on line L7. $\blacksquare$
