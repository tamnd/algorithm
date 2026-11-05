---
tag: HKXC4R
kind: algorithm
slug: karp-rabin-multiple-patterns
name: Karp-Rabin multiple-pattern matching
aliases:
- Karp-Rabin set matching
- Rabin-Karp for many patterns
area: strings/multiple-pattern-matching
level: advanced
summary: Rabin-Karp fingerprinting over a set of equal-length patterns, looking up each window's hash in a table.
solves: [multiple-string-matching]
model: word-ram
complexity:
  vars: {n: the length of the text, k: the number of patterns, m: the total length of the patterns, d: the number of distinct pattern lengths, L: the largest pattern length, z: the number of occurrences, p: the prime modulus}
  time: {worst: O(k + m + n·m + z), expected: O(k + m + d·n + z·(L + 1) + n·m·L/p)}
  space: {extra: O(m)}
properties: {deterministic: false, recursive: false, online: true}
history:
  year: 1987
  people: [Richard M. Karp, Michael O. Rabin]
  note: The fingerprint method is from Karp and Rabin (IBM Journal of Research and Development, 1987, after a 1981 technical report). The set version keeps the pattern fingerprints in a hash table and is a standard extension, given as an exercise in textbooks.
prereqs: [rabin-karp, polynomial-rolling-hash, hash-table]
see_also: [multiple-string-matching, aho-corasick, wu-manber, polynomial-hash-collision-bound, spurious-hit, perfect-hashing, dictionary-matching, anti-hash-tests]
sources:
  - paper: doi:10.1147/rd.312.0249
    title: Richard M. Karp and Michael O. Rabin, Efficient randomized pattern-matching algorithms, IBM Journal of Research and Development 31(2) (1987), 249-260
    locator: the fingerprint functions, their update as a window slides, and the error analysis
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 32.2, The Rabin-Karp algorithm (the exercise on searching for any one of a set of k patterns, first of one length and then of different lengths)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Section 4.4, Karp-Rabin fingerprint methods for exact match
  - paper: doi:10.1145/872757.872770
    title: Saul Schleimer, Daniel S. Wilkerson and Alex Aiken, Winnowing, local algorithms for document fingerprinting, Proceedings of the 2003 ACM SIGMOD International Conference on Management of Data, 76-85
    locator: the hashes of all k-grams of a document, computed with a rolling hash, as the basis of document matching
---

Karp-Rabin multiple-pattern matching finds all occurrences of a set of patterns in a text with one [rolling hash](/polynomial-rolling-hash/) pass per pattern length. It puts the hashes of the patterns of one length into a [hash table](/hash-table/), slides a window of that length over the text, looks up the hash of each window, and compares characters only with the patterns found in the table. With a prime modulus $p$ and a base drawn at random, a wrong candidate appears with probability at most $(\ell-1)/p$ per window and pattern of length $\ell$, so the expected time is linear in the input and the output when all patterns have one length. It is the shortest correct solution of [multiple string matching](/multiple-string-matching/) for patterns of equal length, and it extends without change to two dimensions.

## In plain words

[Rabin-Karp](/rabin-karp/) turns the pattern into a number and every piece of the text of the same length into a number, and compares numbers. With many patterns of the same length, turn each pattern into a number and keep all the numbers in a table that answers "is this number in the table?" in one step.

Then slide over the text once. For each piece, compute its number in a few steps from the number of the piece before, and look it up in the table. If the number is there, compare the letters of the piece with the pattern that has this number, because two different strings can share a number by bad luck.

If the patterns have different lengths, do one such pass for each length.

## The problem

Given a text $T = T[0 \ldots n-1]$ and patterns $P_0, \ldots, P_{k-1}$ over an integer alphabet, output every pair $(s, j)$ with $T[s \ldots s + |P_j| - 1] = P_j$. Indices are 0-based. Occurrences may overlap, also occurrences of different patterns. A pattern listed twice is reported once for each of its indices. The empty pattern occurs at every $s$ from $0$ to $n$. Each character $a$ has a code $c(a) \in \{1, \ldots, p - 1\}$, and distinct characters have distinct codes. Write $m = \sum_j |P_j|$ for the total length of the patterns, $d$ for the number of distinct lengths, $L$ for the largest length and $z$ for the number of pairs in the output.

## The algorithm

Fix a prime $p$ larger than every code. For a string $x$ of length $\ell$ and a base $r$, $h(x) = \sum_{i=0}^{\ell-1} c(x_i)\, r^{\ell-1-i} \bmod p$, computed by Horner's rule. Let $Q$ range over the distinct strings among the patterns, and let $J(Q) = \{j : P_j = Q\}$.

```pseudo id=main
KR-SET(T[0 .. n-1], P_0, ..., P_{k-1})
L1  r ← a uniform random element of {0, 1, ..., p − 1}
L2  for each distinct length ℓ of the patterns do
L3      H ← an empty hash table from hash values to lists of strings
L4      for each distinct pattern Q with |Q| = ℓ do append Q to H[h(Q)]
L5      if ℓ = 0 then output (s, j) for every s in 0 .. n and j in J(ε); next ℓ
L6      if ℓ > n then next ℓ
L7      R ← r^(ℓ−1) mod p; ht ← h(T[0 .. ℓ−1])
L8      for s ← 0 to n − ℓ do
L9          for each Q in the list H[ht] do
L10             if T[s .. s + ℓ − 1] = Q then output (s, j) for every j in J(Q)
L11         if s < n − ℓ then ht ← ((ht − c(T[s]) · R) · r + c(T[s + ℓ])) mod p
```

Line L4 groups the patterns by hash; a pattern listed twice is stored once, with all its indices. Line L7 computes the hash of the first window, and line L11 rolls it: it removes the term of the leaving character, shifts the rest by one power of $r$, and adds the entering character, as in [Rabin-Karp](/rabin-karp/). Line L10 is the verification; it rejects a [spurious hit](/spurious-hit/), a pattern whose hash equals the window hash although the strings differ. The output comes length by length; sort it if the order by $s$ matters.

**The table.** Python's dictionary is enough in practice. For a guarantee, build a static [perfect hash table](/perfect-hashing/) on the at most $k$ hash values of each length: $O(k)$ expected build time and $O(1)$ worst-case lookups.

## Example

Take $T = $ abababbb ($n = 8$), the patterns $P_0 = $ aba, $P_1 = $ abb, $P_2 = $ aba and $P_3 = $ baa, so $\ell = 3$ for all of them. The codes are $c(\mathrm{a}) = 1$, $c(\mathrm{b}) = 2$; the prime is the tiny $p = 13$ and the draw is $r = 5$, so $R = 5^2 \bmod 13 = 12$. Line L4 gives $h(\mathrm{aba}) = 10$ with $J = \{0, 2\}$, $h(\mathrm{abb}) = 11$ with $J = \{1\}$ and $h(\mathrm{baa}) = 4$ with $J = \{3\}$.

| $s$ | window | $ht$ | $H[ht]$ | L10 | output |
|---|---|---|---|---|---|
| 0 | aba | 10 | aba | equal | (0, 0), (0, 2) |
| 1 | bab | 5 | empty | | |
| 2 | aba | 10 | aba | equal | (2, 0), (2, 2) |
| 3 | bab | 5 | empty | | |
| 4 | abb | 11 | abb | equal | (4, 1) |
| 5 | bbb | 10 | aba | differ | |

The output is (0, 0), (0, 2), (2, 0), (2, 2) and (4, 1): the two occurrences of aba overlap, and the duplicate pattern $P_2$ is reported with $P_0$. Line L10 runs four times and rejects once, at $s = 5$: $h(\mathrm{bbb}) - h(\mathrm{aba}) = r^2 + 1$, which is zero modulo 13 only for $r = 5$ and $r = 8$. The pattern baa never occurs and its hash 4 never appears. With $p = 2^{61} - 1$ instead of 13, a spurious hit of one window with one pattern of length 3 has probability below $10^{-18}$.

## Correctness

The output is exactly the set of occurrences, for every value of $r$; only the time depends on $r$. Within the pass for a length $\ell \ge 1$, the invariant is $ht = h(T[s \ldots s + \ell - 1])$ at line L9, by line L7 and the rolling identity of line L11. If $P_j$ occurs at $s$, then $Q = P_j$ equals the window, so $h(Q) = ht$, $Q$ is in the list $H[ht]$, line L10 finds the strings equal, and $(s, j)$ is output. Each output pair passed the test of line L10, so it is an occurrence. Each pair is output once, because $Q$ appears once in the table and each $s$ is visited once in the pass for $|Q|$. The full proof is in the proof file below.

## Complexity

**Preprocessing.** Hashing all patterns costs $O(m)$, and building the tables costs $O(k)$ expected. Line L7 costs $O(\ell)$ per length, at most $m$ in all.

**Scan.** Each length $\ell \le n$ takes $O(n)$ time for lines L8, L9 and L11, so the scan is $O(d \cdot n)$. The distinct lengths $\ell_1 < \ell_2 < \cdots$ satisfy $\ell_i \ge i - 1$ and sum to at most $m$, so $d \le \sqrt{2m} + 1$.

**Verification.** A test at line L10 costs $O(\ell)$. A successful test outputs at least one pair, so the successful tests cost $O(z \cdot L)$ in all. A failed test needs a distinct pattern $Q \ne$ window with $h(Q) = h(\text{window})$; for two fixed distinct strings of length $\ell$ this has probability at most $(\ell - 1)/p$ over $r$ by the [collision bound](/polynomial-hash-collision-bound/). With $k_\ell$ distinct patterns of length $\ell$, the expected cost of failed tests is at most

$$\sum_{\ell} (n - \ell + 1)\, k_\ell\, \frac{\ell - 1}{p}\, \ell \;\le\; \frac{n\, m\, L}{p}.$$

Writing the output costs $O(z)$. So the expected time is $O(k + m + d \cdot n + z (L + 1) + n m L / p)$. With all $k$ patterns of one length $\ell \ge 1$ and $p \ge n m \ell$, it is $O(m + n + z \ell)$.

**Worst case.** For a bad base, such as $r = 1$ where anagrams collide, every window can be tested against every distinct pattern of its length, so the time is $O(k + m + n \cdot m + z)$. Such bases are rare for a prime $p$ much larger than $nmL$.

**Space.** The tables hold one entry per distinct pattern, and the algorithm keeps $O(1)$ words for the window. The implementation stores the codes of the patterns, $O(m)$ words.

## Properties

- **Las Vegas.** With line L10 the output is always exact; only the time is random.
- **Monte Carlo variant.** Without line L10, every hash match is reported. The time is $O(k + m + d \cdot n + z')$ for $z'$ reported pairs, and the probability of any false pair is at most $n m / p$ by the union bound.
- **Online per length.** Each pass reads the text left to right and decides position $s$ when $T[s + \ell - 1]$ arrives. Running the $d$ passes side by side with $d$ rolling hashes gives a one-pass online algorithm with $O(d)$ work per character.
- **Arithmetic, not automata.** The memory is $O(k)$ words for the tables, with no trie; adding or removing a pattern is one table update. This makes the method simple to keep up to date when the set changes.

## Variants and improvements

- **One length, many patterns.** The original setting: with all $|P_j| = \ell$ the scan is one pass, $O(n + m + z\ell)$ expected. It is the standard method to test which of many fixed-length strings, such as $q$-grams, occur in a text.
- **Different lengths by truncation.** Instead of $d$ passes, hash only the first $\ell_{\min}$ characters of each pattern, look up windows of length $\ell_{\min}$, and verify the full pattern on a hit. This is one pass, but each hit may verify many patterns that share a prefix hash; [Wu-Manber](/wu-manber/) uses this idea with a block hash and a shift table.
- **Two dimensions.** For a set of $m \times m$ arrays, hash each column of a window, roll the hash of the row of column hashes, and look it up in the table of array hashes. This is the two-dimensional method of Karp and Rabin with a set in place of one pattern.
- **Fingerprints for documents.** Plagiarism and near-duplicate detection hash every $q$-gram of each document with a rolling hash and look the hashes up in a table of all documents. Winnowing keeps only a sample of the hashes to save space.
- **Deterministic alternatives.** [Aho-Corasick](/aho-corasick/) solves the same problem in $O(n + m + z)$ worst-case time with an automaton; [dictionary matching](/dictionary-matching/) studies the general setting.

## When to use it

Use it for many patterns of one length or of a few lengths, when the set changes often, when memory for a trie is a problem, or in two dimensions. It is also the quickest correct method to write. For patterns of many different lengths, the $d$ passes cost $O(dn)$, and [Aho-Corasick](/aho-corasick/) is better. When patterns are long and the alphabet is large, [Wu-Manber](/wu-manber/) skips parts of the text and reads fewer characters.

## Pitfalls

- **Matching on the hash alone.** Without line L10, a collision is reported as an occurrence. With a fixed base or modulus $2^{64}$, an adversary can force such collisions; see [anti-hash tests](/anti-hash-tests/).
- **A table keyed by hash only.** Two different patterns of one length can have the same hash; the table must keep a list per hash, or one of them is lost. In the example with $p = 13$, the strings aba and bbb share the hash 10.
- **Duplicated patterns.** Storing a pattern twice makes line L10 compare it twice. Group the indices by distinct pattern, as line L4 does, or the verification cost grows with the number of copies.
- **Many lengths.** One pass per length is $O(dn)$; with patterns of all lengths from 1 to $L$, that is $\Theta(nL)$ even with no occurrence.
- **Codes and lengths.** Hashes of strings of different lengths are never compared, so a zero code would not cause errors here; it does when hashes of different lengths share a table, as in the truncation variant.
- **The empty pattern.** It has no window to roll; treat it apart, as line L5 does.

## Implementations

## History

Karp and Rabin introduced the randomized fingerprint method for pattern matching in a technical report of 1981, published in 1987. Their paper treats one pattern, two-dimensional patterns and the error analysis. Keeping the fingerprints of many patterns in a table is a direct extension; CLRS gives it as an exercise in the section on Rabin-Karp. The same table of rolling hashes is the basis of document fingerprinting tools such as winnowing (Schleimer, Wilkerson and Aiken, 2003), and the [Wu-Manber](/wu-manber/) algorithm (1994) combines a hash table of pattern blocks with a shift table.

## References
