---
tag: MZTBB1
kind: algorithm
slug: a-star-parsing
name: A* parsing
aliases:
- A* PCFG parsing
area: natural-language-and-speech/natural-language-parsing
level: advanced
summary: Agenda-based exact Viterbi parsing that pops chart items by inside score plus an admissible and monotonic estimate of the outside score.
solves: [most-probable-parse]
model: word-ram
complexity:
  vars: {n: the number of words, g: the number of rules of the grammar in Chomsky normal form, m: the number of nonterminals}
  time: {worst: O(n^3 g log(n g) + n^3 m^2)}
  space: {extra: O(n^3 g)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 2003
  people: [Dan Klein, Christopher D. Manning]
  note: "Klein and Manning ordered the agenda of a chart parser by inside score plus a precomputed admissible and monotonic outside estimate, and kept the Viterbi parse exact."
prereqs: [probabilistic-cky, a-star-search]
see_also: [a-star-optimality, consistent-heuristic, admissible-heuristic, most-probable-parse, dijkstra, hypergraph, beam-search, constituency-parsing]
sources:
  - paper: "Dan Klein and Christopher D. Manning, A* Parsing: Fast Exact Viterbi Parse Selection, Proceedings of HLT-NAACL 2003"
    title: "Dan Klein and Christopher D. Manning, A* Parsing, Fast Exact Viterbi Parse Selection"
    locator: "the agenda parser, the admissible and monotonic conditions on the estimate, the context summary estimates NULL, SX, SXL, SXLR and TRUE, and the measurements of edges processed"
  - book: isbn:9780262133609
    title: "Christopher D. Manning and Hinrich Schütze, Foundations of Statistical Natural Language Processing, MIT Press, 1999"
    locator: "Chapter 11, Probabilistic Context Free Grammars (the grammar of the example)"
  - url: https://web.stanford.edu/~jurafsky/slp3/
    title: "Daniel Jurafsky and James H. Martin, Speech and Language Processing, third edition draft"
    locator: "Appendix E, Statistical Constituency Parsing"
---

A* parsing finds the [most probable parse](/most-probable-parse/) of a sentence under a probabilistic context-free grammar, the same tree that [probabilistic CKY](/probabilistic-cky/) finds, but it does not fill the whole chart. It keeps an agenda, a [priority queue](/priority-queue/) of chart items, and always takes next the item whose inside score plus an estimate of its outside score is largest. When the estimate never underestimates the true outside score and never lets the priority rise along a derivation, the first complete parse taken from the agenda is optimal, exactly as in [A* search](/a-star-search/). Klein and Manning introduced it in 2003. Their estimates are precomputed from the grammar alone, and in their measurements the parser processed a small fraction of the items that exhaustive parsing builds. The worst case stays cubic in the sentence length, with an extra log factor for the queue.

## In plain words

A chart parser builds small pieces of a parse, such as a noun phrase over two words, and combines them into larger pieces until one piece covers the whole sentence. Exhaustive parsing builds every piece. Many of them are useless, because no good parse of the whole sentence uses them.

A* parsing builds the pieces in order of promise. The promise of a piece is its own score times a guess of the best score that the rest of the sentence can add around it. The guess is computed in advance and is always optimistic. A piece with a high score in a hopeless context waits, and a piece that the best parse needs comes out early.

Because the guess is optimistic in the right way, the first full parse that comes out is the best one. A weak guess still gives the right answer, only more slowly.

## The problem

The input is a grammar $G = (N, \Sigma, R, S)$ in [Chomsky normal form](/chomsky-normal-form/), with a probability $q(r) > 0$ on each rule, and a sentence $w = w_1 \cdots w_n$. The output is a [parse tree](/parse-tree/) of $w$ with root $S$ and the largest probability, or the answer that there is none. This is the problem of [most probable parse](/most-probable-parse/), and the page works with natural logs in the Viterbi semiring (max, +, $-\infty$, 0), so the score of a tree is the sum of $\log q$ over its rules.

A chart item is $e = [X, i, j]$ over the fencepost span $(i, j)$, which covers the words $w_{i+1}, \ldots, w_j$. Its inside score $\beta(X, i, j)$ is the best score of a subtree with root $X$ over those words. Its outside score $\alpha(X, i, j)$ is the best score of the rest of a full parse around it, as on the [inside-outside algorithm](/inside-outside-algorithm/) page, with max in place of sum. The best parse has the score $\beta(S, 0, n)$, and for every item $\beta(e) + \alpha(e)$ is the best score of a full parse that contains $e$.

An estimate $a(e)$ of $\alpha(e)$ is **admissible** if $a(e) \ge \alpha(e)$ for every item: in log space, it never underestimates. It is **consistent**, which Klein and Manning call monotonic, if for every rule $Z \to X\,Y$ and items $e = [X, i, j]$, $f = [Y, j, k]$, $g = [Z, i, k]$,

$$a(e) \ge \log q(Z \to X\,Y) + \beta(f) + a(g),$$

and the mirror inequality holds for the right child. In words, building a larger item never raises the priority $b + a$. These are the conditions of [admissible heuristics](/admissible-heuristic/) and [consistent heuristics](/consistent-heuristic/) in graph search, with the costs replaced by negated log probabilities.

## The algorithm

$b(e)$ is the best inside score found so far for item $e$, initially $-\infty$. The agenda holds copies of items with the priority $b(e) + a(e)$. An item is finished when it leaves the agenda for the first time.

```pseudo id=main
A-STAR-PARSE(G, q, w, a)               ▷ a: a consistent estimate of the outside score
L1  for i ← 0 to n-1 do for each rule X → w_{i+1} do RELAX([X, i, i+1], log q(X → w_{i+1}), w_{i+1})
L2  while the agenda is not empty do
L3      pop a copy of an item e = [X, i, j] with the largest priority b + a(e)
L4      if e is finished then continue         ▷ a stale copy
L5      mark e finished
L6      if e = [S, 0, n] then return b(e) and the tree from the back pointers of e
L7      for each finished [Y, j, k] and each rule Z → X Y do RELAX([Z, i, k], log q(Z → X Y) + b(e) + b([Y, j, k]), (j, X, Y))
L8      for each finished [Y, h, i] and each rule Z → Y X do RELAX([Z, h, j], log q(Z → Y X) + b([Y, h, i]) + b(e), (i, Y, X))
L9  return no parse

RELAX(e, s, bp)
L10 if e is not finished and s > b(e) then b(e) ← s;  back(e) ← bp;  push a copy of e with priority s + a(e) unless a(e) = -∞
```

Lines L7 and L8 combine the item just finished with finished neighbours on its right and on its left. Each item is finished once, so each pair of adjacent finished items is combined once, when the later of the two is finished. Line L10 pushes a new copy when a score improves, instead of a decrease-key on the queue, and line L4 drops the copies that are out of date. The goal test is at line L6, when the goal is popped, not when it is first reached at line L10.

With $a = 0$ (the NULL estimate) the priority is the inside score alone, and the parser is uniform cost search, the parsing form of [Dijkstra's algorithm](/dijkstra/) on the [hypergraph](/hypergraph/) of items. The implementation also provides the SX estimate of Klein and Manning. It summarizes the context of an item by its label and the number of words to its left and to its right, and takes the best outside score over all sentences with that context summary. With $\mathrm{in}(Y, k)$, the best inside score of $Y$ over any $k$ words,

$$\mathrm{out}(S, 0, 0) = 0, \qquad \mathrm{out}(X, l, r) = \max\Big(\max_{Z \to X Y,\ k} \mathrm{out}(Z, l, r - k) + \log q + \mathrm{in}(Y, k),\ \max_{Z \to Y X,\ k} \mathrm{out}(Z, l - k, r) + \log q + \mathrm{in}(Y, k)\Big),$$

and $a([X, i, j]) = \mathrm{out}(X, i, n - j)$. The tables depend only on the grammar and the sentence length, so they can be computed once for all sentences up to a maximum length. Both NULL and SX are consistent, and since $a(\text{goal}) = 0$, both are admissible.

## Example

Take the grammar of Manning and Schütze from the [probabilistic CKY](/probabilistic-cky/) page,

$$S \to NP\ VP\ [1.0], \quad PP \to P\ NP\ [1.0], \quad VP \to V\ NP\ [0.7] \mid VP\ PP\ [0.3], \quad NP \to NP\ PP\ [0.4],$$

$$P \to \text{with}\ [1.0], \quad V \to \text{saw}\ [1.0], \quad NP \to \text{astronomers}\ [0.1] \mid \text{ears}\ [0.18] \mid \text{saw}\ [0.04] \mid \text{stars}\ [0.18] \mid \text{telescopes}\ [0.1],$$

and $w$ = *astronomers saw stars with ears*, with $n = 5$. Exhaustive CKY builds 12 items with a nonzero score. The tables list the items in the order they are finished, with $e^{b}$, $e^{a}$ and the priority $e^{b + a}$ shown as probabilities. The numbers come from the implementation, with ties broken first in, first out.

With the NULL estimate, $a = 0$:

| pop | item | $e^b$ | priority |
|---|---|---|---|
| 1 | $[V, 1, 2]$ | 1 | 1 |
| 2 | $[P, 3, 4]$ | 1 | 1 |
| 3 | $[NP, 2, 3]$ | 0.18 | 0.18 |
| 4 | $[NP, 4, 5]$ | 0.18 | 0.18 |
| 5 | $[PP, 3, 5]$ | 0.18 | 0.18 |
| 6 | $[VP, 1, 3]$ | 0.126 | 0.126 |
| 7 | $[NP, 0, 1]$ | 0.1 | 0.1 |
| 8 | $[NP, 1, 2]$ | 0.04 | 0.04 |
| 9 | $[NP, 2, 5]$ | 0.01296 | 0.01296 |
| 10 | $[S, 0, 3]$ | 0.0126 | 0.0126 |
| 11 | $[VP, 1, 5]$ | 0.009072 | 0.009072 |
| 12 | $[S, 0, 5]$ | 0.0009072 | 0.0009072 |

Between pops 11 and 12 the parser pops the stale copy of $[VP, 1, 5]$ with the score 0.006804, from the reading $VP \to VP\ PP$, and line L4 drops it. All 12 items are finished, because the goal has the smallest score of all.

With the SX estimate:

| pop | item | $e^b$ | $e^a$ | priority |
|---|---|---|---|---|
| 1 | $[V, 1, 2]$ | 1 | 0.00163296 | 0.00163296 |
| 2 | $[NP, 2, 3]$ | 0.18 | 0.009072 | 0.00163296 |
| 3 | $[P, 3, 4]$ | 1 | 0.00163296 | 0.00163296 |
| 4 | $[NP, 4, 5]$ | 0.18 | 0.009072 | 0.00163296 |
| 5 | $[PP, 3, 5]$ | 0.18 | 0.009072 | 0.00163296 |
| 6 | $[NP, 2, 5]$ | 0.01296 | 0.126 | 0.00163296 |
| 7 | $[VP, 1, 5]$ | 0.009072 | 0.18 | 0.00163296 |
| 8 | $[VP, 1, 3]$ | 0.126 | 0.00972 | 0.00122472 |
| 9 | $[NP, 0, 1]$ | 0.1 | 0.009072 | 0.0009072 |
| 10 | $[S, 0, 5]$ | 0.0009072 | 1 | 0.0009072 |

The value 0.00163296 is the SX bound for the best parse of any 5-word sentence that has a $V$ over its second word. The items of the best tree share it until pop 7. The noun reading $[NP, 1, 2]$ of *saw* and the item $[S, 0, 3]$ are never finished. $[VP, 1, 5]$ is finished at pop 7 by the reading $VP \to V\ NP$, so when $[VP, 1, 3]$ is finished at pop 8, its offer of 0.006804 to $[VP, 1, 5]$ is ignored at line L10. The result in both runs is the tree in which *with ears* modifies *stars*, with probability 0.0009072.

## Correctness

The claim is: with a consistent estimate, line L6 returns the largest log probability $\beta(S, 0, n)$ of a parse of $w$ and a tree with that score; if there is no parse, line L9 is reached; and the parser stops. This is a theorem.

The key step is that every item has its exact inside score when it is finished. Suppose an item $e$ is popped too early, with $b(e) < \beta(e)$. Take a best derivation of $e$ and its lowest node $f$ that is not finished. The children of $f$ are finished with exact scores, so $f$ already has $b(f) = \beta(f)$ and a copy in the agenda. Consistency, applied step by step from $f$ up to $e$, gives $\beta(f) + a(f) \ge \beta(e) + a(e) > b(e) + a(e)$, so that copy of $f$ had a larger priority and would have been popped first. The goal is then popped with its exact score, and the back pointers of finished items never change. The argument is the hypergraph form of the proof on the [A* optimality](/a-star-optimality/) page. The full proof, with termination and the case without a parse, is in [the correctness proof](proofs/correctness.md). It also proves that NULL and SX are consistent.

Admissibility alone is not enough for this version, which never reopens a finished item. An admissible but inconsistent estimate can finish an item with a score below its inside score.

## Complexity

**Time.** An offer at line L7 or L8 is made once for each rule $Z \to X\,Y$ and each pair of adjacent finished items $[X, i, j]$ and $[Y, j, k]$, so there are at most $O(n^3 g)$ offers. Each offer pushes at most one copy, so the agenda holds at most $O(n^3 g + n g)$ copies, and each push or pop costs $O(\log(n g))$ with a [binary heap](/binary-heap/). Scanning the lists of finished neighbours costs $O(n m)$ per finished item, and there are at most $n^2 m$ of them, which adds $O(n^3 m^2)$. The worst case is therefore $O(n^3 g \log(n g) + n^3 m^2)$ on the [word RAM](/word-ram/), plus the cost of the estimate. A* does not beat the cubic bound of CKY in the worst case. Its gain is in the number of items actually built, which depends on the grammar, the sentence and the estimate.

**The estimate.** The SX tables take $O(n^3 g)$ time and $O(n^2 m)$ space, and they depend only on the sentence length, so they are computed once and reused.

**Space.** The chart has $O(n^2 m)$ items and back pointers. With lazy deletion the agenda can hold $O(n^3 g)$ copies in the worst case. A queue with a decrease-key operation keeps it at $O(n^2 m)$.

**Measurement.** Klein and Manning report on Penn Treebank sentences that their most detailed context summary estimate cut the number of edges processed to under 3% of what exhaustive parsing processes, and that a cheaper estimate, precomputed in under a minute, cut it to under 5%.

## Properties

- **Exact.** With a consistent estimate it returns a parse of maximum probability, the same score as probabilistic CKY. Ties between parses of equal score are broken by the order of the queue.
- **Monotone pops.** With a consistent estimate the priorities of the finished items never increase from one pop to the next.
- **Estimate quality trades work for precomputation.** NULL needs nothing and finishes every item whose inside score is above the score of the best parse. SX and richer summaries finish fewer items but need larger tables. The TRUE estimate, the exact outside score, finishes the fewest but costs a full parse to compute.
- **Not online.** The estimate depends on the sentence length, and the goal covers the whole sentence.

## Variants and improvements

- **Richer context summaries.** Klein and Manning also give SXL, SXLR and TRUE, which keep more of the context of the span in the summary, up to the whole sentence for TRUE. More detail gives a tighter bound and fewer items, at the cost of larger tables.
- **Estimates from a coarser grammar.** Map the nonterminals to fewer classes and give each coarse rule the largest probability of the rules mapped to it. Every fine parse maps to a coarse one with at least its probability, so the exact outside scores of the coarse grammar are an admissible bound for the fine grammar. They are consistent too, since they are exact outside scores of a grammar that bounds every fine rule.
- **Uniform cost and Knuth's algorithm.** With $a = 0$ the parser is an agenda version of Dijkstra's algorithm on the item hypergraph.
- **Inexact best-first parsing.** Using a figure of merit that is not an admissible bound, as earlier best-first parsers did, finds a good parse faster but loses the guarantee.
- **Beam search.** Keeping only the best items of each cell of the CKY chart, as in [beam search](/beam-search/), is also inexact, but has a fixed cost.

## When to use it

Use A* parsing when the exact Viterbi parse is required and the grammar is large, so that exhaustive CKY is slow but most items are hopeless. A good estimate can be precomputed for the grammar, as SX can. For short sentences or small grammars, plain probabilistic CKY is simpler and vectorizes better, since its loops do not depend on the scores. When an approximate parse is good enough, beam or coarse-to-fine pruning is usually faster, and neural span-based parsers such as [span-based neural constituency parsing](/span-based-constituency-parsing/) use exhaustive CKY over learned scores instead.

## Pitfalls

- **Goal test at the push.** Returning when the goal first gets a score at line L10 gives the first parse found, not the best one. Test at line L6, when the goal is popped.
- **Inconsistent estimate.** If the estimate underestimates the outside score of an item of the best tree, another parse can be popped first. The tests use an estimate that lowers the outside score of $[NP, 2, 5]$ by a large amount, and the parser returns the reading $VP \to VP\ PP$ with probability 0.0006804 instead of 0.0009072.
- **Stale copies.** Without the test of line L4, a finished item is processed again when an old copy is popped, and lines L7 and L8 make duplicate offers.
- **Wrong sentence length.** The SX table for $n$ words is a bound only for sentences of $n$ words. Looking up $\mathrm{out}(X, i, n - j)$ with the wrong $n$ breaks admissibility.
- **Underflow.** Products of probabilities underflow for long sentences. The page works in log space; the tests parse 12 words with lexical probability $10^{-30}$, where the plain product is 0.0 and the log score is exact.
- **Unary rules.** The page assumes Chomsky normal form. With unary rules $X \to Y$, the parser must also offer $[X, i, j]$ from $[Y, i, j]$ next to lines L7 and L8, and the SX recurrence needs the same unary step. Since $\log q \le 0$, a unary cycle never improves a score in the Viterbi semiring, so the agenda handles it without a closure.

## Implementations

## History

Agenda-based chart parsing was standard in the 1980s, and best-first parsers of the 1990s ordered the agenda by figures of merit that sped up parsing but gave up exactness. Klein and Manning (2003) showed that an agenda ordered by inside score plus an admissible and monotonic outside estimate keeps the Viterbi parse exact while it processes far fewer items. They built on their earlier description of parsing as search on a hypergraph and gave a family of estimates, from NULL to TRUE, precomputed from the grammar by context summaries such as SX. Later work used A* with estimates from coarser grammars and for k-best parsing.

## References
