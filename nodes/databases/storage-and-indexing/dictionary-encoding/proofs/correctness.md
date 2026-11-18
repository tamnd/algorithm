---
title: Dictionary encoding decodes every value back, keeps the order when the dictionary is sorted, and answers selections on codes alone
proves: [correctness]
status: full
---

We use the notation of the page. A column is a list $a_0, \ldots, a_{N-1}$ of values, each of them NULL or an element of a set on which $<$ is a total order. The dictionary $D = (D[0], \ldots, D[d-1])$ lists the distinct non-null values once each (line L1), $\mathrm{code}(D[x]) = x + 1$ and $\mathrm{code}(\mathrm{NULL}) = 0$ (line L2), and $w$ is the number of bits of $d$, at least 1 (line L3). A comparison with NULL is never true.

**Lemma 1 (codes fit).** The map code is a bijection from the values of the column, with NULL, to $\{0, 1, \ldots, d\}$, and every code fits in $w$ bits.

*Proof.* The entries of $D$ are distinct, so $x \mapsto D[x]$ is a bijection from $\{0, \ldots, d-1\}$ to the non-null values, and $x + 1$ maps it to $\{1, \ldots, d\}$. NULL alone has code 0. If $d = 0$ the only code is 0 and $w = 1$. Otherwise $d$ has $w$ bits, so $d < 2^w$, and every code is at most $d$. $\square$

**Lemma 2 (round trip).** For every $i$, `code_at(i)` returns $\mathrm{code}(a_i)$, and `decode(i)` returns $a_i$.

*Proof.* Line L4 writes the $w$ bits of $\mathrm{code}(a_i)$ at the bit positions $iw$ to $iw + w - 1$. For $i \ne j$ these ranges are disjoint, and the array starts with all bits 0, so writing one code does not change another, and the bits of code $i$ are exactly the bits of $\mathrm{code}(a_i)$, which fit by Lemma 1. Line L5 reads the same $w$ positions in the same order of significance. Line L6 maps 0 to NULL and $c \ge 1$ to $D[c - 1]$, the inverse of the map of line L2. $\square$

The array has $\lceil N w / 8 \rceil$ bytes.

**Lemma 3 (order).** If the dictionary is ordered, then for non-null values $a$ and $b$ of the column, $a < b$ if and only if $\mathrm{code}(a) < \mathrm{code}(b)$, and $a = b$ if and only if the codes are equal.

*Proof.* In the ordered case line L1 sorts the distinct values, so $D$ is strictly increasing: $D[x] < D[y]$ if and only if $x < y$. Add 1 to both sides. Equality follows from Lemma 1. $\square$

If the dictionary is in order of first appearance, Lemma 3 fails in general: in the example of the page, Paris has code 1 and Athens has code 4.

**Theorem 1 (selection).** For a comparison $\theta$ in $=, \ne, <, \le, >, \ge$ and a constant $v$, SELECT returns, in increasing order, exactly the positions $i$ with $a_i$ not NULL and $a_i \mathbin{\theta} v$ true. It reads no entry of $D$ at those positions.

*Proof.* If $v$ is NULL no comparison is true, and SELECT returns the empty list. Otherwise let $\ell$ be the number of entries of $D$ that are less than $v$ and $h$ the number that are at most $v$. These are the results of the two binary searches of line L8, and they are correct because $D$ is sorted in the ordered case. Since $D$ is strictly increasing, the indices $x$ with $D[x] \mathbin{\theta} v$ form an interval:

| $\theta$ | $=$ | $<$ | $\le$ | $>$ | $\ge$ |
|---|---|---|---|---|---|
| indices $x$ | $[\ell, h)$ | $[0, \ell)$ | $[0, h)$ | $[h, d)$ | $[\ell, d)$ |

The code range of line L8 is this interval shifted by 1. Its smallest possible code is 1, so the NULL code 0 is never in it. By Lemma 2, line L9 keeps position $i$ if and only if $\mathrm{code}(a_i)$ is in the range, that is, if and only if $a_i$ is not NULL and $a_i \mathbin{\theta} v$. Note that $v$ need not be in $D$.

In the other case (an unordered dictionary, or $\theta$ is $\ne$), lines L10 and L11 compare $v$ with each entry $D[x]$ and put $x + 1$ in $S$ exactly when $D[x] \mathbin{\theta} v$. The code 0 is never put in $S$. By Lemma 2, line L12 keeps $i$ if and only if $a_i$ is not NULL and $a_i \mathbin{\theta} v$. When $\theta$ is $\ne$ and $v$ is in $D$, the implementation skips the loop and keeps the codes other than 0 and $\mathrm{code}(v)$; by Lemma 1 these are the codes of the non-null values different from $v$, so the result is the same.

Every branch visits the positions in increasing order and reads only codes, and the dictionary only at lines L8 and L11, never at a position. $\square$

**Theorem 2 (cost).** The ordered branch makes $O(\log d)$ comparisons of values and reads $N$ codes. The unordered branch makes $d$ comparisons of values and reads $N$ codes, each with a test of membership in $S$.

*Proof.* A binary search in a sorted list of $d$ entries makes at most $\lfloor \log_2 d \rfloor + 1$ comparisons, and line L8 makes two of them. Line L11 makes one comparison for each entry of $D$. Lines L9 and L12 read each code once. $\square$

If $S$ is held as a bitmap of $d + 1$ bits, each membership test is one bit read, so both branches take $O(N)$ steps after the dictionary work, and only the comparisons of the values, which may be long strings, differ.
