---
title: The false positive rate and the cost of a binary fuse filter
proves: [complexity]
status: full
---

**Model.** Assume ideal hashing: in each try, the start segment, the three offsets and the fingerprint of every key are independent and uniform, and different tries use independent functions.

**Theorem 1.** For each key $x \notin S$, $\Pr[\text{QUERY}(x) = \text{true}] = 2^{-r}$.

*Proof.* Whether a try succeeds depends only on the cells of the keys of $S$ in that try, so the final try $T$ is independent of the values of the functions at $x$. Given $T$ and all values on $S$, the table $B$ is fixed, and the cells and the fingerprint of $x$ in try $T$ are still independent and uniform. So $w = B[h_0(x)] \oplus B[h_1(x)] \oplus B[h_2(x)]$ is independent of $\mathrm{fp}(x)$, and $\Pr[\mathrm{fp}(x) = w] = 2^{-r}$. $\square$

**Theorem 2 (time and space).** QUERY takes $\Theta(1)$ time. Each try of BUILD takes $\Theta(n + tL)$ time, which is $\Theta(n)$ for the size rule, and the table has $(t + 2)L r$ bits.

*Proof.* A query computes one set of hash values and reads three cells. In PEEL, each cell enters the queue at most once at line L8 and once for each key that leaves it, so the queue handles at most $(t + 2)L + 3n$ entries, each in constant time; lines L4 and L5 take $n$ steps. For the size rule, $(t + 2)L \le \text{capacity} + 3L$, and $L \le 2^{2.25} n^{\ln 2/\ln 3.33} < 4.8\, n^{0.58}$ is $o(n)$, while capacity is $O(n)$ since the factor is at most $\max(1.125, 0.875 + 0.25 \ln(10^6)/\ln 2) < 6$. So the table has $O(n)$ cells. The expected number of tries is $1/p$, and the expected build time is $\Theta(n)$ whenever $p$ is bounded below by a constant, as the experiments of Graf and Lemire and the threshold results of Dietzfelbinger and Walzer indicate for this size factor. $\blacksquare$
