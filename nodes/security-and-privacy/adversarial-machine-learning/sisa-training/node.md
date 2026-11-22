---
tag: P6S600
kind: algorithm
slug: sisa-training
name: SISA training
aliases:
- sharded isolated sliced aggregated training
area: security-and-privacy/adversarial-machine-learning
level: research
summary: Trains models on disjoint shards in slices with checkpoints, so that deleting a point needs retraining only one shard from one slice.
solves: [machine-unlearning]
model: real-ram
complexity:
  vars: {n: the number of records, d: the dimension, S: the number of shards, R: the number of slices per shard, E: the gradient steps per slice}
  time: {build: "O(E d n R)", delete: "O(E d n R / S)"}
  space: {extra: "O(S R d)"}
properties: {deterministic: true, exact: true, online: true, recursive: false}
history:
  year: 2021
  people: [Lucas Bourtoule, Varun Chandrasekaran, Christopher A. Choquette-Choo, Hengrui Jia, Adelin Travers, Baiwu Zhang, David Lie, Nicolas Papernot]
  note: Bourtoule et al. published SISA at IEEE S&P 2021 (arXiv 2019). It extends the summation-form unlearning of Cao and Yang (2015) to any learner by partitioning the data instead of the computation.
prereqs: [machine-unlearning, stochastic-gradient-descent, ensemble-learning]
see_also: [machine-unlearning, data-poisoning, membership-inference-attack, logistic-regression, gradient-descent, krum-aggregation]
sources:
  - paper: "Lucas Bourtoule, Varun Chandrasekaran, Christopher A. Choquette-Choo, Hengrui Jia, Adelin Travers, Baiwu Zhang, David Lie and Nicolas Papernot, Machine unlearning, IEEE Symposium on Security and Privacy 2021, pages 141 to 159, arXiv:1912.03817"
    locator: the SISA design (sharding, isolation, slicing, aggregation), the checkpoints at slice boundaries, the analysis of the retraining time, and the measured speedups on Purchase, SVHN and ImageNet
  - paper: "Yinzhi Cao and Junfeng Yang, Towards making systems forget with machine unlearning, IEEE Symposium on Security and Privacy 2015, pages 463 to 480"
    locator: unlearning by the summation form, the earlier exact method for statistical query learners
  - paper: "Antonio Ginart, Melody Y. Guan, Gregory Valiant and James Zou, Making AI forget you, data deletion in machine learning, Advances in Neural Information Processing Systems 32 (NeurIPS) 2019, arXiv:1907.05012"
    locator: the definition of exact deletion as equality in distribution with retraining
  - paper: "Alexander Levine and Soheil Feizi, Deep partition aggregation, provable defense against general poisoning attacks, International Conference on Learning Representations (ICLR) 2021"
    locator: the same partition and vote used for a certificate against poisoning, with a partition fixed by a hash of each record
---

SISA training (Sharded, Isolated, Sliced, Aggregated) is an exact method for [machine unlearning](/machine-unlearning/) that works with any learner. It splits the training data into $S$ disjoint shards and trains one model on each, in isolation; inside a shard it feeds the data in $R$ slices and saves a checkpoint after each slice; it predicts by a majority vote of the $S$ models. To delete a record, it retrains only the shard that holds it, starting from the checkpoint saved just before the record's slice. When training is deterministic, the result is bit for bit the model that training from scratch on the remaining data gives. Bourtoule et al. (2021) proposed it and measured unlearning speedups of 4.63 times on Purchase and 2.45 times on SVHN against retraining from scratch.

## In plain words

Suppose a teacher grades with a panel of five judges, and each judge has read a different fifth of the old essays. If one author asks for an essay to be forgotten, only one judge has read it, so only that judge must start over. The other four keep what they know.

SISA goes one step further. Each judge reads their essays in batches and writes down what they knew after each batch. If the essay to forget was in batch three, the judge goes back to the notes from after batch two and rereads only batches three and later, without that essay.

The panel votes, so the final answer depends on all the judges, but each record touched only one of them.

## The problem

**Input.** A dataset $D$ of $n$ records, a learner that can continue training from saved parameters, and later a sequence of deletion requests, each naming a record of $D$.

**Output.** After each request, a predictor that equals the predictor of training from scratch on the records that remain, with less work than retraining. This is exact unlearning in the sense of Ginart et al. (2019); see [machine unlearning](/machine-unlearning/).

**What is compared.** The reference is SISA training itself, run from scratch on $D \setminus R$ with the same partition of the remaining records and the same learner. If each record's shard and slice is a fixed function of the record alone, such as a hash of its id, this is exactly $A(D \setminus R)$ for the learning algorithm $A$ = SISA training.

## The algorithm

Shards are numbered $k = 1..S$ and slices $r = 1..R$. $\mathrm{TRAIN}(\theta, X, E)$ runs $E$ steps of the base learner on the records $X$ from the parameters $\theta$, and $C_{k,r}$ is the checkpoint of shard $k$ after slice $r$.

```pseudo id=main
SISA-TRAIN(D, S, R, E)
L1  split D into disjoint shards D_1..D_S, and each D_k into slices D_k1..D_kR
L2  for k = 1 to S do
L3      theta <- theta_0 ; C_k0 <- theta
L4      for r = 1 to R do
L5          theta <- TRAIN(theta, D_k1 + ... + D_kr, E) ; C_kr <- theta
L6  predict(x) = majority vote of the models C_1R, ..., C_SR on x

SISA-DELETE(u)
L7  find the shard k and slice r with u in D_kr, and remove u from D_kr
L8  theta <- C_k,r-1
L9  for t = r to R do theta <- TRAIN(theta, D_k1 + ... + D_kt, E) ; C_kt <- theta
```

Line L1 fixes the partition. In the code it is a seeded shuffle of the ids; a hash of each id also works. Lines L2 to L5 train each shard in isolation: slice $r$ is added to the slices before it, and training continues from the previous checkpoint. Line L6 aggregates by label vote; Bourtoule et al. use a majority vote of the labels. Lines L7 to L9 delete: only shard $k$ changes, and only its checkpoints from slice $r$ on.

The base learner in the code is logistic regression trained by full-batch gradient descent, with records in a fixed order inside each slice. Any learner works if TRAIN is a deterministic function of its start and its data.

## Example

Twelve records, $S = 3$ shards, $R = 2$ slices of 2 records each, $E$ steps per slice. The cost is counted in per-record gradients.

| step | action | checkpoints written | cost |
|---|---|---|---|
| 1 | train shard 1: slice 1 (2 records), then slices 1 and 2 (4 records) | $C_{11}, C_{12}$ | $2E + 4E$ |
| 2 | train shards 2 and 3 the same way | $C_{21}, C_{22}, C_{31}, C_{32}$ | $12E$ |
| 3 | delete record $u$ in slice 2 of shard 2: start from $C_{21}$, train on 3 records | $C_{22}$ | $3E$ |
| 4 | delete record $v$ in slice 1 of shard 3: start from $C_{30}$, train on 1, then 3 records | $C_{31}, C_{32}$ | $4E$ |

Training costs $18E$. Each deletion costs $3E$ or $4E$; retraining all three shards from scratch after step 3 would cost $6E + 5E + 6E = 17E$. Over all 12 records the mean cost of one deletion is $3.5E$, which matches the formula in Complexity.

On a test input, say the three shards vote $1, 0, 1$, so the prediction is $1$. After step 3 only the vote of shard 2 can change.

## Correctness

**Theorem (exact unlearning, deterministic case).** If TRAIN is a deterministic function of its start and of the ordered list of its records, then after any sequence of deletions every checkpoint $C_{k,r}$, and so the predictor of line L6, is equal to the one that SISA-TRAIN computes from scratch on the remaining records with the same partition.

The invariant is that $C_{k,t}$ equals $T_{k,t}$, the checkpoint that training from scratch on the current shard $k$ would give after slice $t$, for every $k$ and $t$. A deletion from $D_{kr}$ changes the data of shard $k$ only in slices $t \ge r$. So $T_{k,t}$ is unchanged for $t < r$, and for the other shards; line L9 recomputes $T_{k,t}$ for $t \ge r$ by the same recursion $T_{k,t} = \mathrm{TRAIN}(T_{k,t-1}, D_{k1} + \cdots + D_{kt}, E)$. The full proof is in the proof file.

**Randomized learners.** If TRAIN uses randomness, give shard $k$ and slice $t$ its own seed that does not depend on the data. Then the same argument gives equality in distribution, the exact unlearning of Ginart et al.

## Complexity

Let each shard hold $n/S$ records in $R$ equal slices of $m = n/(SR)$ records, and let one step of TRAIN on $x$ records cost $O(x d)$.

- **Training.** Shard $k$ trains on prefixes of $m, 2m, \ldots, Rm$ records, which is $E m R (R + 1)/2$ gradients; over $S$ shards, $E n (R + 1)/2$, so $O(E d n R)$ time. Slicing costs about $(R + 1)/2$ times the work of training each shard once on all its data with $E$ steps.
- **One deletion.** At worst the record is in slice 1, and the shard retrains on all prefixes: $O(E d n R / S)$. For a record chosen uniformly, the mean cost (computed here for this model, and checked by the tests) is $E (R + 1)(m (2R + 1) - 3)/6$ gradients. For large $m$ this is about a fraction $(2R + 1)/(3SR)$ of the cost of training all of SISA again.
- **Space.** $S (R + 1)$ checkpoints of $d + 1$ numbers, so $O(S R d)$, beside the data, which must be kept for retraining.

## Properties

- **Exact.** The result is the model of retraining, not an approximation, so no privacy budget or certificate is needed. A membership test after deletion cannot tell it from retraining, because it is retraining.
- **Isolation.** Each record affects one constituent model. The same structure gives a certificate against poisoning: with a fixed partition, $r$ changed records change at most $r$ votes ([data poisoning](/data-poisoning/), and deep partition aggregation of Levine and Feizi 2021).
- **Online.** Deletion requests are served one at a time as they come.
- **Learner agnostic.** Any learner with a deterministic, resumable training procedure works.

## Variants and improvements

- **No slicing ($R = 1$).** Delete by retraining one shard from scratch, with $S$ checkpoints only.
- **Distribution-aware sharding.** Bourtoule et al. discuss placing records that are more likely to be deleted together in the same shards, so that fewer shards retrain.
- **Batched requests.** Collect requests and retrain each touched shard once from the earliest touched slice. $K$ requests spread uniformly hit $S(1 - (1 - 1/S)^K)$ shards in expectation, so the gain shrinks as $K$ grows past $S$.
- **Summation form.** For learners that use only sums of per-record statistics, subtraction is exact in $O(d)$ or $O(d^2)$ time per request ([machine unlearning](/machine-unlearning/)); SISA is for learners without that structure.

## When to use it

Use SISA when exact deletion is required, the learner has no closed form to update, and some loss of accuracy is acceptable. Each constituent model sees only $n/S$ records, so on hard tasks accuracy drops as $S$ grows; Bourtoule et al. report a small accuracy loss on ImageNet with a speedup of 1.36 times, and larger speedups on simpler tasks. Prefer the summation form when the learner allows it, and certified removal (Guo et al. 2020) when a bounded approximation is enough and a single model must be kept.

## Pitfalls

- **A partition that depends on the deleted record.** If line L1 splits by position (the first $n/S$ records to shard 1, and so on), removing a record shifts the others to new shards, and the result of line L9 is no longer the model of training from scratch. Fix the shard and slice of each record by its id, by a seeded assignment kept from the start or by a hash.
- **Order or seeds that depend on positions.** Line L5 must see the records of each slice in a fixed order, and a stochastic learner must use seeds that do not depend on the data. Otherwise the deleted model and the retrained model differ even though both are valid.
- **Restarting from the wrong checkpoint.** Line L8 must take $C_{k,r-1}$, the state before the slice that held the record. Taking $C_{k,r}$ keeps the influence of the record.
- **Keeping the deleted record elsewhere.** The training data, logs and other copies must be removed too; the method removes the record from the model only.
- **Many shards on a hard task.** Isolation is paid for in accuracy. Choose $S$ with a measured accuracy curve, not only by the deletion cost.

## Implementations

The code runs only on synthetic blobs that the tests build from a fixed seed with mlkit. The tests check, bit for bit on 500 random instances with sequences of deletions, that every checkpoint after each deletion equals the checkpoint of an independent trainer run from scratch on the remaining records, and that the other shards are untouched. They also check that one shard with one slice is exactly the logistic regression of mlkit, the exact mean cost of a deletion against the formula above with fractions, and the vote and accuracy on blobs.

## History

Cao and Yang (2015) posed machine unlearning and solved it exactly for learners in summation form. Ginart et al. (2019) defined exact deletion and gave deletion-efficient k-means. Bourtoule et al. (2019 on arXiv, IEEE S&P 2021) gave SISA, the first exact method for any learner, including deep networks, based on partitioning and checkpoints. The same partition and vote gives the poisoning certificate of deep partition aggregation (Levine and Feizi 2021).

## References
