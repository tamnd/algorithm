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
  - url: "https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm"
    locator: section Algorithm
  - book: isbn:9780321295354
    title: Kleinberg and Tardos, Algorithm Design
    locator: Section 2.4
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 4 (matrix multiplication, Strassen) and Chapter 23 (Floyd-Warshall)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.4 (brute-force 3-sum and the doubling test)
  - paper: "T. C. Hu and M. T. Shing, Computation of matrix chain products, Part I, SIAM Journal on Computing 11 (1982), and Part II, SIAM Journal on Computing 13 (1984)"
    locator: the O(n log n) algorithm
  - paper: "Ryan Williams, Faster all-pairs shortest paths via circuit complexity, STOC 2014"
    locator: the main theorem
---

An algorithm runs in cubic time when its worst-case [time](/time-complexity/) is $\Theta(n^3)$ in the input size $n$, in a stated model such as the [word RAM](/word-ram/). The usual cause is three nested loops that each run over about $n$ values. The textbook method for the product of two $n \times n$ matrices and the [Floyd-Warshall algorithm](/floyd-warshall/) for shortest paths between all pairs of vertices are the main examples. Cubic time is the next common class of [polynomial time](/polynomial-time/) after [quadratic time](/quadratic-time/). At about $10^9$ steps per second it handles inputs of a few thousand items, and it becomes too slow from about ten thousand.

## In plain words

A cube has three sides of the same length. A program with three nested loops, each going over the whole input, does work in proportion to the volume of a cube. If the input becomes twice as large, the work becomes eight times larger. If it becomes ten times larger, the work becomes a thousand times larger.

The typical case is a table of numbers with the same number of rows and columns. To fill each cell, the program combines one row and one column, which takes as many steps as the table has rows. The number of cells is the square of the number of rows, so the total is the cube. The classic method for the product of two tables of numbers works in this way.

## The idea

**Definition.** Fix a model and a case. Let $T(n)$ be the worst-case number of steps on inputs of size $n$. The algorithm runs in *cubic time* when $T(n) = \Theta(n^3)$, and in *at most cubic time* when $T(n) = O(n^3)$. When the input is an $n \times n$ matrix, the size is the number of entries, which is $n^2$, and the same time is $\Theta(N^{3/2})$ in the number $N = n^2$ of entries. State the meaning of $n$ with each bound, see [input size](/input-size/). If $T(n) \sim a n^3$ with $a > 0$, then $T(2n)/T(n) \to 8$ ([tilde notation](/tilde-notation/)). The statement $T(n) = \Theta(n^3)$ alone does not give this limit.

**Loop shapes and their exact counts.** Let the innermost body cost one step. The counts are exact for the loops as written, and the sums are in the page on [arithmetic series](/arithmetic-series/).

- Three independent loops over $1..n$: the body runs $n^3$ times. For $n = 8$ it runs 512 times.
- The indices are strictly increasing, `for i`, `for j in i+1..n`, `for k in j+1..n`: the body runs $\binom{n}{3} = n(n-1)(n-2)/6$ times, the number of triples $i < j < k$. For $n = 8$ it is 56.
- The inner loops stop at the outer indices, `for i in 1..n`, `for j in 1..i`, `for k in 1..j`: the body runs $\sum_{i=1}^{n} i(i+1)/2 = n(n+1)(n+2)/6 = \binom{n+2}{3}$ times. The sum uses $\sum_{i=1}^{n} i^2 = n(n+1)(2n+1)/6$. For $n = 8$ it is 120.
- A quadratic loop whose body costs $\Theta(n)$ is cubic. An example is a loop over all $n^2$ pairs $(i, j)$ in which the body computes a sum of $n$ terms.

Each of these counts is $\Theta(n^3)$, with the same argument as for the [quadratic case](/quadratic-time/). For the triples $i<j<k$, the count $n(n-1)(n-2)/6$ is at most $n^3/6$ and, for $n \ge 3$, at least $n^3/27$, because $n - 1 \ge 2n/3$ and $n - 2 \ge n/3$ when $n \ge 3$, so $n(n-1)(n-2)/6 \ge n \cdot (2n/3) \cdot (n/3)/6 = n^3/27$. As with quadratic time, three nested loops can give a lower class, when an inner bound is a constant or when an index doubles.

**Cost in practice.** At $10^9$ steps per second, $n = 1000$ means $10^9$ steps and about 1 second. For $n = 10^4$ the same code needs $10^{12}$ steps and about 1000 seconds.

## Examples

- **Naive matrix multiplication.** For two $n \times n$ matrices $A$ and $B$, the entry $C_{ij} = \sum_{k=1}^{n} A_{ik} B_{kj}$ needs $n$ multiplications, and there are $n^2$ entries. So the definition makes exactly $n^3$ multiplications of entries and $n^2(n-1)$ additions. For $n = 8$ this is 512 multiplications and 448 additions. The time is $\Theta(n^3)$ on each input. See [naive matrix multiplication](/naive-matrix-multiplication/).
- **Floyd-Warshall.** For a graph with $n$ vertices, the algorithm runs the update $d_{ij} \leftarrow \min(d_{ij}, d_{ik} + d_{kj})$ for each triple $(i, j, k)$. The update runs exactly $n^3$ times, on each input, so the time is $\Theta(n^3)$ in every case. It solves the [all-pairs shortest paths](/all-pairs-shortest-paths/) problem and also computes the [transitive closure](/transitive-closure/) when the update uses the Boolean operations.
- **Matrix chain order.** The dynamic program of [matrix chain multiplication](/matrix-chain-multiplication/) for $n$ matrices tries each split point of each subchain. The number of (subchain, split) pairs is $\sum_{\ell=2}^{n} (n - \ell + 1)(\ell - 1) = \binom{n+1}{3}$. For $n = 4$ it is $3 + 4 + 3 = 10$. The time is $\Theta(n^3)$.
- **Gaussian elimination.** The elimination of a dense $n \times n$ linear system takes $\Theta(n^3)$ arithmetic operations. See [Gaussian elimination](/gaussian-elimination/).
- **3-sum by brute force.** A check of all $\binom{n}{3}$ triples of $n$ numbers for a zero sum makes $\sim n^3/6$ triple checks. Sorting and two pointers solve the problem in $\Theta(n^2)$ time, see [3SUM](/3sum/).
- **Triples.** A test of all $\binom{n}{3}$ triples of vertices for a triangle, given an adjacency matrix, takes $\Theta(n^3)$ time.
- Non-example: the product of an $n \times n$ matrix and a vector takes $\Theta(n^2)$ time, see [matrix-vector multiplication](/matrix-vector-multiplication/).

### Faster algorithms

The cube is not the limit for the problems above, and the status differs for each of them.

- **Matrix multiplication.** [Strassen's algorithm](/strassen-algorithm/) computes the product of two $2 \times 2$ block matrices with 7 block multiplications in place of 8. For $n$ a power of 2 this gives the recurrence $T(n) = 7\,T(n/2) + \Theta(n^2)$, and by the [master theorem](/master-theorem/) $T(n) = \Theta(n^{\lg 7})$, where $\lg 7 \approx 2.807$. Strassen published this in 1969. The best known exponent is smaller. It is the number $\omega$ of the [matrix multiplication exponent](/matrix-multiplication-exponent/), and the trivial lower bound is $n^2$ because the output has $n^2$ entries. Whether $\omega = 2$ is open. Strassen's algorithm pays off in practice only for large matrices, because of its larger constants. The algorithms behind the best known bounds on $\omega$ are not used in practice.
- **Triangle detection.** Given an adjacency matrix, a triangle can be found in $O(n^{\omega})$ time by squaring the matrix.
- **All-pairs shortest paths.** No algorithm with time $O(n^{3-\varepsilon})$, for a constant $\varepsilon > 0$, is known for graphs with real edge weights. The [APSP conjecture](/apsp-conjecture/) of fine-grained complexity says that none exists for integer weights of polynomial size. This is a conjecture, not a theorem. Williams (2014) gives time $n^3/2^{\Omega(\sqrt{\log n})}$, which is faster than $n^3$ by more than any polylogarithmic factor, but it is not $O(n^{3-\varepsilon})$.
- **Matrix chain order.** The algorithm of Hu and Shing takes $O(n \log n)$ time, but it is more complex than the dynamic program. The dynamic program is the one that the textbooks teach.

## Where it is used

Cubic algorithms are practical for $n$ up to a few thousand. Floyd-Warshall is a common choice for dense graphs with a few hundred vertices, because the code has three short loops and no data structure. Dense linear algebra uses cubic algorithms for products, for the solution of linear systems and for matrix inversion, and the libraries tune the loops for the cache of the machine, see [blocked matrix multiplication](/blocked-matrix-multiplication/). Dynamic programs with three indices give cubic time too. For larger inputs the class is usually too slow, and the next step is to find a lower class or an approximation. See [common growth rates](/common-growth-rates/) for the whole list.

## References
