---
tag: Z0KB29
kind: algorithm
slug: joint-sequence-g2p
name: Joint-sequence grapheme-to-phoneme model
aliases:
- graphone model
- Bisani-Ney G2P
area: natural-language-and-speech/speech-analysis-and-synthesis
level: advanced
summary: "Grapheme-to-phoneme conversion with an n-gram model over graphones, pairs of a letter chunk and a phoneme chunk, trained by EM over all joint segmentations and decoded by Viterbi."
solves: [grapheme-to-phoneme-conversion]
model: word-ram
complexity:
  vars: {n: the number of letters of a word, m: the number of phonemes of its pronunciation, H: the number of graphone histories, k: "the number of graphone shapes, L_g (L_p + 1)"}
  time: {worst: "Θ(n m H k)"}
  space: {extra: "Θ(n m H)"}
properties: {deterministic: true, exact: false, online: false, in_place: false}
history:
  year: 2008
  people: [Maximilian Bisani, Hermann Ney]
  note: Bisani and Ney gave the full joint-sequence model with EM training, smoothing and a study of graphone sizes and model orders. Joint n-gram models of letter and phoneme pairs appeared a few years before, for example in Chen 2003.
prereqs: [grapheme-to-phoneme-conversion, n-gram-language-model, expectation-maximization]
see_also: [forward-backward-algorithm, viterbi-algorithm, pronunciation-lexicon, kneser-ney-smoothing, finite-state-transducer, baum-welch-algorithm, text-to-speech, encoder-decoder-model]
sources:
  - paper: doi:10.1016/j.specom.2008.01.002
    title: Maximilian Bisani and Hermann Ney, Joint-sequence models for grapheme-to-phoneme conversion, Speech Communication 50(5), 2008, pages 434 to 451
    locator: the graphone definition, the EM training over joint segmentations, the smoothed M-gram model, the maximum approximation in decoding, and the experiments on graphone size and model order
  - paper: "Stanley F. Chen, Conditional and joint models for grapheme-to-phoneme conversion, Eurospeech 2003, pages 2033 to 2036"
    title: Chen 2003
    locator: the joint n-gram model over aligned letter and phoneme units
  - paper: doi:10.1111/j.2517-6161.1977.tb01600.x
    title: Arthur P. Dempster, Nan M. Laird and Donald B. Rubin, Maximum likelihood from incomplete data via the EM algorithm, Journal of the Royal Statistical Society Series B 39(1), 1977, pages 1 to 38
    locator: Theorem 1 (the likelihood does not decrease)
---

The joint-sequence model converts the spelling of a word into its phonemes. It treats a word and its pronunciation as one sequence of *graphones*: each graphone pairs a short chunk of letters with a short chunk of phonemes, so "six" with the pronunciation S IH K S can be read as s:S, i:IH, x:K S. An [n-gram model](/n-gram-language-model/) gives the probability of a graphone sequence. The alignment of letters to phonemes is not in the training data, so the model is trained with [expectation-maximization](/expectation-maximization/) over all the ways to cut a pair into graphones, which is the [forward-backward algorithm](/forward-backward-algorithm/) on a lattice. A new word is converted by a [Viterbi](/viterbi-algorithm/) search for the best graphone sequence that spells it. Bisani and Ney (2008) gave the full method. It solves [grapheme-to-phoneme conversion](/grapheme-to-phoneme-conversion/) and was a standard baseline before neural sequence models.

## In plain words

English spelling does not map letter by letter to sounds. The letter x often makes two sounds, and some letters make none. The model learns small pieces that pair a few letters with a few sounds, and it learns which pieces tend to follow which.

A dictionary gives words and their sounds, but not which letters go with which sounds. So the training starts with all pieces equally likely. For each word it looks at every way to cut the word and its sounds into pieces, and it gives each way a weight from the current model. It counts the pieces with these weights and makes new probabilities from the counts. This repeats until the numbers stop changing.

To read a new word, it finds the chain of pieces that spells the word and has the highest probability, and outputs their sounds.

## The problem

The input for training is a lexicon of pairs $(g, \varphi)$, where $g = g_1 \ldots g_n$ is a string of letters and $\varphi = \varphi_1 \ldots \varphi_m$ is a string of phonemes. A *graphone* is a pair $q = (q^g, q^\varphi)$ of a letter string and a phoneme string. In this page and its code, $1 \le |q^g| \le L_g$ and $0 \le |q^\varphi| \le L_p$. A *joint segmentation* of $(g, \varphi)$ is a graphone sequence $Q = q_1 \ldots q_K$ with $q_1^g \cdots q_K^g = g$ and $q_1^\varphi \cdots q_K^\varphi = \varphi$. Let $S(g, \varphi)$ be the set of these.

The model is an $M$-gram over graphones with the history padded by $\langle s\rangle$ and an end symbol $\langle/s\rangle$:

$$P(Q) = \prod_{k=1}^{K+1} p(q_k \mid q_{k-M+1} \ldots q_{k-1}), \qquad q_{K+1} = \langle/s\rangle, \qquad p(g, \varphi) = \sum_{Q \in S(g, \varphi)} P(Q).$$

Training asks for the parameters that maximize $\sum \log p(g, \varphi)$ over the lexicon. Conversion asks, for a new $g$, for

$$\hat\varphi = \text{the phonemes of } \arg\max_{Q:\ q_1^g \cdots q_K^g = g} P(Q).$$

This is the *maximum approximation*: the exact rule would maximize $p(g, \varphi)$, a sum over segmentations, over $\varphi$.

## The algorithm

A state of the lattice of a pair is $(i, j, h)$: $i$ letters and $j$ phonemes are covered, and $h$ is the history, the last $M - 1$ graphones. Write $h \oplus q$ for the history after $q$. TRAIN works in the log semiring for sums and DECODE in the Viterbi semiring (max, +). All logs are natural, and $\log 0 = -\infty$.

```pseudo id=main
TRAIN(lexicon, M, L_g, L_p, iterations)
L1  p ← uniform over the graphones that occur in some joint segmentation, and ⟨/s⟩
L2  repeat iterations times
L3      c(h, q) ← 0 for every history h and graphone or end symbol q
L4      for each pair (g, φ) in the lexicon do
L5          run FORWARD(g, φ) and the mirror BACKWARD pass; Z ← p(g, φ)
L6          for each lattice state (i, j, h) and each graphone q that leaves it do
L7              c(h, q) ← c(h, q) + α(i, j, h) · p(q | h) · β(i + |q^g|, j + |q^φ|, h ⊕ q) / Z
L8      p(q | h) ← c(h, q) / Σ_q' c(h, q') for each h
L9  return p

FORWARD(g, φ)                                         ▷ log semiring
L10 log α(0, 0, ⟨s⟩^(M-1)) ← 0
L11 for i ← 0 to |g| - 1, j ← 0 to |φ|, and each h with α(i, j, h) > 0 do
L12     for each q = (g[i .. i+a), φ[j .. j+b)) with 1 ≤ a ≤ L_g and 0 ≤ b ≤ L_p that fits do
L13         h' ← h ⊕ q
L14         log α(i+a, j+b, h') ← log_add(log α(i+a, j+b, h'), log α(i, j, h) + log p(q | h))
L15 return log Z = log_sum over h of log α(|g|, |φ|, h) + log p(⟨/s⟩ | h)

DECODE(g)                                             ▷ Viterbi semiring
L16 δ(0, ⟨s⟩^(M-1)) ← 0
L17 for i ← 0 to |g| - 1 and each h with δ(i, h) > -∞ do
L18     for each graphone q of the model with q^g = g[i .. i+a), 1 ≤ a ≤ L_g do
L19         if δ(i, h) + log p(q | h) > δ(i+a, h ⊕ q) then store it and the back pointer (i, h, q)
L20 h* ← the h that maximizes δ(|g|, h) + log p(⟨/s⟩ | h)
L21 follow the back pointers from (|g|, h*) and return the phonemes of the graphones
```

Line L7 is the expected number of times $q$ follows $h$, the posterior of the arc. The end symbol gets the count $\alpha(|g|, |\varphi|, h)\, p(\langle/s\rangle \mid h) / Z$. Line L8 is the plain maximum likelihood estimate. Bisani and Ney smooth it instead, with discounting of the fractional counts and a cut of small counts; the code here does not smooth, so a graphone never seen after a history keeps probability 0. In the code, every graphone has at least one letter, so the lattice is acyclic in $i$. Bisani and Ney also allow graphones with no letters, which needs a limit on how many come in a row.

**Tie rule.** DECODE visits the states and the graphones in a fixed sorted order, and line L19 replaces a stored value only by a strictly larger one, so the first maximizer in that order wins.

## Example

Take the lexicon six S IH K S, fix F IH K S, box B AA K S, fox F AA K S, sit S IH T and bit B IH T, with $M = 1$ (a unigram over graphones), $L_g = 1$ and $L_p = 2$. Each letter takes 0, 1 or 2 phonemes. There are 36 graphones that occur in some joint segmentation, so the uniform start gives each of the 37 events (with $\langle/s\rangle$) the probability $1/37$.

The pair six, S IH K S has 6 joint segmentations: the ways to write 4 as an ordered sum of 3 parts, each part at most 2. All have 3 graphones, so the uniform model gives each the same weight and the first E step gives each the posterior $1/6$. The table shows the posteriors under the model after one EM iteration and after 30.

| joint segmentation of six | after 1 iteration | after 30 iterations |
|---|---|---|
| s:(none) i:S IH x:K S | 0.0798 | 0.0000 |
| s:S i:IH x:K S | 0.2689 | 1.0000 |
| s:S i:IH K x:S | 0.0965 | 0.0000 |
| s:S IH i:(none) x:K S | 0.4053 | 0.0000 |
| s:S IH i:K x:S | 0.0996 | 0.0000 |
| s:S IH i:K S x:(none) | 0.0498 | 0.0000 |

After one iteration the wrong cut s:S IH, i:(none) is the most likely, because s:S IH is helped by sit and the empty i is cheap. The other words pull the model to the right cut: x:K S occurs in four words and i:IH in four. The log likelihood of the lexicon rises from $-75.6032$ under the uniform model to $-47.5009$, and the model converges to $p(\langle/s\rangle) = 1/4$, $p(\text{i:IH}) = p(\text{x:K S}) = 1/6$ and $1/12$ each for s:S, o:AA, t:T, f:F and b:B. There are 24 events in the lexicon, and these are their relative frequencies under the cuts s:S i:IH x:K S and so on.

DECODE on the unseen word sob finds s:S, o:AA, b:B with log score $\log(1/12^3 \cdot 1/4) = -8.8410$, and outputs S AA B.

## Correctness

The proofs file has three parts. First, the joint segmentations of $(g, \varphi)$ are in bijection with the lattice paths from $(0, 0, \langle s\rangle^{M-1})$ to an end state, and a path has the weight of its graphone sequence. Each graphone has a letter, so increasing $i$ is a topological order, and an induction on $i$ shows that line L14 accumulates the exact sum over paths into each state; line L15 then returns $\log p(g, \varphi)$. Second, splitting each path at an arc shows that line L7 adds the exact posterior expected count of each graphone after each history. Third, line L8 maximizes the expected complete-data log likelihood row by row, so this is an EM step and the log likelihood of the lexicon never decreases (Dempster, Laird and Rubin 1977, Theorem 1). It can stop at a local maximum. DECODE is the same induction in the Viterbi semiring, and it returns a graphone sequence of the largest weight.

## Complexity

A lattice for a pair has at most $(n + 1)(m + 1) H$ states, where $H$ is the number of histories, and $k = L_g (L_p + 1)$ arcs leave each state. FORWARD, BACKWARD and the count loop each take $\Theta(n m H k)$ time and $\Theta(n m H)$ space, so one EM iteration costs this sum over the lexicon. For $M = 1$, $H = 1$. For larger $M$, $H$ can grow like the number of graphones to the power $M - 1$, but only histories seen in the lattice are stored. DECODE takes $\Theta(n H L_g G)$ time, where $G$ is the largest number of graphones with the same letter chunk.

The brute force alternative lists the segmentations: with $L_g = L_p = 1$ a pair has $\binom{n}{m}$ of them, and with $L_g = 1$, $L_p = 2$ the count is the coefficient of $x^m$ in $(1 + x + x^2)^n$, which grows exponentially.

## Properties

- **One model for alignment and conversion.** The same graphone n-gram aligns the training pairs and scores new words, so no separate alignment step or hand rules are needed.
- **Generative and joint.** It models $p(g, \varphi)$, not $p(\varphi \mid g)$. The same model can convert phonemes to letters by decoding on the phoneme side.
- **Local optimum.** EM increases the likelihood but can stop at a local maximum. Bisani and Ney train in stages, from small to large $M$, and start each stage from the previous model.
- **Free of underflow.** The lattice works with log values, so long words do not round to zero.
- **A weighted transducer.** The trained model is a [weighted automaton](/weighted-automaton/) over graphones, which is a [finite-state transducer](/finite-state-transducer/) from letters to phonemes; DECODE is a shortest path search through its composition with the word.

## Variants and improvements

- **Graphone size.** With singular graphones (at most one letter and one phoneme each) and a long history, the model does well; larger graphones are prone to overfit (measurement, reported by Bisani and Ney and by later work that cites them).
- **Smoothing.** Bisani and Ney discount the fractional expected counts in a way close to [Kneser-Ney smoothing](/kneser-ney-smoothing/), and drop counts below a threshold in the E step.
- **Sum over segmentations.** Instead of the maximum approximation, decode with an n-best list of graphone sequences and add the probabilities of the ones with the same phonemes.
- **Viterbi training.** Replace the expected counts by the counts on the best segmentation of each pair, as Viterbi training does for an [HMM](/hidden-markov-model/). Each iteration is cheaper, but it maximizes the weight of the best segmentation, not the likelihood.
- **Neural models.** An [encoder-decoder model](/encoder-decoder-model/) or a [transformer](/transformer/) maps letters to phonemes with no explicit alignment, and is now the usual choice when the lexicon is large.

## When to use it

Use it for a [pronunciation lexicon](/pronunciation-lexicon/) that must cover new words: names, loan words and new terms in a [text-to-speech](/text-to-speech/) front end or an [automatic speech recognition](/automatic-speech-recognition/) system. It needs no aligned data, has few settings and gives a probability for each output, which helps when a recognizer wants several pronunciations per word. For a large lexicon with plenty of compute, a neural sequence model is usually more accurate.

## Pitfalls

- **Graphones with no letters.** If a graphone may have an empty letter side, the lattice is no longer ordered by $i$ and can have cycles. Limit the number of such graphones in a row, or forbid them as this code does.
- **No smoothing.** With the plain maximum likelihood M step, a history not seen in training has no outgoing probability and DECODE fails on many new words. Smooth the M-gram before use on real data.
- **Testing on training words.** The model fits its training lexicon very well. Report phoneme or word error rates on held-out words.
- **The uniform start.** With all graphones equally likely, the first E step favors segmentations with fewer and longer graphones, since each graphone costs one factor. The example shows a wrong cut that wins after one iteration; run EM until the likelihood stops rising.
- **Ties.** Two segmentations can have equal weight. Fix a tie rule if outputs are compared.

## Implementations

## History

Rule systems for letter to sound conversion came first, followed by data-driven methods that needed a fixed one-to-one alignment of letters and phonemes. Joint n-gram models over letter and phoneme units, with the alignment learned by EM, appeared around 2000, and Chen (2003) compared joint and conditional models of this kind. Maximilian Bisani and Hermann Ney, at RWTH Aachen, gave the full joint-sequence framework in 2008, with the name graphone, the EM training with smoothing, and a study of graphone size and model order on several pronunciation lexica. Bisani released the method as the Sequitur G2P tool, which became a common baseline. Neural sequence models have since replaced it in many systems.

## References
