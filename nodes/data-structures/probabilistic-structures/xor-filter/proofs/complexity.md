---
title: The false positive rate of an xor filter
proves: [complexity]
status: full
---

**Model.** Assume ideal hashing: in each try, $h_0, h_1, h_2$ and $\mathrm{fp}$ are independent random functions, with $h_j$ uniform on block $j$ and $\mathrm{fp}$ uniform on $\{0, \ldots, 2^r - 1\}$, and the tries use independent functions.

**Theorem 1.** For each key $x \notin S$, $\Pr[\text{QUERY}(x) = \text{true}] = 2^{-r}$.

*Proof.* Let $T$ be the try at which BUILD stops. Whether a try succeeds depends only on the cells of the keys of $S$ in that try, so $T$ is independent of the values at $x$ of the functions of all tries. The table $B$ is a function of the cells and fingerprints of the keys of $S$ in try $T$. Given $T = t$ and all the values on $S$, the values $h_0(x), h_1(x), h_2(x), \mathrm{fp}(x)$ of try $t$ are still independent and uniform, since $x \notin S$. So the xor $w = B[h_0(x)] \oplus B[h_1(x)] \oplus B[h_2(x)]$ is independent of $\mathrm{fp}(x)$, and
$$ \Pr[\mathrm{fp}(x) = w] = \sum_v \Pr[w = v] \cdot 2^{-r} = 2^{-r}. \quad \square $$

**Theorem 2 (time and space).** QUERY takes $\Theta(1)$ time: four hash values and three cell reads. Each try of BUILD takes $\Theta(n + \ell)$ time, which is $\Theta(n)$. The table has $3\ell r$ bits, with $3\ell \le 1.23 n + 35$.

*Proof.* Lines L6 and L7 visit each key and each cell once. In lines L8 and L9 each cell enters the queue at most once at line L7 and once for each time its count falls to 1, which is at most once for each key that uses it, so the queue has at most $3\ell + 3n$ entries in total, and each is handled in constant time. The loop of lines L4 and L5 has $n$ steps of constant time. The bound on $3\ell$ follows from $\ell \le (1.23 n + 32)/3 + 1$. With Theorem 2 of the correctness proof, the expected time of BUILD is $\Theta(n)/p$, which is $\Theta(n)$ whenever the success probability $p$ of a try is bounded below by a constant, as it is at this table size for large $n$ by the threshold result of Molloy (2005). $\blacksquare$
