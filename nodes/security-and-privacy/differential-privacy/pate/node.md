---
tag: 7WDT5Q
kind: algorithm
slug: pate
name: Private aggregation of teacher ensembles
aliases:
- PATE
area: security-and-privacy/differential-privacy
level: research
summary: "Trains teachers on disjoint data, labels public data by a noisy vote among them, and trains a student model on those labels."
model: real-ram
complexity:
  vars: {n: the number of private examples, k: the number of teachers, Q: the number of public queries, m: the number of classes, d: the dimension}
  time: {worst: O(n d + Q k m d)}
  space: {extra: O(k m d)}
properties: {deterministic: false, randomized: true}
history:
  year: 2017
  people: [Nicolas Papernot, Martín Abadi, Úlfar Erlingsson, Ian Goodfellow, Kunal Talwar]
  note: "Papernot, Abadi, Erlingsson, Goodfellow and Talwar introduced PATE at ICLR 2017, with the Laplace noisy max and a data-dependent moments accountant. Papernot et al. (ICLR 2018) replaced the Laplace noise by Gaussian noise and added a confidence check."
prereqs: [report-noisy-max, subsample-and-aggregate]
see_also: [knowledge-distillation, dp-sgd, laplace-mechanism, gaussian-mechanism, moments-accountant, sequential-composition-theorem, post-processing-theorem, membership-inference-attack]
sources:
  - url: "https://arxiv.org/abs/1610.05755"
    title: "Nicolas Papernot, Martín Abadi, Úlfar Erlingsson, Ian Goodfellow and Kunal Talwar, Semi-supervised knowledge transfer for deep learning from private training data, ICLR 2017"
    locator: "the noisy aggregation mechanism of equation (1) in Section 2.1, and the results with 250 teachers and Laplace noise of scale 20 on MNIST and SVHN"
  - url: "https://arxiv.org/abs/1802.08908"
    title: "Nicolas Papernot, Shuang Song, Ilya Mironov, Ananth Raghunathan, Kunal Talwar and Úlfar Erlingsson, Scalable private learning with PATE, ICLR 2018"
    locator: the Gaussian noisy max (GNMax) and the Confident GNMax aggregator
---

Private aggregation of teacher ensembles (PATE) trains a model on private labeled data without the model ever seeing that data. The private data is split into $k$ disjoint parts, and a teacher model is trained on each part. A student model then learns from public unlabeled data: each public point is labeled by a vote of the teachers, with Laplace noise added to the vote counts. Changing one private example changes only one teacher and so moves at most one vote, which makes each noisy label $2\gamma$-differentially private for the noise scale $1/\gamma$. The student sees only the public points and the noisy labels, so it is private by post-processing. Papernot, Abadi, Erlingsson, Goodfellow and Talwar (2017) introduced it. It is an instance of [subsample and aggregate](/subsample-and-aggregate/) with [report noisy max](/report-noisy-max/) as the aggregator.

## In plain words

Split the private data into many small piles, and train one teacher on each pile. No teacher has seen more than its own pile.

Then take public examples that have no labels. For each one, ask all teachers for a label and count the votes. Add some random noise to the counts, and use the winner as the label. When most teachers agree, the noise rarely changes the winner.

Any one person's data is in one pile only, so it can change at most one vote. The noise hides one vote. Finally a student model learns from the public examples and their noisy labels, and only the student is published.

## The problem

The private data is a sequence $D$ of $n$ labeled examples with labels in $\{0, \ldots, m - 1\}$. A public set of unlabeled points $x_1, \ldots, x_Q$ from a similar distribution is also available, and it is fixed before the run. The neighbor relation is replace: one private example changes, at the same position. The goal is a classifier that is $\varepsilon$-[DP](/differential-privacy-definition/) with respect to the private data and is accurate on new points.

## The algorithm

```pseudo id=main
PATE(D, x_1..x_Q, k, gamma)
L1  split D into k disjoint parts: example i goes to part i mod k
L2  train teacher j on part j, for j = 0..k-1
L3  for t = 1 to Q do
L4      n_c <- the number of teachers that predict class c at x_t, for each class c
L5      label_t <- argmax over c of (n_c + Lap(1/gamma))        ▷ LNMax
L6  train the student on (x_1, label_1), ..., (x_Q, label_Q)
L7  return the student
```

Line L1 splits the data by a rule that does not look at the data, so each example is in exactly one part. Line L2 trains the teachers with any non-private method; in the paper they are deep networks, and in the code they are nearest-centroid classifiers. Line L4 counts the votes at one public point. Line L5 is the Laplace noisy max (LNMax) of the paper: add independent Laplace noise of scale $1/\gamma$ to each count and take the largest. The code draws each Laplace value as the difference of two exponential draws. Line L6 trains the student on public data only; the paper uses semi-supervised learning to make use of the public points that it does not query. Only the student of line L7 is released, never the teachers.

The code uses floats and a seeded generator, so it shows the algorithm but is not a safe deployment. Floating-point Laplace samplers can leak (Mironov 2012). A deployment needs a cryptographic source of randomness and exact samplers, such as the [discrete Gaussian](/discrete-gaussian-mechanism/) for the Gaussian version.

## Example

Take $n = 20$ private points in the plane, ten of class 0 near $(-1, 0)$ and ten of class 1 near $(1, 0)$, in alternate order. With $k = 5$, each teacher gets two points of each class and stores the two class means.

| teacher | mean of class 0 | mean of class 1 |
|---|---|---|
| 0 | (-0.85, 0.15) | (1.05, -0.15) |
| 1 | (-0.75, 0.15) | (0.85, 0.05) |
| 2 | (-1.05, 0) | (0.7, 0.15) |
| 3 | (-1.15, 0) | (1.1, 0) |
| 4 | (-1.1, -0.15) | (1.15, 0.1) |

Three public points get votes and noisy labels with $\gamma = 0.5$, so each answer is $1$-DP. The probability of class 0 is exact, from the noisy max law; the label is the draw of the code with the seed 2.

| public point | votes (class 0, class 1) | P(label 0) | label |
|---|---|---|---|
| (-0.5, 0) | (5, 0) | 0.9077 | 0 |
| (0.02, 0) | (3, 2) | 0.6209 | 0 |
| (0.9, 0) | (0, 5) | 0.0923 | 1 |

The student stores the class means of the labeled public points: $(-0.24, 0)$ for class 0 and $(0.9, 0)$ for class 1. The three labels are $3$-DP by basic composition. When the teachers agree, the noisy label is right with high probability; when they split 3 to 2, the noise often flips the label. With the seeds 4 and 5, the code labels the middle point 1.

For the paper, basic composition gives $2\gamma Q = 0.1 \cdot 100 = 10$ for the MNIST student with 100 queries and $\gamma = 0.05$. The paper reports $(2.04, 10^{-5})$ for it, with an accuracy of 98.00%, from its data-dependent accountant. For SVHN with 1000 queries, the bounds are $100$ and $(8.19, 10^{-6})$, with 90.66%.

## Correctness

**Theorem (privacy).** Under replace, the $Q$ labels are $2\gamma Q$-DP, and so is the student.

The proof has three steps. First, the split of line L1 does not depend on the data, so a changed example changes one part and one teacher. Second, so at every public point at most one vote moves from one class to another, and every count changes by at most 1. Third, for report noisy max with $\mathrm{Lap}(1/\gamma)$ noise, a change of at most 1 in every count changes the probability of each winner by at most $e^{2\gamma}$. The $Q$ answers use independent noise, so the factors multiply, and the student is post-processing. The correctness proof of this page gives all the steps and shows that the factor $2\gamma$ is reached in the limit.

**What the paper proves in addition.** Papernot et al. use the [moments accountant](/moments-accountant/) with a bound that depends on the vote counts. When the teachers agree strongly, a query costs much less than $2\gamma$. That bound is computed from the private votes, so its value is itself private; the theorem above does not cover the release of that number. The tests check the vote counts against an independent oracle, the noisy max law against a closed form with two classes, the sampler against that law, and the bound $2\gamma$ for moved votes.

## Complexity

The model is the [real RAM](/real-ram/), with one exponential draw counted as $O(1)$. The costs are for the nearest-centroid teachers of the code.

- **Teachers.** Lines L1 and L2 cost $O(nd)$, since each example is used by one teacher.
- **Queries.** Line L4 costs $O(kmd)$ for one point and line L5 costs $O(m)$, so the $Q$ queries cost $O(Qkmd)$.
- **Student.** Line L6 costs $O(Qd)$.
- **Space.** The teachers take $O(kmd)$.

With deep networks the cost is that of training $k$ models on $n/k$ examples each, plus $Qk$ predictions.

## Properties

- **Any learner.** The privacy proof treats the teachers as black boxes. They need not be convex or even trained by a known method, as long as each sees only its own part.
- **Privacy does not depend on $n$.** The bound $2\gamma Q$ is the same for every $n$ and $k$. More data helps only accuracy: more teachers make the votes larger, so the same noise flips fewer labels.
- **The cost grows with the number of queries.** Each label costs privacy, so the student should learn from few labels. This is why the paper uses semi-supervised learning for the student.
- **Needs public data.** PATE needs unlabeled public data from a distribution close to the private one. Without it, the method does not apply.
- **Strong agreement is cheap.** In the data-dependent analysis, a query where almost all teachers agree costs much less than $2\gamma$. This is the regime where PATE works well.

## Variants and improvements

- **Gaussian noisy max (GNMax).** Papernot et al. (2018) add Gaussian noise to the counts. With [Renyi DP](/renyi-differential-privacy/) accounting this gives smaller $\varepsilon$ for many queries.
- **Confident GNMax.** The same paper first checks, with noise, whether the largest count is above a threshold, and answers only those queries. Queries where the teachers disagree are skipped, so they cost little privacy.
- **Other students.** Any learner can be the student, including [knowledge distillation](/knowledge-distillation/) of soft labels, as long as it uses only the public points and the noisy labels.

## When to use it

Use PATE when the model is a classifier, public unlabeled data from a similar distribution is available, and the private data is large enough to train many good teachers. It is a good choice when the teachers must be trained by methods that are hard to make private, since they need no private training. When there is no public data, or when the task is not classification, use [DP-SGD](/dp-sgd/) instead.

## Pitfalls

- **A data-dependent split.** Line L1 with parts chosen by clustering or by the labels lets one example move many others between parts. Line L1 must use a fixed rule, such as the position or a random assignment made before the data is seen.
- **Positions under add/remove.** Line L1 by position $i \bmod k$ protects only under replace: removing one example shifts every later example to another part. Under add/remove, line L1 must assign each example by a key that does not change, such as a random draw or a hash of its identifier.
- **Counting gamma per answer.** The budget for line L5 counted as $\gamma$ per answer, as for report noisy max on counting queries under add/remove, is too small here: a moved vote lowers one count and raises another. Count $2\gamma$ for each answer of line L5.
- **Releasing the votes.** Line L5 that also returns the noisy counts, or line L7 that releases the teachers, is not covered by the theorem. Only the winning label of line L5 and the student of line L7 may leave.
- **Publishing the data-dependent epsilon.** A report of the $\varepsilon$ from the vote counts after line L5 uses the private data. Publish the worst-case bound, or a private version of the data-dependent one.
- **Too many queries.** Line L3 run over all public points makes the bound $2\gamma Q$ large. Query few points, and let line L6 use the rest without labels.

## Implementations

## History

Hamm, Cao and Belkin (ICML 2016) trained local classifiers on separate private data sets and transferred their votes to a global classifier on public data. Papernot, Abadi, Erlingsson, Goodfellow and Talwar (ICLR 2017) introduced PATE: deep network teachers on disjoint parts, the Laplace noisy max, a data-dependent moments accountant, and a student trained by semi-supervised learning with generative adversarial networks. They reported single-digit $\varepsilon$ on MNIST and SVHN. Papernot, Song, Mironov, Raghunathan, Talwar and Erlingsson (ICLR 2018) scaled PATE to more classes with the Gaussian noisy max and the confident aggregator.

## References
