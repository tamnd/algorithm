---
tag: 2134ZX
kind: algorithm
slug: duval-algorithm
name: Duval's algorithm
aliases:
- Duval Lyndon factorization algorithm
area: strings/string-combinatorics
level: core
summary: Computes the Lyndon factorization in linear time and constant extra space.
solves: [lyndon-factorization, longest-lyndon-substring]
model: comparison-model
complexity:
  vars: {n: the length of the word}
  time: {worst: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [lyndon-factorization, lyndon-word, lyndon-schutzenberger-theorem, lexicographic-order]
see_also: [booth-algorithm, fkm-algorithm, lyndon-array, minimal-rotation, longest-lyndon-substring, two-way-string-matching, critical-factorization, bijective-burrows-wheeler-transform]
sources:
  - paper: doi:10.1016/0196-6774(83)90017-2
    title: Jean-Pierre Duval, Factorizing words over an ordered alphabet, Journal of Algorithms 4(4), 1983, 363-381
    locator: the factorization algorithm, its proof through the prefixes of powers of Lyndon words, and the bound of 2n comparisons
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.1, Generating all n-tuples (prime strings, preprimes, and the exercises on factoring a string into primes)
  - paper: doi:10.2307/1970044
    title: Kuo-Tsai Chen, Ralph H. Fox and Roger C. Lyndon, Free differential calculus IV. The quotient groups of the lower central series, Annals of Mathematics 68(1), 1958, 81-95
    locator: the existence and uniqueness of the factorization that the algorithm computes
  - url: "https://cp-algorithms.com/string/lyndon_factorization.html"
    locator: Lyndon factorization, Duval algorithm (the three-pointer loop, its linear bound and the least cyclic shift)
---

Duval's algorithm computes the [Lyndon factorization](/lyndon-factorization/) of a word $s$ of length $n$: the unique way to write $s = \ell_1 \ell_2 \cdots \ell_k$ with [Lyndon words](/lyndon-word/) $\ell_1 \ge \ell_2 \ge \cdots \ge \ell_k$. It reads the word from left to right with three indices, keeps the invariant that the part read since the last output is a prefix of a power of a Lyndon word, and outputs the copies of that Lyndon word when a smaller letter arrives. It uses $\Theta(n)$ time, at most $2n - 1$ letter comparisons and $O(1)$ extra space in the [comparison model](/comparison-model/).

## In plain words

You want to cut a word into pieces that are Lyndon words and never grow from left to right. Read the word from the left and keep a block that repeats one Lyndon word, perhaps ending in a part of it. Each new letter is compared with the letter that the repetition predicts. If they are equal, the repetition goes on. If the new letter is larger, the whole block glues into one longer Lyndon word. If it is smaller, the repetition cannot go on: each full copy in the block is a final piece. Output them, and start again just after the last full copy, so that the unfinished part is read again.

## The problem

The input is a word $s = s[0..n-1]$ over a totally ordered [alphabet](/alphabet/); only the three-way comparison of two letters is used. Indices are 0-based. The output is the list of start indices $0 = b_1 < b_2 < \cdots < b_k < n$ of the factors of the Lyndon factorization, so $\ell_r = s[b_r..b_{r+1}-1]$ with $b_{k+1} = n$. The factorization exists and is unique by the [Chen-Fox-Lyndon theorem](/lyndon-schutzenberger-theorem/). For $n = 0$ the list is empty.

## The algorithm

The index $i$ is the start of the part not yet output, $j$ is the next letter to read, and $k$ is the letter that $s[j]$ is compared with. The part $s[i..j-1]$ is always $u^m u'$, where $u$ is a Lyndon word of length $p = j - k$, $m \ge 1$, and $u'$ is a proper prefix of $u$.

```pseudo id=main
DUVAL(s)                                   ▷ s[0 .. n − 1]
L1  i ← 0, F ← empty list
L2  while i < n do
L3      j ← i + 1, k ← i
L4      while j < n and s[k] ≤ s[j] do
L5          if s[k] < s[j] then k ← i else k ← k + 1
L6          j ← j + 1
L7      while i ≤ k do
L8          append i to F                  ▷ the factor s[i .. i + j − k − 1]
L9          i ← i + j − k
L10 return F
```

Line L3 starts a new block with the single letter $s[i]$, so $u = s[i]$, $m = 1$ and $u'$ is empty. Line L4 compares the new letter $s[j]$ with $s[k] = s[j - p]$, the letter that the period $p$ predicts. If they are equal, line L5 moves $k$ forward and the period stays $p$. If $s[j]$ is larger, line L5 sets $k$ to $i$, so the period becomes $j + 1 - i$: the whole block $s[i..j]$ is now one Lyndon word. When $s[j] < s[k]$ or the word ends, lines L7 to L9 output the $m$ copies of $u$, each of length $p = j - k$, and leave $i$ at the start of $u'$.

## Example

Let $s = $ `ababaab` with $a < b$ and $n = 7$. The column $p$ is $j - k$ after the step.

| step | $i$ | $j$ | $k$ | $s[k]$ vs $s[j]$ | action | $p$ |
|---|---|---|---|---|---|---|
| 1 | 0 | 1 | 0 | `a` $<$ `b` | $k \leftarrow 0$, block `ab` is Lyndon | 2 |
| 2 | 0 | 2 | 0 | `a` $=$ `a` | $k \leftarrow 1$ | 2 |
| 3 | 0 | 3 | 1 | `b` $=$ `b` | $k \leftarrow 2$ | 2 |
| 4 | 0 | 4 | 2 | `a` $=$ `a` | $k \leftarrow 3$, block `ababa` $=$ (`ab`)$^2$`a` | 2 |
| 5 | 0 | 5 | 3 | `b` $>$ `a` | stop; output 0 and 2 (`ab`, `ab`), $i \leftarrow 4$ | 2 |
| 6 | 4 | 5 | 4 | `a` $=$ `a` | $k \leftarrow 5$ | 1 |
| 7 | 4 | 6 | 5 | `a` $<$ `b` | $k \leftarrow 4$, block `aab` is Lyndon | 3 |
| 8 | 4 | 7 | 4 | end of word | stop; output 4 (`aab`), $i \leftarrow 7$ | 3 |

The output is $F = [0, 2, 4]$, that is, `ab` $\cdot$ `ab` $\cdot$ `aab`, and `ab` $=$ `ab` $>$ `aab`. The letter `a` at index 4 is read twice: once as the unfinished part $u'$ of the first block, and once as the start of the second block. Steps 1 to 8 use 7 letter comparisons.

## Correctness

The proof rests on one lemma: if $u$ is a Lyndon word, $u'$ a proper prefix of $u$, $m \ge 1$, and $c$ a letter larger than $u[|u'|]$, then $u^m u' c$ is a Lyndon word. With it, the inner loop keeps the invariant $s[i..j-1] = u^m u'$ with $u = s[i..i+p-1]$ Lyndon and $p = j - k$. When the loop stops with $s[j] < s[k]$ or $j = n$, the first factor of the Lyndon factorization of $u' s[j..n-1]$ is at most $u$: it is a prefix of $u'$ or it starts with $u'$ followed by a letter smaller than $u[|u'|]$. So $u, \ldots, u$ followed by the factorization of $u' s[j..n-1]$ is nonincreasing, and by uniqueness it is the Lyndon factorization of $s[i..n-1]$. The full proof is in the proof file.

## Complexity

- **Comparisons.** Count one three-way comparison of $s[k]$ with $s[j]$ per test of line L4 with $j < n$. In one round of the outer loop, $j$ goes from $i + 1$ to its final value $j^*$, so the round uses at most $j^* - i$ comparisons: one for each step of the inner loop and one more for the failed test. The block $s[i..j^*-1] = u^m u'$ has $j^* - i = mp + |u'| \le mp + p - 1 \le 2mp - 1$, and the round moves $i$ forward by $mp$. So a round that moves $i$ by $d$ uses at most $2d - 1$ comparisons, and the total is at most $2n - 1$ for $n \ge 1$. Over all binary words of length 14 the largest count is 21.
- **Time.** Each comparison and each output costs $O(1)$, so the time is $\Theta(n)$. Each index $j \ge 1$ is read at line L4 at least once, because each round starts at an index $i \le j^*$ of the previous round, so there are at least $n - 1$ comparisons and the best case is also $\Theta(n)$.
- **Space.** Three indices, $O(1)$ extra cells, plus the output list of at most $n$ entries. If the factors are streamed instead of stored, the extra space is $O(1)$.

## Properties

- **Ordered alphabet only.** Only comparisons of letters are used, so the algorithm works for any total order, including a reversed order.
- **No table.** Unlike [Booth's algorithm](/booth-algorithm/), there is no failure table; the periodic structure $u^m u'$ is held in the three indices.
- **Delayed output.** A factor is output only when a smaller letter or the end arrives, so the output is not online: the factorization of a prefix of $s$ is not a prefix of the factorization of $s$. For example, `ab` is one factor, but `aba` factors as `ab` $\cdot$ `a`, and `abac` is one factor.

## Variants and improvements

- **Least suffix.** The last factor $\ell_k$ is the lexicographically least suffix of $s$, so Duval's algorithm finds the least suffix in linear time and constant space.
- **Least rotation.** Run the algorithm on $ss$; the start of the last factor that starts below $n$ is a least rotation of $s$. This takes $O(n)$ time and $O(1)$ space, but it may not return the least such index; see [minimal rotation](/minimal-rotation/) and [Booth's algorithm](/booth-algorithm/).
- **Maximal suffix and critical factorization.** A variant of the same loop computes the maximal suffix of a word for an order and for its reverse, which is the step that finds a [critical factorization](/critical-factorization/) in [two-way string matching](/two-way-string-matching/).
- **Longest Lyndon factor.** Each Lyndon factor of $s$ lies inside one factor of the factorization, so the longest factor output is a [longest Lyndon substring](/longest-lyndon-substring/).
- **Necklace generation.** The test "is this word a prefix of a power of a Lyndon word" in line L4 is the same structure that the [FKM algorithm](/fkm-algorithm/) uses to generate necklaces and Lyndon words in lexicographic order.

## When to use it

Use Duval's algorithm whenever you need the Lyndon factorization, the least suffix, or a least rotation with constant extra space. It is short, has no table and needs only comparisons. If you need the Lyndon factorization of every suffix, or the longest Lyndon word starting at each index, compute the [Lyndon array](/lyndon-array/) instead.

## Pitfalls

- **Outputting the whole block.** The block $s[i..j-1]$ may be $u^m u'$ with $m > 1$ or $u'$ nonempty; it is not one Lyndon word. Lines L7 to L9 output only the $m$ full copies of $u$.
- **Restarting at $j$.** Setting $i \leftarrow j$ after the output skips $u'$. On `ababaab` this loses the `a` at index 4 and outputs `ab`, `ab`, `ab`, of total length 6.
- **Strict test in line L4.** With $s[k] < s[j]$ instead of $s[k] \le s[j]$, the loop stops at the first repeat, and the factorization is wrong: on `abac` it gives `ab` $\cdot$ `ac` instead of the single factor `abac`.
- **Wrong factor length.** The length of each output factor is $p = j - k$, not $j - i$; the two differ as soon as the block has more than one copy of $u$.

## Implementations

## History

Chen, Fox and Lyndon proved in 1958 that the factorization exists and is unique. Jean-Pierre Duval published the linear-time algorithm in 1983 in the Journal of Algorithms, together with the bound of $2n$ comparisons, and pointed out its use for the least rotation of a word. The algorithm is related to the generation of Lyndon words in lexicographic order by Fredricksen, Kessler and Maiorana, and its maximal-suffix form is a step of the two-way string matching algorithm of Crochemore and Perrin (1991).

## References
