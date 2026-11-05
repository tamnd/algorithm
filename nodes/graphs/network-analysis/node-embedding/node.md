---
tag: S0DXRY
kind: problem
slug: node-embedding
name: Node embedding
aliases:
- network embedding
- graph embedding
area: graphs/network-analysis
level: advanced
summary: Map each node to a low-dimensional vector that preserves graph structure.
model: real-ram
complexity:
  vars: {n: the number of vertices, d: the embedding dimension}
  time: {worst: O(n^3)}
prereqs: [adjacency-matrix, singular-value-decomposition, node-similarity]
see_also: [deepwalk, node2vec, laplacian-eigenmaps, spectral-clustering, link-prediction, node-similarity, singular-value-decomposition, stochastic-neighbor-embedding]
sources:
  - paper: doi:10.1162/089976603321780317
    title: Mikhail Belkin and Partha Niyogi, Laplacian eigenmaps for dimensionality reduction and data representation, Neural Computation 15(6), 1373 to 1396 (2003)
    locator: Section 3, the objective that keeps adjacent vertices close, and its solution by the generalized eigenvectors of the graph Laplacian
  - paper: doi:10.1145/2623330.2623732
    title: Bryan Perozzi, Rami Al-Rfou and Steven Skiena, DeepWalk, online learning of social representations, Proceedings of the 20th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 701 to 710 (2014)
    locator: Section 4, truncated random walks treated as sentences and fed to the skip-gram model
  - paper: doi:10.1145/2939672.2939754
    title: Aditya Grover and Jure Leskovec, node2vec, scalable feature learning for networks, Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 855 to 864 (2016)
    locator: Section 3, the objective over random-walk neighbourhoods and the second-order biased walk
  - paper: doi:10.1145/3159652.3159706
    title: Jiezhong Qiu, Yuxiao Dong, Hao Ma, Jian Li, Kuansan Wang and Jie Tang, Network embedding as matrix factorization, unifying DeepWalk, LINE, PTE, and node2vec, Proceedings of the 11th ACM International Conference on Web Search and Data Mining, 459 to 467 (2018)
    locator: Section 2, the closed-form matrices that DeepWalk and LINE with negative sampling factorize implicitly
  - paper: doi:10.1073/pnas.1911030117
    title: C. Seshadhri, Aneesh Sharma, Andrew Stolman and Ashish Goel, The impossibility of low-rank representations for triangle-rich complex networks, Proceedings of the National Academy of Sciences 117(11), 5631 to 5637 (2020)
    locator: the theorem that dot-product embeddings of low dimension cannot generate graphs with many triangles among low-degree vertices
  - paper: arxiv:1709.05584
    title: William L. Hamilton, Rex Ying and Jure Leskovec, Representation learning on graphs, methods and applications, IEEE Data Engineering Bulletin 40(3), 52 to 74 (2017)
    locator: Section 2, the encoder-decoder framework (encoder, pairwise decoder, similarity function, loss) and the survey of shallow embedding methods
---

Node embedding asks for a map from the vertices of a graph to vectors in $\mathbb{R}^d$, with $d$ much smaller than the number of vertices, such that the geometry of the vectors reflects the structure of the graph: vertices that are close or similar in the graph get vectors that are close or have a large dot product. The vectors then serve as features for standard machine learning, for [link prediction](/link-prediction/), node classification, clustering and visualization. The problem is defined by a choice of graph similarity and a choice of loss, and the main families of solutions are spectral methods such as [Laplacian eigenmaps](/laplacian-eigenmaps/), matrix factorization, and random-walk methods such as [DeepWalk](/deepwalk/) and [node2vec](/node2vec/).

## In plain words

A graph is hard to feed into most learning tools, which expect each item to be a list of numbers. Node embedding gives each vertex a short list of numbers, its coordinates in a small space, chosen so that the map looks like the graph: friends end up near each other, people in the same group end up in the same region, and people in similar positions, such as two hubs, can end up with similar coordinates.

There is no single right map. Each method picks what "similar" means, such as being linked, sharing neighbours, or often being visited together by a random walker, and then finds the coordinates that keep those similar vertices close. Once the coordinates exist, finding likely new links or grouping vertices becomes a question about points in space.

## Definition

**Input.** A graph $G = (V, E)$ with $n$ vertices, directed or undirected, with or without non-negative edge weights, and a dimension $d \ge 1$.

**Output.** An *embedding* $Z \in \mathbb{R}^{n \times d}$, whose row $z_u$ is the vector of vertex $u$. For a directed graph, methods often return two vectors per vertex, a source vector $z_u$ and a target vector $z'_u$, so that the score of the arc $(u, v)$ is $z_u \cdot z'_v$, which need not equal that of $(v, u)$.

**Objective.** In the encoder-decoder form (Hamilton, Ying and Leskovec), choose a graph similarity $s_G(u, v)$, a decoder $\mathrm{dec}(z_u, z_v)$, usually the dot product or a function of the distance, and a loss $\ell$, and minimize

$$\mathcal{L}(Z) = \sum_{u, v \in V} \ell\bigl(\mathrm{dec}(z_u, z_v),\ s_G(u, v)\bigr).$$

**The matrix form.** With the square loss and the dot-product decoder, the problem is low-rank approximation of a similarity matrix $S$:

$$\min_{Z \in \mathbb{R}^{n \times d}} \bigl\| S - Z Z^\top \bigr\|_F \quad \text{or} \quad \min_{Z, Z' \in \mathbb{R}^{n \times d}} \bigl\| S - Z Z'^\top \bigr\|_F.$$

By the Eckart-Young theorem, the second problem is solved by the truncated [singular value decomposition](/singular-value-decomposition/): if $S = U \Sigma W^\top$, take $Z = U_d \Sigma_d^{1/2}$ and $Z' = W_d \Sigma_d^{1/2}$ from the $d$ largest singular values. For symmetric $S$, the first problem keeps the $d$ largest positive eigenvalues.

**The Laplacian form.** Laplacian eigenmaps minimize $\sum_{\{u, v\} \in E} w_{uv} \|z_u - z_v\|^2$ subject to $Z^\top D Z = I$ and $Z^\top D \mathbf{1} = 0$, with $D$ the diagonal matrix of weighted degrees. The solution is given by the generalized eigenvectors $L y = \lambda D y$ of the Laplacian $L = D - A$ for the $d$ smallest non-zero eigenvalues.

**Ties and disconnected graphs.** When eigenvalues or singular values are equal at the cut-off $d$, the optimal $Z$ is not unique, and any rotation of the vectors within an eigenspace is equally good; embeddings are in any case defined only up to rotation (for dot products) or rigid motion (for distances). On a disconnected graph, the Laplacian has one zero eigenvalue per component, and the first eigenvectors only mark the components; random-walk methods never place vertices of different components in the same walk, so their relative position is set by the negative samples alone. The usual practice is to embed each component separately or to add a small amount of teleportation.

## Variants

- **What to preserve.** First-order proximity (edges), second-order proximity (shared neighbours), higher-order proximity (walks of several steps, as in the Katz matrix or powers of the transition matrix), or structural roles (struc2vec, which makes two hubs in different parts of the graph similar).
- **Shallow and inductive.** Shallow methods learn one free vector per vertex and cannot embed a vertex not seen in training; inductive methods, such as graph neural networks, learn a function of the vertex features and the neighbourhood that applies to new vertices and new graphs.
- **Unsupervised and supervised.** The objectives above use only the graph; supervised versions train the vectors with labels for a downstream task.
- **Attributed, signed, heterogeneous and dynamic graphs.** Vertex features, negative edges, several types of vertex and edge, and graphs that change over time.
- **Other geometries.** Embedding in hyperbolic space fits trees and hierarchies with fewer dimensions than Euclidean space; metric embedding with guaranteed distortion is a separate, worst-case problem.

## Examples

Take two triangles $\{0, 1, 2\}$ and $\{3, 4, 5\}$ joined by the edge 2-3, undirected and without weights.

**Laplacian eigenmaps with $d = 1$.** The Laplacian $L = D - A$ has eigenvalues $0$, $(5 - \sqrt{17})/2 \approx 0.438$, $3$, $3$, $3$ and $(5 + \sqrt{17})/2 \approx 4.562$. The eigenvector of $0.438$ is proportional to $(1, 1, a, -a, -1, -1)$ with $a = (\sqrt{17} - 3)/2 \approx 0.562$: the two triangles go to opposite sides, and the bridge vertices 2 and 3 sit between them, closer to the middle. With the normalized version $L y = \lambda D y$, the second eigenvalue is about $0.205$ and the vector is about $(1, 1, 0.591, -0.591, -1, -1)$.

**Truncated eigendecomposition of $A$ with $d = 2$.** The adjacency matrix has eigenvalues $1 + \sqrt{2} \approx 2.414$, $\sqrt{3}$, $-\sqrt{3}$, $1 - \sqrt{2}$, $-1$ and $-1$. Keeping the two largest positive ones gives $Z = (\sqrt{2.414}\, x_1,\ \sqrt{1.732}\, x_2)$ with the eigenvectors $x_1$ and $x_2$. The error is $\|A - Z Z^\top\|_F = (3 + 1 + 1 + (1 - \sqrt{2})^2)^{1/2} \approx 2.274$. The reconstructed scores are about $0.64$ for the edge 0-1, $0.18$ for the non-edge 0-3 and $-0.04$ for the non-edge 0-4, so for link prediction the vertex nearer the bridge is the more likely partner. The eigenvalue $-\sqrt{3}$ has the same absolute value as $\sqrt{3}$, so an unconstrained rank-2 approximation $Z Z'^\top$ has a second optimum with the same error: a tie at the cut-off.

**Non-example.** One-hot vectors, $z_u = e_u \in \mathbb{R}^n$, preserve the graph only in the trivial sense that the adjacency matrix can be stored next to them; with $d = n$ the problem has no compression and the dot products say nothing about the graph.

## Known algorithms

- **Spectral methods.** [Laplacian eigenmaps](/laplacian-eigenmaps/) (Belkin and Niyogi 2003), and the spectral embedding behind [spectral clustering](/spectral-clustering/). A full eigendecomposition takes $O(n^3)$ time; Lanczos or randomized methods find $d$ eigenvectors of a sparse matrix in about $O(m d + n d^2)$ time per iteration.
- **Matrix factorization of higher-order proximity.** GraRep factorizes the $k$-step transition matrices, HOPE the Katz and personalized PageRank matrices, with a truncated SVD. The similarity matrices are dense, so these methods need $O(n^2)$ memory unless the factorization is done implicitly.
- **Random-walk methods.** [DeepWalk](/deepwalk/) (Perozzi, Al-Rfou and Skiena 2014) runs short uniform random walks from every vertex and trains the skip-gram model of word2vec on them, treating walks as sentences. [node2vec](/node2vec/) (Grover and Leskovec 2016) biases the walks between breadth-first and depth-first exploration. LINE optimizes first- and second-order proximity directly. Their cost is linear in the total length of the walks times $d$.
- **The unifying view.** Qiu and coauthors (2018) showed that DeepWalk with negative sampling implicitly factorizes the matrix $\log\bigl(\frac{\mathrm{vol}(G)}{bT} \bigl(\sum_{r=1}^{T} (D^{-1}A)^r\bigr) D^{-1}\bigr)$, applied entrywise, with window $T$ and $b$ negative samples, so the random-walk methods are matrix factorization methods with a particular similarity.
- **Graph neural networks.** Message passing over neighbours, trained end to end; inductive, and able to use vertex features.

## Bounds

- **Output size.** Any method must write $n d$ numbers, so $\Omega(n d)$ time is needed.
- **Exactness.** For the matrix form, the truncated SVD is optimal in Frobenius and spectral norm (Eckart-Young), and the error is the norm of the dropped singular values; no rank-$d$ embedding does better.
- **Limits of low-dimensional dot products.** Seshadhri, Sharma, Stolman and Goel (2020) proved that if edges are generated with probabilities given by dot products of embeddings in dimension $d$, then the graphs cannot have both low degrees and many triangles, as social networks do, unless $d$ is large. So shallow dot-product embeddings of small dimension cannot reproduce [triadic closure](/triadic-closure/) in sparse graphs.
- **Distortion.** For distance-based embeddings, some graphs, such as expanders, need distortion $\Omega(\log n)$ in any Euclidean embedding, whatever the dimension.

## Reductions

- **To low-rank approximation.** Every method with a dot-product decoder and the square loss reduces to truncated SVD of its similarity matrix; with the skip-gram loss the reduction is through the matrix above.
- **From [spectral clustering](/spectral-clustering/).** Spectral clustering is a Laplacian embedding followed by $k$-means on the vectors.
- **To [link prediction](/link-prediction/) and [node similarity](/node-similarity/).** Any embedding gives a similarity score, the dot product or the distance of two vectors, and so a link predictor.

## Applications

- **Link prediction and recommendation.** Score candidate pairs by their vectors, in social networks, citation graphs and user-item graphs.
- **Node classification.** Use the vectors as features with a few labelled vertices, for example to predict the functions of proteins or the topics of documents.
- **Community detection and visualization.** Cluster the vectors, or embed in two dimensions to draw the graph, often with [t-SNE](/stochastic-neighbor-embedding/) on top of a higher-dimensional embedding.
- **Knowledge graphs.** Related methods embed entities and relations for link completion.

## References
