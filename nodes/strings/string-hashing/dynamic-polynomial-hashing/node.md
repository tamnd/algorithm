---
tag: CMDN0R
kind: technique
slug: dynamic-polynomial-hashing
name: Dynamic polynomial hashing
aliases:
- hashing with point updates
- segment-tree string hashing
area: strings/string-hashing
level: advanced
summary: Maintain polynomial hashes of a string under point updates and answer substring hash queries with a Fenwick or segment tree.
prereqs: [polynomial-rolling-hash, polynomial-hash-collision-bound, fenwick-tree, segment-tree]
see_also: [substring-equality-queries, longest-common-extension-query, palindrome, implicit-treap, rope, lazy-propagation, modular-inverse, anti-hash-tests]
sources:
  - url: https://ioinformatics.org/journal/INFOL119.pdf
    title: Jakub Pachocki and Jakub Radoszewski, Where to use and how not to use polynomial string hashing, Olympiads in Informatics 7 (2013), 90-100
    locator: Section 2 (the polynomial hash and the hash of a substring from prefix hashes, which the trees on this page make dynamic)
  - paper: doi:10.1002/spe.4380240306
    title: Peter M. Fenwick, A new data structure for cumulative frequency tables, Software Practice and Experience 24(3) (1994), 327-336
    locator: the tree of partial sums with point updates and prefix sums in O(log n) time
  - paper: doi:10.1007/BF02522825
    title: Kurt Mehlhorn, R. Sundar and Christian Uhrig, Maintaining dynamic sequences under equality tests in polylogarithmic time, Algorithmica 17(2) (1997), 183-198
    locator: the signatures that give exact equality tests on a collection of strings under concatenation and splitting
  - url: https://arxiv.org/abs/1511.02612
    title: Paweł Gawrychowski, Adam Karczmarz, Tomasz Kociumaka, Jakub Łącki and Piotr Sankowski, Optimal dynamic strings, SODA 2018 (arXiv 1511.02612)
    locator: the abstract and introduction (updates in O(log n) time with high probability, comparisons in O(1) time, and the Ω(log n) lower bound for equality tests)
---

Dynamic polynomial hashing keeps the [polynomial hash](/polynomial-rolling-hash/) of every substring of a string available while the characters of the string change. It stores the terms $c(T[i])\, r^i \bmod p$ in a [Fenwick tree](/fenwick-tree/), or the hashes of segments in a [segment tree](/segment-tree/), so that changing one character and computing the hash of any substring each take $O(\log n)$ time. Two substrings are then compared by their hashes with the same one-sided error as static prefix hashes: for a prime $p$ and a base $r$ drawn uniformly from $\{1, \ldots, p-1\}$, two fixed different substrings of length $\ell$ get equal hashes with probability at most $(\ell - 1)/(p - 1)$. With a balanced search tree in place of the array, the same idea also supports inserting and deleting characters.

## In plain words

A string hash gives each piece of a string a number, so that equal pieces get equal numbers and different pieces almost never do. The usual way stores a running total for each start of the string. If one letter changes, every later running total changes, and fixing them takes as long as the string.

The dynamic way stores the parts of the totals in a tree. One letter is in only a few nodes of the tree, so a change fixes only those nodes. The number of any piece still comes from a few nodes. Both steps take a number of operations that grows only like the number of digits of the length of the string.

## When it applies

- **Equality questions on a changing string.** The task asks whether two substrings are equal, or asks for the longest common extension or a palindrome test, between changes of single characters.
- **Updates and queries mixed.** If all changes come before all questions, rebuild the static prefix hashes of [substring equality queries](/substring-equality-queries/) once instead.
- **A one-sided error is acceptable.** A "different" answer is always right; an "equal" answer can be wrong with a small probability. If the answer must be exact, verify each "equal" in full, or use the exact structures listed under Variations.
- **The operations do not depend on the base.** The bound holds when the operations are fixed before the base is drawn, or when each operation depends only on earlier yes or no answers. It does not hold if the hash values or the base are shown to whoever chooses the operations.

## The template

The string is $T[0 \ldots n-1]$, with 0-based indices, over an integer alphabet: each character has a code $c(a)$ in $\{0, \ldots, p-1\}$, and different characters have different codes. Let $g(x) = \sum_{t=0}^{|x|-1} c(x_t)\, r^t \bmod p$ for a string $x$; this is the polynomial hash with the powers in increasing order.

```pseudo id=main
DYNAMIC-POLYNOMIAL-HASH(T[0 .. n-1])
L1  p ← a prime larger than every code; r ← uniform from {1, ..., p − 1}     ▷ hole: modulus and base
L2  W[k] ← r^k mod p for k = 0, ..., n
L3  build a tree on A[i] = c(T[i]) · W[i] mod p for i = 0, ..., n − 1        ▷ hole: the tree
UPDATE(i, x)
L4  add (c(x) − c(T[i])) · W[i] mod p to A[i] in the tree; T[i] ← x
HASH(i, ℓ)
L5  return A[i] + ... + A[i + ℓ − 1] mod p, as a range sum of the tree       ▷ equals W[i] · g(T[i .. i + ℓ − 1])
EQUAL(i, j, ℓ)
L6  return HASH(i, ℓ) · W[j] = HASH(j, ℓ) · W[i] (mod p)                      ▷ hole: how to align
```

**The holes.**

- *Modulus and base.* A prime $p$, such as the [Mersenne prime](/mersenne-prime/) $2^{61} - 1$ with 128-wide products, and a base drawn at run time. Not arithmetic modulo $2^{64}$, which has [anti-hash tests](/anti-hash-tests/) for every odd base.
- *The tree.* A Fenwick tree gives point updates and prefix sums in $O(\log n)$ time with $n + 1$ words; a range sum is the difference of two prefix sums. A segment tree costs more memory but supports more operations (see Variations).
- *Alignment.* $\mathrm{HASH}(i, \ell)$ carries the factor $r^i$. Line L6 multiplies each side by the factor of the other, which needs no division. If normalized values are needed, for example as keys of a hash table, multiply by $r^{-i}$ instead, with the [modular inverse](/modular-inverse/) of $r$ and its powers precomputed.

**Why it is correct.** Line L3 and every call of line L4 keep the invariant $A[i] = c(T[i])\, r^i \bmod p$ for the current $T$. So $\mathrm{HASH}(i, \ell) = \sum_{t < \ell} c(T[i+t])\, r^{i+t} = r^i\, g(x)$ with $x = T[i \ldots i + \ell - 1]$, and with $y = T[j \ldots j + \ell - 1]$ line L6 compares $r^{i+j} g(x)$ with $r^{i+j} g(y)$. Since $p$ is prime and $r \ne 0$, $r^{i+j}$ is invertible modulo $p$, so line L6 answers yes exactly when $g(x) \equiv g(y)$. If $x = y$, the answer is yes. If $x \ne y$, then $g(x) - g(y)$ is a polynomial in $r$ of degree at most $\ell - 1$ with a coefficient $c(x_t) - c(y_t) \not\equiv 0$, so it has at most $\ell - 1$ roots modulo $p$, and the probability of a false yes is at most $(\ell - 1)/(p - 1)$. For $q$ queries the union bound gives at most $q(n - 1)/(p - 1)$. This also holds if each operation depends on the earlier answers: until the first false yes, all answers are the true answers, so the queries asked are those of one fixed sequence, and the first error is an error on a query of that sequence.

**Cost.** With a Fenwick tree: $O(n)$ time to build, $O(\log n)$ time for UPDATE, HASH and EQUAL, and $O(n)$ space. A segment tree has the same bounds.

**Example.** Let $T = $ abacaba, with the codes a = 1, b = 2, c = 3, the toy prime $p = 101$ and the base $r = 7$.

| $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $T[i]$ | a | b | a | c | a | b | a | |
| $W[i] = 7^i \bmod 101$ | 1 | 7 | 49 | 40 | 78 | 41 | 85 | |
| $A[i]$ | 1 | 14 | 49 | 19 | 78 | 82 | 85 | |
| prefix sum $S[i] = A[0] + \cdots + A[i-1]$ | 0 | 1 | 15 | 64 | 83 | 60 | 41 | 25 |

EQUAL(0, 4, 3) compares aba with aba: $\mathrm{HASH}(0, 3) = S[3] - S[0] = 64$ and $\mathrm{HASH}(4, 3) = S[7] - S[4] \equiv 43$, and $64 \cdot W[4] = 64 \cdot 78 \equiv 43 = 43 \cdot W[0]$, so the answer is yes. Now UPDATE(5, c) adds $(3 - 2) \cdot 41 = 41$ at position 5, so $A[5] = 22$, $S[6] = 82$ and $S[7] = 66$, and $T$ is abacaca. The same query now gives $\mathrm{HASH}(4, 3) = 66 - 83 \equiv 84$, and $43 \ne 84$: aba and aca differ. EQUAL(2, 4, 3) compares aca with aca: $\mathrm{HASH}(2, 3) = 60 - 15 = 45$, and $45 \cdot W[4] \equiv 76$ and $84 \cdot W[2] \equiv 76$, so the answer is yes. The Fenwick tree computes each $S[i]$ from at most $\lfloor \log_2 7 \rfloor + 1 = 3$ of its nodes.

## Classic examples

- [Substring equality queries](/substring-equality-queries/) under point updates: each query is one call of EQUAL.
- [Longest common extension](/longest-common-extension-query/) under point updates: binary search on $\ell$ with EQUAL gives $O(\log^2 n)$ time per query, and a walk down a segment tree gives $O(\log n)$.
- [Palindrome](/palindrome/) queries under point updates: keep a second tree for the reversed string $T'$ with $T'[k] = T[n - 1 - k]$; then $T[i \ldots j]$ is a palindrome if and only if it equals $T'[n - 1 - j \ldots n - 1 - i]$, one comparison of two hashes.
- Order queries: compare $T[i \ldots]$ and $T[j \ldots]$ in lexicographic order by their longest common extension and the next character, which lets a sort keep a set of substrings in order while the string changes.
- Text editing with a [rope](/rope/) or an [implicit treap](/implicit-treap/) whose nodes store hashes, so that substrings of the edited text can be compared at any time.

## Variations

- **Segment tree with Horner combination.** Each node stores the hash $h$ of its segment with the powers in decreasing order and the length of the segment; a parent combines its children $L$ and $R$ by $h(LR) = h(L)\, r^{|R|} + h(R) \bmod p$. A range query combines $O(\log n)$ nodes from left to right, and the result is already normalized, so no alignment is needed.
- **Range assignment.** Setting all of $T[i \ldots j]$ to one character $x$ gives a segment of length $k$ the hash $c(x)(1 + r + \cdots + r^{k-1})$. With these sums precomputed and [lazy propagation](/lazy-propagation/), the segment tree supports range assignment in $O(\log n)$ time.
- **Insertion and deletion.** Replace the array by a balanced search tree keyed by position, such as an [implicit treap](/implicit-treap/), and store in each node the hash and the size of its subtree, combined as in the segment tree. Insert, delete, split and concatenate then take $O(\log n)$ expected time.
- **Several moduli.** Run two independent hashes and answer yes only if both agree; the error bound is the product of the two bounds for two independent bases. A single prime near $2^{61}$ is usually cheaper.
- **Exact structures.** Mehlhorn, Sundar and Uhrig (1997) maintain a collection of strings under concatenation and splitting with exact equality tests, by giving names to blocks of the strings at several levels, with updates in polylogarithmic time. Gawrychowski, Karczmarz, Kociumaka, Łącki and Sankowski (2018) bring updates down to $O(\log n)$ time with high probability and answer equality, order and longest common prefix queries in $O(1)$ time. They also prove that, for a collection under concatenation and splitting with equality queries only, updates or queries need $\Omega(\log n)$ amortized time, so the hashed balanced trees above, with $O(\log n)$ per operation, cannot be beaten by more than a constant factor in that setting.

## Pitfalls

- **Adding the new code instead of the difference.** Line L4 adds $(c(x) - c(T[i]))\, r^i$; adding $c(x)\, r^i$ leaves the old character in the sum. Reduce the difference modulo $p$, since it can be negative.
- **Comparing unaligned hashes.** $\mathrm{HASH}(i, \ell)$ and $\mathrm{HASH}(j, \ell)$ of equal substrings differ by the factor $r^{i - j}$. Compare them as in line L6 or normalize them first.
- **The base 0.** With $r = 0$ only the first character counts. Draw $r$ from $\{1, \ldots, p - 1\}$, or, if $r$ is drawn from $\{0, \ldots, p - 1\}$, use the bound $\ell/p$, which counts the base 0 as a failure.
- **A fixed or visible base.** The bound is over the random base. A constant base, a fixed seed, or hash values printed to the user allow inputs that collide on purpose.
- **Overflow.** For $p = 2^{61} - 1$ the product of two residues needs 122 binary places. In languages with 64-wide integers, use a 128-wide product or the special reduction for Mersenne primes.
- **Codes not below $p$.** If two characters have codes that are equal modulo $p$, they are never told apart.

## Exercises

1. Prove the combination rule $h(LR) = h(L)\, r^{|R|} + h(R)$ for the hash with decreasing powers, and use it to write the query of a segment tree that returns the hash of $T[i \ldots j]$.
2. Show how to answer a longest common extension query in $O(\log n)$ time with one walk down a segment tree, instead of $O(\log^2 n)$ time with binary search.
3. Describe the lazy tag for range assignment: what it stores, and how it changes the hash of a node of length $k$.
4. For the palindrome test with a second tree on the reversed string, which update of the second tree goes with UPDATE$(i, x)$ on the first?
5. A program makes $q = 10^6$ queries on a string of length $n = 10^6$ with $p = 2^{61} - 1$ and a random base. Bound the probability of any false yes. *Answer:* $q(n - 1)/(p - 1) < 10^{12} / (2.3 \times 10^{18}) < 4.4 \times 10^{-7}$.

## References
