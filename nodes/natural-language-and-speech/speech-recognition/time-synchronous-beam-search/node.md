---
tag: 6JVTAP
kind: algorithm
slug: time-synchronous-beam-search
name: Time-synchronous Viterbi beam search
aliases:
- Viterbi beam search
- one-pass decoding
area: natural-language-and-speech/speech-recognition
level: core
summary: Decode speech frame by frame, keeping only states whose score is within a beam of the best, with word ends feeding word starts.
model: word-ram
complexity:
  vars: {n: the number of frames, k: the limit on active hypotheses per frame (at least V), V: the vocabulary size, s: the number of nodes of the prefix tree}
  time: {worst: "O(n k V log k)"}
  space: {extra: "O(s + n k)"}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 1992
  people: [Hermann Ney, Dieter Mergel, Andreas Noll, Horst Paeseler]
  note: Beam search goes back to the Harpy system of Lowerre in 1976. Ney and his colleagues organized the time-synchronous search around a list of active hypotheses in 1992, and later work added the tree lexicon with one copy per predecessor word.
prereqs: [viterbi-algorithm, hidden-markov-model, beam-search, trie, pronunciation-lexicon, n-gram-language-model]
see_also: [token-passing, stack-decoding, word-lattice, hclg-decoding-graph, weight-pushing, top-k-selection, ctc-prefix-beam-search, automatic-speech-recognition]
sources:
  - paper: doi:10.1109/78.124938
    title: Hermann Ney, Dieter Mergel, Andreas Noll and Horst Paeseler, Data driven search organization for continuous speech recognition, IEEE Transactions on Signal Processing 40(2), 1992, pages 272 to 281
    locator: the time-synchronous dynamic programming beam search over a list of active hypotheses
  - paper: doi:10.1109/79.790984
    title: Hermann Ney and Stefan Ortmanns, Dynamic programming search for continuous speech recognition, IEEE Signal Processing Magazine 16(5), 1999, pages 64 to 83
    locator: the sections on time-synchronous beam search, the tree lexicon with copies per predecessor word, and language model look-ahead
  - paper: doi:10.1006/csla.2001.0184
    title: Mehryar Mohri, Fernando Pereira and Michael Riley, Weighted finite-state transducers in speech recognition, Computer Speech and Language 16(1), 2002, pages 69 to 88
    locator: the use of one precompiled network for the same search
---

Time-synchronous Viterbi beam search is the standard first-pass decoder of HMM-based speech recognition. It runs the [Viterbi algorithm](/viterbi-algorithm/) over the HMM states of all words at once, one frame at a time. When a word ends, its score, plus the language model score of the word, starts the first states of the next words. After each frame it drops every hypothesis whose score is more than a fixed beam below the best one, and often keeps only the best $k$. The pruning makes large vocabularies possible, and it also means the search can miss the best word sequence. With no pruning it finds the best path exactly, and [token passing](/token-passing/) finds the same path, since it is the same search described as messages on a network.

## In plain words

You hear the speech one short frame at a time. For each frame you keep a list of guesses: where in which word you are now, and how good the guess is so far. To go to the next frame, each guess can stay in its sound, move to the next sound, or finish its word and start a new one.

Two guesses that reach the same place keep only the better one. Then you throw away every guess that is far worse than the best. At the end you take the best guess that has just finished a word and follow its links back to read the words.

## The problem

The input is a sequence of $n$ frames, an acoustic model that gives the log score $e_t(j)$ of HMM state $j$ at frame $t$, a [pronunciation lexicon](/pronunciation-lexicon/) that turns each word into states, and a bigram [language model](/n-gram-language-model/) $\log p(w \mid v)$. The task is the word sequence $W = w_1 \cdots w_K$ and state path that maximize

$$\log p_{ac} + \lambda \log p_{lm}(W) + |W| \log ip,$$

where $\log p_{ac}$ is the sum of the emission and transition log scores of the path, $p_{lm}(W)$ includes the start $\langle s \rangle$ and the end $\langle /s \rangle$, $\lambda$ is the language model weight and $ip$ is the word insertion penalty. $\lambda$ and $ip$ are heuristics tuned on held-out data, not parts of a probability model. The code writes $\log ip$ as one additive number per word.

In the code each phone is one HMM state with a self loop of log probability $\ell$ and a forward move of log probability $f$, and the exit from the last phone of a word is a forward move too. A real system uses three states per phone, but the search is the same.

## The algorithm

The phones of the words form a prefix tree ([trie](/trie/)), so that words that begin with the same phones share their first states. A hypothesis is a pair (previous word $v$, tree node $q$) with a score and a back pointer. Keeping $v$ in the key gives one copy of the tree per previous word, so the bigram score $\log p(w \mid v)$, added when $w$ ends, is the right one. A word-end record (word, end frame, score, back pointer) remembers each word end for the traceback.

```pseudo id=main
TIME-SYNCHRONOUS-BEAM-SEARCH(tree, lm, e, n)
L1  H ← {(⟨s⟩, c) ↦ e_0(c) for each child c of the root}
L2  for t ← 0 to n - 1 do
L3      PRUNE(H): drop h with score(h) < best - beam; keep at most k best
L4      E ← {}                                      ▷ word ends at frame t
L5      for each (v, q) ∈ H and each word w that ends at q: E[w] ← max(E[w], score + f + λ log p(w | v) + log ip)
L6      if t = n - 1 then exit the loop
L7      for each (v, q) ∈ H: relax (v, q) with score + ℓ + e_{t+1}(q), and (v, c) with score + f + e_{t+1}(c) for each child c
L8      for each w ∈ E and each child c of the root: relax (w, c) with E[w] + e_{t+1}(c)
L9      H ← the relaxed hypotheses of frame t + 1
L10 return the w ∈ E with the best E[w] + λ log p(⟨/s⟩ | w), and trace back its records
```

"Relax" keeps the larger score for a key, with its back pointer: this is the Viterbi recombination. Line L5 recombines the word ends per word and frame, which is enough for a bigram, because the future depends only on the last word.

## Example

The lexicon has the two words $AB = (a, b)$ and $CD = (c, d)$, with equal bigram scores (all 0), $\lambda = 1$, $\log ip = 0$, and $\ell = f = \ln 0.5 \approx -0.693$. There are two frames:

| frame | $a$ | $b$ | $c$ | $d$ |
|---|---|---|---|---|
| 0 | $-1$ | $-9$ | $-2$ | $-9$ |
| 1 | $-9$ | $-5$ | $-9$ | $-1$ |

With no pruning, frame 0 has the hypotheses $a$ at $-1$ and $c$ at $-2$. At frame 1, $a \to b$ gives $-1 - 0.693 - 5 = -6.693$ and $c \to d$ gives $-2 - 0.693 - 1 = -3.693$. The word ends add the exit $f$: $AB$ ends at $-7.386$ and $CD$ at $-4.386$. The search returns $CD$, which is the best path.

With a beam of 0.5, line L3 at frame 0 drops $c$, since $-2 < -1 - 0.5$. Only $AB$ can end, and the search returns $AB$ at $-7.386$, which is 3 worse than the best path. A histogram limit of $k = 1$ fails in the same way. A beam of 1.0 keeps $c$ and finds $CD$. The first frame favors the wrong word, and a narrow beam cannot recover from that.

## Correctness

With no pruning, the search is the Viterbi algorithm on one large HMM: the tree copies with the word-end transitions between them. A hypothesis key (previous word, node) holds everything the future score depends on with a bigram, so keeping only the best score per key loses no optimal path. The best word-end record at the last frame, plus the end score, is then the best path. The tests check this against exhaustive search over all word sequences of at most 5 words and all their segmentations into frames.

With pruning, there is no guarantee. Line L3 can drop the prefix of the best path when that prefix is worse than other prefixes at some frame, as in the example. The returned score is always the score of a real path, so it is never better than the best one.

## Complexity

Let $n$ be the number of frames, $V$ the vocabulary size, $s$ the number of nodes of the tree and $k \ge V$ the histogram limit. At each frame, each of the at most $k$ hypotheses has its self loop and at most $V$ children (line L7), and at most $V$ word ends each start at most $V$ first phones (line L8). That gives $O(k V)$ new hypotheses per frame, and $O(n k V)$ for the whole utterance, plus the top-$k$ selection at line L3. With a heap, the selection costs $O(k V \log k)$ per frame, which gives $O(n k V \log k)$. With linear-time [top-k selection](/top-k-selection/), it is $O(n k V)$. Without a histogram limit, $k$ grows to $s V$, the size of all the tree copies.

The extra space is $O(s)$ for the tree and $O(n k)$ for the word-end records that the traceback needs. A system that keeps only the records on surviving paths, or a lattice, uses less.

## Properties

- **Not exact.** The beam and the histogram limit can drop the best path. With no pruning it is exact.
- **Online.** It reads each frame once, in order, so it can run while the speaker talks. The traceback at the end is short, and partial results can be read from the best hypothesis.
- **Deterministic.** Ties are broken in a fixed order.
- **Same as token passing.** [Token passing](/token-passing/) computes the same scores and finds the same best path when nothing is pruned.

## Variants and improvements

- **Language model look-ahead.** In a tree, the word is known only at the leaf. Look-ahead adds the best language model score of the words below each node early, so pruning sees it sooner (Ney and Ortmanns 1999).
- **A static graph.** Compile the HMMs, lexicon and language model into one [HCLG decoding graph](/hclg-decoding-graph/), so that the search only follows arcs and does not build tree copies.
- **Word-end and phone-start pruning.** Use a separate, narrower beam at word ends, where many hypotheses start at once.
- **Lattice output.** Keep several word-end records per frame, not only the best per word, to output a [word lattice](/word-lattice/).
- **Longer histories.** With a trigram, the key must hold two previous words, which multiplies the tree copies. Rescoring a lattice with the long model is often cheaper ([lattice rescoring](/lattice-rescoring/)).

## When to use it

Use it as the first pass of an HMM-based recognizer with a large vocabulary, when it must run as fast as or faster than the speech. Tune the beam on held-out data: a wider beam makes fewer search errors and runs slower. Use [stack decoding](/stack-decoding/) only when a good estimate of the rest of the utterance is cheap, and a static graph when memory allows.

## Pitfalls

- **Search errors.** A narrow beam can drop the right words early, as in the example. Measure the search errors by comparing with a wider beam.
- **Late language model scores.** With a tree lexicon and no look-ahead, the language model score arrives only at the word end, so the beam prunes on acoustics alone inside words.
- **Wrong recombination.** If the key does not hold the language model history, recombination merges hypotheses with different futures, and the result is no longer the Viterbi path even without pruning.
- **Scale of the scores.** The beam is in log units of the total score, so changing $\lambda$ or the acoustic scale changes what a given beam means.
- **Insertion penalty sign.** A positive $\log ip$ favors many short words, and a negative one favors few long words.

## Implementations

The Python code searches a prefix tree of one-state phones with tree copies per previous word, a bigram, a beam and a histogram limit, and traces back the words and their end frames. The tests compare the score with exhaustive search over all word sequences of at most 5 words and all segmentations, on random lexicons and bigrams with homophones and words that are prefixes of other words. They check that a narrow beam and $k = 1$ return $AB$ in the example, that pruning never gives a better score than no pruning, and that the bigram after each word stays separate.

## History

Lowerre's Harpy system in 1976 introduced beam search for speech. One-pass dynamic programming for connected words, which handles word ends and word starts in the same frame loop, came from Bridle, Brown and Chamberlain in 1982 and from Ney in 1984. Ney, Mergel, Noll and Paeseler 1992 organized the search around a list of active hypotheses built frame by frame. The tree lexicon with one copy per predecessor word and language model look-ahead followed in the 1990s, and Ney and Ortmanns 1999 review them. WFST decoders later replaced the dynamic tree copies with one precompiled graph (Mohri, Pereira and Riley 2002), and kept the same frame-by-frame beam search.

## References
