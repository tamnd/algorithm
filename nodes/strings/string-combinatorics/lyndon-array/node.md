---
tag: KRWVSH
kind: data-structure
slug: lyndon-array
name: Lyndon array
aliases:
- longest Lyndon factor array
area: strings/string-combinatorics
level: core
summary: For each position, the length of the longest Lyndon word starting there.
model: comparison-model
complexity:
  vars: {n: the length of the word}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [lyndon-word, lyndon-factorization, suffix-array, monotonic-stack]
see_also: [duval-algorithm, lyndon-schutzenberger-theorem, lyndon-based-runs-computation, runs-theorem, longest-lyndon-substring, range-minimum-query, maximal-repetition, computing-runs]
sources:
  - paper: doi:10.1016/s0304-3975(03)00099-9
    title: Christophe Hohlweg and Christophe Reutenauer, Lyndon words, permutations and trees, Theoretical Computer Science 307(1), 2003, 173-178
    locator: the link between the Lyndon factorizations of the suffixes, the order of the suffixes (the inverse of the sorting permutation) and binary trees
  - paper: doi:10.1137/15M1011032
    title: Hideo Bannai, Tomohiro I, Shunsuke Inenaga, Yuto Nakashima, Masayuki Takeda and Kazuya Tsuruta, The "Runs" Theorem, SIAM Journal on Computing 46(5), 2017, 1501-1514
    locator: the longest Lyndon word starting at each index, computed from the inverse suffix array by next smaller values, and its use to compute all runs in linear time
  - paper: doi:10.1016/0196-6774(83)90017-2
    title: Jean-Pierre Duval, Factorizing words over an ordered alphabet, Journal of Algorithms 4(4), 1983, 363-381
    locator: the longest Lyndon prefix as the first factor of the Lyndon factorization, computed in linear time
---

The Lyndon array of a word $s$ of length $n$ stores, for each index $i$, the length $\lambda[i]$ of the longest [Lyndon word](/lyndon-word/) that starts at $i$. It is the [Lyndon factorization](/lyndon-factorization/) of every suffix at once: $\lambda[i]$ is the length of the first factor of $s[i..n-1]$, and following $i, i + \lambda[i], \ldots$ lists all the factors. It is built in $O(n)$ time from the inverse [suffix array](/suffix-array/) with one [monotonic stack](/monotonic-stack/) pass, because $i + \lambda[i]$ is the first index after $i$ whose suffix is smaller. The array is the main tool of the linear-time [computation of runs](/lyndon-based-runs-computation/).

## In plain words

At each place in a word, start reading and stop at the last point where what you have read is still a Lyndon word, a word that comes strictly first in dictionary order among all its rotations. Write down that length. The list of these lengths is the Lyndon array. There is a short way to fill it: sort all the endings of the word. The longest Lyndon word starting at a place stops exactly where the first later ending begins that comes before the current ending in dictionary order. One pass from right to left with a stack finds these places for all positions.

## The abstract type

A static array over a word $s$, built once:

- `build(s)`: compute $\lambda[0..n-1]$.
- `query(i)`: return $\lambda[i]$, the length of the longest Lyndon factor $s[i..i+\lambda[i]-1]$.
- `factors(i)`: return the start indices of the Lyndon factorization of the suffix $s[i..n-1]$.

## Representation

The word is $s = s[0..n-1]$ over a totally ordered [alphabet](/alphabet/); the construction compares suffixes, so the cost depends on how the suffix array is built, and the stack pass compares integers. Indices are 0-based. Words are compared in [lexicographic order](/lexicographic-order/), where a proper prefix is smaller; no sentinel is appended. The structure is an array $\lambda[0..n-1]$ of integers.

**Invariant.** For each $i$, $1 \le \lambda[i] \le n - i$, the factor $s[i..i+\lambda[i]-1]$ is a Lyndon word, and no longer factor starting at $i$ is a Lyndon word.

**The key fact.** Let $rank$ be the inverse suffix array, so $rank[i] < rank[j]$ exactly when $s[i..] < s[j..]$. Let $\mathrm{nss}(i)$ be the least $j > i$ with $rank[j] < rank[i]$, or $n$ if there is none, the next smaller suffix. Then
$$ \lambda[i] = \mathrm{nss}(i) - i. $$
*Proof.* By the [Chen-Fox-Lyndon theorem](/lyndon-schutzenberger-theorem/), the longest Lyndon prefix of $s[i..n-1]$ is the first factor of its Lyndon factorization. The factorization of a word starts its factors at the left-to-right minima of its suffixes (characterization 3 on the [Lyndon factorization](/lyndon-factorization/) page). The suffixes of $s[i..n-1]$ are the suffixes of $s$ that start at $i$ or later, in the same order. The first left-to-right minimum after $i$ is the first $j > i$ whose suffix is smaller than the running minimum, which until then is $s[i..]$; that is $\mathrm{nss}(i)$. If there is no such $j$, the suffix has a single factor, of length $n - i$. $\square$

Two more facts follow. **Nesting:** the intervals $[i, i + \lambda[i])$ never cross: if $i < j < i + \lambda[i]$, then $j + \lambda[j] \le i + \lambda[i]$, because $\mathrm{nss}(i)$ has a smaller rank than $i$, hence than every index between, so $\mathrm{nss}(j) \le \mathrm{nss}(i)$. **Length one:** for $i < n - 1$, $\lambda[i] = 1$ if and only if $s[i+1..] < s[i..]$.

## Operations

```pseudo id=main
LYNDON-ARRAY(s)                            ▷ s[0 .. n − 1]
L1  rank ← the inverse suffix array of s
L2  λ[0 .. n − 1] ← 0, S ← empty stack
L3  for i ← n − 1 downto 0 do
L4      while S is not empty and rank[top(S)] > rank[i] do
L5          pop S
L6      if S is empty then λ[i] ← n − i
L7      else λ[i] ← top(S) − i
L8      push i on S
L9  return λ

QUERY(λ, i)
L10 return λ[i]

FACTORS(λ, i)                              ▷ the Lyndon factorization of s[i .. n − 1]
L11 F ← empty list
L12 while i < n do
L13     append i to F, i ← i + λ[i]
L14 return F
```

Line L1 can use any suffix array construction. The loop of lines L3 to L8 is the next-smaller-value pass of a [monotonic stack](/monotonic-stack/), run from right to left: at the start of the iteration for $i$, the stack holds the indices $j > i$ whose rank is smaller than the rank of every index strictly between $i$ and $j$, with the smallest index on top. Lines L4 and L5 pop those with a larger rank than $i$; the top that remains is $\mathrm{nss}(i)$. FACTORS follows the chain of first factors: the rest of the factorization of $s[i..]$ after its first factor is the factorization of $s[i + \lambda[i]..]$.

## Example

Let $s = $ `abaabaabb`, $n = 9$, with $a < b$. The suffix array is $SA = [2, 5, 0, 3, 6, 8, 1, 4, 7]$, so $rank = [2, 6, 0, 3, 7, 1, 4, 8, 5]$. The pass from right to left:

| $i$ | $rank[i]$ | popped | top after pops | $\lambda[i]$ | Lyndon factor | stack after push (top last) |
|---|---|---|---|---|---|---|
| 8 | 5 | none | empty | 1 | `b` | 8 |
| 7 | 8 | none | 8 | 1 | `b` | 8, 7 |
| 6 | 4 | 7, 8 | empty | 3 | `abb` | 6 |
| 5 | 1 | 6 | empty | 4 | `aabb` | 5 |
| 4 | 7 | none | 5 | 1 | `b` | 5, 4 |
| 3 | 3 | 4 | 5 | 2 | `ab` | 5, 3 |
| 2 | 0 | 3, 5 | empty | 7 | `aabaabb` | 2 |
| 1 | 6 | none | 2 | 1 | `b` | 2, 1 |
| 0 | 2 | 1 | 2 | 2 | `ab` | 2, 0 |

So $\lambda = [2, 1, 7, 2, 1, 4, 3, 1, 1]$. FACTORS$(\lambda, 0)$ gives $[0, 2]$, the factorization `ab` $\cdot$ `aabaabb` of $s$, and FACTORS$(\lambda, 3)$ gives $[3, 5]$, the factorization `ab` $\cdot$ `aabb` of `abaabb`. The intervals nest: $[5, 9)$ and $[3, 5)$ lie inside $[2, 9)$, and $[6, 9)$ lies inside $[5, 9)$.

## Correctness

The key fact gives $\lambda[i] = \mathrm{nss}(i) - i$. The stack pass computes $\mathrm{nss}$: it keeps the indices $j > i$ that are smaller in rank than everything between $i$ and $j$; their ranks decrease from the top down, so the pops remove exactly those above $\mathrm{nss}(i)$, and pushing $i$ restores the invariant for $i - 1$. FACTORS is correct because the first factor of $s[i..]$ has length $\lambda[i]$ and the remaining factors form the factorization of the rest, by the uniqueness of the factorization. The full proof is in the proof file.

## Complexity

- **Build.** Each index is pushed once and popped at most once, so lines L2 to L9 take $\Theta(n)$ time. Line L1 takes $O(n)$ time on an integer alphabet with a linear suffix array construction, or $O(n \log n)$ comparisons of letters with a comparison-based one. The implementation on this page uses prefix doubling with a sort, $O(n \log^2 n)$ time.
- **Query.** $O(1)$ time.
- **Factors.** $O(1)$ time per factor reported.
- **Space.** $\Theta(n)$ words for $rank$, $\lambda$ and the stack. After the build, only $\lambda$ is kept.

## Variants

- **Both orders.** The array for the reversed alphabet order is built the same way. Each run of $s$ has a Lyndon root that is a longest Lyndon word starting at its index for one of the two orders, which gives the linear-time [Lyndon-based runs computation](/lyndon-based-runs-computation/) and the proof of the [runs theorem](/runs-theorem/).
- **Without a suffix array.** Running the inner loop of [Duval's algorithm](/duval-algorithm/) from each index gives each $\lambda[i]$ in $O(n - i)$ time and $O(1)$ extra space, $O(n^2)$ in total. Linear-time constructions that do not build the full suffix array also exist.
- **Lyndon forest.** By the nesting property, the intervals $[i, i + \lambda[i])$ form a forest under inclusion.
- **End index form.** Some texts store $i + \lambda[i]$, the next smaller suffix index, instead of the length; the two differ by $i$.

## When to use it

Use the Lyndon array when you need the Lyndon factorization of many suffixes, or the longest Lyndon word at every index: for runs, for squares and repetitions, or for a [longest Lyndon substring](/longest-lyndon-substring/) of every suffix. If you need only the factorization of the whole word, [Duval's algorithm](/duval-algorithm/) is simpler and needs $O(1)$ extra space.

## Pitfalls

- **Comparing letters instead of suffixes.** The next smaller letter is not the next smaller suffix. For `aba`, no letter after index 0 is smaller than `a`, but the suffix `a` is smaller than `aba`, and $\lambda[0] = 2$, not 3.
- **The order of a prefix and its extension.** The ranks must follow the rule that a proper prefix is smaller. A suffix array built with an end marker that is larger than every letter gives the wrong order: for `aa` it puts `aa` before `a`, and the pass returns $\lambda[0] = 2$ instead of 1. A sentinel smaller than every letter is safe.
- **Off by one.** $\lambda[i] = \mathrm{nss}(i) - i$, with $\mathrm{nss}(i) = n$ when no later suffix is smaller; there is no $+1$.

## Implementations

## History

Duval's 1983 algorithm computes the longest Lyndon prefix of a word as the first factor of its Lyndon factorization. Hohlweg and Reutenauer (2003) related the Lyndon factorizations of the suffixes of a word to the order of its suffixes and to binary trees. The Lyndon array became a central tool after Bannai, I, Inenaga, Nakashima, Takeda and Tsuruta proved the runs theorem in 2015, with a linear-time computation of all runs built on the longest Lyndon words at each index, for both orders.

## References
