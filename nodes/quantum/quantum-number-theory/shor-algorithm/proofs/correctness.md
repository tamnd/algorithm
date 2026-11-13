---
title: Shor's algorithm returns a factor and stops with high probability
proves: [correctness]
status: full
---

We use the pseudocode of the page. $N$ is composite, $n = \lceil \log_2 N \rceil$, $Q = 2^t$ is the least power of 2 with $Q \ge N^2$, and for $\gcd(a, N) = 1$ the order $r$ is the least $r > 0$ with $a^r = 1 \pmod N$. All congruences are modulo $N$.

**Lemma 1 (each output is a factor).** If SHOR returns $f$, then $1 < f < N$ and $f$ divides $N$.

*Proof.* Line L1 returns 2 for an even composite $N$, and line L2 returns $b$ with $N = b^k$, $b \ge 2$ and $k \ge 2$, so $1 < b < N$. Line L6 returns $g = \gcd(a, N)$ with $g > 1$, and $g \le a \le N - 2$.

For line L11, line L19 returns only a $q$ with $a^q = 1$, so $r$ divides $m$. Write $r = 2^u d'$ and $m = 2^s d$ with $d'$ and $d$ odd. Then $d'$ divides $d$ and $u \le s$. For $0 \le j \le s$, $a^{2^j d} = 1$ if and only if $r$ divides $2^j d$, that is, if and only if $j \ge u$. If $u = 0$, then $y = a^d = 1$ at line L8, and line L9 skips the rest. If $u \ge 1$, then $y = a^d \ne 1$, and line L10 squares until the next square is 1. It stops at $y = a^{2^{u-1} d}$. Let $z = a^{r/2} = a^{2^{u-1} d'}$. Then $z^2 = 1$ and $d/d'$ is odd, so $y = z^{d/d'} = z$. So line L11 sees $y = a^{r/2}$, and $y \ne 1$ because $r$ is minimal. If $y \ne N - 1$, then $y \not\equiv \pm 1$ but $(y - 1)(y + 1) = y^2 - 1 \equiv 0$. So $N$ divides $(y - 1)(y + 1)$ but neither $y - 1$ nor $y + 1$, because $0 < y - 1 < y + 1 < N$. Hence $\gcd(y - 1, N)$ is neither 1 nor $N$. $\square$

**Lemma 2 (the measurement distribution).** In one pass of lines L14 to L17, the outcome $c \in \{0, \dots, Q - 1\}$ has probability

$$\Pr[c] = \frac{1}{Q^2} \sum_{k=0}^{r-1} \Bigl| \sum_{j=0}^{m_k - 1} \omega^{c r j} \Bigr|^2, \qquad \omega = e^{2\pi i/Q}, \quad m_k = \lceil (Q - k)/r \rceil.$$

*Proof.* After line L16 the state is $Q^{-1/2} \sum_{x=0}^{Q-1} |x\rangle |a^x \bmod N\rangle$. Write $x = k + jr$ with $0 \le k < r$; for a fixed $k$ the values $j$ run over $0 \le j < m_k$. The residues $a^k$ for $0 \le k < r$ are distinct, so the state is $Q^{-1/2} \sum_k \bigl(\sum_j |k + jr\rangle\bigr) |a^k\rangle$ with orthogonal work states. The inverse QFT maps $|x\rangle$ to $Q^{-1/2} \sum_c \omega^{-xc} |c\rangle$. The amplitude of $|c\rangle|a^k\rangle$ is therefore $Q^{-1} \omega^{-kc} \sum_j \omega^{-jrc}$. Its squared modulus is $Q^{-2} |\sum_j \omega^{jrc}|^2$, and the sum over $k$ gives the formula. $\square$

**Lemma 3 (the peaks).** For each integer $s$ with $0 \le s < r$, let $c_s$ be an integer with $|c_s r - sQ| \le r/2$. Then

$$\Pr[c_s] \ge \frac{4}{\pi^2 r}\Bigl(1 - \frac{\pi r}{2Q}\Bigr)^2.$$

*Proof.* Let $\theta = 2\pi (c_s r - sQ)/Q$. Then $\omega^{c_s r j} = e^{i j \theta}$ and $|\theta| \le \pi r/Q$. Since $(Q - k)/r \le m_k < (Q - k)/r + 1$ and $0 \le k < r$, we have $|m_k - Q/r| < 1$.

If $\theta = 0$, the inner sum is $m_k > Q/r - 1 \ge 2Q/(\pi r) - 1$.

If $\theta \ne 0$, the inner sum has modulus $|\sin(m_k \theta/2)| / |\sin(\theta/2)|$. Let $\phi = Q\theta/(2r)$, so $|\phi| \le \pi/2$ and $|\sin \phi| \ge 2|\phi|/\pi = |\theta| Q/(\pi r)$. The sine is 1-Lipschitz, so $|\sin(m_k\theta/2)| \ge |\sin\phi| - |m_k - Q/r|\,|\theta|/2 > |\theta|\bigl(Q/(\pi r) - 1/2\bigr)$. With $|\sin(\theta/2)| \le |\theta|/2$, the modulus is more than $2Q/(\pi r) - 1$.

In both cases the inner sum has modulus at least $\frac{2Q}{\pi r}\bigl(1 - \frac{\pi r}{2Q}\bigr)$, which is positive because $r < N \le \sqrt{Q}$. Squaring, adding the $r$ terms of Lemma 2 and dividing by $Q^2$ gives the bound. $\square$

**Lemma 4 (one pass returns r).** One pass of lines L14 to L19 returns $r$ with probability at least

$$p(r) = \varphi(r) \cdot \frac{4}{\pi^2 r}\Bigl(1 - \frac{\pi r}{2Q}\Bigr)^2,$$

and each $q$ that it returns is a multiple of $r$.

*Proof.* Line L19 returns only a $q$ with $a^q = 1$, and such a $q$ is a multiple of $r$.

Take $s$ with $\gcd(s, r) = 1$ and the outcome $c = c_s$ of Lemma 3. Then $|c/Q - s/r| \le 1/(2Q) \le 1/(2N^2) < 1/(2r^2)$, because $r \le \varphi(N) < N$. By Legendre's criterion (Hardy and Wright, Chapter X), a fraction $s/r$ in lowest terms with $|x - s/r| < 1/(2r^2)$ is a convergent of $x$. So $s/r$ is a convergent of $c/Q$, and $r < N$ passes the test of line L18. The convergent denominators do not decrease, and they are equal only for the first two convergents, which both have denominator 1. Since $a \ne 1$, we have $r \ge 2$, so the convergents before $s/r$ have denominators $q < r$, and $a^q \ne 1$ for them by the minimality of $r$. So line L19 returns $q = r$.

The points $sQ/r$ for distinct $s$ are at least $Q/r > N$ apart, so the outcomes $c_s$ are distinct. There are $\varphi(r)$ values of $s$ with $\gcd(s, r) = 1$, and Lemma 3 bounds each $\Pr[c_s]$. $\square$

Since $r < N \le \sqrt{Q}$, we have $\pi r/(2Q) < \pi/(2N)$, so $p(r) \ge c_0\, \varphi(r)/r$ for a constant $c_0 > 0$ (for $N \ge 15$, $c_0 = 0.32$ works). By Hardy and Wright (Chapter XVIII), $\varphi(r)/r \ge e^{-\gamma}(1 - o(1))/\ln\ln r$, so $p(r) = \Omega(1/\log\log N)$. Each pass of the loop of line L13 returns independently with probability at least $p(r)$, so ORDER stops with probability 1 after $O(\log\log N)$ passes in expectation.

**Lemma 5 (good bases).** Let $N$ be odd and not a prime power, and pick $a$ uniformly from $[2, N - 2]$. Then one pass of the loop of line L3 returns with probability at least $1/2$.

*Proof.* If $\gcd(a, N) > 1$, line L6 returns. Otherwise call the unit $a$ good if $r$ is even and $a^{r/2} \ne N - 1$; by the proof of Lemma 1, line L11 returns exactly for the good bases. $N$ has at least two distinct prime factors, so by the theorem on [factoring to order finding](/factoring-to-order-finding/), at least half of the units in $[1, N - 1]$ are good. The units 1 and $N - 1$ are not good (their orders are 1 and 2, and $(N-1)^{2/2} = N - 1$). Removing two bad units from the units of $[1, N-1]$ keeps the good fraction at least $1/2$. So the probability is at least $1/2$ over the units in $[2, N - 2]$, and line L6 returns for the other values of $a$. $\square$

**Theorem.** For every composite $N$, SHOR($N$) stops with probability 1 and returns a factor $f$ with $1 < f < N$. The loop of line L3 runs at most 2 times in expectation, and each call of ORDER makes $O(\log\log N)$ passes of lines L14 to L19 in expectation.

*Proof.* If $N$ is even or a perfect power, lines L1 and L2 return. Otherwise $N$ is odd, composite and not a prime power. By Lemma 4 each call of ORDER stops, and by Lemma 5 each pass of the loop of line L3 returns with probability at least $1/2$, independently of the earlier passes. So the number of passes is at most a geometric variable with mean 2. Lemma 1 shows that the returned value is a factor. $\blacksquare$
