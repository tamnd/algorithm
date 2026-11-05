---
tag: 5GPQXM
kind: problem
slug: block-edit-distance
name: Block edit distance
aliases:
- edit distance with moves
area: strings/approximate-matching
level: advanced
summary: Edit distance in which whole blocks of text may be moved as a single operation.
prereqs: [edit-distance, edit-operations, np-complete]
see_also: [edit-distance, sorting-by-reversals, lz77, delta-encoding, suffix-tree, matching-statistics, longest-common-subsequence, metric-space]
sources:
  - paper: doi:10.1145/357401.357404
    title: Walter F. Tichy, The string-to-string correction problem with block moves, ACM Transactions on Computer Systems 2(4), 1984
    locator: pages 309 to 321 (the block move model, the minimal covering set of common substrings, and its computation by the longest match at each position)
  - paper: doi:10.1016/S0304-3975(96)00268-X
    title: Daniel P. Lopresti and Andrew Tomkins, Block edit models for approximate string matching, Theoretical Computer Science 181(1), 1997
    locator: pages 159 to 179 (the family of block edit models by coverage and overlap, the NP-complete variants and the polynomial ones)
  - paper: doi:10.1016/j.jda.2005.01.010
    title: Dana Shapira and James A. Storer, Edit distance with move operations, Journal of Discrete Algorithms 5(2), 2007
    locator: pages 380 to 392 (NP-completeness of the distance with character insertions, deletions and substring moves, and a greedy approximation)
  - paper: "Graham Cormode and S. Muthukrishnan, The string edit distance matching problem with moves, ACM Transactions on Algorithms 3(1), 2007 (conference version in SODA 2002)"
    locator: the near-linear deterministic algorithm with approximation factor O(log n log* n) for the edit distance with moves, and its use for matching a pattern in a text
  - paper: doi:10.37236/1947
    title: Avraham Goldstein, Petr Kolman and Jie Zheng, Minimum common string partition problem, hardness and approximations, Electronic Journal of Combinatorics 12, 2005
    locator: article R50 (NP-hardness and APX-hardness of the problem with at most two occurrences of each letter, and the 1.1037 and 4 approximations)
---

The block edit distance is a family of string distances in which one operation can move, copy or delete a whole substring, in addition to the single-character [edit operations](/edit-operations/). The best-known member is the edit distance with moves: the least number of character insertions, deletions and substitutions and substring moves that turn one string into another. Moves let the distance see that two documents hold the same paragraphs in another order, which the plain [edit distance](/edit-distance/) charges at the full length of the moved text. Most versions are [NP-complete](/np-complete/), while the copy model of Tichy has an exact greedy solution in linear time.

## In plain words

The usual edit distance changes one letter at a time. If someone swaps the two halves of a long text, the usual distance is large, because it must delete one half and type it again elsewhere. Yet a person sees one simple change: a block moved.

A block edit distance allows such a move as one step. It counts the fewest steps that turn the first string into the second, where a step is a change of one letter or the move of a whole piece of text.

This distance fits documents and programs, where people move paragraphs and functions around. The price is speed: for most versions, no fast exact method is known, and there are good reasons to think none exists. Fast methods give an answer that is close to the true value within a known factor.

## Definition

Strings are over a finite alphabet $\Sigma$, and indices are 0-based. All operations cost 1. For a string $S$ of length $n$, the operations are:

- a character insertion, deletion or substitution, as in the Levenshtein model;
- a substring move: for $0 \le a < b \le n$ and a position $c$ in $S' = S[0..a)\,S[b..n)$, replace $S$ by $S'[0..c)\,S[a..b)\,S'[c..n - b + a)$.

The **edit distance with moves** $d_{\mathrm{mv}}(S, T)$ is the least number of operations that turn $S$ into $T$. Each operation has an inverse operation of the same cost (a move back, an insertion for a deletion), so $d_{\mathrm{mv}}$ is symmetric, and it is a metric on $\Sigma^*$. The output is a number, not a list of positions. In the matching version of Cormode and Muthukrishnan, the input is a pattern $P$ and a text $T$, and the output gives, for each end position $j$ of $T$, the least distance between $P$ and a substring of $T$ that ends at $j$.

**Tichy's copy model.** Given a source $S$ and a target $T$, write $T$ as a concatenation $T = t_1 t_2 \cdots t_r$ in which each piece $t_i$ is a non-empty substring of $S$ (a copy) or a single symbol (an add). The cost is the number $r$ of pieces. A substring of $S$ can be copied any number of times, and parts of $S$ can be left out.

**Common partition.** When $S$ and $T$ have the same multiset of symbols, a common partition is a split of $S$ into blocks $S = B_1 \cdots B_p$ such that some order of the same blocks gives $T$. The minimum common string partition problem asks for the least $p$.

## Variants

- **Moves without substitutions.** Shapira and Storer study insertions, deletions and moves only. A substitution costs at most 2 in that model.
- **Moves only.** For two strings with the same multiset of symbols, count only substring moves. This version is tied to the common partition, as the reductions section shows.
- **Coverage and overlap.** Lopresti and Tomkins classify block edit models by whether the blocks must cover each string completely and whether blocks may overlap. Some combinations are polynomial and others NP-complete.
- **Copies, block deletions and reversals.** Other models allow a block to be copied, deleted or reversed in one step. With reversals of blocks and no other operation on a permutation, the problem becomes [sorting by reversals](/sorting-by-reversals/).

## Examples

| $S$ | $T$ | Levenshtein | with moves | common partition |
|---|---|---|---|---|
| abcde | cdeab | 4 | 1 | 2 blocks: ab, cde |
| abcdef | defabc | 6 | 1 | 2 blocks: abc, def |
| ab | ba | 2 | 1 | 2 blocks: a, b |
| abcd | dcba | 4 | 3 | 4 blocks |

In the first row, one move of $\texttt{ab}$ to the end gives $\texttt{cdeab}$, while the Levenshtein distance must delete and insert two letters, or substitute four. The last row is the worst case for moves: no two neighbouring letters of $\texttt{abcd}$ stay neighbours in the same order, so every common partition has 4 blocks, and 3 moves are needed.

In the copy model with $S = \texttt{abcdef}$ and $T = \texttt{defabcabcdef}$, the longest match at each position gives $T = \texttt{def} \cdot \texttt{abc} \cdot \texttt{abcdef}$, three copies, while $\operatorname{ed}(S, T) = 6$. A target such as $\texttt{defabcxdef}$ needs an add for the symbol $\texttt{x}$, which does not occur in $S$: $\texttt{def} \cdot \texttt{abc} \cdot \texttt{x} \cdot \texttt{def}$, cost 4.

## Known algorithms

| problem | method | result | source |
|---|---|---|---|
| copy model | longest match at each position, with a [suffix tree](/suffix-tree/) of $S$ | exact, $O(\lvert S \rvert + \lvert T \rvert)$ time for a constant alphabet | Tichy 1984 |
| edit distance with moves | edit sensitive parsing, an embedding into $L_1$ | factor $O(\log n \log^* n)$, near-linear time, deterministic | Cormode and Muthukrishnan |
| insertions, deletions, moves | greedy on longest common substrings | factor $O(\log n)$ on a subclass of the inputs | Shapira and Storer |
| common partition, at most 2 copies of each letter | | factor 1.1037 | Goldstein, Kolman and Zheng |
| common partition, at most 3 copies of each letter | | factor 4, linear time | Goldstein, Kolman and Zheng |

**Why the greedy copy parse is exact.** Let $F$ be the set of the non-empty substrings of $S$ and the single symbols. A substring of a member of $F$ is again in $F$. Let $0 = g_0 < g_1 < \cdots$ be the cut points of the greedy parse, where $g_{i+1}$ is the largest end with $T[g_i..g_{i+1}) \in F$, and let $0 = o_0 < o_1 < \cdots < o_r = |T|$ be the cut points of any parse. Induction on $i$ shows $g_i \ge o_i$: if $o_{i+1} \le g_i$ then $g_{i+1} > g_i \ge o_{i+1}$, and else $T[g_i..o_{i+1})$ is a substring of the piece $T[o_i..o_{i+1}) \in F$, so it is in $F$ and the greedy choice gives $g_{i+1} \ge o_{i+1}$. So the greedy parse ends after at most $r$ pieces. The longest match at each position of $T$ is a [matching statistic](/matching-statistics/), and a suffix tree of $S$ gives all of them in linear time.

## Bounds

- Shapira and Storer proved that deciding $d \le m$ for the distance with character insertions, deletions and substring moves is NP-complete.
- Lopresti and Tomkins proved several of their block edit models NP-complete, and gave polynomial algorithms for the rest.
- Goldstein, Kolman and Zheng proved the minimum common string partition NP-hard and APX-hard, even when each letter occurs at most twice in each string. So it has no polynomial-time approximation scheme unless P = NP.
- Tichy's copy model is in P: the greedy parse is exact and runs in linear time for a constant alphabet.

## Reductions

**Moves and common partitions.** Let $S$ and $T$ have the same multiset of symbols, let $p$ be the size of a minimum common partition, and let $x$ be the least number of substring moves that turn $S$ into $T$. Then

$$\frac{p - 1}{3} \le x \le p - 1.$$

For the upper bound, take a common partition $S = B_1 \cdots B_p$ and $T = B_{\pi(1)} \cdots B_{\pi(p)}$. For $i = 1$ to $p - 1$, move the block $B_{\pi(i)}$ to the position right after the blocks placed before it. After $p - 1$ moves the first $p - 1$ blocks of $T$ are in place, and the last block is the only one left, so it is in place too. For the lower bound, label each symbol with its position in $S$. A move cuts the current string at most at three points: the two ends of the block and the place where it goes. So if the current string is a concatenation of $q$ runs of consecutive positions of $S$, after a move it is a concatenation of at most $q + 3$ such runs. After $x$ moves, $T$ is a concatenation of at most $3x + 1$ runs, and these runs form a common partition, so $p \le 3x + 1$. A constant-factor approximation for one problem is therefore one for the other.

**Compression.** The greedy copy parse of $T$ against $S$ is a parse in the style of [LZ77](/lz77/), with $S$ as the dictionary instead of the text before the current position.

## Applications

- **File differences.** The copy model describes the deltas of a version control system: a new version is stored as copies from the old one plus added text. See [delta encoding](/delta-encoding/).
- **Documents and code.** Plagiarism detection and the comparison of program versions must not charge a moved paragraph or function at its full length.
- **Genomes.** Rearrangements move, copy and reverse long segments of DNA, and the minimum common string partition is a model of them.
- **Near neighbours.** The embedding of Cormode and Muthukrishnan maps strings to vectors in $L_1$, so indexes for vector distances can search strings by the distance with moves, up to the approximation factor.

## References
