---
tag: CPHQYA
kind: technique
slug: pebbling-lower-bound
name: Pebbling lower bound
aliases:
- Hong-Kung lower bound
- red-blue pebbling argument
- S-partition argument
area: foundations/lower-bounds
level: advanced
summary: Proves that a fixed computation DAG needs many I/O moves with S words of fast memory, by showing that every part of a 2S-partition of the DAG is small, so the DAG needs many parts.
prereqs: [red-blue-pebble-game, directed-acyclic-graph, external-memory-model]
see_also: [external-sorting-lower-bound, blocked-matrix-multiplication, fast-fourier-transform, fft-lower-bound, strassen-algorithm, cache-oblivious-model, memory-hierarchy, counting-argument]
sources:
  - paper: doi:10.1145/800076.802486
    title: "Hong Jia-Wei and H. T. Kung, I/O complexity: The red-blue pebble game, Proceedings of the 13th Annual ACM Symposium on Theory of Computing (1981), 326-333"
    locator: Section 3 (S-partitions, Theorem 3.1 and Lemma 3.1), Theorem 4.1 (FFT), Theorem 5.1 and Corollaries 5.1 and 5.2 (information speed, odd-even transposition sort, snake-like mesh), Theorem 6.1 (independent evaluation), Section 7 (products of graphs)
  - paper: doi:10.1016/j.jpdc.2004.03.021
    title: "Dror Irony, Sivan Toledo and Alexander Tiskin, Communication lower bounds for distributed-memory matrix multiplication, Journal of Parallel and Distributed Computing 64(9) (2004), 1017-1026"
    locator: the projection argument with the Loomis-Whitney inequality
  - paper: doi:10.1090/S0002-9904-1949-09320-5
    title: "L. H. Loomis and H. Whitney, An inequality related to the isoperimetric inequality, Bulletin of the American Mathematical Society 55(10) (1949), 961-962"
    locator: the inequality between the size of a set of lattice points and the sizes of its projections
  - paper: doi:10.1145/2395116.2395121
    title: "Grey Ballard, James Demmel, Olga Holtz and Oded Schwartz, Graph expansion and communication costs of fast matrix multiplication, Journal of the ACM 59(6) (2012)"
    locator: abstract (edge expansion in place of partitions, the bound for Strassen-like algorithms)
  - paper: doi:10.1145/322003.322015
    title: "John Hopcroft, Wolfgang Paul and Leslie Valiant, On Time Versus Space, Journal of the ACM 24(2) (1977), 332-337"
    locator: the black pebble game and the space bound O(n/log n) for graphs of bounded in-degree
  - paper: doi:10.1007/BF01683275
    title: "Wolfgang J. Paul, Robert Endre Tarjan and James R. Celoni, Space bounds for a game on graphs, Mathematical Systems Theory 10(1) (1976), 239-251"
    locator: graphs of bounded in-degree that need Omega(n/log n) black pebbles
  - url: https://cs.brown.edu/people/jsavage/book/
    title: "John E. Savage, Models of Computation: Exploring the Power of Computing"
    locator: Chapter 10 (space-time tradeoffs) and Chapter 11 (memory-hierarchy tradeoffs, Section 11.1 the red-blue pebble game, Section 11.2 the memory-hierarchy pebble game)
---

The pebbling lower bound is the method of Hong and Kung (1981) for proving that a computation needs many moves between a small fast memory and a large slow memory. The computation is a fixed [directed acyclic graph](/directed-acyclic-graph/), and the moves are those of the [red-blue pebble game](/red-blue-pebble-game/). The method cuts any play into pieces with few I/O moves, turns each piece into a part of the graph with a small boundary, and then proves that a part with a small boundary has few vertices. Few vertices per part means many parts, and many parts means many I/O moves.

## In plain words

A program with a small fast memory can only work on a little data at a time. Cut the run of the program into pieces, each with a fixed small number of transfers. Inside one piece, everything the program computes must come from a small set of values: the values that were already in fast memory at the start of the piece, and the values that it brought in during the piece. So each piece can only cover a small region of the computation.

The proof work is in one question about the shape of the computation: how many steps can depend on a small set of values? If the answer is "few", the computation splits into many pieces, and each piece costs a fixed number of transfers. So the whole computation costs many transfers, whatever order the program uses.

## When it applies

- The algorithm is fixed as a DAG: every vertex is a value, and its predecessors are the values it is computed from. The bound is for this one DAG, not for the problem that it solves.
- The memory model is a fast memory of $S$ words and an unbounded slow memory, and the cost is the number of words moved between them. With blocks of $B$ words, divide by $B$ (see Variations).
- Every vertex is an ancestor of an output, and each vertex has in-degree at most $S - 1$, so that a play exists.
- The method gives something useful when the DAG has many more vertices than inputs and outputs, and when every vertex depends on many inputs. For a DAG where a small set of values feeds a large region, such as a chain that sums $n$ inputs, the method gives no more than the trivial bound "read each input once".

## The template

Write $G = (V, E)$ for the DAG and $S$ for the number of red pebbles. Use the definitions of the [red-blue pebble game](/red-blue-pebble-game/) page: a $2S$-partition of $G$ cuts $V$ into parts $V_1, \ldots, V_h$ with no edge from a later part to an earlier one, where each part has a dominator set of at most $2S$ vertices and a minimum set of at most $2S$ vertices. $H(2S)$ is the smallest $h$ for which a $2S$-partition exists. The Hong and Kung lemma says that every play makes at least $S\,(H(2S) - 1)$ I/O moves. Hong and Kung prove it with recomputation allowed (Lemma 3.1 of their paper).

1. **Fix the graph.** Write the vertices with coordinates, such as $(i, j)$ for a table or $(i, j, k)$ for the products of matrix multiplication. Write the predecessors of each vertex.
2. **Bound one part.** Take any set $U \subseteq V$ that has a dominator set $D$ with $|D| \le 2S$ and a minimum set with at most $2S$ vertices. Prove $|U| \le F(2S)$ for some function $F$. This is the only step that depends on the graph. Two facts help:
   - Each input in $U$ is in $D$, because the path of length zero from the input to itself must meet $D$.
   - For each vertex $u \in U \setminus D$, every path from an input to $u$ meets $D$ at a vertex before $u$. Choose a few such paths, one along each coordinate, so that the vertex of $D$ on each path fixes some coordinates of $u$. This gives an injection from $U \setminus D$ into tuples of vertices of $D$, or a bound on the projections of $U \setminus D$.
3. **Count parts.** Every part of a $2S$-partition satisfies step 2, and the parts cover $V$. So $H(2S) \ge |V| / F(2S)$.
4. **Conclude.** By the lemma, every play makes at least $S\,\big(|V|/F(2S) - 1\big)$ I/O moves.
5. **Check tightness.** Give a schedule for the same graph, and compare. A gap of a constant factor is the usual result.

## Classic examples

### The two-dimensional grid

Let $G$ have the vertices $(i, j)$ with $0 \le i, j \le n$, except $(0, 0)$. The $2n$ vertices with $i = 0$ or $j = 0$ are the inputs. Each other vertex $(i, j)$ has the two predecessors $(i - 1, j)$ and $(i, j - 1)$. The output is $(n, n)$. This is the dependence graph of a dynamic program on a table, such as edit distance or the longest common subsequence: an entry needs the entry above and the entry to the left. (These programs also use the entry $(i-1, j-1)$. Extra edges only make the set $U$ of step 2 smaller, so the bound below holds for them too.)

**Claim.** With $S \ge 3$ red pebbles, every play makes at least $\frac{n^2 + 2n}{4S + 2} - S$ I/O moves.

**Proof.** Step 2: let $U$ have a dominator set $D$ with $|D| \le 2S$. Each input of $U$ is in $D$. Take $(a, b) \in U \setminus D$, so $a, b \ge 1$. The column path $(0, b), (1, b), \ldots, (a, b)$ goes from an input to $(a, b)$, so it contains a vertex of $D$, and this vertex is in column $b$. The row path $(a, 0), (a, 1), \ldots, (a, b)$ contains a vertex of $D$ in row $a$. So $b$ is one of the columns of the vertices of $D$, and $a$ is one of the rows of the vertices of $D$. There are at most $|D|$ such columns and $|D|$ such rows, so $|U \setminus D| \le |D|^2 \le 4S^2$ and $|U| \le 4S^2 + 2S$. Step 3: the graph has $(n+1)^2 - 1 = n^2 + 2n$ vertices, so $H(2S) \ge (n^2 + 2n)/(4S^2 + 2S)$. Step 4: the lemma gives at least $S\,H(2S) - S \ge \frac{n^2 + 2n}{4S + 2} - S$ moves. $\square$

The proof does not use the minimum set. The bound is $\Omega(n^2/S)$ for $S \le n$.

**A matching schedule.** Let $w = S - 2$ and suppose that $w$ divides $n$. Cut the rows $1, \ldots, n$ into bands of $w$ rows. For the band of rows $a$ to $a + w - 1$: read the $w$ inputs $(a, 0), \ldots, (a + w - 1, 0)$. Then for $j = 1, \ldots, n$: read $(a - 1, j)$, compute $(a, j), (a+1, j), \ldots, (a + w - 1, j)$ in this order, deleting $(i, j - 1)$ after computing $(i, j)$ and deleting $(a - 1, j)$ after computing $(a, j)$, and write $(a + w - 1, j)$ for the next band. In the last band, write only $(n, n)$. At most $w + 2$ red pebbles are in use. Each band reads $w + n$ values, each band except the last writes $n$ values, and the last band writes one. With $n/w$ bands, the total is

$$\frac{n}{w}(w + n) + \Big(\frac{n}{w} - 1\Big) n + 1 = \frac{2n^2}{w} + 1.$$

For $n = 100$ and $w = 10$ the schedule makes $2001$ I/O moves with at most $12$ red pebbles.

**Numbers.** Take $n = 2^{16} = 65\,536$ and $S = 1026$, so $w = 1024$. The schedule makes $2n^2/w + 1 = 8\,388\,609$ I/O moves. The claim gives at least $1\,045\,029$. The ratio is about $8.03$: the constant $4$ in $4S^2$, and the factor $2$ of the schedule, which reads and writes each boundary row. So $Q = \Theta(n^2/S)$ for this graph.

### Matrix multiplication

For the conventional $n \times n$ algorithm, step 2 uses the three projections of a set of products $p_{ijk}$: the pairs $(i,k)$ and $(k,j)$ are bounded by the dominator set, and the pairs $(i,j)$ by the minimum set. The Loomis-Whitney inequality then bounds the set by $(2S)^{3/2}$. The proof and the bound $\frac{n^3}{4\sqrt{2S}} - S$ are on the [red-blue pebble game](/red-blue-pebble-game/) page. [Blocked matrix multiplication](/blocked-matrix-multiplication/) with blocks of side about $\sqrt{S/3}$ meets $O(n^3/\sqrt S)$.

### Fast Fourier transform

For the $n$-point butterfly graph of the [fast Fourier transform](/fast-fourier-transform/), step 2 gives $F(2S) = O(S \log S)$, and the result is $\Omega(n \log n/\log S)$ (Hong and Kung, Theorem 4.1). The outline and a matching schedule are on the [red-blue pebble game](/red-blue-pebble-game/) page, and the bound is the topic of [FFT lower bound](/fft-lower-bound/).

### Sorting networks and meshes

Hong and Kung derive two more bounds from a variant of step 2 that counts vertices on vertex-disjoint paths (see Variations). For the odd-even transposition sorting network on $n$ items, $Q \cdot S = \Omega(n^2)$ (Corollary 5.1). For the snake-like directed mesh with $m$ rows and $n$ columns, $Q = \Omega(mn)$ when $S < m$ (Corollary 5.2): with fewer red pebbles than rows, the program must move a constant fraction of all values.

## Variations

- **Information speed.** Hong and Kung (Theorem 5.1) treat graphs in which the inputs reach the outputs through vertex-disjoint paths, called lines. Suppose that, for any two vertices at distance $d$ on one line, the paths between them pass through at least $F(d)$ vertices on distinct lines, for an increasing function $F$. Then $Q \cdot F^{-1}(S) = \Omega(L)$, where $L$ is the number of vertices on the lines. Step 2 becomes: a part meets at most $S$ lines, with at most $F^{-1}(S) + 1$ vertices on each.
- **Independent evaluation.** For polynomials that are computed as sums of products, with separate summation trees (Hong and Kung, Theorem 6.1), step 2 is replaced by the *S-combination number*: the largest number of product terms that $S$ values can produce for $S$ outputs. Matrix multiplication is the main case.
- **Products of graphs.** Hong and Kung (Section 7) bound the dominator sets of a product of graphs by those of the factors, and list the bound $\Omega(|V| / S^{1/(d-1)})$ for $d$-dimensional grids. Exercise 2 proves this order for the $d$-dimensional version of the grid above with the Loomis-Whitney inequality.
- **Blocks.** In the [external memory model](/external-memory-model/), one I/O moves $B$ words. A block I/O can be replaced by $B$ single moves of the game with $S = M$, so a bound $Q$ for the game gives at least $Q/B$ block I/Os. This bound need not be tight, because the game does not see which values share a block. The [external sorting lower bound](/external-sorting-lower-bound/) uses a counting argument on blocks instead.
- **Distributed memory.** Irony, Toledo and Tiskin (2004) apply the projection argument to each processor of a parallel machine, to bound the words that a processor must send or receive in matrix multiplication.
- **Expansion in place of partitions.** For [Strassen's algorithm](/strassen-algorithm/) and similar algorithms, the DAG does not have the product structure of the conventional algorithm. Ballard, Demmel, Holtz and Schwartz (2012) bound the edge expansion of the DAG instead, and get $\Omega\big((n/\sqrt S)^{\log_2 7} S\big)$ for Strassen's algorithm.
- **Several levels.** Savage (Chapter 11) extends the game to a hierarchy of memories, with a pebble colour for each level and a separate I/O count for each pair of adjacent levels.
- **The black pebble game.** The older game has one colour and no slow memory. It measures the number of pebbles, which is space. Hopcroft, Paul and Valiant (1977) showed that every graph with $n$ vertices and bounded in-degree can be pebbled with $O(n/\log n)$ pebbles, and Paul, Tarjan and Celoni showed graphs that need $\Omega(n/\log n)$. These are bounds on space, not on I/O.

## Pitfalls

- **A bound for a DAG is not a bound for a problem.** The matrix multiplication bound $\Omega(n^3/\sqrt S)$ holds for the conventional DAG. Strassen's algorithm computes the same product with a different DAG and fewer I/O moves for large $n$. A claim such as "matrix multiplication needs $\Omega(n^3/\sqrt S)$ I/Os" without the DAG is false.
- **Recomputation.** The Hong and Kung lemma allows a vertex to be computed many times. Some partition proofs, such as the one on the [red-blue pebble game](/red-blue-pebble-game/) page, assume the one-shot variant. Say which variant the bound uses.
- **The dominator set is not inside the part.** $D$ is any set of vertices of $G$. It can contain inputs and vertices of earlier parts. A proof that assumes $D \subseteq U$ bounds a smaller class of sets and is wrong.
- **The additive $-S$ term.** The bound $S(|V|/F(2S) - 1)$ is negative when $|V| < F(2S)$. For a small graph, or a large $S$, the method gives nothing. In the grid example, the claim is useful only for $S$ well below $n$.
- **Constants.** The constants that the method gives are loose. In the grid example the gap to the schedule is a factor of 8. Use the method for the order of growth, and use a direct argument for exact constants.
- **Pebbles are words, not bytes or blocks.** $S$ counts values. A bound in the game counts single values moved. Convert to blocks as in Variations, and expect to lose a factor.

## Exercises

1. Prove that in the grid example the bound of step 2 cannot be improved by more than a constant factor: find a set $U$ of about $S^2$ vertices with a dominator set of at most $2S$ vertices. (Hint: take a square of side $S$, and its left column and top row.)
2. Generalise the grid to $d$ dimensions: vertices $(x_1, \ldots, x_d)$ with $0 \le x_k \le n$, where each vertex depends on the $d$ vertices with one coordinate smaller by one. Show that for $U \setminus D$, each projection that drops one coordinate has at most $|D|$ elements. Use the Loomis-Whitney inequality $|A|^{d-1} \le \prod_{k=1}^{d} |\pi_k(A)|$ to prove $|U| \le (2S)^{d/(d-1)} + 2S$, and conclude $\Omega(n^d / S^{1/(d-1)})$.
3. Check the count of the band schedule: why are $w + 2$ red pebbles enough, and why must the last value of each band be written but not the other values of that band?
4. Let $G$ sum $n$ inputs in a chain: $s_1 = x_1 + x_2$ and $s_k = s_{k-1} + x_{k+1}$. Show that $Q(G, S) = n + 1$ for every $S \ge 3$. What does the template give, and why can it give no more?
5. Let $G$ compute $y = Ax$ for an $n \times n$ matrix $A$ with the conventional DAG. Show that every play reads at least $n^2$ values. Then explain why the S-partition method cannot prove more than $O(n^2)$ here.

## References
