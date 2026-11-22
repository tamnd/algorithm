---
tag: DEFG9T
kind: algorithm
slug: spectral-signatures-defense
name: Spectral signatures
aliases:
- spectral signature backdoor detection
area: security-and-privacy/adversarial-machine-learning
level: research
summary: Finds poisoned training points by their large projection on the top singular vector of the centered learned features of each class, then removes the top 1.5 epsilon fraction.
model: real-ram
complexity:
  vars: {n: the number of points of one class, d: the dimension of a feature vector, t: the number of power iteration steps}
  time: {worst: "O(n d^2 + t d^3 + n log n)"}
  space: {extra: "O(d^2 + n)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2018
  people: [Brandon Tran, Jerry Li, Aleksander Madry]
  note: Tran, Li and Madry proposed the method at NeurIPS 2018. It uses the spectral idea of robust mean estimation from 2016, and robust whitening (SPECTRE, 2021) made it stronger.
prereqs: [backdoor-attack, singular-value-decomposition, principal-component-analysis]
see_also: [data-poisoning, power-iteration, clean-label-poisoning, svm-poisoning-attack, krum-aggregation, trimmed-mean, machine-unlearning]
sources:
  - paper: "Brandon Tran, Jerry Li and Aleksander Madry, Spectral signatures in backdoor attacks, Advances in Neural Information Processing Systems 31 (NeurIPS) 2018, arXiv:1811.00636"
    locator: "Definition 3.1 (the spectral signature), Lemma 3.1 (separation when the squared mean shift is at least 6 sigma^2 / epsilon), Algorithm 1 (remove the top 1.5 epsilon fraction of scores in each label and retrain)"
  - paper: "Ilias Diakonikolas, Gautam Kamath, Daniel Kane, Jerry Li, Ankur Moitra and Alistair Stewart, Robust estimators in high dimensions without the computational intractability, IEEE Symposium on Foundations of Computer Science (FOCS) 2016"
    locator: the filter that removes points with a large projection on the top eigenvector of the empirical covariance
  - paper: "Jonathan Hayase, Weihao Kong, Raghav Somani and Sewoong Oh, SPECTRE, defending against backdoor attacks using robust statistics, Proceedings of the 38th International Conference on Machine Learning (ICML) 2021"
    locator: robust whitening of the features before the spectral score, for poison that the plain score misses
  - paper: "Bryant Chen, Wilka Carvalho, Nathalie Baracaldo, Heiko Ludwig, Benjamin Edwards, Taesung Lee, Ian Molloy and Biplav Srivastava, Detecting backdoor attacks on deep neural networks by activation clustering, arXiv:1811.03728, 2018"
    locator: the activation clustering defense, which splits the features of each label into two clusters
  - paper: "Battista Biggio and Fabio Roli, Wild patterns, ten years after the rise of adversarial machine learning, Pattern Recognition 84, 2018"
    locator: the threat model in three parts, goal, knowledge and capability
---

Spectral signatures is a defense against [backdoor attacks](/backdoor-attack/) and other [data poisoning](/data-poisoning/) that plants a group of mislabeled points in one class. Tran, Li and Madry (2018) observed that in the learned features of a trained network (a late layer), the poisoned points of a class differ from the clean points of that class in their mean, and that this shift shows in the top singular vector of the centered feature matrix. The method trains the network, takes the feature vectors $R_1, \ldots, R_n$ of each label, gives each point the score $\tau_i = \langle R_i - \hat\mu, v \rangle^2$ for the top right singular vector $v$, removes the $\lfloor 1.5\, \epsilon n \rfloor$ points of largest score, where $\epsilon$ is an assumed upper bound on the poisoned fraction, and retrains. The separation is a theorem about the population; the factor $1.5$ is a tuned heuristic.

## In plain words

A backdoor adds some images with a small trigger and the wrong label. The trained network learns the trigger, so inside the network those images look a little different from the real images of that label. They all differ in the same way.

Take all the images of one label and look at their feature vectors. Find the one direction in which the vectors spread the most. If the poisoned group is large enough and far enough away, that direction points from the clean group to the poisoned group, because the gap between the groups adds spread in that direction.

Now measure each point along that direction, from the center. The poisoned points are far out. Throw away the points that are farthest out, a little more than you think are poisoned, and train again.

## The problem

**The threat model**, in the three parts of Biggio and Roli:

- *Goal of the attacker.* A backdoor: test inputs with a trigger go to a target label, and the accuracy on clean inputs stays high.
- *Knowledge.* The attacker knows the data distribution and the trigger, and may know the architecture. Tran et al. do not let the attacker adapt the poison to the defense.
- *Capability.* Add at most an $\epsilon$ fraction of points to the training set of the target label, with any inputs. The defender has the whole training set and the trained network, and needs no clean held-out set.

**Input.** Feature vectors $R_1, \ldots, R_n \in \mathbb{R}^d$ of the points of one label, and a number $\epsilon \ge 0$.

**Output.** A split of the indices into a removed set of size $k = \min(n, \lfloor 1.5\, \epsilon n \rfloor)$ and a kept set, such that every removed score is at least every kept score.

**The model behind it.** The features of one label come from the mixture $F = (1 - \epsilon) D + \epsilon W$ of a clean distribution $D$ and a poisoned distribution $W$, with means $\mu_D, \mu_W$, covariances $\Sigma_D, \Sigma_W \preceq \sigma^2 I$, and shift $\Delta = \mu_W - \mu_D$. Definition 3.1 of Tran et al. calls a large projection of the poisoned points on the top singular vector a spectral signature.

## The algorithm

```pseudo id=main
SPECTRAL-FILTER(R_1, ..., R_n, epsilon)
L1  mu <- (R_1 + ... + R_n) / n
L2  C <- sum over i of (R_i - mu)(R_i - mu)^T        // C = M^T M for the centered matrix M
L3  v <- a unit eigenvector of the largest eigenvalue of C
L4  tau_i <- ((R_i - mu) . v)^2 for i = 1 to n
L5  sort the indices by tau in decreasing order
L6  remove the first floor(1.5 epsilon n) indices and return the rest
```

Lines L1 and L2 center the features and form $M^\top M$, whose top eigenvector is the top right singular vector of $M$. Line L3 finds it by [power iteration](/power-iteration/) in the code; a full [singular value decomposition](/singular-value-decomposition/) gives the same vector. Line L4 squares the projection, so the sign of $v$ does not matter. Lines L5 and L6 cut a fixed number of points.

**The full defense** (Algorithm 1 of Tran et al.). Train the network on all data, run SPECTRAL-FILTER on the features of each label separately, take the union of the kept points, and train a new network on them from scratch.

## Example

Two coordinates and $n = 8$ points of one label. The last two points are poisoned, so $\epsilon = 0.25$.

$$R = (-2,0),\ (-1,1),\ (-1,-1),\ (-1,2),\ (-1,-2),\ (0,0),\ (3,0),\ (3,0).$$

The mean is $\hat\mu = (0, 0)$, and $C = M^\top M = \begin{pmatrix} 26 & 0 \\ 0 & 10 \end{pmatrix}$, so $v = (1, 0)$. About this mean, the six clean points give a sum of squares of $8$ in the first coordinate and $10$ in the second, so alone they would point $v$ along the second coordinate. The two poisoned points add $18$ to the first. The scores are the squared first coordinates:

| $i$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| $\tau_i$ | 4 | 1 | 1 | 1 | 1 | 0 | 9 | 9 |

The cut is $\lfloor 1.5 \cdot 0.25 \cdot 8 \rfloor = 3$, so the filter removes points 7 and 8, the poisoned ones, and also point 1, a clean point. This is the price of the margin $1.5$.

## Correctness

**The computation.** $M^\top M = C$, so the top right singular vector of $M$ is a top eigenvector of $C$; the scores of line L4 are the squared entries of $M v$, and lines L5 and L6 remove exactly the $k$ largest. When the top eigenvalue is simple, $v$ is unique up to sign, so the scores are unique.

**Theorem (the top direction follows the shift, proved on this page).** For the mixture $F$ above, with $0 < \epsilon < 1$,

$$\Sigma_F = (1 - \epsilon) \Sigma_D + \epsilon \Sigma_W + \epsilon (1 - \epsilon) \Delta \Delta^\top,$$

and every unit top eigenvector $v$ of $\Sigma_F$ satisfies $\langle v, \Delta \rangle^2 \ge \lVert \Delta \rVert^2 - \sigma^2 / (\epsilon (1 - \epsilon))$. The proof compares $v^\top \Sigma_F v$ with the value at $\Delta / \lVert \Delta \rVert$.

**Theorem (separation, proved on this page).** If also $\epsilon < 1/2$ and $\lVert \Delta \rVert^2 \ge 6 \sigma^2 / \epsilon$, then with the threshold $t = \lvert \langle v, \Delta \rangle \rvert / 2$ on $\lvert \langle x - \mu_F, v \rangle \rvert$, a clean point is above $t$ with probability at most $\epsilon / (1 - 2\epsilon)^2$, and a poisoned point is below $t$ with probability at most the same. For $\epsilon = 0.05$ the bound is about $0.062$. Lemma 3.1 of Tran et al. is a separation result of this kind under the same condition $\lVert \Delta \rVert^2 \ge 6\sigma^2/\epsilon$. The full proofs are in the proof file.

**What is not proved.** Both theorems are about the population covariance. The algorithm uses the empirical one, which is close when $n$ is large next to $d$; this is a standard argument that the page does not give. The factor $1.5$ and the use of a late layer are tuned heuristics of Tran et al. The method cannot know $\epsilon$; it must be given.

## Complexity

- **Time.** Line L2 costs $O(n d^2)$. Power iteration costs $O(d^2)$ per step and $t$ steps, where $t$ depends on the gap between the two largest eigenvalues. A single start can be orthogonal to the top eigenvector, so the code first squares $C$ eight times (cost $O(d^3)$ each, the same as $256$ power steps), then runs the iteration from each of the $d$ columns of the result and keeps the best, $O(t d^3)$ in all. A full SVD of $M$ costs $O(n d^2)$ instead. Line L4 costs $O(n d)$ and line L5 $O(n \log n)$. Selection in place of the sort gives $O(n)$ for the cut.
- **Space.** $O(d^2)$ for $C$ and $O(n)$ for the scores.
- **Full defense.** One extra training run, one forward pass over the data for the features, and a filter per label. The second training run dominates.

## Properties

- **No clean data needed.** The defender uses only the training set and the network trained on it.
- **Per label.** The filter runs separately on each label, so it looks for a group inside one label, the label that the attacker targets.
- **Always removes points.** It removes $\lfloor 1.5\, \epsilon n \rfloor$ points of every label, poisoned or not, so on clean data it loses that many clean points.
- **Not exact.** The output depends on the empirical covariance; a few poisoned points can stay and a few clean points can go, as in the example.

## Variants and improvements

- **Robust mean estimation filters** (Diakonikolas et al. 2016). The same score with a data-driven threshold, repeated until the top eigenvalue of the covariance is small; this is the robust statistics origin of the method.
- **SPECTRE** (Hayase et al. 2021). Estimate the clean covariance robustly, whiten the features with it, and score in the whitened space, which finds poison that is weak next to the natural spread.
- **Activation clustering** (Chen et al. 2018). Reduce the features of each label to few dimensions and split them into two clusters; a small cluster is suspect.
- **Scores from several directions.** Projecting on the top few singular vectors in place of one handles poison with more than one trigger in a label.

## When to use it

Use it when a backdoor plants many points of one label and they share a trigger that the network learns, so that their features move together; and when an extra training run is affordable. It needs an upper bound $\epsilon$ on the poisoned fraction. It is a poor fit when the poison is a small fraction with a small shift, below the $6\sigma^2/\epsilon$ scale, or when the clean features of a label have one direction of very large spread, which then wins the top singular vector. It does not address [poisoning of an SVM](/svm-poisoning-attack/) by a few points chosen to raise the error, which need not form a group, and it is not a rule for aggregating updates in distributed training, which is the setting of [Krum](/krum-aggregation/).

## Pitfalls

- **Raw inputs in place of learned features.** The shift that the theorem needs is in the representation of the trained network. In pixel space the trigger is a small change and the natural spread is large; Tran et al. use a late layer.
- **Mixing labels.** Running one filter on all labels together finds the directions between labels, not the poison. Run it per label.
- **Rounding the cut.** $1.5\, \epsilon n$ is often a whole number in exact arithmetic but not in floating point; for $\epsilon = 0.3$ and $n = 60$ the product is $27$, but in double precision it is $26.999999999999996$, and the floor is $26$. The code adds $10^{-9}$ before the floor.
- **Adaptive poison.** An attacker who knows the defense can spread the poison or keep its features close to the clean mean. The theorem then does not apply, and Tran et al. do not claim robustness to this.
- **Removing is not unlearning.** Retraining on the kept points is needed; deleting points from a trained model in place needs [machine unlearning](/machine-unlearning/).

## Implementations

The code runs only on feature vectors that the tests build from a fixed seed: Gaussian clean points and a shifted Gaussian group for the poison. It never reads a real data set or a real network. The tests compare the scores and the top direction with an independent Jacobi eigensolver on 500 random inputs whose top eigenvalue is well separated, check a matrix whose largest column is orthogonal to the top eigenvector, check that the removed scores are at least the kept ones on 500 inputs with ties, check the first theorem on 500 random mixtures, and measure detection with $n = 200$, $d = 8$, $\epsilon = 0.05$ and $\lVert \Delta \rVert^2 = 6/\epsilon$, where all poisoned points are removed in each of 5 trials.

## History

Spectral filters for robust mean estimation appeared in 2016 (Diakonikolas, Kamath, Kane, Li, Moitra and Stewart, and in parallel Lai, Rao and Vempala). Tran, Li and Madry (2018) applied the idea to the learned features of backdoored networks and showed on real image data that it removes poisoned points. Chen et al. (2018) proposed activation clustering at the same time, and Hayase, Kong, Somani and Oh (2021) added robust whitening in SPECTRE.

## References
