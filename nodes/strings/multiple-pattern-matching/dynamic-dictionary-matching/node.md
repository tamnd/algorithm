---
tag: KP5SEV
kind: problem
slug: dynamic-dictionary-matching
name: Dynamic dictionary matching
aliases:
- Amir-Farach dynamic dictionary matching
area: strings/multiple-pattern-matching
level: research
summary: Dictionary matching where patterns can be inserted and deleted over time.
model: word-ram
complexity:
  vars: {n: the length of a query text, ℓ: the total length of the dictionary, p: the length of the pattern inserted or deleted, z: the number of occurrences in the text}
  time: {update: O(p), search: O(n + z)}
  space: {extra: O(ℓ)}
prereqs: [dictionary-matching, aho-corasick]
see_also: [suffix-tree, generalized-suffix-tree, decomposable-searching-problem, global-rebuilding, karp-rabin-multiple-patterns, bird-baker, two-dimensional-dictionary-matching, compressed-suffix-tree]
sources:
  - paper: doi:10.1016/S0022-0000(05)80047-9
    title: Amihood Amir, Martin Farach, Zvi Galil, Raffaele Giancarlo and Kunsoo Park, Dynamic dictionary matching, Journal of Computer and System Sciences 49(2) (1994), 208-222
    locator: the problem statement with insertion and deletion of patterns, and the algorithm based on a suffix tree of the dictionary with a logarithmic slowdown
  - paper: doi:10.1016/0304-3975(94)90176-7
    title: Ramana M. Idury and Alejandro A. Schäffer, Dynamic dictionary matching with failure functions, Theoretical Computer Science 131(2) (1994), 295-310
    locator: the dynamic version of the Aho-Corasick automaton
  - paper: doi:10.1006/inco.1995.1090
    title: Amihood Amir, Martin Farach, Ramana M. Idury, Johannes A. La Poutré and Alejandro A. Schäffer, Improved dynamic dictionary matching, Information and Computation 119(2) (1995), 258-282
    locator: the automaton with separate goto and report transitions, and its O(log ℓ / log log ℓ) slowdown for updates and for scanning
  - paper: doi:10.1109/SFCS.1996.548491
    title: Süleyman Cenk Sahinalp and Uzi Vishkin, Efficient approximate and dynamic matching of patterns using a labeling paradigm, Proceedings of the 37th IEEE Symposium on Foundations of Computer Science (1996), 320-328
    locator: the dynamic dictionary matching result with no slowdown (linear preprocessing, linear text scan, updates in time proportional to the pattern)
  - url: https://arxiv.org/abs/1302.0072
    title: Shoshana Marcus and Dina Sokol, Dynamic 2D dictionary matching in small space, arXiv 1302.0072 (2013)
    locator: Section 2, 1D dynamic dictionary matching (a survey of the one-dimensional results and their slowdowns)
  - paper: doi:10.1016/0196-6774(80)90015-2
    title: Jon Louis Bentley and James B. Saxe, Decomposable searching problems I, Static-to-dynamic transformation, Journal of Algorithms 1(4) (1980), 301-358
    locator: the binary transformation of a static structure for a decomposable searching problem into a structure with insertions
---

Dynamic dictionary matching is [dictionary matching](/dictionary-matching/) in which the dictionary changes: patterns are inserted and deleted between searches, and each search reports all occurrences of the patterns that are in the dictionary at that time. Rebuilding an [Aho-Corasick](/aho-corasick/) automaton after each change costs time proportional to the whole dictionary, so the aim is an update time proportional to the changed pattern and a search time proportional to the text and the output. Amir, Farach, Galil, Giancarlo and Park stated the problem and solved it with a logarithmic slowdown, and Sahinalp and Vishkin removed the slowdown.

## In plain words

A virus scanner or a spam filter has a list of words to look for, and the list changes every day: new words come in, and old ones go out. Each new file must be searched for the words that are in the list at that moment.

You could rebuild the whole search machine after each change, but if the list is long and changes often, that is slow. Dynamic dictionary matching asks for a machine that can take in a new word, or let go of an old one, with work that depends only on the length of that word, while each search stays as fast as with a fixed list.

## Definition

**Data.** A dictionary $D$ of patterns, each a string over an alphabet $\Sigma$ with an identifier $j$. Patterns may repeat under different identifiers. $\ell$ is the total length of the patterns in $D$.

**Operations.**

- $\mathrm{INSERT}(j, P)$ adds the pattern $P$ with the new identifier $j$.
- $\mathrm{DELETE}(j)$ removes the pattern with identifier $j$.
- $\mathrm{SEARCH}(T)$ returns all pairs $(s, j)$ with $P_j$ in $D$ and $T[s \ldots s + |P_j| - 1] = P_j$.

**Conventions.** Indices are 0-based, and occurrences may overlap. A pattern present under two identifiers is reported once for each. The empty pattern occurs at every $s$ in $0, \ldots, n$, where $n = |T|$. The alphabet model is part of each result: the algorithms based on suffix trees and tries need either an ordered alphabet with a $\log \sigma$ factor for branching or hashed transitions with expected bounds.

**Costs.** The time of an update is measured in terms of the length $p$ of the inserted or deleted pattern and the size $\ell$ of the dictionary, and the time of a search in terms of $n$, $z$ and $\ell$. A *slowdown* of $f(\ell)$ means a factor $f(\ell)$ over the static targets: $O(p\, f(\ell))$ for an update and $O((n + z) f(\ell))$ for a search, or with $f(\ell)$ on $n$ alone.

## Variants

- **Insertions only.** The semi-dynamic problem, which the [static-to-dynamic transformation](/decomposable-searching-problem/) of Bentley and Saxe solves from any static structure.
- **Adaptive dictionary matching.** Amir and Farach (1991) gave the first algorithm for a dictionary that changes, under this name.
- **Succinct or compressed dictionaries.** The structure must take space close to the entropy of the dictionary; see [compressed suffix trees](/compressed-suffix-tree/).
- **Two dimensions.** The patterns and the text are matrices, and patterns come and go: the dynamic form of [two-dimensional dictionary matching](/two-dimensional-dictionary-matching/).
- **Approximate patterns.** Sahinalp and Vishkin treat approximate and dynamic matching in the same framework.

## Examples

Start from an empty dictionary and run these operations. The search results are the pairs $(s, j)$ in increasing order.

| step | operation | dictionary after the step | result |
|---|---|---|---|
| 1 | INSERT(0, he) | he | |
| 2 | INSERT(1, she) | he, she | |
| 3 | SEARCH(ushers) | | (1, 1), (2, 0) |
| 4 | INSERT(2, his) | he, she, his | |
| 5 | INSERT(3, hers) | he, she, his, hers | |
| 6 | SEARCH(ushers) | | (1, 1), (2, 0), (2, 3) |
| 7 | INSERT(4, she) | he, she, his, hers, she | |
| 8 | SEARCH(shishe) | | (1, 2), (3, 1), (3, 4), (4, 0) |
| 9 | DELETE(0) | she, his, hers, she | |
| 10 | SEARCH(ushers) | | (1, 1), (1, 4), (2, 3) |
| 11 | INSERT(5, ε) | she, his, hers, she, ε | |
| 12 | SEARCH(she) | | (0, 1), (0, 4), (0, 5), (1, 5), (2, 5), (3, 5) |

Step 8 shows overlapping occurrences: his at 1 and she at 3 share the character at index 3, and he at 4 is a suffix of she at 3. Steps 8 and 10 report the pattern she twice, once under each identifier. Step 12 reports the empty pattern at the four positions 0 to 3 of a text of length 3.

**The logarithmic method on these steps.** Keep the patterns in static Aho-Corasick blocks whose numbers of patterns are distinct powers of 2. An insertion makes a block of one pattern and merges equal blocks, as in adding 1 to a binary counter. After steps 1, 2, 4, 5 and 7 the block sizes are $[1]$, $[2]$, $[2, 1]$, $[4]$ and $[4, 1]$. A search runs the text through each block and joins the outputs. Step 9 rebuilds the block of 4 without he, which leaves $[3, 1]$.

## Known algorithms

- **Rebuild after each update.** Keep one [Aho-Corasick](/aho-corasick/) automaton and rebuild it after each change: $O(\ell)$ time per update with hashed transitions, $O(n + z)$ per search. Best when searches are many and updates rare.
- **Logarithmic method (Bentley and Saxe).** Dictionary matching is a [decomposable searching problem](/decomposable-searching-problem/): the answer for $D_1 \cup D_2$ is the union of the answers. Keep blocks of $2^i$ patterns, each with its own automaton, at most $\lfloor \log_2 k \rfloor + 1$ blocks for $k$ patterns. A pattern is rebuilt at most once per level, so an insertion costs $O(p \log k)$ amortized time, and a search costs $O(n \log k + z)$. A deletion rebuilds the block of the pattern, which can cost $O(\ell)$; [global rebuilding](/global-rebuilding/) spreads such costs.
- **Fingerprints by length.** For each distinct pattern length $L$, keep a [hash table](/hash-table/) of the fingerprints of the patterns of length $L$, and scan the text with a rolling hash for each length, as in [Karp-Rabin for many patterns](/karp-rabin-multiple-patterns/). An update costs $O(p)$ expected time. A search costs $O(n \lambda + z)$ expected time for $\lambda$ distinct lengths, with a small chance of false matches unless each match is verified.
- **Suffix trees (Amir and Farach; Amir, Farach, Galil, Giancarlo and Park).** Store the dictionary in a [generalized suffix tree](/generalized-suffix-tree/) and mark the nodes that are whole patterns. Walking the text through the tree with suffix links finds, for each position $s$, the longest prefix of $T[s \ldots n-1]$ that occurs in the dictionary; the patterns that start at $s$ are the marked prefixes of this match, found by marked-ancestor queries. Updates insert or delete the suffixes of one pattern. Marcus and Sokol summarize the cost as an $O(\log \ell)$ slowdown.
- **Dynamic Aho-Corasick (Idury and Schäffer).** A dynamic form of the automaton, built in linear time, with extra time for updates and for scanning.
- **Separate goto and report structures (Amir, Farach, Idury, La Poutré and Schäffer).** An automaton that stores the goto transitions and the report links separately, with an $O(\log \ell / \log \log \ell)$ slowdown for updates and for scanning.
- **Naming and cores (Sahinalp and Vishkin).** Each pattern gets a hierarchy of names, and its main core aligns with the core of every text substring that matches it, so the text is filtered to few candidate positions. Preprocessing is linear in the dictionary, a search is linear in the text, and an update takes time proportional to the pattern: no slowdown.
- **Compressed and succinct structures.** Chan, Hon, Lam and Sadakane make a compressed suffix tree dynamic, with an $O(\log^2 \ell)$ slowdown. Hon, Lam, Shah, Tam and Vitter use space within the $k$-th order entropy of the dictionary plus lower-order terms, with updates in $O(p \log \sigma + \log \ell)$ time and searches in $O(n \log \ell + z)$ time.

## Bounds

- **Search.** A search needs $\Omega(n + z)$ time in the worst case. The output has $z$ pairs, and if the dictionary holds one pattern of length 1, then every text position must be read, since changing an unread character changes the output.
- **Update.** An insertion needs $\Omega(p)$ time: if it does not read some character of $P$, two patterns that differ only there leave the same structure, and a search with a text equal to one of them gives a wrong answer for the other.
- **Optimality.** The result of Sahinalp and Vishkin meets both lower bounds, the targets that Aho and Corasick set for the static problem, as Marcus and Sokol note.
- **Trade-offs of simple methods.** Rebuilding pays $\Theta(\ell)$ per update for an optimal search; the logarithmic method pays a $\log k$ factor on both sides; fingerprints pay a factor $\lambda$ on the search.

## Reductions

- **From static dictionary matching.** Insert the patterns one by one, then search: a dynamic structure solves the static problem with the same total cost.
- **To decomposable searching.** The union property makes every static structure dynamic for insertions, at a logarithmic cost, by the Bentley-Saxe transformation.
- **Two dimensions to one.** The [Bird-Baker](/bird-baker/) method turns two-dimensional dictionary matching of patterns of one width into two one-dimensional dictionary problems, the rows and the columns of row names. Marcus and Sokol replace both by the dynamic structure of Sahinalp and Vishkin and obtain dynamic two-dimensional dictionary matching with no slowdown.

## Applications

- **Signature scanners.** Virus scanners and intrusion detection systems match traffic or files against sets of signatures that are added and removed over time.
- **Filters and alerts.** Text streams are checked against a changing set of keywords, such as watched names or blocked terms.
- **Two-dimensional data.** Dynamic sets of image patterns, through the reduction above.

## References
