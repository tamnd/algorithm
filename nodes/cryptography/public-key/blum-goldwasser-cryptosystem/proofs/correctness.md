---
title: Blum-Goldwasser decryption recovers the seed and the message
proves: [correctness]
status: full
---

**Setting.** Let $p$ and $q$ be distinct primes with $p \equiv q \equiv 3 \pmod 4$, let $n = pq$ (line L1), and let $a, b$ be integers with $ap + bq = 1$ (line L2). Encryption (lines L4 to L9) takes a unit $r$ modulo $n$, sets $x_0 = r^2 \bmod n$ and $x_i = x_{i-1}^2 \bmod n$ for $i = 1, \ldots, t + 1$, and outputs $c_i = \mathrm{low}_h(x_i) \oplus m_i$ for $i = 1, \ldots, t$ together with $x_{t+1}$. Here $\mathrm{low}_h(x)$ is the number formed by the $h$ lowest binary digits of $x$. Let $e_p = (p+1)/4$ and $e_q = (q+1)/4$, which are integers because $p \equiv q \equiv 3 \pmod 4$.

**Claim.** Lines L10 to L12 return $x_0$, and lines L13 and L14 return $m_1, \ldots, m_t$.

*Proof.* We use Euler's criterion: for a square $s$ modulo $p$ with $p \nmid s$, $s^{(p-1)/2} \equiv 1 \pmod p$. (If $s \equiv w^2$, then $s^{(p-1)/2} \equiv w^{p-1} \equiv 1$ by Fermat's little theorem.)

*Step 1: every $x_i$ is a unit and a square modulo $p$.* $r$ is a unit modulo $n$, so $p \nmid r$, and $x_0 \equiv r^2$ is a square modulo $p$ and not divisible by $p$. If $x_{i-1}$ has these properties, then so does $x_i = x_{i-1}^2$. By induction they hold for all $i \ge 0$.

*Step 2: one square root.* For $i \ge 1$,

$$x_i^{e_p} \equiv \left(x_{i-1}^2\right)^{(p+1)/4} = x_{i-1}^{(p+1)/2} = x_{i-1}^{(p-1)/2} \cdot x_{i-1} \equiv x_{i-1} \pmod p,$$

by Euler's criterion applied to $x_{i-1}$, which is a square by Step 1.

*Step 3: $t + 1$ square roots.* Applying Step 2 for $i = t + 1, t, \ldots, 1$ gives

$$x_{t+1}^{e_p^{\,t+1}} = \left(\cdots\left(x_{t+1}^{e_p}\right)^{e_p}\cdots\right)^{e_p} \equiv x_0 \pmod p.$$

Line L10 sets $d_1 = e_p^{\,t+1} \bmod (p - 1)$. Write $e_p^{\,t+1} = d_1 + k(p-1)$ with $k \ge 0$. By Fermat's little theorem, $x_{t+1}^{p-1} \equiv 1$, because $x_{t+1}$ is a unit modulo $p$. So $u = x_{t+1}^{d_1} \equiv x_{t+1}^{e_p^{\,t+1}} \equiv x_0 \pmod p$ (line L11). In the same way $v \equiv x_0 \pmod q$.

*Step 4: the Chinese remainder step.* Let $z = vap + ubq$ (line L12). Modulo $p$, $z \equiv ubq = u(1 - ap) \equiv u \equiv x_0$. Modulo $q$, $z \equiv vap = v(1 - bq) \equiv v \equiv x_0$. So $p$ and $q$ both divide $z - x_0$, and since they are distinct primes, $n$ divides $z - x_0$. Line L12 reduces $z$ modulo $n$, and $0 \le x_0 < n$, so it returns exactly $x_0$.

*Step 5: the message.* Lines L13 and L14 square $x_0$ repeatedly modulo $n$, so they compute the same values $x_1, \ldots, x_t$ as encryption, and the same $\mathrm{low}_h(x_i)$. For each $i$, $\mathrm{low}_h(x_i) \oplus c_i = \mathrm{low}_h(x_i) \oplus \mathrm{low}_h(x_i) \oplus m_i = m_i$, because XOR is associative and $z \oplus z = 0$. So decryption returns $m_1, \ldots, m_t$ in order. $\blacksquare$
