---
tag: NQC1A8
kind: algorithm
slug: krum-aggregation
name: Krum
aliases:
- Krum aggregation rule
area: security-and-privacy/adversarial-machine-learning
level: research
summary: A Byzantine-robust aggregation rule that needs n > 2f + 2 and picks the update with the smallest sum of squared distances to its n - f - 2 nearest updates.
model: real-ram
complexity:
  vars: {n: the number of updates, d: the dimension of an update, f: the largest number of Byzantine updates}
  time: {worst: "O(n^2 (d + log n))"}
  space: {extra: "O(n)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2017
  people: [Peva Blanchard, El Mahdi El Mhamdi, Rachid Guerraoui, Julien Stainer]
  note: Blanchard, El Mhamdi, Guerraoui and Stainer proposed Krum at NeurIPS 2017. Coordinate-wise median and trimmed mean (Yin et al.) and Bulyan (El Mhamdi et al.) followed in 2018, and attacks that stay inside the honest spread in 2019.
prereqs: [byzantine-fault-tolerance, stochastic-gradient-descent, euclidean-distance]
see_also: [data-poisoning, median, trimmed-mean, geometric-median, approximate-agreement, backdoor-attack, gradient-inversion-attack, k-nearest-neighbors]
sources:
  - paper: "Peva Blanchard, El Mahdi El Mhamdi, Rachid Guerraoui and Julien Stainer, Machine learning with adversaries, Byzantine tolerant gradient descent, Advances in Neural Information Processing Systems 30 (NeurIPS) 2017, arXiv:1703.02757"
    locator: "arXiv:1703.02757v1: Lemma 1 (Section 3, linear rules), Definition 1 ((alpha, f)-Byzantine resilience), Section 4 (the score, Lemma 2 on the cost and Proposition 1 with eta(n, f)), Section 6 (m-Krum)"
  - paper: "Dong Yin, Yudong Chen, Kannan Ramchandran and Peter Bartlett, Byzantine-robust distributed learning, towards optimal statistical rates, Proceedings of the 35th International Conference on Machine Learning (ICML) 2018"
    locator: the coordinate-wise median and coordinate-wise trimmed mean rules and their error rates
  - paper: "El Mahdi El Mhamdi, Rachid Guerraoui and Sebastien Rouault, The hidden vulnerability of distributed learning in Byzantium, Proceedings of the 35th International Conference on Machine Learning (ICML) 2018"
    locator: attacks on Krum in high dimension and the Bulyan rule, which runs Krum repeatedly and then a coordinate-wise trimmed mean
  - paper: "Moran Baruch, Gilad Baruch and Yoav Goldberg, A little is enough, circumventing defenses for distributed learning, Advances in Neural Information Processing Systems 32 (NeurIPS) 2019"
    locator: Byzantine updates that stay within the spread of the honest updates and still bias the model under Krum and the median rules
  - paper: doi:10.1145/357172.357176
    title: Leslie Lamport, Robert Shostak and Marshall Pease, The Byzantine generals problem, ACM Transactions on Programming Languages and Systems 4(3), 1982, pages 382 to 401
    locator: the Byzantine fault model, in which faulty processes behave arbitrarily and may collude
---

Krum is an aggregation rule for distributed training with a parameter server: $n$ clients each send an update vector $V_i \in \mathbb{R}^d$ (a gradient estimate), at most $f$ of them are Byzantine and may send anything, and the server must pick a vector to step with. Krum gives each update the score $s(i)$, the sum of the **squared** distances from $V_i$ to its $n - f - 2$ nearest other updates, and returns the update with the smallest score. It is defined only when $n > 2f + 2$. Blanchard, El Mhamdi, Guerraoui and Stainer (2017) proposed it and proved that, when the honest updates are i.i.d. and their spread is small next to the true gradient, the chosen vector still points in a descent direction. The plain average fails against one Byzantine client.

## In plain words

Many workers each send a suggestion for the next step. Most are honest, but a few may lie, and the liars may work together. If you take the average, one liar can send a huge vector and drag the average anywhere.

Krum asks each suggestion a question: how close are you to your nearest neighbors? It counts only the closest neighbors, as many as it can be sure include mostly honest ones, and adds up the squared distances to them. Then it picks the suggestion with the smallest total, the one that sits in the tightest group.

A liar far away has a large total, so it is not picked. A liar can still be picked if it sits right among the honest suggestions, but then it is close to an honest one, so it cannot do much harm.

## The problem

**The threat model**, in the three parts of Biggio and Roli:

- *Goal of the attacker.* Stop the training from converging, or bias the model.
- *Knowledge.* Full. Blanchard et al. let the Byzantine clients know the rule, the data and the updates of all other clients, and collude.
- *Capability.* Control at most $f$ of the $n$ updates in each round, with arbitrary values. The server is trusted, and the honest updates are i.i.d. unbiased estimates of the gradient $g$.

**Input.** Vectors $V_1, \ldots, V_n \in \mathbb{R}^d$ and an integer $f \ge 0$ with $n > 2f + 2$.

**Output.** One of the input vectors, $V_{i^*}$, where $i^*$ minimizes

$$s(i) = \min_{S \subseteq \{1..n\} \setminus \{i\},\ |S| = n - f - 2} \ \sum_{j \in S} \lVert V_i - V_j \rVert^2 ,$$

with ties broken toward the smallest index, as Blanchard et al. do. The sum of the $n - f - 2$ smallest of the distances from $V_i$ is this minimum.

**Why $n - f - 2$.** Each update has $n - 1$ others. Leaving out $f + 1$ of them makes sure that at least one honest update is among those left out, so every Byzantine neighbor of an honest update is no farther than some honest update. And $n - f - 2 > f$ is what $n > 2f + 2$ says: the neighbor set of any update holds more updates than there are Byzantine ones, so at least $n - 2f - 2 \ge 1$ of them are honest, whether or not the update itself is honest. The proof of Proposition 1 of Blanchard et al. divides by this count. Whether the condition $2f + 2 < n$ is tight is left open in their Section 7.

## The algorithm

```pseudo id=main
KRUM(V_1, ..., V_n, f)
L1  if n <= 2f + 2 then fail
L2  for i = 1 to n do
L3      D <- [ ||V_i - V_j||^2 for every j != i ]
L4      sort D in increasing order
L5      s(i) <- D[1] + ... + D[n - f - 2]
L6      if s(i) < best score so far then i* <- i
L7  return V_{i*}
```

Line L1 rejects inputs where the guarantee cannot hold. Lines L3 to L5 compute the score: the $n - 1$ squared distances, sorted, and the sum of the first $n - f - 2$. Line L6 keeps the first index of smallest score, because the test is strict. Line L7 returns an input vector, never a new one.

**m-Krum.** Section 6 of the arXiv version picks $m$ updates by running Krum, removing the winner and running again, and averages the $m$ winners. Each round must be valid, so $n - m + 1 > 2f + 2$; the paper states the condition as $2f + 2 < n - m$.

## Example

One coordinate, $n = 5$, $f = 1$, so each score sums the $n - f - 2 = 2$ smallest squared distances. The updates are $V = (0, 1, 2, 4, 10)$, and $V_5 = 10$ is Byzantine.

| $i$ | $V_i$ | squared distances to the others | two smallest | $s(i)$ |
|---|---|---|---|---|
| 1 | 0 | 1, 4, 16, 100 | 1, 4 | 5 |
| 2 | 1 | 1, 1, 9, 81 | 1, 1 | 2 |
| 3 | 2 | 4, 1, 4, 64 | 1, 4 | 5 |
| 4 | 4 | 16, 9, 4, 36 | 4, 9 | 13 |
| 5 | 10 | 100, 81, 64, 36 | 36, 64 | 100 |

Krum returns $V_2 = 1$. The average is $17/5 = 3.4$, already pulled toward the Byzantine value; with $V_5 = 1000$ the average would be $201.4$, and Krum would still return $1$.

Now let the Byzantine client send $1.5$ instead. Its squared distances are $2.25, 0.25, 0.25, 6.25$, so its score is $0.5$, and the score of $V_2$ becomes $1 + 0.25 = 1.25$. Krum picks the Byzantine vector. But it lies between two honest updates, and the bound of the next section caps the harm: here $\rho^2 = 4$ (the honest update $2$ is within squared distance $4$ of every honest update), and the chosen vector must be within squared distance $\frac{n - f - 2}{n - 2f - 1} \rho^2 = \frac{2}{2} \cdot 4 = 4$ of some honest update. It is within $0.25$.

## Correctness

**The computation.** The sum of the $n - f - 2$ smallest entries of $D$ is the minimum over all sets $S$ of that size, so line L5 computes $s(i)$ exactly and line L6 returns the first minimizer.

**Theorem (a deterministic bound, proved on this page).** Let $H$ be the set of honest indices, with at most $f$ Byzantine indices and $n > 2f + 2$, and let $\rho^2 = \min_{i \in H} \max_{j \in H} \lVert V_i - V_j \rVert^2$. Then

$$\min_{j \in H} \lVert V_{i^*} - V_j \rVert^2 \ \le\ \frac{n - f - 2}{n - 2f - 1}\, \rho^2 .$$

The idea, from the proof of Proposition 1 of Blanchard et al.: an honest $i$ has at least $n - f - 1$ honest others, so $s(i) \le (n - f - 2) \rho_i^2$; a Byzantine $i^*$ has at most $f - 1$ Byzantine others, so at least $n - 2f - 1$ of its $n - f - 2$ nearest are honest, and $s(i^*) \ge (n - 2f - 1) \min_{j \in H} \lVert V_{i^*} - V_j \rVert^2$. Combine with $s(i^*) \le s(i)$. The full proof is in the proof file.

**Theorem (Blanchard et al. 2017, Proposition 1, cited).** If the honest updates are i.i.d. with mean $g$ and $\mathbb{E}\lVert G - g \rVert^2 = d \sigma^2$, $2f + 2 < n$ and $\eta(n, f) \sqrt{d}\, \sigma < \lVert g \rVert$, then Krum is $(\alpha, f)$-Byzantine resilient with $\sin \alpha = \eta(n, f) \sqrt{d}\, \sigma / \lVert g \rVert$: $\langle \mathbb{E}\,\mathrm{Kr}, g \rangle \ge (1 - \sin \alpha) \lVert g \rVert^2 > 0$, and the moments of order 2 to 4 of the output are bounded by those of $G$. Here

$$\eta(n, f) = \sqrt{2 \left(n - f + \frac{f (n - f - 2) + f^2 (n - f - 1)}{n - 2f - 2}\right)},$$

which is $O(n)$ when $f$ grows with $n$ and $O(\sqrt{n})$ when $f$ is fixed. Their Section 5 turns this into almost sure convergence of the gradient norm to a region where $\lVert \nabla Q \rVert \le \eta \sqrt{d}\, \sigma$.

## Complexity

- **Time.** Each of the $n$ updates needs $n - 1$ distances at $O(d)$ each (line L3) and a sort of $n - 1$ numbers (line L4), so the total is $O(n^2 (d + \log n))$, Lemma 2 of Blanchard et al. A selection algorithm such as [quickselect](/quickselect/) in place of the sort gives $O(n^2 d)$ expected time. Computing each distance once and storing the matrix halves the distance work and costs $O(n^2)$ space.
- **Space.** $O(n)$ extra for the list $D$ of one row, beyond the input.
- **m-Krum.** $m$ runs of Krum, so $O(m n^2 (d + \log n))$.

## Properties

- **Output is an input.** Krum returns one of the $V_i$ and never averages, so its variance is that of a single update. m-Krum trades some robustness for a lower variance.
- **Not linear.** Lemma 1 of Blanchard et al. shows that any rule $\sum_i \lambda_i V_i$ with nonzero $\lambda_i$ can be moved to any vector $U$ by one Byzantine update $V_n = \frac{1}{\lambda_n} U - \sum_{i < n} \frac{\lambda_i}{\lambda_n} V_i$. Krum escapes this because a far update gets a large score.
- **Deterministic and order dependent only through ties.** A permutation of the inputs changes the output only when two scores are equal.
- **Breakdown.** The rule tolerates $f < (n - 2)/2$ Byzantine updates, close to the bound $f < n/2$ of the median.

## Variants and improvements

- **m-Krum** (Blanchard et al., Section 6). Average $m$ winners of repeated Krum. The paper also mentions taking the $m$ best scores of one run and leaves its resilience open.
- **Coordinate-wise median and trimmed mean** (Yin et al. 2018). Aggregate each coordinate with the [median](/median/) or the [trimmed mean](/trimmed-mean/); they prove error rates that are optimal in their statistical model, and the cost is $O(n d)$ expected for the median by selection.
- **Bulyan** (El Mhamdi et al. 2018). Select $\theta = n - 2f$ updates by repeated Krum, then take a coordinate-wise trimmed mean around the median; it needs $n \ge 4f + 3$ and limits the drift per coordinate that Krum allows in high dimension.
- **Geometric median.** The point that minimizes the sum of distances, a robust center that is not an input; see [geometric median](/geometric-median/).

## When to use it

Use Krum when the honest updates are close to i.i.d. and the noise is small next to the gradient, which is the setting of its theorem, and when $n$ is small enough that $n^2$ distance computations per round are cheap. Prefer the coordinate-wise median or trimmed mean when $d$ is large and $n$ is large, since they cost $O(n d)$. With clients whose data differ (non-i.i.d. federated data), honest updates are far apart, the score of an honest outlier client is large, and Krum may ignore the same honest clients every round; then the guarantee does not hold, and the rule biases the model against those clients. None of these rules is a defense against a small targeted change such as a [backdoor](/backdoor-attack/) that stays inside the honest spread.

## Pitfalls

- **Distances that are not squared.** Line L3 must use $\lVert V_i - V_j \rVert^2$. The proofs of Blanchard et al. use squared distances, and so does the bound above; a variant with plain distances is a different rule with no proof here.
- **Counting the update itself.** Line L5 sums $n - f - 2$ distances to *other* updates. Sorting all $n$ distances, including the zero distance to itself, and then summing $n - f - 2$ values sums one other too few. Lemma 2 of Blanchard et al. sums $n - f - 1$ values for this reason, since that list includes the zero.
- **Skipping the size check.** Line L1 must reject $n \le 2f + 2$, the range where the theorem of Blanchard et al. does not apply. For $n \le 2f + 1$ the rule fails outright: then $n - f - 2 \le f - 1$, so $f$ colluders that send the same vector have only each other among their nearest, get score $0$ and win.
- **Ignoring attacks inside the spread.** The bound limits the distance to the honest updates in terms of their spread $\rho$. Baruch et al. (2019) choose Byzantine updates that move each coordinate by a fraction of the honest standard deviation in the same direction every round; this stays within the bound and still biases training. In high dimension the spread $\rho$ grows like $\sqrt{d}\, \sigma$, which is the weakness that Bulyan addresses.
- **Treating the score of one round as an identity.** Krum gives no list of Byzantine clients. An honest client with unusual data looks the same as a Byzantine one.

## Implementations

The code runs only on update vectors that the tests build from a fixed seed, from Gaussian draws and from the logistic gradients of mlkit on synthetic blobs; it never talks to a client or a network. The tests compare the scores and the choice with brute force over every set of $n - f - 2$ other updates on 600 random inputs (half of them with small integers, so that ties occur), check m-Krum against repeated brute force, check the distance bound of the theorem against four abstract Byzantine strategies, check Lemma 1 for the average, and run 40 rounds of training with 2 Byzantine clients out of 9.

## History

Byzantine faults come from Lamport, Shostak and Pease (1982). Blanchard, El Mhamdi, Guerraoui and Stainer (2017) brought the model to distributed stochastic gradient descent, showed that linear rules break with one Byzantine worker, and proposed Krum with its resilience and convergence analysis. In 2018 Yin et al. analyzed the coordinate-wise median and trimmed mean, and El Mhamdi, Guerraoui and Rouault showed that Krum allows a large drift in high dimension and proposed Bulyan. Baruch, Baruch and Goldberg (2019) showed small coordinated changes that pass these rules.

## References
