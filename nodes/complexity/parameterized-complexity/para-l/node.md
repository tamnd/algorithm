---
tag: EMMBAS
kind: definition
slug: para-l
name: para-L
aliases:
- parameterized logspace
area: complexity/parameterized-complexity
level: research
summary: "Parameterized problems decidable in space f(k) + O(log n) for a computable f, that is, logspace after a precomputation on k. It is inside FPT; space f(k) log n gives the larger class XL."
prereqs: [logspace, fixed-parameter-tractable, space-complexity]
see_also: [logspace, nondeterministic-logspace, fixed-parameter-tractable, para-np-hardness, xp, parameterized-vertex-cover, buss-kernel, graph-reachability]
sources:
  - paper: doi:10.1007/s00453-014-9944-y
    title: "Michael Elberfeld, Christoph Stockhusen and Till Tantau, On the space and circuit complexity of parameterized problems: classes and completeness, Algorithmica 71(3), 661-701 (2015)"
    locator: the classes para-L, para-NL, XL and XNL, para-L reductions, and the complete problems for them (conference version in IPEC 2012, LNCS 7535, 206-217)
  - paper: "Liming Cai, Jianer Chen, Rodney G. Downey and Michael R. Fellows, Advice classes of parameterized tractability, Annals of Pure and Applied Logic 84(1), 119-138 (1997)"
    locator: uniform logspace with advice on the parameter, and vertex cover in this class
  - paper: "Jörg Flum and Martin Grohe, Describing parameterized complexity classes, Information and Computation 187(2), 291-319 (2003)"
    locator: the classes para-C, defined as C after a precomputation on the parameter
---

Para-L is the class of [parameterized problems](/parameterized-problem/) that a deterministic machine decides in space $f(k) + O(\log n)$, where $n$ is the input length, $k$ is the [parameter](/parameter/) and $f$ is computable. It is the parameterized form of [logarithmic space](/logspace/): the parameter may cost any amount of memory, but the input may cost only a logarithmic amount, and the two costs add. Para-L is a subset of [FPT](/fixed-parameter-tractable/), and [vertex cover](/parameterized-vertex-cover/) with the cover size as parameter is in it. Space $f(k) \cdot \log n$, where the costs multiply, gives a different and larger class, XL.

## Definition

Machines are deterministic [multitape Turing machines](/multitape-turing-machine/) with a read-only input tape. Only the cells used on the work tapes count toward the space.

**para-L.** A parameterized problem $Q \subseteq \Sigma^* \times \mathbb{N}$ is in para-L if a machine decides it in space $f(k) + O(\log |x|)$ on input $(x, k)$, for a computable $f$. Equivalently, there are a computable map $\pi$ on the parameters and a problem $R$ in L such that $(x, k) \in Q$ if and only if $(x, \pi(k)) \in R$. This is the class "L after a precomputation on the parameter" of Flum and Grohe. Cai, Chen, Downey and Fellows (1997) studied the same class as uniform logspace with advice on the parameter.

**Para-L is inside FPT.** A machine with space $s = f(k) + c \log n$ has at most $2^{O(s)} \cdot n$ configurations, which is $2^{O(f(k))} \cdot n^{O(1)}$. A deterministic machine that halts never repeats a configuration, so its time is at most this number. So $\mathsf{para\text{-}L} \subseteq \mathsf{FPT}$.

**XL.** $Q$ is in XL if a machine decides it in space $f(k) \cdot \log |x|$, that is, if each slice is in L in a uniform way. Every para-L machine fits this bound for $n \ge 2$, so $\mathsf{para\text{-}L} \subseteq \mathsf{XL}$. A machine in space $f(k) \log n$ has $n^{O(f(k))}$ configurations, so $\mathsf{XL} \subseteq \mathsf{XP}$.

**Nondeterminism.** Para-NL and XNL are the same classes with [nondeterministic](/nondeterministic-logspace/) machines. Para-NL is inside FPT as well, by deciding [reachability](/graph-reachability/) in the configuration graph.

**Para-L reductions.** A para-L reduction from $Q$ to $Q'$ is a [parameterized reduction](/parameterized-reduction/) that a machine computes in space $f(k) + O(\log |x|)$: $(x, k) \in Q$ if and only if $(x', k') \in Q'$, and $k' \le g(k)$. Para-L is closed under them. Inside FPT, ordinary parameterized reductions are too strong, because they may run any FPT computation, so completeness for para-NL and similar classes is defined with para-L reductions.

## Examples and non-examples

**Vertex cover is in para-L.** Take a graph with $n$ vertices, given by an edge list, and the parameter $k$. The algorithm follows the [Buss kernel](/buss-kernel/), without writing the kernel down:

1. A vertex of degree more than $k$ is in every cover of size at most $k$. The machine counts the degree of a vertex in $O(\log n)$ space, and it counts these vertices, $h$ of them. If $h > k$, it rejects. Otherwise $k' = k - h$.
2. The other vertices that still have an uncovered edge form the kernel. Each has degree at most $k$, so $k'$ of them cover at most $k' k$ edges. If more edges remain, the machine rejects.
3. Otherwise the kernel has at most $2k^2$ vertices. The machine names a kernel vertex by its rank in the kernel, a number of $O(\log k)$ bits, and finds the real vertex from its rank by a scan of the input. It tries every set of $k'$ ranks, which takes $O(k \log k) + O(\log n)$ bits.

For example, take 12 vertices, the edges from 0 to each of $1, \ldots, 7$, and the edges 12, 89, 9 10 and 10 11, with $k = 3$. Vertex 0 has degree 7, more than 3, so $h = 1$ and $k' = 2$. The rest has the 4 edges 12, 89, 9 10 and 10 11, at most $2 \cdot 3 = 6$, on the 6 vertices 1, 2, 8, 9, 10 and 11. A cover of these 4 edges needs 3 vertices, one for 12 and two for the path 8, 9, 10, 11, which is more than $k' = 2$. So the answer is no. The least cover of the whole graph is $\{0, 1, 8, 10\}$, so with $k = 4$ the answer is yes.

**Non-example: clique.** Clique with parameter $k$ is in XL: the machine stores a candidate set as $k$ vertex names, in $k \lceil \log n \rceil$ bits, and checks the pairs. But clique is W[1]-complete, and para-L is inside FPT, so clique is not in para-L unless $\mathsf{FPT} = \mathsf{W}[1]$. This is the reason the definition adds $f(k)$ and $O(\log n)$ and does not multiply them.

**Directed reachability.** Reachability in directed graphs, with the constant parameter 0, is in para-L if and only if it is in L, that is, if and only if $\mathsf{L} = \mathsf{NL}$. It is in para-NL. So a separation of para-L from para-NL is as hard as a separation of L from NL.

**Results of Elberfeld, Stockhusen and Tantau (2015).** They define para-L, para-NL, XL and XNL, give complete problems for them under para-L reductions, and place many standard problems:

- p-Distance (is there a path of length at most $k$ from $s$ to $t$, with parameter $k$) is complete for the subclass of para-NL in which a machine makes only $f(k) \log n$ nondeterministic choices, and this subclass equals para-NL if and only if $\mathsf{L} = \mathsf{NL}$;
- acceptance of a word by a deterministic finite automaton with $k$ heads, with parameter $k$, is XL-complete, and the nondeterministic version is XNL-complete;
- deciding whether a graph has [treewidth](/treewidth/) at most $k$ is in XL;
- feedback vertex set with parameter $k$ is in a class they call para-L-cert, defined by para-L machines that also read a certificate; they prove that this class is inside XL.

## Related definitions

- *[Logspace](/logspace/) and [NL](/nondeterministic-logspace/).* The classical classes. A problem that is complete for L under suitable reductions stays complete for para-L with a constant parameter.
- *[FPT](/fixed-parameter-tractable/).* The class para-P. Para-L and para-NL are subclasses, in the same way as L and NL are subclasses of P.
- *[Para-NP](/para-np-hardness/).* The nondeterministic polynomial-time para-class, defined by precomputation in the same way.
- *[XP](/xp/).* The time analogue of XL: each slice is in P. XL is inside XP.
- *[Space complexity](/space-complexity/).* The general theory of space-bounded classes, with the conventions on input and work tapes used here.

## References
