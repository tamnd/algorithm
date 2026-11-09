---
tag: WVNB8N
kind: problem
slug: combinatorial-ranking-and-unranking
name: Ranking and unranking combinations
aliases:
- combination rank
- index of a combination
- combination unranking
area: combinatorics/generating-combinations
level: core
summary: Map a k-subset to its index in a fixed order and back again.
complexity:
  vars: {n: the size of the ground set, k: the size of each subset}
  time: {worst: O(n)}
prereqs: [combinatorial-number-system, lexicographic-order]
see_also: [combinatorial-number-system, colexicographic-order, lexicographic-combinations, ranking-unranking, permutation-ranking, uniform-random-subset, enumerative-coding, revolving-door-ordering]
sources:
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration, and Search, CRC Press, 1999
    locator: Chapter 2, Section 2.3, k-element subsets (rank and unrank in lexicographic, co-lex and minimal change order)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.2.1.3, Generating all combinations (Theorem L and the combinatorial number system, and the alternating combinatorial number system for the revolving-door order)
  - paper: doi:10.1016/j.disc.2007.11.048
    title: Frank Ruskey and Aaron Williams, The coolest way to generate combinations, Discrete Mathematics 309(17), 2009, 5305-5320
    locator: Section 3, ranking in cool-lex order (Theorem 2)
---

Ranking a combination means computing its position in a fixed list of all $k$-subsets of an $n$-set. Unranking means the inverse: given a position $r$ with $0 \le r < C(n, k)$, compute the subset at that position. For lexicographic, colexicographic and revolving door order, the rank is a short sum of binomial coefficients, so both maps take $O(k)$ arithmetic operations for ranking and $O(n)$ for unranking, with a table of binomials. The basic tool is the [combinatorial number system](/combinatorial-number-system/).

## In plain words

Write every team of $k$ players from $n$ in a long list, in some fixed order. The *rank* of a team is its line number in the list, counted from $0$. Ranking asks: on which line is this team? Unranking asks: which team is on line $r$?

You do not need to write the list. You can count how many teams come before a given team, group by group, with binomial coefficients. You can also go the other way and build the team on line $r$ one player at a time. With these two maps, one number can stand for one team.

## Definition

Let $\binom{[n]}{k}$ be the set of $k$-subsets of $[n] = \{1, \ldots, n\}$, let $N = C(n, k)$, and let $\prec$ be a total order on $\binom{[n]}{k}$.

**Ranking.** Input: $n$, $k$ and a subset $S \in \binom{[n]}{k}$. Output: $\mathrm{rank}(S) = |\{T : T \prec S\}|$.

**Unranking.** Input: $n$, $k$ and an integer $r$ with $0 \le r < N$. Output: the subset $S$ with $\mathrm{rank}(S) = r$.

So rank is a bijection from $\binom{[n]}{k}$ to $\{0, \ldots, N-1\}$ and unrank is its inverse. The order $\prec$ is part of the problem. This is the case of $k$-subsets of the general [ranking and unranking](/ranking-unranking/) problem.

**Cost model.** Count arithmetic operations on integers up to $N$. These integers have up to $\log_2 N \le n$ bits, so for large $n$ each operation is a [big integer](/big-integer/) operation.

## Variants

- **Colexicographic order.** With $0$-based elements $c_1 < \cdots < c_k$, the rank is $\sum_{i=1}^{k} \binom{c_i}{i}$. It does not depend on $n$. See [colexicographic order](/colexicographic-order/).
- **Lexicographic order.** With $1$-based elements $a_1 < \cdots < a_k$ in $[n]$, the rank is
$$\mathrm{rank}_{\text{lex}}(a) = \binom{n}{k} - 1 - \sum_{i=1}^{k} \binom{n - a_i}{k - i + 1}.$$
The map $a \mapsto n + 1 - a$ turns lexicographic order into reversed colex order, and this formula follows from the colex formula.
- **Revolving door order.** With $0$-based elements $c_1 < \cdots < c_k$, the rank is
$$\binom{c_k + 1}{k} - \binom{c_{k-1} + 1}{k - 1} + \cdots + (-1)^{k-1} \binom{c_1 + 1}{1} - [k \text{ odd}].$$
Knuth calls this the alternating combinatorial number system. See [revolving door ordering](/revolving-door-ordering/).
- **Cool-lex order.** Ruskey and Williams give a rank formula with one binomial for each element, see [cool-lex order](/cool-lex-order/).
- **Other objects.** Subsets in binary counting order have the rank $\sum_{j \in S} 2^{j-1}$. Permutations have the Lehmer code, see [permutation ranking](/permutation-ranking/) and [permutation unranking](/permutation-unranking/). Multisets reduce to subsets, see Reductions.

## Examples

**One set in four orders.** Take $n = 5$, $k = 3$ and $S = \{2, 4, 5\}$, which is $\{1, 3, 4\}$ in $0$-based form.

| order | the list of the $10$ subsets, $1$-based | rank of $\{2, 4, 5\}$ | formula |
| --- | --- | --- | --- |
| lexicographic | $123, 124, 125, 134, 135, 145, 234, 235, 245, 345$ | $8$ | $9 - \binom{3}{3} - \binom{1}{2} - \binom{0}{1} = 8$ |
| colex | $123, 124, 134, 234, 125, 135, 235, 145, 245, 345$ | $8$ | $\binom{4}{3} + \binom{3}{2} + \binom{1}{1} = 8$ |
| revolving door | $123, 134, 234, 124, 145, 245, 345, 135, 235, 125$ | $5$ | $\binom{5}{3} - \binom{4}{2} + \binom{2}{1} - 1 = 5$ |
| cool-lex | $123, 234, 134, 124, 235, 135, 245, 345, 145, 125$ | $6$ | see [cool-lex order](/cool-lex-order/) |

**Lexicographic rank of $\{1, 3, 4\}$.** $9 - \binom{4}{3} - \binom{2}{2} - \binom{1}{1} = 9 - 4 - 1 - 1 = 3$. The list above has $134$ at position $3$.

**Unranking in colex order.** To find the $3$-subset with colex rank $72$: the largest $c$ with $\binom{c}{3} \le 72$ is $8$, the rest is $16$; the largest $c$ with $\binom{c}{2} \le 16$ is $6$, the rest is $1$; then $c_1 = 1$. So the subset is $\{1, 6, 8\}$ in $0$-based form.

**Lexicographic unranking.** To find the lexicographic subset of rank $r$ of $\binom{[n]}{k}$, choose $a_1$ as the least value $v$ such that the subsets that start with a value up to $v$ number more than $r$. The subsets that start with $v$ number $\binom{n - v}{k - 1}$. Subtract the counts of the skipped values from $r$ and go on with $a_2$. For $n = 5$, $k = 3$ and $r = 8$: the counts for $v = 1, 2$ are $6$ and $3$. Since $8 \ge 6$, skip $v = 1$, and $r$ becomes $2$. Since $2 < 3$, $a_1 = 2$. Then in $\{3, 4, 5\}$ with $k = 2$, the counts are $2$ for $v = 3$ and $1$ for $v = 4$, so $a_2 = 4$ with $r = 0$, and $a_3 = 5$. The answer is $\{2, 4, 5\}$.

## Known algorithms

| task | order | method | operations |
| --- | --- | --- | --- |
| rank | colex | sum of $\binom{c_i}{i}$ | $O(k)$ with a binomial table |
| unrank | colex | greedy, one downward scan | $O(n)$ |
| unrank | colex | greedy, binary search for each digit | $O(k \log n)$ |
| rank | lexicographic | mirror, then colex | $O(k)$ |
| unrank | lexicographic | one forward scan over the values | $O(n)$ |
| rank and unrank | revolving door | alternating sum | $O(k)$ and $O(n)$ |
| rank | cool-lex | Ruskey and Williams formula | $O(k)$ |

A table of $\binom{i}{j}$ for $0 \le i \le n$ and $0 \le j \le k$ takes $O(nk)$ time and space, by [Pascal's triangle](/pascal-triangle-dp/). Without the table, each binomial can be updated from the last one with one multiplication and one division as the scan moves by one step.

## Bounds

- **Input and output size.** Ranking must read the $k$ elements, so it needs $\Omega(k)$ time. The rank has $\lceil \log_2 N \rceil$ bits, which is $\Theta(k \log(n/k))$ for $k \le n/2$, so with big integers the output alone costs that many bit operations.
- **Information.** Since rank is a bijection onto $\{0, \ldots, N-1\}$, it is an optimal code for $k$-subsets: no code of fewer than $\lceil \log_2 N \rceil$ bits can tell all $N$ subsets apart.
- **Upper bounds.** The algorithms in the table above take $O(k)$ operations for ranking and $O(n)$ for unranking on the word RAM when $N$ fits in a word.

## Reductions

- **Lexicographic to colex.** The map $a \mapsto n + 1 - a$ followed by $r \mapsto N - 1 - r$ turns one problem into the other.
- **Complement.** The map $S \mapsto [n] \setminus S$ turns the colex order of $k$-subsets into the reverse colex order of $(n - k)$-subsets, so $\mathrm{rank}_k(S) = N - 1 - \mathrm{rank}_{n-k}([n] \setminus S)$.
- **Multisets.** A $k$-multiset $b_1 \le \cdots \le b_k$ of $[n]$ maps to the $k$-subset $\{b_i + i - 1\}$ of $[n + k - 1]$, and the map keeps the lexicographic order. So ranking [combinations with repetition](/combinations-with-repetition/) reduces to ranking subsets.
- **Generation.** Unranking each $r = 0, \ldots, N-1$ solves [k-subset enumeration](/k-subset-enumeration/), but with $O(n)$ operations for each subset, not $O(1)$.

## Applications

- **Random sampling.** Unrank a uniform random integer below $N$ to get a [uniform random subset](/uniform-random-subset/) of size $k$.
- **Parallel and resumable enumeration.** Unrank the start of each block of ranks to split a listing among workers, or to restart a long listing from a saved number.
- **Table lookup.** Use the rank as an index into an array with one entry for each subset, for example a precomputed table of poker hands, with $C(52, 5) = 2598960$ entries.
- **Compression.** [Enumerative coding](/enumerative-coding/) and the [RRR bit vector](/rrr-bitvector/) store a block of bits as its weight and its rank among the blocks of that weight.

## References
