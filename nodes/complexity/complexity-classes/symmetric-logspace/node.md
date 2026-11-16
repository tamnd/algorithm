---
tag: 2KCENG
kind: definition
slug: symmetric-logspace
name: SL (SLOGSPACE)
aliases:
- SL
area: complexity/complexity-classes
level: advanced
summary: The problems that a symmetric nondeterministic machine decides in logarithmic space, or that reduce in logspace to undirected reachability. Reingold proved SL = L.
prereqs: [nondeterministic-logspace, logspace]
see_also: [randomized-logspace, graph-reachability, connected-components, bipartiteness-testing, rl-versus-l, savitch-theorem, immerman-szelepcsenyi-theorem, nondeterministic-turing-machine]
sources:
  - paper: doi:10.1016/0304-3975(82)90058-5
    title: Harry R. Lewis and Christos H. Papadimitriou, Symmetric space-bounded computation, Theoretical Computer Science 19(2), 161 to 187 (1982)
    locator: the symmetric Turing machine, the class SL and the completeness of undirected reachability
  - paper: doi:10.1109/SFCS.1979.34
    title: Romas Aleliunas, Richard M. Karp, Richard J. Lipton, László Lovász and Charles Rackoff, Random walks, universal traversal sequences, and the complexity of maze problems, 20th Annual Symposium on Foundations of Computer Science, 218 to 223 (1979)
    locator: the cover time bound 2|E|(n-1) and the randomized logspace algorithm for undirected reachability
  - paper: doi:10.1145/225058.225101
    title: Noam Nisan and Amnon Ta-Shma, Symmetric logspace is closed under complement, 27th Annual ACM Symposium on Theory of Computing, 140 to 146 (1995)
    locator: SL = coSL
  - paper: doi:10.1145/1391289.1391291
    title: Omer Reingold, Undirected connectivity in log-space, Journal of the ACM 55(4), article 17 (2008)
    locator: the main theorem, undirected reachability in L, and the corollary SL = L
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 21, the deterministic logspace algorithm for undirected connectivity
---

SL, also written SLOGSPACE, is the class of decision problems that a *symmetric* nondeterministic Turing machine decides in space $O(\log n)$. A symmetric machine is one in which every move can be undone by a reverse move, so its configuration graph is undirected. Lewis and Papadimitriou defined the class in 1982 to capture the complexity of undirected reachability, which is complete for it: SL is also the class of problems that reduce to undirected reachability by logspace reductions. Clearly $\mathsf{L} \subseteq \mathsf{SL} \subseteq \mathsf{NL}$. In 2005 Omer Reingold gave a deterministic logspace algorithm for undirected reachability, so $\mathsf{SL} = \mathsf{L}$. The class is still the natural home for problems on undirected graphs, and its history shows how a randomized algorithm was turned into a deterministic one.

## Definition

**Undirected reachability.** USTCON is the language of triples $\langle G, s, t \rangle$ where $G$ is an undirected graph and $s$ and $t$ are in the same connected component of $G$. Compare the directed version PATH, which is complete for NL; see [graph reachability](/graph-reachability/).

**Symmetric machines.** The model is the nondeterministic multitape Turing machine with a read-only input tape, and only the work tapes count; see [NL](/nondeterministic-logspace/). Lewis and Papadimitriou write each transition as a pair of local views, before and after the move, and call the machine *symmetric* if, for every transition, the reverse transition is also in the table. The reverse transition undoes the move: it returns to the old state, restores the old symbols and moves the heads back. So whenever a configuration $C'$ follows from $C$ in one step, $C$ also follows from $C'$ in one step, and the configuration graph of the machine on an input $x$ is in effect undirected.

**Definition.** $\mathsf{SL}$ is the class of languages $A$ for which a symmetric nondeterministic machine with $O(\log n)$ work space accepts exactly the strings in $A$. As for NL, the machine accepts $x$ if some computation from the start configuration reaches an accepting configuration.

**Completeness.** USTCON is SL-complete under logspace reductions (Lewis and Papadimitriou 1982). It is in SL: a symmetric machine walks from $s$ along guessed edges, keeping only the current vertex, and a step from $u$ to $v$ along an undirected edge can always be undone by a step from $v$ to $u$. Every $A \in \mathsf{SL}$ reduces to it: on input $x$, a logspace transducer writes the configuration graph of the symmetric machine on $x$, with the start configuration and a single accepting configuration as $s$ and $t$. That graph is undirected because the machine is symmetric. So an equivalent definition is

$$\mathsf{SL} = \{A : A \le_{\mathrm{L}} \mathrm{USTCON}\}.$$

**Why L is inside SL.** Let $M$ be a deterministic logspace machine that halts, with a single accepting configuration. Its configuration graph has out-degree at most 1 and no directed cycles. Forget the directions. In a graph of this kind each connected component contains exactly one vertex of out-degree 0, the halting configuration that every vertex of the component leads to. So the start configuration and the accepting configuration are in the same component if and only if the run of $M$ accepts. This reduces every language in L to USTCON in logspace.

**Where SL sits.**

- $\mathsf{L} \subseteq \mathsf{SL} \subseteq \mathsf{NL}$, since a symmetric machine is a special nondeterministic machine.
- $\mathsf{SL} \subseteq \mathsf{RL}$. Aleliunas, Karp, Lipton, Lovász and Rackoff (1979) proved that a random walk on a connected graph with $n$ vertices and $|E|$ edges visits every vertex within $2|E|(n-1)$ expected steps. A walk of $4|E|(n-1)$ steps from $s$ therefore meets $t$ with probability at least $1/2$ when $t$ is in the component of $s$, by Markov's inequality, and it never meets $t$ otherwise. The walk keeps the current vertex and a step counter. See [RL](/randomized-logspace/).
- $\mathsf{SL} = \mathsf{coSL}$ (Nisan and Ta-Shma 1995). Before Reingold, this was the main structural fact about the class.
- Space bounds before Reingold. Savitch's theorem gives $O(\log^2 n)$ space for USTCON, as for PATH. Nisan, Szemerédi and Wigderson (1992) reached $O(\log^{3/2} n)$ space, and Armoni, Ta-Shma, Wigderson and Zhou (2000) reached $O(\log^{4/3} n)$.
- $\mathsf{SL} = \mathsf{L}$ (Reingold 2005; journal version 2008).

**Reingold's theorem.** Undirected reachability is in L, so $\mathsf{SL} = \mathsf{L}$. The proof starts from the fact that on a graph of constant degree with diameter $O(\log n)$, a deterministic machine can try every path of length $O(\log n)$ from $s$: such a path is a list of $O(\log n)$ edge labels, each from a constant range, so it fits in $O(\log n)$ bits. Reingold transforms each connected component into a graph of this kind, an expander, without changing which pairs of vertices are connected. First every vertex is replaced by a cycle, so that all degrees are equal to a constant. Then $O(\log n)$ rounds follow. Each round raises the graph to a constant power, which improves its expansion but increases the degree, and then takes the zig-zag product with a fixed small expander, which brings the degree back to a constant and loses only a constant factor of the expansion. After $O(\log n)$ rounds each component is an expander with logarithmic diameter. The final graph is never written down: a neighbor of a vertex in the round-$i$ graph is computed from neighbors in the round-$(i-1)$ graph, with a constant number of extra bits per round, so the whole recursion uses $O(\log n)$ bits.

## Examples and non-examples

**Bipartiteness.** A graph $G$ is bipartite if and only if it has no odd cycle. Form the *double cover* $G \times K_2$: its vertices are the pairs $(v, b)$ with $b \in \{0, 1\}$, and each edge $\{u, v\}$ of $G$ gives the two edges $\{(u, 0), (v, 1)\}$ and $\{(u, 1), (v, 0)\}$. A path in the double cover from $(v, 0)$ to $(v, 1)$ projects to a closed walk of odd length through $v$, and $G$ has such a walk if and only if it has an odd cycle. So $G$ is bipartite if and only if, for every vertex $v$, the vertices $(v, 0)$ and $(v, 1)$ are not connected. For the 5-cycle $C_5$ the double cover has 10 vertices and 10 edges and is a single cycle of length 10, so $(0, 0)$ and $(0, 1)$ are connected and $C_5$ is not bipartite. For the 6-cycle $C_6$ the double cover has 12 vertices and 12 edges and splits into two cycles of length 6, so $(0, 0)$ and $(0, 1)$ are not connected, and $C_6$ is bipartite. The test is a logspace loop over $v$ with one USTCON question each. So bipartiteness is in $\mathsf{L}^{\mathsf{SL}}$, logspace with an oracle for USTCON, and it is in L by Reingold. See [bipartiteness testing](/bipartiteness-testing/) for the linear-time algorithm.

**Cycle detection in undirected graphs.** An edge $\{u, v\}$ lies on a cycle if and only if $u$ and $v$ are still connected after the edge is deleted. The graph with one edge deleted is logspace computable, so whether an undirected graph has a cycle is again a logspace loop over USTCON questions. For a triangle on 0, 1 and 2 with an extra edge from 2 to 3, the edges $\{0,1\}$, $\{1,2\}$ and $\{2,0\}$ pass the test and $\{2,3\}$ does not; for the path 0, 1, 2, 3 no edge passes it.

**Connected components.** Whether a graph is connected, and the number of its components, follow in the same way: compare every pair of vertices, or count the vertices $v$ that are not connected to any smaller vertex. See [connected components](/connected-components/).

**Directed reachability (not known to be in SL).** PATH is NL-complete under logspace reductions, so PATH is in SL if and only if $\mathsf{NL} = \mathsf{SL}$, which after Reingold means $\mathsf{NL} = \mathsf{L}$. This is open. A random walk does not help in directed graphs: in the graph on $0, \ldots, n-1$ with edges $i \to i+1$ and edges $i \to 0$ for $1 \le i \le n-2$, a random walk from 0 needs 766 expected steps to reach $n - 1$ for $n = 10$ and 3145726 for $n = 22$, and for $n = 22$ it reaches $n - 1$ within $n^3 = 10648$ steps with probability only about 0.0034.

## Related definitions

- **L** is equal to SL by Reingold's theorem. See [L](/logspace/).
- **NL** is the class for directed reachability. SL is the symmetric special case. See [NL](/nondeterministic-logspace/).
- **RL** contains SL by the random walk algorithm. Whether $\mathsf{RL} = \mathsf{L}$ is open; Reingold's method is one step toward it. See [RL](/randomized-logspace/) and [RL versus L](/rl-versus-l/).
- **coSL** is the class of complements of SL languages. It equals SL by Nisan and Ta-Shma, and now also by Reingold, since L is closed under complement.
- **Universal traversal sequences.** Aleliunas and his coauthors also showed that, for every $n$ and $d$, a sequence of edge labels of polynomial length visits every vertex of every connected $d$-regular labeled graph with $n$ vertices, from any start vertex. Their proof is probabilistic and does not give an explicit sequence in logspace. Reingold's paper derives logspace-constructible universal *exploration* sequences as a corollary.

## References
