---
tag: 9TN7DN
kind: problem
slug: k-subset-enumeration
name: Enumerating k-subsets (combinations)
aliases:
- generating combinations
- k-combinations enumeration
- listing all k-element subsets
- combination generation
area: combinatorics/generating-combinations
level: intro
summary: List all C(n,k) ways to choose k elements from an n-set, each exactly once.
complexity:
  vars: {n: the size of the ground set, k: the size of each subset, N: the number of k-subsets}
  time: {worst: Ω(N)}
prereqs: [binomial-coefficient, combinatorial-generation]
see_also: [lexicographic-combinations, recursive-combination-generation, revolving-door-ordering, cool-lex-order, ehrlich-loopless-combinations, fixed-weight-binary-strings, combinatorial-number-system, combinations-with-repetition]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.3, Generating all combinations (Algorithms L, T, R and C, the combinatorial number system, revolving-door and near-perfect orders)
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration, and Search, CRC Press, 1999
    locator: Chapter 2, Section 2.3, k-element subsets (lexicographic, co-lex and minimal change orderings)
  - book: isbn:9780125192606
    title: Albert Nijenhuis and Herbert S. Wilf, Combinatorial Algorithms for Computers and Calculators, second edition, Academic Press, 1978
    locator: Chapter 3, Next k-subset of an n-set
  - paper: doi:10.1137/S0036144595295272
    title: Carla Savage, A survey of combinatorial Gray codes, SIAM Review 39(4), 1997, 605-629
    locator: Section on Gray codes for k-subsets (combinations)
---

The k-subset enumeration problem asks for a list of all $C(n, k)$ subsets of size $k$ of an $n$-element set, each exactly once. These subsets are the combinations of $n$ things taken $k$ at a time. Each method needs $\Omega(C(n, k))$ time, and [loopless](/loopless-generation/) methods reach $O(1)$ time in the worst case for each subset, with exactly one element in and one element out at each step.

## In plain words

You have $n$ players and you must pick a team of $k$. You want to see every possible team, once each. The order of the players inside a team does not matter, so the team $\{1, 2\}$ is the same as the team $\{2, 1\}$.

The usual trick is to write each team as a sorted list. Then you list the sorted lists like words in a dictionary: $\{1, 2, 3\}$, then $\{1, 2, 4\}$, and so on. Other orders change only one player at each step, so a program can update its work with one swap.

## Definition

Let $0 \le k \le n$, let $[n] = \{1, \ldots, n\}$, and let $\binom{[n]}{k} = \{S \subseteq [n] : |S| = k\}$. Then $|\binom{[n]}{k}| = C(n, k) = \frac{n!}{k!\,(n-k)!}$, the [binomial coefficient](/binomial-coefficient/). In this page $N = C(n, k)$.

**Input.** The integers $n$ and $k$.

**Output.** A sequence $S_0, S_1, \ldots, S_{N-1}$ in which each element of $\binom{[n]}{k}$ appears exactly once.

**Representation.** The standard form of $S$ is its elements in increasing order, $a_1 < a_2 < \cdots < a_k$. Knuth uses the decreasing form $c_k > \cdots > c_1$ over $\{0, \ldots, n-1\}$. A third form is the $n$-bit string with exactly $k$ ones, see [fixed-weight binary strings](/fixed-weight-binary-strings/).

**Cost model.** The generator keeps one current subset in an array and changes it in place. The visit of each subset is free. If each subset is copied, each copy costs $\Theta(k)$ more.

## Variants

- **Lexicographic order.** Sorted lists compared as words. See [lexicographic combinations](/lexicographic-combinations/).
- **Colexicographic order.** Compare at the largest element first. In bit string form this is the increasing order of the integers with $k$ ones, so [Gosper's hack](/gospers-hack/) produces it. See [colexicographic order](/colexicographic-order/).
- **Minimal change order.** Each step removes one element and adds one element. The [revolving door](/revolving-door-ordering/) order is the classic example. The [Eades and McKay](/eades-mckay-algorithm/) order and [Chase's sequence](/chase-sequence/) add stronger conditions on which elements can change. See [combination Gray code generation](/combination-gray-code-generation/).
- **Prefix shift order.** Each step moves one bit of the string to the front. This is [cool-lex order](/cool-lex-order/).
- **Rank and unrank.** Map each subset to its position in the list and back. See [ranking and unranking combinations](/combinatorial-ranking-and-unranking/) and the [combinatorial number system](/combinatorial-number-system/).
- **With repetition.** Choose $k$ elements with repeats allowed. See [combinations with repetition](/combinations-with-repetition/).
- **One random subset.** Choose one $k$-subset with probability $1/N$, for example by unranking a random integer.

## Examples

**$n = 5$, $k = 3$.** There are $C(5, 3) = 10$ subsets.

| rank | lexicographic | colexicographic | revolving door |
| --- | --- | --- | --- |
| 0 | $123$ | $123$ | $123$ |
| 1 | $124$ | $124$ | $134$ |
| 2 | $125$ | $134$ | $234$ |
| 3 | $134$ | $234$ | $124$ |
| 4 | $135$ | $125$ | $145$ |
| 5 | $145$ | $135$ | $245$ |
| 6 | $234$ | $235$ | $345$ |
| 7 | $235$ | $145$ | $135$ |
| 8 | $245$ | $245$ | $235$ |
| 9 | $345$ | $345$ | $125$ |

In the revolving door column each step removes one element and adds one element. In the lexicographic column the step from $145$ to $234$ changes all three elements.

**Sizes.** A poker hand is a $5$-subset of $52$ cards, and $C(52, 5) = 2598960$. A lottery ticket that picks $6$ of $49$ numbers is one of $C(49, 6) = 13983816$ tickets. Both lists are small enough for a computer to scan in a second or so. $C(100, 50)$ has $97$ bits, so no list of it can ever finish.

## Known algorithms

| algorithm | order | time for each subset | page |
| --- | --- | --- | --- |
| lexicographic successor | lexicographic | $O(1)$ amortized when $k \le n/2$ | [lexicographic combinations](/lexicographic-combinations/) |
| choose or skip recursion | lexicographic | $O(1)$ amortized when $k \le n/2$ | [recursive combination generation](/recursive-combination-generation/) |
| Gosper's hack | colexicographic | $O(1)$ word operations | [next same popcount](/next-same-popcount/) |
| revolving door with Payne's jump | revolving door | $O(1)$ worst case | [Ehrlich's loopless combination generation](/ehrlich-loopless-combinations/) |
| cool-lex | prefix shifts | $O(1)$ worst case | [cool-lex order](/cool-lex-order/) |
| Eades and McKay | strong minimal change | $O(1)$ amortized | [Eades-McKay algorithm](/eades-mckay-algorithm/) |
| Chase's twiddle | Chase's sequence | $O(1)$ amortized | [Chase's sequence](/chase-sequence/) |
| unrank each rank | any ranked order | $O(k)$ arithmetic operations | [ranking and unranking combinations](/combinatorial-ranking-and-unranking/) |

The lexicographic successor scans from the right. Over the whole list the scan takes $C(n, k-1)$ steps in total, which is $k/(n-k+1)$ steps for each subset on average. This is $O(1)$ for $k \le n/2$, but for $k = n - 1$ it is about $n/2$. When $k > n/2$, a program can list the $(n-k)$-subsets and take complements.

## Bounds

- **Lower bound.** There are $N$ outputs, so each algorithm takes $\Omega(N)$ time.
- **Changes.** Two different $k$-subsets differ in at least two positions of their bit strings, one $0 \to 1$ and one $1 \to 0$. So a list in the in-place model makes at least $N - 1$ such swaps, $2(N - 1)$ bit changes. The revolving door order meets this bound.
- **Upper bound.** Loopless algorithms ([Ehrlich's](/ehrlich-loopless-combinations/), [cool-lex](/cool-lex-order/)) take $O(1)$ time in the worst case between two visits, after $O(n)$ initialization. So the total time is $\Theta(N)$ plus $O(n)$.
- **Written output.** If each subset is written in full, the output has $kN$ numbers, so the time is $\Theta(kN)$.

## Reductions

- **To bit strings.** A $k$-subset of $[n]$ is the same as an $n$-bit string with $k$ ones. See [fixed-weight binary strings](/fixed-weight-binary-strings/).
- **Complement.** $S \mapsto [n] \setminus S$ is a bijection from $k$-subsets to $(n-k)$-subsets. A list for $n - k$ gives a list for $k$.
- **Lattice paths.** A $k$-subset is a monotone lattice path with $k$ up steps and $n - k$ right steps: step $j$ goes up when $j \in S$. See [counting lattice paths](/counting-lattice-paths/).
- **Multisets.** The map $a_i \mapsto a_i - (i - 1)$ takes $k$-subsets of $[n + k - 1]$ to $k$-multisets of $[n]$. See [combinations with repetition](/combinations-with-repetition/) and [stars and bars](/stars-and-bars/).
- **From the power set.** A [power set](/power-set-enumeration/) list filtered by size gives the $k$-subsets, but it takes $2^n$ steps, which can be much more than $N$.
- **Pascal's rule.** $\binom{[n]}{k}$ is the disjoint union of $\binom{[n-1]}{k}$ and the sets $T \cup \{n\}$ for $T \in \binom{[n-1]}{k-1}$. This is the recursion behind [Pascal's triangle](/pascal-triangle-dp/), behind the recursive generator and behind the revolving door order.

## Applications

- **Brute force over small selections.** A test for a [clique](/clique-problem/) of size $k$, a [vertex cover](/vertex-cover/) of size $k$ or a [set cover](/set-cover/) with $k$ sets tries all $C(n, k)$ choices, which is $O(n^k)$ for fixed $k$.
- **Feature and sample selection.** Statistics and machine learning try all subsets of $k$ features, or all splits of a sample into two groups of fixed size in exact permutation tests.
- **Test design.** A test suite checks every pair or every triple of options.
- **Indexing.** The [combinatorial number system](/combinatorial-number-system/) stores a $k$-subset as one integer, for example in compressed bit vectors such as the [RRR bit vector](/rrr-bitvector/).

## References
