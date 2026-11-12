---
tag: 1YN38V
kind: concept
slug: elbow-method
name: Elbow method
aliases:
- elbow heuristic
- elbow criterion for the number of clusters
area: machine-learning/clustering
level: intro
summary: Plot the within-cluster sum of squares W_k against k and choose k at the bend. It is a heuristic; the bend has no single definition, and rules such as the chord rule are one choice of many.
prereqs: [k-means-problem]
see_also: [gap-statistic, silhouette-coefficient, calinski-harabasz-index, x-means, g-means, eigengap-heuristic, scree-plot, cluster-validity]
sources:
  - paper: doi:10.1007/BF02289263
    title: "Robert L. Thorndike, Who belongs in the family?, Psychometrika 18(4), 1953, pages 267 to 276"
    locator: the plot of the mean within-group distance against the number of groups, and the search for the point where it stops falling fast
  - paper: doi:10.1109/ICDCSW.2011.20
    title: "Ville Satopaa, Jeannie Albrecht, David Irwin and Barath Raghavan, Finding a Kneedle in a haystack, detecting knee points in system behavior, 31st International Conference on Distributed Computing Systems Workshops, IEEE, 2011, pages 166 to 171"
    locator: the Kneedle method, which scales the curve to the unit square and takes the largest value of the difference curve
  - paper: doi:10.1111/1467-9868.00293
    title: "Robert Tibshirani, Guenther Walther and Trevor Hastie, Estimating the number of clusters in a data set via the gap statistic, Journal of the Royal Statistical Society, Series B 63(2), 2001, pages 411 to 423"
    locator: the motivation of the gap statistic as a formal version of the elbow in log W_k
---

The elbow method chooses the number $k$ of clusters from a plot. For $k = 1, 2, \ldots, K$, it computes the within-cluster sum of squares $W_k$ of a good [k-means](/k-means-problem/) clustering, plots $W_k$ against $k$, and takes the $k$ where the curve bends from a steep fall to a slow fall: the "elbow". The idea goes back to Thorndike in 1953. It is a heuristic. There is no definition of the elbow, different rules pick different values of $k$ on the same curve, and a smooth curve has no elbow at all. This page gives one concrete rule, the farthest point below the chord, and it is only one of many. The [gap statistic](/gap-statistic/) is a formal version of the same idea.

## In plain words

You want to split your data into groups, but you do not know how many groups to use. More groups always make each group tighter, so the total spread inside the groups always goes down. It goes down fast while each new group splits a real group in two. After the real groups are all found, a new group only cuts a tight group in pieces, and the spread goes down slowly.

So you draw the total spread for one group, two groups, three groups and so on. The line drops steeply and then flattens. You choose the number where it turns, like the elbow of a bent arm. When the line bends smoothly, different people see the turn at different places, and the method does not give a clear answer.

## The idea

**Setting.** $X = \{x_1, \ldots, x_n\}$ is a set of $n$ points in $\mathbb{R}^d$ with the squared Euclidean distance, and $k$ is not given. For each $k$, let

$$W_k = \min_{C_1, \ldots, C_k} \sum_{r=1}^{k} \sum_{x \in C_r} \|x - c_r\|^2,$$

the optimal cost of the [k-means problem](/k-means-problem/), with $c_r$ the centroid of $C_r$. In practice $W_k$ is the cost of the best of several runs of [k-means](/k-means/), which is only an upper bound on the optimum.

**The curve always falls.** The optimal $W_k$ never increases with $k$: split any cluster of the best $k$-clustering into two nonempty parts, and the cost does not increase, so $W_{k+1} \le W_k$. Also $W_n = 0$. So the minimum of $W_k$ is no guide; the method looks at the shape of the curve. With heuristic runs of k-means, the curve can go up by a small amount, which is a sign that the runs did not find the optimum.

**A rule for the elbow: the farthest point below the chord.** Take the values $k_1 < \ldots < k_m$ and scale both axes to $[0, 1]$:

$$u_k = \frac{k - k_1}{k_m - k_1}, \qquad v_k = \frac{W_k - W_{k_m}}{W_{k_1} - W_{k_m}}.$$

The curve now runs from $(0, 1)$ to $(1, 0)$, and the chord between the two ends is the line $u + v = 1$. The rule takes the $k$ with the largest value of $1 - u_k - v_k$, which is $\sqrt 2$ times the distance of the point below the chord. Some properties:

- The result does not change when $W$ is multiplied by a positive number or shifted, because of the scaling.
- It is the main step of Kneedle (Satopaa and coauthors, 2011) for a falling convex curve, without the smoothing and the threshold that Kneedle adds for noisy curves.
- It depends on the range $k_1, \ldots, k_m$ that is plotted. This is a real weakness: the elbow is not a property of the data alone.

**Other rules** in use: the largest second difference $W_{k-1} - 2W_k + W_{k+1}$; the first $k$ where the relative drop $(W_k - W_{k+1})/W_k$ falls below a threshold; the share of variance explained, $1 - W_k/W_1$, above a threshold. They can disagree with each other.

**Cost.** The method needs one clustering for each $k$ in the range. For points on a line, the optimal $W_k$ can be found exactly: some optimal clustering uses runs of consecutive sorted points, so dynamic programming over the sorted points gives all $W_1, \ldots, W_K$ in $O(K n^2)$ time. The implementation uses this exact solver, so its curves are the true optimum. In higher dimensions the k-means problem is NP-hard, and each $W_k$ comes from heuristic runs.

## Examples

**A clear elbow.** The values $W_1, \ldots, W_6 = 100, 40, 15, 12, 10, 9$ give $u_k = (k - 1)/5$ and $v_k = (W_k - 9)/91$:

| $k$ | $W_k$ | $u_k$ | $v_k$ | $1 - u_k - v_k$ |
|---|---|---|---|---|
| 1 | 100 | 0 | 1 | 0 |
| 2 | 40 | 0.2 | 0.341 | $209/455 \approx 0.459$ |
| 3 | 15 | 0.4 | 0.066 | $243/455 \approx 0.534$ |
| 4 | 12 | 0.6 | 0.033 | $167/455 \approx 0.367$ |
| 5 | 10 | 0.8 | 0.011 | $86/455 \approx 0.189$ |
| 6 | 9 | 1 | 0 | 0 |

The rule picks $k = 3$. The values $7 W_k + 3$ give the same pick.

**Three groups on a line.** Take the 12 points $0, 1, 2, 3$, then $20, 21, 22, 23$, then $40, 41, 42, 43$. The exact values for $k = 1, \ldots, 8$ are

$$W_k = 3215,\ 815,\ 15,\ 11,\ 7,\ 3,\ 5/2,\ 2.$$

From $k = 2$ to $k = 3$ the cost falls from 815 to 15, and after that each new cluster saves only about 4. The chord rule picks $k = 3$, the true number of groups.

**No elbow.** For the smooth curve $W_k = 1/k$, the chord rule gives an answer that depends only on how far the plot goes:

| largest $k$ plotted | 4 | 6 | 10 | 20 |
|---|---|---|---|---|
| chosen $k$ | 2 | 2 | 3 | 4 |

Data with no clusters, such as points from a uniform distribution, give such smooth curves. The elbow method always returns some $k \ge 2$, so it cannot say that the data have no clusters. The [gap statistic](/gap-statistic/) compares the curve with the curve for data without clusters, and it can return $k = 1$.

## Where it is used

- Choosing $k$ for [k-means](/k-means/) and [k-means++](/k-means-plus-plus/) in data analysis, often together with the [silhouette coefficient](/silhouette-coefficient/) or the [Calinski-Harabasz index](/calinski-harabasz-index/).
- The same reading of a bend is used for the [scree plot](/scree-plot/) of [principal component analysis](/principal-component-analysis/), where the curve is the eigenvalue or the [explained variance](/explained-variance/) against the number of components.
- In [spectral clustering](/spectral-clustering/), the [eigengap heuristic](/eigengap-heuristic/) looks for a jump in the eigenvalues, which is a related idea.
- Knee detection in general, for example the number of neighbors or the radius for [DBSCAN](/dbscan/), and other [hyperparameters](/hyperparameter-tuning/) where the gain of a larger value flattens out. Kneedle was designed for such curves in computer systems.
- Methods that choose $k$ by a statistical test, such as [X-means](/x-means/) and [G-means](/g-means/), are alternatives when a plot is not enough.

## References
