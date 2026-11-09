---
tag: Q97DPS
kind: algorithm
slug: xor-gaussian-elimination
name: Gaussian elimination for XOR-SAT
aliases:
- GF(2) elimination
- Gauss-Jordan elimination over GF(2)
area: logic-and-constraints/sat-solving
level: core
summary: Decide XOR-SAT by Gauss-Jordan elimination over GF(2). A row 0 = 1 means UNSAT; otherwise set the free variables to 0 and read the pivots. It also counts the solutions.
solves: [xor-sat]
model: word-ram
complexity:
  vars: {n: the number of variables, m: the number of XOR clauses}
  time: {worst: "O(m n min(m, n))"}
  space: {extra: O(m n)}
properties: {deterministic: true}
prereqs: [xor-sat, gaussian-elimination, reduced-row-echelon-form]
see_also: [gauss-jordan-elimination, bitset-gaussian-elimination, rank, wiedemann-algorithm, two-sat-algorithm, horn-sat-forward-chaining, model-counting]
sources:
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2 (2022)
    locator: Section 7.2.2.2, Satisfiability (XOR clauses and parity constraints)
  - paper: doi:10.1145/800133.804350
    title: Thomas J. Schaefer, The complexity of satisfiability problems, Proceedings of the 10th ACM Symposium on Theory of Computing (STOC 1978), 216 to 226
    locator: the affine case of the dichotomy theorem (systems of linear equations over GF(2) are solvable in polynomial time)
  - paper: "Mate Soos, Karsten Nohl and Claude Castelluccia, Extending SAT solvers to cryptographic problems, Theory and Applications of Satisfiability Testing (SAT 2009), Lecture Notes in Computer Science 5584, 244 to 257"
    locator: the whole paper (XOR clauses and Gaussian elimination inside a CDCL solver)
  - url: "https://github.com/malb/m4ri"
    locator: M4RI library for dense linear algebra over GF(2) (the method of the Four Russians for elimination)
---

Gaussian elimination over $\mathrm{GF}(2)$ decides [XOR-SAT](/xor-sat/): a set of XOR clauses is a system of linear equations modulo 2, and [Gauss-Jordan elimination](/gauss-jordan-elimination/) solves it. The system has no solution exactly when elimination produces a row that says $0 = 1$. Otherwise it has exactly $2^{n - r}$ solutions, where $r$ is the [rank](/rank/), and one of them comes from setting the free variables to 0. The time is $O(m n \min(m, n))$ entry operations, and much less with rows packed into machine words. The [XOR-SAT](/xor-sat/) page covers the problem; this page covers the algorithm.

## In plain words

An XOR clause says that an odd number, or an even number, of some switches are on. Two such rules can be combined: if you add them, each switch that appears in both cancels out, and the parities add.

The method takes the first switch, picks one rule that mentions it, and adds that rule to every other rule that mentions it. Now only one rule mentions the first switch. It does the same for the next switch with the remaining rules, and so on. At the end, each rule names one switch of its own, plus some switches that no rule controls. If a rule has become "no switches, odd parity", the rules contradict each other. Otherwise turn off the uncontrolled switches and read each controlled switch from its rule.

## The problem

The input is a set of $m$ XOR clauses over $x_1, \ldots, x_n$. Clause $i$ is $x_{v_1} \oplus \cdots \oplus x_{v_k} = b_i$ with $b_i \in \{0, 1\}$. We write it as row $i$ of a matrix $A \in \{0,1\}^{m \times n}$, with $A[i][c] = 1$ when $x_c$ occurs an odd number of times in the clause, so the system is $A x = b$ over $\mathrm{GF}(2)$. The output is UNSAT when no $x \in \{0,1\}^n$ satisfies all clauses, and else one solution. The count of solutions comes at no extra cost.

## The algorithm

```pseudo id=main
XOR-GAUSS(A, b, n)                         ▷ m rows, numbered from 0
L1  r ← 0                                   ▷ the number of pivot rows so far
L2  for c ← 1 to n do
L3      find a row i ≥ r with A[i][c] = 1; if there is none, go to the next c
L4      swap rows i and r, and swap b_i and b_r
L5      for each row j ≠ r with A[j][c] = 1 do
L6          row j ← row j ⊕ row r, and b_j ← b_j ⊕ b_r
L7      pivot[r] ← c, r ← r + 1
L8  for each row j ≥ r do
L9      if b_j = 1 then return UNSAT        ▷ the row says 0 = 1
L10 x ← the all-zero vector
L11 for i ← 0 to r − 1 do x[pivot[i]] ← b_i
L12 return x
```

Over $\mathrm{GF}(2)$ the only nonzero entry is 1, so no division is needed: the pivot is any row with a 1 in the column, and elimination is XOR of rows. Lines L5 and L6 clear the column in all other rows, above and below, so the result is in [reduced row echelon form](/reduced-row-echelon-form/). Then each pivot row reads $x_{pivot[i]} \oplus (\text{free variables}) = b_i$, and with the free variables at 0, line L11 reads the solution directly.

## Example

Take $n = 5$ and four XOR clauses:

$$x_1 \oplus x_2 \oplus x_3 = 1,\quad x_2 \oplus x_3 \oplus x_4 = 0,\quad x_1 \oplus x_4 \oplus x_5 = 1,\quad x_3 \oplus x_5 = 1.$$

The rows show the coefficients of $x_1, \ldots, x_5$, then $b$:

| step | row 0 | row 1 | row 2 | row 3 |
|---|---|---|---|---|
| start | 11100 \| 1 | 01110 \| 0 | 10011 \| 1 | 00101 \| 1 |
| column 1, pivot row 0; add it to row 2 | 11100 \| 1 | 01110 \| 0 | 01111 \| 0 | 00101 \| 1 |
| column 2, pivot row 1; add it to rows 0 and 2 | 10010 \| 1 | 01110 \| 0 | 00001 \| 0 | 00101 \| 1 |
| column 3, swap rows 2 and 3, pivot row 2; add it to row 1 | 10010 \| 1 | 01011 \| 1 | 00101 \| 1 | 00001 \| 0 |
| column 4, no row from 3 on has a 1 | same | same | same | same |
| column 5, pivot row 3; add it to rows 1 and 2 | 10010 \| 1 | 01010 \| 1 | 00100 \| 1 | 00001 \| 0 |

The pivots are the columns 1, 2, 3 and 5, so the rank is $r = 4$, and $x_4$ is free. No zero row is left, so line L9 does not return. The final rows say $x_1 = 1 \oplus x_4$, $x_2 = 1 \oplus x_4$, $x_3 = 1$ and $x_5 = 0$. With $x_4 = 0$, line L11 gives $x = (1, 1, 1, 0, 0)$. The system has $2^{5-4} = 2$ solutions, $(1,1,1,0,0)$ and $(0,0,1,1,0)$, which agrees with a check of all 32 assignments.

Now add the clause $x_1 \oplus x_4 = 0$. The sum of the first two clauses is $x_1 \oplus x_4 = 1$, so the new clause contradicts them. Elimination turns the new row into $00000 \mid 1$, and line L9 returns UNSAT.

## Correctness

Each row operation is invertible over $\mathrm{GF}(2)$, because adding a row twice adds nothing. So the solutions never change. The invariant of the loop of line L2 is that the pivot rows found so far have their pivot column as a unit column, and the other rows are zero in the columns already handled. At the end, a zero row with $b_j = 1$ has no solution. Otherwise each pivot variable equals $b_i$ plus a sum of free variables, so each of the $2^{n - r}$ choices of the free variables gives exactly one solution. The full proof is in the proof file below.

## Complexity

For each of the $n$ columns, line L3 scans at most $m$ rows. A pivot is found at most $\min(m, n)$ times, and then lines L5 and L6 add a row of length $n$ to at most $m - 1$ rows. So the time is $O(m n \min(m, n))$ entry operations in the worst case on the [word RAM](/word-ram/), which is $O(n^3)$ for a square system. With [bitset rows](/bitset-gaussian-elimination/) of $w$ entries per word, a row addition takes $\lceil n/w \rceil$ word operations, so the main term drops to $O(m \min(m, n) \lceil n/w \rceil)$. The Python version stores each row as one integer and gets the same effect. The extra space is $O(m n)$ entries, or $O(m \lceil n/w \rceil)$ words.

The rank of a matrix over a field can be found in $O(n^\omega)$ time for a square matrix, where $\omega$ is the [exponent of matrix multiplication](/matrix-multiplication-exponent/), by reducing elimination to matrix multiplication. So the cubic bound is not optimal in theory.

## Properties

- **Exact and deterministic.** It decides the problem and also counts the solutions.
- **All solutions.** The reduced form describes all solutions as an affine space: a particular solution plus the span of $n - r$ basis vectors, one for each free variable.
- **Certificate of UNSAT.** The row $0 = 1$ is a sum of input rows, and a record of which input rows were added gives a short proof that the system has no solution.

## Variants and improvements

- **Packed rows and the method of the Four Russians.** Pack 64 entries per word, and for dense matrices process groups of columns with precomputed tables of row sums. The M4RI library uses this method.
- **Sparse systems.** For large sparse systems, [structured Gaussian elimination](/structured-gaussian-elimination/) limits the fill-in, and the [Wiedemann algorithm](/wiedemann-algorithm/) uses only products of the matrix with vectors.
- **Inside CDCL solvers.** Solvers such as CryptoMiniSat keep the XOR clauses of a formula as a matrix next to the CNF clauses, and run elimination during the search to find forced literals and conflicts (Soos, Nohl and Castelluccia 2009).
- **Incremental use.** Adding one equation to a reduced system takes one pass: reduce the new row by the pivot rows in $O(r)$ row operations, then make it a new pivot row or find a contradiction.

## When to use it

Use it whenever the constraints are parities: XOR clauses from cryptanalysis of stream ciphers, parity checks of [linear codes](/linear-code/), puzzles of the "lights out" kind, and the affine case of [Schaefer's theorem](/schaefer-dichotomy-theorem/). CNF solvers do badly on such constraints: an XOR of $k$ variables needs $2^{k-1}$ clauses without new variables, and resolution needs exponential size on some XOR systems, such as the Tseitin formulas. For formulas that mix XOR clauses with ordinary clauses, the problem is NP-complete again, and a solver that combines CDCL with elimination is the usual tool. For 2-CNF formulas use the [2-SAT algorithm](/two-sat-algorithm/), and for Horn formulas [forward chaining](/horn-sat-forward-chaining/).

## Pitfalls

- **Elimination only below the pivot.** If line L5 clears only the rows below row $r$, the result is in row echelon form but not reduced, and line L11 cannot set $x[pivot[i]] \gets b_i$. Then back substitution is needed, from the last pivot row up.
- **Forgetting the right side.** Lines L4 and L6 must move and add $b$ with the row. Otherwise the system changes, and line L9 tests the wrong values.
- **Repeated variables.** A clause $x_1 \oplus x_1 \oplus x_2 = 1$ is $x_2 = 1$. Build each row with XOR of the coefficients, not OR, or the matrix is wrong.
- **Treating the zero row as an error.** A zero row with $b_j = 0$ is a redundant equation, not a contradiction. Only $b_j = 1$ means UNSAT.

## Implementations

## History

Elimination of variables from linear equations is old, and the modern method carries the name of Gauss. Its use for XOR constraints in satisfiability is simple once the constraints are seen as equations over $\mathrm{GF}(2)$. Schaefer's dichotomy theorem of 1978 lists systems of linear equations over $\mathrm{GF}(2)$ as one of the six tractable cases of Boolean constraint satisfaction. Soos, Nohl and Castelluccia added XOR clauses with elimination to a CDCL solver in 2009, for problems from cryptography.

## References
