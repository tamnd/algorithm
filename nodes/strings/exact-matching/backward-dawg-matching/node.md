---
tag: YJ949P
kind: algorithm
slug: backward-dawg-matching
name: Backward DAWG matching
aliases:
- BDM
- backward oracle matching
area: strings/exact-matching
level: advanced
summary: Scans windows right to left using a suffix automaton of the reversed pattern; sublinear on average.
solves: [string-matching]
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern, σ: the alphabet size}
  time: {worst: Θ(n m), average: O(n log_σ m / m), best: Θ(n/m), preprocessing: O(m)}
  space: {extra: Θ(m)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [suffix-automaton, string-matching, boyer-moore]
see_also: [boyer-moore-horspool, turbo-boyer-moore, shift-or, knuth-morris-pratt, apostolico-giancarlo, suffix-automaton-size-theorem]
sources:
  - paper: doi:10.1007/BF01185427
    title: M. Crochemore, A. Czumaj, L. Gasieniec, S. Jarominek, T. Lecroq, W. Plandowski and W. Rytter, Speeding up two string-matching algorithms, Algorithmica 12(4-5) (1994), 247-267
    locator: the Reverse Factor algorithm with the suffix automaton of the reversed pattern, its average-case bound O(n log m / m), and Turbo-RF
  - url: http://www-igm.univ-mlv.fr/~lecroq/string/node23.html
    title: Christian Charras and Thierry Lecroq, Exact String Matching Algorithms, 1997
    locator: Reverse Factor algorithm (the use of the smallest suffix automaton of the reversed pattern, the shift from the longest prefix found, the O(mn) worst case, and the optimal average O(n log(m)/m) inspections)
  - book: isbn:9780521813075
    title: Gonzalo Navarro and Mathieu Raffinot, Flexible Pattern Matching in Strings, Cambridge University Press, 2002
    locator: Chapter 2, the factor-based approach (Backward DAWG Matching, BNDM and Backward Oracle Matching)
  - paper: doi:10.1137/0208029
    title: A. C. Yao, The complexity of pattern matching for a random string, SIAM Journal on Computing 8(3) (1979), 368-387
    locator: the lower bound on the average number of text characters any algorithm must inspect
---

Backward DAWG matching solves [string matching](/string-matching/) by reading each window of the text from right to left with the [suffix automaton](/suffix-automaton/) (also called DAWG, directed acyclic word graph) of the reversed pattern. The automaton tells, at each step, whether the part read so far is still a factor of the pattern and whether it is a prefix of the pattern; the scan stops as soon as it is not a factor, and the window moves to the longest prefix of the pattern found. On random text it reads $O(n \log_\sigma m / m)$ characters on average, which matches Yao's lower bound, so it is optimal on average, while its worst case is $\Theta(nm)$.

## In plain words

Boyer-Moore reads a window from its right end and asks whether the letters read are the end of the word. This method asks a weaker question: are the letters read so far a piece of the word anywhere? As long as they are, it keeps reading leftwards. Once they are not, no copy of the word can cover all of them, so the word can jump past the point where reading stopped.

While reading, it also notes each time the letters read are the start of the word. The last such note gives the longest start of the word that ends the window, and the word slides to put its start there.

On random text, a piece of a few letters is rarely part of the word, so the method reads only a few letters per window and jumps almost the whole word length each time.

## The problem

The input is a text $T[0 \ldots n-1]$ and a pattern $P[0 \ldots m-1]$. The analysis uses an integer alphabet of size $\sigma$ with automaton transitions stored in arrays, or a general alphabet with hashed transitions, as in the implementation; only equality of characters matters. Indices are 0-based. The output is every shift $s$, $0 \le s \le n - m$, with $T[s \ldots s+m-1] = P$, in increasing order. Occurrences may overlap. If $m = 0$, every shift $0, \ldots, n$ is output, and if $m > n$, nothing is output.

## The algorithm

Let $P^R$ be the reverse of $P$ and let $\mathcal{A}$ be the suffix automaton of $P^R$, with initial state $q_0$, partial transition function $\delta$ and set $F$ of terminal states. A string $x$ labels a path from $q_0$ exactly when $x$ is a factor of $P^R$, and the path ends in $F$ exactly when $x$ is a suffix of $P^R$. Reading the window from position $s + m - 1$ down to $s + j$ feeds the automaton the string $x = (T[s+j \ldots s+m-1])^R$. So the path exists exactly when $T[s+j \ldots s+m-1]$ is a factor of $P$, and it ends in $F$ exactly when $T[s+j \ldots s+m-1]$ is a prefix of $P$.

```pseudo id=main
BACKWARD-DAWG-MATCHING(T, P)
L1  n ← |T|, m ← |P|
L2  if m = 0 then output 0, 1, …, n and return
L3  (δ, F) ← SUFFIX-AUTOMATON(P reversed)
L4  s ← 0
L5  while s ≤ n − m do
L6      q ← q₀, j ← m, shift ← m
L7      while j > 0 and q ≠ nil do
L8          q ← δ(q, T[s + j − 1]); j ← j − 1          ▷ nil if no transition
L9          if q ≠ nil and q ∈ F then                   ▷ T[s + j .. s + m − 1] is a prefix of P
L10             if j > 0 then shift ← j else output s
L11     s ← s + shift
```

The variable $\mathit{shift}$ holds the smallest $j > 0$ found so far such that $T[s+j \ldots s+m-1]$ is a prefix of $P$, that is the longest proper prefix of $P$ that ends the window. If the scan reaches $j = 0$, the whole window is a factor of $P$ of length $m$, so it equals $P$, and the window is an occurrence. The automaton has at most $2m - 1$ states for $m \ge 2$ and $3m - 4$ transitions for $m \ge 3$ (see the [size theorem](/suffix-automaton-size-theorem/)) and is built in linear time by the online construction.

## Example

Search for $P$ = gcagagag in $T$ = gcatcgcagagagtatacagtacg, with $n = 24$ and $m = 8$, the example of Charras and Lecroq used on the [Boyer-Moore](/boyer-moore/) page.

| $s$ | window | characters read, right to left | prefixes of $P$ found | inspections | shift |
|---|---|---|---|---|---|
| 0 | gcatcgca | a, c, g, c | gca (length 3) | 4 | 5 |
| 5 | gcagagag | g, a, g, a, g, a, c, g | g (length 1), then all 8 | 8 | 7 |
| 12 | gtatacag | g, a, c, a | g (length 1) | 4 | 7 |

At $s = 0$, the strings read are a, ca, gca, cgca as text factors; a and ca are factors of $P$ but not prefixes, gca is a prefix, and cgca is not a factor, so the scan stops after 4 characters and the window moves to align the prefix gca: $s \leftarrow 0 + 5$. At $s = 5$ the whole window is read and is an occurrence; the longest proper prefix seen is g, at $j = 7$. At $s = 12$, the factor acag does not occur in $P$, and the shift is 7. Then $s = 19 > 16$ and the search stops. The output is 5, with 16 text characters inspected, against 17 comparisons for Boyer-Moore and 15 for [Turbo-BM](/turbo-boyer-moore/).

A worst case: for $T = a^{100}$ and $P = a^{10}$, every window is an occurrence, read in full, and the shift is 1, so the search reads $91 \cdot 10 = 910$ characters. A favorable case: for a text of 1000 copies of x and $P$ = abcdefghij, each window stops after one character, x is not a factor, and the shift is 10, for 100 inspections in total.

## Correctness

Two facts make the shift safe. First, let the scan stop at $j$ because $T[s+j \ldots s+m-1]$ is not a factor of $P$. An occurrence starting at $s + d$ with $0 < d \le j$ would contain this whole text factor, which would then be a factor of $P$; so there is none. Second, an occurrence starting at $s + d$ with $j < d < m$ makes $T[s+d \ldots s+m-1]$ a prefix of $P$, and the scan read it and recorded it, so $\mathit{shift} \le d$. Together, no occurrence starts strictly between $s$ and $s + \mathit{shift}$. The full proof is below.

## Complexity

- **Preprocessing.** The suffix automaton of $P^R$ has at most $2m - 1$ states for $m \ge 2$. With transitions in arrays of size $\sigma$ it takes $\Theta(m\sigma)$ time and space; with hashed transitions it takes $O(m)$ expected time and $\Theta(m)$ space.
- **Worst case.** Each window costs at most $m$ inspections and each shift is at least 1, so the search takes $O(nm)$ time. The input $T = a^n$, $P = a^m$ reaches $\Theta(nm)$, as in the example.
- **Average case.** On a text of independent uniform characters over $\sigma \ge 2$ letters, the factors of $P$ of length about $2\log_\sigma m$ are a small fraction of all strings of that length, so a window is read for $O(\log_\sigma m)$ characters on average before the scan leaves the factors, and the shift is at least $m - O(\log_\sigma m)$. Crochemore et al. prove that the expected number of inspections is $O(n \log_\sigma m / m)$. Yao proved that every algorithm must inspect $\Omega(n \log_\sigma m / m)$ characters on average, so the bound is optimal.
- **Best case.** $\Theta(n/m)$ inspections, when each window stops at its last character.
- **Space.** $\Theta(m)$ with hashed transitions.

| claim | value |
|---|---|
| preprocessing | $O(m)$ expected, $\Theta(m\sigma)$ with arrays |
| worst case | $\Theta(nm)$ |
| average, random text | $O(n \log_\sigma m / m)$ inspections |
| best case | $\Theta(n/m)$ |

On a random text of length $10^5$ with a random pattern of length 16, the implementation reads about $0.37n$ characters over 2 letters, $0.18n$ over 4 letters and $0.09n$ over 26 letters.

## Properties

- **Optimal on average.** Its average matches Yao's lower bound, which no Boyer-Moore variant based on suffixes alone achieves for small alphabets.
- **Good on small alphabets.** For DNA, where bad-character shifts are short, the factor test still stops early, because a random string of a few letters is rarely a factor of the pattern.
- **Not online.** It reads each window backwards and needs random access to it.
- **Quadratic worst case.** Without the memory of Turbo-RF, the worst case is $\Theta(nm)$.

## Variants and improvements

- **Turbo-RF.** Crochemore et al. add a memory of the last matched part, like [Turbo-BM](/turbo-boyer-moore/), and get a linear worst case of $O(n)$ while keeping the optimal average.
- **BNDM.** Backward Nondeterministic DAWG Matching, by Navarro and Raffinot, simulates the nondeterministic suffix automaton with bit-parallelism, as [Shift-Or](/shift-or/) does for prefixes. For $m$ up to the word size $w$ it is short and very fast in practice.
- **Backward oracle matching.** BOM, by Allauzen, Crochemore and Raffinot, replaces the suffix automaton by the factor oracle, a smaller automaton with $m + 1$ states that accepts all factors of $P^R$ and some other strings. A rejection still proves that the string is not a factor, so the shift remains safe, but the oracle cannot recognize prefixes, so BOM shifts past the point where the scan stopped. It is among the fastest algorithms for long patterns.
- **Many patterns.** The same idea with an automaton of all reversed patterns gives multiple-pattern variants such as Set BOM.

## When to use it

Use BDM or its bit-parallel form BNDM for patterns of moderate length over small alphabets, such as DNA or protein sequences, and for long patterns in general, when the text is in memory. For short patterns over large alphabets, [Horspool](/boyer-moore-horspool/) is simpler and as fast. If the worst case matters, use Turbo-RF, [Turbo-BM](/turbo-boyer-moore/) or [KMP](/knuth-morris-pratt/).

## Pitfalls

- **Automaton of the pattern instead of its reverse.** The window is read right to left, so the automaton must be built for $P^R$. With the automaton of $P$, the test asks the wrong question and the shifts are wrong. The test `test_automaton_against_definition` checks the automaton on all binary words up to length 6.
- **Shifting past an occurrence.** When the scan reaches $j = 0$, the shift must be the last proper prefix found, not $m$, or overlapping occurrences are missed. The test `test_edges` searches $a^4$ in $a^{10}$ and expects 7 occurrences.
- **Recording the full window as a prefix.** At $j = 0$ the terminal state means an occurrence, not a shift of 0; a shift of 0 makes the loop run forever. Line L10 separates the two cases, and `test_random_against_oracle` runs many periodic inputs over the alphabet a.
- **Terminal states.** Terminal states are those on the suffix-link path from the last state; marking only the last state recognizes only the whole pattern, and the shifts become $m$. The test `test_random_against_oracle` compares every output with the naive search.

## Implementations

## History

The Reverse Factor algorithm was introduced by Crochemore, Czumaj, Gasieniec, Jarominek, Lecroq, Plandowski and Rytter; the journal paper "Speeding up two string-matching algorithms" appeared in Algorithmica in 1994, together with Turbo-RF and [Turbo-BM](/turbo-boyer-moore/). It was the first practical algorithm to reach the average bound that Yao had proved optimal in 1979. Under the name Backward DAWG Matching it became the base of the factor-based family described in Navarro and Raffinot's book: BNDM, which they introduced with bit-parallelism, and Backward Oracle Matching, based on the factor oracle of Allauzen, Crochemore and Raffinot (1999).

## References
