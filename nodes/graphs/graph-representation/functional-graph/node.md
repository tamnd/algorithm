---
tag: XK541X
kind: concept
slug: functional-graph
name: Functional graph
area: graphs/graph-representation
level: core
summary: Directed graph in which every vertex has exactly one outgoing edge, so each component has one cycle with trees feeding it.
prereqs: [directed-graph, degree]
see_also: [floyd-cycle-detection, brent-cycle-detection, pollard-rho, permutation-cycle-decomposition, binary-lifting, rooted-tree, disjoint-set, implicit-graph]
sources:
  - paper: "Philippe Flajolet and Andrew M. Odlyzko, Random mapping statistics, Advances in Cryptology, EUROCRYPT '89, Lecture Notes in Computer Science 434, Springer, 1990"
    locator: pages 329 to 354, the expected number of components, of cyclic points and of terminal and cyclic nodes, and the expected tail and cycle lengths of a random mapping
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 3.1 (Introduction), the exercises on the period and the tail of a sequence x_{n+1} = f(x_n) over a finite set, with Floyd's cycle-finding method
  - paper: "John M. Pollard, A Monte Carlo method for factorization, BIT Numerical Mathematics 15(3), 1975"
    locator: pages 331 to 334, the iteration x ↦ x^2 + c mod n and the detection of its cycle modulo a prime factor
---

A functional graph is the [directed graph](/directed-graph/) of a function $f : V \to V$ on a finite set: its vertices are the elements of $V$ and its edges are the pairs $(v, f(v))$, so each vertex has out-[degree](/degree/) exactly 1. Following the edges from any vertex traces the sequence $v, f(v), f(f(v)), \ldots$, which must repeat, so each weakly connected component of the graph is one directed cycle with [rooted trees](/rooted-tree/) hanging from it, their edges pointing toward the cycle. The whole graph is stored in an array of $n$ entries, and its structure is the base of [cycle detection](/floyd-cycle-detection/), of [Pollard's rho method](/pollard-rho/), of [permutation cycles](/permutation-cycle-decomposition/) and of [binary lifting](/binary-lifting/).

## In plain words

Each item points to exactly one item, maybe to itself. Start anywhere and keep following the pointers. Since there are only finitely many items, you must come back to an item you have seen, and from then on you go round a loop forever. The path you walk looks like the Greek letter rho: a tail and then a loop.

Look at the whole picture and you see a few loops. Into each loop run branches, and into the branches run smaller branches, like trees whose roots sit on the loop. That is all a functional graph can look like. A parent array of a forest, a permutation and a random number generator with a finite state are all examples.

## The idea

**Definition.** Let $V$ be a finite set with $n = |V|$ and $f : V \to V$ a function. The *functional graph* of $f$ is $G_f = (V, \{(v, f(v)) : v \in V\})$. It is a directed graph with self-loops allowed and $m = n$ edges, and each vertex has out-degree exactly 1. Conversely, each directed graph in which each vertex has out-degree exactly 1 is $G_f$ for exactly one $f$, so there are $n^n$ functional graphs on a labelled set of $n$ vertices. In-degrees are arbitrary: $d^-(v) = |f^{-1}(v)|$, and they sum to $n$. A directed graph with out-degree at most 1 is a *partial* functional graph; the vertices with out-degree 0 act as roots.

**Structure theorem.** Call $v$ *cyclic* when $f^k(v) = v$ for some $k \ge 1$. Then:

1. For each $v$ there are unique numbers $\mu(v) \ge 0$, the *tail length*, and $\lambda(v) \ge 1$, the *cycle length*, such that $v, f(v), \ldots, f^{\mu + \lambda - 1}(v)$ are distinct and $f^{\mu + \lambda}(v) = f^{\mu}(v)$.
2. The cyclic vertices are exactly those with $\mu(v) = 0$. On them $f$ is a [permutation](/permutation/), so they split into disjoint directed cycles.
3. Each weakly connected component of $G_f$ contains exactly one cycle.
4. Removing the edges of the cycles leaves a forest in which each tree is rooted at a cyclic vertex and each edge $(v, f(v))$ points from a child to its parent.

*Proof.* (1) The sequence $x_i = f^i(v)$ takes values in a set of $n$ elements, so some value repeats; let $j$ be the least index such that $x_j = x_i$ for some $i < j$, and set $\mu = i$, $\lambda = j - i$. Then $x_0, \ldots, x_{j-1}$ are distinct and $x_j = x_\mu$, and $\mu$ and $\lambda$ are unique by the choice of $j$. Since each $x_{k+1}$ is determined by $x_k$, the sequence repeats with period $\lambda$ from index $\mu$ on.

(2) If $\mu(v) = 0$ then $f^{\lambda}(v) = v$, so $v$ is cyclic. If $v$ is cyclic with $f^k(v) = v$, the sequence of $v$ returns to $x_0$, so its first repeat is of $x_0$, and $\mu(v) = 0$. The map $f$ sends a cyclic $v$ to the cyclic $f(v)$, and on the finite set $C$ of cyclic vertices it is onto, since $v = f(f^{k-1}(v))$, so it is a bijection of $C$.

(3) A component has $p$ vertices and, since each of them has one out-edge and no out-edge leaves the component, exactly $p$ edges. A connected graph with $p$ vertices and $p$ edges, viewed as undirected, has exactly one cycle, counting a loop or a pair of opposite edges as a cycle: a spanning tree uses $p - 1$ edges, and the one remaining edge closes one cycle. The directed cycle that each sequence in the component reaches is such a cycle, so it is the only one.

(4) Delete the edge out of each cyclic vertex. Now each vertex $v$ that is not cyclic has its one out-edge, and following it reaches a cyclic vertex after $\mu(v)$ steps without repeating a vertex. So the remaining graph has no cycle, each non-cyclic vertex has one parent, and each cyclic vertex is a root. $\square$

**Representation.** A functional graph is stored as the array $f[0 \ldots n-1]$ of $n$ vertex numbers. The out-neighbour of $v$ is $f[v]$, found in $O(1)$ time, and the edge query $(u, v)$ is the test $f[u] = v$ in $O(1)$ time. The in-neighbours are not stored; a [compressed sparse column](/compressed-sparse-column/) array of the reverse edges, built in $\Theta(n)$ time, lists them. When $f$ is given as a rule, such as $x \mapsto x^2 + 1 \bmod N$, the graph is an [implicit graph](/implicit-graph/) and is never stored.

**Finding the structure.** All cycles, tails and trees are found in $\Theta(n)$ time and space. One way peels the trees: compute the in-degrees, put each vertex of in-degree 0 in a queue, and repeatedly remove a vertex $v$ from the queue and decrease the in-degree of $f(v)$, adding $f(v)$ to the queue when it reaches 0. The vertices never removed are exactly the cyclic ones, since a vertex on a cycle always keeps its in-edge from the cycle. A walk around each cycle then labels its vertices.

**Cycle detection in $O(1)$ space.** When $f$ is a rule and $n$ is huge, storing the visited vertices is not possible. [Floyd's method](/floyd-cycle-detection/) runs a slow pointer $x_i$ and a fast pointer $x_{2i}$; they meet at the first $i \ge 1$ that is a multiple of $\lambda$ and at least $\mu$, so after at most $\mu + \lambda$ steps. Then $\mu$ and $\lambda$ follow by two more walks. [Brent's method](/brent-cycle-detection/) finds $\lambda$ with fewer evaluations of $f$ by moving the slow pointer only at powers of two.

**Random mappings.** For $f$ chosen uniformly among the $n^n$ functions, Flajolet and Odlyzko give the expected values, as $n \to \infty$: about $\frac{1}{2} \ln n$ components, about $\sqrt{\pi n / 2}$ cyclic vertices, and, for a random start vertex, a tail length and a cycle length of about $\sqrt{\pi n / 8}$ each. So the rho of a random start has about $\sqrt{\pi n / 2}$ distinct vertices, which is the birthday bound, and the reason that Pollard's methods take about $\sqrt{n}$ steps.

## Examples

**A small graph.** Let $V = \{0, \ldots, 9\}$ and

| $v$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| $f(v)$ | 1 | 2 | 0 | 2 | 3 | 6 | 5 | 6 | 8 | 8 |

It has three components. The first has the cycle $0 \to 1 \to 2 \to 0$ and the tail $4 \to 3 \to 2$, a path that is a tree rooted at 2. The second has the cycle $5 \to 6 \to 5$ and the leaf 7 attached to 6. The third has the loop $8 \to 8$ and the leaf 9. The cyclic vertices are $0, 1, 2, 5, 6, 8$, and $f$ restricted to them is the permutation with the cycles $(0\,1\,2)(5\,6)(8)$. The in-degrees are $1, 1, 2, 1, 0, 1, 2, 0, 2, 0$, which sum to 10.

**Floyd's method from 4.** The sequence is $x = 4, 3, 2, 0, 1, 2, 0, 1, 2, \ldots$, so $\mu(4) = 2$ and $\lambda(4) = 3$. The slow and fast pointers compare $x_1 = 3$ with $x_2 = 2$, then $x_2 = 2$ with $x_4 = 1$, then $x_3 = 0$ with $x_6 = 0$, and meet at $i = 3$. Restarting one pointer at $x_0$ and moving both by one step compares $x_0 = 4$ with $x_3 = 0$, $x_1 = 3$ with $x_4 = 1$, and $x_2 = 2$ with $x_5 = 2$, so $\mu = 2$. Walking from $x_2 = 2$ until it returns gives $2, 0, 1, 2$, so $\lambda = 3$.

**Peeling the trees.** The vertices of in-degree 0 are 4, 7 and 9. Removing them lowers the in-degrees of 3, 6 and 8 to 0, 1 and 1. Then 3 is removed, which lowers the in-degree of 2 to 1. No vertex has in-degree 0 any more, and the remaining vertices $0, 1, 2, 5, 6, 8$ are the cyclic ones.

**Counting.** The number of connected functional graphs on $n$ labelled vertices is $(n-1)! \sum_{k=0}^{n-1} n^k / k!$, which gives $1, 3, 17, 142, 1569$ for $n = 1, \ldots, 5$, out of $n^n = 1, 4, 27, 256, 3125$ in all. For $n = 2$ the only disconnected one is the identity, with two loops.

**Special cases.**

- A [permutation](/permutation/) is a functional graph in which each vertex is cyclic, so all in-degrees are 1 and there are no trees.
- The parent array of a [rooted tree](/rooted-tree/) or a forest, with each root pointing to itself, is a functional graph whose cycles are all loops. This is the array of a [disjoint-set](/disjoint-set/) forest.
- A constant function $f(v) = c$ is a star of $n - 1$ leaves pointing into the loop at $c$.
- A singly linked list in which the last node points back to some earlier node is the rho of a single start vertex.

**Non-examples.** A directed graph in which some vertex has two out-edges, such as a vertex with edges to two children in a tree drawn from the root down, is not a functional graph; reverse its edges to get one. An undirected cycle is not a functional graph, since an undirected edge has no direction.

## Where it is used

- **Cycle detection.** [Floyd's](/floyd-cycle-detection/) and [Brent's](/brent-cycle-detection/) methods find $\mu$ and $\lambda$ of a sequence $x_{i+1} = f(x_i)$ with $O(1)$ memory: the period of a pseudo-random generator, a loop in a linked list, or a repeated state of a simulation.
- **Integer factorization and discrete logarithms.** [Pollard's rho method](/pollard-rho/) iterates $x \mapsto x^2 + c \bmod N$; modulo an unknown prime factor $p$ of $N$, the sequence is a walk in a functional graph on $p$ vertices and closes its cycle after about $\sqrt{p}$ steps, which reveals $p$ as a greatest common divisor. [Rho collision search](/pollard-rho-collision-search/) uses the same idea for discrete logarithms and hash collisions.
- **Permutations.** The [cycle decomposition of a permutation](/permutation-cycle-decomposition/) is the cycle structure of its functional graph, found in $\Theta(n)$ time by following each cycle once.
- **Repeated application.** [Binary lifting](/binary-lifting/) stores $f^{2^j}$ for $j = 0, \ldots, \lfloor \log_2 k \rfloor$, and then computes $f^k(v)$ in $O(\log k)$ time, from $O(n \log k)$ precomputation. On the parent array of a tree this gives [lowest common ancestors](/lowest-common-ancestor/).
- **Union-find.** The parent array of a [disjoint-set](/disjoint-set/) structure is a functional graph whose cycles are the loops at the roots, and FIND follows its edges.
- **Deterministic automata.** For each fixed input letter, the transition function of a deterministic finite automaton is a function on its states, so its functional graph shows the eventual behaviour of a long run of that letter.

## References
