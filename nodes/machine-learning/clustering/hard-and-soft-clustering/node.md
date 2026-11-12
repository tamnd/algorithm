---
tag: 79ERAP
kind: concept
slug: hard-and-soft-clustering
name: Hard and soft clustering
aliases:
- hard clustering
- soft clustering
area: machine-learning/clustering
level: intro
summary: Hard clustering assigns each point to one cluster; soft clustering gives each point membership degrees.
prereqs: [clustering-problem]
see_also: [clustering-problem, k-means, fuzzy-c-means, gaussian-mixture-model, expectation-maximization, k-means-problem, partitioning-around-medoids, latent-dirichlet-allocation]
sources:
  - paper: doi:10.1080/01969727308546046
    title: J. C. Dunn, A fuzzy relative of the ISODATA process and its use in detecting compact well-separated clusters, Journal of Cybernetics 3(3), 1973, pages 32 to 57
    locator: the fuzzy partition matrix and the fuzzy objective with exponent 2
  - paper: doi:10.1016/0098-3004(84)90020-7
    title: James C. Bezdek, Robert Ehrlich and William Full, FCM, the fuzzy c-means clustering algorithm, Computers and Geosciences 10(2-3), 1984, pages 191 to 203
    locator: the objective with the exponent m, the membership update, and the limit m to 1 that gives hard c-means
  - paper: doi:10.1109/91.227387
    title: Raghu Krishnapuram and James M. Keller, A possibilistic approach to clustering, IEEE Transactions on Fuzzy Systems 1(2), 1993, pages 98 to 110
    locator: memberships without the constraint that they sum to one
  - paper: "Michael Kearns, Yishay Mansour and Andrew Y. Ng, An information-theoretic analysis of hard and soft assignment methods for clustering, Proceedings of the 13th Conference on Uncertainty in Artificial Intelligence (UAI), 1997"
    locator: the comparison of k-means (hard assignments) with EM (soft assignments) for mixtures
  - book: isbn:9780387310732
    title: Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006
    locator: Section 9.2 (responsibilities of a Gaussian mixture) and Section 9.3.2 (relation to K-means, the limit of small variance)
---

A hard clustering puts each point in exactly one cluster: it is a partition of the data, or a label $a(x) \in \{1, \ldots, k\}$ for each point. A soft clustering gives each point a degree of membership in every cluster, a weight $u_{ij} \in [0, 1]$ for point $i$ and cluster $j$, usually with $\sum_j u_{ij} = 1$. A hard clustering is the special soft clustering whose weights are all 0 or 1. [K-means](/k-means/) and [partitioning around medoids](/partitioning-around-medoids/) are hard. [Fuzzy c-means](/fuzzy-c-means/) is soft with fuzzy memberships, and a [Gaussian mixture model](/gaussian-mixture-model/) is soft with posterior probabilities, called responsibilities. K-means is the limit of the Gaussian mixture when the variance goes to zero.

## In plain words

Think of sorting songs into genres. A hard sort puts each song in one box: rock or jazz. A soft sort can say that a song is 70 percent rock and 30 percent jazz.

The soft answer keeps more information. A point that sits between two groups gets split weights, and you can see that it is a borderline case. A point deep inside a group gets a weight close to 1. If you need one box per point at the end, you can always take the box with the largest weight, but you lose the information about how sure the answer was.

## The idea

**Hard clustering.** A hard clustering of $n$ points into $k$ clusters is a matrix $U \in \{0, 1\}^{n \times k}$ with exactly one 1 in each row. The k-means objective in this notation is
$$J(U, c) = \sum_{i=1}^n \sum_{j=1}^k u_{ij}\,\|x_i - c_j\|^2 .$$

**Why soft weights need a change of objective.** Let the weights be real, $u_{ij} \ge 0$ with $\sum_j u_{ij} = 1$, but keep $J$. For fixed centers, $J$ is linear in each row of $U$, and a linear function on the simplex of weights has a minimum at a vertex. So the best soft weights are again hard: the whole weight goes to the nearest center. A soft method must change the objective, and the two common ways follow.

**Fuzzy memberships.** [Fuzzy c-means](/fuzzy-c-means/) (Dunn 1973, Bezdek 1981) raises the weights to a power $m > 1$ and minimizes $\sum_{i,j} u_{ij}^m \|x_i - c_j\|^2$. For fixed centers, with $d_{ij} = \|x_i - c_j\| > 0$, the best weights are
$$u_{ij} = \Big(\sum_{l=1}^k \big(d_{ij}/d_{il}\big)^{2/(m-1)}\Big)^{-1} .$$
As $m \to 1$ the weights tend to 0 or 1, and the method becomes hard k-means; as $m \to \infty$ every weight tends to $1/k$. Possibilistic c-means drops the condition that the weights of a point sum to 1, so that an outlier can have a small weight in every cluster.

**Probabilistic memberships.** A [Gaussian mixture model](/gaussian-mixture-model/) treats the cluster of each point as a hidden random variable. The soft membership is the posterior probability of the cluster given the point, the responsibility
$$r_{ij} = \frac{\pi_j\,\mathcal{N}(x_i \mid \mu_j, \Sigma_j)}{\sum_{l=1}^k \pi_l\,\mathcal{N}(x_i \mid \mu_l, \Sigma_l)} ,$$
and [expectation maximization](/expectation-maximization/) alternates between computing the responsibilities and refitting the weights $\pi_j$, means and covariances.

**K-means as the hard limit.** Take $\Sigma_j = \sigma^2 I$ for all $j$ and fixed weights $\pi_j > 0$. Then
$$r_{ij} = \frac{\pi_j \exp\big(-\|x_i - \mu_j\|^2/(2\sigma^2)\big)}{\sum_l \pi_l \exp\big(-\|x_i - \mu_l\|^2/(2\sigma^2)\big)} .$$
As $\sigma \to 0$, the term with the smallest distance dominates, so $r_{ij} \to 1$ for the nearest mean and $r_{ij} \to 0$ for the others (if there is no tie). The E step becomes the assignment step of k-means, and the M step, which sets each mean to the weighted average of the points, becomes the update step. So Lloyd's algorithm is EM for this mixture in the limit of zero variance.

**From soft to hard, and back.** A soft clustering gives a hard one by the rule $a(x_i) = \arg\max_j u_{ij}$, the most probable cluster. The converse has no single answer: a hard clustering does not say how sure each assignment is.

**Overlap is a different thing.** In an overlapping clustering a point can be a full member of several clusters, and the weights of a point need not sum to 1. In a mixed membership model, such as [latent Dirichlet allocation](/latent-dirichlet-allocation/), each object is a mixture of clusters by its nature, not by uncertainty: a document is partly about sport and partly about money.

## Examples

Take two centers at $0$ and $4$ on the line and the point $x = 1$, so the distances are $1$ and $3$.

| method | weight on the center 0 | weight on the center 4 |
|---|---|---|
| hard (nearest center) | $1$ | $0$ |
| fuzzy c-means, $m = 2$ | $\big(1 + (1/3)^2\big)^{-1} = 9/10$ | $1/10$ |
| Gaussian mixture, equal weights, $\sigma^2 = 4$ | $1/(1 + e^{-1}) \approx 0.731$ | $\approx 0.269$ |
| Gaussian mixture, equal weights, $\sigma^2 = 1$ | $1/(1 + e^{-4}) \approx 0.982$ | $\approx 0.018$ |

For the Gaussian mixture the ratio of the two responsibilities is $\exp\big((3^2 - 1^2)/(2\sigma^2)\big) = e^{4/\sigma^2}$, so a smaller variance gives a harder answer, as the limit above says. At the midpoint $x = 2$ every soft method gives $1/2$ and $1/2$, and a hard method must break a tie.

## Where it is used

- **Hard methods.** The [k-means algorithm](/k-means/), [partitioning around medoids](/partitioning-around-medoids/), [hierarchical clustering](/hierarchical-clustering-problem/), [DBSCAN](/dbscan/) and [spectral clustering](/spectral-clustering/) return partitions, sometimes with a noise label.
- **Soft methods.** [Fuzzy c-means](/fuzzy-c-means/), the [Gaussian mixture model](/gaussian-mixture-model/) fitted by [expectation maximization](/expectation-maximization/), and topic models such as [latent Dirichlet allocation](/latent-dirichlet-allocation/).
- **Uncertainty.** Soft weights show which points are borderline, for example pixels on the boundary of two regions in [image segmentation](/image-segmentation/), or patients between two disease subtypes.
- **Initialization.** A fast hard method often starts a soft one: the result of k-means is the usual starting point of EM for a Gaussian mixture.
- **Evaluation.** Most [cluster validity](/cluster-validity/) indices, such as the [silhouette coefficient](/silhouette-coefficient/), need a hard clustering, so soft results are first turned hard by the largest weight.

## References
