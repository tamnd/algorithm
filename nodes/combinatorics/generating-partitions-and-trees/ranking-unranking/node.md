---
tag: A6PZ6K
kind: technique
slug: ranking-unranking
name: Ranking and unranking
aliases:
- Rank and unrank
- Ranking by counting completions
area: combinatorics/generating-partitions-and-trees
level: core
summary: Mapping each object to its index in a fixed order (ranking) and back (unranking), enabling direct access to the k-th object.
prereqs: [lexicographic-order, combinatorial-generation]
see_also: [permutation-ranking, combinatorial-number-system, balanced-bracket-sequence-ranking, kth-balanced-bracket-sequence, restricted-growth-string, enumerative-coding, zaks-tree-generation, pruefer-decoding]
sources:
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration and Search, CRC Press, 1999
    locator: Chapter 2 (the definitions of rank, unrank and successor, and their use for subsets, k-subsets and permutations)
  - url: https://page.math.tu-berlin.de/~felsner/SemWS17-18/Ruskey-Comb-Gen.pdf
    title: Frank Ruskey, Combinatorial Generation, working version, University of Victoria, 1995 to 2003
    locator: Chapter 4, Lexicographic Algorithms (ranking and unranking of combinations and of binary trees as sums of edge labels of a lattice walk)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.2.1.3, Generating all combinations (the combinatorial number system), and Section 7.2.1.2 (permutations and mixed-radix numbers)
---

Ranking and unranking is the technique of numbering the objects of a finite set $S$ by the integers $0, 1, \ldots, N - 1$, with $N = |S|$, in a fixed order, and of computing the number of a given object (*ranking*) and the object with a given number (*unranking*) without listing $S$. The usual method writes each object as a sequence of choices and counts, for each choice, how many objects begin with a smaller choice at that point. Its only problem-specific part is a function that counts the completions of a partial object, often a closed form or a table built by [dynamic programming](/memoization/). Rank and unrank give direct access to the $k$-th object, uniform random objects, compact codes and an even split of a listing into parts.

## In plain words

Think of a dictionary. To find the page number of a word, you do not read the dictionary. You count how many words start with a smaller first letter, then, among the words with your first letter, how many have a smaller second letter, and so on. The sum is the position of the word.

Ranking does the same for any objects that you build one choice at a time: brackets, numbers, letters. All it needs is a way to count how many objects can still be built after a given partial choice. Unranking runs the same count in reverse: at each step, it skips whole blocks of objects until it finds the block that holds the wanted number.

## When it applies

- Each object of $S$ is a sequence $x = (x_1, \ldots, x_L)$ of choices, and the order on $S$ is the [lexicographic order](/lexicographic-order/) of these sequences (or an order that a bijection turns into it).
- After any prefix, the set of allowed next choices is easy to list in order, and it depends only on a small *state* $\sigma$ of the prefix, for example its length and a height, a sum or a maximum.
- The number of completions $\mathrm{COUNT}(\sigma, i)$, the objects that extend a prefix of length $i$ with state $\sigma$, can be computed fast: by a closed form such as a binomial coefficient or a factorial, or by a table over all states.
- Signals in a problem: "find the $k$-th object", "the index of this object", "pick an object uniformly at random", "store an object in about $\lg N$ bits".

## The template

The holes are: the initial state $\sigma_0$, the allowed choices $\mathrm{CHOICES}(\sigma)$ in increasing order, the state update $\mathrm{STEP}(\sigma, a)$, and the count $\mathrm{COUNT}(\sigma, i)$ of completions of a prefix of length $i$ that ends in state $\sigma$. The count of a full object is 1.

```pseudo id=main
RANK(x)                          ▷ x = (x_1, ..., x_L) in S
L1  r ← 0, σ ← σ_0
L2  for i ← 1 to L do
L3      for each a in CHOICES(σ) with a < x_i do
L4          r ← r + COUNT(STEP(σ, a), i)       ▷ objects that branch off here
L5      σ ← STEP(σ, x_i)
L6  return r

UNRANK(k)                        ▷ 0 ≤ k < N
L7  σ ← σ_0
L8  for i ← 1 to L do
L9      for each a in CHOICES(σ), in increasing order do
L10         c ← COUNT(STEP(σ, a), i)
L11         if k < c then x_i ← a, σ ← STEP(σ, a), and go to the next i
L12         k ← k − c
L13 return x
```

**Why it works.** An object $y < x$ differs first from $x$ at some index $i$, with $y_i < x_i$. Grouping the smaller objects by that index and by $y_i$ gives disjoint groups, and line L4 adds the size of each group once. So RANK$(x)$ is the number of objects smaller than $x$, its 0-based position. UNRANK keeps the invariant "the wanted object is at position $k$ among the objects with the current prefix" and picks, at each index, the block that holds position $k$. The proofs on the pages of [ranking](/balanced-bracket-sequence-ranking/) and [unranking](/kth-balanced-bracket-sequence/) of bracket words are this argument in full.

**A small run.** Let $S$ be the words of length 3 over $a < b < c$ with no two equal adjacent letters, so $N = 3 \cdot 2 \cdot 2 = 12$. The state is the last letter, the choices are the letters other than it, and $\mathrm{COUNT}(\sigma, i) = 2^{3-i}$. For $x = cab$: at $i = 1$ the smaller choices $a$ and $b$ add $4 + 4$; at $i = 2$ the allowed choices are $a$ and $b$, and none is smaller than $a$; at $i = 3$ the allowed choices are $b$ and $c$, and none is smaller than $b$. So the rank is 8. The list is $aba, abc, aca, acb, bab, bac, bca, bcb, cab, \ldots$, and $cab$ is at position 8.

**Cost.** With $L$ steps, at most $q$ choices per step and a count in time $T$, both functions take $O(L q T)$ time, plus the time to build a count table. The numbers go up to $N$, so each has about $\lg N$ bits. When $N$ is exponential in $L$, as it usually is, the arithmetic is on big integers and costs more than $O(1)$ per operation. Binary search over the choices, with prefix sums of the counts, cuts $q$ to $\lg q$ when the choices are many.

## Classic examples

- [Combinatorial number system](/combinatorial-number-system/) and [ranking combinations](/combinatorial-ranking-and-unranking/): a $k$-subset $c_1 < \cdots < c_k$ in colex order has rank $\sum_i \binom{c_i}{i}$ (0-based elements); the count is a binomial coefficient.
- [Permutation ranking](/permutation-ranking/) and [unranking](/permutation-unranking/): the count of completions is $(n - i)!$, and the rank is the [Lehmer code](/lehmer-code/) read in the [factorial number system](/factorial-number-system/).
- [Ranking](/balanced-bracket-sequence-ranking/) and [unranking](/kth-balanced-bracket-sequence/) balanced bracket sequences: the state is the height, and the count is a [ballot number](/ballot-theorem/) from a table of size $\Theta(n^2)$.
- [Restricted growth strings](/restricted-growth-string/) for set partitions: the state is the length and the current maximum, and the counts come from a table over both.
- [Zaks' algorithm](/zaks-tree-generation/): binary and $t$-ary trees coded by the positions of their internal nodes, ranked with counts of the same ballot type.
- [Prüfer decoding](/pruefer-decoding/): a labeled tree on $[n]$ is ranked by reading its Prüfer sequence as a number in base $n$, which gives all ranks $0$ to $n^{n-2} - 1$.
- [Enumerative coding](/enumerative-coding/): a data compression method that stores a sequence by its rank among all sequences of the same type.

## Variations

- **Bijection to a mixed-radix number.** When the number of choices at step $i$ does not depend on the earlier choices, the rank is a number in a mixed radix, as for permutations and for Prüfer sequences. No table is needed.
- **Rank by decomposition.** For recursive structures, order the objects first by a size parameter and then by the ranks of the parts. For binary trees with $n$ nodes, order by the size $\ell$ of the left subtree, then by the rank of the left subtree, then by the rank of the right subtree. The rank is $\sum_{\ell' < \ell} C_{\ell'} C_{n-1-\ell'} + \mathrm{rank}(L) \cdot C_{n-1-\ell} + \mathrm{rank}(R)$, with $C_m$ the [Catalan numbers](/catalan-numbers/).
- **Gray code orders.** In a Gray code order, the rank is often a short transformation of a mixed-radix number, such as the conversion between the [binary reflected Gray code](/binary-reflected-gray-code/) and binary. The template applies with choices that alternate between increasing and decreasing order.
- **Successor from rank.** A successor function is unrank(rank$(x) + 1$). It is slower than a direct successor rule such as [next permutation](/next-permutation/), but it works for every order the template covers.
- **Random generation.** Unranking a uniform integer in $[0, N)$ gives a uniform random object. This is exact, unlike a random walk, but it needs the big counts.
- **Objects up to symmetry.** Ranking unlabeled objects, such as trees or graphs up to isomorphism, first needs a canonical form, and then a way to count the canonical forms that branch off at each step. For rooted trees the [level sequence](/level-sequence/) gives such a form; for graphs no efficient method of this kind is known in general.

## Pitfalls

- **The order of the choices.** Line L3 and line L9 must use the same order as the listing. Ranking with one order and unranking with the other gives a permutation of the ranks, not the identity.
- **The wrong state.** $\mathrm{COUNT}$ must depend only on what the future choices can see. If the state forgets a constraint, for example the number of opening brackets used, the counts are too large and the ranks skip numbers.
- **Unreachable states.** A choice that leads to a state with no completion has count 0. The test of line L11 then never picks it, but code that divides by a count, or indexes a table out of range, fails there.
- **Overflow.** $N$ grows fast: $20! > 2^{61}$ and the Catalan number $C_{36} > 2^{63}$. Use big integers, or fix the largest size in advance.
- **Off by one.** Ranks here start at 0. Some books number from 1; mixing the two conventions shifts every result by one.

## Exercises

1. Rank and unrank the $k$-subsets of $\{1, \ldots, n\}$ in lexicographic order with the template. Give $\mathrm{COUNT}$ as a binomial coefficient of the remaining elements.
2. A Motzkin path of length $L$ uses the steps up, level and down, starts and ends at height 0 and never goes below it. Give the state, the choices and a table recurrence for $\mathrm{COUNT}$, and rank the paths in the order up $<$ level $<$ down.
3. Show that the rank of the decomposition variation for binary trees is a bijection onto $[0, C_n)$, by induction on $n$.

## References
