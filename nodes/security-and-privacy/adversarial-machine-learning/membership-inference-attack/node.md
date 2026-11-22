---
tag: 52KYBB
kind: algorithm
slug: membership-inference-attack
name: Membership inference attack
aliases:
- shadow model attack
area: security-and-privacy/adversarial-machine-learning
level: advanced
summary: Decides whether a record was in a model's training set from the model's output on it; the classic method fits its decision rule on shadow models trained on similar data.
model: real-ram
complexity:
  vars: {k: the number of shadow models, m: the number of points per shadow set, d: the dimension, s: the number of training steps per model}
  time: {worst: "O(k s m d + k m log(k m))"}
  space: {extra: "O(k m + d)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2017
  people: [Reza Shokri, Marco Stronati, Congzheng Song, Vitaly Shmatikov]
  note: Shokri, Stronati, Song and Shmatikov gave the attack with shadow models at IEEE S&P 2017. Yeom et al. (2018) defined the membership game and its advantage, and Carlini et al. (2022) asked for the true positive rate at a low false positive rate.
prereqs: [logistic-regression, overfitting, generalization-error, differential-privacy-definition]
see_also: [likelihood-ratio-membership-attack, neyman-pearson-lemma, likelihood-ratio-test, dp-sgd, model-inversion-attack, training-data-extraction, machine-unlearning, confusion-matrix]
sources:
  - paper: "Reza Shokri, Marco Stronati, Congzheng Song and Vitaly Shmatikov, Membership inference attacks against machine learning models, IEEE Symposium on Security and Privacy (S&P) 2017, pages 3-18"
    locator: "the shadow model technique (shadow models trained like the target on data from a similar distribution) and the attack model, one binary classifier per output class, trained on the outputs of the shadow models on their own training data (in) and on other data (out)"
  - paper: "Samuel Yeom, Irene Giacomelli, Matt Fredrikson and Somesh Jha, Privacy risk in machine learning: analyzing the connection to overfitting, IEEE Computer Security Foundations Symposium (CSF) 2018, pages 268-282, arXiv:1709.01604"
    locator: "Experiment 1 (the membership experiment), Definition 4 and equation (2) (the membership advantage, equal to the true positive rate minus the false positive rate), Theorem 1 in Section 3.1 (the advantage against an epsilon-differentially private learner is at most e^epsilon - 1), and Section 3.2 (the advantage of simple attacks in terms of the generalization error)"
  - paper: "Nicholas Carlini, Steve Chien, Milad Nasr, Shuang Song, Andreas Terzis and Florian Tramer, Membership inference attacks from first principles, IEEE Symposium on Security and Privacy (S&P) 2022, pages 1897-1914"
    locator: "the argument that average metrics such as accuracy and AUC hide whether an attack identifies any member with confidence, and the advice to report the true positive rate at a low false positive rate"
  - paper: "Ahmed Salem, Yang Zhang, Mathias Humbert, Pascal Berrang, Mario Fritz and Michael Backes, ML-Leaks: model and data independent membership inference attacks and defenses on machine learning models, Network and Distributed System Security Symposium (NDSS) 2019"
    locator: attacks with one shadow model in place of many, and an attack with no shadow model that puts a threshold on the output of the target
  - paper: "Nils Homer et al., Resolving individuals contributing trace amounts of DNA to highly complex mixtures using high-density SNP genotyping microarrays, PLoS Genetics 4(8), 2008"
    locator: membership of one person in a genomic mixture, decided by a statistical test on summary statistics
  - paper: "Battista Biggio and Fabio Roli, Wild patterns, ten years after the rise of adversarial machine learning, Pattern Recognition 84, pages 317-331, 2018"
    locator: the threat model in three parts, goal, knowledge and capability
---

A membership inference attack decides, from the output of a trained model on a record $(x, y)$, whether that record was in the training set. Shokri, Stronati, Song and Shmatikov (2017) gave the classic method: the attacker trains *shadow models* the same way as the target, on data that the attacker owns, so that for these models it knows which records are members. It then learns a rule that tells the outputs on members from the outputs on nonmembers, and applies the rule to the target. The attack works because a model usually fits its own training points better than new points, so its [overfitting](/overfitting/) leaks membership. The quality of the attack is a measurement; the theorems on this page bound it or show that the decision rule is the best of its class.

## In plain words

A model was trained on some records, and you want to know if one given record was among them. Models tend to be more sure of the answer on records they have seen.

So you look at how sure the model is about the true label of the record. If it is very sure, you guess "member", and if not, "nonmember". The only question is where to put the cut.

To find the cut, you train your own copies of the model on data you have. For your copies you know which records went in and which did not, so you can see how sure a copy is in each case and pick the cut that separates the two groups best. Then you use that cut on the real model.

## The problem

**The threat model**, in the three parts of Biggio and Roli:

- *Goal of the attacker.* Learn whether one chosen record was in the training set. This is a privacy goal: in a medical model, membership alone can say that a person has a condition.
- *Knowledge.* Black box access to the output of the target (here the probability of each label), the training procedure, and data from the same distribution as the training data. The attacker does not know the training set.
- *Capability.* Query the target on chosen records and train models of its own. The attacker does not change the target or its training data.

**The membership game** of Yeom et al. (their Experiment 1). Draw a training set $S$ of $n$ records from a distribution $\mathcal{D}$ and train $f = A(S)$. Flip a fair coin $b$. If $b = 0$, draw $z$ uniformly from $S$; if $b = 1$, draw $z$ from $\mathcal{D}$. The attacker gets $z$, $f$, $n$ and $\mathcal{D}$ and outputs a guess of $b$. Its **advantage** is $2 \Pr[\text{correct}] - 1$, which equals

$$\text{Adv} = \text{TPR} - \text{FPR} = \Pr[\text{says member} \mid b = 0] - \Pr[\text{says member} \mid b = 1].$$

A guess that ignores the model has advantage $0$, and a perfect attack has advantage $1$ (up to the small chance that a fresh draw is also in $S$).

**Input.** Shadow sets $D_1, \ldots, D_k$ from the same distribution, each of $m$ records; the training procedure $T$; the target model $f$; a record $(x, y)$.

**Output.** MEMBER or NONMEMBER. The score of a model $g$ on a record is $c(g, x, y)$, the probability that $g$ gives the true label $y$; the rule says MEMBER when $c(f, x, y) \ge \tau$.

## The algorithm

```pseudo id=main
MEMBERSHIP-INFERENCE(D_1, ..., D_k, T, f, x, y)
L1  for j = 1 to k do
L2      g_j <- T(the first half of D_j)
L3      put c(g_j, x', y') into IN for each (x', y') of the first half, and into OUT for each of the second half
L4  tau <- the threshold that maximizes TPR - FPR of the rule "score >= tau" on IN and OUT
L5  return MEMBER if c(f, x, y) >= tau, else NONMEMBER
```

Each shadow set is split into a half that the shadow model trains on (members) and a half that it never sees (nonmembers), so the attacker has labelled scores for both cases. Line L4 sorts the scores and sweeps the cut from the top; the candidates are the scores themselves and $+\infty$, which says MEMBER for nothing. Ties go to the largest $\tau$.

**A simplification.** Shokri et al. train one neural network per output class as the attack model, on the whole vector of output probabilities. This page and its code use one threshold on the confidence of the true label, as in the threshold attacks of Yeom et al. and of Salem et al. (2019). The structure, shadow models whose membership is known, is the same.

## Example

The shadow models give the scores IN $= \{0.9, 0.8, 0.7\}$ and OUT $= \{0.75, 0.6, 0.5\}$. The sweep from the top gives:

| $\tau$ | TPR | FPR | TPR - FPR |
|---|---|---|---|
| $0.9$ | $1/3$ | $0$ | $1/3$ |
| $0.8$ | $2/3$ | $0$ | $2/3$ |
| $0.75$ | $2/3$ | $1/3$ | $1/3$ |
| $0.7$ | $1$ | $1/3$ | $2/3$ |
| $0.6$ | $1$ | $2/3$ | $1/3$ |
| $0.5$ | $1$ | $1$ | $0$ |

Two cuts tie at $2/3$, and line L4 keeps the larger, $\tau = 0.8$. On the target, the members score $0.95, 0.85, 0.6$ and the nonmembers $0.82, 0.55, 0.4$. The rule says MEMBER for $0.95$, $0.85$ and $0.82$, so TPR $= 2/3$, FPR $= 1/3$, and the advantage on the target is $1/3$, less than on the shadow models. The best TPR with FPR $0$ is $2/3$, at the cut $0.85$.

## Correctness

The attack has no correctness in the sense of a right answer: its decisions are guesses, and their quality is a measurement. What is proved is the following.

**Theorem (the advantage, Yeom et al., equation (2)).** In the membership game, $2\Pr[\text{correct}] - 1 = \text{TPR} - \text{FPR}$. It follows from $\Pr[\text{correct}] = \tfrac{1}{2}\text{TPR} + \tfrac{1}{2}(1 - \text{FPR})$; the proof file gives it.

**Theorem (the threshold, proved on this page).** Line L4 returns a $\tau$ that maximizes TPR - FPR over all thresholds $\tau \in \mathbb{R} \cup \{+\infty\}$, and the largest such $\tau$ among the candidates. The rule changes only at the scores, so the sweep sees every distinct rule. The code computes TPR at a fixed FPR in the same sweep.

**Theorem (a model that ignores its data, proved on this page).** If the trained model does not depend on $S$, every attack has advantage $0$. This is the case $\epsilon = 0$ of the next theorem, and the tests use it as a control.

**Theorem (a bound from differential privacy, Yeom et al., Theorem 1).** If the training procedure is $\epsilon$-[differentially private](/differential-privacy-definition/), every attacker has $\text{Adv} \le e^{\epsilon} - 1$.

**Heuristic (why a threshold on confidence).** If the attacker knew the distribution of the score on members and on nonmembers, the [Neyman-Pearson lemma](/neyman-pearson-lemma/) says that the most powerful test at each FPR puts a threshold on the [likelihood ratio](/likelihood-ratio-test/) of the two distributions. A threshold on the confidence is that test only when the ratio grows with the confidence. That is often roughly true on average, but the ratio differs from record to record; the [likelihood ratio attack](/likelihood-ratio-membership-attack/) fits it per record.

## Complexity

- **Shadow models.** $k$ trainings of $s$ steps of full batch gradient descent on $m/2$ points in dimension $d$: $O(k s m d)$.
- **Scores and threshold.** $k m$ scores at $O(d)$ each, then one sort: $O(k m d + k m \log(k m))$.
- **One decision.** $O(d)$ for one query of the target.
- **Space.** $O(k m)$ scores and $O(d)$ for one model at a time.

## Properties

- **Black box.** The attack needs only the output probabilities of the target, not its weights.
- **Average, not per record.** One threshold for all records. A record that is hard for every model gets a low score as a member, and an easy one gets a high score as a nonmember.
- **Grows with overfitting.** Yeom et al. (Section 3.2) show that the advantage of simple attacks grows with the [generalization error](/generalization-error/); in the tests, a weight penalty lowers the advantage (a measurement).
- **Transfer from shadows to target.** The cut is right for the target only if the shadow models behave like it. In the example the advantage falls from $2/3$ on the shadows to $1/3$ on the target.

## Variants and improvements

- **Attack models per class.** Shokri et al. learn a classifier per output class on the whole probability vector, which can use more than the confidence of the true label.
- **Fewer or no shadow models.** Salem et al. (2019) use one shadow model, or none, with a threshold on the output of the target.
- **Loss threshold.** Yeom et al. put a threshold on the loss of the target on the record. For the log loss $-\ln c$, the rule $c \ge \tau$ is the rule "loss $\le -\ln \tau$", so the confidence threshold of this page is a loss threshold.
- **Likelihood ratio attack.** Carlini et al. (2022) fit, per record, the score distributions of shadow models trained with and without that record, and test their ratio. See [likelihood-ratio-membership-attack](/likelihood-ratio-membership-attack/).
- **Defenses.** Training with [DP-SGD](/dp-sgd/) bounds the advantage by the theorem above; [regularization](/regularization/) and early stopping lower it in practice; [PATE](/pate/) trains the released model only on noisy votes. Removal of a record after training is [machine unlearning](/machine-unlearning/), and a membership attack is one way to test it.

## When to use it

Use it to measure the privacy risk of a model that you own or that you train on synthetic data, before you release it, and to check that a defense works. Report the advantage and also the TPR at a low FPR, as Carlini et al. advise, because an attack with a fair average advantage can still fail to identify any single member with confidence. For a strong measurement use the likelihood ratio attack; for a guarantee use differential privacy, since an attack only gives a lower bound on the risk.

## Pitfalls

- **Average metrics hide the risk.** In the tests the attack has advantage $0.36$, but at FPR $5$ percent its TPR is $0.056$, about the FPR itself: it finds members only on average. Report the TPR at a low FPR.
- **The cut overfits the shadows.** A cut fitted on few shadow scores is tuned to them; on the target the advantage can be lower, as in the example.
- **Nonmembers from the training distribution.** The game draws nonmembers from the same distribution as the members. Nonmembers from another distribution make the attack look stronger than it is, because it can then detect the distribution and not membership.
- **Base rates.** The game puts members and nonmembers in equal numbers. When members are rare, even a small FPR gives many more false alarms than true members.
- **No attack is not no risk.** A weak attack does not show that the model is private; only a bound such as differential privacy does.

## Implementations

The code runs only on logistic models and data that the tests build from a fixed seed, Gaussian blobs in $d = 8$ dimensions from the shared helper mlkit; it never queries a real model or reads a real data set. The tests check the threshold against a brute force search with exact fractions on 500 random score lists, check TPR at a fixed FPR the same way on 500 lists, and check the example. They then measure the game with seed 7304: 4 shadow sets of 32 points, and 10 target models, each trained on 16 points with 16 fresh nonmembers. With no weight penalty the advantage is $0.3625$ and the TPR at FPR $5$ percent is $0.056$; with the penalty $1.0 \lVert w \rVert^2 / 2$ the advantage is $0.119$; and for models trained on other data, which ignore their members, it is $-0.025$, sampling noise around the value $0$ of the theorem.

## History

Homer et al. (2008) showed that the presence of one person in a genomic mixture can be decided from summary statistics, which made membership a privacy question. Shokri, Stronati, Song and Shmatikov (2017) gave the attack on machine learning models with shadow models, and Yeom et al. (2018) defined the membership game, linked the advantage to overfitting and bounded it under differential privacy. Salem et al. (2019) showed that one shadow model, or none, is enough for a threshold attack. Carlini et al. (2022) argued for the TPR at a low FPR and gave the likelihood ratio attack.

## References
