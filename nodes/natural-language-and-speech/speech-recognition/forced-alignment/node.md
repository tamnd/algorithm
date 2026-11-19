---
tag: 4HHCES
kind: algorithm
slug: forced-alignment
name: Forced alignment
aliases:
- Viterbi forced alignment
area: natural-language-and-speech/speech-recognition
level: core
summary: Find the time span of each word, phone and HMM state of a known transcript by a Viterbi search through the left-to-right HMM built from that transcript.
solves: [hmm-decoding]
model: floating-point-model
complexity:
  vars: {T: the number of frames, S: the number of HMM states in the chain of the transcript}
  time: {worst: "Θ(T S)"}
  space: {extra: "Θ(T S)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1968
  people: [Taras K. Vintsyuk]
  note: Vintsyuk aligned speech to word templates by dynamic programming in 1968. HMM recognizers later used the same Viterbi recursion through the HMM of a known transcript to segment their training data.
prereqs: [viterbi-algorithm, gmm-hmm-acoustic-model, pronunciation-lexicon]
see_also: [viterbi-training, log-sum-exp-trick, dynamic-time-warping, connectionist-temporal-classification, hidden-semi-markov-model, hybrid-dnn-hmm, traceback, triphone-model]
sources:
  - paper: doi:10.1109/5.18626
    title: Lawrence R. Rabiner, A tutorial on hidden Markov models and selected applications in speech recognition, Proceedings of the IEEE 77(2), 1989, pages 257 to 286
    locator: "Section III.B (the Viterbi algorithm) and Section V.A (scaling)"
  - paper: doi:10.1561/2000000004
    title: Mark Gales and Steve Young, The application of hidden Markov models in speech recognition, Foundations and Trends in Signal Processing 1(3), 2008, pages 195 to 304
    locator: the chapters on the architecture of an HMM-based recognizer and on parameter estimation
  - book: isbn:9780130226167
    title: Xuedong Huang, Alex Acero and Hsiao-Wuen Hon, Spoken Language Processing, Prentice Hall PTR, 2001
    locator: Chapter 8 (hidden Markov models)
  - paper: doi:10.1007/BF01074755
    title: T. K. Vintsyuk, Speech discrimination by dynamic programming, Cybernetics 4(1), 1968, pages 52 to 57 (Kibernetika 4(1), pages 81 to 88, in Russian)
    locator: the dynamic programming alignment of an utterance with word templates
---

Forced alignment finds where each word, phone and HMM state of a known transcript starts and ends in an utterance. It builds one left-to-right [hidden Markov model](/hidden-markov-model/) from the transcript and the [pronunciation lexicon](/pronunciation-lexicon/), and runs the [Viterbi algorithm](/viterbi-algorithm/) through it. Because each state has only a self loop and one forward arc, the search takes $\Theta(T S)$ time for $T$ frames and $S$ states, not the $\Theta(T S^2)$ of a general HMM. It works in log space, because the product of the probabilities of a few hundred frames underflows in double precision.

## In plain words

You have a recording and the exact words that were said. You want to know when each word and each sound starts. Write the sounds of the sentence in order, as a chain. Each sound must take at least one short slice of the recording, and the sounds must come in the order of the chain. Many ways to split the recording fit these rules.

The acoustic model gives a score for each sound on each slice. Forced alignment finds the split with the best total score. It walks through the slices one by one. For each sound in the chain, it keeps the best score of any split that ends with that sound at this slice. At the end it follows the stored choices back, and reads off the start and the end of each sound.

## The problem

The input is a sequence of feature frames $O = o_1 \ldots o_T$ (for example the [MFCC](/mel-frequency-cepstral-coefficients/) vectors of 10 ms frames), a transcript $W = w_1 \ldots w_U$, a lexicon that gives each word a phone sequence, and an acoustic model with a left-to-right HMM of 3 emitting states for each phone. Concatenate the phone HMMs of the transcript into one chain of $S$ states. The code numbers the frames $0, \ldots, T-1$ and the states $0, \ldots, S-1$.

A path $Q = q_0 \ldots q_{T-1}$ starts in state 0, ends in state $S - 1$, and at each frame stays in its state or moves to the next one. There are no skips, so each state takes at least one frame, and a path exists only if $T \ge S$. The task is

$$Q^* = \arg\max_{Q} \log P(O, Q \mid \lambda_W) = \arg\max_Q \Big( e_0(q_0) + \sum_{t=1}^{T-1} \big( w(q_{t-1}, q_t) + e_t(q_t) \big) \Big),$$

where $e_t(j) = \log b_j(o_t)$ is the log emission score, $w(j, j) = \log a_{jj}$ is the log self loop and $w(j, j+1) = \log a_{j, j+1}$ is the log move. All logs are natural logs. The output is $Q^*$, its score, and the spans of the states, phones and words that $Q^*$ implies.

This page joins the phone models directly, without the non-emitting entry and exit states of the HTK convention. The exit transition of the last state is the same factor for every path, so it does not change $Q^*$. A path is a segmentation of the $T$ frames into $S$ non-empty runs in order, so there are $\binom{T-1}{S-1}$ paths.

## The algorithm

The arrays hold $e_t(j)$, $a_j = \log a_{jj}$ and $m_j = \log a_{j, j+1}$. Only the cells with $lo_t \le j \le hi_t$, where $lo_t = \max(0, S - T + t)$ and $hi_t = \min(S - 1, t)$, are computed: a state above $hi_t$ cannot be reached by frame $t$, and a state below $lo_t$ cannot reach state $S-1$ by the last frame.

```pseudo id=main
FORCED-ALIGN(e, a, m)                ▷ e[t][j] = log b_j(o_t), a[j] = log self loop, m[j] = log move j → j + 1
L1  δ[0] ← e[0][0],  δ[j] ← -∞ for j = 1 .. S - 1
L2  for t ← 1 to T - 1 do            ▷ fill δ' from δ, start with δ' = -∞, then set δ ← δ'
L3      for j ← lo_t to hi_t do
L4          stay ← δ[j] + a[j],  move ← δ[j - 1] + m[j - 1]  (move ← -∞ if j = 0)
L5          if move > stay then δ'[j] ← move + e[t][j],  ψ_t[j] ← j - 1    ▷ a tie keeps the self loop
L6          else δ'[j] ← stay + e[t][j],  ψ_t[j] ← j
L7  if δ[S - 1] = -∞ then error "every path has probability 0"
L8  q_{T-1} ← S - 1;  for t ← T - 1 down to 1 do q_{t-1} ← ψ_t[q_t]
L9  return q_0 .. q_{T-1} and δ[S - 1]
```

The value $\delta[j]$ after the pass for frame $t$ is the best log score of a path prefix that ends in state $j$ at frame $t$. The back pointer $\psi_t[j]$ records whether that prefix stayed or moved at the last step. The phone and word spans follow from the states: a phone spans the frames of its 3 states, and a word spans the frames of its phones.

## Example

Align the word "cat", with the phones k, ae and t, to $T = 6$ frames. To keep the table small, each phone has one state here, so $S = 3$. Every self loop and every move has probability 0.5. The emission probabilities $b_j(o_t)$ are:

| frame $t$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| k | 0.8 | 0.6 | 0.2 | 0.1 | 0.1 | 0.1 |
| ae | 0.1 | 0.3 | 0.7 | 0.6 | 0.2 | 0.1 |
| t | 0.1 | 0.1 | 0.1 | 0.3 | 0.7 | 0.8 |

The table below gives $\exp(\delta)$ after each frame, so the numbers are probabilities. The code stores their logs. A dot marks a cell outside $lo_t \ldots hi_t$.

| frame $t$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| k | 0.8 | 0.24 | 0.024 | 0.0012 | · | · |
| ae | · | 0.12 | 0.084 | 0.0252 | 0.00252 | · |
| t | · | · | 0.006 | 0.0126 | 0.00882 | 0.003528 |

For example, at frame 2 the state ae can stay ($0.12 \cdot 0.5 = 0.06$) or come from k ($0.24 \cdot 0.5 = 0.12$). The move is better, so $\delta = 0.12 \cdot 0.7 = 0.084$ and the back pointer is k. At frame 4 the state k is skipped: from k, two frames are not enough to pass through ae and reach t.

The final score is $0.003528$, or $\log 0.003528 = -5.647024$. The back pointers from (frame 5, t) give the path k k ae ae t t, so k spans frames 0 to 1, ae frames 2 to 3 and t frames 4 to 5. There are $\binom{5}{2} = 10$ paths. The next best ones, k ae ae ae t t and k k ae t t t, both have the probability $0.001764$.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It is an induction on $t$ with the invariant that $\delta[j]$ is the best score of a path prefix that ends in state $j$ at frame $t$, for every $j$ in $lo_t \ldots hi_t$, and $-\infty$ elsewhere. The last step of a prefix that ends in $j$ comes from $j$ or from $j - 1$, and the score is a sum along the path, so lines L4 to L6 compute the best prefix from the two best shorter prefixes. At the last frame, $lo_{T-1} = hi_{T-1} = S - 1$, so $\delta[S-1]$ is the best full score, and the back pointers give a path with that score.

The tie rule of line L5 picks one path among the optimal ones: the path whose reversed state sequence is the largest in lexicographic order. Read from the end, each state keeps as many frames as an optimal path allows. The proof also shows that in floating point the code returns the exact maximum of the rounded path scores, because rounding to nearest is monotone.

## Complexity

In the floating-point model, each cell of lines L4 to L6 costs a constant number of additions and comparisons. The band $lo_t \ldots hi_t$ of a frame has at most $\min(S, T - S + 1)$ cells, so the recursion makes $O(T \min(S, T - S + 1))$ steps. This is $\Theta(T S)$ when $T \ge 2S$, the usual case, and only $\Theta(T)$ when $T = S$. The emission scores are a separate cost: $T S$ evaluations of $\log b_j(o_t)$, each $O(M d)$ for a Gaussian mixture with $M$ components of dimension $d$. In practice this term is larger than the recursion.

The array $\delta$ needs $\Theta(S)$ numbers. The back pointers need $\Theta(T S)$ entries, one per cell, which is the $\Theta(T S)$ space in the front matter. Each pointer is one of two values, so one bit per cell is enough. To use less memory, store $\delta$ at every $\sqrt{T}$-th frame only, and recompute the pointers of one block of frames at a time during the traceback. This needs $O(S \sqrt{T})$ memory and about twice the time.

Compare the general [Viterbi algorithm](/viterbi-algorithm/), which takes $\Theta(T N^2)$ time for $N$ states with a full transition matrix. The chain of the transcript has two arcs per state, so each cell looks at two predecessors, not $N$.

## Properties

- **Exact for the model.** The path has the highest $P(O, Q \mid \lambda_W)$ among all paths of the chain. It is not the most accurate segmentation in any other sense; its boundaries are only as good as the acoustic model.
- **Log space.** The test aligns 200 frames whose plain product of probabilities is 0.0 in double precision, and the log version recovers the planted boundaries. Scaling (Rabiner 1989, Section V.A) also works for the forward sum, but log space is the simple choice for a maximum.
- **A minimum duration.** Without skips, each state takes at least one frame, so a phone with 3 states takes at least 3 frames, which is 30 ms at a 10 ms frame step.
- **A fixed tie rule.** Ties keep the self loop, so later states get as many frames as an optimal path allows.

## Variants and improvements

- **Optional silence and alternative pronunciations.** Add an optional silence model between words, and parallel branches for words with more than one pronunciation. The chain becomes a directed acyclic graph of states per frame, and the same recursion runs over the predecessors of each state, in [topological order](/topological-sort/) of the graph. This is what recognizers do in practice.
- **Beam pruning.** Keep only the cells within a fixed log score of the best cell at each frame. This saves time on long utterances, but it is no longer exact.
- **Neural acoustic scores.** A [hybrid DNN-HMM](/hybrid-dnn-hmm/) gives state posteriors. Dividing by the state priors gives scaled likelihoods, and the alignment is unchanged.
- **CTC alignment.** A [CTC](/connectionist-temporal-classification/) model aligns with the same kind of chain, with a blank between the labels.
- **Soft alignment.** The [forward-backward algorithm](/forward-backward-algorithm/) on the same chain gives the posterior of each state at each frame, in place of one best path. Baum-Welch training uses these posteriors; [Viterbi training](/viterbi-training/) uses the forced alignment.
- **Explicit durations.** A [hidden semi-Markov model](/hidden-semi-markov-model/) replaces the geometric durations of the self loops by explicit duration distributions, at a higher cost.

## When to use it

Use forced alignment when the words are known and you need their times. It segments the training data of HMM recognizers, which is the alignment step of [Viterbi training](/viterbi-training/). It also gives phone labels for corpus phonetics, durations for speech synthesis, and word times for subtitles. If the words are not known, use a decoder with a language model instead.

## Pitfalls

- **A wrong transcript.** A missing word, a repeated word or a hesitation that is not in the transcript forces the frames onto the wrong phones, and the error spreads to the neighbors. Add optional silence and filler models, and check alignments with a very low score per frame.
- **Too few frames.** If $T < S$, no path exists. Fast speech and short words with many states can cause this.
- **Products of probabilities.** A product over a few hundred frames underflows to 0 in double precision, and then every path looks the same. Add logs.
- **A large negative number for log 0.** Use $-\infty$. A finite stand-in can make an impossible path look possible after many additions.
- **Missing words in the lexicon.** A word with no pronunciation stops the alignment. Use [grapheme-to-phoneme conversion](/grapheme-to-phoneme-conversion/) for such words.

## Implementations

## History

Vintsyuk 1968 matched speech against word templates by dynamic programming, the same recursion that Viterbi published in 1967 for convolutional codes. When HMMs became the standard acoustic model, the Viterbi search through the HMM of a known transcript became the usual way to segment training data and to label speech corpora (Rabiner 1989; Gales and Young 2008).

## References
