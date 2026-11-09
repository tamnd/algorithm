---
tag: W6SKA5
kind: problem
slug: multiset-permutations
name: Permutations of a multiset
aliases:
- distinct permutations
- permutations with repetition of items
- multiset arrangements
area: combinatorics/generating-permutations
level: core
summary: Generate each distinct arrangement of a list that may contain repeated items exactly once.
model: comparison-model
complexity:
  vars: {n: the number of items, N: the number of distinct arrangements}
  time: {worst: Ω(N)}
prereqs: [permutation, multinomial-coefficient, generating-all-permutations]
see_also: [next-permutation, lexicographic-permutation-successor, multinomial-coefficient, generating-all-permutations, permutation-ranking, combinatorial-generation, loopless-generation, constant-amortized-time-generation]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.2.1.2, Algorithm L (lexicographic permutation generation of a multiset) and the count of multiset permutations
  - paper: doi:10.1137/1.9781611973068.107
    title: Aaron Williams, Loopless generation of multiset permutations using a constant number of variables by prefix shifts, Proceedings of the Twentieth Annual ACM-SIAM Symposium on Discrete Algorithms (SODA 2009) 987-996
    locator: the whole paper (the cool-lex order of multiset permutations and its loopless generation)
  - paper: doi:10.1093/comjnl/47.5.612
    title: James F. Korsh and Paul S. LaFollette, Loopless array generation of multiset permutations, The Computer Journal 47(5) (2004)
    locator: the whole paper
---

The multiset permutation problem asks for a list of all distinct arrangements of a sequence whose items may repeat, such as the letters of BANANA, each exactly once. If the item values have multiplicities $m_1, \ldots, m_k$ with sum $n$, there are $N = n! / (m_1! \cdots m_k!)$ arrangements, a [multinomial coefficient](/multinomial-coefficient/). Methods for [distinct items](/generating-all-permutations/) list each arrangement $m_1! \cdots m_k!$ times, so they are wasteful here. [Next permutation](/next-permutation/) handles repeats correctly and lists the arrangements in lexicographic order, and loopless methods by prefix shifts reach $O(1)$ time per arrangement in the worst case.

## In plain words

You have some letters, and some of them are the same, for example the six letters of BANANA. You want every word that you can spell with all of them, and you want each word once. Swapping the two N's does not give a new word, so a list of all orders of six different letters would show each word many times.

The fix is to treat equal letters as the same from the start. One way is to list the words as in a dictionary: from each word, step to the next larger word with the same letters. This never makes the same word twice. BANANA gives 60 words in this way, not 720.

## Definition

**Input.** A sequence $a_1, \ldots, a_n$ of items from a [totally ordered](/total-order/) set, or, in the same way, the distinct values $v_1 < \cdots < v_k$ with multiplicities $m_1, \ldots, m_k \ge 1$ and $m_1 + \cdots + m_k = n$.

**Output.** A sequence of $N$ visits of an array $A[1 \ldots n]$, such that the arrays at the visits are the $N$ distinct sequences that contain each $v_j$ exactly $m_j$ times, each sequence once.

The count is the multinomial coefficient

$$N = \binom{n}{m_1, \ldots, m_k} = \frac{n!}{m_1!\, m_2! \cdots m_k!},$$

because each of the $n!$ orders of $n$ labeled items gives one arrangement, and each arrangement arises from exactly $m_1! \cdots m_k!$ orders, one for each way to permute the labels of equal items. The output models and the cost measures (total time, amortized time per arrangement, delay) are the same as for [generating all permutations](/generating-all-permutations/). An algorithm is [CAT](/constant-amortized-time-generation/) when its total time is $O(N)$, and [loopless](/loopless-generation/) when its delay is $O(1)$.

## Variants

- **Lexicographic order.** The list must be in [lexicographic order](/lexicographic-order/). Each step is a [lexicographic successor](/lexicographic-permutation-successor/).
- **Two values.** With $k = 2$, an arrangement of $m_1$ zeros and $m_2$ ones is a bit string with $m_2$ ones, and it is the same as a $k$-subset of $[n]$ with $k = m_2$. This is [$k$-subset enumeration](/k-subset-enumeration/).
- **Minimal change.** Consecutive arrangements must differ by a transposition, an adjacent transposition, or a prefix shift. For multisets, such lists do not always exist for every kind of change, and the known results depend on the multiplicities.
- **Ranking and unranking.** Map an arrangement to its position in lexicographic order, and back. See the example below.
- **Partial arrangements.** List the distinct sequences of length $r < n$ made from the multiset.

## Examples

**Small case.** The 12 arrangements of the multiset $\{1, 1, 2, 3\}$ in lexicographic order are 1123, 1132, 1213, 1231, 1312, 1321, 2113, 2131, 2311, 3112, 3121, 3211. Here $N = 4! / (2!\,1!\,1!) = 12$.

**Counts.**

| word | multiplicities | $n!$ | $N$ |
|---|---|---|---|
| BANANA | A 3, N 2, B 1 | 720 | 60 |
| MISSISSIPPI | I 4, S 4, P 2, M 1 | 39 916 800 | 34 650 |
| 0000000001 | 0 9, 1 1 | 3 628 800 | 10 |

**Rank.** The lexicographic rank of an arrangement, counted from 0, is the number of arrangements that come before it. At each position $i$, let $R$ be the multiset of the items not yet used, of size $n - i + 1$. For each distinct value $y$ in $R$ with $y < a_i$, the arrangements that agree with $A$ before position $i$ and have $y$ at position $i$ all come before $A$, and there are $N(R) \cdot c_y / (n - i + 1)$ of them, where $c_y$ is the multiplicity of $y$ in $R$ and $N(R)$ is the number of arrangements of $R$. For the arrangements of BANANA in the order A < B < N, the first is AAABNN with rank 0, ANANAB has rank 22, BANANA has rank 34, NABANA has rank 47, and NNBAAA has rank 59.

## Known algorithms

- **[Next permutation](/next-permutation/)** (Knuth's Algorithm L). Start from the non-decreasing arrangement and take lexicographic successors. The tests $a_j < a_{j+1}$ and $a_j < a_l$ must be strict, and then each arrangement appears once. It uses $O(1)$ extra space. It is not CAT for all multisets: for $n - 1$ zeros and one 1, it makes about $n^2$ comparisons for only $n$ arrangements.
- **Backtracking over distinct values.** Fill the positions from left to right, and at each position try each distinct value that is still available. Each leaf is a distinct arrangement, so there are no repeats. The tree can have $\Theta(n)$ nodes per leaf, as for $n - 1$ zeros and one 1.
- **Loopless generation by prefix shifts.** Korsh and LaFollette (2004) gave a loopless array algorithm. Williams (2009) gave the *cool-lex* order, in which each arrangement comes from the one before it by moving one item to the front of a prefix, and a loopless algorithm for it that uses the array, or a linked list, and a constant number of extra variables.
- **Unranking.** Unrank each of $0, \ldots, N - 1$ with the rank formula. This takes $O(n k)$ arithmetic operations per arrangement with $k$ distinct values, so it is slow for listing, but it lets a parallel program split the work.

## Bounds

- **Lower bound.** $\Omega(N)$ time in the visit model, and $\Omega(n N)$ in the copy model.
- **Upper bound.** $O(N)$ total time and $O(1)$ worst-case delay are possible, by the loopless algorithms above. So the problem is solved optimally.
- **Changes per step.** Two distinct arrangements of the same multiset differ in at least two positions. A prefix shift can move many items by one place, but it changes the array by one cut and one insertion in a linked list.
- **Numbers.** $N$ can be exponential in $n$ even with many repeats: with two values of multiplicity $n/2$ each, $N = \binom{n}{n/2} = \Theta(2^n / \sqrt{n})$.

## Reductions

- **From distinct items.** [Generating all permutations](/generating-all-permutations/) is the case $m_1 = \cdots = m_k = 1$, so each algorithm for multisets also solves it.
- **To distinct items, with a filter.** List all $n!$ orders of the labeled items and keep those in which equal items stand in the order of their labels. This is correct but takes $\Omega(n!)$ time, which can be much larger than $N$.
- **From $k$-subsets.** For $k = 2$ values, the problem is the listing of $k$-subsets, and Gray codes for combinations are Gray codes for these arrangements.

## Applications

- **Anagrams.** List the distinct words that use given letters, as in word games.
- **Schedules with identical tasks.** List the distinct orders of jobs when some jobs are identical, so that the search does not test the same schedule twice.
- **Counting and testing.** Test a program on every input sequence with a fixed multiset of values, for example every bit string with a fixed number of ones.
- **Distinct orders of a sequence.** C++ `std::next_permutation` on a sorted sequence with repeats lists each distinct order once.

## References
