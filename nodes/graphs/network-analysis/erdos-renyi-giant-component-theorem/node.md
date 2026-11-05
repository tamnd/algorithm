---
tag: 81EC6M
kind: theorem
slug: erdos-renyi-giant-component-theorem
name: Erdős-Rényi giant component theorem
aliases:
- phase transition in G(n,p)
area: graphs/network-analysis
level: advanced
summary: For average degree above 1 a giant component emerges; below 1 all components are small.
prereqs: [erdos-renyi-model, chernoff-bound, connected-components, breadth-first-search]
see_also: [giant-component, erdos-renyi-model, erdos-renyi-connectivity-threshold, configuration-model, chung-lu-model, percolation, poisson-distribution, connected-components]
sources:
  - paper: "Paul Erdős and Alfréd Rényi, On the evolution of random graphs, Publications of the Mathematical Institute of the Hungarian Academy of Sciences 5, 17 to 61 (1960)"
    locator: the whole paper (the phase transition at M = n/2 edges, components of order log n below it, and one component of linear order above it)
  - book: isbn:9781107118508
    title: Alan Frieze and Michał Karoński, Introduction to Random Graphs, Cambridge University Press, 2016
    locator: Chapter 2, Evolution (the subcritical phase, the supercritical phase with the giant component of size about βn, and the phase transition)
  - book: isbn:9780521797221
    title: Béla Bollobás, Random Graphs, second edition, Cambridge University Press, 2001
    locator: Chapter 5, The evolution of random graphs, and Chapter 6, The giant component
  - book: isbn:9780471175414
    title: Svante Janson, Tomasz Łuczak and Andrzej Ruciński, Random Graphs, Wiley, 2000
    locator: Chapter 5, The phase transition (the subcritical, critical and supercritical phases, and the critical window of width n^(-1/3))
---

The giant component theorem describes the phase transition of the [Erdős-Rényi model](/erdos-renyi-model/) $G(n, p)$ with $p = c/n$, where $c$ is the mean degree. If $c < 1$, all [connected components](/connected-components/) have $O(\log n)$ vertices. If $c > 1$, one component, the [giant component](/giant-component/), has about $\beta n$ vertices, where $\beta$ is the positive root of $\beta = 1 - e^{-c\beta}$, and all other components have $O(\log n)$ vertices. So the largest component jumps from logarithmic to linear size as the mean degree passes 1. Erdős and Rényi found this transition in 1960; it is the model case of a phase transition in a random structure, and of [percolation](/percolation/) on the complete graph.

## Statement

Let $G(n, p)$ be the random simple graph on $n$ labelled vertices in which each pair is an edge with probability $p$, independently. Let $L_1$ and $L_2$ be the numbers of vertices of its largest and second largest components. An event holds *asymptotically almost surely* (a.a.s.) if its probability tends to 1 as $n \to \infty$. Fix a constant $c > 0$ and let $p = c/n$.

**Theorem.**

1. **Subcritical.** If $c < 1$, then a.a.s. $L_1 \le \bigl\lceil \frac{4}{(1 - c)^2} \ln n \bigr\rceil$.
2. **Supercritical.** If $c > 1$, let $\beta \in (0, 1)$ be the unique positive solution of $\beta = 1 - e^{-c\beta}$. Then for every $\varepsilon > 0$, a.a.s. $|L_1 - \beta n| \le \varepsilon n$, and $L_2 = O(\ln n)$.

At $c = 1$ itself, the largest component has order $n^{2/3}$; the transition happens in a window $p = (1 + \lambda n^{-1/3})/n$ with $\lambda$ bounded.

The graph is undirected and unweighted, and it is disconnected for every constant $c$: the theorem is about the size of the largest component, not about connectivity, which needs $p$ near $\ln n/n$ (see the [connectivity threshold](/erdos-renyi-connectivity-threshold/)).

## In plain words

Join each pair among many points with a small chance, so that each point has on average a fixed number of links. Below one link per point on average, the network is a dust of small groups, the largest of them tiny compared with the whole.

Above one link per point, a single huge group suddenly holds a fixed share of all points, while the rest stay in small groups. With two links per point on average, the huge group has about four fifths of the points.

The reason is that a search outward from a point finds on average the mean degree of new points at each step. Below one it dies out quickly, above one it can grow without end.

## Proof

Part 1 is proved in full. Part 2 is given as a sketch, marked as such; a full proof is in Frieze and Karoński, Chapter 2.

**The exploration process.** Fix a vertex $v$ and find its component by a search like [breadth-first search](/breadth-first-search/). Keep a set of *active* vertices, found but not yet processed, starting with $\{v\}$, and the set of *unseen* vertices, starting with $V \setminus \{v\}$. At step $t = 1, 2, \ldots$, while some vertex is active, take an active vertex $x$, look at each pair $\{x, w\}$ with $w$ unseen, move each $w$ with an edge to the active set, and mark $x$ as processed. Let $\xi_t$ be the number of vertices found at step $t$ and $A_t$ the number of active vertices after it, so $A_0 = 1$ and

$$A_t = A_{t-1} - 1 + \xi_t.$$

The search stops at the first $T$ with $A_T = 0$, and then $T = |C(v)|$, the size of the component of $v$, since each step processes one vertex of it.

Each pair $\{x, w\}$ is looked at once at most: at the step of $x$, if $w$ is still unseen. So given the history up to step $t - 1$, the pairs looked at in step $t$ are new, and $\xi_t$ has the binomial distribution $\mathrm{Bin}(N_t, p)$ with $N_t \le n - 1$ unseen vertices. Add $n - N_t$ extra independent coins with probability $p$, and continue with fresh $\mathrm{Bin}(n, p)$ variables after the search stops. This gives independent $\xi'_t \sim \mathrm{Bin}(n, p)$ with $\xi_t \le \xi'_t$ for all $t \le T$.

**Part 1.** Let $c < 1$ and $k \ge 1$. If $|C(v)| > k$, then $T > k$, so $A_k \ge 1$, which means $\sum_{t=1}^{k} \xi_t \ge k$, and so $Z = \sum_{t=1}^{k} \xi'_t \ge k$. The sum $Z$ has the distribution $\mathrm{Bin}(kn, p)$ with mean $\mu = ck$. Write $k = (1 + \delta)\mu$ with $\delta = (1 - c)/c > 0$. The [Chernoff bound](/chernoff-bound/) $\Pr[Z \ge (1 + \delta)\mu] \le \exp\bigl(-\delta^2 \mu/(2 + \delta)\bigr)$ gives

$$\Pr[|C(v)| > k] \le \exp\Bigl(-\frac{(1 - c)^2}{c^2} \cdot \frac{ck}{(1 + c)/c}\Bigr) = \exp\Bigl(-\frac{(1 - c)^2 k}{1 + c}\Bigr) \le \exp\Bigl(-\frac{(1 - c)^2 k}{2}\Bigr).$$

Take $k = \lceil 4 \ln n/(1 - c)^2 \rceil$; the bound is at most $n^{-2}$. By the union bound over the $n$ choices of $v$, $\Pr[L_1 > k] \le n \cdot n^{-2} = 1/n \to 0$. So a.a.s. $L_1 \le k$. $\blacksquare$

**Part 2 (sketch).** Let $c > 1$.

- *The equation for $\beta$.* Let $f(x) = 1 - e^{-cx} - x$. Then $f(0) = 0$, $f'(0) = c - 1 > 0$, $f(1) = -e^{-c} < 0$, and $f$ is strictly concave, so it has exactly one root in $(0, 1)$. Here $1 - \beta$ is the probability that a Galton-Watson branching process with $\mathrm{Poisson}(c)$ children dies out: the extinction probability $q$ satisfies $q = e^{-c(1 - q)}$.
- *No middle sizes.* Take $k_- = K \ln n$ for a large constant $K$ and $k_+ = n^{2/3}$. For $k_- \le k \le k_+$, at most $k$ vertices have been seen in the first $k$ steps, so $\xi_t$ dominates $\mathrm{Bin}(n - k_+, p)$, with mean about $c > 1$. A component of size $k$ needs $A_k = 0$, that is, a sum of these with mean about $ck$ to be below $k$; a Chernoff bound makes this probability $e^{-\Omega(k)}$. So a.a.s. every component has fewer than $k_-$ or more than $k_+$ vertices.
- *Only one large component.* If two components each had more than $k_+$ vertices, then in a second round of edges added with a small probability (sprinkling), they would join with high probability; done with care, this shows that a.a.s. all vertices in large components are in one component.
- *Its size.* A vertex is in a small component with probability close to the probability that the exploration dies out early, which tends to the extinction probability $1 - \beta$ of the Poisson branching process, since $\mathrm{Bin}(n, c/n)$ tends to $\mathrm{Poisson}(c)$. So the expected number of vertices in small components is $(1 - \beta + o(1))n$. A second moment computation, with the small components of two vertices nearly independent, shows that this number is concentrated. The rest, $(\beta + o(1))n$ vertices, form the giant component, and $L_2 \le k_- = O(\ln n)$.

## Consequences

- **Mean degree 1 is critical.** A sparse random network has a component holding a fixed fraction of all vertices exactly when its mean degree is above 1. This is the reason why sparse networks with mean degree well above 1 usually have one giant component and a dust of small ones.
- **Values of $\beta$.** Iterating $\beta \leftarrow 1 - e^{-c\beta}$ from $\beta = 1$ gives $\beta \approx 0.5828$ for $c = 1.5$, $0.7968$ for $c = 2$, $0.9405$ for $c = 3$ and $0.9802$ for $c = 4$. Near the threshold, $\beta \approx 2(c - 1)$ for $c$ slightly above 1.
- **A simulation.** Three samples of $G(n, c/n)$ with $n = 100000$ gave the largest and second largest components $(26, 25)$, $(26, 22)$, $(20, 19)$ for $c = 0.5$, well below the bound $\lceil 4 \ln n/(1 - c)^2 \rceil = 185$; $(2867, 1148)$, $(804, 779)$, $(2394, 999)$ for $c = 1$, of the order $n^{2/3} \approx 2154$ and very variable; $(58869, 41)$, $(57888, 37)$, $(58271, 37)$ for $c = 1.5$, against $\beta n \approx 58280$; and $(79653, 16)$, $(79520, 20)$, $(79664, 17)$ for $c = 2$, against $\beta n \approx 79680$.
- **Duality.** For $c > 1$, the graph with the giant component removed looks like a subcritical random graph with mean degree $c' = c(1 - \beta) < 1$, where $c' e^{-c'} = c e^{-c}$.
- **Other models.** The same branching argument gives the giant component criterion $\langle k^2 \rangle > 2\langle k \rangle$ of the [configuration model](/configuration-model/) and the condition on the second-order average degree in the [Chung-Lu model](/chung-lu-model/).
- **Algorithms.** The analysis of cuckoo hashing and of some perfect hash functions rests on random graphs and hypergraphs that must stay in the subcritical phase, where all components are small.

## Tightness

The bound in Part 1 has the right order. For $c < 1$, the largest component has $(1 + o(1)) \frac{1}{\alpha}\bigl(\ln n - \frac52 \ln \ln n\bigr)$ vertices, where $\alpha = c - 1 - \ln c > 0$, so $\Theta(\log n)$ cannot be improved; the constant $4/(1 - c)^2$ is not optimal, but near $c = 1$ it has the right growth, since $\alpha \approx (1 - c)^2/2$.

The constant $c$ cannot be replaced by $1$ in either part: at $p = 1/n$ the largest component has order $n^{2/3}$, neither $O(\log n)$ nor linear. In the window $p = (1 + \lambda n^{-1/3})/n$ the sizes of the largest components, divided by $n^{2/3}$, converge to a nondegenerate limit for each fixed $\lambda$.

## History

Erdős and Rényi described the evolution of the random graph with $M$ edges in 1960, and found the "double jump" at $M = n/2$: components of order $\log n$ below it, a component of order $n^{2/3}$ at it, and one of linear order above it. Bollobás in 1984 and Łuczak in 1990 found the critical window of width $n^{-1/3}$ around $p = 1/n$. The branching process view became the standard proof, and Molloy and Reed extended the transition to random graphs with a given degree sequence in 1995.

## References
