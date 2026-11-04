---
title: The false positive rate and the cost of a ribbon filter
proves: [complexity]
status: full
---

**Model.** Assume ideal hashing: in each try, $s(x)$ is uniform on $\{0, \ldots, m - w\}$, the bits $1, \ldots, w - 1$ of $c(x)$ are uniform, and $\mathrm{fp}(x)$ is uniform on $\{0, \ldots, 2^r - 1\}$, independently for all keys and all tries.

**Theorem 1.** For each key $x \notin S$, $\Pr[\text{QUERY}(x) = \text{true}] = 2^{-r}$.

*Proof.* Whether a try succeeds depends only on the hash values of the keys of $S$ in that try. So the final try is independent of the values at $x$, and given the final try and all the values on $S$, the array $Z$ is fixed while $s(x)$, $c(x)$ and $\mathrm{fp}(x)$ are still independent and uniform. The value $v = \bigoplus_{j : c_j(x) = 1} Z[s(x) + j]$ is a function of $Z$, $s(x)$ and $c(x)$ only, so it is independent of $\mathrm{fp}(x)$, and $\Pr[\mathrm{fp}(x) = v] = 2^{-r}$. $\square$

**Theorem 2 (time and space).** Each INSERT-ROW takes at most $w$ rounds of $O(1)$ operations on $w$-bit words, so one try of the build takes $O(n w)$ word operations, and in the row-major layout BACK-SUBSTITUTE takes $O(m w)$ operations on $r$-bit values. A query takes $\Theta(w)$ steps in the row-major layout. The array has $m r$ bits.

*Proof.* The bound on the rounds is Theorem 2 of the correctness proof. Each round does a xor of two rows and two right sides, a test, and a shift by the index of the lowest set bit. Line L9 does at most $w - 1$ xors for each of the $m$ rows. A query reads at most $w$ values. $\blacksquare$
