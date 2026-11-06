---
tag: M6PYPN
kind: problem
slug: most-probable-parse
name: Most probable parse
aliases:
- Viterbi parse
area: automata-and-parsing/context-free-parsing
level: advanced
summary: Given a PCFG and a string, find the parse tree with highest probability.
model: word-ram
complexity:
  vars: {n: the length of the input, g: the size of the grammar}
  time: {worst: O(g n^3)}
  space: {worst: O(g n^2)}
prereqs: [probabilistic-context-free-grammar, parse-tree, cyk-algorithm]
see_also: [probabilistic-cky, inside-outside-algorithm, viterbi-algorithm, earley-parser, shared-packed-parse-forest, a-star-search, k-shortest-paths, ambiguity]
sources:
  - book: isbn:9780262133609
    title: Christopher D. Manning and Hinrich Schütze, Foundations of Statistical Natural Language Processing
    locator: Chapter 11, Probabilistic Context Free Grammars (Section 11.3.3, finding the most likely parse of a sentence)
  - book: isbn:9780131873216
    title: Daniel Jurafsky and James H. Martin, Speech and Language Processing, second edition
    locator: Chapter 14, Statistical Parsing (Section 14.2, Probabilistic CKY Parsing of PCFGs)
  - paper: doi:10.1016/0020-0190(77)90002-3
    title: Donald E. Knuth, A generalization of Dijkstra's algorithm, Information Processing Letters 6(1) (1977)
    locator: pp. 1 to 5 (the lightest derivation of each nonterminal of a grammar with monotone weights)
  - paper: "Dan Klein and Christopher D. Manning, A* parsing: fast exact Viterbi parse selection, Proceedings of HLT-NAACL 2003"
    locator: pp. 119 to 126
  - paper: doi:10.3115/993268.993392
    title: Khalil Sima'an, Computational complexity of probabilistic disambiguation by means of tree-grammars, COLING 1996
    locator: pp. 1175 to 1180 (NP-hardness of the most probable parse for stochastic tree-substitution grammars)
---

The most probable parse problem asks, for a [probabilistic context-free grammar](/probabilistic-context-free-grammar/) and a string $w$, for a [parse tree](/parse-tree/) of $w$ whose probability is as large as possible. It is how a statistical parser picks one reading of an [ambiguous](/ambiguity/) sentence. For a plain PCFG it is solved in time $O(|G| \, n^3)$ by [probabilistic CKY](/probabilistic-cky/), the [CYK algorithm](/cyk-algorithm/) with sums replaced by maxima; for grammars whose trees are built from hidden parts it becomes NP-hard.

## In plain words

A grammar for a natural language usually allows many structures for one sentence. In "she saw stars with telescopes", the telescopes may be how she saw, or which stars she saw. A probabilistic grammar gives each rule a chance of being used, learned from a collection of analysed sentences, and the chance of a whole structure is the product of the chances of the rules in it.

The task is to find the structure with the highest chance. Listing all structures is hopeless, because their number can grow exponentially with the sentence length. The way out is that the best structure for a stretch of words is built from best structures for shorter stretches, so one table of best pieces, filled from short stretches to long ones, gives the answer. The same idea is the Viterbi algorithm for hidden Markov models, applied to trees instead of sequences.

## Definition

**Notation.** The grammar is $G = (V, \Sigma, R, S)$, with productions written $A \to \alpha \mid \beta$, $\varepsilon$ the empty string, $S$ the start symbol, $n$ the length of the input and $|G| = \sum_{A \to \alpha \in R} (|\alpha| + 1)$ the size of the grammar. These are the conventions of all pages of this area.

**PCFG.** A probabilistic grammar is a pair $(G, P)$ with $P : R \to [0, 1]$ and $\sum_{\alpha} P(A \to \alpha) = 1$ for every $A \in V$. The probability of a parse tree $t$ is the product over its inner nodes,

$$P(t) = \prod_{A \to \alpha \text{ used at a node of } t} P(A \to \alpha),$$

with one factor for each node, so a production used twice counts twice. Let $T(w)$ be the set of parse trees of $w$ with root $S$.

**The problem.**

- *Input:* a PCFG $(G, P)$ with rational probabilities and a string $w = a_1 \cdots a_n \in \Sigma^*$.
- *Output:* a tree $\hat t \in T(w)$ with $P(\hat t) = \max_{t \in T(w)} P(t)$, together with this value, or "no parse" when $T(w)$ is empty or every tree has probability $0$.
- *Decision version:* given also a rational $\theta$, is there $t \in T(w)$ with $P(t) \ge \theta$?

Since $P(t \mid w) = P(t) / P(w)$ and $P(w) = \sum_{t \in T(w)} P(t)$ does not depend on $t$, the most probable parse also maximizes the conditional probability $P(t \mid w)$. The value $P(w)$ itself is a different problem, solved by the inside pass of the [inside-outside algorithm](/inside-outside-algorithm/).

**The maximum exists.** $T(w)$ can be infinite: with $A \Rightarrow^+ A$ a tree can repeat a unit chain any number of times. But call a node *labelled* $(A, i, j)$ when it has the label $A$ and its subtree yields $a_{i+1} \cdots a_j$. If a path of $t$ has two nodes with the same label $(A, i, j)$, replacing the subtree of the upper one by the subtree of the lower one gives another tree $t' \in T(w)$, and $P(t) = P(t') \cdot q$ for the product $q \le 1$ of the factors of the removed nodes. So $P(t') \ge P(t)$, and the maximum is reached among the trees in which no path repeats a label. There are at most $|V| (n + 1)^2$ labels, so these trees have bounded height, there are finitely many of them, and the maximum exists.

## Variants

- **Most probable derivation and most probable tree.** In a PCFG a tree is one derivation, and the two problems coincide. In models where several derivations give the same visible tree, for example grammars with latent annotations ($NP_1, NP_2, \ldots$ that are erased in the output) or the stochastic tree-substitution grammars of data-oriented parsing, the probability of a tree is a *sum* over its derivations, and the most probable tree is not the yield of the most probable derivation in general. The example below shows the gap.
- **Weighted grammars.** The weights need not sum to 1. With nonnegative weights at most 1, or with costs $-\log P$ and the goal of a minimum-cost tree, all algorithms below work unchanged. With weights above 1 and unit or $\varepsilon$ cycles the supremum may not be reached.
- **$k$ best parses.** Return the $k$ trees of highest probability, as input to a reranker. This is the tree analogue of [$k$ shortest paths](/k-shortest-paths/); Huang and Chiang (2005) give algorithms that, after the Viterbi pass, extract the $k$ best trees lazily from the chart.
- **Other decision rules.** Instead of the single best tree, choose the tree that maximizes the expected number of correct constituents. Such rules use the posterior probabilities of all constituents from the inside and outside passes, and then a CKY-style maximization over spans.
- **Lattice input.** The input is a weighted automaton of candidate strings, as from a speech recognizer, and the goal is the best pair of string and tree. CKY over the states of the automaton solves it for a PCFG.

## Examples

**Attachment ambiguity.** Take the PCFG

| production | $P$ | production | $P$ |
|---|---|---|---|
| $S \to NP \ VP$ | 1.0 | $NP \to NP \ PP$ | 0.2 |
| $VP \to V \ NP$ | 0.7 | $NP \to she$ | 0.3 |
| $VP \to VP \ PP$ | 0.3 | $NP \to stars$ | 0.3 |
| $PP \to P \ NP$ | 1.0 | $NP \to telescopes$ | 0.2 |
| $V \to saw$ | 1.0 | $P \to with$ | 1.0 |

and $w = $ *she saw stars with telescopes*. It has exactly two parse trees:

- $t_1$, with the $PP$ attached to the verb phrase, $[S \ [NP \ she] \ [VP \ [VP \ [V \ saw] \ [NP \ stars]] \ [PP \ [P \ with] \ [NP \ telescopes]]]]$, with $P(t_1) = 0.3 \cdot 0.3 \cdot 0.7 \cdot 0.3 \cdot 0.2 = 0.00378$;
- $t_2$, with the $PP$ attached to the noun phrase, $[S \ [NP \ she] \ [VP \ [V \ saw] \ [NP \ [NP \ stars] \ [PP \ [P \ with] \ [NP \ telescopes]]]]]$, with $P(t_2) = 0.3 \cdot 0.7 \cdot 0.2 \cdot 0.3 \cdot 0.2 = 0.00252$.

So $P(w) = 0.0063$, the most probable parse is $t_1$, and $P(t_1 \mid w) = 0.6$. Writing $\delta(A, i, j)$ for the probability of the best tree with root $A$ and yield $a_{i+1} \cdots a_j$, the CKY table fills these cells, among others:

| cell | best tree | $\delta$ |
|---|---|---|
| $(VP, 1, 3)$ | $VP \to V \ NP$ over *saw stars* | $0.7 \cdot 1 \cdot 0.3 = 0.21$ |
| $(PP, 3, 5)$ | $PP \to P \ NP$ over *with telescopes* | $1 \cdot 1 \cdot 0.2 = 0.2$ |
| $(NP, 2, 5)$ | $NP \to NP \ PP$ | $0.2 \cdot 0.3 \cdot 0.2 = 0.012$ |
| $(VP, 1, 5)$ | max of $VP \to V \ NP$: $0.7 \cdot 0.012 = 0.0084$ and $VP \to VP \ PP$: $0.3 \cdot 0.21 \cdot 0.2 = 0.0126$ | $0.0126$ |
| $(S, 0, 5)$ | $S \to NP \ VP$ | $0.3 \cdot 0.0126 = 0.00378$ |

The choice between the two readings is made once, in cell $(VP, 1, 5)$, and both candidates are found there without listing whole trees. The two trees share every factor except $P(VP \to VP \ PP) = 0.3$ in $t_1$ and $P(NP \to NP \ PP)$ in $t_2$, so the noun attachment wins exactly when $P(NP \to NP \ PP) > 0.3$, whatever the probabilities of the words.

**Infinitely many trees.** In $S \to S$ (0.5), $S \to a$ (0.5), the string $a$ has the trees $[S \ a]$, $[S \ [S \ a]]$, and so on, with probabilities $0.5, 0.25, 0.125, \ldots$. The best tree is $[S \ a]$, with probability 0.5, while $P(a) = 1$.

**Best derivation is not best tree.** Take $S \to A_1 \ B$ (0.3), $S \to A_2 \ B$ (0.3), $S \to C$ (0.4), $A_1 \to a$, $A_2 \to a$, $B \to b$, $C \to a \ b$ (each 1.0), and erase the indices of $A_1$ and $A_2$ in the output. The string $ab$ has three derivations with probabilities 0.3, 0.3 and 0.4, so the best derivation is $[S \ [C \ a \ b]]$. But the visible tree $[S \ [A \ a] \ [B \ b]]$ comes from two derivations and has probability $0.6$, so it is the most probable tree.

## Known algorithms

- **Viterbi CKY.** For a grammar in [Chomsky normal form](/chomsky-normal-form/), set $\delta(A, i-1, i) = P(A \to a_i)$ and, for spans of length 2 or more,
$$\delta(A, i, j) = \max_{A \to B C \in R} \ \max_{i < m < j} P(A \to B C) \, \delta(B, i, m) \, \delta(C, m, j).$$
Keeping the maximizing production and split point in each cell lets the tree be read back from $(S, 0, n)$. The time is $O(|R| \, n^3)$ and the space $O(|V| \, n^2)$. This is [probabilistic CKY](/probabilistic-cky/). Its correctness rests on the fact that a best tree for a cell is made of best trees for its two subcells, because $P$ is a product of nonnegative factors.
- **General grammars.** Converting to Chomsky normal form changes the trees, and the [unit production elimination](/unit-production-elimination/) and [epsilon production elimination](/epsilon-production-elimination/) steps must carry the probabilities along. A simpler route keeps the grammar: binarize the right sides with fresh symbols of probability 1, which keeps the trees in bijection and the size $O(|G|)$; compute for each nullable $A$ the best probability of a tree with yield $\varepsilon$; and inside each cell close the values under unit productions. Since every factor is at most 1, a cycle never helps, and both the $\varepsilon$ values and the unit closure are lightest-derivation problems that Knuth's 1977 generalization of Dijkstra's algorithm solves, with costs $-\log P$. The total time stays $O(|G| \, n^3)$ apart from the per-cell unit closure.
- **Viterbi Earley.** The [Earley parser](/earley-parser/) with each item carrying the best probability of its partial tree. Stolcke (1995) gives this together with the prefix probabilities; it avoids the conversion and is faster on grammars that predict few items.
- **Agenda-based and A* parsing.** Treat the cells as nodes of a hypergraph and extract them in order of decreasing probability, in the manner of Knuth's algorithm; the first time $(S, 0, n)$ is extracted, its tree is optimal. [A* search](/a-star-search/) with an admissible estimate of the outside probability, as in Klein and Manning (2003), returns the same exact tree while building far fewer cells in practice. [Beam search](/beam-search/) prunes cells instead and gives up exactness.
- **Semiring parsing.** Viterbi CKY, the inside pass and recognition are one algorithm over the semirings $(\max, \times)$, $(+, \times)$ and $(\lor, \land)$ (Goodman 1999). The same chart with $(\max, \times)$ replaced by a $k$-best semiring gives the $k$ best trees.
- **Hard variants.** For the most probable tree under latent annotations or tree-substitution grammars, exact methods enumerate derivations with pruning; the usual practice is an approximation, such as the best derivation, a variational PCFG, or a constituent-based decision rule.

## Bounds

- **Upper bound.** $O(|G| \, n^3)$ time and $O(|G| \, n^2)$ space for a PCFG, by the algorithms above; with a grammar in Chomsky normal form, $O(|V| \, n^2)$ space suffices.
- **Matrix multiplication.** [Valiant's algorithm](/valiant-algorithm/) recognizes in time $O(n^\omega)$ by reducing to Boolean matrix products. For Viterbi parsing the corresponding products are over $(\max, \times)$, and after taking logarithms they are [min-plus products](/min-plus-matrix-multiplication/), for which no algorithm in time $O(n^{3 - \epsilon})$ is known; the [APSP conjecture](/apsp-conjecture/) says there is none. So the cubic bound has resisted the speedups that recognition enjoys.
- **Lower bounds.** The problem is at least as hard as recognition: $w \in L(G)$ exactly when the best tree has positive probability, for any PCFG with positive probabilities on the rules of $G$. For recognition, Abboud, Backurs and Vassilevska Williams (2015) showed that a combinatorial algorithm in time $O(n^{3 - \epsilon})$, or any algorithm in time $O(n^{\omega - \epsilon})$, would give faster algorithms for $k$-clique; these bounds carry over.
- **Number of trees.** $|T(w)|$ can be exponential in $n$, or infinite, so enumerating trees is not polynomial; the dynamic program works because the best tree has optimal substructure.

## Reductions

- **Recognition to MPP.** Give the rules of $A$ the uniform probability $1 / (\text{number of productions of } A)$. Then $w \in L(G)$ if and only if the best tree exists, as above.
- **HMM decoding to MPP.** A [hidden Markov model](/hidden-markov-model/) is a right-linear PCFG: states are nonterminals and each step is a rule $X \to a \ Y$ with the probability of the emission $a$ in $X$ times the transition to $Y$, plus rules $X \to a$ for stopping. A tree of this grammar is a path of states, and the most probable parse is the output of the [Viterbi algorithm](/viterbi-algorithm/). For right-linear grammars the CKY table is not needed: the time drops to $O(|G| \, n)$.
- **MPP to lightest hyperpath.** The chart of a PCFG and a string is a hypergraph with a node for each label $(A, i, j)$ and a hyperedge for each production and split point; the most probable parse is a lightest derivation of $(S, 0, n)$ with costs $-\log P$. Knuth's algorithm, A* and agenda parsing are algorithms for this hypergraph problem.
- **NP-hardness for hidden derivations.** For stochastic tree-substitution grammars, where a tree has many derivations, Sima'an (1996) proved that finding the most probable tree is NP-hard, and so is finding the most probable sentence of a word graph under such a grammar. The difference with PCFGs is the sum over derivations inside the objective, which destroys optimal substructure.

## Applications

- **Statistical parsing of natural language.** PCFGs estimated from treebanks, and their refinements by lexicalization or latent annotations, are decoded by Viterbi CKY or its pruned and A* variants.
- **Speech recognition and lattice parsing.** A PCFG language model scores the best string and tree in a lattice of hypotheses.
- **Biological sequences.** Stochastic grammars of RNA secondary structure find the most probable folding of a sequence as the most probable parse, by the same cubic dynamic program.

## References
