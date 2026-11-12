---
tag: N9KRMF
kind: theorem
slug: no-free-lunch-theorem-learning
name: No free lunch theorem
aliases:
- no free lunch theorem for learning
- no free lunch theorem for supervised learning
area: machine-learning/supervised-learning
level: core
summary: "For every learner and every sample size n below half the domain, some distribution has a perfect classifier while the learner errs at least 1/8 with probability at least 1/7."
prereqs: [pac-learning, markov-inequality, generalization-error]
see_also: [no-free-lunch-theorem, vc-dimension, fundamental-theorem-of-statistical-learning, hypothesis-class, overfitting, occams-razor]
sources:
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, Cambridge University Press, 2014
    locator: Section 5.1 (Theorem 5.1, the no free lunch theorem, with its proof; Corollary 5.2) and Appendix B.1 (the Markov step, Lemma B.1)
  - paper: doi:10.1162/neco.1996.8.7.1341
    title: David H. Wolpert, The lack of a priori distinctions between learning algorithms, Neural Computation 8(7), 1996
    locator: the off-training-set error averaged uniformly over all targets
  - paper: doi:10.1109/4235.585893
    title: David H. Wolpert and William G. Macready, No free lunch theorems for optimization, IEEE Transactions on Evolutionary Computation 1(1), 1997
    locator: the optimization theorem, a different result
  - book: isbn:9780262039406
    title: Mehryar Mohri, Afshin Rostamizadeh and Ameet Talwalkar, Foundations of Machine Learning, second edition, MIT Press, 2018
    locator: Section 3.4 (lower bounds for the realizable and the agnostic case)
---

The no free lunch theorem for learning says that no learner succeeds on every distribution when the sample is small compared with the domain. In the form of Shalev-Shwartz and Ben-David: for every learner $A$ for binary classification and every sample size $n < |X|/2$, there is a distribution on which some classifier has zero error, yet $A$ has error at least $1/8$ with probability at least $1/7$. So a learner needs prior knowledge, usually a restricted [hypothesis class](/hypothesis-class/), and this is why the [VC dimension](/vc-dimension/) of that class decides [PAC learnability](/pac-learning/). It is a different theorem from the [no free lunch theorem for optimization](/no-free-lunch-theorem/) of Wolpert and Macready.

## Statement

**Setting.** Binary classification with the zero-one loss. $X$ is a domain, a distribution $D$ over $X \times \{0, 1\}$ is unknown, and a learner $A$ maps each sample $S \in (X \times \{0, 1\})^n$ to a classifier $A(S) : X \to \{0, 1\}$. $L_D(h) = \Pr_{(x, y) \sim D}[h(x) \ne y]$ is the [true error](/generalization-error/). The learner may be any function of the sample. A randomized learner is covered too: fix its random bits, apply the theorem, and average.

**Theorem (Shalev-Shwartz and Ben-David, Theorem 5.1).** Let $A$ be any learning algorithm for binary classification with the zero-one loss over a domain $X$, and let $n$ be a sample size with $n < |X|/2$. Then there is a distribution $D$ over $X \times \{0, 1\}$ such that

1. some $f : X \to \{0, 1\}$ has $L_D(f) = 0$, and
2. $\Pr_{S \sim D^n}\big[L_D(A(S)) \ge 1/8\big] \ge 1/7$.

The book writes $m$ for the sample size.

**Wolpert's form.** Let $X$ be finite, let the input distribution be fixed, and let the target $f : X \to \{0, 1\}$ be drawn uniformly from all $2^{|X|}$ functions. For every learner and every sequence of training inputs, the *off-training-set error* (the error on the inputs not in the sample) has expectation exactly $1/2$ over $f$. So, averaged over all targets, every learner has the same off-training-set error. Wolpert (1996) states this for general losses and priors; this page proves the binary case.

## In plain words

Suppose the learner sees only a few labeled points from a large set, and nothing ties the labels of the unseen points to the labels it has seen. Then any guess it makes on an unseen point is right for some ways of labeling the world and wrong for others, in exactly equal numbers. Take the learner you like best. For each of its possible guesses, there is a world where the guess is wrong, and the theorem picks such a world. In that world a perfect rule exists, but the learner cannot find it from the sample. So learning is only possible if the learner assumes something about the world before it sees the data.

## Proof

Let $C \subseteq X$ be a set of $2n$ points (possible since $|X| > 2n$). There are $T = 2^{2n}$ functions $f_1, \ldots, f_T$ from $C$ to $\{0, 1\}$. Let $D_i$ be the distribution that draws $x$ uniformly from $C$ and labels it $f_i(x)$. Then $L_{D_i}(f_i) = 0$, so condition 1 holds for every $D_i$. It remains to find an $i$ with condition 2.

**Step 1: some $D_i$ has expected error at least $1/4$.** There are $k = (2n)^n$ sequences of $n$ points of $C$; call them $S_1, \ldots, S_k$. When the points are labeled by $f_i$, write $S_j^i$ for the labeled sample. Under $D_i$ each sequence has probability $1/k$, so $\mathbb{E}_{S \sim D_i^n}[L_{D_i}(A(S))] = \frac1k \sum_{j=1}^{k} L_{D_i}(A(S_j^i))$. A maximum is at least an average, and an average is at least a minimum:

$$\max_{i} \frac1k \sum_{j=1}^{k} L_{D_i}(A(S_j^i)) \;\ge\; \frac1T \sum_{i=1}^{T} \frac1k \sum_{j=1}^{k} L_{D_i}(A(S_j^i)) \;=\; \frac1k \sum_{j=1}^{k} \frac1T \sum_{i=1}^{T} L_{D_i}(A(S_j^i)) \;\ge\; \min_{j} \frac1T \sum_{i=1}^{T} L_{D_i}(A(S_j^i)).$$

Fix $j$. Let $v_1, \ldots, v_p$ be the points of $C$ that are not in $S_j$. The sequence has at most $n$ distinct points, so $p \ge n$. For every $h$,

$$L_{D_i}(h) = \frac{1}{2n} \sum_{x \in C} \mathbf{1}[h(x) \ne f_i(x)] \;\ge\; \frac{1}{2n} \sum_{r=1}^{p} \mathbf{1}[h(v_r) \ne f_i(v_r)] \;\ge\; \frac{1}{2p} \sum_{r=1}^{p} \mathbf{1}[h(v_r) \ne f_i(v_r)],$$

using $2n \le 2p$. Apply this with $h = A(S_j^i)$ and average over $i$:

$$\frac1T \sum_{i=1}^{T} L_{D_i}(A(S_j^i)) \;\ge\; \frac{1}{2p} \sum_{r=1}^{p} \frac1T \sum_{i=1}^{T} \mathbf{1}[A(S_j^i)(v_r) \ne f_i(v_r)] \;\ge\; \frac12 \min_{r} \frac1T \sum_{i=1}^{T} \mathbf{1}[A(S_j^i)(v_r) \ne f_i(v_r)].$$

Fix $r$. Split the $T$ functions into $T/2$ pairs $(f_i, f_{i'})$ that differ only at $v_r$. Since $v_r$ is not in $S_j$, the labeled samples $S_j^i$ and $S_j^{i'}$ are equal, so $A$ returns the same classifier $h$ for both. Exactly one of $f_i(v_r)$ and $f_{i'}(v_r)$ differs from $h(v_r)$. So each pair adds exactly 1 to the sum, and $\frac1T \sum_i \mathbf{1}[A(S_j^i)(v_r) \ne f_i(v_r)] = \frac12$. Putting the steps together, some $i$ has

$$\mathbb{E}_{S \sim D_i^n}\big[L_{D_i}(A(S))\big] \ge \frac12 \cdot \frac12 = \frac14.$$

**Step 2: from expectation to probability.** Let $Z = L_{D_i}(A(S))$ for this $i$. Then $Z \in [0, 1]$ and $\mathbb{E}[Z] \ge 1/4$. Apply [Markov's inequality](/markov-inequality/) to the nonnegative variable $1 - Z$:

$$\Pr[Z \le 1/8] = \Pr[1 - Z \ge 7/8] \le \frac{\mathbb{E}[1 - Z]}{7/8} \le \frac{3/4}{7/8} = \frac67.$$

So $\Pr[Z > 1/8] \ge 1/7$, which gives condition 2 with $D = D_i$. $\blacksquare$

**Proof of Wolpert's form.** Fix the training inputs, and let $x$ be an input that is not among them. The classifier $A(S)$ depends only on the training inputs and on the values of $f$ at them. Under the uniform distribution on targets, the value $f(x)$ is a fair bit independent of those values. So $\Pr_f[A(S)(x) \ne f(x)] = 1/2$ for each unseen $x$, and the off-training-set error, an average of such indicators, has expectation $1/2$. $\blacksquare$

### Check by enumeration

For small $n$, all the quantities of the proof are finite sums, and the code for this page computes them exactly with fractions on $C = \{0, \ldots, 2n - 1\}$.

- **All learners with $n = 1$.** A deterministic learner is a table from the 4 labeled samples to the 4 classifiers on $C = \{0, 1\}$, so there are $4^4 = 256$ learners. For every one of them, the worst $D_i$ has expected error at least $1/4$ and $\Pr[L > 1/8] \ge 1/7$. The smallest worst-case expected error over all 256 learners is exactly $1/4$, and the smallest worst-case $\Pr[L > 1/8]$ is $1/2$.
- **Named learners with $n = 2$ and $n = 3$.** Memorize the sample and answer 0 elsewhere; answer with the majority label of the sample; copy the label of the nearest seen point; fill the unseen points with seeded random bits; or always answer 0. Each one has a target with expected error at least $1/4$ and $\Pr[L > 1/8] \ge 1/7$. For example, the memorizer has expected error $9/16$ on the all-ones target with $n = 2$, and the nearest-point learner has $3/8$ on the target $(0, 0, 1, 1)$, where $\Pr[L > 1/8] = 7/8$.
- **The averages.** For each learner that is consistent with its sample, the error averaged over all $2^{2n}$ targets is $\frac12 (1 - \frac{1}{2n})^n$: $1/4$, $9/32$ and $125/432$ for $n = 1, 2, 3$. This is half the probability that a fixed point of $C$ is missed by the sample, and $(1 - \frac{1}{2n})^n \ge 1 - n \cdot \frac{1}{2n} = \frac12$ by Bernoulli's inequality, which is another way to get the $1/4$ of Step 1 for such learners. For every learner and every input sequence, the off-training-set error averaged over the targets is exactly $1/2$.

## Consequences

- **The class of all functions is not learnable.** If $X$ is infinite, the class of all functions $X \to \{0, 1\}$ is not PAC learnable (Shalev-Shwartz and Ben-David, Corollary 5.2): for $\varepsilon < 1/8$ and $\delta < 1/7$, every sample size $n$ fails on some realizable distribution.
- **Infinite VC dimension means not learnable.** The proof uses only that the class contains all $2^{2n}$ labelings of a set of $2n$ points. So a class that shatters arbitrarily large sets is not PAC learnable. This is the lower bound half of the [fundamental theorem of statistical learning](/fundamental-theorem-of-statistical-learning/).
- **Prior knowledge is necessary.** Choosing a hypothesis class, a [regularizer](/regularization/) or a description language ([Occam's razor](/occams-razor/)) is a bet on which distributions are likely. The theorem says such a bet cannot be avoided, not that one bet is right.
- **No learner is better on average over all targets.** By Wolpert's form, a learner that beats another on some targets loses to it on others, in off-training-set error. A claim that a method is better in general is a claim about the targets that occur in practice.
- **[Overfitting](/overfitting/).** A consistent learner over a class that shatters the sample has no reason to be right off the sample.

## Tightness

- **The constant $1/4$ in Step 1 is reached.** With $n = 1$, the enumeration above shows that the best learner has worst-case expected error exactly $1/4$.
- **The constants $1/8$ and $1/7$ come from Markov's inequality** applied with the threshold $1/8$; another threshold gives another pair. They are not the best possible: with $n = 1$ every learner has $\Pr[L > 1/8] \ge 1/2$ on its worst target.
- **The condition $n < |X|/2$ cannot be dropped.** On a finite $X$ the class of all functions is finite, of size $2^{|X|}$, so by the [union bound](/union-bound/) argument of [generalization error](/generalization-error/), a consistent learner reaches error $\varepsilon$ with probability $1 - \delta$ once $n \ge (|X| \ln 2 + \ln(1/\delta))/\varepsilon$. The theorem only speaks about samples that are small compared with the domain. Quantitative lower bounds of order $(\mathrm{VC}(H) + \ln(1/\delta))/\varepsilon$ for every class are given by Mohri, Rostamizadeh and Talwalkar (Section 3.4).

## History

Wolpert (1996) proved that, averaged uniformly over all targets, all learning algorithms have the same expected off-training-set error, and called such results no free lunch theorems. Wolpert and Macready (1997) proved a separate theorem for black-box optimization: averaged over all objective functions, all search algorithms that do not revisit points have the same distribution of observed values. Shalev-Shwartz and Ben-David (2014) give the form stated here, with a single bad distribution for each learner and explicit constants, and use it to prove that a class of infinite VC dimension is not learnable.

## References
