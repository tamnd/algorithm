---
tag: N6YEV5
kind: problem
slug: count-distinct-substrings
name: Counting distinct substrings
aliases:
- number of distinct substrings
area: strings/suffix-structures
level: core
summary: Count the distinct substrings of a string, using the suffix array and LCP array.
model: word-ram
complexity:
  vars: {n: the length of the string}
  time: {worst: Θ(n)}
prereqs: [suffix-array, lcp-array, suffix]
see_also: [lcp-array, suffix-automaton, suffix-tree, kasai-algorithm, subword-complexity, longest-repeated-substring, element-distinctness]
sources:
  - url: https://cp-algorithms.com/string/suffix-array.html
    title: cp-algorithms, Suffix Array
    locator: section Number of different substrings
  - url: https://cp-algorithms.com/string/suffix-automaton.html
    title: cp-algorithms, Suffix Automaton
    locator: section Number of different substrings
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 5 (suffix trees, where each substring is the path label of a point on the tree) and Section 7.14 (suffix arrays and the Lcp values)
---

Counting distinct substrings is the problem of finding how many different strings occur as contiguous substrings of a given string $T$ of length $n$. A string has $n(n+1)/2$ nonempty substring occurrences, but many can be equal. Each distinct substring is a prefix of a [suffix](/suffix/), so the answer is $n(n+1)/2 - \sum_i LCP[i]$, where $LCP$ is the [LCP array](/lcp-array/) of the [suffix array](/suffix-array/). This gives a $\Theta(n)$ solution for an integer alphabet, and the [suffix automaton](/suffix-automaton/) and the [suffix tree](/suffix-tree/) give the same count by other formulas.

## In plain words

A word of six letters has 21 pieces of consecutive letters: six of length one, five of length two, and so on. Some pieces are copies of each other. In "banana", the piece "ana" occurs twice and "a" occurs three times. The question is how many different pieces there are.

Every piece is the start of some ending of the word. Sort all endings. Each ending brings as many new pieces as it has letters, minus the letters it shares at the start with the ending just above it in the sorted list, because those shorter pieces were already counted there. So the answer is the number of all pieces minus the sum of the shared counts.

## Definition

**Input.** A string $T = T[0 \ldots n-1]$, $n \ge 0$, over an alphabet. For the suffix array method the alphabet is ordered; indices are 0-based and no sentinel is appended.

**Output.** The number

$$d(T) = \bigl|\{\, T[i \ldots j-1] : 0 \le i < j \le n \,\}\bigr|,$$

the number of distinct nonempty substrings. Some sources count the empty string too, which adds 1.

**The formula.** Let $SA$ be the suffix array of $T$, with suffixes $T_p = T[p \ldots n-1]$, and let $LCP[0] = 0$ and $LCP[i] = \mathrm{lcp}(T_{SA[i-1]}, T_{SA[i]})$. Then

$$d(T) = \sum_{i=0}^{n-1} \bigl( (n - SA[i]) - LCP[i] \bigr) = \frac{n(n+1)}{2} - \sum_{i=0}^{n-1} LCP[i].$$

*Proof.* Each nonempty substring is a nonempty prefix of at least one suffix. Assign each distinct substring $u$ to the suffix of smallest rank that starts with $u$. The suffix $S_i = T_{SA[i]}$ has $n - SA[i]$ nonempty prefixes. Its prefix of length $k$ is assigned to a smaller rank exactly when some $S_j$ with $j < i$ starts with it, that is, when $k \le \max_{j < i} \mathrm{lcp}(S_j, S_i)$. By the [LCP-RMQ reduction](/lcp-rmq-reduction/), $\mathrm{lcp}(S_j, S_i) = \min LCP[j+1 \ldots i] \le LCP[i]$, with equality for $j = i - 1$, so the maximum is $LCP[i]$ (and 0 for $i = 0$). So $S_i$ gets exactly $(n - SA[i]) - LCP[i]$ substrings, its prefixes of lengths $LCP[i] + 1$ to $n - SA[i]$. The sum over $i$ counts each distinct substring once. Since $\{SA[i]\}$ is $\{0, \ldots, n-1\}$, $\sum_i (n - SA[i]) = n + (n-1) + \cdots + 1 = n(n+1)/2$. $\square$

## Variants

- **With the empty string.** Add 1.
- **Of a fixed length $k$.** The number of distinct substrings of length $k$ is the number of ranks $i$ with $n - SA[i] \ge k$ and ($i = 0$ or $LCP[i] < k$). The sequence of these numbers for $k = 1, 2, \ldots$ is the [subword complexity](/subword-complexity/) of $T$.
- **The $k$-th distinct substring in lexicographic order.** The substrings assigned to rank $i$ come before those of rank $i + 1$ in lexicographic order, so prefix sums of $(n - SA[i]) - LCP[i]$ and one binary search find it in $O(\log n)$ time.
- **Online.** Count after each appended symbol. The suffix automaton gives each new count in amortized $O(1)$ time, for a constant alphabet: appending a symbol adds $len(cur) - len(link(cur))$ new substrings.
- **Several strings.** Count the distinct substrings of a set of strings with a [generalized suffix automaton](/generalized-suffix-automaton/) or a [generalized suffix tree](/generalized-suffix-tree/).
- **Substrings of a range.** Count the distinct substrings of $T[l \ldots r]$ for many query ranges. This is much harder, and the methods above do not answer it directly.

## Examples

| $T$ | $n$ | $\sum LCP$ | $d(T)$ | distinct substrings of length $1, 2, \ldots, n$ |
|---|---|---|---|---|
| `banana` | 6 | 6 | 15 | 3, 3, 3, 3, 2, 1 |
| `mississippi` | 11 | 13 | 53 | 4, 7, 7, 7, 7, 6, 5, 4, 3, 2, 1 |
| `abcd` | 4 | 0 | 10 | 4, 3, 2, 1 |
| `aaaaa` | 5 | 10 | 5 | 1, 1, 1, 1, 1 |
| `abababab` | 8 | 21 | 15 | 2, 2, 2, 2, 2, 2, 2, 1 |

The derivation for `banana`, with $SA = [5, 3, 1, 0, 4, 2]$ and $LCP = [0, 1, 3, 0, 0, 2]$:

| rank $i$ | suffix | $n - SA[i]$ | $LCP[i]$ | new substrings |
|---|---|---|---|---|
| 0 | a | 1 | 0 | a |
| 1 | ana | 3 | 1 | an, ana |
| 2 | anana | 5 | 3 | anan, anana |
| 3 | banana | 6 | 0 | b, ba, ban, bana, banan, banana |
| 4 | na | 2 | 0 | n, na |
| 5 | nana | 4 | 2 | nan, nana |

The new counts are $1 + 2 + 2 + 6 + 2 + 2 = 15$. The [suffix automaton](/suffix-automaton/) of `banana` has 10 states, and the sum of $len(v) - len(link(v))$ over its 9 states other than the root is also 15.

**Extremes.** For each string of length $n$, $n \le d(T) \le n(n+1)/2$ when $n \ge 1$ and there is at least one symbol. The lower bound is reached by $\texttt{a}^n$, where each length has one substring. The upper bound is reached exactly when all $n$ symbols are different: then all substrings are different, and if two symbols are equal, two substrings of length 1 are equal.

## Known algorithms

| method | time | notes |
|---|---|---|
| put all substrings in a hash set | $\Theta(n^3)$ expected (with string hashing of each substring), $O(n^2)$ expected with rolling hashes | simple check for small $n$; hashes can collide |
| suffix array and [LCP array](/lcp-array/) | $O(n)$ for an integer alphabet, plus $O(n \log n)$ for sorting a general ordered alphabet | build $SA$, then [Kasai's algorithm](/kasai-algorithm/), then the formula |
| [suffix automaton](/suffix-automaton/) | $O(n \log \sigma)$ with sorted transition maps | $d(T) = \sum_{v \ne root} (len(v) - len(link(v)))$; also online |
| [suffix tree](/suffix-tree/) of $T$ without sentinel | $O(n)$ for an integer alphabet | $d(T)$ is the sum of the lengths of the edge labels, since each point on an edge is one substring; with a sentinel, subtract 1 for each of the leaf edges that end with it |

The suffix automaton formula holds because the substrings in one state $v$ are the suffixes of its longest string with lengths from $len(link(v)) + 1$ to $len(v)$, and each substring is in exactly one state.

## Bounds

- **Upper bound.** $O(n)$ time in the [word RAM](/word-ram/) for an integer alphabet $\{0, \ldots, n^{O(1)}\}$, with a linear [suffix array construction](/suffix-array-construction/).
- **Lower bound for an integer alphabet.** $\Omega(n)$, since each symbol must be read: changing an unread symbol to a new symbol changes the count.
- **Lower bound for a general ordered alphabet.** $\Omega(n \log n)$ comparisons. All symbols of $T$ are different if and only if $d(T) = n(n+1)/2$, so [element distinctness](/element-distinctness/) reduces to this problem in $O(n)$ time, and element distinctness needs $\Omega(n \log n)$ comparisons. So the $O(n \log n)$ method with a comparison sort is optimal in the [comparison model](/comparison-model/).
- **The answer can be large.** $d(T)$ is up to $n(n+1)/2$, which needs about $2 \log_2 n$ binary digits. In fixed-width integer arithmetic, $n > 92681$ makes $n(n+1)/2$ larger than $2^{32}$.

## Reductions

- **To LCP array construction.** The count is one sum over the [LCP array](/lcp-array/), in $O(n)$ time.
- **From element distinctness.** As above, so the problem is at least as hard as element distinctness in the comparison model.
- **Of the longest repeated substring.** Both problems read the same arrays. The [longest repeated substring](/longest-repeated-substring/) is the maximum of the LCP array, and the count uses its sum.

## Applications

- A measure of the complexity or variety of a sequence, for example of a DNA region: a low count shows repeats.
- The [subword complexity](/subword-complexity/) of words in combinatorics on words, such as the [Sturmian words](/sturmian-word/), which have exactly $k + 1$ factors of each length $k$.
- A standard test case for suffix structures in programming contests, and the check that a suffix automaton or suffix array implementation is right.
- Ranking and unranking substrings in lexicographic order.

## References
