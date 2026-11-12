---
tag: MSKX4H
kind: theorem
slug: k-means-plus-plus-guarantee
name: k-means++ approximation guarantee
aliases:
- Arthur-Vassilvitskii bound
- k-means++ O(log k) bound
area: machine-learning/clustering
level: advanced
summary: "The k-means++ seeds have expected k-means cost at most 8(ln k + 2) times the optimum, and the factor Theta(log k) is tight for this seeding."
prereqs: [k-means-plus-plus, k-means-problem]
see_also: [k-means-plus-plus, k-means, k-means-problem, approximation-ratio, triangle-inequality, k-median-problem, randomized-algorithm]
sources:
  - paper: "David Arthur and Sergei Vassilvitskii, k-means++: the advantages of careful seeding, Proceedings of the 18th Annual ACM-SIAM Symposium on Discrete Algorithms (SODA), 2007, pages 1027 to 1035"
    locator: Lemma 2.1 (centroid identity), Lemmas 3.1 to 3.3 and Theorem 3.1 (the upper bound), Lemma 4.1 and Theorem 4.1 (the lower bound), Theorem 5.1 (D^l seeding)
  - book: isbn:9781107057135
    title: Shai Shalev-Shwartz and Shai Ben-David, Understanding Machine Learning, From Theory to Algorithms, Cambridge University Press, 2014
    locator: Section 22.2 (the k-means objective and the centroid as the best center)
  - paper: "Rafail Ostrovsky, Yuval Rabani, Leonard J. Schulman and Chaitanya Swamy, The effectiveness of Lloyd-type methods for the k-means problem, 47th IEEE Symposium on Foundations of Computer Science (FOCS), 2006, pages 165 to 176"
    locator: the analysis of a similar seeding on well separated inputs
---

The k-means++ guarantee states that the $k$ centers chosen by [k-means++ seeding](/k-means-plus-plus/) have an expected [k-means cost](/k-means-problem/) of at most $8(\ln k + 2)$ times the optimal cost, for every finite set of points in $\mathbb{R}^d$. The bound comes from the seeding alone, before any iteration of the [k-means algorithm](/k-means/), and it does not depend on $n$ or $d$. Arthur and Vassilvitskii proved it in 2007 and also showed that the factor is tight up to a constant: some inputs force an expected factor of $2 \ln k$.

## Statement

Let $X \subset \mathbb{R}^d$ be a finite set of $n$ points with the Euclidean norm, and $1 \le k \le n$. For a finite set $C$ of centers and $Y \subseteq X$ write $D(x) = \min_{c \in C} \|x - c\|$ and $\phi(Y) = \sum_{x \in Y} D(x)^2$. Let $\phi_{\mathrm{OPT}}$ be the least value of $\phi(X)$ over all sets of $k$ centers. Let $C$ be built by D² seeding: $c_1$ uniform in $X$, and each next center $x \in X$ with probability $D(x)^2 / \phi(X)$ for the centers so far, until $|C| = k$.

**Theorem (Arthur and Vassilvitskii, 2007).** $\mathbb{E}[\phi(X)] \le 8(\ln k + 2) \, \phi_{\mathrm{OPT}}$.

**Lower bound.** For each $k$ there are inputs on which $\mathbb{E}[\phi(X)] \ge (2 \ln k - o(\ln k)) \, \phi_{\mathrm{OPT}}$ for D² seeding.

The expectation is over the random choices of the seeding only; the bound holds for every input. It is an approximation in expectation, not a bound on each run.

## In plain words

k-means++ picks its first guesses with a rule that favors far points. The theorem says that this rule is never much worse than the best possible answer, on average. The total squared distance of the guesses is at most about $8 \ln k$ times the best total, whatever the data looks like. The number of points and the number of features do not matter.

The bound has a logarithm because the method can still waste a guess on a group it already covers. The second half of the theorem says that some data really makes it waste guesses this often, so the logarithm cannot be removed for this rule.

## Proof

Fix an optimal set of $k$ centers and its clusters $A_1, \ldots, A_k$, each point in the cluster of its nearest optimal center. Each optimal center is the mean of its cluster, so $\phi_{\mathrm{OPT}}(A) = \sum_{x \in A} \|x - \mu(A)\|^2$, with $\mu(A)$ the mean of $A$. If some $A_j$ is empty, the proof below runs with fewer clusters and the extra centers only lower the cost; so we assume that all $k$ clusters are non-empty. We use the centroid identity of the [k-means problem](/k-means-problem/): for each $z$,
$$\sum_{x \in A} \|x - z\|^2 = \phi_{\mathrm{OPT}}(A) + |A| \, \|\mu(A) - z\|^2 . \tag{1}$$

**Lemma 1 (a uniform center).** Let $A$ be an optimal cluster and $a$ uniform in $A$. With the single center $a$, $\mathbb{E}[\phi(A)] = 2 \phi_{\mathrm{OPT}}(A)$.

*Proof.* By (1), $\mathbb{E}[\phi(A)] = \frac{1}{|A|} \sum_{a \in A} \sum_{x \in A} \|x - a\|^2 = \frac{1}{|A|} \sum_{a \in A} \big( \phi_{\mathrm{OPT}}(A) + |A| \|a - \mu(A)\|^2 \big) = 2 \phi_{\mathrm{OPT}}(A)$. $\square$

**Lemma 2 (a D² center).** Let $C$ be a set of centers with $\phi(A) > 0$ for an optimal cluster $A$. Add one center $a \in A$ chosen with probability $D(a)^2 / \phi(A)$. Then the new cost of $A$ has expectation at most $8 \phi_{\mathrm{OPT}}(A)$.

*Proof.* The new cost of $A$ is $\sum_{x \in A} \min(D(x), \|x - a\|)^2$. For $a, x \in A$ the [triangle inequality](/triangle-inequality/) gives $D(a) \le D(x) + \|x - a\|$, so $D(a)^2 \le 2 D(x)^2 + 2 \|x - a\|^2$. Average over $x \in A$:
$$D(a)^2 \le \frac{2}{|A|} \sum_{x \in A} D(x)^2 + \frac{2}{|A|} \sum_{x \in A} \|x - a\|^2 .$$
Put this bound into the expectation $\sum_{a \in A} \frac{D(a)^2}{\phi(A)} \sum_{x \in A} \min(D(x), \|x - a\|)^2$. The first part gives
$$\frac{2}{|A|} \sum_{a \in A} \frac{\sum_x D(x)^2}{\phi(A)} \sum_{x \in A} \min(D(x), \|x - a\|)^2 \le \frac{2}{|A|} \sum_{a \in A} \sum_{x \in A} \|x - a\|^2 ,$$
because the fraction equals 1 and the minimum is at most $\|x - a\|^2$. The second part gives
$$\frac{2}{|A|} \sum_{a \in A} \frac{\sum_x \|x - a\|^2}{\phi(A)} \sum_{x \in A} \min(D(x), \|x - a\|)^2 \le \frac{2}{|A|} \sum_{a \in A} \sum_{x \in A} \|x - a\|^2 ,$$
because the minimum is at most $D(x)^2$ and $\sum_x D(x)^2 = \phi(A)$. By Lemma 1, each right side is $2 \cdot 2 \phi_{\mathrm{OPT}}(A)$. The sum is $8 \phi_{\mathrm{OPT}}(A)$. $\square$

**Lemma 3 (the induction).** Let $C$ be any set of centers with cost $\phi = \phi(X) > 0$. Call $u \ge 1$ optimal clusters *uncovered*, let $X_u$ be the union of their points, and let $X_c = X \setminus X_u$. Add $t$ centers by D² seeding, with $0 \le t \le u$, and let $\phi'$ be the cost after them. With $H_t = 1 + \frac12 + \cdots + \frac1t$ and $H_0 = 0$,
$$\mathbb{E}[\phi'] \le \big( \phi(X_c) + 8 \phi_{\mathrm{OPT}}(X_u) \big)(1 + H_t) + \frac{u - t}{u} \, \phi(X_u) .$$

*Proof.* Induction on $t$, with $u$ free. All costs on the right side are those of $C$. The right side grows with $\phi(X_c)$ and with $\phi(X_u)$. If at some time the cost is 0, all later costs are 0 and the claim holds; so we assume each step has $\phi > 0$.

*Case $t = 0$.* Then $\phi' = \phi(X_c) + \phi(X_u)$, which is at most the right side.

*Case $t = u = 1$.* The new center lies in $X_u$, which is one cluster $A$, with probability $\phi(X_u)/\phi$; then by Lemma 2 the expected new cost is at most $\phi(X_c) + 8\phi_{\mathrm{OPT}}(X_u)$. Otherwise, with probability $\phi(X_c)/\phi$, the cost does not increase. So $\mathbb{E}[\phi'] \le \phi(X_c) + 8\phi_{\mathrm{OPT}}(X_u) + \frac{\phi(X_c)}{\phi} \phi \le 2(\phi(X_c) + 8\phi_{\mathrm{OPT}}(X_u))$, which is the right side with $H_1 = 1$.

*Case $t \ge 1$, $u \ge 2$.* Assume the claim for $t - 1$ and all $u$. Look at the first new center.

It lies in $X_c$ with probability $\phi(X_c)/\phi$. No cost increases, and the claim for $(t - 1, u)$ bounds the rest by
$$\big( \phi(X_c) + 8\phi_{\mathrm{OPT}}(X_u) \big)(1 + H_{t-1}) + \frac{u - t + 1}{u} \phi(X_u) .$$

It lies in the uncovered cluster $A$ with probability $\phi(A)/\phi$, and given this, it is a D² draw from $A$. Then $A$ becomes covered. By Lemma 2 the expected new cost of $A$ is at most $8\phi_{\mathrm{OPT}}(A)$, and the claim for $(t - 1, u - 1)$, with $A$ moved to the covered part, bounds the rest by
$$\big( \phi(X_c) + 8\phi_{\mathrm{OPT}}(A) + 8\phi_{\mathrm{OPT}}(X_u) - 8\phi_{\mathrm{OPT}}(A) \big)(1 + H_{t-1}) + \frac{u - t}{u - 1} \big( \phi(X_u) - \phi(A) \big) .$$
(The bound for $(t-1, u-1)$ is linear in the cost of the covered part, so we may take the expectation over the center in $A$ first.)

Sum the second case over the $u$ uncovered clusters with the weights $\phi(A)/\phi$. The power mean inequality gives $\sum_A \phi(A)^2 \ge \phi(X_u)^2 / u$, so
$$\sum_A \phi(A) \big( \phi(X_u) - \phi(A) \big) \le \phi(X_u)^2 - \frac{\phi(X_u)^2}{u} = \frac{u - 1}{u} \phi(X_u)^2 .$$
So the second case adds at most $\frac{\phi(X_u)}{\phi} \big( \phi(X_c) + 8\phi_{\mathrm{OPT}}(X_u) \big)(1 + H_{t-1}) + \frac{u - t}{u} \cdot \frac{\phi(X_u)}{\phi} \phi(X_u)$.

Add the two cases and use $\frac{\phi(X_c)}{\phi} + \frac{\phi(X_u)}{\phi} = 1$ and $\frac{u - t + 1}{u} = \frac{u - t}{u} + \frac1u$:
$$\mathbb{E}[\phi'] \le \big( \phi(X_c) + 8\phi_{\mathrm{OPT}}(X_u) \big)(1 + H_{t-1}) + \frac{u - t}{u} \phi(X_u) + \frac{1}{u} \cdot \frac{\phi(X_c) \, \phi(X_u)}{\phi} .$$
The last term is at most $\phi(X_c)/u \le \phi(X_c)/t$, because $\phi(X_u) \le \phi$ and $t \le u$. Since $H_{t-1} + 1/t = H_t$, the claim follows. $\square$

**Proof of the theorem.** The first center $c_1$ is uniform in $X$. Given that it lies in the optimal cluster $A$, it is uniform in $A$. Apply Lemma 3 to $C = \{c_1\}$ with the $u = k - 1$ other clusters uncovered and $t = k - 1$ new centers. The last term is 0, so
$$\mathbb{E}[\phi' \mid c_1] \le \big( \phi(A) + 8\phi_{\mathrm{OPT}} - 8\phi_{\mathrm{OPT}}(A) \big)(1 + H_{k-1}) .$$
By Lemma 1, $\mathbb{E}[\phi(A) \mid c_1 \in A] = 2\phi_{\mathrm{OPT}}(A) \le 8\phi_{\mathrm{OPT}}(A)$. So $\mathbb{E}[\phi'] \le 8\phi_{\mathrm{OPT}}(1 + H_{k-1})$. Finally $H_{k-1} \le 1 + \ln k$, which gives $8(\ln k + 2)\phi_{\mathrm{OPT}}$. For $k = 1$ the bound is $2\phi_{\mathrm{OPT}}$ by Lemma 1 alone. $\square$

**The lower bound (sketch of Section 4 of the paper).** Take $k$ regular simplices, each with $n/k$ vertices and edge length $\delta$, in mutually orthogonal subspaces, so that the centers of two simplices are far apart compared with $\delta$. The optimal clusters are the simplices. A D² draw lands in an uncovered simplex with high probability, but not always, and once only a few simplices are uncovered their total weight is comparable with the weight of the covered ones. When $n/k$ grows and the distance between the simplices is tuned to $\delta$, the expected number of simplices that stay uncovered behaves like a harmonic sum. Arthur and Vassilvitskii show by an induction of the same form as Lemma 3 that the expected cost is then at least $2 \ln k \cdot \phi_{\mathrm{OPT}}$ up to lower order terms (their Theorem 4.1).

## Consequences

- **An $O(\log k)$ approximation in linear time.** The seeding runs in $O(nkd)$ time and is an expected $O(\log k)$ approximation for the [k-means problem](/k-means-problem/), which is NP-hard.
- **The bound survives Lloyd's algorithm.** The [k-means algorithm](/k-means/) never increases the cost, so k-means++ followed by Lloyd's iterations has the same expected bound.
- **High probability by repetition.** By Markov's inequality one run has cost at most $16(\ln k + 2)\phi_{\mathrm{OPT}}$ with probability at least $1/2$. The best of $r$ independent runs fails this only with probability at most $2^{-r}$.
- **Other powers.** The same proof with the inequality $(a + b)^\ell \le 2^{\ell - 1}(a^\ell + b^\ell)$ gives $2^{2\ell}(\ln k + 2)$ for the cost $\sum D(x)^\ell$ with $D^\ell$ seeding (Theorem 5.1 of the paper). For $\ell = 1$ this covers the [k-median problem](/k-median-problem/) in a Euclidean space and, more generally, in a [metric space](/metric-space/).
- **A base for other methods.** Analyses of k-means||, of the local search of Lattanzi and Sohler, and of coresets build on Lemmas 1 to 3.

## Tightness

- **The logarithm.** The lower bound shows that no analysis of D² seeding alone can give a factor $o(\log k)$. The constant 8 is not known to be tight; the gap between $2 \ln k$ and $8 \ln k$ is open as far as the paper goes.
- **Expectation, not each run.** A single run can be much worse than the bound: in the example of the k-means++ page, both seeds land in the same natural cluster with probability $37/2666$, and then the cost is 61 times the optimum.
- **Uniform seeding has no bound.** If the centers are $k$ data points chosen uniformly, the expected cost can be arbitrarily larger than $\phi_{\mathrm{OPT}}$: take $k = 2$, many points at 0 and one point far away. D² weights make the far point likely to be a center.
- **Constant factors need more.** Constant factor algorithms exist, for example local search with $9 + \varepsilon$ (Kanungo and others, 2004), and D² seeding followed by a short local search (Lattanzi and Sohler, 2019).

## History

Arthur and Vassilvitskii presented the theorem at SODA 2007, together with the matching lower bound and the extension to $D^\ell$ seeding. Ostrovsky, Rabani, Schulman and Swamy had analysed a similar seeding in 2006 under a separation condition on the data. The proof by covered and uncovered clusters became a standard tool for the later analyses of seeding methods.

## References
