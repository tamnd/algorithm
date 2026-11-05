---
tag: EFKVZ9
kind: concept
slug: giant-component
name: Giant component
aliases:
- giant connected component
area: graphs/network-analysis
level: core
summary: Unique connected component containing a positive fraction of all nodes.
prereqs: [connected-components, erdos-renyi-model]
see_also: [erdos-renyi-giant-component-theorem, erdos-renyi-connectivity-threshold, configuration-model, percolation, strongly-connected-components, degree-distribution, sir-epidemic-model]
sources:
  - paper: "Paul Erdős and Alfréd Rényi, On the evolution of random graphs, Publications of the Mathematical Institute of the Hungarian Academy of Sciences 5, 17 to 61 (1960)"
    locator: the whole paper (the phase transition at about n/2 edges and the birth of the giant component)
  - book: isbn:9781107118508
    title: Alan Frieze and Michał Karoński, Introduction to Random Graphs, Cambridge University Press, 2016
    locator: Chapter 2, Evolution (the subcritical, critical and supercritical phases of G(n,p), and the size of the giant component)
  - paper: doi:10.1002/rsa.3240060204
    title: Michael Molloy and Bruce Reed, A critical point for random graphs with a given degree sequence, Random Structures and Algorithms 6(2-3), 161 to 180 (1995)
    locator: the main theorem (the criterion on the sum of d(d-2) times the fraction of vertices of degree d)
  - book: isbn:9780199206650
    title: M. E. J. Newman, Networks, An Introduction, Oxford University Press, 2010
    locator: Chapter 12, Random graphs (the giant component and its size), Chapter 13, Random graphs with general degree distributions (the generating function method), and Chapter 16, Percolation and network resilience
  - paper: doi:10.1016/S1389-1286(00)00083-9
    title: Andrei Broder, Ravi Kumar, Farzin Maghoul, Prabhakar Raghavan, Sridhar Rajagopalan, Raymie Stata, Andrew Tomkins and Janet Wiener, Graph structure in the Web, Computer Networks 33(1-6), 309 to 320 (2000)
    locator: the bow-tie picture of the web graph and the sizes of its parts
---

A giant component is a [connected component](/connected-components/) that holds a positive fraction of all the vertices of a graph, as the number of vertices grows. The term belongs to families of graphs, such as the [Erdős-Rényi model](/erdos-renyi-model/), where at most one such component can exist with high probability, and it appears suddenly when the mean degree passes a threshold. In a single real network, the name is given to the largest component when it holds most of the vertices and all other components are small.

## In plain words

Pour people into a city one friendship at a time, at random. At first, the friendships make many small separate groups of two or three people. Most people know nobody in other groups.

Then, quite suddenly, the small groups start to join. Once each person has on average more than one friend, one group grows to hold a large share of the whole city, while all the other groups stay tiny. This big group is the giant component. Adding more friendships makes it grow until almost everyone is in it. There is only one: two big groups would almost surely be joined by some friendship soon.

## The idea

**Definition for a family of graphs.** Let $G_n$ be a random graph on $n$ vertices for each $n$, and let $L_1(G_n) \ge L_2(G_n)$ be the sizes of its largest and second largest components. The family has a giant component when there is a constant $\theta > 0$ such that $L_1(G_n) \ge \theta n$ with probability tending to 1. In the usual models, the giant is then unique in a strong sense: $L_2(G_n) = o(n)$, and in fact $L_2(G_n) = O(\log n)$, with probability tending to 1. A single finite graph does not have a giant component in this exact sense, since "a positive fraction" needs $n \to \infty$.

**The Erdős-Rényi phase transition.** In $G(n, p)$ with $p = c/n$ and a constant $c > 0$, with probability tending to 1:

- if $c < 1$, every component has $O(\log n)$ vertices;
- if $c = 1$, the largest component has order $n^{2/3}$ vertices;
- if $c > 1$, there is a unique giant component with $(\beta(c) + o(1))\, n$ vertices, and every other component has $O(\log n)$ vertices. Here $\beta = \beta(c)$ is the unique root in $(0, 1)$ of
$$\beta = 1 - e^{-c\beta}.$$

The equation has a short reason. A vertex is outside the giant when none of its neighbours leads to the giant. Its number of neighbours is close to a Poisson variable with mean $c$, so the probability of this is $\sum_k e^{-c} \frac{c^k}{k!} (1 - \beta)^k = e^{-c\beta}$. The full statement is the [Erdős-Rényi giant component theorem](/erdos-renyi-giant-component-theorem/); the graph becomes connected only much later, at $p = \ln n / n$, the [connectivity threshold](/erdos-renyi-connectivity-threshold/).

**Given degrees: the Molloy-Reed criterion.** In the [configuration model](/configuration-model/), where a fraction $\lambda_d$ of the vertices has degree $d$, and under conditions on the maximum degree, a giant component exists with high probability when

$$\sum_{d} d(d - 2) \lambda_d > 0,$$

that is when $\mathbb{E}[D^2] > 2\,\mathbb{E}[D]$, and does not exist when the sum is negative. The reason is that the neighbour reached along a random edge has degree $d$ with probability proportional to $d \lambda_d$, and it has $d - 1$ further edges. The giant exists when this number of further edges has mean more than 1. For $G(n, c/n)$ the degrees are close to Poisson with mean $c$, so $\mathbb{E}[D^2] = c^2 + c$, and the criterion $c^2 + c > 2c$ gives $c > 1$ again.

**The size from generating functions.** Let $G_0(x) = \sum_d \lambda_d x^d$, and $G_1(x) = G_0'(x)/G_0'(1)$ for the further edges of a neighbour. Let $u$ be the smallest root in $[0, 1]$ of $u = G_1(u)$, the probability that an edge does not lead to the giant. Then the giant holds a fraction $1 - G_0(u)$ of the vertices. This is the method of Newman, Strogatz and Watts, in Chapter 13 of Newman's book.

**Directed graphs.** In a [directed graph](/directed-graph/), the giant can be weak or strong. A giant [strongly connected component](/strongly-connected-components/) comes with an *in* part, the vertices that reach it, and an *out* part, the vertices it reaches: the bow-tie of Broder and co-authors.

**Weights and ties.** Edge weights play no role; only the presence of an edge counts. When two components of a finite graph tie for the largest, the graph has no clear giant; in the models above this has probability tending to 0 above the threshold.

## Examples

**Sizes in $G(n, c/n)$.** Solving $\beta = 1 - e^{-c\beta}$ for a few mean degrees gives the share of the vertices in the giant:

| mean degree $c$ | 0.5 | 1 | 1.5 | 2 | 3 | 4 |
|---|---|---|---|---|---|---|
| $\beta(c)$ | 0 | 0 | 0.5828 | 0.7968 | 0.9405 | 0.9802 |

At $c = 2$, about 80% of the vertices lie in one component, although the graph has only about $n$ edges and many isolated vertices: a vertex has no edge with probability about $e^{-2} \approx 0.135$.

**Degrees 1 and 3.** Let half of the vertices have degree 1 and half degree 3. The criterion gives $1 \cdot (-1) \cdot \tfrac12 + 3 \cdot 1 \cdot \tfrac12 = 1 > 0$, so there is a giant. With $G_0(x) = \tfrac12 x + \tfrac12 x^3$, $G_0'(1) = 2$ and $G_1(u) = \tfrac14 + \tfrac34 u^2$. The equation $u = \tfrac14 + \tfrac34 u^2$ has the roots $\tfrac13$ and $1$, so $u = \tfrac13$, and the giant holds $1 - G_0(\tfrac13) = 1 - \tfrac16 - \tfrac1{54} = \tfrac{22}{27} \approx 0.815$ of the vertices.

**Degrees 1 and 2 only.** If all degrees are 1 or 2, then $d(d-2) \le 0$ for each $d$ that occurs, and the sum is negative as soon as some vertex has degree 1. Such a graph is a union of paths and cycles, and no giant appears. With all degrees 2, the sum is 0, the critical case, and the graph is a union of cycles.

**The web graph.** In the crawl of about 203 million pages studied by Broder and co-authors, the giant strongly connected component held about 56 million pages, and the *in* and *out* parts held about 43 million each. Most pages were in the weak giant component, but less than a third were in the strong one.

## Where it is used

- The [Erdős-Rényi model](/erdos-renyi-model/) and the [configuration model](/configuration-model/): the giant is their best-known phase transition.
- [Percolation](/percolation/) on networks: removing vertices or edges at random until the giant disappears measures how robust a network is. Networks with a heavy-tailed [degree distribution](/degree-distribution/) keep their giant under random removal of most vertices, since $\mathbb{E}[D^2]$ is large, but lose it fast when the vertices of highest degree are removed first.
- Epidemics: in the [SIR model](/sir-epidemic-model/), a large outbreak happens exactly when the graph of transmitting contacts has a giant component, and the expected outbreak size is the size of that giant.
- Data analysis: many network statistics, such as the [effective diameter](/effective-diameter/) or [closeness centrality](/closeness-centrality/), are computed on the largest component only, after the [connected components](/connected-components/) are found in linear time.

## References
