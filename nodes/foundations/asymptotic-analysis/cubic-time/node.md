---
tag: K606T2
kind: concept
slug: cubic-time
name: Cubic time
area: foundations/asymptotic-analysis
level: intro
summary: Running time proportional to the cube of the input size, typical of algorithms that examine all triples or use three nested loops.
prereqs: [asymptotic-notation, time-complexity, quadratic-time, arithmetic-series]
see_also: [polynomial-time, naive-matrix-multiplication, strassen-algorithm, matrix-multiplication-exponent, floyd-warshall, matrix-chain-multiplication, doubling-hypothesis, common-growth-rates]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Sections 4.1 and 4.2 (square matrix multiplication and Strassen's algorithm), Section 14.2 (matrix-chain multiplication) and Chapter 23 (all-pairs shortest paths, the Floyd-Warshall algorithm)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 2.4, A Survey of Common Running Times (cubic time)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.4, Analysis of Algorithms (brute-force ThreeSum and the doubling test)
  - paper: doi:10.1137/0211028
    title: T. C. Hu and M. T. Shing, Computation of matrix chain products, Part I, SIAM Journal on Computing 11(2), 362 to 373 (1982); Part II, SIAM Journal on Computing 13(2), 228 to 251 (1984)
    locator: the O(n log n) algorithm
  - paper: doi:10.1145/2591796.2591811
    title: Ryan Williams, Faster all-pairs shortest paths via circuit complexity, Proceedings of the 46th ACM Symposium on Theory of Computing (STOC 2014), 664 to 673
    locator: the main theorem
---

An algorithm runs in cubic time when its cost is $\Theta(n^3)$ in a size parameter $n$, in a stated model such as the [word RAM](/word-ram/) and a stated case. The usual cause is three nested loops that each run over about $n$ values. The definition-based product of two $n \times n$ matrices, the [Floyd-Warshall algorithm](/floyd-warshall/) for shortest paths between all pairs of vertices, and the dynamic program for [matrix chain multiplication](/matrix-chain-multiplication/) are the main examples. Cubic time is the next common class of [polynomial time](/polynomial-time/) after [quadratic time](/quadratic-time/), and at about $10^9$ simple steps per second it handles $n$ up to about 1000 in one second.

## In plain words

A cube has three sides of the same length. A program with three nested loops, each going over the whole input, does work in proportion to the volume of a cube. If the input becomes twice as large, the work becomes eight times larger. If it becomes ten times larger, the work becomes a thousand times larger.

The typical case is a table of numbers with the same number of rows and columns. To fill each cell, the program combines one row and one column, which takes as many steps as the table has rows. The number of cells is the square of the number of rows, so the total is the cube. The classic method for the product of two tables of numbers works in this way.

## The idea

### Definition

Fix a model and a case. Let $T(n)$ be the cost on inputs with size parameter $n$. The algorithm runs in *cubic time* when $T(n) = \Theta(n^3)$, and in *at most cubic time* when $T(n) = O(n^3)$. If $T(n) \sim a n^3$ with $a > 0$, then $T(2n)/T(n) \to 8$ ([tilde notation](/tilde-notation/)). The statement $T(n) = \Theta(n^3)$ alone does not give this limit.

The parameter $n$ is often not the input size. For an $n \times n$ matrix, the input has $N = n^2$ entries, and a time of $\Theta(n^3)$ is $\Theta(N^{3/2})$ in the input size. For a graph with $V$ vertices, Floyd-Warshall is $\Theta(V^3)$ whether the graph has $V$ edges or $V^2$. State what $n$ counts with each bound, see [input size](/input-size/).

### Loop shapes and their exact counts

Let the innermost body cost one step. The counts are exact for the loops as written.

- Three independent loops over $1..n$: $n^3$ runs. For $n = 8$, 512.
- Strictly increasing indices, `for i`, `for j in i+1..n`, `for k in j+1..n`: $\binom{n}{3} = n(n-1)(n-2)/6$ runs, the number of triples $i < j < k$. For $n = 8$, 56.
- Inner loops that stop at the outer indices, `for i in 1..n`, `for j in 1..i`, `for k in 1..j`: $\sum_{i=1}^{n} i(i+1)/2 = n(n+1)(n+2)/6 = \binom{n+2}{3}$ runs, using $\sum_{i=1}^n i^2 = n(n+1)(2n+1)/6$. For $n = 8$, 120.
- A quadratic loop whose body costs $\Theta(n)$, for example a loop over all $n^2$ pairs $(i, j)$ whose body adds $n$ terms.

Each count is $\Theta(n^3)$. For the triples, $n(n-1)(n-2)/6 \le n^3/6$, and for $n \ge 3$ we have $n - 1 \ge 2n/3$ and $n - 2 \ge n/3$, so $n(n-1)(n-2)/6 \ge n \cdot (2n/3) \cdot (n/3)/6 = n^3/27$. As with quadratic time, three nested loops can give a lower class when an inner bound is a constant or an index doubles.

### Worked examples

**The product of two matrices.** For $n \times n$ matrices $A$ and $B$, the entry $C_{ij} = \sum_{k=1}^{n} A_{ik} B_{kj}$ needs $n$ multiplications and $n - 1$ additions, and there are $n^2$ entries. So the definition makes exactly $n^3$ multiplications and $n^2(n-1)$ additions on each input: 512 and 448 for $n = 8$, and $10^9$ multiplications for $n = 1000$. See [naive matrix multiplication](/naive-matrix-multiplication/).

**Floyd-Warshall.** For a graph with vertices $1, \ldots, V$, the algorithm runs the update $d_{ij} \leftarrow \min(d_{ij}, d_{ik} + d_{kj})$ for $k = 1, \ldots, V$ in the outer loop and for each pair $(i, j)$ inside. *Invariant.* If the graph has no negative cycle, then after the round for $k$, $d_{ij}$ is the length of a shortest path from $i$ to $j$ whose inner vertices are all in $\{1, \ldots, k\}$. A shortest such path either avoids $k$, and then its length is the value of $d_{ij}$ from the round before, or it passes through $k$ once, and then it is a shortest path from $i$ to $k$ followed by one from $k$ to $j$, both with inner vertices in $\{1, \ldots, k-1\}$. The update runs exactly $V^3$ times on each input, so the time is $\Theta(V^3)$ in each case. On the five-vertex example graph of CLRS, Chapter 23 (edges $1 \to 2$ of weight 3, $1 \to 3$ of 8, $1 \to 5$ of $-4$, $2 \to 4$ of 1, $2 \to 5$ of 7, $3 \to 2$ of 4, $4 \to 1$ of 2, $4 \to 3$ of $-5$, $5 \to 4$ of 6), the 125 updates give the distance $-3$ from vertex 1 to vertex 3, along the path $1 \to 5 \to 4 \to 3$.

**Matrix chain order.** For a chain of $n$ matrices, the dynamic program tries each split point of each subchain. The number of pairs (subchain, split) is $\sum_{\ell=2}^{n} (n - \ell + 1)(\ell - 1) = \binom{n+1}{3}$, so the time is $\Theta(n^3)$. For the six matrices of sizes $30 \times 35$, $35 \times 15$, $15 \times 5$, $5 \times 10$, $10 \times 20$ and $20 \times 25$ (the example of CLRS, Section 14.2), the program examines $\binom{7}{3} = 35$ pairs and finds the least cost of 15125 scalar multiplications.

### Faster algorithms

The cube is not the limit for these problems, and the status differs for each of them.

- **Matrix multiplication.** [Strassen's algorithm](/strassen-algorithm/) multiplies two $2 \times 2$ block matrices with 7 block products in place of 8. For $n$ a power of 2 this gives $T(n) = 7\,T(n/2) + \Theta(n^2)$, so $T(n) = \Theta(n^{\lg 7})$ by the [master theorem](/master-theorem/), with $\lg 7 \approx 2.807$. The best known exponent is smaller. It is the subject of the [matrix multiplication exponent](/matrix-multiplication-exponent/) $\omega$, and the trivial lower bound is $\Omega(n^2)$ because the output has $n^2$ entries. Whether $\omega = 2$ is open. The algorithms behind the best known bounds on $\omega$ are not used in practice.
- **Triangle detection.** With an adjacency matrix, a triangle can be found in $O(n^{\omega})$ time by a matrix product, in place of a check of the $\binom{n}{3}$ triples.
- **All-pairs shortest paths.** No algorithm with time $O(n^{3-\varepsilon})$ for a constant $\varepsilon > 0$ is known for dense graphs with arbitrary real weights. The [APSP conjecture](/apsp-conjecture/) says that none exists for integer weights of polynomial size. Williams (2014) gives time $n^3/2^{\Omega(\sqrt{\log n})}$, which beats $n^3$ by more than any polylogarithmic factor but is not $O(n^{3-\varepsilon})$.
- **Matrix chain order.** Hu and Shing (1982, 1984) give an $O(n \log n)$ algorithm. It is more complex than the dynamic program, which is the one that textbooks teach.

### Pitfalls

- **Operations are not bit operations.** The bound $\Theta(n^3)$ for [Gaussian elimination](/gaussian-elimination/) counts arithmetic operations. Over the rational numbers, the numerators and denominators can grow during the run, so the bit cost needs a separate bound on the sizes of the entries. With floating-point numbers each operation is one step, but the result is approximate. Name the model.
- **The measure of input size.** "Cubic in the side $n$ of a matrix" is $N^{3/2}$ in the number $N$ of entries. A claim that the naive matrix product is "cubic in the input size" is false.
- **Pseudo-polynomial loops.** A triple loop in which one index runs to a number $W$ in the input takes $\Theta(n^2 W)$ time, which is polynomial in the value $W$ and exponential in its $\lg W$ bits. See [pseudo-polynomial time](/pseudo-polynomial-time/).
- **Asymptotically faster is not faster in practice.** Strassen's algorithm pays off only above some matrix size, and it is less stable numerically. The best known bounds on $\omega$ come with constants that make them useless for real inputs.
- **Negative cycles.** Floyd-Warshall stays $\Theta(V^3)$ with negative edges, but its distances are correct only when no negative cycle exists. An entry $d_{ii} < 0$ at the end shows a negative cycle through $i$.

## Examples

- Naive product of two $8 \times 8$ matrices: 512 multiplications and 448 additions.
- Floyd-Warshall on 5 vertices: 125 updates, on any graph.
- Matrix chain order for the 6 matrices above: 35 (subchain, split) pairs and a least cost of 15125.
- Brute-force 3SUM: a check of all $\binom{n}{3}$ triples of $n$ numbers for a zero sum, about $n^3/6$ checks. Sedgewick and Wayne use it to show the doubling ratio 8. Sorting and two pointers solve [3SUM](/3sum/) in $\Theta(n^2)$ time.
- Non-example: the product of an $n \times n$ matrix and a vector takes $n^2$ multiplications, see [matrix-vector multiplication](/matrix-vector-multiplication/).
- Non-example: Strassen's algorithm, $\Theta(n^{\lg 7})$, is $O(n^3)$ but not cubic.

## Where it is used

Cubic algorithms are practical for $n$ up to a few thousand. Floyd-Warshall is a common choice for dense graphs with a few hundred vertices, because the code is three short loops with no data structure. Dense linear algebra uses cubic algorithms for products, for linear systems and for matrix inversion, and the libraries arrange the loops for the cache of the machine, see [blocked matrix multiplication](/blocked-matrix-multiplication/). Dynamic programs over intervals, such as matrix chain order and the [CYK algorithm](/cyk-algorithm/) for context-free parsing, take cubic time in the length of the input. See [common growth rates](/common-growth-rates/) for the whole list.

## References
