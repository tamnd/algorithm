---
tag: VSJF1S
kind: problem
slug: spatial-search
name: Spatial search
aliases:
- quantum search on graphs
- finding a marked vertex
area: quantum/quantum-search
level: advanced
summary: "Find a marked vertex of a graph when the search moves only along edges. Quantum walks need Θ(sqrt(N)) steps on the hypercube and grids of dimension 3 or more, O(sqrt(N log N)) on the 2D grid."
prereqs: [unstructured-search, walk, markov-chain, quantum-query-model]
see_also: [quantum-walk-search, grover-search, grover-optimality, quantum-query-complexity, spectral-gap, ambainis-element-distinctness, triangle-finding, quantum-random-access-memory]
sources:
  - paper: doi:10.4086/toc.2005.v001a004
    title: "Scott Aaronson and Andris Ambainis, Quantum search of spatial regions, Theory of Computing 1, 2005, pages 47-79"
    locator: with the numbering of arXiv:quant-ph/0303041, the abstract and the model section (the query model on graphs with local moves; O(sqrt(N)) on grids of dimension 3 or more, O(sqrt(N) log^(3/2) N) in dimension 2, and the O(sqrt(N))-qubit protocol for disjointness)
  - paper: doi:10.1103/PhysRevA.67.052307
    title: "Neil Shenvi, Julia Kempe and K. Birgitta Whaley, Quantum random-walk search algorithm, Physical Review A 67, 052307, 2003"
    locator: the main result (a coined walk finds a marked vertex of the n-dimensional hypercube in O(sqrt(N)) steps); a general locator
  - paper: doi:10.1103/PhysRevA.70.022314
    title: "Andrew M. Childs and Jeffrey Goldstone, Spatial search by quantum walk, Physical Review A 70, 022314, 2004"
    locator: the abstract (continuous-time search with full speedup on the complete graph, the hypercube and lattices of dimension above 4, a polylogarithmic loss in dimension 4, and no substantial speedup below 4)
  - paper: arxiv:quant-ph/0402107
    title: "Andris Ambainis, Julia Kempe and Alexander Rivosh, Coins make quantum walks faster, Proceedings of the 16th ACM-SIAM SODA, 2005, pages 1099-1108"
    locator: the abstract (O(sqrt(N) log N) on the 2D grid and O(sqrt(N)) in dimension 3 or more, with a coined discrete-time walk)
  - paper: doi:10.1103/PhysRevA.78.012310
    title: "Avatar Tulsi, Faster quantum-walk algorithm for the two-dimensional spatial search, Physical Review A 78, 012310, 2008"
    locator: the abstract (O(sqrt(N log N)) steps on the 2D grid with one extra control qubit), arXiv:0801.0497
  - paper: doi:10.1137/S0097539796300933
    title: "Charles H. Bennett, Ethan Bernstein, Gilles Brassard and Umesh Vazirani, Strengths and weaknesses of quantum computing, SIAM Journal on Computing 26(5), 1997, pages 1510-1523"
    locator: the lower bound Omega(sqrt(N)) for unstructured search, which holds on every graph
  - paper: doi:10.1109/FOCS.2004.53
    title: "Mario Szegedy, Quantum speed-up of Markov chain based algorithms, Proceedings of the 45th IEEE FOCS, 2004, pages 32-41"
    locator: the whole paper (detection of a marked set with the square root of the classical hitting time, for symmetric chains)
  - paper: doi:10.1137/090745854
    title: "Frédéric Magniez, Ashwin Nayak, Jérémie Roland and Miklos Santha, Search via quantum walk, SIAM Journal on Computing 40(1), 2011, pages 142-164"
    locator: with the numbering of arXiv:quant-ph/0608026, Theorem 3 (the cost S + (1/sqrt(eps))(U/sqrt(delta) + C)) and Section 1.5 (the history of grid search)
  - paper: arxiv:1002.2419
    title: "Hari Krovi, Frédéric Magniez, Maris Ozols and Jérémie Roland, Quantum walks can find a marked element on any graph, Algorithmica 74(2), 2016"
    locator: the main theorem (finding one marked vertex in the square root of the extended hitting time); a general locator
  - paper: doi:10.1145/3357713.3384252
    title: "Andris Ambainis, András Gilyén, Stacey Jeffery and Martins Kokainis, Quadratic speedup for finding marked vertices by quantum walks, Proceedings of the 52nd ACM STOC, 2020, pages 412-424"
    locator: the main theorem (finding in the square root of the hitting time, up to a logarithmic factor, for any reversible chain and any marked set)
---

Spatial search asks for a marked vertex of a graph when the search can only move along the edges of the graph and look at the vertex where it is. It is [unstructured search](/unstructured-search/) with a locality rule. On the complete graph the rule has no effect and [Grover search](/grover-search/) needs $\Theta(\sqrt{N})$ steps. On the hypercube and on grids of dimension $d \ge 3$, quantum walks also reach $\Theta(\sqrt{N})$. On the two-dimensional grid the best known bound is $O(\sqrt{N \log N})$, and a classical random walk needs $\Theta(N \log N)$ steps there. This page is the problem; the general algorithm is [quantum walk search](/quantum-walk-search/), which finds a marked state of a [Markov chain](/markov-chain/) with about the square root of the classical cost.

## In plain words

A robot moves on a map of rooms joined by doors and looks for a room with a prize. It can only see the room it is in, and each move goes through one door. A normal robot must visit almost every room. A quantum robot can be in many rooms at once, as a wave, and it can look in all of them in one step. Grover's method needs far fewer looks than the number of rooms, but it needs to jump between any two rooms. If every jump must walk through doors, the long walks can use up the gain. Quantum walks keep most of the gain on maps where the rooms are well connected. On a flat square map they lose only a small extra factor. On a long corridor there is no gain, because the robot must still walk to the far end.

## Definition

**Input.** A connected undirected graph $G = (V, E)$ with $N$ vertices, known in advance, and an unknown set $M \subseteq V$ of marked vertices. The marking is given by a phase oracle $O_M|v\rangle = (-1)^{[v \in M]}|v\rangle$, which acts on the vertex register. The bit form $|v\rangle|b\rangle \mapsto |v\rangle|b \oplus [v \in M]\rangle$ is equivalent, with one call, by [phase kickback](/phase-kickback/).

**Locality.** The state lives in the span of $|v\rangle|z\rangle$, where $v$ is the current vertex and $z$ is a local work register, for example a coin that names an edge. One step is either a call of the oracle at the current vertex, or a local unitary that maps $|v\rangle|z\rangle$ into the span of the states $|w\rangle|z'\rangle$ with $w = v$ or $\{v, w\} \in E$. The unitaries can depend on $G$ but not on $M$. This is the model of Aaronson and Ambainis. In the continuous-time form the state evolves under a Hamiltonian $-\gamma L - \sum_{m \in M}|m\rangle\langle m|$, where $L$ is the Laplacian of $G$, and the cost is the evolution time.

**Output.** A vertex of $M$, or "none" if $M$ is empty. The decision version only asks whether $M$ is empty.

**Cost.** The number of steps, oracle calls and local moves together, with bounded error (success probability at least $2/3$). The usual case has one marked vertex, or $|M| = k$ with $k$ known.

The step count of this model is a time bound for a machine that stores the data in space and moves between them. It is not the same as the query count of the [quantum query model](/quantum-query-model/), where a query reads any position at unit cost; that cost is a time bound only with [quantum random access memory](/quantum-random-access-memory/).

## Variants

- **Markov chain form.** In place of a graph, take a reversible ergodic chain $P$ with stationary distribution $\pi$ and spectral gap $\delta$, and count three costs: $S$ to prepare $\pi$, $U$ for one step of $P$ and $C$ to check a state. A marked set has $\pi(M) \ge \varepsilon$. This is the form of the general algorithms, and the graph form is the simple random walk on $G$.
- **Detection versus finding.** For one marked vertex the two are almost the same. For several marked vertices, detection was solved first (Szegedy, 2004), and finding with the square root of the hitting time came later (Ambainis, Gilyén, Jeffery and Kokainis, 2020).
- **Discrete versus continuous time.** The continuous-time walk of Childs and Goldstone gives no substantial gain on lattices of dimension below 4. The discrete-time walk of Ambainis, Kempe and Rivosh uses a coin register, which names an edge, and it gives the gain in dimensions 2 and 3.
- **Search on implicit graphs.** The vertices can be large objects, such as the $r$-element subsets of an input in the Johnson graph. Then $N$ is the number of objects and a step is an update of the data stored with a vertex.

## Examples

- **The complete graph on $N = 8$ vertices.** Every vertex is next to every other one, so locality costs nothing. With one marked vertex, two Grover iterations find it with probability $\sin^2(5\arcsin\sqrt{1/8}) \approx 0.945$.
- **The cycle on $N$ vertices.** Start at vertex 0 and mark vertex $N/2$. Each step moves amplitude by at most one edge, so after fewer than $N/2$ steps the state has no amplitude on vertex $N/2$, and the state is the same whether or not it is marked. So every algorithm needs $\Omega(N)$ steps, and the quantum gain is lost.
- **The $\sqrt{N} \times \sqrt{N}$ grid with wrap-around**, for example $1000 \times 1000$ with $N = 10^6$. A classical random walk from a random vertex needs $\Theta(N \log N)$ steps on average to hit one marked vertex, and a systematic scan needs $N$ steps. A quantum walk needs $O(\sqrt{N \log N})$ steps, on the order of $\sqrt{10^6 \cdot 14} \approx 3700$ up to a constant factor.

## Known algorithms

| graph | steps | method |
|---|---|---|
| complete graph | $\Theta(\sqrt{N})$ | [Grover search](/grover-search/) |
| hypercube $\{0,1\}^n$, $N = 2^n$ | $O(\sqrt{N})$ | coined walk of Shenvi, Kempe and Whaley (2003) |
| grid of dimension $d \ge 3$ | $O(\sqrt{N})$ | recursive search of Aaronson and Ambainis (2003); coined walk of Ambainis, Kempe and Rivosh (2005) |
| 2D grid | $O(\sqrt{N}\log^{3/2} N)$ | Aaronson and Ambainis |
| 2D grid | $O(\sqrt{N}\log N)$ | Ambainis, Kempe and Rivosh |
| 2D grid | $O(\sqrt{N \log N})$ | Tulsi (2008), with one extra control qubit |
| lattice of dimension $d > 4$ | $O(\sqrt{N})$ time | continuous-time walk of Childs and Goldstone (2004); dimension 4 loses a polylogarithmic factor |
| any reversible chain | $O(S + (1/\sqrt{\varepsilon})(U/\sqrt{\delta} + C))$ | [quantum walk search](/quantum-walk-search/) of Magniez, Nayak, Roland and Santha |
| any reversible chain | about $\sqrt{HT}$ | Szegedy (detection); Krovi, Magniez, Ozols and Roland (one marked vertex); Ambainis, Gilyén, Jeffery and Kokainis (any marked set, up to a logarithmic factor) |

Here $HT$ is the hitting time of the classical walk to the marked set. All entries are bounded-error step counts. The square root of the hitting time matches the grid results: on the 2D grid $HT = \Theta(N \log N)$, and $\sqrt{HT} = \Theta(\sqrt{N \log N})$.

## Bounds

| bound | source | model and error |
|---|---|---|
| $\Omega(\sqrt{N})$ on every graph | [Grover optimality](/grover-optimality/) (Bennett, Bernstein, Brassard and Vazirani) | quantum, bounded error; holds already without locality |
| $\Omega(D)$, $D$ the distance from the start to the farthest vertex | locality, as in the cycle example | any algorithm that starts at one vertex |
| $\Theta(N)$ | a walk along a spanning tree visits every vertex in $2(N - 1)$ moves | classical, deterministic |
| $\Theta(HT)$ for a random walk | the definition of the hitting time | classical random walk |

The lower bound $\Omega(\sqrt{N})$ is reached on the complete graph, the hypercube and grids of dimension $d \ge 3$. On the 2D grid the best upper bound in the table is $O(\sqrt{N \log N})$, a factor $\sqrt{\log N}$ above it. On the cycle and the path the bound $\Omega(D) = \Omega(N)$ shows that there is no quantum gain. The [quantum query complexity](/quantum-query-complexity/) of plain search, $\Theta(\sqrt{N})$, is the limit for every graph.

## Reductions

- **Unstructured search** is spatial search on the complete graph with loops; one step of the walk is the [Grover diffusion operator](/grover-diffusion-operator/).
- **Element distinctness, triangle finding and $k$-distinctness** reduce to search on the Johnson graph of $r$-element subsets of the input, where a subset is marked when it contains a solution; see [Ambainis element distinctness](/ambainis-element-distinctness/) and [triangle finding](/triangle-finding/).
- **Spatial search to a classical walk.** Any classical random walk search with hitting time $HT$ gives a quantum walk search with about $\sqrt{HT}$ steps, by the results in the last row of the table.

## Applications

- **Physical search.** A quantum computer whose memory is laid out in space, with only nearest-neighbor operations, must pay for the moves. The grid results show that a square-root gain survives in dimension 3 and, up to a logarithmic factor, in dimension 2.
- **Communication complexity.** Aaronson and Ambainis used search on a grid to get a protocol for set disjointness with $O(\sqrt{n})$ qubits of communication.
- **Quantum walk algorithms.** The Markov chain form is the base of the walk algorithms for element distinctness, triangle finding and other subgraph searches, and of their time-efficient versions.

## References
