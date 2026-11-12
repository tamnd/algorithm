---
tag: FTEMPN
kind: problem
slug: hmm-parameter-learning
name: HMM parameter learning
aliases:
- HMM training
- HMM learning problem
area: machine-learning/probabilistic-inference
level: core
summary: "Estimate the start, transition and emission probabilities of a hidden Markov model from observation sequences. Baum-Welch (EM) finds a local maximum of the likelihood."
prereqs: [hidden-markov-model, maximum-likelihood-estimation]
see_also: [baum-welch-algorithm, expectation-maximization, forward-backward-algorithm, viterbi-algorithm, hmm-evaluation, hmm-decoding, gaussian-mixture-model, hidden-semi-markov-model]
sources:
  - paper: doi:10.1109/5.18626
    title: Lawrence R. Rabiner, A tutorial on hidden Markov models and selected applications in speech recognition, Proceedings of the IEEE 77(2), 1989, pages 257 to 286
    locator: "Section II.C (Problem 3 of the three basic problems), Section III.C (no known analytical solution; the Baum-Welch re-estimation finds a local maximum) and Section V.B (several observation sequences)"
  - paper: doi:10.1214/aoms/1177697196
    title: Leonard E. Baum, Ted Petrie, George Soules and Norman Weiss, A maximization technique occurring in the statistical analysis of probabilistic functions of Markov chains, Annals of Mathematical Statistics 41(1), 1970, pages 164 to 171
    locator: the re-estimation step and the proof that it does not decrease the likelihood
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: "Section 13.2.1 (maximum likelihood for the HMM)"
---

HMM parameter learning asks for the parameters $\lambda = (\pi, A, B)$ of a [hidden Markov model](/hidden-markov-model/) that best explain a set of observation sequences. The usual criterion is the [maximum likelihood](/maximum-likelihood-estimation/) $\arg\max_\lambda P(O \mid \lambda)$. It is the third of the three basic HMM problems in Rabiner's tutorial. When the state paths are seen, the answer is a closed formula. When they are hidden, the likelihood is a sum over $N^T$ paths for each sequence, it can have many local maxima, and the standard method, the [Baum-Welch algorithm](/baum-welch-algorithm/), finds a local maximum only.

## In plain words

You have many sequences of symbols and you believe that a hidden process with $N$ states made them. You want the numbers of that process: how it starts, how it moves, and what each state shows. If you could see the states, you would count and divide. You cannot, so you guess, estimate the states from the guess, count with these estimates, and repeat. The result depends on the first guess.

## Definition

**Input:** the number of states $N$, the alphabet $1, \ldots, M$, and $R \ge 1$ sequences $O^{(1)}, \ldots, O^{(R)}$.

**Output:** stochastic $(\pi, A, B)$ that maximize

$$L(\lambda) = \sum_{r=1}^{R} \log P(O^{(r)} \mid \lambda), \qquad P(O \mid \lambda) = \sum_{Q} P(Q, O \mid \lambda).$$

The maximum is not unique: a relabeling of the states gives the same $L$. Methods that cannot promise the global maximum return a local one or a stationary point.

## Variants

- **Supervised.** The state paths are given with the sequences. The maximum likelihood estimate is the normalized counts of starts, moves and emissions, in $\Theta(T + N^2 + N M)$ time for $T$ symbols in all.
- **Unsupervised.** Only the outputs are given. This is the hard case, solved locally by EM.
- **MAP estimation.** Add a prior, usually a Dirichlet on each row. In EM this adds pseudocounts.
- **Discriminative training.** Choose the parameters of several HMMs together so that they tell classes apart, instead of fitting each class alone.
- **Structure.** Choose $N$ and the zero pattern of $A$ (for example a left-to-right model) as well as the numbers.

## Examples

**Supervised.** In the rain and dry model of the HMM page, suppose you are told that $O = (u, u, n, u)$ came from the path R R D R. The moves are R to R, R to D and D to R, so the estimate is $A_R = (1/2, 1/2)$ and $A_D = (1, 0)$. R emitted u three times and D emitted n once, so $B_R = (1, 0)$ and $B_D = (0, 1)$. With so little data many estimates are 0, which is why priors help.

**Unsupervised.** Start Baum-Welch from the parameters of the HMM page and train on the same $O$ with the path hidden. One round raises $\log P(O)$ from $-3.0136$ to $-2.1694$ and gives the new start vector $(0.8770, 0.1230)$. The Baum-Welch page works through this round.

## Known algorithms

| Algorithm | What it returns | Cost of one round |
|---|---|---|
| Count and normalize | the exact MLE when the paths are seen | $\Theta(T + N^2 + N M)$, one pass |
| Expected counts by listing all paths | one EM round | $\Theta(T N^T)$ for a sequence of length $T$ |
| [Baum-Welch](/baum-welch-algorithm/) ([EM](/expectation-maximization/) with [forward-backward](/forward-backward-algorithm/)) | a local maximum or stationary point; $L$ never decreases | $\Theta(T N^2 + N M)$ |
| Viterbi training (counts along the [Viterbi](/viterbi-algorithm/) path) | a local optimum of the best-path score, not of $L$ | $\Theta(T N^2 + N M)$ |
| Gradient ascent on $L$ | a stationary point | $\Theta(T N^2 + N M)$ per gradient |

## Bounds

The likelihood is not concave in $\lambda$ and can have many local maxima, so local methods carry no guarantee of reaching the global maximum. In practice one runs EM from several starts and keeps the best. Each EM round needs at least the cost of [HMM evaluation](/hmm-evaluation/) on every sequence, $\Theta(T N^2)$ for a dense $A$. The number of rounds is not bounded in advance.

## Reductions

- **To EM for a latent variable model.** The hidden path is the latent variable. The E step is [marginal inference](/marginal-inference/) on the chain, and the M step is counting.
- **Mixtures as a special case.** If every row of $A$ is forced to equal $\pi$, the model is a mixture, and Baum-Welch becomes EM for a mixture model such as a [Gaussian mixture](/gaussian-mixture-model/).

## Applications

- **Speech recognition.** The acoustic models of words and phones were trained by Baum-Welch on recorded speech.
- **Biological sequences.** [Profile HMMs](/profile-hmm/) are trained from aligned or unaligned members of a protein family.
- **Unsupervised segmentation.** Fitting a small HMM to a time series, such as a genome or a sensor log, finds regimes without labels.

## References
