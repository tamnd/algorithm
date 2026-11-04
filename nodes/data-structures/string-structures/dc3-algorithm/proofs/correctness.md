---
title: DC-v sorts the sample by recursion and all suffixes by one comparison through the sample
proves: [correctness]
status: full
---

We use the pseudocode and notation of the page. Let $t$ have length $n$, with $t[p] = 0$ for $p \ge n$ and $t[p] \ge 1$ for $p < n$. Write $T_i$ for the suffix $t[i \ldots]$, read with its trailing zeros, and $T_i < T_j$ for the lexicographic order; for $i \ne j$, $T_i \ne T_j$, since $T_i$ has its first zero at offset $n - i$. The proof is by induction on $n$: we assume that DC returns the suffix array of every shorter string, and the base case $n \le 2v$ sorts directly.

**Lemma 1 (the first difference of two sample suffixes).** Let $i \ne j$ be in $S$, and let $q$ be the least $q \ge 0$ with $t[i + q] \ne t[j + q]$. If $i$ is in class $d$ and $i'$ is the last position of class $d$ in $S$, then $i + q < i' + v$.

*Proof.* The position $i'$ is the largest $p \le n$ with $p \equiv d$, so $i' > n - v$ and $i' + v - 1 \ge n$. The first zero of $T_i$ is at offset $n - i$, and $T_j$ has a nonzero letter there unless $n - i \ge n - j$; in the same way $T_i$ has a nonzero letter at offset $n - j$ unless $n - j \ge n - i$. Since $i \ne j$, the two first zeros are at different offsets, so $q \le \min(n - i, n - j) \le n - i$, and $i + q \le n \le i' + v - 1$. $\square$

**Lemma 2 (the sample ranks).** After line L5, for $i, j \in S$, $rank[i] < rank[j]$ if and only if $T_i < T_j$, and the ranks are $1, \ldots, \lvert S \rvert$.

*Proof.* Line L2 gives equal names to equal $v$-tuples and orders the names like the tuples. If all names differ, the order of the names is the order of the first $v$ letters, which decides each comparison, so the names are the ranks. Otherwise let $W$ be the string of names of line L4, and let $\sigma(i)$ be the place of $i$ in $W$. For $i$ in class $d$, the letters of $W$ from $\sigma(i)$ up to the end of the block of class $d$ are the names of $i, i + v, \ldots, i'$, which are the names of the consecutive $v$-blocks of $T_i$ up to offset $i' - i + v - 1$. Compare $T_i$ and $T_j$, with $q$ as in Lemma 1, and let $p = \lfloor q / v \rfloor$. The blocks $0, \ldots, p - 1$ of $T_i$ and $T_j$ are equal, so they have the same names, and block $p$ differs at its letter $q - pv$, so the names of block $p$ differ in the same direction as $t[i + q]$ and $t[j + q]$. By Lemma 1 applied to $i$ and to $j$, block $p$ of each suffix is still inside the block of its class in $W$. So the suffixes of $W$ at $\sigma(i)$ and $\sigma(j)$ first differ at offset $p$, in the same direction as $T_i$ and $T_j$. $W$ is shorter than $t$ when $n > 2v$, since $\lvert S \rvert \le \lvert D \rvert \lceil (n + 1)/v \rceil < n$, so by induction line L4 returns its suffix array, and line L5 ranks $S$ in the order of the $T_i$. $\square$

Set $rank[p] = 0$ for $p > n$. This is consistent with the order: such a $p$ is never compared with a rank unless the letters before it already include a zero at a place where the other suffix has a zero too, which we treat in Lemma 3.

**Lemma 3 (the comparison).** Let $i, j < n$, $i \ne j$, and let $\ell < v$ be such that $i + \ell$ and $j + \ell$ are in classes of $D$. Then $T_i < T_j$ if and only if $(t[i \ldots i + \ell - 1], rank[i + \ell]) < (t[j \ldots j + \ell - 1], rank[j + \ell])$ in lexicographic order.

*Proof.* $T_i$ is $t[i \ldots i + \ell - 1]$ followed by $T_{i + \ell}$, and the same for $j$. If the first $\ell$ letters differ, both sides are decided by them. If they are equal, then neither contains a zero: a zero at offset $r < \ell$ in both would put both first zeros at the same offset, so $n - i = n - j$. Hence $i + \ell \le n$ and $j + \ell \le n$, both are in $S$, $i + \ell \ne j + \ell$, and the comparison of $T_i$ and $T_j$ is the comparison of $T_{i + \ell}$ and $T_{j + \ell}$, which by Lemma 2 is that of their ranks. $\square$

**Line L6.** For a position $i$ of class $c$, $i + \ell_c$ is in a class of $D$, so by Lemma 3 with $j$ in the same class and $\ell = \ell_c$, sorting by the key $(t[i \ldots i + \ell_c - 1], rank[i + \ell_c])$ sorts the class in the order of the suffixes. The radix sort is correct, and the keys of distinct positions differ by Lemma 3, so the order is strict.

**Lines L7 and L8.** For classes $a$ and $b$, $D$ is a difference cover, so there are $x, y \in D$ with $x - y \equiv a - b \pmod v$. With $\ell = (x - a) \bmod v$, $(a + \ell) \bmod v = x$ and $(b + \ell) \bmod v = (b + x - a) \bmod v = y$, both in $D$, so the least such $\ell$ exists and $off[a][b]$ is defined. By Lemma 3, the comparison of line L8 is the order of the suffixes, for any two positions. Merging lists that are sorted in this order, with this comparison, gives all positions $0, \ldots, n - 1$ in the order of their suffixes, which is the suffix array. $\blacksquare$
