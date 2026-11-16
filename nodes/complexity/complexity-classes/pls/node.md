---
tag: BD9P8A
kind: definition
slug: pls
name: PLS
aliases:
- polynomial local search
area: complexity/complexity-classes
level: advanced
summary: "The total search problems of finding a local optimum, where a start solution, the cost and an improving neighbour are each computed in polynomial time. Local Max-Cut under flips is complete."
prereqs: [tfnp, local-search-problem]
see_also: [local-search-problem, tfnp, ppad, fnp, maximum-cut, hill-climbing, kernighan-lin, nash-equilibrium-computation]
sources:
  - paper: doi:10.1016/0022-0000(88)90046-3
    title: David S. Johnson, Christos H. Papadimitriou and Mihalis Yannakakis, How easy is local search?, Journal of Computer and System Sciences 37(1) (1988)
    locator: pp. 79 to 100 (the definition of PLS, PLS reductions, Circuit Flip and the Kernighan-Lin neighbourhood are PLS-complete, and a PLS problem is not NP-hard unless NP = coNP)
  - paper: doi:10.1137/0220004
    title: Alejandro A. Schäffer and Mihalis Yannakakis, Simple local search problems that are hard to solve, SIAM Journal on Computing 20(1) (1991)
    locator: pp. 56 to 87 (Max-Cut with the flip neighbourhood is PLS-complete, tight reductions, exponential improving paths, and the PSPACE-completeness of the standard-algorithm problem)
  - paper: doi:10.1145/3568163
    title: John Fearnley, Paul W. Goldberg, Alexandros Hollender and Rahul Savani, The complexity of gradient descent (CLS = PPAD intersection PLS), Journal of the ACM 70(1) (2023), Article 7
    locator: the main theorem (CLS = PPAD ∩ PLS); conference version in STOC 2021, pp. 46 to 59, doi 10.1145/3406325.3451052
  - paper: doi:10.1016/0304-3975(91)90200-L
    title: Nimrod Megiddo and Christos H. Papadimitriou, On total functions, existence theorems and computational complexity, Theoretical Computer Science 81(2) (1991)
    locator: pp. 317 to 324 (TFNP and its relation to NP and coNP)
---

PLS (polynomial local search) is the class of search problems that ask for a local optimum, in the setting where each single step of local search runs in polynomial time. Johnson, Papadimitriou and Yannakakis defined it in 1988. A local optimum always exists, so PLS lies inside [TFNP](/tfnp/). The open question is how many steps it takes to reach one. The page on the [local search problem](/local-search-problem/) gives the problems, the algorithms and a worked Max-Cut instance. This page gives the class: its formal definition, its reductions, its complete problems and its place among the other classes.

## Definition

Fix the alphabet $\{0, 1\}$. Machines are deterministic [multitape Turing machines](/multitape-turing-machine/).

**A PLS problem.** A problem $\Pi$ in PLS is a maximization or minimization problem with these parts:

- a set of instances, decidable in polynomial time;
- for each instance $I$, a finite set $F(I)$ of *solutions*, all strings of length at most $p(|I|)$ for a polynomial $p$;
- an integer *cost* $c(I, s)$ for each solution $s$;
- for each solution $s$, a set $N(I, s) \subseteq F(I)$ of *neighbours*.

Three polynomial-time algorithms must exist:

1. $A$: given $I$, output a solution $s_0 \in F(I)$;
2. $B$: given $I$ and a string $s$, decide whether $s \in F(I)$, and if so compute $c(I, s)$;
3. $C$: given $I$ and $s \in F(I)$, either report that no neighbour has a better cost, or output a neighbour $s' \in N(I, s)$ with a better cost.

The search problem is: given $I$, find a *local optimum*, a solution $s$ such that no neighbour of $s$ has a better cost. PLS is the class of these search problems.

**PLS is in TFNP.** $F(I)$ is finite and not empty, because $A$ gives one solution. A solution with the best cost in $F(I)$ is a local optimum, so a solution exists. A claimed solution $s$ is checked in polynomial time: run $B$ to see that $s \in F(I)$, then run $C$ and see that it reports no better neighbour.

**The standard algorithm.** Start at $s_0 = A(I)$ and apply $C$ until it reports a local optimum. Each step improves the cost, so no solution is visited twice, and the run ends. But $|F(I)|$ can be $2^{p(|I|)}$, so the number of steps can be exponential. Membership in PLS says only that one step is cheap.

**PLS reductions.** A PLS reduction from $\Pi_1$ to $\Pi_2$ is a pair of polynomial-time maps $(f, g)$. The map $f$ sends an instance $I$ of $\Pi_1$ to an instance $f(I)$ of $\Pi_2$. The map $g$ sends each local optimum $s$ of $f(I)$ to a local optimum $g(I, s)$ of $I$. These reductions compose. A problem is *PLS-complete* if it is in PLS and every problem in PLS reduces to it. A reduction is *tight* (Schäffer and Yannakakis) if it also keeps the shape of improving paths, so that long paths in $\Pi_1$ give long paths in $\Pi_2$.

**Facts about the class.**

- $\mathsf{FP} \subseteq \mathsf{PLS} \subseteq \mathsf{TFNP}$, where FP is read as the total search problems with a polynomial-time solution. Whether $\mathsf{FP} = \mathsf{PLS}$ is open.
- *Not NP-hard unless $\mathsf{NP} = \mathsf{coNP}$.* If a PLS problem were FNP-complete, then $\mathsf{NP} = \mathsf{coNP}$ (Johnson, Papadimitriou and Yannakakis). This is the case of PLS in the [TFNP](/tfnp/) theorem: an unsatisfiable formula would have a short certificate, a local optimum of the image instance that $g$ maps to "no".
- *The standard algorithm and its paths.* For the PLS-complete problems with tight reductions, such as Max-Cut with the flip neighbourhood, there are instances and start solutions from which every improving path is exponentially long. The problem "find the local optimum that the standard algorithm reaches from a given start" is PSPACE-complete for these problems (Schäffer and Yannakakis). Both facts are about one algorithm. They do not show that the search problem itself has no polynomial-time algorithm.
- *Continuous local search.* CLS is the subclass for local optima of smooth functions found by gradient steps. Fearnley, Goldberg, Hollender and Savani proved $\mathsf{CLS} = \mathsf{PPAD} \cap \mathsf{PLS}$, with the [gradient descent](/gradient-descent/) problem of finding a KKT point on the square $[0, 1]^2$ as a complete problem.

## Examples and non-examples

**PLS-complete problems.**

- *Circuit Flip* (Johnson, Papadimitriou and Yannakakis). Given a Boolean circuit with $n$ inputs and $m$ outputs, a solution is an input string, its cost is the output read as a binary number, and the neighbours are the inputs at Hamming distance 1. Find an input that no single flip improves. This is the generic complete problem: the circuit can encode the cost and the neighbourhood of any PLS problem.
- *Graph partitioning with the [Kernighan-Lin](/kernighan-lin/) neighbourhood* (Johnson, Papadimitriou and Yannakakis).
- *Local Max-Cut with the flip neighbourhood* (Schäffer and Yannakakis). A solution is a split of the vertices of an edge-weighted graph into two sides, the cost is the weight of the edges across the split, and a neighbour moves one vertex. The weights are integers in binary. See [maximum cut](/maximum-cut/) and the worked instance on the [local search problem](/local-search-problem/) page.
- *Pure Nash equilibria of congestion games*, through a reduction from local Max-Cut. See the [local search problem](/local-search-problem/) page.

**Problems in PLS that are easy.** If the cost takes only polynomially many values, the standard algorithm runs in polynomial time. Unweighted Max-Cut is an example: the cut size lies between 0 and the number of edges $m$, so there are at most $m$ improving steps. The hard instances of local Max-Cut need weights with many bits.

**A long path in an easy problem.** Let the instances be $1^n$, the solutions be the strings in $\{0, 1\}^n$, and the cost of $s$ be its position in the reflected Gray code $g(i) = i \oplus \lfloor i/2 \rfloor$, to be maximized. The neighbours of $s$ are the strings at Hamming distance 1. Every string except the last one, $g(2^n - 1) = 10\cdots0$, has its successor in the Gray code as a neighbour, so $10\cdots0$ is the only local optimum. A run from $0^n$ that always moves to the improving neighbour with the smallest gain visits every string in Gray code order. It took 15 steps for $n = 4$, 1023 for $n = 10$ and 1,048,575 for $n = 20$, which is $2^n - 1$ in each case. A run that moves to the neighbour with the largest gain flips the leading bit, reaches $10\cdots0$ and stops after 1 step. The problem is in FP, since the answer is $10\cdots0$ for every $n$. So an exponential run of the standard algorithm with one pivot rule says nothing about the difficulty of the problem. The lower bounds of Schäffer and Yannakakis are stronger: for local Max-Cut they hold for every improving path.

**Non-examples.**

- *Global optima.* "Find a maximum cut" asks for a global optimum. Its decision version is NP-complete, so it is not in PLS unless $\mathsf{NP} = \mathsf{coNP}$.
- *Problems where one step is hard.* If a neighbourhood has exponentially many members and finding an improving one is NP-hard, then algorithm $C$ does not exist in polynomial time, and the problem is not known to be in PLS.

## Related definitions

- **[Local search problem](/local-search-problem/)** gives the problems, the standard algorithm and its variants, and the worked Max-Cut example. This page does not repeat them.
- **[TFNP](/tfnp/)** is the class of total search problems in FNP, and PLS is one of its subclasses.
- **[PPAD](/ppad/)** is the subclass defined by the directed parity argument. Its complete problems include Nash equilibria. PLS and PPAD meet in CLS.
- **[FNP](/fnp/)** and **[FP](/fp/)** are the classes of all search problems with short checkable answers and of those with a polynomial-time solution.
- **[Hill climbing](/hill-climbing/)** is the standard algorithm in its general form.

## References
