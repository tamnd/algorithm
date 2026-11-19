---
tag: W6039V
kind: algorithm
slug: viterbi-training
name: Viterbi training
aliases:
- segmental k-means
area: natural-language-and-speech/speech-recognition
level: core
summary: Train an HMM by alternating a Viterbi alignment of the data with re-estimation from the hard counts. It never lowers the best-path likelihood and is a fast stand-in for Baum-Welch.
solves: [hmm-parameter-learning]
model: word-ram
complexity:
  vars: {k: the number of rounds, T: the total number of frames, N: the number of states, M: the number of output symbols}
  time: {worst: "Θ(k T N^2)"}
  space: {extra: "Θ(T N + N^2 + N M)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1990
  people: [Biing-Hwang Juang, Lawrence R. Rabiner]
  note: Juang and Rabiner described the segmental k-means algorithm for the parameters of an HMM and showed that it converges in the likelihood of the best state path. Speech recognizers used the method before as a fast way to train and to start Baum-Welch.
prereqs: [forced-alignment, baum-welch-algorithm, k-means]
see_also: [viterbi-algorithm, expectation-maximization, gaussian-mixture-model, gmm-hmm-acoustic-model, phonetic-decision-tree-state-tying, vector-quantization, hybrid-dnn-hmm, maximum-likelihood-estimation]
sources:
  - paper: doi:10.1109/29.60082
    title: Biing-Hwang Juang and Lawrence R. Rabiner, The segmental K-means algorithm for estimating parameters of hidden Markov models, IEEE Transactions on Acoustics, Speech, and Signal Processing 38(9), 1990, pages 1639 to 1641
    locator: the algorithm and its convergence in the best-path likelihood
  - paper: doi:10.1109/5.18626
    title: Lawrence R. Rabiner, A tutorial on hidden Markov models and selected applications in speech recognition, Proceedings of the IEEE 77(2), 1989, pages 257 to 286
    locator: the discussion of initial estimates of the HMM parameters by segmental k-means
  - paper: doi:10.1561/2000000004
    title: Mark Gales and Steve Young, The application of hidden Markov models in speech recognition, Foundations and Trends in Signal Processing 1(3), 2008, pages 195 to 304
    locator: the chapter on parameter estimation
---

Viterbi training estimates the parameters $\lambda = (\pi, A, B)$ of a [hidden Markov model](/hidden-markov-model/) from unlabeled sequences. Each round aligns every training sequence with its best state path by the [Viterbi algorithm](/viterbi-algorithm/), and then sets the parameters to the relative frequencies of the counts along those paths. It is the hard-count version of the [Baum-Welch algorithm](/baum-welch-algorithm/), in the same way that [k-means](/k-means/) is the hard-count version of EM for a [Gaussian mixture](/gaussian-mixture-model/). In speech recognition the method is also called segmental k-means (Juang and Rabiner 1990).

## In plain words

You have a model with a few hidden states and many recordings, but nobody told you which state made which part of each recording. Start with a rough guess of the model. Then repeat two steps. First, for each recording, find the one sequence of states that the current model likes best. Second, pretend that this guess is the truth: count how often each state starts, how often each state follows each other state, and how often each state makes each output, and turn the counts into new probabilities.

Each round makes the best sequence of states at least as likely as before, so the process stops. It can stop at a poor answer if the first guess is poor. It is faster than the method that weighs all state sequences, and it gives a clear label to every frame.

## The problem

The input is a set of training sequences $O^1, \ldots, O^R$ over $M$ symbols, a number of states $N$, and a start model $\lambda_1$. Write $\log$ for the natural log, with $\log 0 = -\infty$. Viterbi training looks for a model with a large value of

$$F(\lambda) = \sum_{r=1}^{R} \max_{Q} \log P(O^r, Q \mid \lambda),$$

the log joint probability of the best state path of each sequence. Compare the objective of Baum-Welch, the total log likelihood $\sum_r \log P(O^r \mid \lambda) = \sum_r \log \sum_Q P(O^r, Q \mid \lambda)$, which sums over all paths. The two objectives have different maxima in general. This is the [HMM parameter learning](/hmm-parameter-learning/) problem with the best path in place of the sum.

The code uses discrete outputs, so $b_j(k)$ is a table. In a [GMM-HMM acoustic model](/gmm-hmm-acoustic-model/) the outputs are feature vectors, and the update of $b_j$ fits a Gaussian mixture to the frames that the paths give to state $j$. With one Gaussian per state this is again a closed form: the mean and the variance of those frames. With more components, k-means on the frames of each state splits them among the components, which is where the name segmental k-means comes from.

## The algorithm

```pseudo id=main
VITERBI-TRAINING(O^1 .. O^R, λ, K, tol)
L1  F_old ← -∞
L2  for round ← 1 to K do
L3      for r ← 1 to R do  Q^r, s_r ← VITERBI(λ, O^r)        ▷ best path and its log joint
L4      F ← s_1 + ... + s_R
L5      if F ≤ F_old + tol then return λ
L6      F_old ← F
L7      count along Q^1 .. Q^R: n_i starts in i, n_ij steps i → j, c_jk frames in j with symbol k
L8      π_i ← n_i / Σ n,  a_ij ← n_ij / Σ_j' n_ij',  b_j(k) ← c_jk / Σ_k' c_jk'    ▷ a row with no counts keeps its value
L9  return λ
```

Line L3 is a [forced alignment](/forced-alignment/) when each sequence has a known transcript, because then the HMM of the sequence is the left-to-right chain of its transcript. The general case on this page runs the full Viterbi recursion over all $N$ states. The tie rule of the code is that of the Viterbi algorithm page: the smallest state index wins.

The start model matters. A common start for a left-to-right model is the uniform segmentation: cut each sequence into $N$ equal parts, give part $j$ to state $j$, and estimate $\lambda_1$ from these paths. The function uniform_segmentation_start of the code does this.

## Example

Take $N = 2$ states and the symbols $x, y$. The single training sequence is $O = (x, y, x)$. The start model has $\pi = (0.2, 0.8)$, $a_{ij} = 0.5$ for all $i, j$, $b_1 = (0.8, 0.2)$ and $b_2 = (0.5, 0.5)$, where $b_j = (b_j(x), b_j(y))$.

**Round 1.** The transitions are uniform, so the best path takes the best state at each frame: state 2 first, because $\pi_2 b_2(x) = 0.4 > \pi_1 b_1(x) = 0.16$, then state 2 for $y$ ($0.5 > 0.2$), then state 1 for $x$ ($0.8 > 0.5$). The path $Q = (2, 2, 1)$ has $P(O, Q) = 0.4 \cdot 0.5 \cdot 0.5 \cdot 0.5 \cdot 0.8 = 0.04$. The counts are one start in state 2, the steps $2 \to 2$ and $2 \to 1$, the emissions $x, y$ in state 2 and $x$ in state 1. So $\pi = (0, 1)$, row 2 of $A$ becomes $(0.5, 0.5)$, row 1 has no counts and keeps $(0.5, 0.5)$, $b_1 = (1, 0)$ and $b_2 = (0.5, 0.5)$.

**Round 2.** The best path is again $(2, 2, 1)$, now with $P(O, Q) = 1 \cdot 0.5 \cdot 0.5 \cdot 0.5 \cdot 0.5 \cdot 1 = 0.0625$. The counts are the same, so the model does not change.

**Round 3.** The objective is again $0.0625$, so line L5 stops. The values of $\exp(F)$ were $0.04$, $0.0625$ and $0.0625$.

The total likelihood went the other way. Under the start model $P(O) = 0.1274$, and under the final model $P(O) = 0.09375$. Viterbi training raised the probability of the best path and lowered the probability of the data. The test test_total_likelihood_can_decrease checks these numbers.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). For a fixed tuple of paths $\mathbf{Q}$, the log joint $G(\lambda; \mathbf{Q}) = \sum_r \log P(O^r, Q^r \mid \lambda)$ splits into one term $\sum_x c_x \log p_x$ for each row of $\pi$, $A$ and $B$. By Gibbs' inequality, the relative frequencies of line L8 maximize each term, so they maximize $G$. This is a theorem. Then

$$F(\lambda_{k+1}) \ge G(\lambda_{k+1}; \mathbf{Q}_k) \ge G(\lambda_k; \mathbf{Q}_k) = F(\lambda_k),$$

because $F$ is a maximum over paths. So $F$ never decreases (a theorem, in exact arithmetic). There are finitely many tuples of paths, and the proof shows that a tuple can repeat only in the last two rounds, so the algorithm stops after a finite number of rounds. It stops at a fixed point, which is a local optimum of the alternation and not in general the global maximum of $F$.

## Complexity

A round runs the Viterbi algorithm on each sequence, which takes $\Theta(T_r N^2)$ time for a sequence of $T_r$ frames, and counts along the paths in $\Theta(T_r)$ time. With $T = \sum_r T_r$ frames in total, a round takes $\Theta(T N^2)$ time and $k$ rounds take $\Theta(k T N^2)$. The normalization adds $\Theta(N^2 + N M)$ per round. A left-to-right model with a self loop and one move per state takes $\Theta(T N)$ time per round, as in forced alignment.

The back pointers of one sequence take $\Theta(T_r N)$ space, the paths take $\Theta(T)$ and the model and the counts take $\Theta(N^2 + N M)$. The bound in the front matter allows all back pointers at once.

A Baum-Welch round also takes $\Theta(T N^2)$ time, so the saving of Viterbi training is a constant factor: one max pass and a traceback in place of a forward pass, a backward pass and the posteriors, and integer counts in place of sums of posteriors. With Gaussian mixtures, each frame updates only the statistics of one state, which is a larger saving.

## Properties

- **Monotone in the best-path likelihood.** $F(\lambda)$ never decreases (a theorem). The total likelihood $P(O \mid \lambda)$ can decrease, as the example shows.
- **Finite stop.** In exact arithmetic the algorithm stops after finitely many rounds (a theorem). In practice it stops after a few rounds, often fewer than Baum-Welch needs, but this is an observation and not a bound.
- **Local optimum.** The result depends on the start model. The test test_learns_a_left_to_right_model shows a start with almost flat emissions that ends with a much lower objective than the uniform segmentation start.
- **Zeros stay zero.** A transition or emission with probability 0 is never on a best path with finite score, so it gets no counts and stays 0. A left-to-right topology stays left-to-right.
- **Hard labels.** Every frame belongs to one state. This makes the statistics simple, and it gives labels for other uses, for example the targets of a [hybrid DNN-HMM](/hybrid-dnn-hmm/).
- **Biased estimates.** Hard counts favor the winning state at every frame, so the estimates are biased when the states overlap. When the best path holds most of the probability mass, the two methods give nearly the same result (a heuristic).

## Variants and improvements

- **Baum-Welch.** Replace the hard counts by the posteriors of the [forward-backward algorithm](/forward-backward-algorithm/). This is EM, and it never decreases the total likelihood. Baum-Welch is the soft-count version and Viterbi training is the hard-count version of the same alternation.
- **Viterbi then Baum-Welch.** A common recipe runs a few rounds of Viterbi training from a uniform segmentation, and then Baum-Welch from the result. Rabiner 1989 describes segmental k-means as a way to get the initial estimates.
- **Training with transcripts.** In speech, the HMM of each utterance is built from its transcript, and line L3 is forced alignment. This is the usual alignment step of recognizer training.
- **N-best or beam paths.** Count along a few best paths, or along the paths inside a beam, to get between hard and soft counts.
- **Continuous outputs.** Re-estimate each state's Gaussian mixture from its frames, by k-means and then one fit of the mixture, or by one EM step on the frames of the state.

## When to use it

Use Viterbi training to start an HMM from a rough model, to train when the best path dominates (well separated states, as in speech with good features), and when you need a hard label for every frame. Use Baum-Welch when the states overlap, when the data are few, or when you need the maximum likelihood estimate. In speech, both appear in one recipe: Viterbi alignments give the first models and the frame labels, and Baum-Welch refines the models.

## Pitfalls

- **A poor start.** A state can lose all its frames, and then its rows keep the old values and never change. Start from a uniform segmentation or from a trained smaller model.
- **Zero counts.** A symbol that a state never emits in the paths gets probability 0, and an unseen test sequence can then have probability 0. Smooth the counts or floor the probabilities.
- **The wrong objective.** Do not report the total likelihood as the training curve of Viterbi training and expect it to rise. Track $F$.
- **Products of probabilities.** Use log space. A product over a few hundred frames underflows in double precision.
- **Ties in the alignment.** Different tie rules give different paths and different counts. Fix the tie rule if you need reproducible models.

## Implementations

## History

Juang and Rabiner 1990 described the segmental k-means algorithm: alternate a Viterbi segmentation of the training data with a k-means clustering of the frames of each state, and re-estimate the model. They showed that it converges in the likelihood of the best state path. The method was already part of the training of speech recognizers at that time, often as the start for Baum-Welch (Rabiner 1989). Gales and Young 2008 describe the alignment step and the re-estimation in the context of modern recognizers.

## References
