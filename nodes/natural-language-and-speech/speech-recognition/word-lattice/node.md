---
tag: 5BPGS0
kind: data-structure
slug: word-lattice
name: Word lattice
aliases:
- speech lattice
area: natural-language-and-speech/speech-recognition
level: core
summary: A directed acyclic graph of word hypotheses with times and scores that compactly holds many alternative transcriptions.
model: word-ram
complexity:
  vars: {N: the number of nodes, E: the number of arcs}
  time: {worst: "O(N + E)"}
  space: {extra: "O(N + E)"}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [topological-sort, dag-shortest-paths, forward-backward-algorithm, n-gram-language-model]
see_also: [confusion-network, lattice-rescoring, time-synchronous-beam-search, token-passing, minimum-bayes-risk-decoding, k-shortest-paths, word-error-rate, weighted-automaton]
sources:
  - paper: doi:10.1006/csla.1996.0022
    title: Stefan Ortmanns, Hermann Ney and Xavier Aubert, A word graph algorithm for large vocabulary continuous speech recognition, Computer Speech and Language 11(1), 1997, pages 43 to 72
    locator: the construction of word graphs during the beam search and the measurement of their density
  - paper: doi:10.1109/89.906002
    title: Frank Wessel, Ralf Schlüter, Klaus Macherey and Hermann Ney, Confidence measures for large vocabulary continuous speech recognition, IEEE Transactions on Speech and Audio Processing 9(3), 2001, pages 288 to 298
    locator: word posterior probabilities computed on word graphs by forward-backward, used as confidence measures
  - paper: doi:10.1006/csla.2000.0152
    title: Lidia Mangu, Eric Brill and Andreas Stolcke, Finding consensus in speech recognition, word error minimization and other applications of confusion networks, Computer Speech and Language 14(4), 2000, pages 373 to 400
    locator: the lattice definitions and the computation of link posteriors with a scaled combined score
---

A word lattice, or word graph, is the output of a speech decoder that keeps more than one answer. It is a directed acyclic graph. Each node is a point in time, and each arc is a word hypothesis that starts at the time of its source node and ends at the time of its target node, with an acoustic score and a language model score. Each path from the start node to a final node is one transcription. Because paths share arcs, a lattice of a few hundred arcs can hold millions of transcriptions. The standard queries are one pass over the nodes in topological order: the best path, the number of paths, the total score, and the posterior probability of each arc by forward-backward. Later passes rescore lattices with stronger models ([lattice rescoring](/lattice-rescoring/)) or turn them into [confusion networks](/confusion-network/).

## In plain words

A recognizer is often unsure. At one point it might have heard "recognize speech" or "wreck a nice beach". Instead of writing down one answer, it draws a map. Each dot is a moment in time, and each arrow is a word that could fill the gap between two moments, with a score for how well it fits the sound and how likely it is as language.

Any route from the first dot to the last one is a possible sentence. Routes share arrows, so the map stays small even when it holds very many sentences. To find the best route, or how likely each arrow is, you walk through the dots once from left to right, and once back.

## The abstract type

A lattice stores a set of weighted word sequences and answers queries about them.

- `add_node(time)` and `add_arc(u, v, word, ac, lm)` build the graph. An arc may not go back in time, and the graph must stay acyclic.
- `best_path(λ, ip)` returns the path with the best combined score.
- `num_paths()` returns the number of paths.
- `total(semiring, weight)` returns the semiring sum over all paths, for example the log of the total probability.
- `arc_posteriors(λ, ip, κ)` returns, for each arc, the posterior probability that the transcription uses it.
- `prune(b, λ, ip)` returns a smaller lattice with the arcs that lie on a path within $b$ of the best path.

The combined log score of an arc $a$ and of a path $W$ is

$$s(a) = \log p_{ac}(a) + \lambda \log p_{lm}(a) + \log ip, \qquad S(W) = \sum_{a \in W} s(a),$$

which is the decoder score $\log p_{ac} + \lambda \log p_{lm} + |W| \log ip$. The language model weight $\lambda$ and the insertion penalty $ip$ are tuned heuristics.

## Representation

The nodes are numbered $0, \ldots, N - 1$, with a time each. The arcs are in one array of tuples (source, target, word, acoustic score, language model score), and each node has a list of its outgoing and of its incoming arc numbers. There is one start node and a set of final nodes. A lattice looks like the [trellis](/trellis/) of a Viterbi decoder, but its nodes are word boundaries, not states at every frame.

**Invariant.**

- **(L1) Acyclic.** There is no directed cycle. The code checks it in the topological sort.
- **(L2) Time.** For every arc, the time of its source is at most the time of its target.
- **(L3) Adjacency.** Arc $k$ is in the outgoing list of its source and in the incoming list of its target, once each.

The language model score on an arc is only valid for the word history that the lattice structure fixes. A trigram score on an arc needs all paths into its source node to end in the same two words. Lattices from a bigram decoder keep one node per (time, last word), and rescoring with a longer history splits nodes (see [lattice rescoring](/lattice-rescoring/)).

## Operations

Every query is a pass over the nodes in topological order in some semiring: $(\max, +)$ for the best path, $(\mathrm{logadd}, +)$ for totals and posteriors, $(+, \times)$ with weight 1 for the path count.

```pseudo id=main
LATTICE-FORWARD(Λ, ⊕, ⊗, w)
L1  order ← TOPOLOGICAL-SORT(Λ)
L2  α(start) ← 1̄;  α(v) ← 0̄ for every other node v
L3  for each node u in order do
L4      for each arc a from u to v: α(v) ← α(v) ⊕ (α(u) ⊗ w(a))

LATTICE-BACKWARD(Λ, ⊕, ⊗, w)
L5  β(q) ← 1̄ for each final q;  β(v) ← 0̄ for every other node v
L6  for each node u in reverse order do
L7      for each arc a from u to v: β(u) ← β(u) ⊕ (w(a) ⊗ β(v))

ARC-POSTERIOR(a from u to v)       ▷ α, β in the log semiring with w(a) = κ s(a); log Z = logadd of α(q) over final q
L8  γ(a) ← exp(α(u) + κ s(a) + β(v) - log Z)

PRUNE(Λ, b)                        ▷ α, β in the (max, +) semiring with w(a) = s(a); B = the best path score
L9  keep the arcs a from u to v with α(u) + s(a) + β(v) ≥ B - b
L10 keep the start, the final nodes and the ends of the kept arcs
```

The acoustic scale $\kappa$ in line L8 matters. The acoustic log scores of one frame are not independent, so raw path scores are far too peaked, and the best path would get a posterior near 1. Scaling the combined score by $\kappa$, often $1 / \lambda$, keeps the language model on its own scale and flattens the acoustic part. Mangu, Brill and Stolcke 2000 and Wessel et al. 2001 compute posteriors this way.

## Example

The lattice has the nodes 0 (time 0), 1 and 2 (time 30) and 3 (time 60, final), and five arcs:

| arc | words | $\log p_{ac}$ | $p_{lm}$ |
|---|---|---|---|
| $0 \to 1$ | a | $-10$ | 0.6 |
| $0 \to 2$ | x | $-9$ | 0.4 |
| $1 \to 3$ | b | $-12$ | 0.5 |
| $1 \to 3$ | c | $-10$ | 0.5 |
| $2 \to 3$ | b | $-12$ | 0.9 |

There are 3 paths: "a b", "a c" and "x b". With $\lambda = 1$ and $\log ip = 0$, "a c" is best with $-20 + \ln 0.3 \approx -21.204$, ahead of "x b" with $-21 + \ln 0.36 \approx -22.022$. With $\lambda = 10$, the language model counts more, and "x b" is best with $-21 + 10 \ln 0.36 \approx -31.217$, ahead of "a c" with $-32.040$ and "a b" with $-34.040$.

With $\lambda = 10$ and $\kappa = 1 / 10$, the posteriors are 0.6262 for "a", 0.3738 for "x", 0.2819 and 0.3738 for the two "b" arcs, and 0.3443 for "c". The two arcs out of node 0 add up to 1, and so do the three arcs into node 3 (Corollary 2 of the proof). So the best path is "x b", but the most likely first word is "a" (0.6262) and the most likely second word is "b" ($0.2819 + 0.3738 = 0.6557$). Choosing word by word gives "a b", which is not the best path. A [confusion network](/confusion-network/) makes this idea precise. With $\kappa = 1$ instead, the posterior of "x" rises to 0.6674, which shows how the scale sharpens the distribution.

Pruning with $\lambda = 10$ and a beam of 1 keeps "x b" and "a c" (within 0.823 of the best) and drops the arc "b" from node 1, since its best path "a b" is 2.823 below the best. The result has 4 arcs and 2 paths.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). By induction along the topological order, $\alpha(v)$ is the semiring sum over all paths from the start to $v$: each path to $v$ has exactly one last arc, and its source was finished before $v$. The same holds for $\beta$ in reverse. A path through an arc $a$ from $u$ to $v$ splits uniquely into a path to $u$, the arc $a$ and a path from $v$, so by distributivity $\alpha(u) \otimes w(a) \otimes \beta(v)$ is the sum over the paths through $a$. In the log semiring that gives the posterior, and in $(\max, +)$ it gives the best score through $a$, which is what pruning compares with the beam. When every path covers every frame once, the arcs that span a frame have posteriors that add up to 1.

## Complexity

Let $N$ be the number of nodes and $E$ the number of arcs. The topological sort, the forward pass and the backward pass each look at every node and arc once, so the best path, the path count, the total, all arc posteriors, and pruning take $O(N + E)$ time and $O(N + E)$ extra space, with a semiring operation in $O(1)$. The number of paths can be exponential in $N$: a chain of $m$ time slots with two arcs each has $2^m$ paths in $3m$ words of storage. The path count itself can then need $O(N)$ bits.

## Variants

- **N-best lists.** A list of the $n$ best paths is a simple lattice with no shared arcs. It is easy to rescore with any model but holds far fewer alternatives for its size. [k shortest paths](/k-shortest-paths/) extracts it from a lattice.
- **Word graphs with merged nodes.** Ortmanns, Ney and Aubert 1997 build the graph from the word ends of the beam search and merge the nodes with the same time and word history.
- **Lattices as weighted automata.** A lattice is an acyclic [weighted automaton](/weighted-automaton/). WFST tools can then determinize it, keep the best path per word sequence, or compose it with a new language model.
- **Phone or state lattices.** Arcs can also hold phones or HMM states, with word labels on some arcs, as in Kaldi.

## When to use it

Use a lattice when a later step needs more than the best transcription: rescoring with a long-span or neural language model, confidence scores from posteriors, minimum word error decoding with a confusion network, discriminative training, or keyword search. Use the best path alone when nothing downstream needs alternatives.

## Pitfalls

- **Unscaled posteriors.** Without an acoustic scale, nearly all the mass goes to the best path, and the posteriors are useless as confidences.
- **Language model scores tied to a history.** Replacing the language model on the arcs is only valid if every path into a node has the history the new model needs.
- **Pruned lattices hold new paths.** Pruning keeps the arcs of good paths, and their combinations can form paths outside the beam. This is harmless but surprising.
- **Silence and filler arcs.** Real lattices have arcs for silence and noise, and they must not count as words when you score word errors.
- **Very large path counts.** Do not enumerate the paths. Every query here is a single pass.

## Implementations

The Python code stores a lattice with node times, an arc array and in and out lists, and gives a topological sort with a cycle check, generic forward and backward passes over the semirings of the helper module, the best path, the path count, arc posteriors with an acoustic scale, and beam pruning. The tests compare the path count, the total log score, the best path and every arc posterior with enumeration of all paths on random lattices, check that the arcs that span each frame have posteriors that add up to 1, check that pruning keeps every path within the beam and the best score, and check the example.

## History

Lattices came out of the work on multi-pass speech recognition around 1990, when decoders started to keep several alternatives for later passes with stronger models. Ortmanns, Ney and Aubert 1997 gave a word graph algorithm for large vocabularies and showed that about 10 word hypotheses per spoken word were enough to lose almost no accuracy. Posterior probabilities on lattices, computed by forward-backward with a scaled score, became the standard confidence measure (Wessel et al. 2001) and the basis of consensus decoding (Mangu, Brill and Stolcke 2000). Today WFST toolkits such as Kaldi store lattices as acyclic weighted automata.

## References
