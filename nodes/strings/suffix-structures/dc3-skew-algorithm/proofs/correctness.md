---
title: The DC3 algorithm sorts the suffixes in linear time
proves: [correctness, termination, time.worst]
status: full
---

**Notation.** $T = T[0 \ldots n-1]$ with symbols in $\{1, \ldots, K\}$, and $T[n] = T[n+1] = T[n+2] = 0$. Positions are 0-based, $T_i = T[i \ldots n-1]$, and the order is lexicographic with a proper prefix first. For $i \ge n$, $T_i$ is the empty string. Because 0 is smaller than all symbols, comparing the padded strings $T[i \ldots n+2]$ gives the same order as comparing the suffixes, and two different suffixes never compare equal. Let $n_0 = \lceil n/3 \rceil$, $n_1 = \lfloor (n+1)/3 \rfloor$, $n_2 = \lfloor n/3 \rfloor$: the numbers of positions $i < n$ with $i \bmod 3 = 0, 1, 2$. The *sample* $B_{12}$ is the set of positions $i < n + (n_0 - n_1)$ with $i \bmod 3 \ne 0$. When $n \bmod 3 = 1$, it contains the dummy position $n$, whose suffix is empty.

**Lemma 1 (reduced string).** Let $name(i)$ be the rank of the triple $T[i \ldots i+2]$ among the distinct triples of the sample, from 1. Let $R$ be the string $name(1)\,name(4)\,name(7) \cdots$ (all sample positions $\equiv 1$, $n_0$ of them) followed by $name(2)\,name(5) \cdots$ (all $\equiv 2$, $n_2$ of them). For sample positions $i$ and $j$, $T_i < T_j$ if and only if the suffix of $R$ that starts at the index of $i$ is smaller than the suffix that starts at the index of $j$.

*Proof.* The suffix of $R$ at the index of $i \equiv 1$ is $name(i)\,name(i+3) \cdots$ up to the end of the first half, followed by the names of the second half. The run of names $name(i)\,name(i+3) \cdots$ spells $T_i$ triple by triple, padded with zeros. The last triple of the first half contains a 0: if $n \bmod 3 \ne 1$, the last position $\equiv 1$ below $n$ is $n - 1$ or $n - 2$, whose triple reaches index $n$; if $n \bmod 3 = 1$, it is the dummy $n$ with triple $(0, 0, 0)$. A triple that contains a 0 can be equal to another triple only if the zeros are at the same offsets, which happens only for the triples that end at the same place in $T$. So when two suffixes of $R$ are compared, they differ at the latest at the first triple that contains the end of $T$, before the comparison reaches the second half of $R$ (except for two equal triples at the very same position, which means $i = j$). For two positions $\equiv 2$ the same argument applies, since the last triple of the second half also contains a 0. Comparing names in order is comparing triples in order, and comparing triples is comparing the padded suffixes. $\square$

**Lemma 2 (sample ranks).** After lines L4 to L7, $rank(i)$ for $i \in B_{12}$ is the rank of $T_i$ among the sample suffixes, from 1, and $rank(i) = 0$ for $i \ge n + (n_0 - n_1)$ through the padding.

*Proof.* If all names are different (line L7), the triple order is the suffix order, because two suffixes that differ in the first triple compare as the triples. Otherwise line L6 sorts the suffixes of $R$, which by Lemma 1 orders the sample suffixes; the recursion is correct by induction on $n$, since $|R| = n_0 + n_2 < n$ for $n \ge 2$. $\square$

**Lemma 3 (non-sample order).** For $i, j \equiv 0$, $T_i < T_j$ if and only if $(T[i], rank(i+1)) < (T[j], rank(j+1))$.

*Proof.* $T_i = T[i]\,T_{i+1}$ and $i + 1 \in B_{12}$ or $i + 1 \ge n$. If $T[i] \ne T[j]$ the first symbols decide. Otherwise $T_{i+1}$ and $T_{j+1}$ decide, and by Lemma 2 their ranks compare as they do. Line L8 takes the positions $i + 1 \equiv 1$ in the sorted sample order, which is sorted by $rank(i+1)$, and sorts them stably by $T[i]$, so the result is sorted by the pair. $\square$

**Lemma 4 (merge).** For $i \equiv 0$ and $j \in B_{12}$:

- if $j \equiv 1$: $T_i < T_j$ if and only if $(T[i], rank(i+1)) < (T[j], rank(j+1))$, because $i + 1 \equiv 1$ and $j + 1 \equiv 2$ are both in the sample or beyond the end;
- if $j \equiv 2$: $T_i < T_j$ if and only if $(T[i], T[i+1], rank(i+2)) < (T[j], T[j+1], rank(j+2))$, because $i + 2 \equiv 2$ and $j + 2 \equiv 1$ are both in the sample or beyond the end.

*Proof.* As in Lemma 3, peel one or two symbols and compare the rest by the sample ranks. A rank of 0 belongs to an empty suffix and is smaller than all others. The pairs or triples are never equal for $i \ne j$, since the suffixes are different. $\square$

**Theorem 1 (correctness).** DC3 returns the suffix array of $T$.

*Proof.* The sample suffixes are sorted by Lemma 2, without the dummy, which is the smallest and is skipped at the start of the merge. The other suffixes are sorted by Lemma 3. Line L9 merges two sorted lists, and by Lemma 4 each comparison of the merge is correct. So the result lists all $n$ suffixes in order. For $n \le 1$ the result is trivial. $\square$

**Theorem 2 (time).** DC3 runs in $O(n)$ time when $K = O(n)$.

*Proof.* Without the recursion, each line is a scan or a counting sort with $O(K + n)$ buckets; in the recursive calls the alphabet is the names, at most the length of the string. The reduced string has length $n_0 + n_2 \le \lceil 2n/3 \rceil + 1$, so the time satisfies $t(n) \le t(\lceil 2n/3 \rceil + 1) + O(n)$, whose solution is $O(n)$. The recursion depth is $O(\log n)$, and the recursion stops, since the length drops for $n \ge 2$ and the case $n \le 1$ returns at once. $\blacksquare$
