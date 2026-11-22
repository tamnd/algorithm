---
tag: CGYJMS
kind: algorithm
slug: likelihood-ratio-membership-attack
name: Likelihood ratio membership attack
aliases:
- LiRA
area: security-and-privacy/adversarial-machine-learning
level: research
summary: Fits Gaussians to a record's logit-scaled confidence under models trained with and without it, and tests membership by their likelihood ratio.
model: real-ram
complexity:
  vars: {k: the number of shadow models, m: the number of records in the pool, d: the dimension, s: the number of training steps per model}
  time: {worst: "O(k s m d + k m d)"}
  space: {extra: "O(k m + k d)"}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2022
  people: [Nicholas Carlini, Steve Chien, Milad Nasr, Shuang Song, Andreas Terzis, Florian Tramer]
  note: Carlini et al. gave the attack at IEEE S&P 2022 with the argument that membership attacks must be judged by their true positive rate at a low false positive rate.
prereqs: [membership-inference-attack, likelihood-ratio-test, neyman-pearson-lemma, logistic-regression]
see_also: [differential-privacy-definition, dp-sgd, machine-unlearning, model-inversion-attack, training-data-extraction, overfitting, generalization-error]
sources:
  - paper: "Nicholas Carlini, Steve Chien, Milad Nasr, Shuang Song, Andreas Terzis and Florian Tramer, Membership inference attacks from first principles, IEEE Symposium on Security and Privacy (S&P) 2022, pages 1897-1914"
    locator: "the online attack (Gaussians fitted to the logit-scaled confidence of shadow models trained with and without the record, and their likelihood ratio), the offline attack (models without the record only, and a one-sided test), the variant with one variance for all records, and the evaluation by the true positive rate at a low false positive rate"
  - paper: "Reza Shokri, Marco Stronati, Congzheng Song and Vitaly Shmatikov, Membership inference attacks against machine learning models, IEEE Symposium on Security and Privacy (S&P) 2017, pages 3-18"
    locator: shadow models trained like the target, whose membership the attacker knows
  - paper: "Samuel Yeom, Irene Giacomelli, Matt Fredrikson and Somesh Jha, Privacy risk in machine learning: analyzing the connection to overfitting, IEEE Computer Security Foundations Symposium (CSF) 2018, pages 268-282, arXiv:1709.01604"
    locator: "Experiment 1 and Definition 4 (the membership game and its advantage), and Theorem 1 in Section 3.1 (the advantage against an epsilon-differentially private learner is at most e^epsilon - 1)"
  - paper: "Alexandre Sablayrolles, Matthijs Douze, Cordelia Schmid, Yann Ollivier and Herve Jegou, White-box vs black-box: Bayes optimal strategies for membership inference, Proceedings of the 36th International Conference on Machine Learning (ICML) 2019"
    locator: membership inference as a Bayes decision on the loss, with a threshold calibrated per record
  - paper: "Lauren Watson, Chuan Guo, Graham Cormode and Alexandre Sablayrolles, On the importance of difficulty calibration in membership inference attacks, International Conference on Learning Representations (ICLR) 2022"
    locator: the score of a record minus its score under reference models that did not train on it
  - paper: "Battista Biggio and Fabio Roli, Wild patterns, ten years after the rise of adversarial machine learning, Pattern Recognition 84, pages 317-331, 2018"
    locator: the threat model in three parts, goal, knowledge and capability
---

The likelihood ratio attack (LiRA) of Carlini et al. (2022) decides whether one record $(x, y)$ was in the training set of a model by a statistical test made for that record. The attacker trains many shadow models, about half of them on data that includes the record and half on data that does not. It fits one Gaussian to the logit-scaled confidence $\phi$ of the first group on the record and one to that of the second group, and computes the ratio of the two densities at the value of the target model. A [membership inference attack](/membership-inference-attack/) with one threshold for all records treats easy and hard records alike; LiRA calibrates each record, which is what lets it find members at a low false positive rate. Its strength is a measurement; the [Neyman-Pearson lemma](/neyman-pearson-lemma/) explains why a likelihood ratio is the right statistic.

## In plain words

Some records are easy: every model is sure about them, whether it trained on them or not. Others are odd ones that a model gets right only when it has seen them. One global cut on "how sure is the model" mixes these up.

So, for the one record you ask about, train many copies of the model. Half of the copies see the record and half do not. Look at how sure each group is about the record; each group gives a bell curve.

Now look at how sure the real model is. If that value fits the bell curve of the copies that saw the record much better than the other curve, say "member". The ratio of the two curves at that value is the score.

## The problem

**The threat model**, in the three parts of Biggio and Roli:

- *Goal of the attacker.* Decide whether one chosen record was in the training set, with few false alarms.
- *Knowledge.* Black box access to the output probabilities of the target, the training procedure, and a pool of data from the same distribution that contains the record.
- *Capability.* Query the target on chosen records and train many models of its own. The attacker does not change the target or its training data.

The attack is judged in the membership game of Yeom et al. (see [membership-inference-attack](/membership-inference-attack/)), by the advantage $\text{TPR} - \text{FPR}$ and, above all, by the TPR at a low FPR.

**Input.** A pool $D$ of $m$ records that contains the record $(x, y)$; the training procedure $T$; an even number $k$ of shadow models; the target $f$; a cut $t$.

**Output.** MEMBER or NONMEMBER. With $c$ the probability that a model gives the true label $y$, the score is the **logit-scaled confidence**

$$\phi = \ln \frac{c}{1 - c}.$$

For a logistic model with $z = \langle w, x \rangle + b$ and $s = 2y - 1$, $c = \sigma(s z)$, so $\phi = s z$ exactly.

## The algorithm

```pseudo id=main
LIRA(D, T, k, f, x, y, t)
L1  for j = 1 to k/2 do: pick a random half H of D; train one shadow model on H and one on D minus H
L2  for each shadow g: phi_g <- phi(g, x, y); put it into IN if g trained on (x, y), else into OUT
L3  fit N(mu_in, v_in) to IN and N(mu_out, v_out) to OUT
L4  phi* <- phi(f, x, y)
L5  Lambda <- ln N(phi*; mu_in, v_in) - ln N(phi*; mu_out, v_out)
L6  return MEMBER if Lambda >= t, else NONMEMBER
```

Line L1 trains the models in pairs on complementary halves, so every record of the pool is IN for exactly $k/2$ models. The same shadow models serve every record of the pool, so the cost of training is shared. With few shadow models the variances are noisy; Carlini et al. then use one IN variance and one OUT variance for all records, and the code does the same when asked (the branch at line L3; the means are fitted per record in line L5).

**The offline attack.** When the attacker cannot train models on the record (for example, the record arrives after the shadows are trained), it uses OUT models only and the one-sided test $\Pr[Z \le \phi^*]$ for $Z \sim N(\mu_{\text{out}}, v_{\text{out}})$: a value of $\phi^*$ far above what models without the record give means MEMBER.

## Example

Two records, each with three IN and three OUT shadow values, so all four variances are $2/3$.

- Record A: IN $= \{2, 3, 4\}$, OUT $= \{0, 1, 2\}$, so $\mu_{\text{in}} = 3$, $\mu_{\text{out}} = 1$. The target gives $\phi^* = 2.5$. With equal variances, $\Lambda = \big((\phi^* - \mu_{\text{out}})^2 - (\phi^* - \mu_{\text{in}})^2\big) / (2v) = (2.25 - 0.25) / (4/3) = 1.5$, so with $t = 0$ the answer is MEMBER.
- Record B: IN $= \{5, 6, 7\}$, OUT $= \{3, 4, 5\}$. The target gives $\phi^* = 4.5$, so $(\phi^* - \mu_{\text{out}})^2 = 0.25$, $(\phi^* - \mu_{\text{in}})^2 = 2.25$, and $\Lambda = (0.25 - 2.25) / (4/3) = -1.5$: the answer is NONMEMBER.

The target is more sure of B ($4.5$) than of A ($2.5$), so any one global cut on $\phi$ that calls A a member also calls B a member. LiRA sees that B is an easy record, for which $4.5$ is a normal value even without training. The offline score of A is $\Pr[Z \le 2.5] \approx 0.967$ for $Z \sim N(1, 2/3)$.

## Correctness

The attack decides by a test and can be wrong; its error rates are measurements. The following hold.

**Theorem (the most powerful test, Neyman-Pearson).** If the distributions of $\phi^*$ for members and nonmembers of one record were known, the test that says MEMBER when their density ratio is at least a cut has the largest TPR among all tests with the same FPR. See the [Neyman-Pearson lemma](/neyman-pearson-lemma/) and the [likelihood ratio test](/likelihood-ratio-test/).

**Heuristic (the Gaussian fit).** LiRA replaces the true distributions by Gaussians fitted to shadow models. Carlini et al. report that after the logit scaling the values of one record over many models are close to Gaussian, which they are not before it, since $c$ is crowded near $1$. Both the fit and the stand-in of shadow models for the target are assumptions, not theorems.

**Theorem (a per-record cut, proved on this page).** With equal variances $v$ and $\mu_{\text{in}} > \mu_{\text{out}}$, $\Lambda = \frac{\mu_{\text{in}} - \mu_{\text{out}}}{v}\big(\phi^* - \frac{\mu_{\text{in}} + \mu_{\text{out}}}{2}\big)$, so LiRA is a threshold on $\phi^*$ whose cut depends on the record. A global threshold is the special case where all records share their means.

**Theorem (the balanced shadows and the logit, proved on this page).** Line L1 makes every record IN for exactly $k/2$ models, and for a logistic model $\phi = s z$.

**Theorem (no attack beats privacy, Yeom et al., Theorem 1).** Against an $\epsilon$-[differentially private](/differential-privacy-definition/) training procedure every attacker, LiRA included, has advantage at most $e^\epsilon - 1$; and against a model that does not depend on its data, the expected advantage of LiRA at a fixed cut is $0$ in the game of the tests (proved on this page).

## Complexity

- **Shadow models.** $k$ trainings of $s$ steps of full batch gradient descent on $m/2$ records in dimension $d$: $O(k s m d)$. This dominates.
- **Scores.** $\phi$ of every shadow on every pool record, $O(k m d)$, then $O(k)$ per record for the fits and $O(d)$ for the target.
- **Space.** $O(k d)$ for the models and $O(k m)$ for the values of $\phi$.
- **The cost in practice.** Training many models is the price of the attack; Carlini et al. use far more models than a threshold attack needs. The offline attack trains the models once for all future records.

## Properties

- **Per record.** Each record gets its own null distribution, so easy records do not cause false alarms and odd records are found.
- **Strong at a low FPR.** The gain over a global threshold shows most at a low FPR; the average advantage of the two attacks can be close (in the tests, $0.31$ against $0.32$).
- **Randomized.** The random halves of line L1 make the scores random; the code takes the halves from a seeded generator.
- **A lower bound on risk.** A strong attack shows that a model leaks; a failed attack does not show that it does not.

## Variants and improvements

- **Offline LiRA.** OUT models only, as above. It is weaker but needs no training per record.
- **Fixed variance.** One IN and one OUT variance for all records, for when there are few shadow models.
- **Calibrated thresholds.** Sablayrolles et al. (2019) calibrate a loss threshold per record, and Watson et al. (2022) subtract the score of the record under reference models; both are simpler forms of the same idea.
- **Defenses.** [DP-SGD](/dp-sgd/) bounds the advantage of every attack by the theorem above, and the TPR at a low FPR of LiRA is a common way to audit such training in practice. Removal of records after training is [machine unlearning](/machine-unlearning/).

## When to use it

Use it to measure the privacy risk of a model that you own or that you train on synthetic data, when you care whether any single record can be identified with confidence, which is the question that a privacy audit asks. Report the TPR at a low FPR, such as 1 percent or less. If training many models is too costly, use the offline variant or the threshold attack of [membership-inference-attack](/membership-inference-attack/), and say that the result is weaker. For a guarantee, train with differential privacy.

## Pitfalls

- **Few shadow models.** With a handful of IN and OUT values per record the fitted variances are noise, and a tiny variance gives a huge ratio. Use one variance for all records, or a floor on the variance (the code has both).
- **Raw confidence.** Without the logit scaling, $c$ is near $1$ for most records and the Gaussian fit is poor.
- **Selection of the cut on the test data.** The best advantage over all cuts, read off the same scores, is biased upward: in the control of the tests, where the true advantage is $0$, it is $0.09$. The control test uses the fixed cut $t = 0$.
- **The partner model.** In a game with complementary halves, a target must not use its partner as a shadow: the partner's mask is the complement of the target's, so the IN and OUT lists would then depend on the answer.
- **Shadows unlike the target.** Different training data, model size or training steps make the null distributions wrong.
- **The pool must hold the record.** The online attack trains IN models on the record; without them only the offline test is possible.

## Implementations

The code runs only on logistic models and data that the tests build from a fixed seed, Gaussian blobs in $d = 8$ dimensions from the shared helper mlkit; it never queries a real model or reads a real data set. The tests check the scores against the normal distribution of the Python standard library on 500 random parameter sets, check $\phi$ against the log odds on 500 random models, check the balanced halves and the example. They then measure the game with seed 7401: a pool of 32 records and 32 models in 16 pairs, each trained on 16 records and used once as the target, with the 30 models of the other pairs as shadows, so that every record has 15 IN and 15 OUT values. At FPR 1 percent LiRA with one variance finds 6.25 percent of the members, and one global threshold on $\phi$ finds 0.59 percent; the best advantages are $0.31$ and $0.32$. When every model is trained on other data and so ignores the pool, the advantage at the cut $0$ is $0.0625$ and the TPR at FPR 1 percent is 1.4 percent, noise around the value $0$ of the theorem.

## History

Shokri et al. (2017) introduced shadow models, and Yeom et al. (2018) defined the membership game. Sablayrolles et al. (2019) framed membership as a Bayes decision with a per-record calibration, and Watson et al. (2022) showed the value of calibration by the difficulty of a record. Carlini et al. (2022) gave the likelihood ratio attack with Gaussians on the logit-scaled confidence and argued that attacks must be judged by their TPR at a low FPR, which is now the common way to report them.

## References
