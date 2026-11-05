---
tag: QM5K9J
kind: problem
slug: dominators-problem
name: Dominators problem
aliases:
- immediate dominators
area: graphs/tree-algorithms
level: advanced
summary: For each vertex of a rooted directed graph, find its immediate dominator.
prereqs: [directed-graph, reachability, depth-first-search, rooted-tree]
see_also: [dominator-tree, lengauer-tarjan-algorithm, articulation-point, block-cut-tree, transpose-graph, directed-acyclic-graph, lowest-common-ancestor, path-compression]
sources:
  - paper: doi:10.1145/357062.357071
    title: "Thomas Lengauer and Robert Endre Tarjan, A fast algorithm for finding dominators in a flowgraph, ACM Transactions on Programming Languages and Systems 1(1) (1979), 121-141"
    locator: Section 1 (the definitions of flowgraph, dominator and immediate dominator, and the history of earlier algorithms) and Sections 2 and 3 (the semidominator theorems and the O(m log n) and O(m alpha(m, n)) versions)
  - paper: "Edward S. Lowry and C. W. Medlock, Object code optimization, Communications of the ACM 12(1) (1969), 13-22"
    locator: the use of dominators to find loops in the FORTRAN H compiler, and the first algorithm to compute them
  - paper: "Paul W. Purdom Jr. and Edward F. Moore, Immediate predominators in a directed graph, Communications of the ACM 15(8) (1972), 777-778"
    locator: the algorithm that removes each vertex in turn and tests reachability
  - paper: "Stephen Alstrup, Dov Harel, Peter W. Lauridsen and Mikkel Thorup, Dominators in linear time, SIAM Journal on Computing 28(6) (1999), 2117-2132"
    locator: the whole paper (a linear-time algorithm on a RAM)
  - paper: "Adam L. Buchsbaum, Loukas Georgiadis, Haim Kaplan, Anne Rogers, Robert E. Tarjan and Jeffery R. Westbrook, Linear-time algorithms for dominators and other path-evaluation problems, SIAM Journal on Computing 38(4) (2008), 1533-1573"
    locator: the whole paper (linear time on a RAM and on a pointer machine)
  - url: https://www.cs.rice.edu/~keith/EMBED/dom.pdf
    title: "Keith D. Cooper, Timothy J. Harvey and Ken Kennedy, A Simple, Fast Dominance Algorithm"
    locator: the iterative algorithm over the reverse postorder with the two-finger intersection, and the experiments against Lengauer-Tarjan
---

In a directed graph with a start vertex $r$, a vertex $d$ *dominates* a vertex $v$ if every path from $r$ to $v$ passes through $d$. Among the dominators of $v \ne r$ there is a unique one closest to $v$, its *immediate dominator* $\mathrm{idom}(v)$, and the dominators problem asks for $\mathrm{idom}(v)$ for every vertex reachable from $r$. The answers form a tree rooted at $r$, the [dominator tree](/dominator-tree/), in which the dominators of $v$ are exactly its ancestors. The problem comes from compilers, where dominators find loops and place the phi-functions of static single assignment form. It is solved in $O(m \log n)$ time by the simple [Lengauer-Tarjan algorithm](/lengauer-tarjan-algorithm/), and in $O(n + m)$ time by more complex methods.

## In plain words

Think of a building with one entrance and many rooms joined by one-way doors. A room "guards" another room if you cannot reach the second room from the entrance without walking through the first. The entrance guards every room, and every room guards itself.

For each room, we want the guard that stands closest to it: the last room you are forced to pass on every possible way in. Those closest guards fit together into a family tree, with the entrance at the top, and the guards of a room are exactly the rooms above it in that tree. The problem is to find this tree quickly, even for a building with a million rooms.

## Definition

A *flow graph* is a directed graph $G = (V, E)$ with $n$ vertices, numbered $0, \ldots, n - 1$, $m$ edges, and a start vertex $r$ from which every vertex is reachable. (Vertices that $r$ cannot reach are dropped first; no path reaches them, so dominance is not defined for them.) The graph is unweighted, and self-loops and parallel edges are allowed and do not matter.

- $d$ **dominates** $v$, written $d \;\mathrm{dom}\; v$, if every path from $r$ to $v$ contains $d$. Every vertex dominates itself, and $r$ dominates every vertex.
- $d$ **strictly dominates** $v$ if $d$ dominates $v$ and $d \ne v$.
- For $v \ne r$, the **immediate dominator** $\mathrm{idom}(v)$ is the strict dominator of $v$ that is dominated by every other strict dominator of $v$.

The strict dominators of $v$ all lie on every path from $r$ to $v$, and on a simple path they appear in the same order each time, so they are totally ordered by dominance and $\mathrm{idom}(v)$ exists and is unique. The **dominators problem**: given $G$ and $r$, output $\mathrm{idom}(v)$ for every vertex $v \ne r$.

## Variants

- **Postdominators.** In a graph with an exit vertex $x$, $d$ postdominates $v$ if every path from $v$ to $x$ contains $d$. These are the dominators of the [transpose graph](/transpose-graph/) with start $x$.
- **All dominators of each vertex.** The full relation can have $\Theta(n^2)$ pairs, so it is given implicitly by the dominator tree, which answers "does $d$ dominate $v$" in $O(1)$.
- **Acyclic flow graphs.** In a [directed acyclic graph](/directed-acyclic-graph/), processing vertices in topological order, $\mathrm{idom}(v)$ is the [lowest common ancestor](/lowest-common-ancestor/), in the partial dominator tree, of all predecessors of $v$.
- **Undirected graphs.** Every edge can be used both ways, and a vertex $d \notin \{r, v\}$ dominates $v$ exactly when $d$ is an [articulation point](/articulation-point/) that separates $r$ from $v$; the dominator tree follows from the [block-cut tree](/block-cut-tree/) rooted at the block of $r$.
- **Dynamic dominators.** Maintain the dominator tree while edges are inserted or deleted.

## Examples

Take the flow graph on $0, \ldots, 8$ with start 0 and the 11 edges

$$0 \to 1,\; 1 \to 2,\; 2 \to 3,\; 2 \to 4,\; 3 \to 4,\; 3 \to 7,\; 4 \to 5,\; 5 \to 6,\; 6 \to 3,\; 7 \to 8,\; 8 \to 6.$$

| $v$ | strict dominators | $\mathrm{idom}(v)$ | why |
|---|---|---|---|
| 1 | 0 | 0 | |
| 2 | 0, 1 | 1 | the only way in is $0 \to 1 \to 2$ |
| 3 | 0, 1, 2 | 2 | reached by $2 \to 3$ or by $2 \to 4 \to 5 \to 6 \to 3$ |
| 4 | 0, 1, 2 | 2 | reached by $2 \to 4$ or $3 \to 4$ |
| 5 | 0, 1, 2, 4 | 4 | its only predecessor is 4 |
| 6 | 0, 1, 2 | 2 | $2 \to 4 \to 5 \to 6$ avoids 3, and $2 \to 3 \to 7 \to 8 \to 6$ avoids 4 and 5 |
| 7 | 0, 1, 2, 3 | 3 | its only predecessor is 3 |
| 8 | 0, 1, 2, 3, 7 | 7 | its only predecessor is 7 |

So $\mathrm{idom} = [-, 0, 1, 2, 2, 4, 2, 3, 7]$. The dominator tree has root 0 with child 1, then 2, whose children are 3, 4 and 6; 4 has child 5, and 3 has child 7, which has child 8. Vertex 6 shows that the immediate dominator need not be a predecessor: its predecessors are 5 and 8, neither of which dominates it.

Simple shapes:

- **A single vertex.** $n = 1$, no edges, and the output is empty.
- **A path** $0 \to 1 \to \cdots \to n - 1$. $\mathrm{idom}(v) = v - 1$, and the dominator tree is the path.
- **A star** $0 \to v$ for $v = 1, \ldots, n - 1$. $\mathrm{idom}(v) = 0$ for all $v$, even if edges between the leaves are added.
- **A diamond** $0 \to 1, 0 \to 2, 1 \to 3, 2 \to 3$. $\mathrm{idom}(3) = 0$, because the two branches bypass each other.

## Known algorithms

| algorithm | time | notes |
|---|---|---|
| remove each vertex and test reachability (Purdom and Moore 1972) | $O(n(n + m))$ | the definition, run directly |
| iterative data flow, $\mathrm{Dom}(v) = \{v\} \cup \bigcap_{u \to v} \mathrm{Dom}(u)$ | $O(n^2)$ per pass with bit vectors | several passes; Lowry and Medlock (1969) used a version of it |
| Cooper, Harvey and Kennedy (2001) | quadratic on some families of graphs | iterates on $\mathrm{idom}$ in reverse postorder; fast in practice on control-flow graphs |
| [Lengauer-Tarjan](/lengauer-tarjan-algorithm/), simple version | $O(m \log n)$ | DFS, semidominators, [path compression](/path-compression/) |
| Lengauer-Tarjan, sophisticated version | $O(m\, \alpha(m, n))$ | balanced linking |
| Alstrup, Harel, Lauridsen and Thorup (1999) | $O(n + m)$ | on a RAM |
| Buchsbaum, Georgiadis, Kaplan, Rogers, Tarjan and Westbrook (2008) | $O(n + m)$ | on a RAM and on a pointer machine |

The iterative data-flow method starts with $\mathrm{Dom}(r) = \{r\}$ and $\mathrm{Dom}(v) = V$ for the others, and repeats the equation until nothing changes; the result is the largest solution, which is the dominator relation. The Cooper-Harvey-Kennedy algorithm stores only $\mathrm{idom}$ and computes the intersection of two dominator sets by walking up the current tree with two fingers.

## Bounds

- **Upper bound.** $O(n + m)$ time (Alstrup et al. 1999; Buchsbaum et al. 2008).
- **Lower bound.** $\Omega(n + m)$, since every edge may matter: deleting one edge can change $\mathrm{idom}$ of a vertex.
- **Output size.** $n - 1$ numbers, although the dominance relation itself may have $\Theta(n^2)$ pairs, as on a path.

## Reductions

- **Dominance to reachability.** For $d \ne v$, $d$ dominates $v$ if and only if $v$ is not reachable from $r$ in $G - d$. This gives the $O(n(n + m))$ algorithm.
- **Postdominators to dominators.** Reverse every edge and start from the exit.
- **Acyclic dominators to LCA.** In topological order, $\mathrm{idom}(v)$ is the LCA of the predecessors of $v$ in the dominator tree built so far; with [binary lifting](/binary-lifting/), which lets leaves be added, this takes $O(m \log n)$ time.
- **Undirected dominators to articulation points.** As in the Variants section, through the block-cut tree.

## Applications

- **Loops in compilers.** An edge $u \to h$ whose head $h$ dominates its tail $u$ is a back edge; the natural loop of $h$ is $h$ and the vertices that reach $u$ without passing $h$. This was the original use of dominators.
- **Static single assignment form.** Phi-functions are placed on the dominance frontiers, which are computed from the dominator tree (Cytron, Ferrante, Rosen, Wegman and Zadeck, 1991).
- **Control dependence.** Postdominators tell which branches decide whether a statement runs.
- **Memory analysis.** In a heap snapshot with the roots as start, an object dominates everything it alone keeps alive, and the *retained size* of an object is the total size of its subtree in the dominator tree.
- **Connectivity of directed graphs.** The strong articulation points and the two-vertex connectivity of a directed graph can be found with dominator trees in linear time (Italiano, Laura and Santaroni, 2012).

## References
