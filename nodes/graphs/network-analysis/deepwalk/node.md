---
tag: 0SCSY9
kind: algorithm
slug: deepwalk
name: DeepWalk
area: graphs/network-analysis
level: advanced
summary: Learns node embeddings by applying skip-gram to random-walk sequences.
solves: [node-embedding]
model: word-ram
complexity:
  vars:
    n: the number of vertices
    d: the dimension of the embedding
    γ: the number of walks started at each vertex
    t: the length of each walk
    w: the window size
  time:
    worst: Θ(n d + γ n t w d log n)
    best: Θ(n d + γ n)
  space:
    extra: Θ(n d + t)
properties: {directed: true, weighted: false, deterministic: false, recursive: false}
prereqs: [node-embedding, stochastic-gradient-descent, markov-chain]
see_also: [node2vec, node-embedding, link-prediction, community-detection, laplacian-eigenmaps, singular-value-decomposition, huffman-coding, softmax-regression]
sources:
  - paper: doi:10.1145/2623330.2623732
    title: Bryan Perozzi, Rami Al-Rfou and Steven Skiena, DeepWalk, online learning of social representations, Proceedings of the 20th ACM SIGKDD Conference (KDD 2014), 701 to 710
    locator: Section 4 (the random walk generator, the SkipGram update and the hierarchical softmax) and Section 6 (the parameter settings)
  - paper: arXiv:1301.3781
    title: Tomas Mikolov, Kai Chen, Greg Corrado and Jeffrey Dean, Efficient estimation of word representations in vector space (2013)
    locator: Section 3 (the continuous skip-gram model and the hierarchical softmax with a Huffman tree)
  - paper: doi:10.1145/3159652.3159706
    title: Jiezhong Qiu, Yuxiao Dong, Hao Ma, Jian Li, Kuansan Wang and Jie Tang, Network embedding as matrix factorization, unifying DeepWalk, LINE, PTE, and node2vec, Proceedings of the 11th ACM WSDM Conference (WSDM 2018), 459 to 467
    locator: Section 2 (the matrix that DeepWalk with negative sampling implicitly factorizes)
  - paper: doi:10.1145/2939672.2939754
    title: Aditya Grover and Jure Leskovec, node2vec, scalable feature learning for networks, Proceedings of the 22nd ACM SIGKDD Conference (KDD 2016), 855 to 864
    locator: Section 3 (biased second-order random walks that generalize the walks of DeepWalk)
---

DeepWalk learns a vector of $d$ real numbers for each vertex of a graph, a [node embedding](/node-embedding/), so that vertices that appear close together on short random walks get vectors that point in similar directions. It treats each random walk as a sentence and each vertex as a word, and trains the skip-gram model of word2vec on these sentences: for each vertex in a walk, it raises the modelled probability of the vertices at most $w$ steps away in the same walk, by [stochastic gradient descent](/stochastic-gradient-descent/) with a hierarchical softmax. With $\gamma$ walks of length $t$ from each of the $n$ vertices, the work is $O(\gamma n t w d \log n)$, almost linear in $n$. Perozzi, Al-Rfou and Skiena proposed it in 2014, and it started the line of walk-based embeddings that includes [node2vec](/node2vec/).

## In plain words

Imagine wandering through a social network, each time stepping to a random friend of the current person, and writing down the names along the way. Do this many times from everyone. People in the same tight group show up near each other in these lists again and again.

DeepWalk reads the lists the way a language model reads text. It gives each person a short list of numbers, and slowly adjusts the numbers so that, from the numbers of one person, it can guess well who is written next to them in the lists.

At the end, people from the same group have similar numbers, and the numbers can be fed to any standard learning method, for example to predict missing friendships or to guess the group of a person.

## The problem

The input is a graph $G = (V, E)$ with $V = \{0, \ldots, n-1\}$, given by adjacency lists; $\mathrm{Adj}[v]$ lists the out-neighbours of $v$, and an undirected edge is in both lists. The graph has no weights and need not be connected. The parameters are the dimension $d$, the window size $w$, the number $\gamma$ of walks started at each vertex, the walk length $t$ and the learning rate $\alpha$.

The output is a matrix $\Phi$ with one row $\Phi_v \in \mathbb{R}^d$ per vertex. The model behind it is the skip-gram model with a hierarchical softmax. Put the $n$ vertices at the leaves of a binary tree with $n - 1$ inner nodes, and give each inner node $i$ a vector $\Psi_i \in \mathbb{R}^d$. For a vertex $u$, let $(i_1, s_1), \ldots, (i_L, s_L)$ be the inner nodes on the path from the root to the leaf of $u$, with $s_l = +1$ if the path goes to the left child and $s_l = -1$ if it goes to the right. With $\sigma(z) = 1/(1 + e^{-z})$, the model sets

$$\Pr(u \mid v) = \prod_{l=1}^{L} \sigma\bigl(s_l\, \Psi_{i_l} \cdot \Phi_v\bigr).$$

These numbers sum to 1 over $u$, since $\sigma(z) + \sigma(-z) = 1$ at each branch. Given the walks, the training objective is the sum, over each pair $(v, u)$ with $u$ at most $w$ positions from $v$ in a walk, of $-\log \Pr(u \mid v)$. DeepWalk does not compute an exact minimum of this non-convex loss; it runs one pass of stochastic gradient descent over the pairs as the walks are generated.

## The algorithm

```pseudo id=main
DEEPWALK(G, d, w, γ, t, α)
L1  Φ_v ← random vector in [−1/(2d), 1/(2d)]^d for each v;  Ψ_i ← 0 for each inner node i of the tree
L2  for pass ← 1 to γ do
L3      O ← a random permutation of V
L4      for each v in the order O do
L5          W ← a random walk of at most t vertices from v, each step to a uniform out-neighbour
L6          for j ← 1 to |W| do
L7              for each k with 1 ≤ k ≤ |W|, 0 < |k − j| ≤ w do
L8                  take the gradient of −log Pr(W[k] | Φ_{W[j]}) along the tree path of W[k]
L9                  for each (i, s) on the path: g ← α (1 − σ(s Ψ_i · Φ_{W[j]})) s;  Ψ_i ← Ψ_i + g Φ_{W[j]};  then Φ_{W[j]} ← Φ_{W[j]} + Σ g Ψ_i (old values)
L10 return Φ
```

The walk on line L5 stops early at a vertex with no out-neighbour. Line L9 is one gradient step of size $\alpha$ on the loss of the single pair, for both $\Phi_{W[j]}$ and the vectors on the path, all computed from the values before the step. The implementation uses a complete binary tree in heap layout and a constant $\alpha$; the paper builds the tree by [Huffman coding](/huffman-coding/) of the vertex frequencies, so that frequent vertices have short paths, and lowers $\alpha$ linearly during training.

## Example

Take the undirected graph with the vertices 0 to 6 and the 9 edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,3\}$, $\{2,3\}$, $\{3,4\}$, $\{4,5\}$, $\{4,6\}$, $\{5,6\}$: a group $\{0, 1, 2\}$, a group $\{4, 5, 6\}$, and the vertex 3 between them.

**One walk.** A walk of $t = 10$ vertices from 0 is $0, 1, 3, 1, 2, 0, 2, 1, 2, 3$. With $w = 2$, each position pairs with the up to 4 positions at most 2 away, which gives $2(2wt - w(w+1)) = 34$ pairs, starting $(0, 1), (0, 3), (1, 0), (1, 3), (1, 1), (3, 0), \ldots$ The pair $(1, 1)$ comes from the two visits to vertex 1 at positions 2 and 4; a vertex may be its own context.

**The tree.** For $n = 7$ the heap layout has the inner nodes 0 to 5 and the leaf of vertex $u$ at node $6 + u$. The path of vertex 0 is (node 0, right), (node 2, right), of length 2; the paths of the other vertices have length 3. At the start all $\Psi_i = 0$, so each branch has probability $\sigma(0) = 1/2$, and $\Pr(u \mid v)$ is $1/4$ for $u = 0$ and $1/8$ for the other six vertices, which sums to 1.

**Training.** With $d = 8$, $w = 2$, $\gamma = 20$, $t = 10$, $\alpha = 0.05$ and the seed 0, the cosines between the learned vectors are:

|   | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| 0 | 1.00 | 0.91 | 0.89 | 0.15 | −0.65 | −0.71 | −0.68 |
| 1 | 0.91 | 1.00 | 0.77 | 0.25 | −0.47 | −0.41 | −0.44 |
| 2 | 0.89 | 0.77 | 1.00 | 0.14 | −0.42 | −0.58 | −0.43 |
| 3 | 0.15 | 0.25 | 0.14 | 1.00 | 0.29 | 0.26 | 0.33 |
| 4 | −0.65 | −0.47 | −0.42 | 0.29 | 1.00 | 0.91 | 0.95 |
| 5 | −0.71 | −0.41 | −0.58 | 0.26 | 0.91 | 1.00 | 0.95 |
| 6 | −0.68 | −0.44 | −0.43 | 0.33 | 0.95 | 0.95 | 1.00 |

The two groups are clear: cosines from 0.77 to 0.95 inside a group, from −0.41 to −0.71 across, and the vertex 3 weakly similar to everyone. On 35 fixed test walks of length 10 (1190 pairs), the total loss falls from 2369.2 before training, which is $\ln 2$ times the total path length, to 1822.6 after.

## Correctness

**Theorem.** DEEPWALK stops. Each walk of line L5 is a run of the simple random walk on $G$, the pairs of lines L6 and L7 are exactly the pairs of positions at most $w$ apart, the model probabilities $\Pr(\cdot \mid v)$ form a probability distribution on $V$, and each execution of line L9 is one step of gradient descent with step $\alpha$ on $-\log \Pr(W[k] \mid \Phi_{W[j]})$ at the current parameters.

The walk claim holds because each step draws a uniform element of the current list. The distribution claim is an induction on the tree: the probabilities of the leaves below an inner node add up to the product of the branch probabilities down to that node, because the two children of a node get $\sigma(z)$ and $\sigma(-z)$. The gradient claim is a direct computation: $\frac{d}{dz}\bigl(-\log \sigma(z)\bigr) = -(1 - \sigma(z))$, so the partial derivatives of the pair loss are $-(1 - \sigma(s_l \Psi_{i_l} \cdot x))\, s_l\, x$ for $\Psi_{i_l}$ and the sum of $-(1 - \sigma(s_l \Psi_{i_l} \cdot x))\, s_l\, \Psi_{i_l}$ for $x$; the inner nodes on a path are distinct, and line L9 reads each $\Psi_{i_l}$ before it changes it, and changes $x$ only at the end. So DeepWalk is stochastic gradient descent on the skip-gram objective of its walks. As for any SGD on a non-convex loss, there is no guarantee of a global minimum. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model with real numbers in floating point, each arithmetic operation in $O(1)$ time.

- **Initialization.** Line L1 writes $n$ vectors of length $d$ and $n - 1$ zero vectors, $\Theta(nd)$.
- **Walks.** There are $\gamma n$ walks of at most $t$ vertices, and each step is a uniform choice in $O(1)$ time, so $O(\gamma n t)$ in all.
- **Pairs.** A walk of $t$ vertices has at most $2wt$ pairs. Each pair walks a tree path of length at most $\lceil \log_2 n \rceil$ and does $O(d)$ work per node, so $O(d \log n)$ per pair and $O(\gamma n t w d \log n)$ in all. This is the worst case when no walk stops early, which holds for every graph without sinks and $t > 2w$.
- **Best case.** In a graph without arcs every walk has one vertex and no pairs, so the time is $\Theta(nd + \gamma n)$.
- **Space.** $\Theta(nd)$ for $\Phi$ and $\Psi$, plus $O(t)$ for the current walk.

With a Huffman tree, the expected path length is about the entropy of the vertex frequencies in the walks, at most $\lceil \log_2 n \rceil + 1$. The paper uses $d = 128$, $w = 10$, $\gamma = 80$ and $t = 40$ in its experiments. The walks are independent, and the updates are sparse, so the paper also runs the updates in parallel without locks, as in word2vec.

## Properties

- **Directed or undirected, no weights.** The walks follow out-arcs, so a directed graph works as given; a walk stops at a sink. The basic method ignores weights; the common change is to step to a neighbour with probability proportional to the weight of the arc.
- **Randomized.** The initial vectors, the order of the vertices and the walks are random. With a fixed seed, as in the implementation, the run is deterministic. Different seeds give different embeddings, which need not be related by a rotation, since the loss is not convex.
- **Not recursive.** Nested loops over passes, vertices, walk positions, windows and tree paths.
- **Ties and disconnected graphs.** A walk never leaves the component of its start, so no pair ever links two components, and the relative position of their embeddings is set only by the random initial vectors and the shared tree. Do not read meaning into distances between components. There are no ties to break: all choices are random.
- **Online.** The updates need only the current walk, so new walks, from new vertices or new edges, can be added to a trained model.

## Variants and improvements

- **Huffman tree.** The paper and word2vec build the hierarchical softmax tree by Huffman coding, so that the vertices seen most often in the walks have the shortest paths.
- **Negative sampling.** Instead of the tree, each pair pulls $\Phi_v$ towards a context vector of $u$ and pushes it away from the context vectors of a few random vertices. Most later implementations use it.
- **node2vec.** Grover and Leskovec replace the uniform walk with a second-order walk that has two parameters, which move between walks that stay near the start, like a breadth-first search, and walks that go far, like a depth-first search. DeepWalk is the case where both parameters are 1.
- **Matrix factorization.** Qiu, Dong, Ma, Li, Wang and Tang showed that DeepWalk with negative sampling, for long walks, implicitly factorizes the entrywise logarithm of a matrix built from the average of the powers $1$ to $w$ of the random-walk matrix $D^{-1}A$. NetMF computes such a factorization directly, with a [singular value decomposition](/singular-value-decomposition/). This links DeepWalk to spectral methods such as [Laplacian eigenmaps](/laplacian-eigenmaps/).
- **Graph neural networks.** Methods that compute embeddings from vertex features by message passing came later and can embed vertices not seen in training, which DeepWalk cannot do without more training.

## When to use it

Use DeepWalk to get vertex features for a graph without vertex attributes, for tasks such as vertex classification with few labels, [link prediction](/link-prediction/) and a rough view of [community structure](/community-detection/). It scales to millions of vertices and is easy to run in parallel. When the vertices have rich attributes, or when new vertices must be embedded without retraining, a graph neural network is often a better choice. For small graphs, an exact spectral embedding gives a deterministic answer with known properties.

## Pitfalls

- **Learning rate.** A constant rate that is too large makes the vectors grow without bound and oscillate; a rate that is too small leaves them near the random start. The paper lowers it linearly to near zero.
- **Comparing runs.** Two runs give different embeddings. Compare tasks or neighbour lists, not coordinates.
- **Updating in place.** In line L9 the gradient for $\Phi_{W[j]}$ must use each $\Psi_i$ before its update, and $\Phi_{W[j]}$ must stay fixed while the path is processed. Updating both at once in the wrong order gives a step that is not a gradient step.
- **Sinks.** In a directed graph a walk that reaches a vertex without out-arcs stops; vertices that can reach only sinks get few pairs and poor vectors. Add the reverse arcs or restart walks when that matters.
- **Too few walks.** With small $\gamma$ or $t$, rare vertices get few updates, and their vectors stay close to the random start.

## Implementations

## History

Mikolov, Chen, Corrado and Dean introduced the skip-gram model with a hierarchical softmax for learning word vectors from text in 2013. Perozzi, Al-Rfou and Skiena observed in 2014 that the frequencies of vertices in short random walks on social networks follow a power law, like the frequencies of words, and applied skip-gram to the walks; they called the method DeepWalk and tested it on vertex classification with few labels. Grover and Leskovec generalized the walks in node2vec in 2016, and Qiu and coauthors explained DeepWalk with negative sampling as an implicit matrix factorization in 2018.

## References
