---
title: Kasiski examination lists the repeat distances exactly, and true repeats give multiples of the period
proves: [correctness]
status: full
---

Let $c = c_0 \ldots c_{n-1}$ be a string of letters, let $\ell \ge 1$, and write $c[i] = c_i \ldots c_{i+\ell-1}$ for $0 \le i \le n - \ell$.

**Claim 1.** Lines L1 to L3 compute the multiset $D$ of the numbers $j - i$ over all pairs $i < j$ with $c[i] = c[j]$ and $c[t] \ne c[i]$ for each $t$ with $i < t < j$. In words: for each position, the distance to the next occurrence of the same piece, if there is one.

*Proof.* Lines L1 and L2 visit $i = 0, 1, \ldots, n - \ell$ in increasing order and append $i$ to the list of the piece $c[i]$. So, for each piece $s$, its list holds exactly the positions $q_1 < q_2 < \ldots < q_r$ with $c[q_t] = s$, in increasing order. A pair $i < j$ of such positions has no occurrence of $s$ between them if and only if $i = q_t$ and $j = q_{t+1}$ for some $t$. Line L3 adds $q_{t+1} - q_t$ for each $t < r$, and for each piece with $r \ge 2$, which is exactly the set of such pairs. Each position $i$ is the first member of at most one pair, so $|D| < n$. $\square$

**Claim 2.** Let a periodic cipher with period $m$ map the plaintext letters $p_0 \ldots p_{n-1}$ to $c_j = f_{j \bmod m}(p_j)$, for functions $f_0, \ldots, f_{m-1}$. If $p_i \ldots p_{i+\ell-1} = p_j \ldots p_{j+\ell-1}$ and $m \mid (j - i)$, then $c[i] = c[j]$.

*Proof.* For $0 \le t < \ell$, $j + t \equiv i + t \pmod m$, so $(j + t) \bmod m = (i + t) \bmod m$ and $c_{j+t} = f_{(i+t) \bmod m}(p_{j+t}) = f_{(i+t) \bmod m}(p_{i+t}) = c_{i+t}$. $\square$

The Vigenère cipher is such a cipher, with $f_r(x) = (x + k_r) \bmod 26$.

**Claim 3.** Call a distance $j - i$ in $D$ *true* if $p_i \ldots p_{i+\ell-1} = p_j \ldots p_{j+\ell-1}$ and $m \mid (j - i)$. If every distance in $D$ is true and $D$ is not empty, then $m$ divides $g = \gcd(D)$, and $m$ divides each element of $D$, so $\mathrm{count}(m) = |D|$ in line L4.

*Proof.* Each element of $D$ is a multiple of $m$ by the definition of true. So $m$ is a common divisor of $D$, and it divides the greatest common divisor $g$. $\square$

**What the claims do not say.** Claim 2 has no converse. Each $f_r$ is a bijection, so $c[i] = c[j]$ with $m \mid (j - i)$ forces equal plaintext, but $c[i] = c[j]$ with $m \nmid (j - i)$ can happen by chance, and then $j - i$ is a false hit. The gcd can also be a proper multiple of $m$. So line L5 is a heuristic choice: it returns the $m$ that divides the most distances beyond the count $|D|/m$ expected by chance, and no claim says that it is always the period.

Claim 1 proves that the method computes the repeat distances exactly, and Claims 2 and 3 prove the fact that the method rests on: true repeats give multiples of the period. $\blacksquare$
