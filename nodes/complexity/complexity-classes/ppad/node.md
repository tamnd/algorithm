---
tag: E0ZXST
kind: definition
slug: ppad
name: PPAD
aliases:
- "polynomial parity argument, directed"
area: complexity/complexity-classes
level: advanced
summary: "The total search problems that reduce to END-OF-THE-LINE: given circuits for a successor and a predecessor, find another end of the line that starts at 0^n. Nash equilibria are complete."
prereqs: [tfnp, boolean-circuit]
see_also: [tfnp, pls, fnp, nash-equilibrium-computation, nash-existence-theorem, nash-equilibrium, local-search-problem, pigeonhole-principle]
sources:
  - paper: doi:10.1016/S0022-0000(05)80063-7
    title: Christos H. Papadimitriou, On the complexity of the parity argument and other inefficient proofs of existence, Journal of Computer and System Sciences 48(3) (1994)
    locator: pp. 498 to 532 (the classes PPAD, PPA and PPP, the inclusions among them, Brouwer fixed points in PPAD and the PPAD-completeness of Sperner's lemma in three dimensions)
  - paper: doi:10.1137/070699652
    title: Constantinos Daskalakis, Paul W. Goldberg and Christos H. Papadimitriou, The complexity of computing a Nash equilibrium, SIAM Journal on Computing 39(1) (2009)
    locator: pp. 195 to 259 (the END OF THE LINE problem, graphical games and the PPAD-completeness of Nash equilibria); conference version in STOC 2006
  - paper: doi:10.1145/1516512.1516516
    title: Xi Chen, Xiaotie Deng and Shang-Hua Teng, Settling the complexity of computing two-player Nash equilibria, Journal of the ACM 56(3) (2009)
    locator: the PPAD-completeness of two-player Nash equilibria and of approximate equilibria with polynomially small error
  - paper: doi:10.1145/3568163
    title: John Fearnley, Paul W. Goldberg, Alexandros Hollender and Rahul Savani, The complexity of gradient descent (CLS = PPAD intersection PLS), Journal of the ACM 70(1) (2023), Article 7
    locator: the main theorem; conference version in STOC 2021, doi 10.1145/3406325.3451052
---

PPAD (polynomial parity argument, directed) is the subclass of [TFNP](/tfnp/) defined by one complete problem, END-OF-THE-LINE. The problem gives a directed graph in which every vertex has at most one predecessor and at most one successor, and a vertex that starts a line. The graph has $2^n$ vertices and is given by two circuits, not by a list of edges. A line that starts somewhere must end somewhere, so another end exists, and the task is to find one. Papadimitriou defined PPAD in 1994. The class matters because finding a [Nash equilibrium](/nash-equilibrium-computation/) is PPAD-complete, and so are Brouwer fixed points and Sperner's lemma.

## Definition

Fix the alphabet $\{0, 1\}$. Machines are deterministic [multitape Turing machines](/multitape-turing-machine/), and circuits are [Boolean circuits](/boolean-circuit/) with AND, OR and NOT gates of fan-in at most 2.

**END-OF-THE-LINE.** This is the form of Daskalakis, Goldberg and Papadimitriou.

- *Instance:* two circuits $S$ and $P$, each with $n$ inputs and $n$ outputs, such that $P(0^n) = 0^n \ne S(0^n)$.
- *Solution:* a string $x \in \{0, 1\}^n$ with $P(S(x)) \ne x$, or with $S(P(x)) \ne x \ne 0^n$.

**The graph.** Read $S$ as "successor" and $P$ as "predecessor". The graph on $\{0, 1\}^n$ has an edge from $x$ to $y$ when $x \ne y$, $S(x) = y$ and $P(y) = x$. So an edge exists only when the two circuits agree on it. Each vertex has at most one outgoing edge and at most one incoming edge, so the graph is a union of directed paths, directed cycles and isolated vertices. The condition $P(0^n) = 0^n$ says that $0^n$ has no predecessor. A string with $P(S(x)) \ne x$ has no outgoing edge, so it ends a line. A string other than $0^n$ with $S(P(x)) \ne x$ has no incoming edge, so it starts a line. The solutions are these ends, except the known start $0^n$.

**Why a solution exists.** If $P(S(0^n)) \ne 0^n$, then $0^n$ is itself a solution. Otherwise $0^n$ has an outgoing edge. Follow the edges from $0^n$. The walk never returns to $0^n$, because $0^n$ has no incoming edge, and it never visits a vertex twice, because each vertex has one predecessor at most. There are $2^n$ vertices, so the walk stops at a vertex with no outgoing edge, and that vertex is a solution. The argument is a parity argument: every path has two ends, so the number of ends other than $0^n$ is odd.

**The class.** PPAD is the class of search problems in TFNP that reduce to END-OF-THE-LINE under the reductions of [FNP](/fnp/): a pair of maps $(f, g)$ computable in polynomial time, where $f$ maps an instance $x$ to an instance $f(x)$ of END-OF-THE-LINE and $g(x, z)$ maps each solution $z$ of $f(x)$ to a solution of $x$. A problem is PPAD-complete if it is in PPAD and END-OF-THE-LINE reduces to it.

**Why the problem can be hard.** The walk from $0^n$ is the obvious algorithm, but a line can pass through up to $2^n - 1$ edges before it ends. The circuits have size polynomial in $n$, so the walk can take time exponential in the input size. Nothing else is known in general: whether END-OF-THE-LINE is in FP is open.

**Facts about the class.**

- $\mathsf{FP} \subseteq \mathsf{PPAD} \subseteq \mathsf{PPA} \subseteq \mathsf{TFNP}$ and $\mathsf{PPAD} \subseteq \mathsf{PPP}$ (Papadimitriou 1994). PPA uses undirected graphs of degree at most 2, and PPP uses the pigeonhole principle (see [TFNP](/tfnp/)).
- $\mathsf{PPAD} \cap \mathsf{PLS} = \mathsf{CLS}$, the class of continuous local search (Fearnley, Goldberg, Hollender and Savani). Before this result, the inclusion $\mathsf{CLS} \subseteq \mathsf{PPAD} \cap \mathsf{PLS}$ was known and many expected it to be strict.
- *Not NP-hard unless $\mathsf{NP} = \mathsf{coNP}$.* PPAD is inside TFNP, so by the theorem on the [TFNP](/tfnp/) page no PPAD problem is FNP-complete unless $\mathsf{NP} = \mathsf{coNP}$.

## Examples and non-examples

**A small instance.** Take $n = 3$ and read the strings as the numbers 0 to 7. Let the circuits compute these tables:

| $x$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $S(x)$ | 3 | 4 | 2 | 6 | 1 | 7 | 6 | 7 |
| $P(x)$ | 0 | 4 | 2 | 0 | 1 | 5 | 3 | 5 |

The condition $P(0) = 0 \ne S(0) = 3$ holds. The edges, where $S(x) = y$ and $P(y) = x$, are $0 \to 3$, $3 \to 6$, $1 \to 4$, $4 \to 1$ and $5 \to 7$. So the graph has the line $0 \to 3 \to 6$, the cycle $1 \to 4 \to 1$, the line $5 \to 7$ and the isolated vertex 2. The solutions are 6 and 7, where $P(S(x)) \ne x$, and 5, where $S(P(x)) = 7 \ne 5$. The walk from 0 reaches the solution 6 after 2 steps. There are 3 solutions, an odd number, as the parity argument says. The line $5 \to 7$ does not touch the line from 0, so a solver may return 5 or 7 without ever finding 6.

**PPAD-complete problems.**

- *END-OF-THE-LINE*, by definition.
- *Sperner's lemma in three dimensions* (Papadimitriou 1994): given a coloring of a subdivided simplex by a circuit, with the usual boundary rule, find a fully colored small simplex.
- *Nash equilibria.* Daskalakis, Goldberg and Papadimitriou (2009) proved that finding an approximate Nash equilibrium is PPAD-complete for games with a fixed number of players, through graphical games. Chen, Deng and Teng (2009) proved it for two players, where an exact equilibrium has rational coordinates of polynomial size. See [Nash equilibrium computation](/nash-equilibrium-computation/) for the games, the algorithms and the approximation results.

**Problems in PPAD.**

- *Brouwer fixed points.* Given a continuous map of a cube to itself, computed by a circuit, find an approximate fixed point (Papadimitriou 1994). The exact fixed point can be irrational, so the problem asks for a point that moves by at most a given $\varepsilon$.
- *Any problem in FP*, read as a total search problem: the reduction can solve the instance itself and output a fixed END-OF-THE-LINE instance.

**Non-examples.**

- *Finding a cycle or a line through a given vertex.* A vertex can lie on a cycle, as 1 and 4 above, and then no end is near it. The parity argument only guarantees an end somewhere.
- *Finding the end of the line that starts at $0^n$.* This asks for one specific solution, 6 above, and not for any end. It is a different problem from END-OF-THE-LINE, and a reduction to it does not show membership in PPAD.
- *Equilibria with an extra property.* Deciding whether a two-player game has an equilibrium in which player 1 gets at least a given payoff is NP-complete (Gilboa and Zemel 1989, see [Nash equilibrium computation](/nash-equilibrium-computation/)). The extra condition can fail, so the search problem is no longer total, and the NP-hardness does not contradict the PPAD bound for finding some equilibrium.

**A common mistake.** PPAD-hardness is not NP-hardness. A PPAD-complete problem always has a solution, and if it were NP-hard, then $\mathsf{NP} = \mathsf{coNP}$. PPAD-completeness says that the problem is as hard as END-OF-THE-LINE. It is evidence of difficulty only if one believes that END-OF-THE-LINE has no polynomial-time algorithm.

## Related definitions

- **[TFNP](/tfnp/)** is the class of total search problems. PPAD, PLS, PPA and PPP are its main subclasses.
- **[PLS](/pls/)** is the subclass for local optima. A local search walk improves a cost, while a PPAD walk follows a line with no cost. The two classes meet in CLS.
- **[Nash equilibrium computation](/nash-equilibrium-computation/)** is the main PPAD-complete problem. The Lemke and Howson algorithm described there follows a path in a graph of the END-OF-THE-LINE kind.
- **[Nash's theorem](/nash-existence-theorem/)** gives the existence that makes the Nash problem total. Its proof uses a fixed-point theorem, which is the source of the link with Brouwer fixed points.
- **[FNP](/fnp/)** gives the reductions used to define PPAD.

## References
