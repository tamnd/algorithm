---
tag: JRGGZ5
kind: problem
slug: maximum-inner-product-search
name: Maximum inner product search
aliases:
- MIPS
area: searching/similarity-search
level: advanced
summary: Find the stored vector with the largest inner product with a query vector.
prereqs: [nearest-neighbor-search, dot-product]
see_also: [nearest-neighbor-search, approximate-nearest-neighbor, locality-sensitive-hashing, random-hyperplane-lsh, ball-tree, convex-hull, cosine-similarity, orthogonal-vectors]
sources:
  - paper: doi:10.1145/2339530.2339677
    title: Parikshit Ram and Alexander G. Gray, Maximum inner-product search using cone trees, Proceedings of the 18th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD 2012)
    locator: pages 931 to 939 (the problem, the failure of the metric indexes, and the branch-and-bound bounds for ball trees and cone trees)
  - paper: "Anshumali Shrivastava and Ping Li, Asymmetric LSH (ALSH) for sublinear time maximum inner product search (MIPS), Advances in Neural Information Processing Systems 27 (NIPS 2014)"
    locator: pages 2321 to 2329 (the impossibility of a symmetric LSH for inner products over R^d, and the asymmetric transforms with the norm powers)
  - paper: doi:10.1145/2645710.2645741
    title: Yoram Bachrach, Yehuda Finkelstein, Ran Gilad-Bachrach, Liran Katzir, Noam Koenigstein, Nir Nice and Ulrich Paquet, Speeding up the Xbox recommender system using a euclidean transformation for inner-product spaces, Proceedings of the 8th ACM Conference on Recommender Systems (RecSys 2014)
    locator: pages 257 to 264 (the extra coordinate that turns MIPS into Euclidean nearest neighbor search)
  - paper: "Behnam Neyshabur and Nathan Srebro, On symmetric and asymmetric LSHs for inner product search, Proceedings of the 32nd International Conference on Machine Learning (ICML 2015)"
    locator: PMLR volume 37, pages 1926 to 1934 (simple-LSH, the reduction to the angular distance on the unit sphere, and the comparison with ALSH)
  - paper: doi:10.1016/j.tcs.2005.09.023
    title: Ryan Williams, A new algorithm for optimal 2-constraint satisfaction and its implications, Theoretical Computer Science 348(2-3), 2005
    locator: pages 357 to 365 (the reduction from CNF satisfiability to orthogonal vectors)
---

Maximum inner product search (MIPS) asks, for a set $P$ of $n$ vectors in $\mathbb{R}^d$ and a query $q$, for a vector $p \in P$ that maximizes the [dot product](/dot-product/) $\langle q, p \rangle$. It is the query of recommender systems built on matrix factorization, where users and items are vectors and the predicted rating is their inner product, and of the output layer of classifiers with many classes. The inner product is not a distance: a vector need not be its own best match, and the [triangle inequality](/triangle-inequality/) does not hold. So [metric indexes](/metric-space-indexing/) and the usual [locality-sensitive hashing](/locality-sensitive-hashing/) do not apply directly. One extra coordinate reduces exact MIPS to Euclidean [nearest neighbor search](/nearest-neighbor-search/), and asymmetric transforms reduce approximate MIPS to angular LSH. In the plane the answer is a vertex of the [convex hull](/convex-hull/) and a query takes $O(\log n)$ time; in dimension $c \log n$, the batch version cannot be solved in time $O(n^{2 - \varepsilon})$ unless the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/) fails.

## In plain words

A movie service describes each user and each movie by a list of numbers learned from ratings. To guess how much a user likes a movie, it multiplies the two lists entry by entry and adds the products. A large sum means a good match. To recommend, it needs the movie with the largest sum for this user, out of millions.

This is not the same as finding the closest movie. A movie with long lists, a very popular one, can win against a movie that points in nearly the same direction as the user but has short lists. Tools built for closeness, which rely on the rule that a detour is never shorter than the direct path, fail here. The fix is to add one more number to every list, chosen so that the largest sum becomes the smallest distance, and then use a closeness tool.

## Definition

Let $P = \{p_1, \ldots, p_n\} \subset \mathbb{R}^d$ be given in advance, and preprocessed. A **MIPS query** is a vector $q \in \mathbb{R}^d$, and its answer is an index

$$i^* \in \arg\max_{1 \le i \le n} \langle q, p_i \rangle, \qquad \langle q, p \rangle = \sum_{k=1}^{d} q_k p_k.$$

The cost of a query is measured in the real RAM, with $O(d)$ time for one inner product. The scan computes all $n$ inner products in $\Theta(nd)$ time.

Since $\|q - p\|^2 = \|q\|^2 + \|p\|^2 - 2\langle q, p \rangle$ and $\|q\|$ is fixed, MIPS equals Euclidean nearest neighbor search exactly when all $\|p\|$ are equal, and it equals the search for the largest [cosine similarity](/cosine-similarity/) in the same case. In general the three differ, and $\langle p, p \rangle$ need not be the largest of $\langle p, p' \rangle$ over $p' \in P$.

## Variants

- **Top-$k$ MIPS.** Return the $k$ vectors with the largest inner products.
- **$c$-approximate MIPS.** For $0 < c < 1$ and a query with $\max_i \langle q, p_i \rangle > 0$, return some $p$ with $\langle q, p \rangle \ge c \max_i \langle q, p_i \rangle$. The factor is multiplicative, so this variant makes sense only for positive maxima.
- **$(S, cS)$ decision.** Given $S > 0$: if some $\langle q, p \rangle \ge S$, return a $p$ with $\langle q, p \rangle \ge cS$. This is the form solved by LSH.
- **Batch, or bichromatic, MIPS.** Given $Q$ and $P$, find for every $q \in Q$ its best $p$, or the best pair overall. With $|Q| = |P| = n$ and $d \le n$, the matrix product $Q P^{\mathsf{T}}$ gives all $n^2$ inner products in $O(n^{\omega})$ arithmetic operations, $\omega < 2.372$.
- **Unit queries.** In recommendation, the best item does not depend on the norm of the user vector, so one may assume $\|q\| = 1$.

## Examples

Let $P = \{a, b, c, d, e, f\}$ with $a = (1, 0)$, $b = (4, 1)$, $c = (2, 3)$, $d = (0, 2)$, $e = (-1, -1)$, $f = (1, 1)$, and $q = (2, 1)$.

| vector | $p$ | $\langle q, p \rangle$ | $\lVert q - p \rVert$ | in the hull |
|---|---|---|---|---|
| a | (1, 0) | 2 | 1.4142 | no |
| b | (4, 1) | 9 | 2 | yes |
| c | (2, 3) | 7 | 2.2361 | yes |
| d | (0, 2) | 2 | 2.2361 | yes |
| e | (−1, −1) | −3 | 3.6056 | yes |
| f | (1, 1) | 3 | 1 | no |

The MIPS answer is $b$, with inner product 9, but the nearest neighbor of $q$ is $f$, at distance 1. For the query $q = f = (1, 1)$, the inner product of $f$ with itself is 2, while $b$ and $c$ both reach 5: $f$ is not its own best match. Only the hull vertices $b$, $c$, $d$ and $e$ can be answers, since a linear function on a polygon is largest at a vertex.

The reduction to nearest neighbors uses $M = \max_p \|p\| = \|b\| = \sqrt{17}$ and maps each $p$ to $(p, \sqrt{M^2 - \|p\|^2})$, so $b \mapsto (4, 1, 0)$, $c \mapsto (2, 3, 2)$, $a \mapsto (1, 0, 4)$, and $q \mapsto (2, 1, 0)$. The squared distances are $\|q\|^2 + M^2 - 2\langle q, p \rangle = 22 - 2\langle q, p \rangle$: 4 for $b$, 8 for $c$, 18 for $a$ and $d$, 16 for $f$ and 28 for $e$. The nearest transformed vector is $b$, the MIPS answer.

## Known algorithms

- **Scan.** $\Theta(nd)$ time per query, and the baseline for $d$ in the hundreds. Batched queries run as a matrix product.
- **Low dimension.** For $d = 2$, the answer is a vertex of $\mathrm{conv}(P)$ extreme in direction $q$. Build the hull in $O(n \log n)$ time, for example by a [Graham scan](/graham-scan/), and answer each query by binary search on the edge directions in $O(\log n)$ time. For $d = 3$ the Dobkin and Kirkpatrick hierarchy gives $O(\log n)$ queries with $O(n)$ space after $O(n \log n)$ preprocessing.
- **Branch and bound on trees.** Ram and Gray use a [ball tree](/ball-tree/): for a ball of center $c$ and radius $r$, every $p$ in it has $\langle q, p \rangle \le \langle q, c \rangle + r\|q\|$ by the Cauchy-Schwarz inequality, and a ball whose bound is below the best inner product so far is skipped. Cone trees index the queries by direction for batch MIPS. These are exact; their speedup fades as $d$ grows.
- **Reduction plus nearest neighbor index.** The extra coordinate of Bachrach et al. below turns exact MIPS into exact Euclidean nearest neighbor search, so any exact or approximate nearest neighbor index applies: [k-d trees](/kd-tree/) in low dimension, graph indexes such as [HNSW](/hnsw/), or [product quantization](/product-quantization/). Approximation factors do not carry over unchanged; see the next item.
- **Asymmetric LSH.** Shrivastava and Li scale the data so that $\|p\| \le U < 1$, normalize the query, and use different transforms for data and queries, with appended powers $\|p\|^2, \|p\|^4, \ldots, \|p\|^{2^m}$, followed by Euclidean LSH. Neyshabur and Srebro's simple-LSH scales the data into the unit ball, maps $p \mapsto (p, \sqrt{1 - \|p\|^2})$ and a unit query $q \mapsto (q, 0)$, so that the inner product becomes the cosine of the angle, and hashes with [random hyperplanes](/random-hyperplane-lsh/). For the $(S, cS)$ problem it has query time $O(n^{\rho} \log n)$ inner products with $\rho = \log p_1 / \log p_2$, where $p_1 = 1 - \arccos(S)/\pi$ and $p_2 = 1 - \arccos(cS)/\pi$, and succeeds with constant probability.
- **Quantization.** Store the vectors compressed by [product quantization](/product-quantization/), whose code tables give approximate inner products by table lookups; refine the best few exactly. Variants of the quantizer weight the error in the direction of the vector, which matters most for inner products.

## Bounds

**Low dimension.** For fixed $d = 2$, the hull method gives $O(\log n)$ query time, $O(n)$ space and $O(n \log n)$ preprocessing in the real RAM, and it is exact.

**No symmetric LSH over all of $\mathbb{R}^d$.** Shrivastava and Li show that no family of hash functions $h$, used in the same way on data and queries, satisfies the $(S, cS)$ condition of LSH for the inner product on all of $\mathbb{R}^d$. The reason is that $\langle x, x \rangle$ can be smaller than $\langle x, y \rangle$, while $\Pr[h(x) = h(x)] = 1$ is the largest possible collision probability. This is why the methods above are asymmetric.

**Conditional lower bound for the batch version.** Assume the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/). For every $\varepsilon > 0$ there is a $c$ such that no algorithm decides in time $O(n^{2 - \varepsilon})$, for $Q, P \subseteq \{-1, 0, 1\}^d$ with $|Q| = |P| = n$ and $d = c \log n$, whether $\max_{q \in Q, p \in P} \langle q, p \rangle \ge 0$. The reduction below from [orthogonal vectors](/orthogonal-vectors/) and Williams' theorem give it. So an index that answers each query exactly in time $O(n^{1 - \varepsilon})$ after preprocessing in time $O(n^{2 - \varepsilon})$ would refute SETH. The same reduction does not rule out a good multiplicative approximation, since the maximum is 0; hardness of approximation needs other reductions.

## Reductions

**MIPS to nearest neighbor search (Bachrach et al.).** Let $M = \max_{p \in P} \|p\|$. Map $p \mapsto \hat p = (p, \sqrt{M^2 - \|p\|^2}) \in \mathbb{R}^{d+1}$ and $q \mapsto \hat q = (q, 0)$. Then $\|\hat p\| = M$ for every $p$, and

$$\|\hat q - \hat p\|^2 = \|q\|^2 + M^2 - 2\langle q, p \rangle,$$

which is decreasing in $\langle q, p \rangle$. So the nearest $\hat p$ to $\hat q$ is a MIPS answer, and the map costs $O(nd)$ preprocessing and $O(d)$ per query. A $c$-approximate nearest neighbor, $\|\hat q - \hat p\| \le c \min \|\hat q - \hat p'\|$, gives an additive guarantee on the inner product that depends on $\|q\|^2 + M^2$, not a multiplicative one.

**MIPS to angular search (simple-LSH).** After dividing all $p$ by $M$, map $p \mapsto (p, \sqrt{1 - \|p\|^2})$, a unit vector, and a unit query $q \mapsto (q, 0)$. The inner product is unchanged, and it is now the cosine of the angle between two unit vectors. So the $(S, cS)$ problem for MIPS becomes an angular near neighbor problem with angles $\arccos S$ and $\arccos cS$.

**Orthogonal vectors to MIPS.** Given $A, B \subseteq \{0, 1\}^d$, an orthogonal pair exists if and only if $\max_{a \in A, b \in B} \langle -a, b \rangle \ge 0$, since $\langle -a, b \rangle = -a \cdot b \le 0$ with equality exactly for orthogonal pairs. So batch MIPS on $Q = \{-a\}$ and $P = B$ decides orthogonal vectors.

**MIPS from nearest neighbor search.** Conversely, $\arg\min_p \|q - p\|^2 = \arg\max_p (\langle q, p \rangle - \|p\|^2/2)$, and the map $p \mapsto (p, -\|p\|^2/2)$, $q \mapsto (q, 1)$ turns Euclidean nearest neighbor search into MIPS in dimension $d + 1$.

## Applications

- **Recommender systems.** With a matrix factorization of the ratings, the top items for a user are the top-$k$ MIPS answers for the user vector over the item vectors. Bachrach et al. built their transform for the Xbox recommender.
- **Classification with many classes.** A linear classifier picks the class whose weight vector has the largest inner product with the features; with millions of classes this is a MIPS query.
- **Retrieval for language models.** Dense retrieval embeds passages and questions, and scores them by inner product; the best passages are found by approximate MIPS.
- **Attention.** The keys with the largest inner product with a query dominate the softmax of attention, and approximate MIPS selects them in sparse attention methods.

## References
