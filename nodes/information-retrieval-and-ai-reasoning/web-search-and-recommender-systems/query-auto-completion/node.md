---
tag: VPH702
kind: problem
slug: query-auto-completion
name: Query auto-completion
aliases:
- query autocompletion
- type-ahead search
- QAC
- search suggestions
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: core
summary: Given a typed prefix, suggest the k most likely complete queries in a few milliseconds.
prereqs: [trie, top-k-selection]
see_also: [most-popular-completion, radix-tree, ternary-search-tree, range-minimum-query, cartesian-tree, mean-reciprocal-rank, noisy-channel-spelling-correction, levenshtein-automaton]
sources:
  - paper: doi:10.1145/1963405.1963424
    title: Ziv Bar-Yossef and Naama Kraus, Context-sensitive query auto-completion, Proceedings of the 20th International Conference on World Wide Web (WWW 2011), 107-116
    locator: the definition of MostPopularCompletion as the maximum likelihood estimate from the log, the context-sensitive methods NearestCompletion and HybridCompletion, and the automatic evaluation by weighted MRR on the public AOL query log
  - paper: doi:10.1561/1500000055
    title: Fei Cai and Maarten de Rijke, A survey of query auto completion in information retrieval, Foundations and Trends in Information Retrieval 10(4), 273-363, 2016
    locator: the chapters on popularity-based methods (heuristic and learned), on time-sensitive and user-sensitive methods, and on efficiency
  - paper: doi:10.1145/2488388.2488440
    title: Bo-June (Paul) Hsu and Giuseppe Ottaviano, Space-efficient data structures for top-k completion, Proceedings of the 22nd International Conference on World Wide Web (WWW 2013), 583-594
    locator: the top-k completion problem over a scored string set, the Completion Trie, the RMQ Trie and the Score-Decomposed Trie, and the measured times of about a microsecond per completion
  - paper: "Simon Gog, Giulio Ermanno Pibiri and Rossano Venturini, Efficient and effective query auto-completion, Proceedings of the 43rd International ACM SIGIR Conference (SIGIR 2020), arXiv:2005.06213"
    locator: the efficiency requirements of a deployed completion service at eBay, and the top-k completions of a prefix as the k smallest values in a lexicographic range of the sorted log, found by range minimum queries
---

Query auto-completion is the problem of suggesting, after each key press in a search box, a short ranked list of complete queries that start with what the user has typed so far. It has two parts: a quality part, which is to rank the candidates by how likely the user is to want each one, and a speed part, which is to find the top $k$ among millions of logged queries within the time of one key press. The basic method, [most popular completion](/most-popular-completion/), ranks by log frequency with a [trie](/trie/) and has its own page; this page states the problem, the ways to measure it, and the methods that add context, time or tolerance to typing errors.

## In plain words

When you type "bin" into a search box, the box shows a few full queries, such as "bing" or "binary search", so that you can pick one instead of typing the rest. The engine has to guess what you want from a few letters. The usual guess uses what other people searched for most often, and a better guess also looks at what you searched for a minute ago, what time it is, or where you are. The engine must make this guess again after every letter, and it must answer before you type the next one, so the search among all past queries has to be very fast. A good list puts the query that you want near the top, early in your typing.

## Definition

The input is:

- a set $Q$ of candidate queries, usually the distinct queries of a log, each with a score such as its count;
- a prefix $p$, the text typed so far, and optionally a context $x$: the earlier queries of the session, the user, the time, the place;
- a small number $k$ of suggestions, such as 10.

The output is a list $L = (q_1, \ldots, q_k)$ of distinct candidates that each have $p$ as a prefix. If $q^*$ is the query the user finally submits, a list is good when $q^*$ appears in it at a high place. Two measures are common:

- **Reciprocal rank.** $1/i$ if $q^* = q_i$, and 0 if $q^*$ is not in the list. Its mean over test cases is [mean reciprocal rank](/mean-reciprocal-rank/) (MRR). Bar-Yossef and Kraus use a weighted form of MRR.
- **Success at $k$.** 1 if $q^*$ is in the list, else 0.

With a model $P(q \mid p, x)$ of the intended query, the expected reciprocal rank of a list is $\sum_{i=1}^{k} P(q_i \mid p, x)/i$. The weights $1/i$ decrease, so by the rearrangement inequality this sum is largest for the $k$ most probable candidates sorted by probability, and the same list also maximizes the expected success at $k$. The problem therefore splits into estimating $P(q \mid p, x)$ and finding the top $k$ under it fast. Most popular completion is the case where $x$ is ignored and $P$ is the maximum likelihood estimate from the counts.

The speed part is the **top-$k$ completion problem** of Hsu and Ottaviano: given a set of strings with scores, return the $k$ highest scored strings that start with $p$. It runs once per key press for every user, so it must answer within a few milliseconds.

## Variants

- **Context-sensitive completion.** Rerank the candidates by their similarity to the earlier queries of the session. Bar-Yossef and Kraus call this NearestCompletion and its mix with popularity HybridCompletion.
- **Time-sensitive completion.** Weigh recent queries more, or predict the counts of the coming hours, so that news and seasonal queries rise fast (Cai and de Rijke).
- **Personalized completion.** Use the history, profile or location of the user (Cai and de Rijke).
- **Learned ranking.** Generate candidates by popularity, then rerank them with a [learning to rank](/learning-to-rank/) model on features of the prefix, the candidate and the context.
- **Error-tolerant completion.** Accept candidates whose start is within a small [edit distance](/edit-distance/) of $p$, so that a typo in the first letters does not hide the answer; a [Levenshtein automaton](/levenshtein-automaton/) can drive the search in the trie, and [noisy channel spelling correction](/noisy-channel-spelling-correction/) gives a model of the errors.
- **Dynamic logs.** Counts change all the time, so the index must take updates or be rebuilt often.
- **Completion of words, not queries.** Mobile keyboards and code editors complete the current word or token from a language model or a symbol table. The same top-$k$ prefix search applies.

## Examples

**One prefix.** A log has bing 80, binary search 50, binary search tree 30, bin packing 25, binomial heap 15 and bit manipulation 20. For $p$ = "bin" the candidates are the first five, with total count 200, so the maximum likelihood probabilities are $0.4$, $0.25$, $0.15$, $0.125$ and $0.075$. For $k = 3$ the best list is bing, binary search, binary search tree, with expected success $0.8$ and expected reciprocal rank $0.4 + 0.25/2 + 0.15/3 = 0.575$. The same three queries in the reverse order have expected reciprocal rank $0.15 + 0.25/2 + 0.4/3 \approx 0.408$. The [most popular completion](/most-popular-completion/) page traces how a scored trie finds this list without looking at "bin packing" or "binomial heap".

**Context.** A user who searched for "sorting algorithms" a moment ago and now types "bin" more likely wants "binary search" than "bing". A context-sensitive method moves it to the top, and if the guess about the context is wrong, it pushes the right answer down. Bar-Yossef and Kraus measured both effects on the AOL log: the MRR of MostPopularCompletion after one typed character was about $0.187$, and HybridCompletion improved the MRR by $31.5\%$ on average over MostPopularCompletion. These are measurements on one public log.

## Known algorithms

| method | quality model | index | query time |
|---|---|---|---|
| filter and sort the log | counts | none | $O(nL + n \log n)$ for $n$ queries of length at most $L$ |
| [most popular completion](/most-popular-completion/) | counts | trie with the best score below each node | $O(m + kL \log(kL))$ for a prefix of length $m$ |
| precomputed lists | counts | top $k$ stored at each trie node | $O(m + k)$, with $k$ entries per stored node |
| Completion Trie, RMQ Trie, Score-Decomposed Trie (Hsu and Ottaviano) | counts | compressed tries | measured at about a microsecond per completion |
| sorted array with [range minimum queries](/range-minimum-query/) (Gog, Pibiri and Venturini) | counts | the queries in sorted order and an RMQ structure over their scores | $O(m \log n + k \log k)$ |
| NearestCompletion and HybridCompletion (Bar-Yossef and Kraus) | context and counts | popular candidates, reranked | the candidate search plus the reranking |

The bound in the sorted array row counts $O(\log n)$ string comparisons of length at most $m$ for the [binary search](/binary-search/) of the range, and $k$ steps of a heap over subranges, each with one constant-time range minimum query.

## Bounds

- **Lower bound.** Any method must read the $m$ characters of the prefix and write the answer, so $\Omega(m + \text{output size})$ time is needed. Precomputed lists reach it, at the cost of storing $k$ answers per node.
- **Exact top $k$ in output-sensitive time.** The scored trie of most popular completion pops only nodes on the paths to the returned queries, so its work does not depend on how many queries share the prefix.
- **Space.** A plain trie can need one node per character of the log. Hsu and Ottaviano report compressed tries whose size is competitive with a general-purpose compressor applied to the log, with the same answers; this is a measurement on their data.
- **Quality.** Under a fixed model $P(q \mid p, x)$, no list does better in expected reciprocal rank or success at $k$ than the sorted top $k$ (the argument in the definition). The quality of a method is therefore the quality of its model, which is measured on logs, not proved.

## Reductions

- **To range top-$k$.** Sort the candidates as strings. The candidates that start with $p$ form one contiguous range, found by two binary searches. Top-$k$ completion is then the problem of reporting the $k$ largest scores in a range, which repeated [range minimum queries](/range-minimum-query/) on the negated scores solve: take the extreme, split the range around it, and keep the parts in a heap. A [Cartesian tree](/cartesian-tree/) over the scores gives the same order as a tree walk.
- **To top-$k$ selection.** Without an index, the task is [top-$k$ selection](/top-k-selection/) over the candidates with the prefix, after a filter.
- **To ranked retrieval.** Context-sensitive completion is [ranked retrieval](/ranked-retrieval/) over a small candidate set, with the prefix as a hard filter and the context as the query.

## Applications

- **Web and site search boxes.** Suggestions save key presses and steer users toward queries that the engine answers well.
- **E-commerce search.** Product search suggests queries and categories as the user types; Gog, Pibiri and Venturini describe the efficiency needs of such a service at eBay.
- **Address bars, contact lists and command palettes.** The candidates are URLs, names or commands, ranked by frequency and recency.
- **Mobile keyboards and code editors.** They complete words or identifiers with the same prefix search over a scored vocabulary.

## References
