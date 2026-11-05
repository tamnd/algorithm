---
tag: CDF7D0
kind: technique
slug: prefix-doubling
name: Prefix doubling
aliases:
- doubling
area: strings/suffix-structures
level: core
summary: Sort substrings of length 2^k from those of length 2^(k-1), doubling the length each round.
prereqs: [suffix, radix-sort]
see_also: [manber-myers-algorithm, karp-miller-rosenberg-algorithm, larsson-sadakane-algorithm, suffix-array, substring-equality-queries, lca-binary-lifting, range-minimum-query, list-ranking]
sources:
  - paper: doi:10.1145/800152.804905
    title: Richard M. Karp, Raymond E. Miller and Arnold L. Rosenberg, Rapid identification of repeated patterns in strings, trees and arrays, STOC 1972
    locator: pages 125 to 136; the naming of substrings of length 2^k from pairs of names of length 2^(k-1)
  - paper: doi:10.1137/0222058
    title: Udi Manber and Gene Myers, Suffix arrays, a new method for on-line string searches, SIAM Journal on Computing 22(5), 1993
    locator: pages 935 to 948; the sorting of the suffixes in rounds of doubled length with bucket sorts
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 32.5, Suffix arrays (ranks of prefixes of length 2^k computed from pairs of ranks)
  - paper: doi:10.1016/j.tcs.2007.07.017
    title: N. Jesper Larsson and Kunihiko Sadakane, Faster suffix sorting, Theoretical Computer Science 387(3), 2007
    locator: pages 258 to 272
---

Prefix doubling is a technique for problems on all substrings of a string: give each substring of length $k$ an integer *name*, such that equal substrings get equal names, and then compute the names of length $2k$ from pairs of names of length $k$. After $\lceil \lg n \rceil$ rounds the names cover whole [suffixes](/suffix/). Karp, Miller and Rosenberg introduced it in 1972 to find repeated patterns, and Manber and Myers used it to build the [suffix array](/suffix-array/) in $O(n \log n)$ time. The same doubling of a step length appears in [binary lifting](/lca-binary-lifting/), in sparse tables for [range minimum queries](/range-minimum-query/) and in pointer jumping for [list ranking](/list-ranking/).

## In plain words

Comparing two long pieces of a text letter by letter is slow. Instead, give each piece a short number, its name, so that two pieces have the same name exactly when they are equal.

Start with pieces of one letter: the name is the letter. A piece of two letters is a piece of one letter followed by another piece of one letter, so its name can be made from the pair of their names. A piece of four letters is two pieces of two letters, and so on. Each round doubles the length, and each round only needs pairs of numbers from the round before. After a small number of rounds, the pieces are as long as the text, and the names sort all endings of the text.

## When it applies

- The objects are the substrings, or the suffixes, of one string, and a long object splits into two shorter objects of the same kind: $S[i \ldots i + 2k - 1] = S[i \ldots i + k - 1] \cdot S[i + k \ldots i + 2k - 1]$.
- The question is about equality or order, and equality or order of the whole is decided by the two halves in a fixed way: compare the first halves, then the second.
- You can afford $\Theta(n)$ space for the names of one round, and $O(\log n)$ rounds of linear or near-linear work.

When the answer needs the true order of whole suffixes in $O(n)$ time over an integer alphabet, induced sorting ([SA-IS](/sa-is/)) or recursion on a sample ([DC3](/dc3-skew-algorithm/)) is faster.

## The template

Let $S = S[0 \ldots n-1]$, 0-based, over a general ordered alphabet. Write $S_i^{\ell}$ for the prefix of length $\min(\ell, n - i)$ of the suffix $S_i$. No sentinel is appended; the name $\bot$ of the empty string, smaller than every other name, plays its role.

```pseudo id=main
PREFIX-DOUBLING(S)
L1  name[i] ← the rank of S[i] among the distinct symbols, for 0 ≤ i < n
L2  k ← 1
L3  while not DONE(name, k) do
L4      key[i] ← (name[i], name[i + k]), with ⊥ when i + k ≥ n
L5      name ← RENAME(key)                  ▷ equal keys get equal names
L6      k ← 2k
L7  return name                             ▷ name[i] is the name of S_i^k
```

The holes are:

1. **The meaning of a name.** Either only equality is kept (any injective map from keys to integers), or also order (the name is the rank of the key in sorted order). Order needs a sort; equality alone can use a hash table.
2. **RENAME.** A comparison sort of the pairs gives $O(n \log n)$ per round. Two passes of [counting sort](/counting-sort/), second component first, give $O(n)$ per round because names are integers below $n$, which is [radix sort](/radix-sort/). A hash table gives $O(n)$ expected per round for equality names.
3. **DONE.** Stop when $k \ge n$, or earlier when all names are distinct, because then the names of the $k$-prefixes already order the suffixes. Some problems stop at the first $k$ for which a property appears or disappears.

**Why it works.** By induction on the rounds, $name[i] = name[j]$ if and only if $S_i^k = S_j^k$, and for order names, $name[i] < name[j]$ if and only if $S_i^k < S_j^k$. The step uses $S_i^{2k} = S_i^k \cdot S_{i+k}^k$: two strings that split this way are equal when both halves are equal, and they compare like their first halves when these differ and like their second halves otherwise. The suffix array page proves this split lemma in full, including the case of a suffix shorter than $k$.

**Cost.** There are at most $\lceil \lg n \rceil + 1$ rounds. With radix sort the total is $O(n \log n)$ time and $O(n)$ space.

**Trace.** Take $S = \texttt{abaabab}$, $n = 7$, with order names.

| $k$ after the round | names $name[0 \ldots 6]$ | the strings $S_i^k$ |
|---|---|---|
| 1 | 0 1 0 0 1 0 1 | a b a a b a b |
| 2 | 1 3 0 1 3 1 2 | ab ba aa ab ba ab b |
| 4 | 2 5 0 3 6 1 4 | abaa baab aaba abab bab ab b |

After the round that gives $k = 4$, the seven names are different, so DONE holds. Listing the positions by name gives the suffix array $[2, 5, 0, 3, 6, 1, 4]$. In the round from $k = 2$ to $k = 4$, position 0 has the key $(name[0], name[2]) = (1, 0)$ and position 3 has $(1, 1)$: both start with $\texttt{ab}$, and $\texttt{aa} < \texttt{ab}$ decides.

## Classic examples

- **Suffix array by doubling.** [Manber-Myers](/manber-myers-algorithm/) uses order names and bucket sorts, $O(n \log n)$ time. The simpler version with a comparison sort, $O(n \log^2 n)$, is in the [suffix array](/suffix-array/) page and in CLRS Section 32.5.
- **Repeated patterns.** The [Karp-Miller-Rosenberg algorithm](/karp-miller-rosenberg-algorithm/) uses equality names to find all repeated substrings of a given length, in strings, trees and arrays.
- **Equality of any two substrings.** Keep the names of all rounds, $O(n \log n)$ space. For a length $L$ with $2^j \le L < 2^{j+1}$, the substrings $S[a \ldots a + L - 1]$ and $S[b \ldots b + L - 1]$ are equal if and only if the names of length $2^j$ at $a$ and $b$ agree and the names of length $2^j$ at $a + L - 2^j$ and $b + L - 2^j$ agree. This answers [substring equality queries](/substring-equality-queries/) in $O(1)$ time without hashing. In $\texttt{abaabab}$, $S[0 \ldots 2] = S[3 \ldots 5] = \texttt{aba}$, and the names of length 2 are $1 = 1$ at positions 0 and 3, and $3 = 3$ at positions 1 and 4.
- **Faster suffix sorting.** [Larsson-Sadakane](/larsson-sadakane-algorithm/) refines only the groups of suffixes that still share a name, and uses the current name of $S_{i+k}$ rather than the name of the previous round, which is still correct and saves work in practice.
- **Doubling on trees and lists.** The same idea, with "the node $2^j$ steps up" in place of "the substring of length $2^j$", gives [binary lifting](/lca-binary-lifting/) for the [lowest common ancestor](/lowest-common-ancestor/), the sparse table for [range minimum queries](/range-minimum-query/), and pointer jumping for [list ranking](/list-ranking/).

## Variations

- **Equality names by hashing.** A hash table from pairs to new names gives expected $O(n)$ per round. Unlike [polynomial hashing](/polynomial-rolling-hash/), there are no false matches: the table maps distinct pairs to distinct names.
- **Tripling.** Combine three blocks of length $k$ into one of length $3k$. There are fewer rounds, but each round sorts triples. The idea of a sample of positions modulo 3 reappears in [DC3](/dc3-skew-algorithm/), which does not double.
- **Early stop by group.** Stop refining a group of positions once it has one member (Larsson-Sadakane), or once a property holds for it.
- **Sorting with the inverse array.** Manber and Myers sort by the first component for free: if the suffixes are already sorted by $k$-prefix, then sorting the positions $i - k$ by the rank of $S_i$ gives their order by the second component.

## Pitfalls

- **The wrong value for a missing half.** When $i + k \ge n$, the second half is empty, and its name must be below every real name. Giving it the name 0 of the smallest symbol makes $\texttt{a}$ equal to $\texttt{aa}$ in the first round.
- **Radix sort in the wrong order.** In the two passes of counting sort, the stable pass on the second component must come first. Sorting by the first component first and then by the second sorts the pairs by their second component.
- **Rotations instead of suffixes.** If the second half wraps around, with $name[(i + k) \bmod n]$ in line L4, the names are those of rotations. For a periodic string such as $(\texttt{ab})^4$ the rotations at 0 and 2 are equal, the names never become distinct, and a DONE test that waits for distinct names never ends. Use the empty second half $\bot$, or bound the rounds by $k \ge n$.
- **Space of all rounds.** Keeping the names of all $\lceil \lg n \rceil$ rounds, for substring equality queries, needs $\Theta(n \log n)$ words. For a suffix array only the last round is needed.

## Exercises

1. Show that for $S = \texttt{a}^n$, $n \ge 2$, exactly $\lceil \lg n \rceil$ rounds are needed before all names are distinct.
   <details><summary>Hint</summary>After the round that gives block length $k$, the $n - k + 1$ positions $i$ with $n - i \ge k$ all have the $k$-prefix $\texttt{a}^k$ and so the same name. The names are distinct only when $n - k + 1 \le 1$, that is, $k \ge n$. Since $k = 2^r$ after $r$ rounds, $r = \lceil \lg n \rceil$.</details>
2. Use the names of all rounds to find the length of the longest substring that occurs at least twice, in $O(n \log n)$ time.
   <details><summary>Hint</summary>Equality names of length $L$ for any $L$ follow from two overlapping blocks. "Some substring of length $L$ occurs twice" is monotone in $L$, so search $L$ by binary search, and test each $L$ with a hash set of name pairs.</details>
3. Write RENAME with two passes of counting sort and prove that it sorts the pairs.
4. Show that no string of length 8 over the alphabet $\{a, b\}$ has pairwise distinct names after the first round.
   <details><summary>Hint</summary>After the first round the names are those of the 2-prefixes. Positions 0 to 6 have 2-prefixes of length 2, and there are only 4 such strings over two letters, so two of these 7 positions share a name.</details>

## References
