---
tag: PB06E3
kind: algorithm
slug: most-popular-completion
name: Most popular completion
aliases:
- popularity-based query completion
- MostPopularCompletion
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: core
summary: Suggests the past queries that extend the prefix with the highest log frequency, found by a top-k search in a scored trie.
solves: [query-auto-completion]
model: word-ram
complexity:
  vars: {m: the length of the prefix, k: the number of completions, L: the length of the longest logged query}
  time: {expected: O(m + k L log(k L))}
  space: {extra: O(k L)}
properties: {deterministic: true, recursive: false}
history:
  year: 2011
  people: [Ziv Bar-Yossef, Naama Kraus]
  note: Bar-Yossef and Kraus named MostPopularCompletion as the standard baseline of query auto-completion in 2011; Hsu and Ottaviano gave compact tries for its top-k search in 2013.
prereqs: [query-auto-completion, trie, priority-queue]
see_also: [top-k-selection, radix-tree, ternary-search-tree, range-minimum-query, cartesian-tree, binary-search, noisy-channel-spelling-correction, maximum-likelihood-estimation]
sources:
  - paper: doi:10.1145/1963405.1963424
    title: Ziv Bar-Yossef and Naama Kraus, Context-sensitive query auto-completion, Proceedings of the 20th International Conference on World Wide Web (WWW 2011), 107-116
    locator: the definition of MostPopularCompletion as the maximum likelihood estimate of the next query from the frequencies in the log, used as the baseline of the context-sensitive methods NearestCompletion and HybridCompletion
  - paper: doi:10.1145/2488388.2488440
    title: Bo-June (Paul) Hsu and Giuseppe Ottaviano, Space-efficient data structures for top-k completion, Proceedings of the 22nd International Conference on World Wide Web (WWW 2013), 583-594
    locator: the Completion Trie, with the children of each node sorted by score and a best-first search on a priority queue, and the RMQ Trie and the Score-Decomposed Trie; the measured times of about a microsecond per completion
  - paper: doi:10.1561/1500000055
    title: Fei Cai and Maarten de Rijke, A survey of query auto completion in information retrieval, Foundations and Trends in Information Retrieval 10(4), 273-363, 2016
    locator: the chapters on popularity-based methods (heuristic and learned), on time-sensitive and user-sensitive methods, and on efficiency
  - paper: "Simon Gog, Giulio Ermanno Pibiri and Rossano Venturini, Efficient and effective query auto-completion, Proceedings of the 43rd International ACM SIGIR Conference (SIGIR 2020), arXiv:2005.06213"
    locator: the top-k completions of a prefix as the k smallest values in a lexicographic range of the sorted log, found by range minimum queries
---

Most popular completion is the method that answers a typed prefix with the $k$ past queries that start with it and were issued most often. Bar-Yossef and Kraus named it MostPopularCompletion in 2011 and showed that it is the maximum likelihood choice when the next query is assumed to follow the frequencies of the log. This page gives the fast top-$k$ search in a [trie](/trie/) whose nodes store the largest count below them, the idea of the Completion Trie of Hsu and Ottaviano. The trie page covers the plain data structure, and [query auto-completion](/query-auto-completion/) covers the problem and the methods that use context, time or the user.

## In plain words

A search engine remembers every query that people typed and how many times. When you have typed "bin", it looks at all the remembered queries that begin with "bin" and shows the few that were typed most often. The trick is to do this fast without looking at every query. The engine keeps the queries in a tree of letters, where each branch remembers the highest count of any query further down it. It then always follows the branch with the best remembered count, so it walks straight to the most popular queries and skips the branches that cannot win.

## The problem

The log is a map from queries to counts: each query $q$ is a non-empty string and its count $c(q) \ge 1$ is the number of times it was issued. For a prefix $p$ and an integer $k \ge 0$, return the queries $q$ with $p$ as a prefix, ordered by count descending, then by the query string ascending, and keep the first $k$. The tie rule makes the answer unique. If $P(q \mid p)$ is estimated by $c(q)$ divided by the total count of the queries that start with $p$, this order is the order of the estimated probability, so the answer is the maximum likelihood top $k$.

## The algorithm

Build a trie over the log. Each node $x$ stores the count of the query that ends at it (0 if none), $\mathrm{best}(x)$, the largest count in its subtree, and $\mathrm{pre}(x)$, its preorder number in a traversal that visits children in character order, so that preorder numbers sort like the strings. The children of each node are kept sorted by $(-\mathrm{best}, \mathrm{pre})$. The search is best-first on a [priority queue](/priority-queue/) of nodes and finished queries, with the key $(-\mathrm{best}, \mathrm{pre}, \text{kind})$, where a finished query has kind 0 and a node kind 1:

```pseudo id=main
MOST-POPULAR(T, p, k)          ▷ T: the scored trie of the log
L1  s ← root of T
L2  for each character a of p:
L3      if s has no child a then return the empty list
L4      s ← child a of s
L5  H ← heap with the node entry of s
L6  out ← empty list
L7  while H is not empty and |out| < k:
L8      e ← pop the entry with the smallest key from H
L9      if e is a finished query q then append (q, c(q)) to out; continue
L10     x ← the node of e
L11     if a query q ends at x then push q with key (−c(q), pre(x), 0)
L12     push the first child y of x with key (−best(y), pre(y), 1)
L13     if x ≠ s then push the next sibling z of x with key (−best(z), pre(z), 1)
L14 return out
```

Lines L12 and L13 follow the first-child and next-sibling links, so each node is pushed once, and a node is only expanded when its best count can still beat every entry in the heap. Building the trie takes one pass over the log to insert the queries and update $\mathrm{best}$ along each path, one traversal for the preorder numbers, and one sort of the children of each node.

## Example

Take a log of seven queries:

| query | count |
|---|---|
| bing | 80 |
| binary search | 50 |
| bm25 | 40 |
| binary search tree | 30 |
| bin packing | 25 |
| bit manipulation | 20 |
| binomial heap | 15 |

For the prefix "bin" and $k = 3$, lines L1 to L4 walk down to the node of "bin", whose best count is 80. Its children in the order of their best counts are "g" (80), "a" (50), " " (25) and "o" (15). The search pops "bin", then "bing" and its finished query, so "bing" (80) is the first answer. Next it expands the ten nodes of "binary search", one character at a time, because their best count 50 is larger than anything else in the heap, and returns "binary search" (50). The node of "binary search" still has the best count 30 below it, so the five nodes of " tree" come next and give "binary search tree" (30). The answer is bing, binary search, binary search tree. The search popped 17 nodes, the nodes on the three paths, and never entered "bin packing" or "binomial heap": their best counts 25 and 15 stayed in the heap behind the answers. For the prefix "bi" and $k = 5$ the answer adds bin packing (25) and bit manipulation (20); "bm25" does not start with "bi".

## Correctness

The file proofs/correctness.md gives the proof. Preorder numbers in character order sort the nodes like their strings, so the key order of finished queries is the tie order of the problem. The first-child and next-sibling links make a tree over the subtree of $s$ in which the keys of nodes grow from parent to successor, because a child cannot have a larger best count than its parent and a later sibling comes later in the sorted order. So when a query is popped, no query with a smaller key can still be hidden below an entry in the heap: that entry would have a smaller key than the popped one. The finished queries therefore leave the heap in the tie order, and the first $k$ of them are the answer.

## Complexity

Every node that the search pops lies on the path from $s$ to one of the returned queries. A node with a best count above the $k$-th answer has a winner below it, and a node with the same best count but a smaller string either is a prefix of the $k$-th answer or holds only smaller strings, which are returned. So at most $\min(k, n_p)(L - m + 1)$ nodes are popped, where $n_p$ is the number of queries with the prefix, and each pop pushes at most three entries. With hash tables for the children, the walk down the prefix costs $O(m)$ expected time and the search $O(kL \log(kL))$, with $O(kL)$ extra space for the heap. Building the trie costs $O(T \log \sigma)$ time for a log with $T$ characters in total and at most $\sigma$ children per node, and the trie has at most $T + 1$ nodes. The baseline that filters and sorts the whole log costs $O(nL + n \log n)$ time for each prefix, for $n$ logged queries.

## Properties

- **Exact.** The answer is the exact top $k$ of the log under the tie rule, not an approximation.
- **Output-sensitive.** The work depends on $k$ and on the length of the answers, not on the number of queries with the prefix.
- **Static scores.** The counts are fixed when the trie is built. A change of one count changes $\mathrm{best}$ on the whole path to the root and the order of siblings along it.
- **Deterministic.** Equal logs and prefixes give equal answers.

## Variants and improvements

- **Compact tries.** Hsu and Ottaviano store the Completion Trie with path compression, as in a [radix tree](/radix-tree/), and compress the scores; they report about a microsecond per completion with space competitive with gzip of the log. Their Score-Decomposed Trie and RMQ Trie are other layouts with the same output.
- **Sorted array and range minimum queries.** Sort the queries; the queries with a given prefix form one range, found by [binary search](/binary-search/). The top $k$ of a range come from a [range minimum query](/range-minimum-query/) structure over the negated counts: take the minimum, split the range around it, and keep the parts in a heap. Gog, Pibiri and Venturini build their system on this idea.
- **Precomputed lists.** Store the top $k$ answers at every node, or at every node near the root. A lookup is then a walk down the prefix, at the cost of $k$ entries for each stored node.
- **Time-sensitive counts.** Replace raw counts with counts that decay with age, or with counts predicted for the next hours, so that new and seasonal queries rise. Cai and de Rijke survey these methods.
- **Context and personal history.** Bar-Yossef and Kraus rerank the popular candidates by their similarity to the previous queries of the session (NearestCompletion), and combine the two scores (HybridCompletion).
- **Fuzzy prefixes.** Allow a few edits in the prefix, so that a typo in the first letters does not hide the right completions. See [noisy channel spelling correction](/noisy-channel-spelling-correction/) for a model of the errors.

## When to use it

Use most popular completion as the first method for any query box with a large log, and as the baseline against which context-aware or learned methods are measured. It needs only counts, it is exact and fast, and for short prefixes the most frequent queries are usually good guesses. It is weak for rare prefixes with few logged queries, for new events that the log has not seen often yet, and when the same prefix means different things to different users.

## Pitfalls

- **Ties.** Many queries share a count, especially rare ones. Without a tie rule the shown list can change from one build to the next.
- **Unsafe and private queries.** A raw log contains queries that should not be suggested, such as offensive text or personal data. Filter the log before building the trie.
- **Stale counts.** Counts over a long period favour old queries. Use a time window or decay.
- **Updates.** Raising one count can reorder siblings on the whole path to the root. Batch the updates and rebuild, or use a structure built for updates.
- **Normalization.** Decide on case, spaces and Unicode forms before counting, or the counts of one query split over several strings.
- **Very short prefixes.** For one letter the answers are the global top queries, which are the same for everyone and often not useful. Many systems show nothing until a few letters are typed.

## Implementations

## History

Query suggestion from logs was part of web search engines before the research papers named the method. Bar-Yossef and Kraus defined MostPopularCompletion in 2011 as the maximum likelihood estimator from the log and used it as the baseline for context-sensitive completion. Hsu and Ottaviano studied the data structures for the top-$k$ search in 2013 and gave three compact tries. Gog, Pibiri and Venturini returned to the efficiency question in 2020 with an index built on range minimum queries. Cai and de Rijke surveyed the field in 2016.

## References
