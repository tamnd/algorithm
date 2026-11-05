---
tag: 23D20Y
kind: problem
slug: multiple-string-matching
name: Multiple string matching
aliases:
- multi-pattern matching
- exact set matching
- multiple pattern matching
area: strings/multiple-pattern-matching
level: core
summary: Find all occurrences in a text of each pattern from a given finite set.
model: word-ram
complexity:
  vars: {n: the length of the text, m: the total length of the patterns, z: the number of occurrences}
  time: {worst: Θ(n + m + z)}
prereqs: [string-matching, alphabet]
see_also: [aho-corasick, dictionary-matching, commentz-walter, set-horspool, wu-manber, karp-rabin-multiple-patterns, output-sensitive-matching, two-dimensional-dictionary-matching]
sources:
  - paper: doi:10.1145/360825.360855
    title: Alfred V. Aho and Margaret J. Corasick, Efficient string matching, an aid to bibliographic search, Communications of the ACM 18(6) (1975), 333-340
    locator: the problem statement and the main theorem on the number of state transitions
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Section 3.4, Exact matching with a set of patterns, Section 3.5, Three applications of exact set matching, and Section 7.2, APL2, Suffix trees and the exact set matching problem
  - book: isbn:9780521813075
    title: Gonzalo Navarro and Mathieu Raffinot, Flexible Pattern Matching in Strings, Cambridge University Press, 2002
    locator: Chapter 3, Multiple string matching (prefix-, suffix- and factor-based approaches and the experimental map)
  - paper: doi:10.1016/j.tcs.2004.03.058
    title: Gonzalo Navarro and Kimmo Fredriksson, Average complexity of exact and approximate multiple string matching, Theoretical Computer Science 321(2-3) (2004), 283-290
    locator: the average-case lower bound for exact multiple string matching on random text
---

Multiple string matching is the problem of finding every occurrence in a text of every pattern from a finite set. With a text of length $n$, patterns of total length $m$ and $z$ occurrences, it is solved in $\Theta(n + m + z)$ time on the [word RAM](/word-ram/) for a constant or integer alphabet, by the [Aho-Corasick algorithm](/aho-corasick/), and this bound is optimal. It generalizes [string matching](/string-matching/) from one pattern to many, and it is the core of keyword search, virus scanning and network intrusion detection.

## In plain words

You have a long text and a list of words. You want every place where any of the words appears, and which word it is. One place can hold several answers: the word "she" also contains "he", and both count.

The simple method searches for each word on its own, which reads the text once for each word. Good methods read the text only once for the whole list, or skip parts of it. Their time grows with the length of the text, the total length of the words and the number of answers, but not with the number of words.

## Definition

**Alphabet.** An [alphabet](/alphabet/) $\Sigma$ of size $\sigma$, in one of the models of [string matching](/string-matching/): general (equality tests only), ordered (comparisons) or integer ($\Sigma = \{0, \ldots, \sigma - 1\}$, characters may index arrays).

**Input.** A text $T = T[0 \ldots n-1] \in \Sigma^n$ and a finite list of patterns $\mathcal{P} = (P_0, \ldots, P_{k-1})$ with $P_j \in \Sigma^*$. Write $m = \sum_{j} |P_j|$ for the total length, and $\ell_{\min}$ and $\ell_{\max}$ for the shortest and the longest pattern length. Indices are 0-based.

**Output.** The set of occurrences

$$\mathrm{Occ}(\mathcal{P}, T) = \{\, (s, j) : 0 \le j < k,\ 0 \le s \le n - |P_j|,\ T[s \ldots s + |P_j| - 1] = P_j \,\},$$

and $z = |\mathrm{Occ}(\mathcal{P}, T)|$.

**Conventions.**

- Occurrences may overlap, and one may lie inside another, whether they are of the same pattern or of different patterns.
- If a pattern occurs twice in the list, under the indices $j \ne j'$, each occurrence is reported once for $j$ and once for $j'$. Most authors assume distinct patterns; the definition above also covers lists.
- An empty pattern occurs at each $s$ from $0$ to $n$.
- The order of the output is free. Algorithms that read the text from left to right usually report by increasing end position $s + |P_j|$.

The size $z$ can be large: $z \le (n + 1)k$, and the patterns $a, a^2, \ldots, a^k$ on the text $a^n$ give $z = \sum_{\ell=1}^{k} (n - \ell + 1)$, which is about $kn$ for $k \ll n$. So a bound must contain $z$, or the problem must ask for less output.

## Variants

- **Decision.** Does any pattern occur? The answer is one bit, so $z$ drops out of the bound.
- **First occurrence.** Return the occurrence with the least end position, as a scanner that stops at the first hit does.
- **Counting.** Return, for each pattern, the number of its occurrences. With the [failure tree](/failure-link/) of the Aho-Corasick trie, this takes $O(n + m)$ time, independent of $z$.
- **Leftmost-longest, non-overlapping.** Scan from left to right; at each position take the longest pattern that starts there, skip past it, and continue. Tokenizers and "replace all" functions use this rule, and regular expression engines use a similar leftmost-first rule for an alternation.
- **Dictionary matching.** The set is fixed and preprocessed once, then many texts are searched. This is [dictionary matching](/dictionary-matching/); when patterns are inserted and deleted, it is [dynamic dictionary matching](/dynamic-dictionary-matching/).
- **Indexed text.** The text is fixed and preprocessed, and the patterns come later. A [suffix tree](/suffix-tree/) or [suffix array](/suffix-array/) of the text then answers each pattern in time that depends on its length and its number of occurrences.
- **Equal lengths.** All patterns have the same length $\ell$. Then a hash of each text window of length $\ell$ can be looked up in a table: see [Karp-Rabin for many patterns](/karp-rabin-multiple-patterns/).
- **Two dimensions.** The text and the patterns are matrices: [two-dimensional dictionary matching](/two-dimensional-dictionary-matching/).
- **Approximate.** An occurrence may have a few errors: see [approximate dictionary lookup](/approximate-dictionary-lookup/) and the [k-mismatch problem](/k-mismatch-problem/).

## Examples

| text | patterns $(P_0, P_1, \ldots)$ | occurrences $(s, j)$ | $z$ |
|---|---|---|---|
| ushers | he, she, his, hers | (1, 1), (2, 0), (2, 3) | 3 |
| aaaa | a, aa | (0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0) | 7 |
| abab | ab, ab, b | (0, 0), (0, 1), (1, 2), (2, 0), (2, 1), (3, 2) | 6 |
| banana | an, ana, nan, x | (1, 0), (1, 1), (2, 2), (3, 0), (3, 1) | 5 |
| abc | the empty string | (0, 0), (1, 0), (2, 0), (3, 0) | 4 |

In ushers, she at 1 and he at 2 end at the same position, and he at 2 is a prefix of hers at 2. In banana, the two occurrences of ana overlap, and nan at 2 overlaps both. The pattern x does not occur, so it adds nothing to $z$. The third row lists ab twice, so each of its occurrences counts twice.

**The leftmost-longest variant.** On banana with the same patterns, the scan finds no pattern at 0, takes ana at 1 (longer than an), jumps to 4, and finds nothing more. Its output is the one occurrence (1, 1), while the full problem has five.

## Known algorithms

- **One search per pattern.** Run [Knuth-Morris-Pratt](/knuth-morris-pratt/) for each pattern: $O(kn + m)$ time. Good only for very few patterns.
- **[Aho-Corasick](/aho-corasick/).** A [trie](/trie/) with [failure links](/failure-link/) and [dictionary suffix links](/dictionary-suffix-link/): $O(n + m + z)$ time with $O(1)$ child lookups, which is optimal in the worst case. It reads each text character once.
- **[Commentz-Walter](/commentz-walter/).** A Boyer-Moore style scan with a trie of the reversed patterns. It skips text on average when $\ell_{\min}$ is large, but its worst case is $O(n \ell_{\max})$ in its basic form.
- **[Set Horspool](/set-horspool/).** The same trie of reversed patterns, with the Horspool shift of the last window character. Simple and fast for few patterns over a large alphabet.
- **[Wu-Manber](/wu-manber/).** Shifts by blocks of $B$ characters with a [block shift table](/block-shift-table/) and checks candidates through a hash table. Fast in practice for many long patterns.
- **[Karp-Rabin with many patterns](/karp-rabin-multiple-patterns/).** Rolling hashes of the text windows looked up in a table of pattern hashes, for patterns of equal length: $O(n + m)$ expected time when the occurrences are few.
- **Bit-parallel methods.** [Shift-Or](/shift-or/) extends to several short patterns packed into one machine word.
- **Index of the text.** A [generalized suffix tree](/generalized-suffix-tree/) or a suffix tree of the text gives $O(n + m + z)$ time as well, with a larger constant and more memory.

## Bounds

**Worst-case lower bound.** Each algorithm must write $z$ pairs. It must read all of each pattern in the worst case, because a change to any character of a pattern can change the output for some text. For the text, the case of one pattern is a special case, and every algorithm for one pattern of length $\ell$ reads at least $n - \ell + 1$ text characters in the worst case (Rivest's bound; see the [string matching lower bound](/string-matching-lower-bound/)). So the worst-case time is $\Omega(n + m + z)$ when $n \ge 2\ell_{\min}$, in any model where reading a character costs one step.

**Upper bound.** Aho-Corasick meets this bound for an integer alphabet with an array per node, after $O(m\sigma)$ setup, and in expected time with hash tables. With balanced search trees for the children, the bound is $O((n + m)\log \sigma + z)$.

**Average case.** On a uniformly random text over $\sigma$ characters and $r$ random patterns of the same length $\ell$, Navarro and Fredriksson proved that each algorithm must examine $\Omega(n \log_\sigma(r\ell)/\ell)$ text characters on average. This extends Yao's bound $\Omega(n \log_\sigma \ell / \ell)$ for one pattern. Aho-Corasick reads every text character, so for long patterns it is far from this bound, and the skipping algorithms of this area aim at it.

## Reductions

- **From single string matching.** One pattern is a set of size 1, so each lower bound of [string matching](/string-matching/) applies.
- **To single string matching.** Run a single-pattern algorithm $k$ times: $O(kn + m)$ time. This is linear only for a constant number of patterns.
- **To matching in an index.** Build a suffix tree of $T$ in $O(n)$ time for an integer alphabet, then search each $P_j$ in $O(|P_j| + z_j)$ time, where $z_j$ is its number of occurrences. The total is $O(n + m + z)$.
- **Equal lengths by padding is wrong.** Patterns of different lengths cannot be padded to one length, because the padding characters would have to match the text. The reduction to equal lengths instead takes the prefix of length $\ell_{\min}$ of each pattern as a filter and verifies each candidate, as Wu-Manber does.

## Applications

- **Keyword search.** `grep -F` with many fixed strings, and bibliographic search, the original motivation of Aho and Corasick.
- **Security.** Virus scanners match files against databases of byte signatures, and network intrusion detection systems match packet payloads against thousands of rule strings.
- **Biology.** Search a genome for many primers, probes or motifs at once.
- **Text processing.** Find all dictionary words in a text, build a tokenizer by the leftmost-longest rule, and censor a list of words.
- **Two-dimensional matching.** The rows of a matrix pattern are a set of strings; the [Bird-Baker](/bird-baker/) method matches them with Aho-Corasick.

## References
