---
title: Miller-Rabin never rejects a prime, and accepts an odd composite with probability below 4^-k
proves: [correctness, termination, error]
status: full
---

We use the pseudocode MILLER-RABIN$(n, k)$ of the page. For odd $n \ge 3$ write $n - 1 = 2^s d$ with $d$ odd. A base $a \in [1, n - 1]$ is a *strong liar* for $n$ if $a^d \equiv 1 \pmod n$ or $a^{2^j d} \equiv -1 \pmod n$ for some $0 \le j < s$; $S(n)$ is the set of strong liars. $\varphi$ is Euler's totient function, and $v_2(m)$ is the exponent of 2 in $m$.

**Termination.** Line L3 halves $n - 1$ at most $\lg n$ times. The loop of line L4 runs at most $k$ times, and each pass does one exponentiation and at most $s - 1$ squarings. So the call ends.

**Lemma 1 (a round passes exactly for strong liars).** Let $n \ge 5$ be odd and $a \in [2, n - 2]$. The round of lines L5 to L11 with the base $a$ ends at line L7 or L10 if and only if $a \in S(n)$, and otherwise it returns false at line L11.

*Proof.* After line L6, $x = a^d \bmod n$, and after the $j$-th pass of line L9, $x = a^{2^j d} \bmod n$, by induction on $j$. Line L7 passes exactly when $a^d \equiv \pm 1$, which covers the cases $a^d \equiv 1$ and $j = 0$. Line L10 passes in pass $j$ exactly when $a^{2^j d} \equiv -1$ for some $1 \le j \le s - 1$. So the round passes if and only if one of the defining conditions of a strong liar holds. $\square$

**Lemma 2 (no nontrivial square roots of 1 modulo a prime).** If $p$ is prime and $x^2 \equiv 1 \pmod p$, then $x \equiv \pm 1 \pmod p$.

*Proof.* $p \mid x^2 - 1 = (x - 1)(x + 1)$, so $p$ divides one of the factors. $\square$

**Lemma 3 (a prime is accepted).** If $n$ is prime, MILLER-RABIN$(n, k)$ returns true for every choice of the bases.

*Proof.* For $n \in \{2, 3\}$ line L1 returns true. Otherwise $n \ge 5$ is odd, and line L2 does not return. Let $a \in [2, n - 2]$, so $n \nmid a$. Put $x_j = a^{2^j d} \bmod n$ for $0 \le j \le s$. By Fermat's little theorem $x_s = 1$. Let $t$ be the least index with $x_t = 1$. If $t = 0$, then $a^d \equiv 1$ and $a \in S(n)$. If $t > 0$, then $x_{t-1}^2 = x_t = 1$ and $x_{t-1} \ne 1$, so $x_{t-1} \equiv -1$ by Lemma 2, with $0 \le t - 1 < s$, and $a \in S(n)$. By Lemma 1 every round passes, and line L12 returns true. $\square$

**Lemma 4 (false is right).** If MILLER-RABIN$(n, k)$ returns false, then $n$ is not prime.

*Proof.* Line L1 returns false only for $n \in \{0, 1\}$. Line L2 returns false for even $n \ge 4$. Line L11 returns false only when a round fails, which by Lemma 3 does not happen for a prime. $\square$

**Lemma 5 (counting in a cyclic group).** Let $G$ be a cyclic group of order $N$ and $m \ge 1$. Then $x^m = 1$ has $\gcd(m, N)$ solutions in $G$. If $N$ is even and $-1$ denotes the unique element of order 2, then $x^m = -1$ has a solution if and only if $v_2(m) < v_2(N)$, and then it has $\gcd(m, N)$ solutions.

*Proof.* Let $g$ generate $G$ and $x = g^t$, $0 \le t < N$. Then $x^m = 1$ if and only if $N \mid tm$, which has $\gcd(m, N)$ solutions $t$. Next $-1 = g^{N/2}$, and $x^m = -1$ if and only if $tm \equiv N/2 \pmod N$. With $c = \gcd(m, N)$ this is solvable if and only if $c \mid N/2$, with $c$ solutions. As $v_2(c) = \min(v_2(m), v_2(N))$, $c \mid N/2$ holds if and only if $v_2(m) < v_2(N)$. $\square$

**Lemma 6 (Monier's count).** Let $n = \prod_{i=1}^r p_i^{e_i}$ be odd and composite with distinct primes $p_i$, $v_i = v_2(p_i - 1)$ and $\nu = \min_i v_i$. Then

$$|S(n)| = \Big(1 + \sum_{j=0}^{\nu - 1} 2^{jr}\Big) \prod_{i=1}^r \gcd(d, p_i - 1).$$

*Proof.* Each $(\mathbb{Z}/p_i^{e_i}\mathbb{Z})^*$ is cyclic of order $N_i = p_i^{e_i - 1}(p_i - 1)$, with $v_2(N_i) = v_i$. For $m \mid n - 1$ we have $p_i \nmid m$, so $\gcd(m, N_i) = \gcd(m, p_i - 1)$. By the Chinese remainder theorem the number of solutions of $a^m \equiv \pm 1 \pmod n$ is the product of the numbers of solutions modulo the $p_i^{e_i}$. By Lemma 5, $a^d \equiv 1$ has $T = \prod_i \gcd(d, p_i - 1)$ solutions. For $0 \le j < s$, $a^{2^j d} \equiv -1$ has $\prod_i 2^j \gcd(d, p_i - 1) = 2^{jr} T$ solutions if $j < \nu$, since then $j < v_i$ and $\gcd(2^j d, p_i - 1) = 2^j \gcd(d, p_i - 1)$; it has none if $j \ge \nu$. As every $p_i \equiv 1 \pmod{2^\nu}$, $n \equiv 1 \pmod{2^\nu}$, so $\nu \le s$. The cases are disjoint: if $a^{2^j d} \equiv -1$, then $a^{2^{j'} d} \equiv 1$ for $j' > j$, and if $a^d \equiv 1$ then no power $a^{2^j d}$ is $-1$. Adding the counts gives the formula. $\square$

**Lemma 7 (Monier-Rabin).** If $n > 9$ is odd and composite, then $|S(n)| \le \varphi(n)/4$.

*Proof.* Keep the notation of Lemma 6. Since $d$ is odd, $\gcd(d, p_i - 1)$ divides the odd part $(p_i - 1)/2^{v_i}$. With $\varphi(n) = \prod_i p_i^{e_i - 1}(p_i - 1)$ this gives

$$\frac{|S(n)|}{\varphi(n)} \le \frac{1 + \sum_{j<\nu} 2^{jr}}{2^{v_1 + \cdots + v_r}} \cdot \frac{1}{\prod_i p_i^{e_i - 1}}, \tag{1}$$

with equality in the first factor when each $\gcd(d, p_i - 1)$ is the whole odd part. Since $\sum_i v_i \ge r\nu$, $\nu \ge 1$ and $\sum_{j<\nu} 2^{jr} = (2^{r\nu} - 1)/(2^r - 1)$,

$$\frac{1 + \sum_{j<\nu} 2^{jr}}{2^{r\nu}} = \frac{1}{2^r - 1} + 2^{-r\nu} \frac{2^r - 2}{2^r - 1} \le \frac{1}{2^r - 1} + 2^{-r} \frac{2^r - 2}{2^r - 1} = 2^{1-r}. \tag{2}$$

*Case $r \ge 3$.* By (1) and (2), $|S(n)|/\varphi(n) \le 2^{1-r} \le 1/4$.

*Case $r = 2$, $n$ not squarefree.* The last factor in (1) is at most $1/3$, so $|S(n)|/\varphi(n) \le \frac12 \cdot \frac13 < \frac14$.

*Case $n = pq$ with primes $p < q$.* If $v_1 + v_2 > 2\nu$, the first factor in (1) is at most half of the left side of (2), so $|S(n)|/\varphi(n) \le \frac12 \cdot \frac12$. If $v_1 = v_2 = \nu$, let $q' = (q - 1)/2^\nu$ be the odd part of $q - 1$. If $q' \mid d$, then $q - 1 = 2^\nu q'$ divides $2^s d = n - 1$, because $\nu \le s$. But $n - 1 = p(q - 1) + (p - 1)$, so then $q - 1 \mid p - 1$, which is false as $0 < p - 1 < q - 1$. So $\gcd(d, q - 1)$ is a proper divisor of the odd number $q'$, hence at most $q'/3$, and the bound (1) improves by the factor $1/3$: $|S(n)|/\varphi(n) \le \frac13 \cdot \frac12 < \frac14$.

*Case $r = 1$, $n = p^e$ with $e \ge 2$.* Lemma 6 gives $|S(n)| = 2^\nu \gcd(d, p - 1) \le 2^\nu (p - 1)/2^\nu = p - 1$, so $|S(n)|/\varphi(n) \le p^{1-e}$. This is at most $1/5$ if $p \ge 5$, and at most $1/9$ if $p = 3$ and $e \ge 3$. The remaining case $n = 9$ is excluded. $\square$

**Theorem (error).** Let $n \ge 5$ be odd and composite. Then MILLER-RABIN$(n, k)$ returns true with probability exactly $q^k$, where $q = (|S(n)| - 2)/(n - 3)$, and $q < 1/4$. So the probability is less than $4^{-k}$.

*Proof.* Lines L1 and L2 do not return. By Lemma 1 the call returns true if and only if each of the $k$ bases drawn in line L5 is in $S(n)$. The bases are independent and uniform on the $n - 3$ integers of $[2, n - 2]$. The liars $1$ and $n - 1$ are not in this range, and they are distinct, so $|S(n)| - 2$ of the $n - 3$ bases are liars, and each round passes with probability $q$. For $n = 9$, $S(9) = \{1, 8\}$, so $q = 0$. For $n > 9$, Lemma 7 and $\varphi(n) \le n - 1$ give

$$q \le \frac{(n - 1)/4 - 2}{n - 3} = \frac{n - 9}{4(n - 3)} < \frac14.$$

The $k$ rounds are independent, so the probability of true is $q^k < 4^{-k}$. $\blacksquare$

**Remark.** The probability is over the random bases only. It holds for every odd composite $n$, with no assumption on how $n$ was chosen. Together with Lemma 3 this shows that the test has one-sided error: a wrong answer is always true, on a composite input.
