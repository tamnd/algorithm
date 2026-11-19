---
tag: NXHD7B
kind: algorithm
slug: ctc-prefix-beam-search
name: CTC prefix beam search
aliases:
- prefix beam search
- CTC beam search decoding
area: natural-language-and-speech/speech-recognition
level: advanced
summary: Beam search over output prefixes of a CTC model that merges paths giving the same prefix, tracking blank and non-blank endings.
solves: [automatic-speech-recognition]
model: word-ram
complexity:
  vars: {T: the number of frames, K: the number of output symbols with the blank, W: the beam width}
  time: {worst: "O(T W K)"}
  space: {extra: "O(W K + T W)"}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 2014
  people: [Awni Y. Hannun, Andrew L. Maas, Daniel Jurafsky, Andrew Y. Ng]
  note: Graves et al. described prefix search decoding for CTC in 2006. Hannun, Maas, Jurafsky and Ng gave the beam version with an n-gram language model for large vocabulary recognition in 2014.
prereqs: [connectionist-temporal-classification, beam-search]
see_also: [greedy-decoding, shallow-fusion, n-gram-language-model, joint-ctc-attention, rnn-transducer, time-synchronous-beam-search, top-k-selection, length-normalization]
sources:
  - paper: "Awni Y. Hannun, Andrew L. Maas, Daniel Jurafsky and Andrew Y. Ng, First-pass large vocabulary continuous speech recognition using bi-directional recurrent DNNs, arXiv:1408.2873, 2014 (preprint)"
    title: The prefix beam search with a language model and an insertion bonus
    locator: "Section 3 (decoding, eqs. 7 to 9), Algorithm 1 and Table 1"
  - paper: doi:10.1145/1143844.1143891
    title: "Alex Graves, Santiago Fernández, Faustino Gomez and Jürgen Schmidhuber, Connectionist temporal classification: labelling unsegmented sequence data with recurrent neural networks, ICML 2006, pages 369 to 376"
    locator: Section 3.2 (best path decoding and prefix search decoding)
  - paper: doi:10.1109/JSTSP.2017.2763455
    title: Shinji Watanabe, Takaaki Hori, Suyoun Kim, John R. Hershey and Tomoki Hayashi, Hybrid CTC/attention architecture for end-to-end speech recognition, IEEE Journal of Selected Topics in Signal Processing 11(8), 2017, pages 1240 to 1253
    locator: the section on joint decoding with the CTC prefix score
---

CTC prefix beam search finds a likely label sequence from the per-frame outputs of a [CTC](/connectionist-temporal-classification/) network. Many frame-level paths collapse to the same labels, so the probability of a labeling is a sum over paths, and the best single path does not give the best labeling. The search therefore keeps label prefixes, not paths. For each prefix it stores two numbers: the probability of the paths that end in a blank, and of the paths that end in the last label. These two numbers are enough to extend the prefix by one frame exactly. A beam keeps the $W$ best prefixes after each frame, and a language model can be added when a label is appended.

## In plain words

A CTC network gives, for every short slice of sound, how likely each letter is and how likely "nothing" (the blank) is. Many slice-by-slice outputs spell the same text: "c_aa_t" and "cc_a_tt" both spell "cat". The text you want is the one whose outputs add up to the most.

The search reads the slices one by one and keeps a short list of the best partial texts. For each partial text it remembers two totals: the outputs that end in a blank, and those that end in the last letter. The split matters for doubled letters: after "a", another "a" continues the same letter, but after "a_", another "a" starts a new one. At the end, the best text on the list is the answer. A longer list costs more time but loses less.

## The problem

The input is a $T \times K$ matrix of output probabilities $y_t(k)$ of a CTC network, for frames $t = 1, \ldots, T$ and symbols $k$ in $L \cup \{\varnothing\}$. The blank is written $\varnothing$ in formulas, "_" in examples and index 0 in the code. The map $\mathcal{B}$ merges runs of equal symbols and then deletes the blanks, and

$$p(\ell \mid x) = \sum_{\pi : \mathcal{B}(\pi) = \ell} \prod_{t=1}^{T} y_t(\pi_t).$$

The task is to find $\ell^* = \arg\max_\ell \, p(\ell \mid x)\, \Lambda(\ell)$, where $\Lambda(\ell)$ is an optional language model weight. Hannun et al. (2014) use $\Lambda(W) = p_{\mathrm{LM}}(W)^{\alpha} |W|^{\beta}$ for a word sequence $W$, with a weight $\alpha$ and an insertion bonus $\beta$ set on held-out data. The code here takes a hook $\mathrm{lm}(\ell, c)$ that returns the log weight of appending label $c$ to the prefix $\ell$, and $\ln \Lambda(\ell)$ is the sum of the hook along $\ell$. Without a language model, $\Lambda = 1$.

The number of labelings grows exponentially in $T$. With a beam that keeps every prefix the search is exact, and it then costs exponential time. With a fixed beam it is a heuristic.

## The algorithm

For a prefix $\ell$ after frame $t$, $b(\ell)$ is the log probability of the paths of frames $1..t$ that collapse to $\ell$ and end in $\varnothing$, and $nb(\ell)$ the same for the paths that end in a label, which must be $\ell_{\mathrm{end}}$, the last label of $\ell$. $\oplus$ is log_add, $a \oplus b = \ln(e^a + e^b)$, and $x \mathrel{\oplus}= v$ means $x \leftarrow x \oplus v$. A missing entry of the map $N$ is $(-\infty, -\infty)$.

```pseudo id=main
PREFIX-BEAM-SEARCH(ln y, W, lm)   ▷ ln y: T × K log outputs, ∅ = index 0, lm(ℓ, c) = 0 if no LM; ln is the natural log
L1  A ← { ε : (b = 0, nb = -∞) }
L2  for t ← 1 to T do
L3      N ← empty map
L4      for each prefix ℓ in A, with (b, nb) = A[ℓ] do
L5          N[ℓ].b ⊕= ln y_t(∅) + (b ⊕ nb)                 ▷ a blank keeps the prefix
L6          if ℓ ≠ ε then N[ℓ].nb ⊕= ln y_t(ℓ_end) + nb        ▷ the run of the last label goes on
L7          for each label c do
L8              if c = ℓ_end then s ← b else s ← b ⊕ nb         ▷ a repeated label needs a blank between
L9              N[ℓ c].nb ⊕= ln y_t(c) + s + lm(ℓ, c)
L10     A ← the W prefixes of N with the largest b ⊕ nb
L11 return the prefix in A with the largest b ⊕ nb, and that score
```

Line L8 is the reason for the two numbers. If the new label equals the last label of $\ell$, only the paths that end in a blank start a new copy of it; the paths that end in the label merge with it and stay in $\ell$ (line L6). Every update accumulates with $\oplus$. Algorithm 1 of Hannun et al. (2014) writes some of these updates as assignments, but two different prefixes, or the same prefix by two routes, can add to the same entry, so an assignment loses probability. This is a known source of bugs.

Hannun et al. also handle a prefix $\ell^+ = \ell c$ that was scored at the previous frame but pruned: when $\ell$ makes $\ell^+$ again, they add the blank and repeat continuations of the old scores of $\ell^+$. The code has this as the option recover. It does not change the result of a full beam, and it can only add probability.

## Example

Use the outputs of the example on the CTC page, with the alphabet {_, a, b} and $T = 3$:

| frame | _ | a | b |
|---|---|---|---|
| 1 | 0.5 | 0.4 | 0.1 |
| 2 | 0.4 | 0.3 | 0.3 |
| 3 | 0.3 | 0.1 | 0.6 |

The scores below are probabilities $e^{b} + e^{nb}$; the code stores logs. With a beam of $W = 3$:

| after frame | kept prefixes | pruned |
|---|---|---|
| 1 | ε 0.5, a 0.4, b 0.1 | none |
| 2 | a 0.43, b 0.22, ε 0.2 | ab 0.12, ba 0.03 |
| 3 | b 0.294, ab 0.258, a 0.176 | |

After frame 2, the prefix "a" has $b = 0.16$ (the path a_) and $nb = 0.27$ (the paths _a and aa). At frame 3, "b" collects $0.22 \cdot 0.3 = 0.066$ by a blank, $0.18 \cdot 0.6 = 0.108$ by repeating b, and $0.2 \cdot 0.6 = 0.12$ from the empty prefix, so 0.294. The prefix "ab" gets only $0.43 \cdot 0.6 = 0.258$ from "a", because its own 0.12 from frame 2 was pruned. The search returns "b", which is wrong.

The exact answer is "ab" with $p = 0.366$; "b" has 0.294. A full beam finds it, and so does $W = 4$. $W = 2$ also returns "ab", but with the score 0.258, because it pruned "b" and "ab" at frame 2. So a wider beam is not always better. With the recover option, $W = 2$ and $W = 3$ both return "ab" with the exact 0.366. Greedy decoding reads _ _ b and returns "b". The tests check all these numbers.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). A path of $t$ frames that collapses to $\ell$ comes from a path of $t - 1$ frames in exactly one of four ways: a blank after a path of $\ell$; the last label again after a path of $\ell$ that ends in that label; the last label after a path of $\ell^-$ that ends in a blank; or the last label after a path of $\ell^-$ that ends in a different label. Lines L5, L6 and L9 add exactly these four terms, so by induction on $t$, with a beam that prunes nothing, $b$ and $nb$ are exact and line L11 returns a maximizer of $p(\ell \mid x)\Lambda(\ell)$ (a theorem). With pruning, every stored value is a sum over a subset of the paths, so the returned score is a lower bound on the true score of the returned prefix. There is no guarantee about which prefix is returned (see the example).

## Complexity

Each frame touches at most $W$ prefixes and does $O(K)$ log_add operations for each one, so it scores at most $W K$ entries. Selecting the best $W$ of them takes $O(W K)$ time with a linear time [top-k selection](/top-k-selection/), or $O(W K \log(W K))$ with a sort, as in the code. The total is $O(T W K)$ log_add operations in the word-RAM model, plus the selection, plus the language model calls. Storing prefixes as nodes of a trie makes each extension $O(1)$; the code uses tuples, which costs $O(n)$ for a prefix of length $n$. The map of a frame has at most $W K$ entries, and the trie of the kept prefixes has at most $T W$ nodes, which gives the space bound.

In practice the beam is large: Hannun et al. used $W = 200$ over a character alphabet. Frames where the blank has almost all the probability can be skipped, and symbols with a very small $y_t(c)$ can be left out of line L7.

## Properties

- **Exact with a full beam.** It returns the most probable labeling (a theorem). The number of prefixes is then exponential in $T$.
- **Not exact with a finite beam.** It may return a wrong labeling, and the error is not monotone in $W$ (the example).
- **Better than greedy decoding in practice.** Greedy decoding returns the labeling of the most probable path, which is not in general the most probable labeling (Graves et al. 2006, Section 3.2). A beam of 1 is not the same as greedy decoding, because it ranks by the summed probability of the prefix.
- **Online.** It reads one frame at a time and can output the common part of the prefixes in the beam while the audio arrives.
- **Language model at word ends.** With a word language model, Hannun et al. apply $p_{\mathrm{LM}}$ when a space is appended, so the weight of a word is known only when the word ends.

## Variants and improvements

- **Prefix search decoding** (Graves et al. 2006) expands the most probable prefix first and stops when no prefix can beat the best complete one. It is exact but can take exponential time; they also split the output at frames where the blank is very likely.
- **Shallow fusion.** Adding the language model inside the search, as here, is [shallow fusion](/shallow-fusion/). Rescoring an n-best list or a [word lattice](/word-lattice/) with a larger model is the other option.
- **WFST decoding.** Compose a CTC token transducer with a lexicon and a grammar and run a [time-synchronous beam search](/time-synchronous-beam-search/) over the graph.
- **CTC prefix scores in attention decoding.** [Joint CTC-attention](/joint-ctc-attention/) decoding scores each output prefix of an attention decoder with the CTC prefix probability (Watanabe et al. 2017).
- **Transducer beam search.** The [RNN transducer](/rnn-transducer/) has its own beam search with a similar merge of prefixes, but its label probabilities depend on the prefix.

## When to use it

Use it to decode a CTC model when a language model is available or when greedy decoding is not accurate enough. On the Wall Street Journal eval92 test set, Hannun et al. measured a word error rate of 35.8% without a language model, 24.4% with a dictionary constraint and 14.1% with a bigram language model, at a beam of 200 (their Table 1). If no language model is used and the outputs are peaky, greedy decoding is much cheaper and often nearly as good.

## Pitfalls

- **Assignment instead of accumulation.** Every update of $b$ and $nb$ must add. Several prefixes and several routes add to the same entry.
- **The repeated label.** Extending $\ell$ by $\ell_{\mathrm{end}}$ uses only $b(\ell)$. Using $b \oplus nb$ makes "a a" read as "aa" and counts the same paths twice.
- **Pruning prefixes of probability 0.** A prefix with more repeats than the frames allow has score $-\infty$. Keep it out of the beam, or a small beam fills up with dead prefixes.
- **Unnormalized language model weights.** With $\alpha$ and $\beta$, the score is no longer a probability, and the best labeling depends on both. Tune them on held-out data.
- **Comparing prefixes of different lengths.** Long prefixes collect more language model penalties; without the insertion bonus $\beta$ the search prefers short outputs. See [length normalization](/length-normalization/).

## Implementations

The code takes the per-frame output distributions of the network as given and implements the prefix beam search with an optional language model hook and the recover step; it does not train a network. The tests compare a full beam with exhaustive search over all labelings for $T \le 6$ and $K \le 3$, with and without a bigram language model.

## History

Graves et al. (2006) defined best path decoding and prefix search decoding for CTC and showed that the first is not exact. Hannun, Maas, Jurafsky and Ng (2014) gave the prefix beam search with an n-gram language model, which made a CTC network without an HMM competitive for large vocabulary recognition. The CTC prefix probability later became a score inside attention decoders (Watanabe et al. 2017).

## References
