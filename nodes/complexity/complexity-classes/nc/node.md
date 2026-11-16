---
tag: 0QRGN1
kind: definition
slug: nc
name: NC
aliases:
- Nick's class
area: complexity/complexity-classes
level: advanced
summary: The problems decided by uniform Boolean circuits of polynomial size and polylogarithmic depth, that is in polylogarithmic parallel time on polynomially many processors.
prereqs: [boolean-circuit, p, logspace]
see_also: [ac0, tc0, circuit-value-problem, parallel-prefix, branching-program, transitive-closure, determinant, aks-sorting-network]
sources:
  - paper: doi:10.1109/SFCS.1979.29
    title: Nicholas Pippenger, On simultaneous resource bounds, 20th IEEE Symposium on Foundations of Computer Science, 307 to 311 (1979)
    locator: the definition of the class by simultaneous size and depth bounds
  - paper: doi:10.1137/0206054
    title: Allan Borodin, On relating time and space to size and depth, SIAM Journal on Computing 6(4), 733 to 744 (1977)
    locator: the theorems that NL is in NC2 and that NC^i is in space O(log^i n)
  - paper: doi:10.1016/0022-0000(81)90038-6
    title: Walter L. Ruzzo, On uniform circuit complexity, Journal of Computer and System Sciences 22(3), 365 to 383 (1981)
    locator: uniformity conditions and the characterization by alternating Turing machines
  - paper: doi:10.1016/S0019-9958(85)80041-3
    title: Stephen A. Cook, A taxonomy of problems with fast parallel algorithms, Information and Control 64, 2 to 22 (1985)
    locator: the classes NC^i and AC^i and the problems placed in them
  - paper: doi:10.1016/0022-0000(89)90037-8
    title: David A. Barrington, Bounded-width polynomial-size branching programs recognize exactly those languages in NC1, Journal of Computer and System Sciences 38(1), 150 to 164 (1989)
    locator: the main theorem and the commutator construction in S5
  - book: isbn:9780195085914
    title: Raymond Greenlaw, H. James Hoover and Walter L. Ruzzo, Limits to Parallel Computation, P-Completeness Theory, Oxford University Press (1995)
    locator: the chapters on parallel models and the list of P-complete problems
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press (2009)
    locator: Chapter 6, Boolean circuits (the classes NC and AC and P-completeness)
---

NC is the class of decision problems that have uniform [Boolean circuits](/boolean-circuit/) of polynomial size and depth $O(\log^k n)$ for some constant $k$. Depth is parallel time and size bounds the number of processors, so NC is the formal class of problems with fast parallel algorithms: polylogarithmic time on a polynomial number of processors. It is named after Nicholas Pippenger, who studied circuits with simultaneous size and depth bounds in 1979. NC is contained in [P](/p/), and whether the two are equal is open. The problems that are [P-complete](/circuit-value-problem/), such as circuit evaluation, are the ones believed to have no fast parallel algorithm.

## Definition

**The levels.** For $i \ge 1$, a language $L$ is in $\mathsf{NC}^i$ if there are a polynomial $s$, a constant $c$ and a uniform circuit family $\{C_n\}$ that decides $L$, where:

- *size*: $C_n$ has at most $s(n)$ gates,
- *depth*: $C_n$ has depth at most $c \log^i n$,
- *gate set and fan-in*: AND and OR of fan-in 2, NOT of fan-in 1,
- *uniformity*: a deterministic machine prints $C_n$ from $1^n$ in space $O(\log n)$ (logspace uniformity). For $\mathsf{NC}^1$ the standard choice is DLOGTIME uniformity, because a logspace machine is stronger than an $\mathsf{NC}^1$ circuit.

Then $\mathsf{NC} = \bigcup_{i \ge 1} \mathsf{NC}^i$. The class $\mathsf{NC}^0$, with constant depth and fan-in 2, contains only functions in which each output bit depends on a constant number of input bits.

**The AC levels.** $\mathsf{AC}^i$ is the same with AND and OR of unbounded fan-in, so $\mathsf{AC}^0$ is [AC0](/ac0/). An unbounded fan-in gate with at most $s(n)$ inputs is a tree of fan-in 2 gates of depth $O(\log n)$, and so

$$\mathsf{NC}^i \subseteq \mathsf{AC}^i \subseteq \mathsf{NC}^{i+1}, \qquad \mathsf{NC} = \bigcup_i \mathsf{AC}^i.$$

[TC0](/tc0/) and the classes $\mathsf{TC}^i$ fit between the two levels in the same way.

**Machine characterizations.** Several models give the same class, which is evidence that NC is a natural notion.

- *PRAM.* NC is the class of problems solved by a parallel random access machine in time $O(\log^k n)$ with polynomially many processors. Concurrent writes with unbounded fan-in correspond to the AC levels: $\mathsf{AC}^i$ is time $O(\log^i n)$ on a CRCW PRAM.
- *Alternating machines.* Ruzzo (1981) showed that uniform $\mathsf{NC}^i$ equals the languages decided by [alternating Turing machines](/alternating-turing-machine/) in time $O(\log^i n)$ and space $O(\log n)$, under a suitable uniformity condition.
- *Space.* Borodin (1977) proved that $\mathsf{NC}^i \subseteq \mathsf{DSPACE}(\log^i n)$, by evaluating the circuit depth-first.

**The main chain.**

$$\mathsf{NC}^1 \subseteq \mathsf{L} \subseteq \mathsf{NL} \subseteq \mathsf{AC}^1 \subseteq \mathsf{NC}^2 \subseteq \mathsf{NC} \subseteq \mathsf{P}.$$

$\mathsf{NC}^1 \subseteq$ [L](/logspace/) is Borodin's space bound for $i = 1$. [NL](/nondeterministic-logspace/) $\subseteq \mathsf{AC}^1$ comes from reachability by repeated squaring (below). NC is in polylogarithmic space, so by the [space hierarchy theorem](/space-hierarchy-theorem/) NC is not equal to [PSPACE](/pspace/). No other inclusion in the chain is known to be strict.

## Examples and non-examples

**Prefix sums and addition, in $\mathsf{NC}^1$.** The [parallel prefix](/parallel-prefix/) circuit computes all prefix sums of $n$ elements under an associative operator in depth $O(\log n)$. Carries of a binary addition are such prefix products, so addition is in $\mathsf{NC}^1$ (and in AC0). Iterated addition, multiplication and division are in TC0 and so in $\mathsf{NC}^1$. Sorting $n$ numbers is in $\mathsf{NC}^1$ by the [AKS sorting network](/aks-sorting-network/), with depth $O(\log n)$.

**Reachability and transitive closure, in $\mathsf{AC}^1$.** Let $A$ be the adjacency matrix of a directed graph on $m$ vertices and $R_0 = I \lor A$. Then $R_{t+1} = R_t \cdot R_t$ over the Boolean semiring records the pairs at distance at most $2^{t+1}$, and $\lceil \log_2(m-1) \rceil$ squarings give the [transitive closure](/transitive-closure/). One Boolean product is depth 2 with unbounded fan-in, or depth $O(\log m)$ with fan-in 2, so the whole computation is in $\mathsf{AC}^1 \subseteq \mathsf{NC}^2$. For the directed path $0 \to 1 \to \cdots \to 7$ on $m = 8$ vertices, vertex $0$ reaches $3$, $5$ and $8$ vertices (itself included) after the first, second and third squaring, and a fourth squaring changes nothing, as $\lceil \log_2 7 \rceil = 3$ predicts. Directed reachability is complete for NL, which gives $\mathsf{NL} \subseteq \mathsf{AC}^1$.

**Linear algebra, in $\mathsf{NC}^2$.** The [determinant](/determinant/) of an integer matrix, the characteristic polynomial, matrix inversion and the rank are in $\mathsf{NC}^2$ (Csanky for fields of characteristic 0, Berkowitz for any commutative ring). [Gaussian elimination](/gaussian-elimination/) as written is sequential, but the problems it solves are parallel.

**Barrington's theorem, $\mathsf{NC}^1$ as width 5.** Barrington (1989) proved that $\mathsf{NC}^1$ equals the languages decided by [branching programs](/branching-program/) of width 5 and polynomial length. The proof represents a gate by a sequence of permutations of $\{1, \ldots, 5\}$ that multiplies to a fixed 5-cycle when the gate is $1$ and to the identity when it is $0$. An AND gate uses a commutator: for $\sigma = (1\,2\,3\,4\,5)$ and $\tau = (1\,3\,5\,4\,2)$, the product $\sigma \tau \sigma^{-1} \tau^{-1}$, applied from right to left, is the 5-cycle $(1\,4\,3\,5\,2)$. It is not the identity, and it becomes the identity as soon as $\sigma$ or $\tau$ is replaced by the identity. So it behaves as an AND, and each level of the circuit multiplies the length of the program by 4. Depth $O(\log n)$ gives length $4^{O(\log n)}$, a polynomial. The construction needs a non-solvable group, which is why width 5 and $S_5$ appear.

**Matching, in randomized NC.** Deciding whether a graph has a [perfect matching](/perfect-matching/) is in RNC, the randomized version of NC, by the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/) applied to the Tutte matrix. For [bipartite matching](/bipartite-matching/), Fenner, Gurjar and Thierauf (2016) gave quasi-NC circuits, of size $2^{O(\log^2 n)}$ and polylogarithmic depth. Whether perfect matching is in NC is open.

**P-complete problems: probably not in NC.** A problem is P-complete if it is in P and every problem in P reduces to it by a logspace reduction (or an NC reduction). NC is closed under such reductions, so if one P-complete problem is in NC then $\mathsf{NC} = \mathsf{P}$. The standard example is the [circuit value problem](/circuit-value-problem/): given a circuit and an input, compute the output. Others are linear programming, maximum flow, and the order in which a depth-first search visits the vertices when it always takes the lowest-numbered neighbor. Greenlaw, Hoover and Ruzzo (1995) list many more.

**Open cases.** For some problems in P neither membership in NC nor P-completeness is known. The greatest common divisor of two $n$-bit integers is the standard example: the [Euclidean algorithm](/euclidean-algorithm/) needs $\Theta(n)$ rounds in the worst case, and no polylogarithmic-depth circuit is known.

## Related definitions

- [AC0](/ac0/) and [TC0](/tc0/): the constant-depth classes at the bottom of the AC and TC hierarchies.
- [P](/p/): NC is the parallel subclass, with P-completeness as the evidence of separation.
- [Branching programs](/branching-program/) and [logspace](/logspace/): $\mathsf{NC}^1$ is width-5 branching programs, and $\mathsf{L}$ is polynomial-size branching programs with a uniformity condition.
- [Circuit value problem](/circuit-value-problem/): the P-complete problem that marks the upper limit of NC.

## References
