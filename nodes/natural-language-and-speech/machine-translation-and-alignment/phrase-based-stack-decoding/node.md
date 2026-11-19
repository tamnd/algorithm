---
tag: 7R5WTX
kind: algorithm
slug: phrase-based-stack-decoding
name: Stack decoding for phrase-based translation
aliases:
- multi-stack beam decoding
area: natural-language-and-speech/machine-translation-and-alignment
level: core
summary: Beam search with one stack per number of covered source words, adding phrase translations to hypotheses with a future cost estimate.
solves: [machine-translation]
model: word-ram
complexity:
  vars: {m: the source sentence length, k: the stack size, o: the number of translation options of the sentence}
  time: {worst: "O(m k o log(k o))"}
  space: {extra: "O(m k o)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2004
  people: [Philipp Koehn]
  note: Koehn (2004) described the beam search of the Pharaoh decoder, with stacks by the number of translated words, a future cost estimate, hypothesis recombination and histogram and threshold pruning. Moses (2007) kept the same search.
prereqs: [phrase-based-translation-model, beam-search]
see_also: [stack-decoding, log-linear-translation-model, cube-pruning, n-gram-language-model, noisy-channel-translation-model, np-complete, traveling-salesman-problem, a-star-search]
sources:
  - paper: "Philipp Koehn, Pharaoh: a beam search decoder for phrase-based statistical machine translation models, Proceedings of AMTA 2004, Lecture Notes in Computer Science 3265, pages 115 to 124, ACL Anthology 2004.amta-papers.13"
    title: Koehn 2004
    locator: the decoding algorithm with stacks by the number of foreign words translated, the future cost estimate, recombination and pruning
  - paper: "Kevin Knight, Decoding complexity in word-replacement translation models, Computational Linguistics 25(4), 1999, pages 607 to 615, ACL Anthology J99-4005"
    title: Knight 1999
    locator: "Section 4.1 (decoding IBM Model 1 with a bigram language model is NP-complete, by a reduction from the Hamilton circuit problem, and its relation to the traveling salesman problem)"
  - paper: "Philipp Koehn, Franz Josef Och and Daniel Marcu, Statistical phrase-based translation, HLT-NAACL 2003, ACL Anthology N03-1017"
    title: Koehn, Och and Marcu 2003
    locator: the phrase-based model and the beam search decoder used in its experiments
  - book: isbn:9780521874151
    title: Philipp Koehn, Statistical Machine Translation, Cambridge University Press, 2010
    locator: "Chapter 6 (decoding: translation options, hypothesis expansion, recombination, stack decoding, future cost)"
---

Stack decoding for phrase-based translation is the [beam search](/beam-search/) that the Pharaoh and Moses decoders use to find a high-scoring translation under a [phrase-based model](/phrase-based-translation-model/). It builds the translation from left to right, one phrase at a time, and each step may translate any untranslated part of the source, so the phrases can be reordered. Partial translations go into stacks by the number of source words they cover, and each stack is pruned by the score so far plus an estimate of the cost of the rest. The search is a heuristic: with pruning it can miss the best translation, and exact decoding with free reordering is [NP-complete](/np-complete/).

## In plain words

The decoder writes the translation from left to right. At each step it picks a piece of the source sentence that it has not translated yet, anywhere in the sentence, and appends one translation of that piece. A partial translation remembers which source words it has used.

There are far too many partial translations to keep. So they are sorted into stacks: one stack for partial translations that used one source word, one for two words, and so on. Each stack keeps only its best few. To compare fairly a partial translation that did the easy words with one that did the hard words, the decoder adds a guess of what the remaining words will cost. Two partial translations that can continue in exactly the same ways are merged, and only the better one is kept.

## The problem

Translation runs from the source $f = f_1 \ldots f_m$ to a target sentence $e$. Spans are fencepost: $(s, t)$ covers $f_{s+1} \ldots f_t$. A *derivation* is a sequence of steps $(s_k, t_k, \bar e_k)$ whose source spans cover each source word once, where $\bar e_k$ is a translation of $f_{s_k+1} \ldots f_{t_k}$ in the phrase table. Its target is $e = \bar e_1 \cdots \bar e_n$. This page uses a [log-linear](/log-linear-translation-model/) score with four features, all logs natural:

$$\mathrm{score} = \sum_k \bigl(\mathrm{tm}_k - \delta \, |s_k - t_{k-1}| + \omega \, |\bar e_k|\bigr) + \mu \ln p_{\mathrm{LM}}(\texttt{<s>} \; e \; \texttt{</s>}),$$

where $\mathrm{tm}_k$ is the log phrase score (already weighted), $t_0 = 0$, $\delta$ weights the distortion (the jump from the end of the last phrase to the start of the next), $\omega$ is a word penalty, and the language model is a bigram model weighted by $\mu$. An optional distortion limit $d$ forbids jumps with $|s_k - t_{k-1}| > d$. The goal is a derivation with the largest score. Real decoders use more features and a longer language model history; the search does not change.

## The algorithm

A *hypothesis* stores its score, its coverage (the set of covered source words), its last target word, the end of its last source phrase, and a back pointer. Its *state* is the triple (coverage, last word, end). Two hypotheses with the same state have the same set of possible completions with the same added scores, so only the better one needs to be kept. This is *recombination*.

The *future cost* $\mathrm{fc}(s, t)$ is an estimate of the best score for translating $f_{s+1} \ldots f_t$ alone: the best monotone segmentation of the span into phrases, each scored by its translation score, word penalty and a language model estimate without context, and with no distortion. A dynamic program over spans, shorter spans first, computes it for all spans before the search. The future cost of a hypothesis is the sum of $\mathrm{fc}$ over the maximal runs of uncovered words.

```pseudo id=main
DECODE(f, model, k, θ, d)                       ▷ k: stack size, θ: threshold, d: distortion limit
L1  compute fc(s, t) for all spans
L2  stacks S_0 .. S_m; S_0 ← { (score 0, coverage ∅, last <s>, end 0) }
L3  for c ← 0 to m − 1 do
L4      prune S_c by score + future cost: keep those within θ of the best, then the best k
L5      for each hypothesis h in S_c do
L6          for each translation option (s, t, ē, tm) do
L7              if (s, t) overlaps the coverage of h or |s − end(h)| > d then continue
L8              h' ← h + (s, t, ē): add tm, the LM scores of ē after last(h), −δ |s − end(h)| and ω |ē|
L9              key ← (coverage(h'), last(h'), end(h'))
L10             in S_{c + t − s}: keep h' if key is new or h' is better than the hypothesis with this key
L11 for each h in S_m do
L12     total(h) ← score(h) + μ ln p(</s> | last(h)); keep the best
L13 follow the back pointers from the best h to get the steps
```

Line L4 does both kinds of pruning of Pharaoh: *threshold pruning* drops hypotheses whose score plus future cost is more than $\theta$ below the best in the stack, and *histogram pruning* keeps at most $k$. Lines L9 and L10 do recombination. Line L12 adds the end of sentence term, which only complete hypotheses can have.

## Example

Translate the German $f$ = morgen fliege ich into English. The phrase table has morgen to tomorrow with score $-0.2$, fliege to will fly ($-0.7$) or fly ($-0.9$), ich to I ($-0.1$), and the two-word phrase fliege ich to I will fly ($-1.5$). The bigram language model has, in natural log, $\ln p(\text{tomorrow} \mid \texttt{<s>}) = -1.0$, $\ln p(\text{I} \mid \text{tomorrow}) = -1.2$, $\ln p(\text{will} \mid \text{I}) = -0.6$, $\ln p(\text{fly} \mid \text{will}) = -0.4$, $\ln p(\texttt{</s>} \mid \text{fly}) = -0.5$, a few other bigrams, and $-6$ for every unseen bigram. The weights are $\mu = 1$, $\delta = 0.5$ and $\omega = 0$, with no distortion limit.

**Future cost.** The table gives $\mathrm{fc}(0,1) = -1.2$ (tomorrow), $\mathrm{fc}(0,2) = -2.5$, $\mathrm{fc}(0,3) = -3.8$, $\mathrm{fc}(1,2) = -1.3$, $\mathrm{fc}(1,3) = -2.6$ and $\mathrm{fc}(2,3) = -1.3$.

**Stack 1.** Expanding the empty hypothesis gives tomorrow with score $-1.2$ and score plus future cost $-1.2 - 2.6 = -3.8$; I (from ich, a jump of 2) with score $-7.1$; and two hypotheses from fliege. When "fly" is reached twice with the same state, recombination keeps the better one: the state (fliege covered, last word fly, end 2) gets $-7.6$ first and then $-7.4$, and only $-7.4$ stays.

**Stack 3.** The full hypotheses are compared with the end of sentence term. "Tomorrow I will fly", made of tomorrow and then the two-word phrase, gets

$-0.2 - 1.5 + (-1.0 - 1.2 - 0.6 - 0.4 - 0.5) = -5.4$.

The best translation that uses only one-word phrases is the same string with the steps tomorrow, I (a jump forward of 1), will fly (a jump back of 2), and gets $-6.2$, because it pays $0.5 + 1.0$ for distortion and the phrase scores $-0.2 - 0.1 - 0.7$. The sentence has 14 derivations in all. The decoder with no pruning returns $-5.4$, the same as a search over all of them.

**Without the phrase "fliege ich".** The best derivation is then the reordering one, with score $-6.2$. With a distortion limit of 1, the jump back of 2 is forbidden, and the decoder returns "tomorrow will fly I".

**A pruning error.** Take the source "a b" with a to x ($-0.1$) or y ($-1.0$), b to z ($0$), a distortion limit of 0, and the bigrams $\ln p(x \mid \texttt{<s>}) = \ln p(y \mid \texttt{<s>}) = -1$, $\ln p(z \mid x) = -5$, $\ln p(z \mid y) = -0.1$ and $\ln p(\texttt{</s>} \mid z) = 0$. The best translation is "y z" with $-2.1$. With a stack size of 1, stack 1 keeps only x, because it looks better ($-1.1$ against $-2.0$, and both have the same future cost), and the decoder returns "x z" with $-6.1$. A threshold of 0.5 makes the same error.

## Correctness

Without pruning, the decoder returns a derivation with the largest score; this is a theorem, proved in the proofs file. The proof rests on two facts. First, the score that a completion adds depends only on the state of the hypothesis, because the language model is a bigram model and the distortion depends only on the end of the last phrase; so recombination never loses the best derivation. Second, every step goes from a stack with fewer covered words to one with more, so the stacks can be processed in order. With pruning, the decoder is a heuristic: line L4 can drop the hypothesis that the best derivation passes through, as in the example. The test file compares the decoder with an exhaustive search over all segmentations, all orders and all options, for random models and sentences of up to 4 words.

## Complexity

Count in the [word RAM](/word-ram/) model, with each language model lookup as one step. Let $o$ be the number of translation options of the sentence. With stack size $k$, each of the $m$ stacks expands at most $k$ hypotheses, each with at most $o$ options, so there are $O(m k o)$ expansions, each costing $O(1)$ for phrases of bounded length. Sorting a stack for pruning costs $O(N \log N)$ for the $N$ hypotheses it received, and $N \le k o$. The future cost table costs $O(m^3 + o)$ once. The space is dominated by the hypotheses created, $O(m k o)$. Decoders keep $o$ small by keeping only the best few translations of each source phrase.

Without pruning, the number of states can grow like $2^m$ times the number of target words, so the search is exponential. This is unavoidable in the worst case unless P = NP: finding the best translation with free reordering is [NP-hard](/np-hard/), and its decision version is NP-complete (Knight 1999, for a word-based model with a bigram language model, by a reduction from the Hamilton circuit problem, a special case of the [traveling salesman problem](/traveling-salesman-problem/)). With a distortion limit $d$, the coverage sets that can occur are limited, and the number of states is linear in $m$ for fixed $d$ and vocabulary, though exponential in $d$.

## Properties

- **Not exact.** Pruning makes it a heuristic, as for every beam search; the narrow-beam example above is a search error.
- **Exact without pruning.** With an unlimited stack size and threshold, it is a complete dynamic program over states, but exponential.
- **Recombination is safe.** It never loses the best derivation, for an $n$-gram language model with the state extended to the last $n - 1$ words.
- **Left to right output.** The target is built in order, so the $n$-gram language model can be scored at once, while the source is covered in any order.
- **Fair comparison by coverage size.** Hypotheses in one stack cover the same number of source words, so their scores are comparable, and the future cost corrects for which words were covered.

## Variants and improvements

- **Coverage stacks.** Some decoders put hypotheses with the same coverage set into one stack, or group them by coverage inside a stack, to keep diversity.
- **Cube pruning.** Moses also offers [cube pruning](/cube-pruning/) for phrase-based search: hypotheses and translation options are sorted, and only the most promising combinations are scored.
- **A-star search.** With an admissible future cost (one that never underestimates the best completion), [A* search](/a-star-search/) finds the exact best; the future cost of Pharaoh is not admissible, because it ignores distortion and the language model context.
- **Exact decoding.** Integer linear programming and [Lagrangian relaxation](/lagrangian-relaxation/) give exact results on many sentences at a higher cost.
- **Lattice and n-best output.** Keeping the recombined hypotheses as back links gives a [word lattice](/word-lattice/) of the search space, from which n-best lists for [minimum error rate training](/minimum-error-rate-training/) are taken.
- **Stack decoding for speech.** The older [stack decoding](/stack-decoding/) of speech recognition keeps one priority queue; the multi-stack version here avoids comparing hypotheses of different coverage.

## When to use it

Use it to decode a phrase-based model, with a stack size in the hundreds, a distortion limit of about 6 words (the Moses default) for languages with similar word order, and a threshold that drops hypotheses far below the best. Raise the stack size if the model score of the output improves with it: then the search makes errors. For models built on a synchronous grammar, such as [Hiero](/hierarchical-phrase-based-translation/), use chart decoding with cube pruning instead.

## Pitfalls

- **Pruning without future cost.** If line L4 ranks by the score alone, hypotheses that took the easy words first win, and the hard words are left for later with no good options.
- **Recombination on too small a state.** With a trigram model, the state must hold the last two target words; with a distortion feature, it must hold the end of the last phrase. A smaller key merges hypotheses with different futures and can lose the best one.
- **Forgetting the end of sentence.** Add $\ln p(\texttt{</s>} \mid \cdot)$ to complete hypotheses before choosing the best, as in line L12.
- **Distortion in the future cost.** Pharaoh's future cost leaves distortion out. If a variant adds an estimate of it, the estimate must be the same for hypotheses that are compared, or the ranking is unfair.
- **Gaps that cannot be filled.** With a distortion limit, a hypothesis can leave a gap that it can never reach again. Such hypotheses waste stack space, so a decoder should test, before it adds a hypothesis, that the first gap can still be reached.

## Implementations

## History

Stack decoding came from speech recognition, and the early word-based translation decoders adapted it. Koehn (2004) described the multi-stack beam search of the Pharaoh decoder, with stacks by the number of translated source words, a future cost estimate from the best phrase segmentation of each span, recombination, and histogram and threshold pruning. Knight (1999) had shown that exact decoding is NP-complete when the words can be reordered freely. Moses (Koehn et al. 2007) became the open-source successor of Pharaoh and kept the same search, with cube pruning added later.

## References
