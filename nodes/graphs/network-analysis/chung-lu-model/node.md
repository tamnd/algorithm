---
tag: 42BR9Z
kind: model
slug: chung-lu-model
name: Chung-Lu model
aliases:
- expected degree model
area: graphs/network-analysis
level: advanced
summary: Random graph in which edge probabilities match prescribed expected degrees.
prereqs: [erdos-renyi-model, degree-distribution, bernoulli-trials]
see_also: [configuration-model, erdos-renyi-model, degree-distribution, scale-free-network, giant-component, stochastic-block-model, modularity, barabasi-albert-model]
sources:
  - paper: doi:10.1007/PL00012580
    title: Fan Chung and Linyuan Lu, Connected components in random graphs with given expected degree sequences, Annals of Combinatorics 6(2), 125 to 145 (2002)
    locator: the whole paper (the model, the expected degrees, the second-order average degree, and the results on the giant component and on small components)
  - paper: doi:10.1073/pnas.252631999
    title: Fan Chung and Linyuan Lu, The average distances in random graphs with given expected degrees, Proceedings of the National Academy of Sciences 99(25), 15879 to 15882 (2002)
    locator: the whole paper (the average distance about log n over log of the second-order average degree, and of order log log n for power laws with exponent between 2 and 3)
  - book: isbn:9780821836576
    title: Fan Chung and Linyuan Lu, Complex Graphs and Networks, CBMS Regional Conference Series in Mathematics 107, American Mathematical Society, 2006
    locator: Chapter 5, Random graphs with given expected degrees, and the following chapters on components, distances and eigenvalues
  - paper: doi:10.1007/978-3-642-21286-4_10
    title: Joel C. Miller and Aric Hagberg, Efficient generation of networks with given expected degrees, Algorithms and Models for the Web Graph (WAW 2011), Lecture Notes in Computer Science 6732, 115 to 126
    locator: the whole paper (sampling in O(n + m) expected time by sorting the weights and skipping pairs with geometric jumps)
---

The Chung-Lu model is a random [graph](/graph/) in which each vertex $i$ has a weight $w_i$, its target expected degree, and each pair $\{i, j\}$ is joined independently with probability $w_i w_j / W$, where $W = \sum_k w_k$. So vertex $i$ has expected degree about $w_i$. Like the [configuration model](/configuration-model/), it produces graphs with a chosen [degree distribution](/degree-distribution/), for example a power law, but it fixes only the expected degrees, and its edges are independent, which makes it easy to analyse and to sample. With all weights equal it is the [Erdős-Rényi model](/erdos-renyi-model/) $G(n, p)$. Chung and Lu introduced it in 2002 and used it to study components and distances in power-law graphs.

## The machine

**Input.** Non-negative weights $w_1, \ldots, w_n$ with $W = \sum_i w_i > 0$ and $\max_i w_i^2 \le W$, so that every probability below is at most 1.

**Edges.** For each pair $i < j$, put the edge $\{i, j\}$ with probability

$$p_{ij} = \frac{w_i w_j}{W},$$

independently of all other pairs. The result is a simple undirected graph without weights. Chung and Lu also allow a self-loop at $i$ with probability $w_i^2/W$; with it, the expected degree of $i$, a loop counted once, is exactly $\sum_j w_i w_j / W = w_i$. Without loops it is

$$\mathbb{E}[\deg(i)] = w_i - \frac{w_i^2}{W},$$

which is close to $w_i$ when $w_i$ is much smaller than $W$.

**When the condition fails.** If some $w_i^2 > W$, the common fixes are to cap the probability at $\min(1, w_i w_j/W)$, which lowers the degrees of the largest hubs, or to use one of the variants below.

**Generating a sample.** Tossing one coin per pair takes $\Theta(n^2)$ time. Miller and Hagberg sort the weights in decreasing order; for a fixed $i$, the probabilities $p_{ij}$ then decrease in $j$, and they skip ahead by geometric jumps with the current probability as an upper bound, accepting each candidate with the ratio of the true probability to the bound. This gives a sample in $O(n + m)$ expected time, where $m$ is the number of edges.

**Directed version.** Give each vertex an out-weight and an in-weight with equal totals $W$, and keep each arc $(i, j)$ with probability $w_i^{\mathrm{out}} w_j^{\mathrm{in}}/W$.

**Disconnected outputs.** The graph is not forced to be connected. A vertex with a small weight is isolated with a fixed positive probability, so a typical sample has isolated vertices and small components along with any giant component.

## What it counts

The model is a probability space over simple graphs on $\{1, \ldots, n\}$. Results are stated for a sequence of weight vectors with $n \to \infty$ and hold *asymptotically almost surely* (a.a.s.) when their probability tends to 1. Two averages play the main roles: the average weight $d = W/n$, and the **second-order average degree**

$$\tilde d = \frac{\sum_i w_i^2}{\sum_i w_i},$$

the expected weight of the vertex at the end of a random edge. Since $\sum w_i^2 \ge W^2/n$, always $\tilde d \ge d$.

**Degrees.** The degree of $i$ is a sum of independent [Bernoulli trials](/bernoulli-trials/) with mean about $w_i$, so it is close to a Poisson variable with mean $w_i$ when all $p_{ij}$ are small. The degree distribution of the graph is a mixture of Poisson distributions over the weights: if the weights have a power-law tail with exponent $\tau$, so do the degrees.

**Edges.** The expected number of edges is $\sum_{i < j} w_i w_j / W = (W^2 - \sum_i w_i^2)/(2W) = (W - \tilde d)/2$.

**A small exact example.** Take $w = (3, 2, 2, 1, 1, 1)$, so $W = 10$, $\max w_i^2 = 9 \le 10$, $d = 5/3$ and $\tilde d = 20/10 = 2$. The probabilities are $3/5$ for the pairs $\{0,1\}$ and $\{0,2\}$, $2/5$ for $\{1,2\}$, $3/10$ from 0 to each of 3, 4 and 5, $1/5$ from 1 or 2 to each of 3, 4 and 5, and $1/10$ among 3, 4 and 5. Then:

- The expected number of edges is $(10 - 2)/2 = 4$.
- Without loops, the expected degrees are $2.1, 1.6, 1.6, 0.9, 0.9, 0.9$, that is, $w_i - w_i^2/10$; the heaviest vertex loses the most.
- Vertex 0 is isolated with probability $(2/5)^2 (7/10)^3 = 343/6250 \approx 0.055$, and each of 3, 4 and 5 with probability $1134/3125 \approx 0.363$.
- Summing over all $2^{15}$ graphs, the graph is connected with probability about $0.183$.

## Relation to other models

- **Erdős-Rényi.** With $w_i = c$ for all $i$, every pair has probability $c/n$, which is $G(n, c/n)$; then $d = \tilde d = c$.
- **Configuration model.** The [configuration model](/configuration-model/) gives the exact degrees but has dependent edges, loops and multiple edges. The Chung-Lu model gives a simple graph with independent edges and only expected degrees. For many properties of sparse graphs with light-tailed weights the two behave alike.
- **Related inhomogeneous models.** The Norros-Reittu model uses $1 - e^{-w_i w_j/W}$ and the generalized random graph of Britton, Deijfen and Martin-Löf uses $w_i w_j/(W + w_i w_j)$. Both are always valid probabilities, and they agree with Chung-Lu when $w_i w_j \ll W$.
- **Modularity.** The term $k_i k_j / (2m)$ in [modularity](/modularity/) is the Chung-Lu probability with the observed degrees as weights and $W = 2m$.
- **Block models.** A degree-corrected [stochastic block model](/stochastic-block-model/) with one block is the Chung-Lu model; with several blocks it adds community structure.
- **Growth models.** The [Barabási-Albert model](/barabasi-albert-model/) produces power-law degrees by a growth process with dependences between edges; a Chung-Lu graph with the same degree tail is a static version with independent edges.

## Known results in the model

These are the main results of Chung and Lu, stated loosely; the papers give the exact conditions on the weights.

**Giant component.** If $\tilde d < 1$, then a.a.s. all components are small, with volume, the sum of the weights, at most of order $\sqrt n \log n$. If the average weight $d > 1$, then a.a.s. there is a unique giant component of linear volume, and the second largest component has order $\log n$ vertices. For $w_i = c$, both conditions reduce to the threshold $c = 1$ of the [giant component theorem](/erdos-renyi-giant-component-theorem/). For heavy-tailed weights $\tilde d$ is much larger than $d$, which is why a power-law graph can have a giant component with a small average degree.

**Distances.** If $\tilde d > 1$ and the weights satisfy some regularity conditions, the average distance between vertices of the giant component is $(1 + o(1)) \ln n / \ln \tilde d$. For power-law weights with exponent $2 < \tau < 3$, the average distance is of order $\ln \ln n$, much shorter than in [small-world networks](/small-world-network/) with light tails; for $\tau > 3$ it is of order $\ln n$.

**Spectrum.** The largest eigenvalue of the adjacency matrix is about $\max(\tilde d, \sqrt{\max_i w_i})$ under suitable conditions, which separates the regime where the hubs dominate from the one where the average structure does.

## References
