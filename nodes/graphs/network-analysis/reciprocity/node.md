---
tag: MN0WPB
kind: definition
slug: reciprocity
name: Reciprocity
aliases:
- mutuality
area: graphs/network-analysis
level: intro
summary: Fraction of directed edges whose reverse edge also exists.
prereqs: [directed-graph, in-degree-and-out-degree]
see_also: [triadic-closure, assortativity, clustering-coefficient, degree-distribution, erdos-renyi-model, configuration-model]
sources:
  - book: isbn:9780199206650
    title: M. E. J. Newman, Networks, An Introduction, Oxford University Press, 2010
    locator: Chapter 7, Measures and metrics (the section on reciprocity)
  - book: isbn:9780521387071
    title: Stanley Wasserman and Katherine Faust, Social Network Analysis, Methods and Applications, Cambridge University Press, 1994
    locator: Chapter 13, Dyads and triads (the dyad census with mutual, asymmetric and null dyads, and indices of mutuality)
  - paper: doi:10.1103/PhysRevLett.93.268701
    title: Diego Garlaschelli and Maria I. Loffredo, Patterns of link reciprocity in directed networks, Physical Review Letters 93, 268701 (2004)
    locator: the definition of the coefficient rho, which compares r with the density of the graph
---

Reciprocity is the fraction of the arcs of a [directed graph](/directed-graph/) whose reverse arc is also present. If $u$ links to $v$, it asks how often $v$ links back to $u$. It is a basic statistic of social and communication networks: friendship nominations, e-mail and follower graphs have high reciprocity, while citation graphs and food webs have almost none.

## Definition

Let $G = (V, E)$ be a simple directed graph with $n = |V|$ vertices and $m = |E|$ arcs, without self-loops. The arcs have no weights. An arc $(u, v) \in E$ is *reciprocated* when $(v, u) \in E$ as well. The **reciprocity** of $G$ is

$$r = \frac{\bigl|\{(u, v) \in E : (v, u) \in E\}\bigr|}{m} = \frac{1}{m} \sum_{u \ne v} A_{uv} A_{vu},$$

where $A$ is the [adjacency matrix](/adjacency-matrix/). It is defined only when $m \ge 1$. So $0 \le r \le 1$, with $r = 1$ exactly when every arc has its reverse (the graph is an undirected graph seen as directed) and $r = 0$ exactly when no pair of vertices has arcs both ways. The sum $\sum_{u \ne v} A_{uv} A_{vu} = \operatorname{tr}(A^2)$ when there are no self-loops, so $r = \operatorname{tr}(A^2)/m$.

**Dyad census.** Each unordered pair $\{u, v\}$ of distinct vertices is a *dyad*. It is *mutual* when both arcs exist, *asymmetric* when exactly one exists, and *null* when neither exists. With $M$, $A_s$ and $N$ the numbers of each kind,

$$M + A_s + N = \binom{n}{2}, \qquad m = 2M + A_s, \qquad r = \frac{2M}{2M + A_s}.$$

Some authors report the dyad fraction $M/(M + A_s)$ instead of $r$. It counts connected pairs and not arcs, and it is smaller than $r$ whenever $0 < M$ and $0 < A_s$, so a report must say which one it uses.

**Corrected reciprocity.** A dense graph has many reciprocated arcs by chance alone. In a random directed graph with the same density $\bar a = m / (n(n-1))$, each reverse arc is present with probability about $\bar a$, so $r \approx \bar a$. Garlaschelli and Loffredo define

$$\rho = \frac{r - \bar a}{1 - \bar a}.$$

It is the Pearson correlation coefficient of the entries $A_{uv}$ and $A_{vu}$ over the ordered pairs $u \ne v$. So $\rho > 0$ means more mutual arcs than chance, $\rho = 0$ means as many as chance, and $\rho < 0$ means fewer (antireciprocal). It is defined for $0 < \bar a < 1$.

**Weights, ties and disconnected graphs.** The definition counts arcs, not weights. Weighted versions exist (for example, $\sum_{u \ne v} \min(w_{uv}, w_{vu}) / \sum_{u \ne v} w_{uv}$), but they are a different number. There are no ties to break. The statistic is a sum over all arcs, so a disconnected graph needs no special case: each component adds its own arcs to the numerator and to the denominator. Self-loops are left out, because the reverse of a loop is the loop itself.

**Cost.** With adjacency lists and a [hash table](/hash-table/) of the arcs, $r$ takes $O(n + m)$ expected time: for each arc $(u, v)$, look up $(v, u)$.

## Examples and non-examples

**A worked example.** Take the vertices $a, b, c, d, e$ and the 8 arcs $a \to b$, $b \to a$, $b \to c$, $c \to b$, $c \to d$, $d \to a$, $a \to c$, $e \to a$.

| dyad kind | the dyads | count |
|---|---|---|
| mutual | $\{a, b\}$, $\{b, c\}$ | $M = 2$ |
| asymmetric | $\{c, d\}$, $\{a, d\}$, $\{a, c\}$, $\{a, e\}$ | $A_s = 4$ |
| null | $\{b, d\}$, $\{b, e\}$, $\{c, e\}$, $\{d, e\}$ | $N = 4$ |

The 4 arcs of the two mutual dyads are reciprocated, so $r = 4/8 = 0.5$. The dyad fraction is $2/6 = 1/3$. The density is $\bar a = 8/20 = 0.4$, so $\rho = (0.5 - 0.4)/(1 - 0.4) = 1/6 \approx 0.167$. The graph has a little more reciprocity than a random graph of the same density.

**Standard cases.**

- An undirected graph, stored as a directed graph with both arcs of each edge, has $r = 1$.
- A [directed acyclic graph](/directed-acyclic-graph/) has $r = 0$, because a mutual pair is a cycle of length 2. Citation networks are close to this case.
- A tournament (exactly one arc in each pair) has $r = 0$ and $\bar a = 1/2$, so $\rho = -1$: it is as antireciprocal as possible.
- In the directed [Erdős-Rényi model](/erdos-renyi-model/), where each ordered pair is an arc with probability $p$ on its own, the expected number of reciprocated arcs is $n(n-1)p^2$ and the expected number of arcs is $n(n-1)p$, so $r \approx p$ and $\rho \approx 0$.

**Non-examples.**

- The density $m / (n(n-1))$ is not a reciprocity. A complete directed graph has density 1, and one mutual pair with many isolated vertices has density near 0, yet both have $r = 1$.
- The [clustering coefficient](/clustering-coefficient/) is not a reciprocity. It counts closed triangles, and a cycle of length 2 is not a triangle.
- A high in-degree of $v$ does not mean that $v$ reciprocates. A celebrity in a follower graph has a high in-degree and a low fraction of reciprocated arcs.

## Related definitions

- [In-degree and out-degree](/in-degree-and-out-degree/): the mutual arcs at $v$ are at most $\min(\deg^-(v), \deg^+(v))$.
- [Triadic closure](/triadic-closure/): the analogue of reciprocity for three vertices, studied with the triad census.
- [Assortativity](/assortativity/): another correlation coefficient over the edges of a graph.
- [Configuration model](/configuration-model/): the null model to use when the degrees, and not only the density, must be kept.
- [Clustering coefficient](/clustering-coefficient/): the fraction of closed paths of length 2 in an undirected graph.

## References
