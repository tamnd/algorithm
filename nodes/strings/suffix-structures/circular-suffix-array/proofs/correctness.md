---
title: Cyclic prefix doubling sorts the rotations of a string
proves: [correctness, termination, time.worst]
status: full
---

**Notation.** $T = T[0 \ldots n-1]$ with $n \ge 1$, and all position arithmetic is modulo $n$. The rotation $R_i = T[i \ldots n-1]\,T[0 \ldots i-1]$. For $\ell \ge 1$, let $R_i^{(\ell)}$ be the string of length $\ell$ whose $k$-th symbol is $T[(i + k) \bmod n]$; it is the prefix of length $\ell$ of the infinite periodic word $R_i R_i R_i \cdots$. The claim is that CYCLIC-SORT returns $CA$ with $(R_{CA[0]}, CA[0]) < (R_{CA[1]}, CA[1]) < \cdots$ in the order that compares the rotation first and the position second.

**Lemma 1.** For $\ell \ge n$, $R_i^{(\ell)} < R_j^{(\ell)}$ if and only if $R_i < R_j$, and $R_i^{(\ell)} = R_j^{(\ell)}$ if and only if $R_i = R_j$.

*Proof.* $R_i^{(n)} = R_i$. If $R_i \ne R_j$, the two rotations have the same length $n$, so they first differ at some offset $k < n$, and $R_i^{(\ell)}$ and $R_j^{(\ell)}$ first differ at the same offset $k$ with the same two symbols. If $R_i = R_j$, then the two periodic words are equal, so all their prefixes are equal. $\square$

**Lemma 2 (doubling).** $R_i^{(2\ell)} = R_i^{(\ell)} R_{i+\ell}^{(\ell)}$. So $R_i^{(2\ell)} < R_j^{(2\ell)}$ if and only if the pair $(R_i^{(\ell)}, R_{i+\ell}^{(\ell)})$ is smaller than $(R_j^{(\ell)}, R_{j+\ell}^{(\ell)})$ in the order that compares the first component first.

*Proof.* The symbol at offset $k \ge \ell$ of $R_i^{(2\ell)}$ is $T[i + k] = T[(i + \ell) + (k - \ell)]$, which is the symbol at offset $k - \ell$ of $R_{i+\ell}^{(\ell)}$. Two strings of the same length $2\ell$ compare as the pairs of their halves. $\square$

**Invariant.** At each test of line L4 with the current value $\ell$ of $length$:

> **(D)** $p$ is a permutation of $0, \ldots, n-1$ with $R_{p[0]}^{(\ell)} \le R_{p[1]}^{(\ell)} \le \cdots \le R_{p[n-1]}^{(\ell)}$, and $cls[i]$ is the number of distinct strings among $R_0^{(\ell)}, \ldots, R_{n-1}^{(\ell)}$ that are smaller than $R_i^{(\ell)}$. In particular $0 \le cls[i] < n$, and $cls[i] < cls[j]$ if and only if $R_i^{(\ell)} < R_j^{(\ell)}$.

*Initialization.* Before the first test, $\ell = 1$ and $R_i^{(1)} = T[i]$. The symbols are mapped to their ranks among the distinct symbols, which is exactly the class of (D), and line L2 sorts the positions by this key.

*Maintenance.* Assume (D) for $\ell$, with $\ell < n$. Line L5 sets $pn[r] = p[r] - \ell$. As $r$ goes from 0 to $n-1$, the position $x = pn[r]$ has $x + \ell = p[r]$, so the list $pn$ is sorted by $R_{x+\ell}^{(\ell)}$, the second half of $R_x^{(2\ell)}$ (Lemma 2). It is a permutation, because $x \mapsto x - \ell$ is a bijection modulo $n$. Line L6 sorts $pn$ stably by $cls[x]$, that is, by the first half. A stable sort by the first key of a list already sorted by the second key gives the list sorted by the pair, so by Lemma 2 the new $p$ is sorted by $R_x^{(2\ell)}$. Line L7 walks through the new $p$. Two neighbors have equal $R^{(2\ell)}$ if and only if both halves are equal, which (D) lets us test by the classes, and the new class increases by 1 exactly when the string changes. Since $p$ is sorted, the new class of $x$ is the number of distinct values below $R_x^{(2\ell)}$. Line L8 doubles $\ell$, so (D) holds at the next test.

*Termination.* $\ell$ takes the values $1, 2, 4, \ldots$, so the loop stops after $\lceil \log_2 n \rceil$ rounds, when $\ell \ge n$. Then by (D) and Lemma 1, $cls[i] < cls[j]$ if and only if $R_i < R_j$, and $cls[i] = cls[j]$ if and only if $R_i = R_j$. Line L9 sorts the list $0, 1, \ldots, n-1$ stably by $cls$. The result is sorted by rotation, and equal rotations keep the increasing order of their positions. This is the claim. For $n = 0$, line L1 returns the empty array. $\square$

**Theorem (time).** CYCLIC-SORT takes $O(n \log n)$ time after the symbols are mapped to $0, \ldots, \sigma - 1$.

*Proof.* Lines L5 to L8 take $O(n)$ time: a counting sort with $n$ buckets is $O(n)$, and line L7 makes $O(1)$ class comparisons for each $r$. There are $\lceil \log_2 n \rceil$ rounds. Lines L2 and L9 are counting sorts with at most $n$ buckets, since $\sigma \le n$. The mapping of symbols takes $O(n)$ time for an integer alphabet of size $O(n)$ and $O(n \log n)$ comparisons for a general ordered alphabet. $\blacksquare$
