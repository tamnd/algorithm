---
tag: N6PVZ9
kind: concept
slug: output-sensitive-matching
name: Output-sensitive matching
aliases:
- output-sensitive pattern matching
- O(n + m + z) matching
area: strings/multiple-pattern-matching
level: core
summary: A matching bound of the form O(n + m + z), where n is the text length, m the total pattern length and z the number of occurrences, so the time pays for each answer once and for nothing else.
prereqs: [multiple-string-matching, asymptotic-notation]
see_also: [aho-corasick, dictionary-suffix-link, failure-link, suffix-tree, document-listing, orthogonal-range-reporting, chan-algorithm]
sources:
  - paper: doi:10.1145/360825.360855
    title: Alfred V. Aho and Margaret J. Corasick, Efficient string matching, an aid to bibliographic search, Communications of the ACM 18(6) (1975), 333-340
    locator: the theorem that the number of state transitions is less than twice the text length, and the cost of the output function
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Section 3.4.6, The full Aho-Corasick algorithm (output links and the O(n + m + k) bound), and Section 7.2 (exact set matching with a suffix tree)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 33, Computational Geometry (the convex hull and its output-sensitive algorithms in the chapter notes)
---

Output-sensitive matching means a running time that depends on the size of the output as well as on the size of the input. For [multiple string matching](/multiple-string-matching/), the standard form is $O(n + m + z)$: linear in the text length $n$, the total pattern length $m$ and the number $z$ of occurrences. A bound in terms of the input alone would have to be $\Theta(nk)$ for $k$ patterns, because the output can be that large; the output-sensitive bound is linear on inputs with few occurrences. The [Aho-Corasick algorithm](/aho-corasick/) reaches it with [dictionary suffix links](/dictionary-suffix-link/).

## In plain words

Some searches have few answers and some have a huge number. If you search a long run of the letter a for the words "a", "aa" and "aaa", almost every position is an answer three times. No method can write a million answers in less time than it takes to write them.

So a fair measure of speed counts two things: the work to read the input, and the work to write the answers. A method is output-sensitive when it spends a fixed amount of work on each input letter and on each answer, and wastes no time on places where nothing is found. Such a method is fast when there are few answers, and as fast as possible when there are many.

## The idea

**The bound.** Write $n = |T|$, $m = \sum_j |P_j|$ and $z = |\mathrm{Occ}(\mathcal{P}, T)|$. An algorithm is output-sensitive in this sense when its time is $O(n + m + z)$, or, after the patterns are preprocessed once, $O(n + z)$ per text. Every algorithm must read the input and write the output, so in the worst case $\Omega(n + m + z)$ is a lower bound in any model where a read or a write costs one step, and an output-sensitive algorithm is optimal up to a constant factor.

**Why the output must appear in the bound.** The output can be much larger than the input.

- For any list of $k$ patterns, $z \le (n + 1)k$, and the patterns $a, a^2, \ldots, a^k$ on the text $a^n$ have $z = \sum_{\ell=1}^{k}(n - \ell + 1) = k(n + 1) - k(k+1)/2$.
- For *distinct nonempty* patterns, the patterns that end at one text position are suffixes of one string with distinct lengths. If $D$ of them end there, their lengths sum to at least $1 + 2 + \cdots + D = D(D+1)/2$, and this is at most $m$, so $D < \sqrt{2m}$. Hence $z < n\sqrt{2m}$.
- The bound $n\sqrt{2m}$ is tight up to a constant: the patterns $a, \ldots, a^L$ have $m = L(L+1)/2$, so $L \approx \sqrt{2m}$, and on $a^n$ they give $z \approx nL$.

So a bound in $n$ and $m$ alone is at least $\Omega(n\sqrt{m})$ for distinct patterns and $\Omega(nk)$ for lists, while most real searches have $z$ much smaller than $n$.

**Where the extra cost hides.** A matcher that finds each end position in $O(1)$ amortized time still has to list the patterns that end there. In a trie with [failure links](/failure-link/), these are the pattern nodes on the failure chain of the current node. Walking the whole chain costs its length, which can be the length of the longest pattern even when no node on it is a pattern. The [dictionary suffix link](/dictionary-suffix-link/) jumps from a node straight to the next pattern node on its chain, so each step of the walk produces at least one occurrence. The reporting cost then becomes $O(1 + z_e)$ at end position $e$, where $z_e$ is the number of occurrences that end there, and $O(n + z)$ in total.

**Other ways to pay for the output.** Copying the output set of $\mathrm{fail}(v)$ into $v$, as the original paper does, also gives $O(n + z)$ search time, but the stored sets can take $\Theta(m^{3/2})$ space. Counting, rather than listing, needs no reporting at all: the number of occurrences of each pattern is a sum of visit counts over its subtree of the failure tree, which takes $O(n + m)$ time whatever $z$ is.

**Output-sensitive does not mean fast in each step.** The bound is amortized over the whole text. One text character can still cause many failure steps, and one end position can have up to $\sqrt{2m}$ occurrences.

## Examples

**Reporting work.** The table counts, for a text $a^{1000}$, the nodes visited by two reporting methods of Aho-Corasick: walking the full failure chain (the root included) after each character, and walking the dictionary links. The number $z$ is the number of occurrences.

| patterns | $z$ | failure-chain visits | dictionary-link visits |
|---|---|---|---|
| $a^{9}b$, b | 0 | 9964 | 0 |
| $a^{49}b$, b | 0 | 48824 | 0 |
| $a, a^2, \ldots, a^{10}$ | 9955 | 10955 | 9955 |
| $a, a^2, \ldots, a^{50}$ | 48775 | 49775 | 48775 |

In the first two rows there is no occurrence, but the failure-chain walk does about $nL$ work, where $L$ is the pattern length, because the current node is $a^{L-1}$ after the first $L - 1$ characters. The dictionary-link walk does none. In the last two rows the output is large, and both methods do work in proportion to it; the failure chain adds one visit of the root per character.

**Counting the output.** For $a, \ldots, a^{10}$ on $a^{1000}$, the value $z = 10 \cdot 1001 - 55 = 9955$ follows from the formula above. Here $m = 55$ and $\sqrt{2m} \approx 10.5$, and at most 10 patterns end at any position, as the bound $D < \sqrt{2m}$ allows.

## Where it is used

- [Aho-Corasick](/aho-corasick/) runs in $O(n + m + z)$ time with [dictionary suffix links](/dictionary-suffix-link/).
- A [suffix tree](/suffix-tree/) answers "where does $P$ occur in $T$" in $O(|P| + \mathrm{occ})$ time after $O(n)$ preprocessing, by listing the leaves below one node.
- [Document listing](/document-listing/) asks for the documents that contain a pattern in time proportional to their number, not to the number of occurrences.
- In geometry, [orthogonal range reporting](/orthogonal-range-reporting/) runs in $O(\log n + k)$ time for $k$ reported points, and [Chan's algorithm](/chan-algorithm/) computes a convex hull in $O(n \log h)$ time for $h$ hull vertices.

## References
