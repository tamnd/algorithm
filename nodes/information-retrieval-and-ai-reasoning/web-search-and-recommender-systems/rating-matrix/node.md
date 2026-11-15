---
tag: YWE719
kind: definition
slug: rating-matrix
name: User-item rating matrix
aliases:
- utility matrix
- user-item matrix
area: information-retrieval-and-ai-reasoning/web-search-and-recommender-systems
level: intro
summary: A sparse matrix with a row per user and a column per item, holding known ratings or interactions and blanks elsewhere.
prereqs: [recommendation-problem]
see_also: [sparse-matrix, compressed-sparse-row, implicit-feedback, matrix-completion, collaborative-filtering, matrix-factorization-recommendation, cosine-similarity, jaccard-similarity]
sources:
  - book: isbn:9783319296579
    title: Charu C. Aggarwal, Recommender Systems, The Textbook, Springer, 2016
    locator: Chapter 2 (the ratings matrix, its sparsity, and the users and items that neighborhood methods compare on it)
  - paper: doi:10.1109/MC.2009.263
    title: Yehuda Koren, Robert Bell and Chris Volinsky, Matrix factorization techniques for recommender systems, IEEE Computer 42(8), 30-37, 2009
    locator: sections Recommender system strategies (explicit and implicit feedback) and A basic matrix factorization model (the sparse rating matrix and the fit to the observed entries only)
  - paper: doi:10.1145/1401890.1401944
    title: Yehuda Koren, Factorization meets the neighborhood, a multifaceted collaborative filtering model, Proceedings of the 14th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD 2008), 426-434
    locator: Section 2.5 (the binary matrix of rated and not rated as implicit feedback)
  - paper: doi:10.1145/1639714.1639717
    title: Benjamin M. Marlin and Richard S. Zemel, Collaborative prediction and ranking with non-random missing data, Proceedings of the Third ACM Conference on Recommender Systems (RecSys 2009)
    locator: the models in which the chance that a rating is missing depends on its value, and their effect on prediction and ranking
---

The user-item rating matrix has one row for each user and one column for each item, and the entry in row $u$ and column $i$ holds what is known about the pair: a rating, a count, a mark that an event took place, or a blank. It is the common input of [collaborative filtering](/collaborative-filtering/) and of the [recommendation problem](/recommendation-problem/). In real data most entries are blank, and a blank means that the value is unknown, not that it is zero.

## Definition

Let $U$ be a set of $m$ users and $I$ a set of $n$ items. A *rating matrix* is a partial function $R : U \times I \to V$, written as an $m \times n$ array whose entry $r_{ui}$ is either a value in $V$ or blank. The set of known pairs is $K = \{ (u, i) : r_{ui} \text{ is not blank} \}$ and $s = |K|$.

- **Explicit data.** $V$ is a rating scale, such as $\{1, 2, 3, 4, 5\}$, and $r_{ui}$ is a rating that $u$ gave to $i$.
- **Implicit data.** $V$ is $\{1\}$ for an event such as a purchase or a click, or the positive numbers for a count or a time. Pairs without an event are often stored as 0, but the 0 then means "no event seen", which is not the same as "disliked".

The *density* of $R$ is $s / (m n)$. The row of $u$ gives $I_u = \{ i : (u, i) \in K \}$, the items that $u$ rated, and the column of $i$ gives $U_i = \{ u : (u, i) \in K \}$, the users who rated $i$. For two users, the *co-rated items* are $I_u \cap I_v$, and for two items, the *common users* are $U_i \cap U_j$; neighborhood methods compare rows or columns on these sets only.

Because $s$ is usually far below $m n$, the matrix is stored as a [sparse matrix](/sparse-matrix/): a list of triples $(u, i, r_{ui})$, or [compressed sparse rows](/compressed-sparse-row/) for fast access to each $I_u$, and the same by columns for each $U_i$. The storage is $O(s + m + n)$, not $O(m n)$.

The blanks are not a random sample of the pairs. Users choose what to rate, and they tend to rate what they expect to like. Marlin and Zemel (2009) study models in which the chance that an entry is blank depends on its value, and show that ignoring this can bias both the predicted ratings and the rankings.

## Examples and non-examples

The toy matrix of this group has four users, four items, $s = 14$ and density $14/16 = 0.875$, with the two blanks $r_{u_1 i_3}$ and $r_{u_4 i_1}$:

| | $i_1$ | $i_2$ | $i_3$ | $i_4$ |
|---|---|---|---|---|
| $u_1$ | 5 | 4 | - | 1 |
| $u_2$ | 4 | 5 | 4 | 2 |
| $u_3$ | 1 | 2 | 2 | 5 |
| $u_4$ | - | 1 | 1 | 4 |

Here $I_{u_1} = \{i_1, i_2, i_4\}$, $U_{i_3} = \{u_2, u_3, u_4\}$, and the co-rated items of $u_1$ and $u_4$ are $\{i_2, i_4\}$.

- **Its binary form.** Replace every known rating by 1 and every blank by 0. The result records only which items each user rated. Koren (2008) uses this matrix as implicit feedback in [SVD++](/svd-plus-plus/), since the fact of rating says something about the user even when the value is not used.
- **The Netflix Prize data.** More than 100 million ratings of about 500,000 customers for more than 17,000 films (Koren, Bell and Volinsky, 2009). From these rounded counts, the density is about 1 percent.
- **Non-example: blanks filled with zeros.** The dense matrix with 0 in every blank of the toy matrix is a different object. A truncated [singular value decomposition](/singular-value-decomposition/) of it fits the zeros as if they were ratings and predicts low values for all unseen items. Methods for rating matrices sum over $K$ only.
- **Non-example: an item feature matrix.** A matrix with a row per item and a column per feature, such as genres or words, describes the items, not the users. It is the input of [content-based filtering](/content-based-filtering/). The term-document matrix of [latent semantic analysis](/latent-semantic-analysis/) has a similar shape, but its zeros are known values: the word does not occur.

## Related definitions

- **The bipartite view.** $R$ is the weighted adjacency matrix of a bipartite graph with users on one side, items on the other, and an edge for each known pair.
- **Low rank.** Latent factor models such as [matrix factorization](/matrix-factorization-recommendation/) assume that the full matrix, with every blank filled by the true value, is close to a matrix of low rank. [Matrix completion](/matrix-completion/) studies when such a matrix can be recovered from the known entries.
- **Implicit feedback.** [Implicit feedback](/implicit-feedback/) is the case of event data, with its own treatment of the blanks.
- **Similarity of rows and columns.** [Cosine similarity](/cosine-similarity/) on centered ratings, and [Jaccard similarity](/jaccard-similarity/) on binary rows, compare two users or two items.

## References
