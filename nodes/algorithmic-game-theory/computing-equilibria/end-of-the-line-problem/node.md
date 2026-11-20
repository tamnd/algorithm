---
tag: AW752P
kind: problem
slug: end-of-the-line-problem
name: End of the line problem
aliases:
- END OF THE LINE
- EOTL
area: algorithmic-game-theory/computing-equilibria
level: advanced
summary: Given circuits for successor and predecessor on an exponential graph with a known source, find another source or sink. It defines PPAD.
prereqs: [ppad, boolean-circuit, handshaking-lemma]
see_also: [ppad-completeness-of-nash, sperner-lemma, scarf-algorithm, lemke-howson-algorithm, tfnp, pls, pspace, nash-equilibrium-computation]
sources:
  - paper: doi:10.1016/S0022-0000(05)80063-7
    title: "Christos H. Papadimitriou, On the complexity of the parity argument and other inefficient proofs of existence, Journal of Computer and System Sciences 48(3) (1994), 498-532"
    locator: the parity argument for directed graphs, the class PPAD, the sink-only variant PPADS and the PSPACE-completeness of finding the other end of the given line
  - paper: doi:10.1137/070699652
    title: "Constantinos Daskalakis, Paul W. Goldberg and Christos H. Papadimitriou, The complexity of computing a Nash equilibrium, SIAM Journal on Computing 39(1) (2009), 195-259"
    locator: the definition of END OF THE LINE with the circuits S and P, and the reductions between it and Nash equilibria
  - paper: doi:10.1109/FOCS.2015.94
    title: "Nir Bitansky, Omer Paneth and Alon Rosen, On the cryptographic hardness of finding a Nash equilibrium, IEEE 56th Annual Symposium on Foundations of Computer Science (FOCS 2015), 1480-1498"
    locator: hard instances of END OF THE LINE from indistinguishability obfuscation and one-way functions
  - paper: doi:10.1145/3568163
    title: "John Fearnley, Paul W. Goldberg, Alexandros Hollender and Rahul Savani, The complexity of gradient descent: CLS = PPAD ∩ PLS, Journal of the ACM 70(1) (2022), article 7"
    locator: END OF POTENTIAL LINE and the result that CLS is the intersection of PPAD and PLS
---

END OF THE LINE is the search problem behind the class [PPAD](/ppad/). The input describes a huge directed graph in which every node has at most one incoming edge and at most one outgoing edge, so the graph is a set of paths and cycles. One node, the all-zero string, is known to start a path. The task is to find the end of some path: a sink, or a source other than the known one. A solution always exists by a parity argument, and it is easy to check, but the graph has exponentially many nodes, so walking along the path can take exponential time. PPAD is the class of search problems that reduce to END OF THE LINE in polynomial time, and finding a [Nash equilibrium](/nash-equilibrium/) is one of them ([PPAD-completeness of Nash](/ppad-completeness-of-nash/)).

## In plain words

Picture a very long list of rooms, so many that you cannot visit them all. Each room has at most one door in and at most one door out, and a small program tells you, for any room, where its doors lead. You stand in a room that has a door out but no door in. Follow the doors, and you must arrive at a room with no door out, because the rooms are finite and you can never come back. Somewhere there is a room that is the end of a corridor. The question is whether you can find one such room much faster than by walking, and in general nobody knows how.

## Definition

**END OF THE LINE.** The input is two Boolean circuits $S$ and $P$, each with $n$ input bits and $n$ output bits, such that $P(0^n) = 0^n \ne S(0^n)$. They define a directed graph on the $2^n$ strings of $n$ bits: there is an edge from $x$ to $y$ if $S(x) = y$ and $P(y) = x$. So $S$ proposes a successor, $P$ proposes a predecessor, and an edge exists only when both agree. The output is a string $x$ with

$$P(S(x)) \ne x \qquad\text{or}\qquad S(P(x)) \ne x \ne 0^n .$$

The first condition says that $x$ has no outgoing edge, and the second says that $x$ has no incoming edge and is not the start. The circuits have size polynomial in $n$, so the input has size polynomial in $n$, while the graph has $2^n$ nodes.

In the graph, every node has in-degree at most 1 and out-degree at most 1. The start $0^n$ has in-degree 0. If it has out-degree 0, it is a solution by the first condition. If not, it is the source of a path, and the path is finite, so it ends at a sink. So a solution always exists, and the problem is in [TFNP](/tfnp/): solutions are short and a polynomial-time test checks them. This is the directed form of the [handshaking lemma](/handshaking-lemma/): in a graph of this kind, the number of sources equals the number of sinks, so a known source forces an end somewhere.

Under the formal conditions, a string $x$ whose successor does not point back to it counts as a sink even if it also has no predecessor. So a node that is isolated in the graph can be a solution. Some texts add the rule that $S(x) = P(x) = x$ for every node that is not on a path, and with this rule the solutions are exactly the sinks and the sources other than $0^n$.

## Variants

- **Sink only.** Asking only for a sink defines the class PPADS, which contains PPAD. Papadimitriou (1994) defined both.
- **Other end of this line.** Asking for the sink of the path that starts at $0^n$, and not for any end, gives a problem that is [PSPACE](/pspace/)-complete (Papadimitriou 1994). Path-following methods such as [Lemke-Howson](/lemke-howson-algorithm/) solve this harder problem, and Goldberg, Papadimitriou and Savani (2013) used it to show that the specific equilibrium that Lemke-Howson finds is PSPACE-complete to compute.
- **Undirected graphs.** With an undirected graph of degree at most 2 and a known leaf, the task of finding another leaf defines the class PPA. Consensus halving and necklace splitting are PPA-complete in some regimes ([consensus halving](/consensus-halving/)).
- **End of potential line.** If each node also has a potential that increases along the edges, the problem defines the class CLS. Fearnley, Goldberg, Hollender and Savani (2022) showed that CLS is the intersection of PPAD and [PLS](/pls/).
- **Query model.** The circuits are replaced by oracles that give $S(x)$ and $P(x)$ on request. Then an adversary can hide a long path among the $2^n$ nodes, and every algorithm needs exponentially many queries in the worst case.

## Examples

Take $n = 3$. Let $S$ and $P$ be as in the table, where a string that maps to itself has no successor or no predecessor.

| $x$ | 000 | 001 | 011 | 100 | 110 | 111 | 010 | 101 |
|---|---|---|---|---|---|---|---|---|
| $S(x)$ | 001 | 011 | 011 | 110 | 111 | 111 | 010 | 101 |
| $P(x)$ | 000 | 000 | 001 | 100 | 100 | 110 | 010 | 101 |

The edges are $000 \to 001 \to 011$ and $100 \to 110 \to 111$, and the nodes 010 and 101 are isolated. The solutions are 011 (a sink, since $P(S(011)) = P(011) = 001$), 111 (a sink) and 100 (a source other than 000, since $S(P(100)) = S(100) = 110$). The walk from 000 finds 011 after 2 steps. There are 3 path ends other than the start, an odd number, as the parity argument says. In general there can be many paths and cycles, and a walk from $0^n$ can be $2^n - 1$ steps long.

## Known algorithms

- **Follow the line.** Start at $0^n$ and apply $S$ until $P(S(x)) \ne x$. This uses at most $2^n$ evaluations of the circuits, and it finds the other end of the line that starts at $0^n$.
- **Path-following methods for concrete problems.** [Lemke-Howson](/lemke-howson-algorithm/) for bimatrix games, [Scarf's algorithm](/scarf-algorithm/) for fixed points and the path proof of the [Sperner lemma](/sperner-lemma/) are all walks of this kind on graphs that are given implicitly by the problem.
- **No general shortcut.** No algorithm with a running time below exponential in $n$ is known for general circuits.

## Bounds

The trivial upper bound is $O(2^n \cdot s)$ time, where $s$ is the size of the circuits. The problem is PPAD-complete by definition, so a polynomial-time algorithm would put every problem in PPAD, such as Nash equilibria of [bimatrix games](/bimatrix-game/), in polynomial time. It is in TFNP, so it is not [NP-hard](/np-hard/) unless NP equals coNP. In the query model, exponentially many queries are needed, and the same kind of argument gives the lower bounds for approximate Brouwer fixed points of Hirsch, Papadimitriou and Vavasis (1989). With circuits, the hardness rests on assumptions: Bitansky, Paneth and Rosen (2015) built hard instances from indistinguishability obfuscation and [one-way functions](/one-way-function/), and later work used weaker cryptographic assumptions.

## Reductions

- **To END OF THE LINE.** A problem is in PPAD if it reduces to END OF THE LINE. Nash equilibria of bimatrix games reduce by the Lemke-Howson path, and approximate Brouwer fixed points and Sperner triangles reduce by the path argument of the [Sperner lemma](/sperner-lemma/).
- **From END OF THE LINE.** Daskalakis, Goldberg and Papadimitriou (2006, 2009) reduced END OF THE LINE to a 3-dimensional Brouwer problem, then to [graphical games](/graphical-game/), and then to Nash equilibria of games with 3 or more players. Chen, Deng and Teng (2006, 2009) went down to 2 players. So all these problems are PPAD-complete.
- **Market equilibria.** Arrow-Debreu equilibria with piecewise-linear concave utilities are also PPAD-hard ([PPAD-hardness of Arrow-Debreu](/ppad-hardness-of-arrow-debreu/)).

## Applications

The problem is the main tool to show that a total search problem is unlikely to have a polynomial algorithm. A PPAD-completeness proof explains why path-following methods are slow on some inputs and why no simple formula is expected. The class contains equilibria of games and markets, approximate fixed points of continuous maps, and problems that a Sperner argument solves, such as [rental harmony](/rental-harmony/).

## References
