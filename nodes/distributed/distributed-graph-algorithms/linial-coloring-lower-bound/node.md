---
tag: 781NR6
kind: theorem
slug: linial-coloring-lower-bound
name: Linial's coloring lower bound
aliases:
- Linial lower bound for coloring
- Omega(log* n) coloring lower bound
area: distributed/distributed-graph-algorithms
level: advanced
summary: A deterministic LOCAL algorithm that 3-colours every directed n-cycle needs at least (1/2) log* n − 1 rounds. So Cole-Vishkin is optimal up to a factor 2.
prereqs: [local-model, ring-coloring, iterated-logarithm, chromatic-number]
see_also: [cole-vishkin, ring-coloring, linial-algorithm, distributed-vertex-coloring, distributed-mis, round-elimination, locally-checkable-labeling, kmw-lower-bound]
sources:
  - paper: doi:10.1137/0221015
    title: Nathan Linial, Locality in distributed graph algorithms, SIAM Journal on Computing 21(1), 1992
    locator: pp. 193 to 201 (the neighbourhood graph B(t, n), the bound on its chromatic number, and the (1/2) log* n − 1 lower bound for 3-colouring the n-cycle)
  - paper: doi:10.1145/2611462.2611505
    title: Juhana Laurinharju and Jukka Suomela, Brief announcement, Linial's lower bound made easy, PODC 2014
    locator: pp. 377 and 378 (the proof by k-ary colourings of increasing tuples, with the bound (1/2) log* n − 1 for directed cycles)
  - paper: doi:10.1137/0404036
    title: Moni Naor, A lower bound on probabilistic algorithms for distributive ring coloring, SIAM Journal on Discrete Mathematics 4(3), 1991
    locator: pp. 409 to 412 (the Omega(log* n) bound for randomized algorithms)
  - url: https://jukkasuomela.fi/da2020/
    title: Juho Hirvonen and Jukka Suomela, Distributed Algorithms 2020, online textbook
    locator: Chapter 1 (fast colouring of cycles) and Chapter 11 (hardness of colouring)
---

Linial's lower bound states that every deterministic algorithm in the [LOCAL model](/local-model/) that properly 3-colours every directed cycle of $n$ nodes needs at least $\frac{1}{2} \log^* n - 1$ rounds, where $\log^*$ is the [iterated logarithm](/iterated-logarithm/). It holds even though messages are unbounded, the cycle is oriented, and every node knows $n$. Together with [Cole-Vishkin](/cole-vishkin/) it shows that [ring colouring](/ring-coloring/) takes $\Theta(\log^* n)$ rounds, and it was the first lower bound on locality in distributed graph algorithms. The proof on this page is the one of Laurinharju and Suomela (2014), which gives the same bound as Linial's (1992) argument by a shorter route.

Notation on this page: a directed $n$-cycle has nodes $v_0, \dots, v_{n-1}$, each with an edge to its successor $v_{(j+1) \bmod n}$, and the identifiers are a permutation of $\{1, \dots, n\}$. $\operatorname{tower}(0) = 1$ and $\operatorname{tower}(j+1) = 2^{\operatorname{tower}(j)}$, and $\log^* n$ is the least $K \ge 0$ with $n \le \operatorname{tower}(K)$. A tuple $(x_1, \dots, x_k)$ is increasing if $x_1 < \dots < x_k$.

## Statement

**Theorem.** Let $n \ge 1$ and $t \ge 0$. Let $\mathcal{A}$ be a deterministic algorithm in the synchronous LOCAL model such that, on every directed $n$-cycle with identifiers $\{1, \dots, n\}$, every node outputs a colour in $\{1, 2, 3\}$ after $t$ rounds and adjacent nodes output different colours. Then

$$t \ge \tfrac{1}{2} \log^* n - 1.$$

The bound also holds for undirected cycles and for larger identifier spaces, since an algorithm for those cases also solves this one. Linial states the result through the **neighbourhood graph** $B_{t,n}$: its vertices are the $(2t+1)$-tuples of distinct identifiers, and $(x_1, \dots, x_{2t+1})$ is adjacent to $(x_2, \dots, x_{2t+2})$ whenever $x_1, \dots, x_{2t+2}$ are distinct. For $n \ge 2t + 2$, a $t$-round algorithm with $c$ colours exists exactly when the chromatic number of $B_{t,n}$ is at most $c$, and Linial proves that this chromatic number is at least $\log^{(2t)} n$, the logarithm iterated $2t$ times.

## In plain words

After a few rounds, a computer on a ring knows only the serial numbers near it. Its colour is a fixed function of that short list. Two neighbours see lists that overlap in all but one number, and their colours must differ.

Take such a rule for lists of some length. Build a rule for lists one number shorter: the new colour of a short list is the set of all old colours that its longer versions get. Neighbours still get different colours, but the number of colours grows from some number to two raised to that number. Repeat until the lists have length one. Then every serial number needs its own colour, so the number of serial numbers is at most a tower of twos whose height is about twice the number of rounds.

## Proof

Let $k = 2t + 1$.

*Small cycles.* If $n \le k$, then $t \ge (n - 1)/2 \ge \frac{1}{2} \log^* n - 1$, because $\log^* n \le n$ for every $n \ge 1$. So assume $n \ge k + 1 = 2t + 2$.

*Step 1: from the algorithm to a colouring of tuples.* In $t$ rounds of the LOCAL model, the output of a node depends only on what lies within distance $t$ of it. On a directed cycle with $n \ge 2t + 2$ this is the path of $2t + 1$ nodes centred at the node, with their identifiers in cycle order, plus the value $n$, which is fixed. So there is a function $A$ with $\mathcal{A}(v_j) = A(x_{j-t}, \dots, x_{j+t})$, where $x_i$ is the identifier of $v_{i \bmod n}$. Let $x_1 < \dots < x_{k+1}$ be any increasing tuple from $\{1, \dots, n\}$. Since $n \ge k + 1$, some directed $n$-cycle carries $x_1, \dots, x_{k+1}$ on $k + 1$ consecutive nodes, with the other identifiers placed on the other nodes in any order. The nodes that see $(x_1, \dots, x_k)$ and $(x_2, \dots, x_{k+1})$ are adjacent, so $A(x_1, \dots, x_k) \ne A(x_2, \dots, x_{k+1})$.

Call a function $f$ on the increasing $k$-tuples of $\{1, \dots, n\}$ a **proper $k$-ary $c$-colouring** if it takes at most $c$ values and $f(x_1, \dots, x_k) \ne f(x_2, \dots, x_{k+1})$ for every increasing $(k+1)$-tuple. Step 1 shows that $A$, restricted to increasing tuples, is a proper $k$-ary 3-colouring.

*Step 2: one arity less.* Let $k \ge 2$ and let $f$ be a proper $k$-ary $c$-colouring. For an increasing $(k-1)$-tuple, define

$$g(x_1, \dots, x_{k-1}) = \{\, f(x_1, \dots, x_{k-1}, y) : x_{k-1} < y \le n \,\}.$$

The value of $g$ is a subset of the $c$ colours of $f$, so $g$ takes at most $2^c$ values. Assume, for a contradiction, that $g(x_1, \dots, x_{k-1}) = g(x_2, \dots, x_k)$ for some increasing $k$-tuple $x_1 < \dots < x_k$. The colour $a = f(x_1, \dots, x_k)$ lies in $g(x_1, \dots, x_{k-1})$, since $x_k > x_{k-1}$. So $a$ lies in $g(x_2, \dots, x_k)$, and $a = f(x_2, \dots, x_k, y)$ for some $y > x_k$. But $(x_1, \dots, x_k, y)$ is an increasing $(k+1)$-tuple, so $f(x_1, \dots, x_k) \ne f(x_2, \dots, x_k, y)$, which contradicts the choice of $y$. So $g$ is a proper $(k-1)$-ary $2^c$-colouring.

*Step 3: arity one.* A proper 1-ary $c$-colouring $f$ has $f(x) \ne f(y)$ for all $x < y$, so it is one-to-one on $\{1, \dots, n\}$, and $c \ge n$.

*Step 4: counting.* Let $c_1 = 3$ and $c_{j+1} = 2^{c_j}$. Starting from the $k$-ary 3-colouring of Step 1 and applying Step 2 exactly $k - 1$ times gives a proper 1-ary colouring with at most $c_k$ colours, so $n \le c_k$ by Step 3. By induction, $c_j < \operatorname{tower}(j + 1)$: for $j = 1$, $3 < 4 = \operatorname{tower}(2)$, and $c_{j+1} = 2^{c_j} < 2^{\operatorname{tower}(j+1)} = \operatorname{tower}(j + 2)$. So $n < \operatorname{tower}(k + 1)$, which gives $\log^* n \le k + 1 = 2t + 2$, that is, $t \ge \frac{1}{2} \log^* n - 1$. $\blacksquare$

## Consequences

- **Colouring with any constant number of colours.** A proper $c$-colouring of a cycle becomes a 3-colouring in $c - 3$ more rounds, by removing one colour class per round. So $c$ colours need $\frac{1}{2} \log^* n - c + 2$ rounds. In particular, [distributed $(\Delta + 1)$-colouring](/distributed-vertex-coloring/) needs $\Omega(\log^* n)$ rounds, since a cycle has $\Delta = 2$.
- **Maximal independent set.** From an MIS of a cycle, a 3-colouring follows in 1 round. Between two consecutive members lie one or two other nodes, because each non-member has a member neighbour. Members take colour 1; a non-member takes colour 2 if its other neighbour is a member or has a larger identifier, and colour 3 otherwise. So [distributed MIS](/distributed-mis/) on cycles needs $\frac{1}{2} \log^* n - O(1)$ rounds.
- **Maximal matching.** From a maximal matching of a directed cycle, a 3-colouring follows in 1 round: the tail of each matched edge takes colour 1, its head colour 2, and an unmatched node colour 3. Two unmatched nodes are never adjacent, and the node after a head is a tail or unmatched, so the colouring is proper. So [distributed maximal matching](/distributed-maximal-matching/) on cycles needs $\frac{1}{2} \log^* n - O(1)$ rounds.
- **Ruling sets.** A $(2, \beta)$-[ruling set](/ruling-set/) of a cycle leaves gaps of at most $2\beta$ nodes, and each gap can compute an MIS of its own nodes in $O(\beta)$ rounds. So a ruling set with constant $\beta$ also needs $\Omega(\log^* n)$ rounds on cycles.
- **A gap for local problems.** On cycles, every [locally checkable problem](/locally-checkable-labeling/) has complexity $O(1)$, $\Theta(\log^* n)$ or $\Theta(n)$; this bound is the lower end of the middle class.
- **Randomization.** Naor (1991) proves that randomized algorithms also need $\Omega(\log^* n)$ rounds to 3-colour a ring.

## Tightness

The bound is tight up to an additive constant. [Cole-Vishkin](/cole-vishkin/) 3-colours a directed cycle in $\log^* n + O(1)$ rounds by reading one successor per round. A node that reads $t$ nodes on each side can run $2t$ steps of the same method for the node $t$ positions behind it, which gives $\frac{1}{2} \log^* n + O(1)$ rounds; the [ring colouring](/ring-coloring/) page has the details.

Step 2 loses almost nothing for $k = 2$. The increasing pairs of $\{0, \dots, n-1\}$ with the edges $(x, y) \sim (y, z)$ form a graph with chromatic number exactly $\lceil \lg n \rceil$. A colouring with that many colours gives $(x, y)$ the index of the highest bit where $x$ and $y$ differ: if $(x, y)$ and $(y, z)$ got the same index $i$, then bit $i$ of $y$ would be 1 (as $x < y$) and 0 (as $y < z$). This is the deterministic coin tossing step of Cole-Vishkin.

For tiny cases the chromatic number of $B_{t,n}$ is small: $B_{0,n}$ is the complete graph on $n$ vertices, with chromatic number $n$. For one round, $B_{1,4}$ has chromatic number 2 and $B_{1,5}$ and $B_{1,6}$ have chromatic number 3. So one round suffices to 3-colour directed cycles of up to 6 nodes with identifiers $\{0, \dots, n-1\}$, and zero rounds do not suffice for 3 colours once $n \ge 4$.

## History

Linial proved the bound in a FOCS 1987 paper, published in the journal in 1992, through the chromatic number of the neighbourhood graph $B_{t,n}$, and in the same paper gave the matching $O(\log^* n)$ upper bound for $O(\Delta^2)$ colours on all graphs. Naor (1991) extended it to randomized algorithms. Laurinharju and Suomela (2014) gave the short proof on this page, by colourings of increasing tuples, for the same bound $\frac{1}{2} \log^* n - 1$.

## References
