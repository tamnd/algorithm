---
tag: A919QT
kind: algorithm
slug: latent-semantic-analysis
name: Latent semantic analysis
aliases:
- latent semantic indexing
- LSI
- LSA
area: machine-learning/dimensionality-reduction
level: core
summary: "Replace a weighted term-document matrix by its rank-k truncated SVD. Documents and folded-in queries become k-dimensional vectors that are compared by cosine similarity."
model: real-ram
complexity:
  vars: {m: the number of terms, n: the number of documents, k: the number of retained dimensions, S: the number of Jacobi sweeps, N: the number of nonzero entries of A}
  time: {worst: "Θ(m n^2 + S n^3)"}
  space: {extra: "Θ(n^2 + (m + n) k)"}
properties: {deterministic: true, online: false, exact: true, recursive: false, supervised: false, linear: true}
history:
  year: 1988
  people: [Scott Deerwester, Susan T. Dumais, George W. Furnas, Thomas K. Landauer, Richard Harshman]
  note: Furnas, Deerwester, Dumais, Landauer, Harshman and colleagues at Bellcore presented SVD-based retrieval at SIGIR 1988. The 1990 JASIS paper by Deerwester and colleagues is the standard reference.
prereqs: [singular-value-decomposition, cosine-similarity]
see_also: [principal-component-analysis, nonnegative-matrix-factorization, latent-dirichlet-allocation, randomized-pca, golub-kahan-svd-algorithm, lanczos-algorithm, inverted-file-index, random-projection]
sources:
  - paper: "doi:10.1002/(SICI)1097-4571(199009)41:6<391::AID-ASI1>3.0.CO;2-9"
    title: Scott Deerwester, Susan T. Dumais, George W. Furnas, Thomas K. Landauer and Richard Harshman, Indexing by latent semantic analysis, Journal of the American Society for Information Science 41(6), 1990
    locator: pp. 391 to 407 (the model, folding in of queries, the nine-title example with k = 2)
  - paper: "George W. Furnas, Scott Deerwester, Susan T. Dumais, Thomas K. Landauer, Richard A. Harshman, Lynn A. Streeter and Karen E. Lochbaum, Information retrieval using a singular value decomposition model of latent semantic structure, Proceedings of the 11th ACM SIGIR Conference, 1988"
    locator: pp. 465 to 480 (the first published description of the method)
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schütze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 18 (Section 18.3 low-rank approximations, Section 18.4 latent semantic indexing)
  - paper: doi:10.1137/1037127
    title: Michael W. Berry, Susan T. Dumais and Gavin W. O'Brien, Using linear algebra for intelligent information retrieval, SIAM Review 37(4), 1995
    locator: pp. 573 to 595 (term weighting, folding in, SVD updating)
  - paper: doi:10.1007/BF02288367
    title: Carl Eckart and Gale Young, The approximation of one matrix by another of lower rank, Psychometrika 1(3), 1936
    locator: pp. 211 to 218 (the truncated SVD is the best low-rank approximation)
  - paper: doi:10.1037/0033-295X.104.2.211
    title: Thomas K. Landauer and Susan T. Dumais, A solution to Plato's problem, the latent semantic analysis theory of acquisition, induction, and representation of knowledge, Psychological Review 104(2), 1997
    locator: pp. 211 to 240 (LSA as a model of word meaning, the synonym test)
  - paper: doi:10.1145/312624.312649
    title: Thomas Hofmann, Probabilistic latent semantic indexing, Proceedings of the 22nd ACM SIGIR Conference, 1999
    locator: pp. 50 to 57 (the probabilistic model that replaces the SVD)
  - paper: doi:10.1137/090771806
    title: Nathan Halko, Per-Gunnar Martinsson and Joel A. Tropp, Finding structure with randomness, probabilistic algorithms for constructing approximate matrix decompositions, SIAM Review 53(2), 2011
    locator: pp. 217 to 288 (randomized truncated SVD for large sparse matrices)
---

Latent semantic analysis (LSA), called latent semantic indexing (LSI) in information retrieval, replaces a weighted term-document matrix $A$ by its rank-$k$ truncated [singular value decomposition](/singular-value-decomposition/) $A_k = U_k \Sigma_k V_k^{\top}$. Each document becomes a $k$-dimensional vector, each term becomes a $k$-dimensional vector, and a query is folded into the same space by $\hat q = \Sigma_k^{-1} U_k^{\top} q$. Documents are then ranked by [cosine similarity](/cosine-similarity/) in that space. Because $A_k$ is the best rank-$k$ approximation of $A$, the method keeps the strongest patterns of word co-occurrence and drops the rest. A document can then match a query with which it shares no word. LSA was introduced by Deerwester, Dumais, Furnas, Landauer and Harshman, with the standard paper in 1990.

## In plain words

Word matching misses relevant documents that use different words for the same idea, such as "car" and "automobile". It also returns documents that use a query word in another sense.

LSA starts from a table that counts how often each word occurs in each document. It then keeps only the few strongest patterns in that table, for example "these words tend to occur together". Every document and every word gets a short list of numbers that tells how much of each pattern it has.

Two words that occur with the same neighbours get similar lists, even if they never occur in the same document. A query is turned into a list of the same kind, and documents whose lists point in nearly the same direction are returned first. So a document can be found without any of the query words.

## The problem

Given $n$ documents over a vocabulary of $m$ terms, build the $m \times n$ matrix $A$ whose entry $a_{i j}$ is a weight of term $i$ in document $j$. The weight is a raw count, or tf-idf $a_{i j} = \mathrm{tf}_{i j} \log(n / \mathrm{df}_i)$, or the log-entropy weight used in much of the LSI literature. Choose $k \ll \min(m, n)$. The reduction step is the low-rank approximation problem
$$ \min_{\operatorname{rank}(B) \le k} \lVert A - B \rVert_F , $$
whose solution is $A_k$. The retrieval step is: given a query $q \in \mathbb{R}^m$, weighted like a document, rank the documents by their similarity to $q$ in the space spanned by $u_1, \ldots, u_k$.

## The algorithm

```pseudo id=main
LSA(D, k, q)
L1  A ← weighted term-document matrix of the documents D        ▷ m × n
L2  (Σ_k, U_k, V_k) ← rank-k truncated SVD of A
L3  q̂ ← Σ_k⁻¹ U_kᵀ q                                            ▷ fold in the query
L4  scale: document j ↦ Σ_k v_j,  query ↦ Σ_k q̂
L5  score_j ← cosine(Σ_k v_j, Σ_k q̂) for j = 1, …, n
L6  return the documents sorted by decreasing score
```

Here $v_j$ is row $j$ of $V_k$, written as a column. Line L4 is a choice: Deerwester and colleagues compare documents through $V_k \Sigma_k$, and some systems compare the unscaled rows of $V_k$. Lines L1 and L2 run once for a collection. Lines L3 to L6 run once per query. A new document is folded in by line L3 in the same way as a query, and its vector is appended to $V_k$.

## Example

The nine titles of Deerwester and colleagues, five about human-computer interaction ($c_1$ to $c_5$) and four about graph theory ($m_1$ to $m_4$), give a $12 \times 9$ count matrix over these index terms:

| document | index terms |
| --- | --- |
| $c_1$ | human, interface, computer |
| $c_2$ | computer, user, system, response, time, survey |
| $c_3$ | interface, user, system, EPS |
| $c_4$ | human, system (twice), EPS |
| $c_5$ | user, response, time |
| $m_1$ | trees |
| $m_2$ | trees, graph |
| $m_3$ | trees, graph, minors |
| $m_4$ | graph, minors, survey |

The singular values of $A$ are 3.34, 2.54, 2.35, 1.64, 1.50, 1.31, 0.85, 0.56 and 0.36, and their squares add up to $\lVert A \rVert_F^2 = 31$. With $k = 2$ the squared error is $\lVert A - A_2 \rVert_F^2 = 31 - 3.34^2 - 2.54^2 \approx 13.38$, the sum of the seven discarded squares. The rows of $V_2$ are

| | $c_1$ | $c_2$ | $c_3$ | $c_4$ | $c_5$ | $m_1$ | $m_2$ | $m_3$ | $m_4$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| $v_{j 1}$ | 0.197 | 0.606 | 0.463 | 0.542 | 0.279 | 0.004 | 0.015 | 0.024 | 0.082 |
| $v_{j 2}$ | −0.056 | 0.166 | −0.127 | −0.232 | 0.107 | 0.193 | 0.438 | 0.615 | 0.530 |

The first dimension measures the computer topic and the second the graph topic. For the query "human computer interaction", only "human" and "computer" are index terms. The term vectors are $u_{\text{human}} = (0.221, -0.113)$ and $u_{\text{computer}} = (0.241, 0.043)$, so line L3 gives $\hat q = ((0.221 + 0.241)/3.34,\ (-0.113 + 0.043)/2.54) \approx (0.138, -0.028)$. The cosines after line L4, next to the cosines with the raw columns of $A$, are:

| document | $c_3$ | $c_1$ | $c_4$ | $c_2$ | $c_5$ | $m_4$ | $m_3$ | $m_2$ | $m_1$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LSA, $k = 2$ | 0.998 | 0.998 | 0.987 | 0.937 | 0.908 | 0.050 | −0.099 | −0.106 | −0.124 |
| raw counts | 0 | 0.816 | 0.289 | 0.289 | 0 | 0 | 0 | 0 | 0 |

All five $c$ titles rank above all four $m$ titles. The titles $c_3$ and $c_5$ contain no query word and get raw cosine 0, but LSA puts $c_3$ at the top. The same effect shows for terms. The rows for "human" and "user" in $A$ have correlation $-0.38$, since the two words never occur in the same title. In $A_2$ their correlation is $0.94$, and the correlation of "human" with "minors" is $-0.83$.

## Correctness

The [proof](proofs/correctness.md) shows three facts. First, $A_k$ is the best approximation of $A$ of rank at most $k$ in the Frobenius and spectral norms, with $\lVert A - A_k \rVert_F^2 = \sum_{i > k} \sigma_i^2$ and $\lVert A - A_k \rVert_2 = \sigma_{k+1}$. This is the Eckart-Young theorem, proved there with [Weyl's inequality](/weyls-inequality/). Second, folding in column $j$ of $A$ gives exactly row $j$ of $V_k$, and in general $\Sigma_k \hat q$ holds the coordinates of the orthogonal projection of $q$ onto the span of $u_1, \ldots, u_k$. Third, the cosine of line L5 equals the cosine between that projection and column $j$ of $A_k$, so the scores compare the query with the documents of the denoised matrix.

## Complexity

Line L1 costs time linear in the total length of the documents. For a dense SVD, the implementation forms $A^{\top} A$ in $\Theta(m n^2)$ and diagonalizes it with Jacobi sweeps at $\Theta(n^3)$ each; the [Golub-Kahan](/golub-kahan-svd-algorithm/) algorithm costs $\Theta(m n \min(m, n))$ and is more accurate. Real collections are large and sparse, so the top $k$ triplets are found with the [Lanczos algorithm](/lanczos-algorithm/) or a randomized method at $O(N k)$ per pass over the $N$ nonzero entries, plus $O((m + n) k^2)$ for orthogonalization. Folding in a query costs $\Theta(m k)$, or the number of query terms times $k$ with a sparse query. Scoring costs $\Theta(n k)$ per query, against the cost of a sparse [inverted file](/inverted-file-index/) lookup for word matching. The reduced space takes $\Theta((m + n) k)$ memory, and it is dense even when $A$ is sparse.

## Properties

- Deterministic up to the signs of the singular vectors. Flipping the sign of $u_i$ and $v_i$ together changes neither $A_k$ nor any score.
- Unsupervised and linear: the representation of a document is a linear function of its weighted term vector.
- Not centered. LSA takes the SVD of $A$ itself, while [principal component analysis](/principal-component-analysis/) takes it after subtracting the mean document. On nonnegative data the first LSA dimension often points close to the mean document.
- The coordinates can be negative and are usually hard to name, unlike the factors of [nonnegative matrix factorization](/nonnegative-matrix-factorization/).
- The choice of $k$ is empirical. With $k = \operatorname{rank}(A)$ and the scaling of line L4, the ranking is the same as the ranking by cosine on the raw columns.

## Variants and improvements

- **Term weighting.** Raw counts let frequent words dominate. Tf-idf and log-entropy weights work better in most reported experiments.
- **Updating.** Folding in is cheap but leaves $U_k$ and $\Sigma_k$ unchanged, so the space slowly goes stale as documents are added. SVD updating methods revise the factors in place at a cost between folding in and recomputing.
- **Randomized truncated SVD.** Halko, Martinsson and Tropp compute $A_k$ with a few passes over a sparse matrix; see [randomized PCA](/randomized-pca/).
- **Probabilistic LSA.** Hofmann (1999) replaced the SVD by a mixture model fitted with EM, so that the factors are probabilities. [Latent Dirichlet allocation](/latent-dirichlet-allocation/) adds a Dirichlet prior to that model.
- **Nonnegative factors.** [Nonnegative matrix factorization](/nonnegative-matrix-factorization/) of the same matrix gives topics as nonnegative word weights.
- **Random projection.** [Random projection](/random-projection/) of the term vectors gives a cheaper reduction with no SVD, at the cost of keeping noise directions.
- **Word vectors.** Rows of $U_k \Sigma_k$, or of a factorization of a word-context matrix, are early word embeddings. LSA was evaluated this way on the TOEFL synonym test by Landauer and Dumais (1997).

## When to use it

Use LSA when word matching misses relevant documents because of synonyms, when a small dense representation of documents or terms is needed for clustering or classification, or as a fast baseline for topic structure. It needs a collection large enough for co-occurrence statistics, and it assumes that a linear subspace captures the topics. Prefer word matching through an inverted index when exact terms matter, for example for names and codes, or when the collection changes faster than the SVD can be refreshed. Prefer probabilistic topic models when the factors must be read as topics.

## Pitfalls

- **Comparing different spaces.** A query must be folded in with the same weighting, the same vocabulary and the same $U_k$ and $\Sigma_k$ as the documents. Query words outside the vocabulary are dropped silently.
- **Stale folding in.** Many folded-in documents do not change the axes. Recompute or update the SVD from time to time.
- **Scaling.** Ranking by rows of $V_k$, of $V_k \Sigma_k$ or of $V_k \Sigma_k^{1/2}$ gives different results. State the choice and keep it.
- **Choosing $k$.** Too small a $k$ merges unrelated topics, as with $k = 2$ above where every title is either "computer" or "graph". Too large a $k$ keeps the noise that LSA is meant to remove. Tune $k$ on held-out queries.
- **Polysemy.** A word gets one vector, the weighted average of its senses, so LSA handles synonyms better than words with several meanings.
- **Dense output.** $U_k$ and $V_k$ are dense, so the inverted index for the reduced space is no longer sparse, and nearest-neighbour search is needed for large $n$.

## Implementations

## History

Furnas, Deerwester, Dumais, Landauer, Harshman, Streeter and Lochbaum at Bellcore described retrieval with a truncated SVD of the term-document matrix at SIGIR 1988, and the method was patented in 1989. Deerwester, Dumais, Furnas, Landauer and Harshman gave the full account in 1990, under the name latent semantic indexing, with the nine-title example above. The mathematical core is older: Eckart and Young proved in 1936 that the truncated SVD gives the best low-rank approximation. Berry, Dumais and O'Brien (1995) described the linear algebra of weighting, folding in and updating. In the 1990s Landauer and Dumais used the same model, called latent semantic analysis, as a theory of how people learn word meanings. Hofmann's probabilistic LSI (1999) and latent Dirichlet allocation (2003) moved topic modelling to probabilistic models.

## References
