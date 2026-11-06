---
title: The segmented sieve returns exactly the primes in [L, R]
proves: [correctness]
status: full
---

For $m \ge 2$ let $\mathrm{lpf}(m)$ be the least prime factor of $m$. Recall that a composite $m$ satisfies $\mathrm{lpf}(m)^2 \le m$: writing $m = q k$ with $q = \mathrm{lpf}(m)$, every prime factor of $k \ge 2$ divides $m$ and so is at least $q$, which gives $k \ge q$.

After line L1, $L \ge 2$. If $L > R$, there is no integer in $[\max(L,2), R]$ and the empty answer is correct; this covers $R < 2$. From now on $2 \le L \le R$. Line L2 is the [sieve of Eratosthenes](/sieve-of-eratosthenes/), so `base` is the increasing list of all primes $p \le \lfloor \sqrt R \rfloor$, that is, all primes with $p^2 \le R$.

**The blocks.** Line L3 sets $lo = L$. Each pass of the loop of line L4 handles the block $[lo, hi]$ with $hi = \min(lo + B - 1, R) \ge lo$, since $B \ge 1$ and $lo \le R$, and line L11 sets the next $lo$ to $hi + 1$. So the blocks are $[L, hi_1], [hi_1 + 1, hi_2], \ldots$, consecutive, disjoint and in increasing order, and each has at least one number. The loop stops at the first $lo > R$; since $lo$ grows by at least 1 in each pass, it stops, and the last block ends at $hi = R$. So the blocks cover $[L, R]$ exactly.

**One block.** Fix a block $[lo, hi]$ with $2 \le lo \le hi \le R$. Line L6 sets every flag to true, and only line L9 changes a flag, always to false. We show that after line L9 is done, for $lo \le m \le hi$, the flag $S[m - lo]$ is false if and only if $m$ is composite.

*Only composites are cleared.* Line L9 clears $m = s + tp$ for a base prime $p$ and an integer $t \ge 0$, where $s$ from line L8 is a multiple of $p$ with $s \ge p^2$. So $m$ is a multiple of $p$ and $m \ge p^2 > p$; such an $m$ has the proper divisor $p > 1$ and is composite.

*Every composite is cleared.* Let $m$ in $[lo, hi]$ be composite and $q = \mathrm{lpf}(m)$. Then $q^2 \le m \le R$, so $q$ is a base prime, and $q^2 \le m \le hi$, so line L7 handles $q$. Line L8 sets $s = \max(q^2, \lceil lo / q \rceil q)$. Both terms are multiples of $q$. The number $\lceil lo/q \rceil q$ is the least multiple of $q$ that is at least $lo$, so it is at most $m$; also $q^2 \le m$. Hence $s \le m$, and $m - s$ is a multiple of $q$, as both are. So $m = s + tq$ for some $t \ge 0$, and since $m \le hi$, the loop of line L9 reaches $m$ and clears its flag.

*Line L8 is well defined.* $\lceil lo / q \rceil$ is computed in integers as $\lfloor (lo + q - 1)/q \rfloor$; nothing else is needed.

So line L10 appends exactly the primes of $[lo, hi]$, in increasing order of $j$.

*Termination of one block.* Line L7 runs over a finite list, and line L9 advances $m$ by $p \ge 2$ until it passes $hi$.

**Conclusion.** The blocks partition $[L, R]$ in increasing order, and each block appends its primes in increasing order. So the list returned in line L12 is the increasing list of all primes $p$ with $L \le p \le R$. $\blacksquare$

**Cost of marking.** For a base prime $p$ and a block of length $\ell$, line L9 runs at most $\lfloor \ell / p \rfloor + 1$ times, since its values are distinct multiples of $p$ in an interval of length $\ell$. Summing over the blocks and the base primes gives the bound in the complexity section.
