---
tag: DTMWXP
kind: technique
slug: lattice-rescoring
name: Lattice rescoring
aliases:
- n-best rescoring
area: natural-language-and-speech/speech-recognition
level: core
summary: Rescore the paths of a lattice or n-best list from a first pass with a stronger language or acoustic model.
prereqs: [n-gram-language-model, word-lattice, k-shortest-paths]
see_also: [weighted-transducer-composition, confusion-network, shallow-fusion, recurrent-neural-network-language-model, hclg-decoding-graph, time-synchronous-beam-search, minimum-bayes-risk-decoding, kneser-ney-smoothing]
sources:
  - paper: doi:10.1109/ICASSP.1990.115542
    title: Richard Schwartz and Yen-Lu Chow, The N-best algorithm, an efficient and exact procedure for finding the N most likely sentence hypotheses, ICASSP 1990, pages 81 to 84
    locator: the N-best search and the use of its list of sentences by later knowledge sources
  - paper: doi:10.1006/csla.1996.0022
    title: Stefan Ortmanns, Hermann Ney and Xavier Aubert, A word graph algorithm for large vocabulary continuous speech recognition, Computer Speech and Language 11(1), 1997, pages 43 to 72
    locator: word graphs as a compact set of alternatives from the first recognition pass
  - paper: doi:10.1006/csla.2001.0184
    title: Mehryar Mohri, Fernando Pereira and Michael Riley, Weighted finite-state transducers in speech recognition, Computer Speech and Language 16(1), 2002, pages 69 to 88
    locator: composition of weighted transducers as the general way to combine a set of hypotheses with a model
---

Lattice rescoring is the second pass of a multi-pass speech recognizer. The first pass decodes with a model that is cheap enough for the search, usually a small n-gram language model, and writes a [word lattice](/word-lattice/) or a list of the $N$ best sentences. The second pass replaces the language model scores on these hypotheses with the scores of a stronger model and picks the new best path. For an n-gram model, the lattice is first expanded so that each node knows the last $n - 1$ words, and the rescoring is then exact: every path gets exactly the score it would get from a full search with the new model, restricted to the paths of the lattice. For a model with unbounded history, such as a recurrent or transformer language model, the lattice cannot be expanded exactly in finite size, and rescoring is approximate.

## In plain words

The first pass of a recognizer must be fast, so it uses a simple language model. It does not throw away the near misses. It keeps them in a lattice, or as a short list of the best sentences.

The second pass looks only at these candidates. It has time for a much better language model, so it scores each candidate again and picks the new winner. The catch is that a better model often looks further back in the sentence. Then two candidates that shared a part of the lattice may need different scores for that part, so the shared part must first be split.

## When it applies

- The first pass keeps enough alternatives: the right sentence, or a good one, must be in the lattice. The best that rescoring can reach is the lattice oracle, the path with the fewest errors in the lattice.
- The acoustic score and the language model score are stored separately on each arc, so that the old language model score can be removed.
- The new model scores words given their history: an n-gram model of any order, a recurrent or transformer language model, or a better acoustic model if the arcs keep their times.

## The template

The score of a path $W$ is $\log p_{ac} + \lambda \log p_{lm}(W) + |W| \log ip$, with a tuned language model weight $\lambda$ and insertion penalty $ip$.

1. **Strip the old model.** Keep the acoustic score $\log p_{ac}(a)$ of each arc and drop $\log p_{lm}(a)$.
2. **Expand the lattice to the new history.** For an n-gram model, make one new node for each pair (old node, last $n - 1$ words) that some path reaches. Process the old nodes in topological order. For each new node $(u, h)$ and each old arc $a$ from $u$ to $v$ with word $w$, add an arc from $(u, h)$ to $(v, h')$, where $h'$ is the last $n - 1$ words of $h\,w$. This is the [composition](/weighted-transducer-composition/) of the lattice with the n-gram model as an automaton.
3. **Score the arcs.** Put $\log p_{new}(w \mid h)$ on each new arc, and the end-of-sentence probability on the arcs into final nodes.
4. **Search again.** Take the best path, the arc posteriors or a [confusion network](/confusion-network/) of the expanded lattice with the new scores. $\lambda$ and $ip$ must be tuned again for the new model.

**Why it is exact for an n-gram model.** The expansion maps each path of the old lattice to exactly one path of the new one, with the same words and acoustic scores, because the start of a path fixes its history and each arc fixes the next one. Every arc of the new lattice knows the full n-gram context of its word, so the sum of the new arc scores is the new language model score of the path. So the best path of the expanded lattice is the best path of the lattice under the new model.

**Cost.** The expanded lattice has one node per distinct (node, history) pair. The number of histories at a node is at most the number of distinct word sequences of length $n - 1$ that end there, and in the worst case it grows like $|V|^{n-1}$, but on real lattices it is much smaller. The rescoring itself is one pass over the expanded lattice.

**A list of the $N$ best sentences.** The simplest second pass extracts the $N$ best paths ([k shortest paths](/k-shortest-paths/)), scores each sentence with any model at all, and sorts them again. This works for every model, including sentence-level ones, and costs $N$ full model evaluations. Schwartz and Chow 1990 gave an exact N-best search for this use. A list holds far fewer alternatives than a lattice of the same size, because a lattice shares the common parts of its paths.

## Classic examples

**Bigram to trigram.** A bigram lattice has one node per (time, last word). Here there are three word positions with two choices each: "the" or "a", then "cat" or "cap", then "sat" or "sad". The lattice has 8 nodes (start, two per position, end), 12 arcs and 8 paths. The acoustic log scores are the $-3$, a $-3.2$, cat $-4$, cap $-3.9$, sat $-5$, sad $-4.8$. The bigram model gives $p(\text{the} \mid \langle s \rangle) = p(\text{a} \mid \langle s \rangle) = 0.5$, 0.3 to each word of the second position, and 0.4 to each of the third, with $\lambda = 1$ and $\log ip = 0$. The best path is then "the cap sad" with $-11.7 + \ln 0.5 + \ln 0.3 + \ln 0.4 \approx -14.513$.

A trigram model keeps the probabilities of the first two words and gives $p(\text{sat} \mid \text{the cat}) = 0.6$, $p(\text{sad} \mid \text{the cat}) = 0.2$, and 0.3 to the third word in every other history. The node for "cat" has two histories, "the cat" and "a cat", which need different scores for "sat". The expansion makes one node per (time, last two words): 2 at the first position, 4 at the second and 4 at the third, plus the start and the end, which is 12 nodes and 18 arcs. It still has 8 paths. After rescoring, "the cat sat" wins with $-12 + \ln 0.5 + \ln 0.3 + \ln 0.6 \approx -14.408$, ahead of "the cap sad" with $-14.801$. The first pass put four paths ahead of "the cat sat", but the lattice kept it.

**A neural language model on a lattice.** A recurrent model has an unbounded history, so exact expansion would make one node per distinct path prefix. A common approximation merges the expanded nodes whose last $k$ words agree, for a small $k$, and keeps one model state for each merged node, the state of the best path into it. This is exact for the paths that it keeps, but it scores the merged paths with a history that is not their own.

## Variations

- **On-the-fly expansion.** Compute the expanded nodes lazily during the best-path search, so that only the nodes on good paths are built.
- **Lattice pruning first.** Prune the lattice with a beam ([word lattice](/word-lattice/)) before the expansion, to bound its size.
- **Interpolated scores.** Add the new model score to the old one, $\lambda_1 \log p_{old} + \lambda_2 \log p_{new}$, with both weights tuned on held-out data.
- **Acoustic rescoring.** With the times on the arcs, a stronger acoustic model can rescore each word segment. Cross-word context models need the neighboring words, which is the same expansion as for the language model.
- **One-pass alternatives.** [Shallow fusion](/shallow-fusion/) adds the stronger model during the first search, at a higher cost per step.

## Pitfalls

- **Old scores left in.** If the old language model score is not removed, the path scores mix the two models with untuned weights.
- **Merging histories.** Rescoring a bigram lattice with a trigram without expansion gives each arc one history, the wrong one for some paths. The result is not the trigram score of any path.
- **Untuned weights.** The best $\lambda$ and insertion penalty for the new model are usually different from those of the first pass.
- **A lattice that is too small.** Rescoring cannot recover a word that is not in the lattice. Measure the lattice oracle error to see how much is left to gain.
- **Expansion blowup.** A dense lattice and a high order can give a very large expanded lattice. Prune first, or expand lazily.
- **Non-words.** Silence, noise and filler arcs must not enter the history of the new model, unless it was trained with them.

## Exercises

1. In the example, list the four histories at the third position after expansion, and check the 18 arcs: 2 from the start, 4 into the second position, 8 into the third, and 4 into the end.
2. Show that a lattice whose node set is (time, last $n - 1$ words) needs no expansion for an n-gram model of order $n$ or less.
3. A bigram lattice has $m$ positions with two words each, and every word follows every word of the position before it. Count the nodes of the bigram lattice and of its trigram expansion.
4. Rank the 8 paths of the example under the bigram model. How long must a list of the best sentences be so that it surely holds "the cat sat", when ties can be broken either way?
5. Explain why rescoring with the approximation that merges histories on the last $k$ words is exact for an n-gram model when $k \ge n - 1$.

## References
