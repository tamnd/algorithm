---
tag: 7V4M5X
kind: model
slug: gmm-hmm-acoustic-model
name: GMM-HMM acoustic model
aliases:
- GMM-HMM
area: natural-language-and-speech/speech-recognition
level: core
summary: Model each phone by a left-to-right HMM, usually three states, whose emissions are Gaussian mixtures over feature vectors.
prereqs: [hidden-markov-model, gaussian-mixture-model, pronunciation-lexicon, source-channel-speech-recognition]
see_also: [triphone-model, phonetic-decision-tree-state-tying, viterbi-training, baum-welch-algorithm, hybrid-dnn-hmm, maximum-likelihood-linear-regression, map-speaker-adaptation, maximum-mutual-information-training]
sources:
  - paper: doi:10.1109/5.18626
    title: Lawrence R. Rabiner, A tutorial on hidden Markov models and selected applications in speech recognition, Proceedings of the IEEE 77(2), 1989, pages 257 to 286
    locator: the sections on continuous observation densities, left-to-right models and the re-estimation of mixture densities
  - paper: doi:10.1109/TIT.1986.1057145
    title: Biing-Hwang Juang, Stephen E. Levinson and Man Mohan Sondhi, Maximum likelihood estimation for multivariate mixture observations of Markov chains, IEEE Transactions on Information Theory 32(2), 1986, pages 307 to 309
    locator: the re-estimation formulas for HMMs with Gaussian mixture outputs and their convergence
  - paper: doi:10.1561/2000000004
    title: Mark Gales and Steve Young, The application of hidden Markov models in speech recognition, Foundations and Trends in Signal Processing 1(3), 2008, pages 195 to 304
    locator: the chapters on the architecture of an HMM-based recognizer and on parameter estimation
  - book: isbn:9780130226167
    title: Xuedong Huang, Alex Acero and Hsiao-Wuen Hon, Spoken Language Processing, Prentice Hall PTR, 2001
    locator: Chapter 8 (hidden Markov models) and Chapter 9 (acoustic modeling)
---

A GMM-HMM acoustic model gives the density $p(O \mid W)$ of the feature frames of an utterance for a word sequence $W$, as the channel of the [source-channel model](/source-channel-speech-recognition/). Each phone is a left-to-right [hidden Markov model](/hidden-markov-model/), usually with three emitting states, and each state emits feature vectors from a [Gaussian mixture](/gaussian-mixture-model/) with diagonal covariances. The [pronunciation lexicon](/pronunciation-lexicon/) turns $W$ into phones, and the phone HMMs joined in that order give the HMM of the utterance. From the 1980s to about 2010 almost every large vocabulary recognizer used this model, mostly with [triphone](/triphone-model/) states tied by [decision trees](/phonetic-decision-tree-state-tying/).

## The machine

The frames are vectors $o_t \in \mathbb{R}^d$, one every 10 ms, for example 13 [MFCC](/mel-frequency-cepstral-coefficients/) values with their first and second [differences](/delta-features/), so $d = 39$.

**One phone.** A phone HMM has three emitting states $1, 2, 3$ in a chain, for the start, the middle and the end of the phone. State $j$ has a self loop with probability $a_{jj}$ and an arc to the next state with probability $1 - a_{jj}$; the arc out of state 3 leaves the phone. There are no arcs back, so the model is left-to-right, and a phone takes at least 3 frames.

**One state.** State $j$ emits a frame with the density

$$b_j(o) = \sum_{m=1}^{M} c_{jm}\, \mathcal{N}(o; \mu_{jm}, \Sigma_{jm}), \qquad c_{jm} \ge 0, \quad \sum_m c_{jm} = 1,$$

a mixture of $M$ Gaussians with diagonal covariances $\Sigma_{jm} = \mathrm{diag}(\sigma^2_{jm1}, \ldots, \sigma^2_{jmd})$. With natural logs, one component has

$$\log \mathcal{N}(o; \mu, \Sigma) = -\frac{1}{2} \Big( d \log(2\pi) + \sum_{k=1}^{d} \log \sigma_k^2 + \sum_{k=1}^{d} \frac{(o_k - \mu_k)^2}{\sigma_k^2} \Big),$$

and $\log b_j(o)$ is a [log-sum-exp](/log-sum-exp-trick/) over the components.

**One utterance.** For a transcript $W$, the lexicon gives a phone sequence, and the phone HMMs joined in that order give one chain of $S$ states, with optional silence models between the words. The density of the frames is the sum over the state paths $Q$ of the chain:

$$p(O \mid W) = \sum_{Q} \prod_{t=1}^{T} a_{q_{t-1} q_t}\, b_{q_t}(o_t).$$

The frames are independent given the states. The [forward algorithm](/forward-algorithm/) computes this sum, and the Viterbi algorithm gives the best path, which is the [forced alignment](/forced-alignment/) of the utterance.

**Training.** Baum-Welch, which is EM for this model, re-estimates the transitions, the mixture weights, the means and the variances from the posteriors of the states and the components (Juang, Levinson and Sondhi 1986). Training runs on the chain of each training utterance, built from its transcript, so the phone boundaries are not needed. A common recipe starts from one Gaussian per state, often from a [Viterbi training](/viterbi-training/) start, and splits the components of each state in two between rounds of Baum-Welch until $M$ is reached.

## What it counts

The model gives $\log p(O \mid W)$, a sum over the frames, for the decoder to add to the language model score. The cost of the model is the evaluation of the emission densities: a state with $M$ diagonal Gaussians of dimension $d$ takes $\Theta(M d)$ operations per frame. A decoder evaluates the states that are active in its beam at each frame, and this term often dominates the cost of the search.

The number of parameters is the number of states times $M (2d + 1)$, for the means, the variances and the weights, plus the transitions. For example, 5000 tied states with 16 components of dimension 39 have $5000 \cdot 16 \cdot 79 = 6\,320\,000$ parameters. The number of tied states and the number of components are chosen to fit the amount of training data, which is a heuristic.

## Relation to other models

- **[Hidden Markov model](/hidden-markov-model/).** A GMM-HMM is an HMM with continuous emissions. A mixture state is the same as $M$ states with one Gaussian each, entered with the probabilities $c_{jm}$, so the HMM algorithms apply with a larger state set.
- **[Gaussian mixture model](/gaussian-mixture-model/).** Each state is a GMM over the frames that the state emits. With one state and no time structure, the model is a plain GMM, as used for speaker verification.
- **[Triphone model](/triphone-model/).** The phone HMMs can depend on the neighboring phones. The structure of the model is the same, with many more states, and the states are tied by [phonetic decision trees](/phonetic-decision-tree-state-tying/).
- **[Hybrid DNN-HMM](/hybrid-dnn-hmm/).** Keeps the HMM, the tied states and the lexicon, and replaces the Gaussian mixtures by a neural network that predicts the state posteriors. Hybrid systems are usually trained on alignments from a GMM-HMM.
- **Adaptation.** [MLLR](/maximum-likelihood-linear-regression/) moves the Gaussian means of the model by shared affine maps, and [MAP adaptation](/map-speaker-adaptation/) moves them toward the data of a new speaker with the model as the prior.
- **Discriminative training.** [Maximum mutual information training](/maximum-mutual-information-training/) keeps the model and changes the training goal from the likelihood to the posterior of the correct transcript.
- **Template matching.** [Dynamic time warping](/dynamic-time-warping/) aligns the frames with stored examples in place of a statistical model. The Viterbi alignment of a GMM-HMM is its statistical counterpart.

## Known results in the model

- **EM never lowers the likelihood.** Baum-Welch re-estimation for HMMs with Gaussian mixture outputs never decreases the likelihood of the training data (Juang, Levinson and Sondhi 1986, a theorem). It finds a local maximum, not in general the global one.
- **Geometric durations.** A state with self loop probability $a$ stays for $\delta$ frames with probability $a^{\delta - 1} (1 - a)$, a geometric distribution with mean $1 / (1 - a)$ (a theorem of the model). The most likely duration is one frame, which does not match real phones. A [hidden semi-Markov model](/hidden-semi-markov-model/) models durations directly.
- **Diagonal covariances.** Diagonal Gaussians assume that the features are uncorrelated within a component. The discrete cosine transform of the MFCCs makes the features nearly uncorrelated, and a mixture of diagonal Gaussians can model the correlation that is left. This is a heuristic justification, and full or structured covariances give small gains at a much larger cost.
- **Measured accuracy.** With tied-state triphones, the GMM-HMM system of Young, Odell and Woodland 1994 had a word error rate of 3.87 percent on the Resource Management Feb'89 test set, and 4.90 percent on the Wall Street Journal Nov'93 5k test (measurements). Hybrid DNN-HMM systems later reduced the error rates on most tasks.

## References
