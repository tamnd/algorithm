---
tag: BW4ZT9
kind: algorithm
slug: maximum-mutual-information-training
name: Maximum mutual information training
aliases:
- MMI training
- MMIE
area: natural-language-and-speech/speech-recognition
level: advanced
summary: Train acoustic models to maximize the posterior of the correct transcript against competitors from a lattice, a discriminative criterion.
solves: [automatic-speech-recognition, hmm-parameter-learning]
model: floating-point-model
complexity:
  vars: {T: the number of frames, N: the number of states of the numerator and denominator graphs, E: the number of arcs of both graphs, P: the number of pdfs}
  time: {worst: "Θ(T (N + E + P))"}
  space: {extra: "Θ(T (N + P))"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1986
  people: [Lalit R. Bahl, Peter F. Brown, Peter V. de Souza, Robert L. Mercer]
  note: Bahl, Brown, de Souza and Mercer proposed in 1986 to estimate HMM parameters by maximum mutual information instead of maximum likelihood. Woodland and Povey made it work for large vocabulary recognition with lattices in 2002.
prereqs: [baum-welch-algorithm, gmm-hmm-acoustic-model, word-lattice]
see_also: [lattice-free-mmi, hybrid-dnn-hmm, maximum-likelihood-estimation, generative-vs-discriminative-models, forward-backward-algorithm, connectionist-temporal-classification, word-error-rate, pointwise-mutual-information]
sources:
  - paper: doi:10.1109/ICASSP.1986.1169179
    title: Lalit R. Bahl, Peter F. Brown, Peter V. de Souza and Robert L. Mercer, Maximum mutual information estimation of hidden Markov model parameters for speech recognition, ICASSP 1986, pages 49 to 52
    locator: the whole paper (the MMI criterion for HMM parameters)
  - paper: doi:10.1006/csla.2001.0182
    title: Phil C. Woodland and Daniel Povey, Large scale discriminative training of hidden Markov models for speech recognition, Computer Speech and Language 16(1), 2002, pages 25 to 47
    locator: the sections on the MMIE objective, lattice-based training, acoustic scaling and the extended Baum-Welch update
  - paper: "P. S. Gopalakrishnan, Dimitri Kanevsky, Arthur Nádas and David Nahamoo, An inequality for rational functions with applications to some statistical estimation problems, IEEE Transactions on Information Theory 37(1), 1991, pages 107 to 113"
    title: The extended Baum-Welch growth transform for rational objectives
    locator: the main theorem and its application to discrete HMM parameters
  - paper: doi:10.1007/978-1-4613-1367-0_3
    title: "Yves Normandin, Maximum mutual information estimation of hidden Markov models, in Automatic Speech and Speaker Recognition: Advanced Topics, Kluwer, 1996, pages 57 to 81"
    locator: the chapter (the extended Baum-Welch update for Gaussian densities)
---

Maximum mutual information (MMI) training is a way to estimate the parameters of an HMM acoustic model. Maximum likelihood training makes the audio likely under the model of the correct transcript and ignores the other transcripts. MMI makes the correct transcript likely compared with all the others: it maximizes the log posterior probability of the reference words given the audio. The objective is a difference of two log sums over paths, one over the paths of the reference (the numerator) and one over the paths of all competing transcripts (the denominator, in practice a [word lattice](/word-lattice/)). A [forward-backward](/forward-backward-algorithm/) pass over each graph gives the objective and its exact gradient: the acoustic scale times the difference of the two state posteriors. The parameters then move by gradient steps or by the extended Baum-Welch update.

## In plain words

A recognizer makes errors when a wrong sentence scores almost as high as the right one. Ordinary training only pushes the right sentence up. It never looks at the wrong sentences, so it does not learn what to tell apart.

MMI training looks at both. For each training recording it builds two networks of sound units: one for the right sentence, and one for every sentence the recognizer considers likely. It then asks what share of the total score goes to the right sentence, and it changes the model to make that share larger. A sound unit that the right sentence uses gets pushed up. A unit that the wrong sentences use gets pushed down. When the right sentence already takes almost all of the score, the push is close to zero. So the training spends its effort on the confusable parts.

## The problem

Training data are utterances $r = 1, \ldots, R$ with audio $O_r$ (frames $o_1, \ldots, o_T$) and reference word sequences $W_r$. The acoustic model gives, for each pdf $p$ (a tied HMM state) and frame $t$, a log likelihood $\ell_t(p) = \ln p_\theta(o_t \mid p)$, from a Gaussian mixture, a discrete distribution or a scaled network output. The language model $P(W)$ is fixed. The MMI objective with acoustic scale $\kappa$ is

$$F(\theta) = \sum_{r=1}^{R} \ln \frac{p_\theta(O_r \mid M_{W_r})^{\kappa} P(W_r)}{\sum_{W} p_\theta(O_r \mid M_W)^{\kappa} P(W)},$$

where $M_W$ is the HMM of the word sequence $W$ and $p_\theta(O \mid M_W)$ sums over its state paths. With $\kappa = 1$ and a fixed language model, maximizing $F$ is the same as maximizing an estimate of the mutual information between words and audio, which gives the name. The task is to compute $F$ and $\partial F / \partial \ell_t(p)$, and then to improve $\theta$.

Both sums are sums over the paths of a graph. Write the numerator graph $G_{\mathrm{num}}$ for the paths of $W_r$ and the denominator graph $G_{\mathrm{den}}$ for the paths of all $W$ (it must hold the numerator). A path $q_1 \ldots q_T$ of states has the score $\mathrm{init}(q_1) + \sum_t w(q_{t-1}, q_t) + \mathrm{final}(q_T) + \kappa \sum_t \ell_t(\mathrm{pdf}(q_t))$, where the arc weights hold the transition, pronunciation and language model log probabilities. Then $F = \ln Z_{\mathrm{num}} - \ln Z_{\mathrm{den}}$ with $Z_G$ the sum of $e^{\mathrm{score}}$ over the paths of $G$. In the code the graph weights hold the frame-level form $\kappa \ell_t$; Woodland and Povey (2002) scale the acoustic likelihoods, which is the same, and also keep the language model unscaled.

## The algorithm

$\oplus$ is log_add, $a \oplus b = \ln(e^a + e^b)$. All logs are natural logs.

```pseudo id=main
MMI-GRADIENT(ℓ, G_num, G_den, κ)   ▷ ℓ: T × P log likelihoods; returns F and dF/dℓ
L1  for G in {G_num, G_den} do
L2      α_1(j) ← init(j) + κ ℓ_1(pdf j);  α_t(j) ← ⊕ over arcs i→j of (α_{t-1}(i) + w(i,j)), plus κ ℓ_t(pdf j)
L3      ln Z_G ← ⊕ over j of (α_T(j) + final(j))
L4      β_T(j) ← final(j);  β_t(i) ← ⊕ over arcs i→j of (w(i,j) + κ ℓ_{t+1}(pdf j) + β_{t+1}(j))
L5      γ^G_t(p) ← Σ over states j with pdf j = p of exp(α_t(j) + β_t(j) - ln Z_G)
L6  F ← ln Z_num - ln Z_den
L7  g_t(p) ← κ (γ^num_t(p) - γ^den_t(p))
L8  return F and g
```

The gradient with respect to the model parameters follows by the chain rule. For a network, $g$ is the error signal at the output layer (after the division by the priors of a [hybrid model](/hybrid-dnn-hmm/)). For discrete output distributions $b_p(v)$ and $\kappa = 1$, the derivative with respect to $\ln b_p(v)$ is $c^{\mathrm{num}}_p(v) - c^{\mathrm{den}}_p(v)$, where $c_p(v)$ sums $\gamma_t(p)$ over the frames with symbol $v$. The extended Baum-Welch (EBW) update is

$$b'_p(v) = \frac{c^{\mathrm{num}}_p(v) - c^{\mathrm{den}}_p(v) + D\, b_p(v)}{\sum_{v'} \left( c^{\mathrm{num}}_p(v') - c^{\mathrm{den}}_p(v') + D\, b_p(v') \right)}.$$

$D$ must keep every value positive. Gopalakrishnan et al. (1991) proved that a large enough $D$ never decreases the objective. Normandin (1996) gave the form for Gaussian means and variances, where each Gaussian gets its own $D$.

## Example

Take two words A and B, each one HMM state with its own pdf (0 and 1) and a self loop of weight 1, a language model with $P(\mathrm{A}) = P(\mathrm{B}) = 0.5$, and $T = 2$ frames with these likelihoods:

| frame | pdf 0 (A) | pdf 1 (B) |
|---|---|---|
| 1 | 0.6 | 0.3 |
| 2 | 0.5 | 0.4 |

The reference is A. With $\kappa = 1$, the numerator graph has one path with weight $0.5 \cdot 0.6 \cdot 0.5 = 0.15$. The denominator holds A and B, with weights 0.15 and $0.5 \cdot 0.3 \cdot 0.4 = 0.06$, so $Z_{\mathrm{den}} = 0.21$. The posterior of A is $0.15 / 0.21 = 0.714286$ and $F = \ln 0.714286 = -0.336472$.

At each frame, $\gamma^{\mathrm{num}} = (1, 0)$ and $\gamma^{\mathrm{den}} = (5/7, 2/7)$, so the gradient is $(+0.285714, -0.285714)$: raise the score of A and lower B, by the posterior mass that B takes. With $\kappa = 0.5$, the weights become $0.5\sqrt{0.30}$ and $0.5\sqrt{0.12}$, the posterior of A falls to 0.612574, and the gradient is $\pm 0.5 \cdot 0.387426 = \pm 0.193713$. A small $\kappa$ makes the competitors stronger, so more of the data gets a non-zero gradient. The tests check these numbers.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). The forward and backward recursions sum $e^{\mathrm{score}}$ over all partial paths, by induction on $t$ and distributivity, so line L3 gives $\ln Z_G$ and line L5 gives the posterior of each pdf at each frame under the distribution of $G$ over its paths. The score of a path depends on $\ell_t(p)$ only by $\kappa$ times the indicator that the path is in pdf $p$ at frame $t$, so $\partial \ln Z_G / \partial \ell_t(p) = \kappa \gamma^G_t(p)$, and line L7 is the exact gradient (a theorem). The gradient of each frame sums to 0. If the denominator holds the numerator paths, $F \le 0$ and $e^F$ is the posterior of the reference.

## Complexity

Each forward or backward step visits every state and every arc once per frame, so one graph costs $\Theta(T (N + E))$ log_add operations, and line L5 and line L7 add $\Theta(T (N + P))$. Space is $\Theta(T N)$ for $\alpha$ and $\beta$ plus $\Theta(T P)$ for the posteriors. In large vocabulary training the denominator is a lattice of the competing hypotheses, generated once by a recognizer with a weak language model, and its size dominates the cost. [Lattice-free MMI](/lattice-free-mmi/) replaces it by a phone graph that is the same for every utterance.

## Properties

- **Exact objective and gradient.** For given graphs, the two forward-backward passes compute $F$ and its gradient exactly (a theorem).
- **A log posterior.** If the denominator holds the numerator, $F \le 0$, and $F = 0$ only when no competitor has weight. Then the gradient is 0 (a corollary).
- **The gradient is a difference of counts.** Statistics of the numerator push up, statistics of the denominator push down, and well-recognized utterances contribute almost nothing.
- **Not concave.** $F$ is a difference of two log sums and has local optima, so training starts from a maximum likelihood model.
- **Matches maximum likelihood only in the limit.** If the model family contains the true distribution and there is unlimited data, both criteria give it. With a wrong model, MMI usually gives a lower error rate.

## Variants and improvements

- **Lattice-based MMI.** The denominator is a word lattice from a first decoding pass, with the time boundaries of the words fixed (Woodland and Povey 2002).
- **Lattice-free MMI.** The denominator is a phone n-gram graph, run on all frames of short chunks (see [lattice-free MMI](/lattice-free-mmi/)).
- **Boosted MMI** adds a term to the competing paths in proportion to their errors, so close competitors weigh more.
- **Minimum phone error (MPE) and state-level minimum Bayes risk (sMBR)** maximize the expected accuracy over the lattice paths instead of the posterior of the reference. They share the lattice and the forward-backward machinery.
- **Sequence training of neural networks.** The same gradient $g$ trains the network of a [hybrid DNN-HMM](/hybrid-dnn-hmm/) model, usually after cross-entropy training.

## When to use it

Use it after maximum likelihood or cross-entropy training of an HMM-based recognizer, to lower the word error rate. It needs a good starting model, the lattices (or a phone graph), and a held-out set to choose $\kappa$, $D$ and the number of iterations. It does not fit end-to-end models such as [CTC](/connectionist-temporal-classification/), which already have a normalized sequence-level loss.

## Pitfalls

- **Acoustic scale.** With $\kappa = 1$ the acoustic scores dwarf the language model, the posterior of the best path is close to 1, and few frames get a gradient. Use the same small scale as in decoding (for example the inverse of the language model weight).
- **The numerator must be in the denominator.** Otherwise $F$ can be positive and is no longer a log posterior; add the reference to each lattice.
- **Too small $D$.** The EBW update can give negative probabilities or variances, or decrease $F$. Set $D$ per pdf from the denominator counts, with a safe lower bound.
- **Over-training.** The objective keeps improving on the training set while the test error rises. Smooth towards the maximum likelihood statistics and stop early.
- **Stale lattices.** The lattices come from an older model. Regenerate them, or use a lattice-free denominator.

## Implementations

The code takes the per-frame log likelihoods and the two graphs as given and computes the objective, its gradient and the extended Baum-Welch update of discrete distributions; it does not train a network. The tests compare the forward pass with a sum over all paths, the gradient with finite differences, and check that the update does not decrease the objective.

## History

Bahl, Brown, de Souza and Mercer (1986) proposed estimating the parameters of a speech HMM by maximum mutual information. Gopalakrishnan, Kanevsky, Nádas and Nahamoo (1991) extended the Baum-Eagon inequality to rational functions, which gave the extended Baum-Welch update for discrete distributions, and Normandin (1996) gave the update for Gaussian densities. Woodland and Povey (2002) made MMI work on large vocabulary tasks with lattices for the denominator, acoustic scaling and a weak language model. Povey et al. (2016) removed the lattices with [lattice-free MMI](/lattice-free-mmi/).

## References
