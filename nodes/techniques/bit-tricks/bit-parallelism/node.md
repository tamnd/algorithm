---
tag: B7GJ28
kind: technique
slug: bit-parallelism
name: Bit parallelism
aliases:
- bit-parallel algorithms
- word-level parallelism
area: techniques/bit-tricks
level: advanced
summary: Packing many small values into one machine word so that one operation updates them all at once.
prereqs: [bitwise-operations, bit-set, word-ram]
see_also: [shift-or, bitap-algorithm, myers-bit-parallel-algorithm, bit-parallel-lcs, simd-within-a-register, bit-slicing, four-russians-method, bitset-adjacency-matrix]
sources:
  - paper: doi:10.1145/135239.135243
    title: Ricardo Baeza-Yates and Gaston H. Gonnet, A new approach to text searching, Communications of the ACM 35(10), 1992
    locator: pp. 74 to 82
  - paper: doi:10.1145/316542.316550
    title: Gene Myers, A fast bit-vector algorithm for approximate string matching based on dynamic programming, Journal of the ACM 46(3), 1999
    locator: pp. 395 to 415
  - paper: doi:10.1016/0020-0190(86)90091-8
    title: Lloyd Allison and Trevor I. Dix, A bit-string longest-common-subsequence algorithm, Information Processing Letters 23(5), 1986
    locator: pp. 305 to 310
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.1.3, Bitwise Tricks and Techniques
---

Bit parallelism stores a set of up to $w$ small facts, such as the active states of an automaton or one column of a dynamic programming table, as the bits of one machine word, and updates all of them at once with shifts, Boolean operations and additions. A computation that would take $m$ steps for each input symbol then takes $O(\lceil m / w \rceil)$ word operations. The classic examples are the [Shift-Or](/shift-or/) string search of Baeza-Yates and Gonnet (1992), the bit-vector [longest common subsequence](/bit-parallel-lcs/) of Allison and Dix (1986), and [Myers's bit-vector algorithm](/myers-bit-parallel-algorithm/) for approximate matching (1999). Bitset dynamic programming, such as the subset sum update `r |= r << a`, uses the same idea.

## In plain words

A computer word has 64 bits, and one instruction changes all 64 at once. If your algorithm keeps track of many yes-or-no facts that change in the same way at each step, keep each fact in one bit of a word. Then one instruction updates all the facts together.

For example, to search for a short word in a long text, keep one bit for each prefix of the word: is this prefix ending here? When the next letter of the text comes, every prefix that was alive moves one step forward if the letter fits, which is a shift and an AND. Instead of checking each prefix, you do two instructions.

## When it applies

- The state of the algorithm after each step is a vector of $m$ bits, or of small numbers, for a parameter $m$ that is often at most $w$, such as the length of a pattern.
- The update is the same rule for every position, and it depends only on nearby positions, so shifts carry the information between neighbours.
- The rule can be written with AND, OR, XOR, NOT, shifts and, where a chain of dependencies runs along the vector, an addition, whose carry propagates along the bits in one instruction.
- For $m > w$, the vector splits into $\lceil m / w \rceil$ words, with the bit that leaves one word by a shift or a carry passed to the next.

## The template

1. **Encode the state.** Choose what bit $i$ of the state word $D$ means after reading the input up to position $j$, for example "the first $i + 1$ symbols of the pattern match the text ending at $j$".
2. **Precompute masks.** For each input symbol $c$, a mask $B[c]$ with bit $i$ set when the rule for position $i$ accepts $c$. This costs $O(\sigma + m)$ for an alphabet of size $\sigma$.
3. **Write the update as word operations.** Express the new state of each bit through the old state of the same bit and of its neighbours, and translate: "bit $i - 1$ of the old state" is a left shift, "and the symbol fits" is an AND with $B[c]$.
4. **Read the answer.** Test one bit, count the ones, or watch a counter updated from the top bits.

**Example (Shift-And).** Search for $p$ = aba in $t$ = abaababa. The masks are $B[\mathtt a] = 101_2$ and $B[\mathtt b] = 010_2$. The update is $D \leftarrow ((D \ll 1) \mathbin{|} 1) \mathbin{\&} B[t_j]$, and a match ends at $j$ when bit 2 of $D$ is 1. The states after each symbol are 001, 010, 101, 001, 010, 101, 010, 101, so matches end at positions 2, 5 and 7, and start at 0, 3 and 5. Each symbol costs four word operations, whatever the length of the pattern up to $w$.

**Cost.** For a state of $m$ bits and an input of length $n$, $O(n \lceil m / w \rceil)$ word operations, against $O(nm)$ for the direct method.

## Classic examples

- **Exact string matching.** [Shift-Or](/shift-or/) of Baeza-Yates and Gonnet keeps the complement of the Shift-And state, which saves the OR with 1. It runs in $O(n \lceil m / w \rceil)$ time. The [Bitap algorithm](/bitap-algorithm/) extends it to classes of symbols and to $k$ errors with $k + 1$ state words.
- **Longest common subsequence.** Allison and Dix encode the differences between adjacent entries of a column of the LCS table as a bit vector and update it with an addition, which propagates the dependencies along the column through the carry. One form of the update, for a symbol $c$ of the second string, is $U = V \mathbin{\&} M[c]$, $V \leftarrow (V + U) \mathbin{|} (V - U)$, starting from $V$ of all ones; the LCS length is the number of zeros in $V$. For $a$ = abcb and $b$ = bacbb this gives 3. See [bit-parallel LCS](/bit-parallel-lcs/).
- **Approximate matching.** [Myers's algorithm](/myers-bit-parallel-algorithm/) encodes the vertical differences of the edit distance table, each in $\{-1, 0, 1\}$, in two bit vectors, and computes [approximate string matching](/approximate-string-matching/) with edit distance in $O(n \lceil m / w \rceil)$ time.
- **Subset sum.** Keep the set of reachable sums as a bitset $r$, with $r = 1$ at the start. Adding an item of size $a$ is $r \leftarrow r \mathbin{|} (r \ll a)$. For the items 3, 5 and 7, the reachable sums are 0, 3, 5, 7, 8, 10, 12 and 15. For $n$ items and a bound $S$ this is $O(n S / w)$ word operations for the [subset sum problem](/subset-sum-problem/).
- **Graph algorithms.** With a [bitset adjacency matrix](/bitset-adjacency-matrix/), the common neighbours of $u$ and $v$ are $N(u) \mathbin{\&} N(v)$, so [triangle counting](/triangle-counting/) costs $O(n^3 / w)$ for each pass over all pairs, and the BFS frontier of a dense graph updates in $O(n / w)$ words for each vertex.

## Variations

- **Several machines at once.** A [nondeterministic finite automaton](/nondeterministic-finite-automaton/) with at most $w$ states runs with one bit for each state; the Glushkov construction gives automata whose transitions are shifts for regular expressions.
- **Counters in fields.** Keep small counters, not bits, in fields of a word, and update them with [SIMD within a register](/simd-within-a-register/).
- **Instances in bits.** Run $w$ independent copies of a circuit, one in each bit position: this is [bit slicing](/bit-slicing/), the transpose of this layout.
- **Combined with tables.** The [Four Russians method](/four-russians-method/) adds a $\log n$ factor on top of the factor $w$ by precomputing the effect of blocks of bits.
- **Vector registers.** With 256-bit or 512-bit registers, $w$ grows, but shifts and carries across 64-bit lanes need extra instructions.

## Pitfalls

- **Bits that fall off.** A left shift drops the top bit and an addition loses the carry out. For states longer than one word, pass these bits to the next word by hand.
- **Shift by $w$ or more.** In C, a shift by the word size or more is undefined. Patterns of length exactly $w$ need care in the match test.
- **Wrong bit order.** If bit $i$ stands for prefix $i + 1$, the shift goes left; with the other order it goes right. Mixing the two gives wrong matches that still look plausible.
- **Large alphabets.** The mask table has one word for each symbol. For Unicode text, map the symbols of the pattern to a small alphabet first, with one class for all other symbols.
- **The bound is not better than $O(nm / w)$.** The method divides the work by $w$ but does not change its form. When $m$ is much larger than $w$, algorithms with a better dependence on $m$, such as the Knuth-Morris-Pratt or suffix-based methods for exact matching, can be faster.

## Exercises

1. Run Shift-Or, with the complemented state, on the pattern abab and the text abababb, and list the states and the matches.
2. Extend Shift-And to patterns with classes of symbols, such as `a[bc]a`, and show that only the masks change.
3. Prove that the subset sum update $r \leftarrow r \mathbin{|} (r \ll a)$ gives the set of sums of subsets of the items processed so far, and adapt it to count, modulo 2, the number of subsets with each sum.
4. Prove that the LCS update $V \leftarrow (V + U) \mathbin{|} (V - U)$ with $U = V \mathbin{\&} M[c]$ keeps, as zeros of $V$, the positions where the LCS row increases, for a pattern of length at most $w$. Check it on $a$ = abcb and $b$ = bacbb.
5. Give a bit-parallel algorithm that tests whether a text contains the pattern with at most one substituted symbol, using two state words, and bound its time.

## References
