---
tag: XG7BKF
kind: problem
slug: machine-unlearning
name: Machine unlearning
aliases:
- data deletion from models
area: security-and-privacy/adversarial-machine-learning
level: research
summary: Remove the effect of chosen training points from a trained model, so that it matches a model trained without them.
history:
  year: 2015
  people: [Yinzhi Cao, Junfeng Yang, Antonio Ginart, James Zou, Chuan Guo, Laurens van der Maaten, Lucas Bourtoule, Nicolas Papernot]
  note: Cao and Yang (2015) posed the problem and unlearned learners in summation form. Ginart et al. (2019) defined exact deletion, Guo et al. (2020) certified removal, and Bourtoule et al. (2021) gave SISA training.
prereqs: [empirical-risk-minimization, differential-privacy-definition]
see_also: [sisa-training, data-poisoning, membership-inference-attack, approximate-differential-privacy, k-means, ridge-regression]
sources:
  - paper: "Yinzhi Cao and Junfeng Yang, Towards making systems forget with machine unlearning, IEEE Symposium on Security and Privacy 2015, pages 463 to 480"
    locator: the problem, the summation form of statistical query learners, and unlearning by subtracting the terms of the removed points
  - paper: "Antonio Ginart, Melody Y. Guan, Gregory Valiant and James Zou, Making AI forget you, data deletion in machine learning, Advances in Neural Information Processing Systems 32 (NeurIPS) 2019, arXiv:1907.05012"
    locator: the definition of a deletion operation whose output has the distribution of retraining, and the deletion efficient k-means algorithms (quantized and divide and conquer)
  - url: "https://proceedings.mlr.press/v119/guo20c.html"
    title: Chuan Guo, Tom Goldstein, Awni Hannun and Laurens van der Maaten, Certified data removal from machine learning models, Proceedings of the 37th International Conference on Machine Learning (ICML), PMLR 119, 2020, pages 3832 to 3842
    locator: the definition of epsilon-certified removal, the Newton step removal for L2-regularized linear models, and the loss perturbation that hides the residual gradient
  - paper: "Lucas Bourtoule, Varun Chandrasekaran, Christopher A. Choquette-Choo, Hengrui Jia, Adelin Travers, Baiwu Zhang, David Lie and Nicolas Papernot, Machine unlearning, IEEE Symposium on Security and Privacy 2021, pages 141 to 159"
    locator: SISA training, the cost of a deletion, and the discussion of what unlearning must guarantee
  - paper: "Varun Gupta, Christopher Jung, Seth Neel, Aaron Roth, Saeed Sharifi-Malvajerdi and Chris Waites, Adaptive machine unlearning, Advances in Neural Information Processing Systems 34 (NeurIPS) 2021"
    locator: deletion requests that depend on the published models, and why guarantees for fixed requests do not carry over
  - url: "https://eur-lex.europa.eu/eli/reg/2016/679/oj"
    title: Regulation (EU) 2016/679, the General Data Protection Regulation
    locator: Article 17, the right to erasure
---

Machine unlearning is the problem of removing the effect of some training points from a trained model, at less cost than training again, so that the result is the model, or the distribution of models, that training without those points would give. Retraining from scratch always solves it and is the baseline; the question is how much faster an algorithm can be, and what it must store. The problem has an exact form (Ginart et al. 2019: the same distribution as retraining) and an approximate form in the style of differential privacy (Guo et al. 2020: certified removal). It matters for the right to erasure in data protection law, for removing [poisoned](/data-poisoning/) or wrong points found after training, and for the privacy of people who leave a dataset.

## In plain words

A model is trained on many records. Later someone asks that their record be deleted. Deleting the record from the database is easy. But the model has already learned from it, and it may still remember it.

The sure way to forget is to train a new model on the data that is left. That can take days for a large model, and requests may come every hour. Machine unlearning asks for a faster way that gives the same result as training again, or a result that nobody can tell apart from it.

Some models make this easy. A model that only keeps a total of the records can subtract the deleted record from the total. Other models mix every record into every number they hold, and for them the only exact methods either keep extra data or train parts of the model again.

## Definition

Let $\mathcal{D}$ be the set of datasets, finite multisets of records from a universe $\mathcal{Z}$. A learning algorithm $A$ maps a dataset $D$ to a model in a set $\Theta$; it may be randomized, and it may also output a state $s$ (stored data, checkpoints, statistics) beside the model. A deletion request is a subset $R \subseteq D$.

**Exact unlearning** (Ginart et al. 2019). An unlearning algorithm $U$ takes $D$, the output $(\theta, s)$ of $A$ on $D$, and $R$, and returns a model and a new state. It is exact if for every $D$ and every $R \subseteq D$,

$$U(D, A(D), R) \overset{d}{=} A(D \setminus R),$$

equality in distribution of the model and the state. For a deterministic $A$ this says that $U$ returns exactly the model of training on $D \setminus R$.

**Approximate unlearning** (Guo et al. 2020, *certified removal*). For $\epsilon \ge 0$ and $0 \le \delta < 1$, $U$ is an $(\epsilon, \delta)$-certified removal for $A$ if for every $D$, every $x \in D$ and every measurable set $T$ of models,

$$\Pr[U(D, A(D), \{x\}) \in T] \le e^{\epsilon} \Pr[A(D \setminus \{x\}) \in T] + \delta \quad \text{and} \quad \Pr[A(D \setminus \{x\}) \in T] \le e^{\epsilon} \Pr[U(D, A(D), \{x\}) \in T] + \delta .$$

Guo et al. state the case $\delta = 0$ as two ratio bounds $e^{-\epsilon}$ and $e^{\epsilon}$; the form above is the same with $\delta$ added, as in [approximate differential privacy](/approximate-differential-privacy/).

**Cost.** The cost of $U$ is its time per request (or per batch of requests) and the size of the state $s$, compared with the time of $A$ on $D \setminus R$. An algorithm is useful when the time per request is much smaller than retraining, amortized over a stated sequence of requests.

## Variants

- **One request, a batch, or a sequence.** A sequence of requests may be adaptive: a user may choose what to delete after seeing the published models. Gupta et al. and later work treat this case; a guarantee for one request does not compose for free.
- **Deterministic exact unlearning.** The model must be bit for bit the model of retraining with the same random seed. [SISA training](/sisa-training/) meets this.
- **Distributional exact unlearning.** Only the distribution must match (Ginart et al.), which allows randomized algorithms such as quantized k-means.
- **Certified (approximate) unlearning.** An $(\epsilon, \delta)$ bound as above, for example for L2-regularized linear models (Guo et al. 2020).
- **Heuristic unlearning.** Fine-tuning on the remaining data, or ascent on the loss of the deleted points, with no guarantee. These are tested with [membership inference](/membership-inference-attack/) after deletion, which can show a failure but cannot prove success.

## Examples

**A sum can be unlearned exactly.** Least squares through the origin in one dimension has $w = \sum_i x_i y_i / \sum_i x_i^2$. Keep the state $s = (\sum_i x_i y_i, \sum_i x_i^2)$. For the points $(1, 2)$, $(2, 3)$ and $(3, 7)$, the state is $(29, 14)$ and $w = 29/14 \approx 2.0714$. To delete $(3, 7)$, subtract its terms: the state becomes $(29 - 21, 14 - 9) = (8, 5)$ and $w = 1.6$, which is exactly the result of training on the two points that remain. This is the *summation form* of Cao and Yang (2015): a learner that reads the data only through sums of per-point terms is unlearned by subtraction, in time independent of $n$. [Ridge regression](/ridge-regression/) with the state $(X^\top X, X^\top y)$ works the same way in $O(d^2)$ per deleted point plus one solve.

**The median cannot be unlearned from the median alone.** The datasets $\{1, 4, 6, 9, 12\}$ and $\{1, 5, 6, 9, 12\}$ have the same median $6$. Delete $9$ from each: the medians of what is left are $(4 + 6)/2 = 5$ and $(5 + 6)/2 = 5.5$. So no algorithm that is given only the median and the deleted point can return the right answer for both. An exact unlearner for the [median](/median/) must keep more state, for example the sorted data in a balanced search tree, with $O(\log n)$ time per deletion.

**A differentially private learner certifies removal by doing nothing.** If $A$ is $(\epsilon, \delta)$-differentially private under the add/remove relation, then $D$ and $D \setminus \{x\}$ are neighbors, and the identity $U(D, (\theta, s), \{x\}) = \theta$ satisfies both inequalities of certified removal for one request, by the definition of DP. For $k$ requests the bound degrades as in the [group privacy theorem](/group-privacy-theorem/). The price is the loss of accuracy that DP costs.

## Known algorithms

- **Retraining from scratch.** Exact, with the time of training on $D \setminus R$ per request and no extra state beyond the data.
- **Summation form** (Cao and Yang 2015). Exact for learners that use only sums of per-point statistics: naive Bayes, linear and [ridge regression](/ridge-regression/), and statistical query learners.
- **SISA training** (Bourtoule et al. 2021). Exact and deterministic for any learner: split the data into disjoint shards, train one model per shard in slices with checkpoints, and aggregate the predictions; a deletion retrains one shard from the checkpoint before the slice that held the point. See [SISA training](/sisa-training/).
- **Deletion efficient k-means** (Ginart et al. 2019). Quantized k-means, which keeps the output unchanged unless a deletion moves a center across a quantization cell, and divide and conquer k-means, which keeps a tree of sub-problems; both are exact in distribution, with an amortized deletion time well below retraining for their stated settings. See [k-means](/k-means/).
- **Certified removal for linear models** (Guo et al. 2020). For an L2-regularized convex loss, remove $x$ by one Newton step $\theta^- = \theta + H^{-1} \nabla_\theta \ell(\theta, x)$, where $H$ is the Hessian of the loss on $D \setminus \{x\}$, and train with a random linear term $b^\top \theta$ added to the objective so that the small residual gradient of the Newton step is hidden; this gives $(\epsilon, \delta)$-certified removal under their assumptions on the loss.

## Bounds

- **Upper bound.** Retraining gives exact unlearning at the cost of training; no algorithm needs more.
- **State lower bounds.** For a deterministic $A$, an exact unlearner that keeps state $s$ must be able to compute $A(D \setminus R)$ from $s$ and $R$ for every allowed $R$. So $s$ must determine all those models; the median example above shows that the model alone is often not enough. The size of $s$ needed depends on the learner and has no general formula.
- **Approximate unlearning and privacy.** A DP learner gives certified removal of one point with no extra time, with the identity as $U$; the converse is false, since a learner that is not private at all can still have a certified removal algorithm. A certified removal guarantee is a statement about distributions, so like DP it holds against every later test, including [membership inference](/membership-inference-attack/).

## Reductions

- **To retraining.** Every instance reduces to training on $D \setminus R$, in the time of $A$.
- **From differential privacy.** An $(\epsilon, \delta)$-DP learner under add/remove is an $(\epsilon, \delta)$-certified removal for one request with the identity as $U$ (Examples above).
- **To partition and aggregation.** A learner that can be split into independent parts, each trained on a disjoint subset, reduces exact unlearning to retraining one part. This is the design of SISA, and the same partition gives a certificate against poisoning ([data poisoning](/data-poisoning/)).

## Applications

- **The right to erasure.** Article 17 of the EU General Data Protection Regulation gives a person the right to have personal data erased. Whether that right extends to models trained on the data is a legal question; unlearning gives a technical way to meet the strongest reading.
- **Removing bad data.** Points found later to be poisoned, mislabeled or obtained without consent can be removed without a full retrain (Cao and Yang 2015 name pollution attacks as one motive).
- **Privacy audits.** Unlearning is tested by comparing the model after deletion with retrained models, and by membership inference on the deleted points.

## References
