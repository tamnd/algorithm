---
title: The KMR naming gives the ranks of all basic factors
proves: [correctness, termination, time.worst]
status: full
---

**Notation.** $T = T[0 \ldots n-1]$ with $n \ge 1$, positions 0-based. For $j \ge 0$ with $2^j \le n$, the *basic factors* of level $j$ are $F_j(i) = T[i \ldots i + 2^j - 1]$ for $0 \le i \le n - 2^j$. The claim is that KMR returns arrays with

> **(N)** $NAME_j[i]$ is the number of distinct strings among $F_j(0), \ldots, F_j(n - 2^j)$ that are smaller than $F_j(i)$,

for every level $j$ with $2^j \le n$. In particular, $NAME_j[i] = NAME_j[i']$ if and only if $F_j(i) = F_j(i')$, and $NAME_j[i] < NAME_j[i']$ if and only if $F_j(i) < F_j(i')$.

**Lemma 1 (doubling).** For $2^{j+1} \le n$ and $0 \le i \le n - 2^{j+1}$, $F_{j+1}(i) = F_j(i)\,F_j(i + 2^j)$. Two strings of the same length $2^{j+1}$ compare as the pairs of their halves, the first half first.

*Proof.* The first $2^j$ symbols of $F_{j+1}(i)$ are $F_j(i)$, and the next $2^j$ are $T[i + 2^j \ldots i + 2^{j+1} - 1] = F_j(i + 2^j)$; the index $i + 2^j \le n - 2^j$ is a valid start of level $j$. For strings $x = x_1 x_2$ and $y = y_1 y_2$ with $|x_1| = |y_1|$ and $|x_2| = |y_2|$, the first difference of $x$ and $y$ is in the first halves if $x_1 \ne y_1$, and otherwise in the second halves. $\square$

**Theorem 1.** At each test of line L3, (N) holds for the levels $0, \ldots, j$.

*Proof.* By induction on $j$. For $j = 0$, line L1 gives each symbol its rank among the distinct symbols, which is (N) for single symbols. Assume (N) for level $j$ and $2^{j+1} \le n$. Line L4 forms the pairs $(NAME_j[i], NAME_j[i + 2^j])$. By (N) for level $j$, the pairs compare as $(F_j(i), F_j(i + 2^j))$, so by Lemma 1 they compare as $F_{j+1}(i)$. Line L5 sorts the positions by the pairs; the two passes of the radix sort are stable counting sorts, the second key first, so the result is sorted by the pair. Lines L6 to L8 scan the sorted positions and increase the counter $r$ exactly when the pair differs from the one before. The first position gets $r = 0$, and the name of a position is the number of distinct pairs before its pair in sorted order, which is the number of distinct factors of level $j + 1$ smaller than $F_{j+1}(i)$. That is (N) for level $j + 1$. $\square$

**Termination.** The level $j$ increases by 1 in each round, and the loop stops when $2^{j+1} > n$, after $\lfloor \log_2 n \rfloor$ rounds. For $n = 0$ the algorithm returns at once.

**Corollary (comparison of factors).** For $1 \le \ell \le n$ and $k = \lfloor \log_2 \ell \rfloor$, the factor $T[p \ldots p + \ell - 1]$ is smaller than, equal to or larger than $T[q \ldots q + \ell - 1]$ as the pair $(NAME_k[p], NAME_k[p + \ell - 2^k])$ compares with $(NAME_k[q], NAME_k[q + \ell - 2^k])$.

*Proof.* Since $2^k \le \ell < 2^{k+1}$, the two windows of length $2^k$ at offsets 0 and $\ell - 2^k$ cover the factor, and they overlap or touch. If the first windows differ, the first difference of the two factors is inside them, and (N) gives the order. If the first windows are equal, the two factors agree on offsets $0$ to $2^k - 1$, which include the overlap $\ell - 2^k$ to $2^k - 1$. So their first difference, if any, is at an offset of at least $2^k$, inside the second windows, and the second windows compare as the factors do. $\square$

**Theorem 2 (time).** KMR takes $O(n \log n)$ time and $O(n \log n)$ words of space for all levels, after the symbols are mapped to their ranks.

*Proof.* Level $j + 1$ has $n - 2^{j+1} + 1 \le n$ positions. Line L4 and lines L6 to L8 take $O(n)$ time, and line L5 is two counting sorts with $n$ buckets, since names are below $n$, so $O(n)$ time. There are $\lfloor \log_2 n \rfloor$ rounds, and each level stores at most $n$ names. $\blacksquare$
