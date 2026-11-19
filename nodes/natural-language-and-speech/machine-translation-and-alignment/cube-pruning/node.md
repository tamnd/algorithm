---
tag: 6RZK3C
kind: algorithm
slug: cube-pruning
name: Cube pruning
aliases:
- lazy k-best combination
area: natural-language-and-speech/machine-translation-and-alignment
level: advanced
summary: Approximate k-best combination of hypotheses at each chart cell with a language model, exploring a grid of sorted options lazily from a heap.
solves: [machine-translation]
model: word-ram
complexity:
  vars: {k: the number of items popped per cell, r: the largest number of children of a rule, g: the number of hyperedges into the cell}
  time: {worst: "O((g + k r) log(g + k r))"}
  space: {extra: "O(g + k r)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2007
  people: [David Chiang, Liang Huang]
  note: Chiang (2007) introduced cube pruning in the Hiero decoder to add a language model to chart decoding. It adapts the lazy k-best algorithm of Huang and Chiang (2005). Huang and Chiang (2007) described it on hypergraphs and added cube growing.
prereqs: [hierarchical-phrase-based-translation, priority-queue]
see_also: [hypergraph, k-shortest-paths, binary-heap, beam-search, phrase-based-stack-decoding, n-gram-language-model, ghkm-rule-extraction, top-k-selection]
sources:
  - paper: "David Chiang, Hierarchical phrase-based translation, Computational Linguistics 33(2), 2007, pages 201 to 228, ACL Anthology J07-2003"
    title: Chiang 2007
    locator: the decoder with a language model and the cube pruning method that it introduces
  - paper: "Liang Huang and David Chiang, Forest rescoring: faster decoding with integrated language models, ACL 2007, pages 144 to 151, ACL Anthology P07-1019"
    title: Huang and Chiang 2007
    locator: cube pruning on a hypergraph, why the language model makes it approximate, and cube growing
  - paper: "Liang Huang and David Chiang, Better k-best parsing, Proceedings of the 9th International Workshop on Parsing Technologies (IWPT 2005), pages 53 to 64, ACL Anthology W05-1506"
    title: Huang and Chiang 2005
    locator: the lazy k-best algorithm on a hypergraph, exact for monotone combination functions
  - book: isbn:9780521874151
    title: Philipp Koehn, Statistical Machine Translation, Cambridge University Press, 2010
    locator: "Chapter 11 (tree-based models: decoding with a language model, cube pruning)"
---

Cube pruning is a heuristic that builds the best few items of one cell of a chart decoder, for example in [hierarchical phrase-based translation](/hierarchical-phrase-based-translation/), without scoring every combination of a rule with the items of its children. Each rule with $r$ children gives an $r$-dimensional grid of combinations, sorted along each axis, and cube pruning explores it from the best corner with a [priority queue](/priority-queue/), stopping after $k$ items. Without a language model this is the exact lazy $k$-best algorithm of Huang and Chiang (2005). With an [n-gram language model](/n-gram-language-model/) the scores are no longer monotone along the axes, so cube pruning is approximate.

## In plain words

A chart decoder builds translations of long pieces of a sentence from translations of shorter pieces. A rule says, for example, "put the translation of this part, then the word of, then the translation of that part". Each part has a list of candidates, best first. Trying every pair is too slow.

So the method starts with the best candidate of each part and computes that combination. Then it looks at the neighbours: the next candidate of the first part with the best of the second, and the best of the first with the next of the second. It always expands the best combination seen so far, up to a fixed number. If the score were just a sum, this would find the true best combinations. The language model also scores the words where the parts meet, so a worse candidate can join better, and the method can miss it.

## The problem

Translation runs from a source $f = f_1 \ldots f_m$ to a target $e$. A chart decoder for a synchronous grammar fills a cell for each source span $(s, t)$ (fencepost: it covers $f_{s+1} \ldots f_t$). An *item* is a partial translation with a score and target words. A *hyperedge* into the cell is a rule that applies to the span, with a rule score, a target pattern of words and variables, and one child cell for each variable. The child cells are already filled, and each holds a list of items sorted best first.

For a hyperedge with child lists $L_1, \ldots, L_r$, a *grid point* $j = (j_1, \ldots, j_r)$ chooses item $j_x$ of list $L_x$. Its item has the target words of the pattern with each variable replaced by the words of its chosen child, and the score

$$\mathrm{sc}(j) = \text{rule score} + \sum_x \mathrm{score}(L_x[j_x]) + \mu \sum (\text{new bigrams}),$$

where the new bigrams are those that cross a boundary between a rule word and a child or between two children, logs are natural, and $\mu$ is the language model weight. The task is to find the $k$ highest items over all grid points of all hyperedges into the cell. Exhaustive scoring costs $\sum_e \prod_x |L_{e,x}|$, which is $k^r$ per rule when each child keeps $k$ items.

## The algorithm

```pseudo id=main
CUBE-PRUNE(hyperedges, k)
L1  Q ← empty max-heap; buffer ← empty list; seen ← ∅
L2  for each hyperedge e with no empty child list do push (sc_e(0, .., 0), e, (0, .., 0)) on Q; add it to seen
L3  while Q is not empty and |buffer| < k do
L4      pop the best (score, e, j) from Q
L5      append its item to buffer
L6      for x ← 1 to r_e do
L7          j' ← j with j_x raised by one; if j' is in the grid and (e, j') ∉ seen then
L8              compute sc_e(j'); push it on Q; add (e, j') to seen
L9  sort buffer by score, best first
L10 return buffer
```

Line L2 puts the best corner of every hyperedge into one heap, so the hyperedges of the cell compete with each other. Lines L6 to L8 push the $r$ neighbours of the popped point. The set *seen* stops a point from being pushed twice, because a point with two raised coordinates has two predecessors. Line L9 is needed because the pops are not in order of score when the language model is used. In a full decoder the buffer then goes through recombination of items with the same language model state, and becomes the cell's sorted list.

## Example

A rule $X \to \langle X_1 \, X_2, X_1 \, X_2 \rangle$ joins a subject and a verb. The subject cell has he ($-1.0$), they ($-1.2$), she ($-1.5$), and the verb cell has go ($-0.8$), goes ($-1.0$), went ($-1.6$). The bigram scores at the junction, in natural log, are $-3.0$ for "he go", "they goes" and "she go", $-0.4$ for "he goes" and "she goes", $-0.3$ for "they go", and $-0.6$ for the three with went. The rule score is 0 and $\mu = 1$. The full grid of scores is

| | go | goes | went |
|---|---|---|---|
| he | $-4.8$ | $-2.4$ | $-3.2$ |
| they | $-2.3$ | $-5.2$ | $-3.4$ |
| she | $-5.3$ | $-2.9$ | $-3.7$ |

The scores are not sorted along the rows or columns, because of the junction bigram. Cube pruning with $k = 3$ runs as follows.

| pop | point | item | score | pushed |
|---|---|---|---|---|
| 1 | (0, 0) | he go | $-4.8$ | they go ($-2.3$), he goes ($-2.4$) |
| 2 | (1, 0) | they go | $-2.3$ | she go ($-5.3$), they goes ($-5.2$) |
| 3 | (0, 1) | he goes | $-2.4$ | he went ($-3.2$) |

The result is they go $-2.3$, he goes $-2.4$, he go $-4.8$. The true top three are they go $-2.3$, he goes $-2.4$ and she goes $-2.9$. The point "she goes" is never pushed, because both of its predecessors, "they goes" and "she go", score badly. With $k = 4$, the fourth pop is he went ($-3.2$), and "she goes" is still missed.

Without the language model ($\mu = 0$), the scores are the sums $-1.8, -2.0, -2.0, \ldots$, which decrease along every row and column. Cube pruning with $k = 3$ then returns he go $-1.8$, he goes $-2.0$ and they go $-2.0$, the exact top three.

## Correctness

Two theorems are proved in the proofs file. If the score is monotone, that is, it never increases when one coordinate is raised, the first $k$ pops are exactly the $k$ best grid points, in order. The reason is that every unpopped point has an ancestor in the heap that scores at least as high, so the heap's best is the best unpopped point. For any scores, every returned item is a real grid point with its true score, the result is sorted, and with $k$ at least the grid size every point is returned. Cube pruning with a language model is a heuristic: the example shows a case where it misses a top item. The test file checks exactness against brute force without a language model on 400 random cells, and finds misses with one.

## Complexity

Count in the [word RAM](/word-ram/) model, with one language model lookup as one step. Let $g$ be the number of hyperedges into the cell and $r$ the largest number of children of a rule. Each pop pushes at most $r$ points, so the heap holds at most $g + k r$ entries. The $g$ first pushes, the $k$ pops and the other pushes cost $O((g + k r) \log(g + k r))$ with a [binary heap](/binary-heap/), plus $g + k r$ computations of an item score, each costing $O(1)$ for a bigram model and items of bounded length. Exhaustive scoring would cost $g k^r$ item scores. For a whole chart with $O(m^2)$ cells, the time is $O(m^2 (g + k r) \log(g + k r))$ where $g$ is now the largest number of hyperedges per cell.

## Properties

- **Exact without a language model.** It is then the lazy $k$-best algorithm (a theorem).
- **Approximate with a language model.** The junction bigrams make the scores non-monotone, so it is a heuristic, and its search errors fall as $k$ grows.
- **Sorted output.** The buffer is sorted at the end, so the next cells see sorted lists, which the method needs.
- **Shares one heap per cell.** All hyperedges of a cell compete in one heap, so a cell with many rules spends its $k$ pops on the most promising rules.
- **Not a beam on each rule.** A rule whose corner is poor may get no pops at all.

## Variants and improvements

- **Cube growing.** Huang and Chiang (2007) compute the child lists lazily too, on demand from the parent, which saves work on lists that are never read far.
- **Phrase-based cube pruning.** Moses applies the same grid search to phrase-based decoding, with the hypotheses of a stack on one axis and the translation options of a source span on the other.
- **Diversity.** Some decoders keep at least one pop per hyperedge, so that a rule is not shut out by a bad corner.
- **Better estimates.** Better language model estimates of the first and last words of an item make the scores closer to monotone, and fewer items are missed.
- **Lazy k-best on a hypergraph.** The same lazy enumeration, applied to a whole [hypergraph](/hypergraph/) without a language model, gives the $k$ best derivations of a [CKY-style](/probabilistic-cky/) chart, like [k shortest paths](/k-shortest-paths/).

## When to use it

Use cube pruning in a chart decoder for a synchronous grammar, such as Hiero or a syntax-based model with [GHKM rules](/ghkm-rule-extraction/), to integrate an n-gram language model. A pop limit $k$ in the hundreds or around a thousand per cell is common. Without a language model, the same procedure is exact and is the lazy way to get k-best lists from a chart. For phrase-based decoding, the usual [stack decoder](/phrase-based-stack-decoding/) is simpler; cube pruning there is a speed option.

## Pitfalls

- **Pushing a point twice.** A point with two raised coordinates has two predecessors. Without the *seen* set it enters the heap twice and appears twice in the output.
- **Unsorted child lists.** The method assumes the child lists are sorted best first. Sort each cell's buffer before it is used as a child, as in line L9.
- **Counting the bigrams twice.** A child's score already includes the bigrams inside it. Add only the new bigrams at the junctions.
- **The first words of an item.** The first $n - 1$ words of an item have no left context until a parent places them. Use a language model estimate for them, and correct it when the context is known; otherwise items that start with rare words are ranked too low or too high.
- **Expecting exactness.** With a language model, a larger $k$ reduces search errors but does not remove them.

## Implementations

## History

Huang and Chiang (2005) gave lazy algorithms to find the $k$ best derivations of a hypergraph, by exploring for each hyperedge the grid of the children's sorted derivations from its corner. Chiang (2007) used the same exploration with a language model in the Hiero decoder and called it cube pruning, after the three-dimensional grid of a rule with two nonterminals and its translation options. Huang and Chiang (2007) described it for general hypergraphs, explained that the language model makes the scores non-monotone, and added cube growing. It became the standard search of hierarchical and syntax-based decoders such as Joshua, Moses and cdec.

## References
