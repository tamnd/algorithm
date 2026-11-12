---
tag: 457GJ1
kind: problem
slug: biclustering-problem
name: Biclustering problem
aliases:
- co-clustering
- two-way clustering
- biclustering of a data matrix
area: machine-learning/clustering
level: advanced
summary: "Find submatrices of a data matrix (a subset of rows with a subset of columns) whose entries follow a pattern, such as a low mean squared residue. NP-hard in its main forms."
prereqs: [clustering-problem, bipartite-graph, np-hard]
see_also: [subspace-clustering-problem, clique-subspace-clustering, maximum-clique, konig-theorem, bipartite-maximum-independent-set, singular-value-decomposition, normalized-cut, nonnegative-matrix-factorization]
sources:
  - paper: "Yizong Cheng and George M. Church, Biclustering of expression data, Proceedings of the Eighth International Conference on Intelligent Systems for Molecular Biology (ISMB 2000), AAAI Press, 2000, pages 93 to 103"
    locator: "the mean squared residue H(I, J) (equation 2), delta-biclusters, Theorem 1 (finding the largest square delta-bicluster is NP-hard, by reduction from balanced complete bipartite subgraph), and Algorithms 1 to 4 (single node deletion, multiple node deletion, node addition, and masking of found biclusters with random values)"
  - paper: doi:10.1109/TCBB.2004.2
    title: "Sara C. Madeira and Arlindo L. Oliveira, Biclustering algorithms for biological data analysis: a survey, IEEE/ACM Transactions on Computational Biology and Bioinformatics 1(1), 2004, pages 24 to 45"
    locator: "the definitions of bicluster and biclustering, the four classes of bicluster types (constant values, constant values on rows or columns, coherent values, coherent evolutions), the bicluster structures, and the classes of algorithms"
  - paper: "John A. Hartigan, Direct clustering of a data matrix, Journal of the American Statistical Association 67(337), 1972, pages 123 to 129"
    locator: the first block clustering of the rows and columns of a data matrix at the same time, with constant-value blocks
  - paper: "René Peeters, The maximum edge biclique problem is NP-complete, Discrete Applied Mathematics 131(3), 2003, pages 651 to 654"
    locator: NP-completeness of the biclique with the most edges in a bipartite graph
  - book: "Michael R. Garey and David S. Johnson, Computers and Intractability: A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979, ISBN 0-7167-1045-5"
    locator: "problem GT24, balanced complete bipartite subgraph"
---

The biclustering problem asks for submatrices of an $n \times m$ data matrix $A$, each made of a subset $I$ of the rows and a subset $J$ of the columns, whose entries follow a simple pattern. An ordinary clustering groups the rows using all columns. A bicluster groups some rows using only some columns, and different biclusters may use different columns and may overlap. The standard measure of fit is the *mean squared residue* $H(I, J)$ of Cheng and Church (2000), which is 0 exactly when the submatrix is additive, $a_{ij} = \mu + \alpha_i + \beta_j$. Finding the largest submatrix with $H(I, J) \le \delta$ is NP-hard (Cheng and Church), and so is the binary case of finding the all-ones submatrix with the most entries (Peeters 2003), a maximum edge biclique. The practical methods are heuristics, such as greedy node deletion. Madeira and Oliveira (2004) classify the bicluster types, the structures and the algorithms.

## In plain words

Picture a big table with genes as rows and lab experiments as columns. Each cell holds how active a gene was in an experiment. A normal clustering puts genes in groups that behave alike in all the experiments.

But often a set of genes moves together in only a few experiments, and does unrelated things in the others. Biclustering looks for such blocks: some rows and some columns, picked together, so that inside the block the numbers follow a clear pattern, for example "each row is the same curve, moved up or down".

The difficulty is that there are very many ways to choose rows and columns. Finding the largest good block is hard in general, so people use fast methods that are good in practice but can miss the best block.

## Definition

Let $A = (a_{ij})$ be an $n \times m$ real matrix with row set $X$ and column set $Y$. A *bicluster* is a pair $(I, J)$ with $\emptyset \ne I \subseteq X$ and $\emptyset \ne J \subseteq Y$; it stands for the submatrix $A_{IJ}$. Write the row means, column means and overall mean of $A_{IJ}$ as

$$a_{iJ} = \frac{1}{|J|}\sum_{j \in J} a_{ij}, \qquad a_{Ij} = \frac{1}{|I|}\sum_{i \in I} a_{ij}, \qquad a_{IJ} = \frac{1}{|I||J|}\sum_{i \in I, j \in J} a_{ij}.$$

The *residue* of an entry is $r_{ij} = a_{ij} - a_{iJ} - a_{Ij} + a_{IJ}$, and the *mean squared residue* is

$$H(I, J) = \frac{1}{|I||J|}\sum_{i \in I, j \in J} r_{ij}^2.$$

$H(I, J) = 0$ iff $a_{ij} = a_{iJ} + a_{Ij} - a_{IJ}$ for all $i \in I, j \in J$, that is, iff $A_{IJ}$ is additive. A *$\delta$-bicluster* is a bicluster with $H(I, J) \le \delta$.

**The problem (Cheng and Church form).** Given $A$ and $\delta \ge 0$, find a $\delta$-bicluster of the largest size. Size is usually the area $|I| \cdot |J|$; Cheng and Church also use $|I| + |J|$, and prove hardness for square biclusters.

**The general problem (Madeira and Oliveira).** Given $A$ and a merit function on biclusters, find one bicluster or a set of biclusters $(I_1, J_1), \ldots, (I_k, J_k)$ that score well, where the structure of the set (one block, a partition of both rows and columns, or arbitrary overlapping blocks) is part of the problem statement.

Some facts about $H$:

- **Invariance.** Adding a constant $c_i$ to row $i$ and $d_j$ to column $j$ does not change any residue, so it does not change $H$.
- **Scaling.** Multiplying all entries by $c$ multiplies $H$ by $c^2$. So $\delta$ depends on the units of the data.
- **Random data.** If the entries are independent with variance $\sigma^2$, then $\mathbb{E}[H(I, J)] = \sigma^2 \frac{(|I| - 1)(|J| - 1)}{|I||J|}$, because the residues are the projection of the entries on a subspace of dimension $(|I| - 1)(|J| - 1)$. For entries uniform on $[a, b]$ it tends to $(b - a)^2/12$, the value that Cheng and Church use to calibrate $\delta$.

## Variants

- **Bicluster types (Madeira and Oliveira).** *Constant values* ($a_{ij} = \mu$); *constant values on rows* ($a_{ij} = \mu + \alpha_i$) or on columns; *coherent values*, additive ($\mu + \alpha_i + \beta_j$, exactly the $H = 0$ case) or multiplicative ($\mu \alpha_i \beta_j$, additive after taking logarithms of positive data); and *coherent evolutions*, where only the order or the sign of changes matters, as in order-preserving submatrices.
- **Structures.** One bicluster; a checkerboard, where the rows and the columns are each partitioned and every block is a bicluster (often called *co-clustering*); exclusive rows or exclusive columns; nested (tree) structures; and arbitrary overlapping biclusters.
- **Binary matrices.** For a 0/1 matrix, a constant all-ones bicluster is a biclique of the [bipartite graph](/bipartite-graph/) with an edge $ij$ for each 1. The size can be the number of vertices $|I| + |J|$, the number of edges $|I||J|$, or balanced ($|I| = |J| = k$).
- **Probabilistic models.** The plaid model (Lazzeroni and Owen) writes $A$ as a sum of overlapping additive layers. Co-clustering by information theory (Dhillon, Mallela and Modha) partitions the rows and the columns to keep the most mutual information of the joint distribution.

## Examples

**An additive bicluster.** With row effects $\alpha = (0, 2, 5)$ and column effects $\beta = (1, 3, 4, 8)$,

$$A = \begin{pmatrix} 1 & 3 & 4 & 8 \\ 3 & 5 & 6 & 10 \\ 6 & 8 & 9 & 13 \end{pmatrix}, \qquad H = 0.$$

The map $x \mapsto 3x + 7$ keeps $H = 0$. On the non-additive matrix $\begin{pmatrix} 1 & 2 & 3 \\ 2 & 4 & 6 \\ 4 & 8 & 13 \end{pmatrix}$, $H = 118/81$, and after $x \mapsto 3x + 7$, $H = 118/9$, which is $9$ times larger.

**Random data.** Averaging $H$ over all 0/1 matrices of a given shape ($\sigma^2 = 1/4$) gives exactly $1/16$ for $2 \times 2$, $1/12$ for $2 \times 3$ and $1/9$ for $3 \times 3$, which matches $\frac{1}{4} \cdot \frac{(|I| - 1)(|J| - 1)}{|I||J|}$. A script enumerated the 16, 64 and 512 matrices with exact fractions.

**Greedy deletion that works.** Cheng and Church's single node deletion removes, while $H > \delta$, the row or the column with the largest mean of $r_{ij}^2$ along it. Take $\delta = 0$ and the additive matrix above with a noisy row and a noisy column added:

$$M = \begin{pmatrix} 1 & 3 & 4 & 8 & 0 \\ 3 & 5 & 6 & 10 & 9 \\ 6 & 8 & 9 & 13 & 2 \\ 9 & 0 & 7 & 1 & 5 \end{pmatrix}.$$

At first $H = 184/25$. The largest row score is $394/25$ (row 3) and the largest column score $4931/400$ (column 3), so row 3 goes. Then $H = 632/225$, and column 4 has score $2528/225$, the largest, so it goes. Now $H = 0$ on rows $\{0, 1, 2\}$ and columns $\{0, 1, 2, 3\}$, and a brute force over all biclusters confirms that no $0$-bicluster has a larger area than this $3 \times 4$ block.

**Greedy deletion that fails.** For

$$G = \begin{pmatrix} 3 & 1 & 1 & 1 \\ 3 & 2 & 1 & 1 \\ 2 & 0 & 2 & 0 \\ 3 & 0 & 1 & 1 \end{pmatrix},$$

$H = 15/64$. The rows $\{0, 1, 3\}$ with the columns $\{0, 2, 3\}$ are all equal to $(3, 1, 1)$, a $3 \times 3$ block with $H = 0$, and the brute force finds no larger one. But the first deletion takes column 2 (score $29/64$, against $27/64$ for the best row), which this block needs. Greedy deletion stops at a $2 \times 3$ block with $H = 0$ (rows $\{0, 2\}$, columns $\{0, 1, 3\}$), area 6 instead of 9.

## Known algorithms

- **Direct clustering (Hartigan 1972).** Splits the matrix into blocks of near-constant values, row and column splits at once.
- **Cheng and Church (2000).** Single node deletion ($O(nm)$ per step to update the scores), multiple node deletion (remove all rows or columns with score above $\alpha H$, for speed on large matrices), and node addition (add back the rows and columns whose score is at most $H$, and also rows that fit after a sign change). To find several biclusters, they replace each found block with random values and repeat, which loses overlaps and adds noise.
- **Spectral co-clustering.** Dhillon (2001) partitions the bipartite graph of rows and columns by the [normalized cut](/normalized-cut/), using the [singular vectors](/singular-value-decomposition/) of the scaled matrix $D_1^{-1/2} A D_2^{-1/2}$. Kluger and others (2003) find checkerboards by a similar spectral method.
- **Enumeration.** For binary data, exact algorithms list all maximal all-ones submatrices, such as Bimax (Prelić and others, 2006); their cost depends on the output size.
- **Model-based and order-based.** The plaid model (fitted layer by layer), SAMBA (heavy subgraphs of a bipartite graph, Tanay, Sharan and Shamir), and OPSM (order-preserving submatrices, Ben-Dor, Chor, Karp and Yakhini).
- **Factorization.** [Nonnegative matrix factorization](/nonnegative-matrix-factorization/) with sparse factors gives soft biclusters: the support of each rank-one term.

## Bounds

- **Search space.** There are $(2^n - 1)(2^m - 1)$ biclusters, so brute force is exponential in both dimensions.
- **Hardness.** Finding the largest square $\delta$-bicluster is NP-hard (Cheng and Church, Theorem 1, from the balanced complete bipartite subgraph problem). The maximum edge biclique, that is, the all-ones submatrix of a 0/1 matrix with the most entries, is NP-complete (Peeters 2003). The balanced biclique is NP-complete (Garey and Johnson, GT24).
- **A polynomial case.** The biclique with the most vertices $|I| + |J|$ is easy: $(I, J)$ is a biclique of $G$ iff $I \cup J$ is an independent set of the bipartite complement (the pairs of $X \times Y$ that are not edges). In a bipartite graph the [maximum independent set](/bipartite-maximum-independent-set/) has size $|V|$ minus a maximum matching, by [König's theorem](/konig-theorem/).
- **Output size.** The graph $K_{k,k}$ minus a perfect matching has $2^k - 2$ maximal bicliques: one for each non-empty proper subset $S$ of the indices, with rows $S$ and columns the complement of $S$. So listing all maximal biclusters can take exponential time even for small inputs.

## Reductions

- **Binary biclustering and bicliques.** A 0/1 matrix is the biadjacency matrix of a bipartite graph, and constant all-ones biclusters are exactly its bicliques. So any hardness for bicliques carries over.
- **To cliques.** Make $X$ and $Y$ each into a clique and keep the edges of $A$ between them. Then $I \cup J$ is a clique iff $(I, J)$ is a biclique (with $I, J$ non-empty), so a [maximum clique](/maximum-clique/) algorithm finds a maximum vertex biclique; this direction is useful for solvers, not for hardness.
- **Checkerboard co-clustering as graph partitioning.** Partitioning rows and columns together into $k$ groups is a cut problem on the bipartite graph, solved by spectral relaxation as above.
- **Subspace clustering.** A bicluster is a set of objects (rows) that agree in a subset of attributes (columns). With the rows as points, an axis-parallel [subspace cluster](/subspace-clustering-problem/) is a bicluster with a density or distance criterion in place of $H$; Kriegel, Kröger and Zimek call the biclustering view "pattern-based clustering".

## Applications

- **Gene expression.** Genes by conditions: find sets of genes co-regulated in some conditions (Cheng and Church used yeast and human lymphoma data).
- **Text.** Documents by words: co-cluster documents with the words that define their topics.
- **Recommendation and market baskets.** Users by items: find groups of users who like the same group of items.

## References
