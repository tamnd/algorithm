---
title: The subtract-with-borrow generator under RANLUX is a multiplicative LCG modulo b^r - b^s + 1, which gives its period
proves: [correctness]
status: full
---

Fix a base $b \ge 2$ and lags $0 < s < r$, and put $m = b^r - b^s + 1$. Note $m \equiv 1 \pmod b$, so $\gcd(m, b) = 1$. The subtract-with-borrow (SWB) generator keeps $x_{n-r}, \ldots, x_{n-1} \in \{0, \ldots, b - 1\}$ and a borrow $c_{n-1} \in \{0, 1\}$. Lines L6 and L7 compute $d = x_{n-s} - x_{n-r} - c_{n-1}$ and set $x_n = d$, $c_n = 0$ if $d \ge 0$, and $x_n = d + b$, $c_n = 1$ otherwise. In both cases

$$x_n - b c_n = x_{n-s} - x_{n-r} - c_{n-1}. \tag{1}$$

**Lemma 1 (three-term relation).** $x_n - x_{n-s} + x_{n-r} = b c_n - c_{n-1} \in \{-1, 0, b - 1, b\}$.

*Proof.* Rearrange (1); $c_n, c_{n-1} \in \{0, 1\}$. $\square$

So the points $(x_{n-r}, x_{n-s}, x_n)/b$ lie on the four planes $u_3 - u_2 + u_1 \in \{-1/b, 0, 1 - 1/b, 1\}$. This is the defect that RANLUX removes by discarding values; the tests check the relation on 5000 outputs of ranlux24_base.

For the state at time $n$, read the stored values as base-$b$ numbers with the oldest value as the lowest digit:

$$A_r(n) = \sum_{k=0}^{r-1} x_{n-r+k}\, b^k, \qquad A_s(n) = \sum_{k=0}^{s-1} x_{n-s+k}\, b^k, \qquad K_n = A_s(n) - A_r(n) - c_{n-1}.$$

**Lemma 2 (the step is division by $b$ modulo $m$).** $b K_{n+1} = K_n - m x_n$, and $x_n = K_n \bmod b$. Hence $K_{n+1} \equiv b^{-1} K_n \pmod m$, and $K_{n+1}$ is a function of $K_n$ alone: $K_{n+1} = \psi(K_n)$ with $\psi(K) = (K - m (K \bmod b))/b$.

*Proof.* One step drops the oldest digit and appends $x_n$ on top, so $b A_r(n+1) = A_r(n) - x_{n-r} + x_n b^r$ and $b A_s(n+1) = A_s(n) - x_{n-s} + x_n b^s$. Then

$$b K_{n+1} = K_n + c_{n-1} - x_{n-s} + x_{n-r} + x_n (b^s - b^r) - b c_n.$$

By (1), $-b c_n = x_{n-s} - x_{n-r} - c_{n-1} - x_n$. Substituting, all terms cancel except $b K_{n+1} = K_n - x_n (b^r - b^s + 1) = K_n - m x_n$. Reducing modulo $b$ and using $m \equiv 1$ gives $x_n \equiv K_n \pmod b$, and $0 \le x_n < b$. $\square$

**Lemma 3 (the state and $K$ have the same cycles).** On a cycle of the state, the cycle length equals the least $L \ge 1$ with $K_{n+L} = K_n$.

*Proof.* $K_n$ is a function of the state, so a state cycle of length $L$ repeats $K$ with period dividing $L$. Conversely, if $K$ has period $L'$ along the cycle, then $x_n = K_n \bmod b$ has period $L'$, and the state at time $n$, the values $x_{n-r}, \ldots, x_{n-1}$ together with $c_{n-1} = A_s(n) - A_r(n) - K_n$, has period dividing $L'$. $\square$

**Lemma 4 (cycles live in $[-m, 0]$).** The interval $[-m, 0]$ is invariant under $\psi$, and every $K$ on a cycle of $\psi$ lies in it.

*Proof.* Let $x = K \bmod b \in [0, b - 1]$, so $\psi(K) = (K - m x)/b$, and $(K - m(b - 1))/b \le \psi(K) \le K / b$. If $-m \le K \le 0$, then $\psi(K) \le 0$ and $\psi(K) \ge (-m - m(b - 1))/b = -m$. If $K > 0$, then $\psi(K) \le K / b < K$ and $\psi(K) > -m$ (since $K + m > 0$), so the orbit either stays positive and strictly decreases, or enters $[-m, 0]$ and stays there; in both cases it never returns to $K$. If $K < -m$, then $\psi(K) \le K/b < 0$ and $\psi(K) > K$ (equivalent to $K < -m$), so the orbit stays negative and strictly increases until it enters $[-m, 0]$; again it never returns to $K$. $\square$

**Theorem (period of the SWB).** Every orbit of the state is eventually periodic. On a cycle, $-m \le K_n \le 0$, and the cycle length is 1 if $K_n \in \{0, -m\}$ (the outputs are constantly 0 or constantly $b - 1$), and otherwise it is the multiplicative order of $b$ modulo $m / \gcd(K_n, m)$. In particular, if $m$ is prime, every cycle other than the two fixed ones has length exactly $\operatorname{ord}_m(b)$.

*Proof.* The state set is finite, so every orbit is eventually periodic. On a cycle, Lemma 4 gives $-m \le K_n \le 0$. If $K_n = 0$, then $x_n = 0$ and $K_{n+1} = 0$; if $K_n = -m$, then $x_n = (-m) \bmod b = b - 1$ and $K_{n+1} = (-m - m(b - 1))/b = -m$. Otherwise $-m < K_n < 0$, so $K_n \not\equiv 0 \pmod m$; then $K_{n+1} \equiv b^{-1} K_n \not\equiv 0$ and $K_{n+1} \in [-m, 0]$, so $K_{n+1}$ is the unique element of $(-m, 0)$ congruent to $b^{-1} K_n$. Hence $K_{n+L} = K_n$ if and only if $b^{-L} K_n \equiv K_n$, that is $m \mid (b^L - 1) K_n$, that is $m / g \mid b^L - 1$ with $g = \gcd(K_n, m)$. The least such $L$ is $\operatorname{ord}_{m/g}(b)$, and Lemma 3 turns this into the length of the state cycle. If $m$ is prime and $K_n \in (-m, 0)$, then $g = 1$. $\square$

The tests check Lemma 2 and the Theorem on every state of every SWB with $b \in \{2, 3, 4, 5\}$, $2 \le r \le 5$ and $b^r \le 700$.

**Corollary (RANLUX).** For Lüscher's parameters $b = 2^{24}$, $r = 24$, $s = 10$, and also for $b = 2^{48}$, $r = 12$, $s = 5$, the modulus is $m = 2^{576} - 2^{240} + 1$. It is prime, and the period $\rho = \operatorname{ord}_m(2^{24})$ of ranlux24_base divides $N = (m - 1)/48 > 2^{570}$ and is a multiple of an explicit integer greater than $2^{333}$.

*Proof.* Primality, by Pocklington's criterion: if $F$ divides $m - 1$, $F^2 > m$, and for every prime $q \mid F$ there is an $a$ with $a^{m-1} \equiv 1 \pmod m$ and $\gcd(a^{(m-1)/q} - 1, m) = 1$, then $m$ is prime. Take $F = 2^{240} \operatorname{lcm}(2^{48} - 1, 2^{56} - 1)$, which divides $m - 1 = 2^{240}(2^{336} - 1)$ because 48 and 56 divide 336. Its prime factors come from trial division of $2^{48} - 1$ and $2^{56} - 1$, and $F > 2^{336} > \sqrt m$. The tests find a base $a < 100$ for each $q$. For the period, the tests compute $b^N \equiv 1 \pmod m$, so $\rho \mid N$. For each prime $q \mid F$ with $q^e \| N$, they find $b^{N/q} \not\equiv 1$, so $\rho \nmid N/q$ and $q^e \mid \rho$. The product of these $q^e$ exceeds $2^{333}$. $\blacksquare$

Lüscher (1994) gives the period as $(m - 1)/48 \approx 5 \cdot 10^{171}$; the full equality needs the factorization of $N$, which this page does not check. Decimation keeps the period finite and does not shorten it below $\rho / \gcd(\rho, p)$ blocks of $p$ steps, since after $j$ blocks the SWB has made $j p$ steps. The quality claims of RANLUX, the luxury levels, rest on Lüscher's dynamical argument and on statistical tests, not on this proof.
