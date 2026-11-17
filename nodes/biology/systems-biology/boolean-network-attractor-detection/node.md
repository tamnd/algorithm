---
tag: 0RASN0
kind: problem
slug: boolean-network-attractor-detection
name: Boolean network attractor detection
aliases:
- attractor finding in Boolean networks
area: biology/systems-biology
level: advanced
summary: "Find the fixed points and cycles of a synchronous or asynchronous Boolean network. Deciding if a fixed point exists is NP-complete; exact methods use state space search, SAT or BDDs."
prereqs: [boolean-function, functional-graph, strongly-connected-components, sat]
see_also: [random-boolean-network, gene-regulatory-network, binary-decision-diagram, tarjan-scc, condensation-graph, cdcl, np-complete, floyd-cycle-detection]
sources:
  - paper: "Tatsuya Akutsu, Satoru Kuhara, Osamu Maruyama and Satoru Miyano, A system for identifying genetic networks from gene expression patterns produced by gene disruptions and overexpressions, Genome Informatics 9, 151-160, 1998"
    title: Tatsuya Akutsu, Satoru Kuhara, Osamu Maruyama and Satoru Miyano, A system for identifying genetic networks from gene expression patterns produced by gene disruptions and overexpressions, 1998
    locator: the paper usually cited for the NP-hardness of finding a fixed point of a Boolean network
  - paper: doi:10.1109/TCBB.2010.20
    title: Elena Dubrova and Maxim Teslenko, A SAT-based algorithm for finding attractors in synchronous Boolean networks, IEEE/ACM Transactions on Computational Biology and Bioinformatics 8(5), 1393-1399, 2011
    locator: bounded model checking of paths of growing length, with the found attractors excluded
  - paper: doi:10.1093/bioinformatics/btn336
    title: Abhishek Garg, Alessandro Di Cara, Ioannis Xenarios, Luis Mendoza and Giovanni De Micheli, Synchronous versus asynchronous modeling of gene regulatory networks, Bioinformatics 24(17), 1917-1925, 2008
    locator: the algorithms on reduced ordered binary decision diagrams for the attractors of synchronous and asynchronous networks
  - paper: doi:10.1109/TC.1986.1676819
    title: Randal E. Bryant, Graph-based algorithms for Boolean function manipulation, IEEE Transactions on Computers C-35(8), 677-691, 1986
    locator: reduced ordered binary decision diagrams and their operations
  - paper: doi:10.1137/0201010
    title: Robert Tarjan, Depth-first search and linear graph algorithms, SIAM Journal on Computing 1(2), 146-160, 1972
    locator: the linear time algorithm for strongly connected components
  - paper: doi:10.1016/0022-5193(69)90015-0
    title: Stuart A. Kauffman, Metabolic stability and epigenesis in randomly constructed genetic nets, Journal of Theoretical Biology 22(3), 437-467, 1969
    locator: attractors of synchronous Boolean networks read as cell types
---

An *attractor* of a Boolean network is a set of states that the dynamics never leaves and that has no smaller such set inside it. Attractor detection asks for the attractors of a given network: whether there is a fixed point, all fixed points, or all attractors with their lengths and, sometimes, their basins. In models of gene regulation the attractors stand for the stable behaviors of a cell, such as cell types or a cell cycle. Deciding whether a network has a fixed point is NP-complete, even when every gene reads at most two genes, so no exact method is known that is fast on all networks. For small networks a full search of the $2^n$ states solves every version; for larger ones the methods encode the question as satisfiability or with binary decision diagrams. This page is about the computation on one given network. The [gene regulatory network](/gene-regulatory-network/) page describes the model, the [random Boolean network](/random-boolean-network/) page the typical attractors of random networks, and [gene regulatory network inference](/gene-regulatory-network-inference/) the task of finding the network from data.

## In plain words

Each gene of the network is on or off, and a rule for each gene says what it does next, given the genes it reads. Start from any pattern of on and off genes and keep applying the rules. Since there are only finitely many patterns, the run must end in a loop, or stop at a pattern that does not change. Those loops and resting patterns are the attractors. The task is to find all of them.

With a few genes you can try every starting pattern. With a hundred genes there are far too many patterns, so the methods instead describe the condition "this pattern does not change" or "this pattern comes back after some steps" as a logic formula and let a solver search for patterns that satisfy it.

## Definition

A Boolean network on $n$ genes is a list of functions $f_1, \ldots, f_n : \{0, 1\}^n \to \{0, 1\}$, where $f_i$ depends on a set of input genes. The functions are given as formulas or circuits, or as truth tables over the inputs when each gene has at most $K$ inputs. The *state graph* has the $2^n$ states as nodes; its edges depend on the update scheme.

- **Synchronous.** All genes update at once: $x \to F(x) = (f_1(x), \ldots, f_n(x))$. Each state has exactly one successor, so the state graph is a [functional graph](/functional-graph/), and the attractors are its cycles. A cycle of length 1 is a *fixed point*, and a longer cycle is a *cyclic attractor*.
- **Asynchronous.** One gene updates at a time: $x \to x'$, where $x'$ equals $x$ except that $x'_i = f_i(x)$, for each $i$ with $f_i(x) \neq x_i$. A state can have up to $n$ successors. The attractors are the *terminal* [strongly connected components](/strongly-connected-components/) of the state graph: the components with no edge leaving them, the sinks of the [condensation graph](/condensation-graph/). A fixed point is a state with no successor, and it is a fixed point in both schemes.

The *basin* of an attractor is the set of states that can reach it. In the synchronous scheme the basins partition the state space; in the asynchronous scheme a state can reach several attractors.

The main tasks, from easy to hard to state:

1. **Fixed point existence.** Is there an $x$ with $F(x) = x$?
2. **Fixed point listing or counting.** List or count all such $x$.
3. **Attractor listing.** List all attractors of the given scheme, possibly only those of length at most $p$.

## Variants

- **Bounded length.** Find the synchronous attractors of length at most $p$. For fixed $p$ this is a satisfiability question in $p n$ variables.
- **Restricted functions.** Networks of AND and OR functions, of threshold functions, or of monotone functions only. Fixed point existence stays NP-complete for networks of in-degree 2 whose functions are ANDs and ORs of literals, as the reduction below shows.
- **Other update schemes.** Block sequential updates, in which groups of genes update in a fixed order, and the most permissive scheme, which allows the intermediate values of a gene. Each scheme has its own attractors; the fixed points are the same in all of them.
- **Basins and control.** Find the basin sizes of the attractors, or a smallest set of genes to fix so that the network reaches a chosen attractor.

## Examples

**A switch.** Take two genes that repress each other, as in a [genetic toggle switch](/genetic-toggle-switch/): $A' = \neg B$ and $B' = \neg A$, with states written $AB$. Synchronously, $01$ and $10$ are fixed points, and $00 \to 11 \to 00$ is a cycle of length 2. Asynchronously, $00$ goes to $10$ or to $01$, and $11$ goes to $01$ or to $10$, so the only attractors are the two fixed points. The cycle exists only because both genes switch at the same instant, which a real cell does not do.

**A ring of three repressors.** Take $A' = \neg C$, $B' = \neg A$, $C' = \neg B$, a Boolean form of the [repressilator](/repressilator/), with states $ABC$. A fixed point would need $A = \neg C = B = \neg A$, which is impossible. Synchronously, $000 \to 111 \to 000$ is a cycle of length 2, and the other six states form one cycle of length 6, $100 \to 101 \to 001 \to 011 \to 010 \to 110 \to 100$. Asynchronously, each of those six states has exactly one gene with $f_i(x) \neq x_i$, so it has one successor, the next state of the same cycle; the six states form a terminal component, a cyclic attractor. The states $000$ and $111$ have three successors each and lead into it, so they are not part of any attractor.

**Toward an algorithm.** The [random Boolean network](/random-boolean-network/) page gives a scan of the synchronous state space that returns every attractor and its basin in $O(2^n)$ steps, with a test against a second method for $n$ up to 12. In the example there, with $A' = B$, $B' = A$ and $C' = A \wedge B$, the attractors are two fixed points and one cycle of length 2, with basins of 2, 2 and 4 states.

## Known algorithms

- **Full state space search, synchronous.** Compute $F$ on all $2^n$ states and find the cycles of the functional graph, in $O(2^n n K)$ time for in-degree $K$ and $O(2^n)$ space. For one trajectory, [Floyd's cycle detection](/floyd-cycle-detection/) or [Brent's method](/brent-cycle-detection/) finds the attractor that it reaches with $O(1)$ stored states, but covering all attractors needs all starts.
- **Full state space search, asynchronous.** Build the state graph, with at most $n 2^n$ edges, find its strongly connected components with [Tarjan's algorithm](/tarjan-scc/) in time linear in its size, and keep the components with no edge leaving them. This costs $O(n 2^n)$ time and space.
- **Fixed points by SAT.** The fixed points are the satisfying assignments of $\bigwedge_i (x_i \leftrightarrow f_i(x))$. A [CDCL](/cdcl/) solver finds one, and blocking clauses list them all, one solver call per fixed point.
- **Cycles by bounded model checking.** Unroll the network $p$ times with variables $x^0, \ldots, x^p$, add $x^{t+1} = F(x^t)$ and $x^p = x^0$, and solve. Dubrova and Teslenko (2011) search paths of growing length, exclude the attractors found so far, and stop when no path of the current length can avoid them. The method has no polynomial bound; its cost grows with the lengths of the attractors and of the paths that lead to them.
- **Binary decision diagrams.** Represent sets of states and the transition relation as [reduced ordered BDDs](/binary-decision-diagram/) (Bryant 1986), and compute attractors by repeated image and preimage operations, which work on whole sets of states at once. Garg et al. (2008) used this for both update schemes. The cost depends on the size of the diagrams, which is exponential for some functions and orders of the variables.
- **Network reduction.** A gene that no other gene reads can be removed before the search: the synchronous attractors of the smaller network map one to one onto those of the full network, because the removed gene's value is a function of the previous state. Genes with constant functions can be fixed and propagated in the same way. These rules often shrink models a lot, but give no bound in general.

## Bounds

**Fixed point existence is NP-complete (theorem).** It is in NP, since a state $x$ is a certificate that is checked by evaluating $F(x)$. It is [NP-hard](/np-hard/) by the reduction below, even for networks in which every gene reads at most two genes and every function is the identity or an AND or OR of two literals. The result is usually credited to Akutsu, Kuhara, Maruyama and Miyano (1998).

**Counting fixed points is #P-complete (theorem).** The reduction below is parsimonious: each satisfying assignment of the formula gives exactly one fixed point. So counting fixed points is as hard as counting the satisfying assignments of a 3-CNF formula.

**No subexponential algorithm under ETH (theorem, conditional).** The reduction maps a [3-SAT](/3-sat/) formula with $v$ variables and $m$ clauses to a network with $v + 3m + 1$ genes. Under the exponential time hypothesis and the sparsification lemma, 3-SAT has no $2^{o(v + m)}$ time algorithm, so fixed point existence has no $2^{o(n)}$ time algorithm for networks of in-degree 2.

**Output size.** The identity network $x_i' = x_i$ has $2^n$ fixed points, so listing all attractors takes $\Omega(2^n)$ time in the worst case, whatever the method. The full search is optimal in this sense.

## Reductions

**From 3-SAT to fixed point existence.** Let $\varphi = C_1 \wedge \cdots \wedge C_m$ with clauses $C_j = \ell_{j1} \vee \ell_{j2} \vee \ell_{j3}$ over variables $u_1, \ldots, u_v$. Build a network with these genes and functions:

- a gene $x_k$ with $x_k' = x_k$ for each variable;
- for each clause, genes $a_j$ and $c_j$ with $a_j' = \ell_{j1} \vee \ell_{j2}$ and $c_j' = a_j \vee \ell_{j3}$, where a literal $\neg u_k$ is read as $\neg x_k$;
- a chain $y_1' = c_1$ and $y_j' = y_{j-1} \wedge c_j$ for $j = 2, \ldots, m$;
- a gene $z$ with $z' = \neg z \vee y_m$.

Every gene reads at most two genes. At a fixed point, each $a_j$, $c_j$ and $y_j$ equals its function of the current state, so $c_j = 1$ exactly when $x$ satisfies $C_j$, and $y_m = 1$ exactly when $x$ satisfies $\varphi$. The gene $z$ is fixed only if $z = \neg z \vee y_m$; with $y_m = 0$ this says $z = \neg z$, which is impossible, and with $y_m = 1$ it says $z = 1$. So the network has a fixed point if and only if $\varphi$ is satisfiable, and the fixed points correspond one to one to the satisfying assignments, since all genes other than the $x_k$ are then determined. The network has $v + 3m + 1$ genes and is built in linear time.

**From fixed points to SAT.** The formula $\bigwedge_i (x_i \leftrightarrow f_i(x))$ has the fixed points as its models, so any SAT solver decides the problem; with truth tables of in-degree $K$ the formula has $O(n 2^K)$ clauses.

**From asynchronous attractors to strongly connected components.** As in the definition, the attractors are the sink components of the state graph, so an SCC algorithm on the explicit state graph solves the problem in time linear in $n 2^n$.

**From synchronous attractors to cycle detection.** The state graph is a functional graph, so its attractors are its cycles, which any [cycle detection](/cycle-detection/) method finds from each start.

## Applications

- **Cell fates in models of gene regulation.** Boolean models of real [gene regulatory networks](/gene-regulatory-network/) have tens to hundreds of genes. Their fixed points are compared with the measured expression patterns of cell types, and their cyclic attractors with oscillations such as the cell cycle.
- **Typical behavior of random networks.** The number and length of the attractors of [random Boolean networks](/random-boolean-network/) are measured by exact detection on small networks.
- **Choice of the update scheme.** Comparing the synchronous and asynchronous attractors of a model shows which cycles are artifacts of the synchronous update, as in the switch example.
- **Control.** Finding genes whose fixed values remove an unwanted attractor, for example a disease state, starts from the list of attractors.

## References
