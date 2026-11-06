---
title: The Lucy_Hedgehog method returns pi(x)
proves: [correctness]
status: full
---

For $m \ge 2$ let $\mathrm{lpf}(m)$ be the least prime factor of $m$; a composite $m$ satisfies $\mathrm{lpf}(m)^2 \le m$, because $m = \mathrm{lpf}(m) \cdot k$ with $k \ge 2$, and every prime factor of $k$ is at least $\mathrm{lpf}(m)$. For $q \ge 1$ and $v \ge 0$ let $S_q(v) = \#\{ 2 \le n \le v : n \text{ prime or } \mathrm{lpf}(n) > q \}$.

If $x < 2$, line L1 returns 0, which is $\pi(x)$. Assume $x \ge 2$, so $r = \lfloor \sqrt x \rfloor \ge 1$, and let $V = \{\lfloor x/k \rfloor : k \ge 1\}$.

**Facts about $V$.** (a) For $v \in V$ and an integer $p \ge 1$, $\lfloor v/p \rfloor \in V$ or $\lfloor v/p \rfloor = 0$: if $v = \lfloor x/k \rfloor$, then $\lfloor v/p \rfloor = \lfloor x/(kp) \rfloor$, since writing $x = kpq + s$ with $0 \le s < kp$ gives $\lfloor x/k \rfloor = pq + \lfloor s/k \rfloor$ with $\lfloor s/k \rfloor < p$. (b) Every integer $1 \le v \le r$ is in $V$. Let $k = \lfloor x/v \rfloor$; then $k \ge x/v - 1$ and, since $v^2 \le x$, $k \ge v$. As $k \le x/v$, $\lfloor x/k \rfloor \ge v$. If $\lfloor x/k \rfloor \ge v + 1$, then $k(v+1) \le x$, so $x/v - 1 < k \le x/(v+1)$, which gives $x < v(v+1)$; but $k \ge v$ and $k(v + 1) \le x$ give $v(v+1) \le x$, a contradiction. So $\lfloor x/k \rfloor = v$.

**Invariant.** For $p = 2, \ldots, r + 1$: at the start of round $p$ of line L4 (or after the loop, for $p = r + 1$), $S[v] = S_{p-1}(v)$ for all $v \in V$.

*Base.* For $p = 2$, line L3 sets $S[v] = v - 1 = \#\{2 \le n \le v\} = S_1(v)$, since every $n \ge 2$ has $\mathrm{lpf}(n) \ge 2 > 1$.

*Step.* Assume the invariant at the start of round $p$, with $2 \le p \le r$. By fact (b), $p$ and $p - 1$ lie in $V$.

First, $S_{p-1}(p) - S_{p-1}(p-1)$ is 1 if $p$ counts in $S_{p-1}(p)$ and 0 otherwise, that is, 1 if and only if $p$ is prime or $\mathrm{lpf}(p) > p - 1$. As $\mathrm{lpf}(p) \le p$, $\mathrm{lpf}(p) > p - 1$ means $\mathrm{lpf}(p) = p$, that is, $p$ is prime. So the test of line L5 holds exactly when $p$ is composite.

*Case $p$ composite.* No $n$ has $\mathrm{lpf}(n) = p$, since $\mathrm{lpf}(n)$ is prime. So $\mathrm{lpf}(n) > p - 1$ if and only if $\mathrm{lpf}(n) > p$, hence $S_p = S_{p-1}$, and line L5 leaves $S$ unchanged, as required.

*Case $p$ prime.* Comparing the definitions, $S_{p-1}(v) - S_p(v)$ is the number of $2 \le n \le v$ that are not prime and have $\mathrm{lpf}(n) = p$; call this $C_p(v)$. If $v < p^2$, then $C_p(v) = 0$, because a composite $n$ with $\mathrm{lpf}(n) = p$ has $n \ge p^2$. Let $v \ge p^2$ and $w = \lfloor v/p \rfloor \ge p$. The map $n \mapsto k = n/p$ is a bijection from the composites $n \le v$ with $\mathrm{lpf}(n) = p$ to the integers $2 \le k \le w$ with $\mathrm{lpf}(k) \ge p$: if $n = pk$ is such a composite, then $k \ge 2$, $k \le v/p$, and every prime factor of $k$ divides $n$, hence is at least $p$; conversely, if $2 \le k \le w$ has $\mathrm{lpf}(k) \ge p$, then $n = pk \le v$ is composite with $\mathrm{lpf}(n) = p$. The integers $2 \le k \le w$ that count in $S_{p-1}(w)$ are those that are prime or have $\mathrm{lpf}(k) \ge p$; the ones among them with $\mathrm{lpf}(k) < p$ are exactly the primes below $p$, and all $\pi(p - 1)$ of them are at most $p - 1 < w$. Hence $C_p(v) = S_{p-1}(w) - \pi(p - 1)$. Finally $S_{p-1}(p - 1) = \pi(p - 1)$, because every $2 \le n \le p - 1$ has $\mathrm{lpf}(n) \le n \le p - 1$, so only the primes count. By the invariant, line L6 sets $c = S_{p-1}(p - 1) = \pi(p - 1)$.

Line L7 visits the $v \in V$ with $v \ge p^2$ in decreasing order. When it updates $v$, it reads $S[w]$ with $w = \lfloor v/p \rfloor \in V$ by fact (a) ($w \ge p \ge 1$), and $w < v$; every value updated earlier in this round is larger than $v$, so $S[w]$ still holds $S_{p-1}(w)$. Also $p - 1 < p^2$, so $S[p - 1]$ is not changed in this round, and $c$ is correct throughout. So line L8 sets $S[v] = S_{p-1}(v) - (S_{p-1}(w) - \pi(p-1)) = S_{p-1}(v) - C_p(v) = S_p(v)$. Each $v$ is updated once, from its old value $S_{p-1}(v)$. The values $v < p^2$ are not touched and keep $S_{p-1}(v) = S_p(v)$. So the invariant holds at the start of round $p + 1$.

**Conclusion.** After the loop, $S[x] = S_r(x)$ (and $x \in V$ with $k = 1$). Every composite $n \le x$ has $\mathrm{lpf}(n) \le \sqrt n \le \sqrt x$, hence $\mathrm{lpf}(n) \le r$, so it does not count in $S_r(x)$, while every prime $n \le x$ does. So line L9 returns $S_r(x) = \pi(x)$.

**The two arrays.** The implementation stores $S[v]$ at `small[v]` for $v \le r$ and at `large[k]` for $v = \lfloor x/k \rfloor$, $1 \le k \le r$. Every $v \in V$ with $v > r$ has such a $k$, namely $k = \lfloor x/v \rfloor$: from $v = \lfloor x/j \rfloor$ we get $j \le x/v$, so $j \le k$ and $\lfloor x/k \rfloor \le v$, while $k \le x/v$ gives $\lfloor x/k \rfloor \ge v$; and $k \le x/v < x/\sqrt x = \sqrt x$, so $k \le r$. The loop over `large` for $k = 1, 2, \ldots$ followed by the loop over `small` from $r$ down is a pass in decreasing order of $v$, the cell read for $\lfloor x/(kp) \rfloor$ is `large[kp]` if $kp \le r$ and `small[x // (kp)]` otherwise, and in the latter case $\lfloor x/(kp) \rfloor \le r$ holds, because $kp \ge r + 1 > \sqrt x$. A value stored in both arrays receives the same update in both, from the same old values, so the two copies stay equal. $\blacksquare$
