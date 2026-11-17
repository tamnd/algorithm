---
title: Topological overlap lies in the unit interval, and average linkage on it gives a monotone tree that a static cut splits into modules
proves: [correctness]
status: full
---

We prove what the steps of the pipeline compute. The soft-threshold adjacency has entries in $[0, 1]$ (Lemma 1). The topological overlap is symmetric and lies in $[0, 1]$ (Lemma 2). The Lance-Williams update computes average linkage exactly (Lemma 3), the merge heights never decrease (Lemma 4), so a cut at a fixed height gives the clusters of the tree at that height (Lemma 5). Power iteration returns the first eigenvector of $X^\top X$, which is the module eigengene, when the top eigenvalue is simple (Lemma 6). That modules found this way are biological units is a modelling claim, and the choice of the power $\beta$ by a scale-free fit is a heuristic. Neither is proved here.

**Setting.** The matrix $X$ holds $n$ genes and $m$ samples. Line L1 computes the Pearson correlations $r_{ij}$. Line L2 sets $a_{ij} = |r_{ij}|^\beta$ (unsigned) or $a_{ij} = ((1 + r_{ij})/2)^\beta$ (signed) for $i \ne j$, with $\beta > 0$, and $a_{ii} = 1$. Line L3 computes the connectivity $k_i = \sum_{u \ne i}a_{iu}$. Line L4 computes, for $i \ne j$,
$$\mathrm{TOM}_{ij} = \frac{l_{ij} + a_{ij}}{\min(k_i, k_j) + 1 - a_{ij}}, \qquad l_{ij} = \sum_{u \ne i, j}a_{iu}a_{uj},$$
and $\mathrm{TOM}_{ii} = 1$. Line L5 sets the distance $d_{ij} = 1 - \mathrm{TOM}_{ij}$.

**Lemma 1 (adjacency).** $a$ is symmetric and $0 \le a_{ij} \le 1$.

*Proof.* $r_{ij} = r_{ji}$, and $-1 \le r_{ij} \le 1$ by the Cauchy-Schwarz inequality. So $|r_{ij}|$ and $(1 + r_{ij})/2$ lie in $[0, 1]$, and so do their powers with $\beta > 0$. $\square$

**Lemma 2 (topological overlap).** For any symmetric $a$ with entries in $[0, 1]$ and $a_{ii} = 1$, $\mathrm{TOM}$ is symmetric and $0 \le \mathrm{TOM}_{ij} \le 1$. Also $\mathrm{TOM}_{ij} = 0$ exactly when $a_{ij} = 0$ and no third gene is joined to both $i$ and $j$.

*Proof.* Symmetry holds because $l_{ij}$, $a_{ij}$ and $\min(k_i, k_j)$ are symmetric in $i$ and $j$. Since $a_{uj} \le 1$, $l_{ij} \le \sum_{u \ne i, j}a_{iu} = k_i - a_{ij}$, and in the same way $l_{ij} \le k_j - a_{ij}$. So $l_{ij} + a_{ij} \le \min(k_i, k_j)$. The denominator is $\min(k_i, k_j) + 1 - a_{ij} \ge \min(k_i, k_j)$, since $a_{ij} \le 1$. It is positive: if $a_{ij} < 1$ it is greater than $\min(k_i, k_j) \ge 0$, and if $a_{ij} = 1$ it is $\min(k_i, k_j) \ge a_{ij} = 1$. So $0 \le l_{ij} + a_{ij} \le \text{denominator}$, which gives $0 \le \mathrm{TOM}_{ij} \le 1$. The numerator is a sum of nonnegative terms, so it is 0 exactly when $a_{ij} = 0$ and every product $a_{iu}a_{uj}$ is 0. $\square$

So $d$ is a symmetric dissimilarity with entries in $[0, 1]$ and a zero diagonal. It need not satisfy the triangle inequality, and the steps below do not need it.

**Lemma 3 (the Lance-Williams update is average linkage).** At every step of average_linkage, the stored distance between two current clusters $P$ and $Q$ equals $D(P, Q) = \frac{1}{|P||Q|}\sum_{x \in P, y \in Q}d_{xy}$.

*Proof.* By induction on the steps. At the start every cluster is one gene and the stored distance is $d_{xy}$. Suppose the claim holds before clusters $A$ and $B$ merge. For another cluster $C$,
$$D(C, A \cup B) = \frac{1}{|C|(|A| + |B|)}\left(\sum_{x \in C, y \in A}d_{xy} + \sum_{x \in C, y \in B}d_{xy}\right) = \frac{|A|D(C, A) + |B|D(C, B)}{|A| + |B|},$$
which is the value the code stores. The distances between clusters other than $A$ and $B$ do not change. $\square$

**Lemma 4 (monotone heights).** The heights $h_1, h_2, \dots, h_{n-1}$ of the merges satisfy $h_1 \le h_2 \le \dots \le h_{n-1}$.

*Proof.* At step $t$ the code merges a pair $A, B$ with the smallest current distance $h_t$, so every current distance is at least $h_t$. After the merge, the new distances $D(C, A \cup B)$ are weighted means of $D(C, A) \ge h_t$ and $D(C, B) \ge h_t$, so they are at least $h_t$ as well. The other distances do not change. So every distance after step $t$ is at least $h_t$, and $h_{t+1} \ge h_t$. $\square$

This is the reducibility property of average linkage. It fails for centroid and median linkage, where a later merge can be lower than an earlier one.

**Lemma 5 (the static cut).** For a height $H$, the labels of cut_tree put two genes in the same module exactly when they are in the same cluster after the merges with $h_t \le H$, and by Lemma 4 these merges are the first $T$ merges for some $T$. Clusters with fewer than min_size genes get the label 0.

*Proof.* By Lemma 4, the set $\{t : h_t \le H\}$ is an initial segment $\{1, \dots, T\}$. For each kept merge, the code joins all its members in a union-find structure. The clusters after $T$ merges are exactly the members of the clusters that these merges create, together with the genes not yet merged, so the union-find classes are these clusters. The code then numbers the classes with at least min_size genes by decreasing size and gives 0 to the rest. $\square$

This static cut is not the Dynamic Tree Cut of Langfelder, Zhang and Horvath (2008), which the WGCNA package uses by default. A dynamic cut can split one branch at different heights, so its modules need not be clusters of one level of the tree.

**Lemma 6 (the eigengene).** Let $Z$ be the module matrix with each gene standardized to mean 0 and sample standard deviation 1. Let $C = Z^\top Z$, a symmetric positive semidefinite $m \times m$ matrix with eigenvalues $\lambda_1 \ge \lambda_2 \ge \dots \ge 0$ and unit eigenvectors $e_1, \dots, e_m$. If $\lambda_1 > \lambda_2$ and the start vector $v_0$ has $e_1^\top v_0 \ne 0$, the iterates $v_t = Cv_{t-1}/\|Cv_{t-1}\|$ converge to $\pm e_1$, and $e_1$ is the first right singular vector of $Z$, the direction $v$ with $\|v\| = 1$ that maximizes $\|Zv\|^2$.

*Proof.* Write $v_0 = \sum_i c_ie_i$ with $c_1 \ne 0$. Then $C^tv_0 = \sum_i c_i\lambda_i^te_i$, and $v_t$ is this vector divided by its length. The terms with $i \ge 2$ have size at most $|c_i|(\lambda_2/\lambda_1)^t$ relative to the first term, which tends to 0. So $v_t \to \operatorname{sign}(c_1)e_1$, since every $\lambda_i \ge 0$ and no sign changes occur. For a unit vector $v$, $\|Zv\|^2 = v^\top Cv \le \lambda_1$, with equality at $v = e_1$. This is the first right singular vector by the definition of the [singular value decomposition](/singular-value-decomposition/). $\square$

The error after $t$ steps is $O((\lambda_2/\lambda_1)^t)$, so the iteration is slow when the module has two strong directions. The code fixes the sign of the result so that it has a nonnegative inner product with the mean standardized gene of the module, as WGCNA does, so that the eigengene goes up when most module genes go up. The start vector $(1, 1.01, 1.02, \dots)$ is fixed. It is orthogonal to $e_1$ only for special data, and then the code returns another eigenvector; the tests do not hit this case.

**The scale-free fit.** scale_free_fit bins the connectivities, fits a least-squares line to $\log_{10}p(k)$ against $\log_{10}k$, and returns $R^2$ and the slope. WGCNA picks the smallest $\beta$ whose $R^2$ passes a threshold such as 0.8. This rule is a heuristic of Zhang and Horvath (2005). It is not a test, and coexpression networks need not be scale-free.

**What the tests check.** The test file checks the Pearson correlation, both adjacencies, the page example, the TOM against a brute force and against the bounds of Lemma 2 with its two extreme cases, average linkage against a brute force that recomputes $D(P, Q)$ from its definition, the order of Lemma 4, the cut labels of Lemma 5, the eigengene against a rank one module and against the Rayleigh quotient bound of Lemma 6, and the scale-free fit against a direct regression. The recovery of planted modules is a measurement.

**Complexity.** With $n$ genes and $m$ samples, the correlations take $\Theta(n^2m)$ time and the TOM takes $\Theta(n^3)$ time as written (a matrix product does the same work). The average linkage code scans all current pairs at each of the $n - 1$ steps, which is $O(n^3)$ time; a nearest-neighbour chain makes it $O(n^2)$. The cut takes $O(n^2)$ time in the worst case because it reads the member lists. For a module of $g$ genes, the eigengene takes $O(gm^2)$ to form $C$ and $O(m^2)$ per iteration. The extra space is $\Theta(n^2)$.
