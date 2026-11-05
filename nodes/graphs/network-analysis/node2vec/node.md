---
tag: 3SC38Y
kind: algorithm
slug: node2vec
name: node2vec
area: graphs/network-analysis
level: advanced
summary: Biased random walks with return and in-out parameters, then skip-gram.
solves: [node-embedding]
model: real-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, Δ: the maximum degree, r: the walks per vertex, l: the walk length, k: the window, s: the negative samples per pair, d: the dimension}
  time: {worst: O(r n l (Δ + k s d))}
  space: {extra: O(m + r n l + n d)}
properties: {directed: false, weighted: true, deterministic: false, recursive: false}
history:
  year: 2016
  people: [Aditya Grover, Jure Leskovec]
  note: Grover and Leskovec introduced node2vec at KDD 2016, generalizing the uniform walks of DeepWalk with a second-order walk controlled by a return parameter p and an in-out parameter q.
prereqs: [node-embedding, deepwalk, markov-chain, alias-method]
see_also: [node-embedding, deepwalk, laplacian-eigenmaps, link-prediction, alias-method, markov-chain, personalized-pagerank, structural-equivalence]
sources:
  - paper: doi:10.1145/2939672.2939754
    title: Aditya Grover and Jure Leskovec, node2vec, scalable feature learning for networks, Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 855 to 864 (2016)
    locator: Section 3.2 (the second-order walk with the bias alpha equal to 1/p, 1 or 1/q by the distance from the previous vertex), Algorithm 1, and Section 4 (the Les Misérables case study and the experiments)
  - paper: doi:10.1145/2623330.2623732
    title: Bryan Perozzi, Rami Al-Rfou and Steven Skiena, DeepWalk, online learning of social representations, Proceedings of the 20th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, 701 to 710 (2014)
    locator: Section 4, uniform truncated random walks used as sentences for the skip-gram model
  - paper: arxiv:1310.4546
    title: Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg Corrado and Jeffrey Dean, Distributed representations of words and phrases and their compositionality, Advances in Neural Information Processing Systems 26 (2013)
    locator: Section 2.2, the skip-gram objective with negative sampling and the noise distribution proportional to the unigram count to the power 3/4
  - paper: doi:10.1145/3159652.3159706
    title: Jiezhong Qiu, Yuxiao Dong, Hao Ma, Jian Li, Kuansan Wang and Jie Tang, Network embedding as matrix factorization, unifying DeepWalk, LINE, PTE, and node2vec, Proceedings of the 11th ACM International Conference on Web Search and Data Mining, 459 to 467 (2018)
    locator: Section 2.4, the matrix that node2vec with negative sampling factorizes implicitly, in terms of the stationary distribution of the second-order walk
  - paper: doi:10.1145/355744.355749
    title: Alastair J. Walker, An efficient method for generating discrete random variables with general distributions, ACM Transactions on Mathematical Software 3(3), 253 to 256 (1977)
    locator: the alias method, which samples from a fixed discrete distribution in constant time after linear preprocessing
---

node2vec is a [node embedding](/node-embedding/) method: it learns a vector for every vertex of a graph by running many short random walks and then training the skip-gram model of word2vec on them, so that vertices that often appear near each other in walks get similar vectors. Its novelty over [DeepWalk](/deepwalk/) is the walk. Each step depends on the previous vertex as well as the current one, through a *return parameter* $p$ and an *in-out parameter* $q$. With a small $q$ the walk moves outward, like depth-first search, and the vectors reflect communities; with a large $q$ it stays near its start, like breadth-first search, and the vectors pick up local structure. Grover and Leskovec (2016) showed that tuning $p$ and $q$ improves link prediction and node classification over DeepWalk.

## In plain words

Imagine a walker who moves through a social network, one friendship at a time, and writes down the names of the people met. Do this many times from everyone, and the lists of names look like sentences. Then use a tool built for text, which learns from sentences that words appearing in the same context mean similar things, and it will give each person a list of numbers, a vector, such that people met close together in the walks get similar vectors.

node2vec adds two knobs to the walker. One controls how often the walker goes straight back to the person just left. The other controls whether the walker prefers to stay among friends of that person, exploring the local circle, or to head outward to people who are farther away. Staying local captures who sits in the same circle; heading out captures the larger groups of the network.

## The problem

**Input.** An undirected graph $G = (V, E)$ with $n$ vertices and positive edge weights $w(u, v)$ (weight 1 for unweighted graphs), a dimension $d$, the number of walks per vertex $r$, the walk length $\ell$ (counted in vertices), the window size $k$, the number of negative samples $s$, and the parameters $p > 0$ and $q > 0$.

**Output.** A matrix $Z \in \mathbb{R}^{n \times d}$ with a row $z_u$ for each vertex, intended to approximately maximize the skip-gram objective

$$\sum_{u \in V} \sum_{c \in N_S(u)} \Bigl( \log \sigma(z_u \cdot y_c) + \sum_{j = 1}^{s} \mathbb{E}_{x \sim P_n} \log \sigma(-z_u \cdot y_x) \Bigr),$$

where $N_S(u)$ is the multiset of vertices that appear within $k$ positions of an occurrence of $u$ in the walks, $\sigma(x) = 1/(1 + e^{-x})$, $y_c$ is a second "context" vector for each vertex, and $P_n$ is the noise distribution, proportional to the number of occurrences of a vertex in the walks raised to the power $3/4$.

**The biased walk.** If the walk has just gone from $t$ to $v$, the next vertex $x$ is a neighbour of $v$ chosen with probability proportional to

$$\pi(t, v, x) = \alpha_{pq}(t, x)\, w(v, x), \qquad \alpha_{pq}(t, x) = \begin{cases} 1/p & \text{if } x = t, \\ 1 & \text{if } x \text{ is adjacent to } t, \\ 1/q & \text{otherwise}, \end{cases}$$

that is, by whether $x$ is at distance 0, 1 or 2 from $t$. The first step of a walk, which has no previous vertex, chooses a neighbour with probability proportional to the edge weight.

## The algorithm

```pseudo id=main
NODE2VEC(G, d, r, ℓ, k, p, q)
L1  for each step t → v of G and each x ∈ N(v): π(t, v, x) ← w(v, x)/p if x = t, w(v, x) if x ∈ N(t), w(v, x)/q otherwise
L2  walks ← empty list
L3  repeat r times
L4      for each u ∈ V in a random order do
L5          walk ← [u]; if ℓ > 1 and N(u) ≠ ∅ then append x ∈ N(u) chosen with probability ∝ w(u, x)
L6          while 1 < |walk| < ℓ do
L7              t, v ← the last two vertices of walk; append x ∈ N(v) chosen with probability ∝ π(t, v, x)
L8          append walk to walks
L9  Z ← SKIPGRAM-SGD(walks, d, k, s)
L10 return Z
```

Line L1 defines the transition weights of the second-order walk; an implementation either stores an [alias table](/alias-method/) for every pair $(t, v)$ with an edge, as in the original paper, or computes the weights of the neighbours of $v$ when the walk reaches it. Lines L3 and L4 start $r$ walks at every vertex. Line L5 takes the first step by edge weight, and lines L6 and L7 extend the walk with the biased rule until it has $\ell$ vertices. A walk from an isolated vertex stops at line L5 with one vertex. Line L9 runs stochastic gradient descent on the skip-gram objective: for every vertex $u$ in a walk and every $c$ within $k$ positions of it, it raises $\sigma(z_u \cdot y_c)$ and lowers $\sigma(z_u \cdot y_x)$ for $s$ vertices $x$ drawn from the noise distribution.

## Example

Take two triangles $\{0, 1, 2\}$ and $\{3, 4, 5\}$ joined by the edge 1-3, without weights. Suppose a walk has just gone from 0 to 1. The neighbours of 1 are 0 (the previous vertex, distance 0), 2 (adjacent to 0, distance 1) and 3 (distance 2 from 0). The next step has these probabilities:

| $p$, $q$ | to 0 (return) | to 2 (stay local) | to 3 (move out) |
|---|---|---|---|
| 1, 1 (DeepWalk) | 1/3 | 1/3 | 1/3 |
| 1, 2 | 0.4 | 0.4 | 0.2 |
| 4, 1/2 | 1/13 | 4/13 | 8/13 |

With $q = 2$ the walk stays in the first triangle four times out of five; with $p = 4$ and $q = 1/2$ it crosses to the other triangle with probability $8/13 \approx 0.62$ and rarely turns back. One walk of 8 vertices from 0 with $p = 4$ and $q = 1/2$ was $0, 1, 2, 0, 1, 3, 4, 3$.

For the vectors, take two cliques on $\{0, \dots, 4\}$ and $\{5, \dots, 9\}$ joined by the edge 4-5, and run node2vec with $d = 8$, $r = 10$, $\ell = 20$, $k = 3$, $s = 5$ and $p = q = 1$. In one run, the mean cosine similarity of the vectors was $0.99$ for pairs in the same clique and $0.25$ for pairs in different cliques: the two communities are separated in the vector space.

## Correctness

The walk phase is exact: at every step, the vertex appended at line L7 is a neighbour of $v$, and it is $x$ with probability exactly $\pi(t, v, x) / \sum_{y \in N(v)} \pi(t, v, y)$, which is well defined because $v$ has at least the neighbour $t$ and all weights are positive. So each walk is a sample of the second-order Markov chain with the stated rule, and on an undirected graph a walk from a vertex with a neighbour never gets stuck and has exactly $\ell$ vertices. With $p = q = 1$ every $\alpha$ is 1 and the walk is the first-order weighted random walk of DeepWalk. The learning phase performs gradient steps on the skip-gram loss with negative sampling: for one pair the loss is $-\log \sigma(z_u \cdot y_c) - \sum_x \log \sigma(-z_u \cdot y_x)$, whose gradient with respect to $z_u$ is $-(1 - \sigma(z_u \cdot y_c))\, y_c + \sum_x \sigma(z_u \cdot y_x)\, y_x$. The objective is not convex, so SGD finds a local optimum, not a global one; this is a heuristic, as in word2vec. The full proof of the walk phase and of the update rule is in the proof file below.

## Complexity

Let $L = r n \ell$ be the total length of the walks. Computing the weights when the walk reaches $v$ costs $O(\deg v)$ per step with hashed adjacency, so the walks take $O(L \Delta)$ time; with alias tables built in advance for every pair $(t, v)$, each step costs $O(1)$, but the tables take $\Theta(\sum_v \deg(v)^2)$ time and space, which can be far more than $m$ on graphs with hubs. The skip-gram phase handles at most $2k$ context vertices for each of the $L$ positions, each with $s + 1$ dot products and updates of length $d$, so it takes $O(L k s d)$ time per epoch for $s \ge 1$. The walks take $O(L)$ space, the graph $O(m)$, and the two vector tables $O(n d)$. In practice the walks are generated in parallel and the skip-gram phase uses asynchronous SGD.

## Properties

- **Undirected and weighted.** Weights enter through $w(v, x)$. The method extends to directed graphs by following out-arcs; the walk can then stop early at a vertex with no out-arcs.
- **Randomized.** The walks, the order of the start vertices, the negative samples and the initial vectors are random; two runs give different vectors, and the vectors are defined only up to rotation, so only dot products and distances should be compared.
- **Second-order.** The walk is a Markov chain on directed edges $(t, v)$, not on vertices, so its analysis, and the matrix that the method factorizes implicitly, depend on the chain over the $2m$ directed edges.
- **Local information.** A step looks only at $v$, its neighbours and whether they are neighbours of $t$, so the walk can be run on graphs too large for a global eigendecomposition.

## Variants and improvements

- **[DeepWalk](/deepwalk/).** The special case $p = q = 1$, with hierarchical softmax instead of negative sampling in the original.
- **Faster walks.** Rejection sampling with the first-order weights as proposal avoids the $\Theta(\sum \deg^2)$ alias tables: accept $x$ with probability $\alpha_{pq}(t, x) / \max(1, 1/p, 1/q)$.
- **The matrix view.** Qiu and coauthors (2018) express node2vec with negative sampling as the implicit factorization of a matrix built from the stationary distribution and the powers of the second-order walk, and NetMF factorizes such matrices directly.
- **Edge features.** For link prediction, the paper combines the vectors of two vertices by the Hadamard (entrywise) product, the average, or the $L_1$ or $L_2$ distance, and trains a classifier on the result.
- **Inductive methods.** Graph neural networks learn a function of vertex features that applies to new vertices, which node2vec cannot embed without retraining.

## When to use it

Use node2vec to get general-purpose vertex features from a graph without vertex attributes, for link prediction, node classification or clustering, when the graph is too large for a dense matrix factorization but small enough that many walks per vertex fit in memory. Tune $p$ and $q$ on a validation task, typically over $\{1/4, 1/2, 1, 2, 4\}$; when there is no task to tune on, $p = q = 1$ (DeepWalk) is a strong default. For small graphs, a spectral embedding such as [Laplacian eigenmaps](/laplacian-eigenmaps/) is deterministic and often as good.

## Pitfalls

- **Alias tables on graphs with hubs.** A vertex of degree $\Delta$ needs $\Delta$ tables of size $\Delta$, so a hub with $10^5$ neighbours needs $10^{10}$ entries. Compute the weights on the fly or use rejection sampling.
- **Confusing $p$ and $q$.** A small $p$ makes the walk return; a small $q$ makes it go out (depth-first). A large $q$ keeps it local (breadth-first).
- **Comparing vectors from different runs.** Each run gives vectors in an arbitrary rotation; train once and compare vectors within a run, or align runs first.
- **Isolated vertices and small components.** An isolated vertex appears in no context, and its vector stays at its random initial value; vertices of different components never share a walk, and their relative position is set only by the negative samples.
- **Leakage in link prediction.** The edges held out for testing must be removed before the walks are generated, or the evaluation measures memorization.

## Implementations

## History

Aditya Grover and Jure Leskovec introduced node2vec at KDD 2016, building on DeepWalk (Perozzi, Al-Rfou and Skiena 2014), which in turn borrowed the skip-gram model with negative sampling of word2vec (Mikolov and coauthors 2013). Qiu and coauthors (2018) later showed that these walk-based methods implicitly factorize matrices of walk probabilities, linking them to spectral methods.

## References
