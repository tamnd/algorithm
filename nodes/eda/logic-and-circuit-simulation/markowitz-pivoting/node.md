---
tag: RPNJK6
kind: technique
slug: markowitz-pivoting
name: Markowitz pivoting
aliases:
- Markowitz criterion
- Markowitz ordering
area: eda/logic-and-circuit-simulation
level: core
summary: Chooses as pivot the entry that minimizes (r - 1)(c - 1), with r and c its row and column counts, subject to a size threshold, to limit fill-in in sparse LU.
prereqs: [sparse-matrix, fill-in, lu-decomposition, partial-pivoting, modified-nodal-analysis]
see_also: [minimum-degree-ordering, fill-reducing-ordering, gilbert-peierls-lu, klu-solver, growth-factor, complete-pivoting, sparse-linear-systems, elimination-tree]
sources:
  - paper: "Harry M. Markowitz, The elimination form of the inverse and its application to linear programming, Management Science 3(3), 255 to 269, 1957"
    title: Harry M. Markowitz, The elimination form of the inverse and its application to linear programming, Management Science 3(3), 255 to 269, 1957
    locator: the pivot rule that takes the nonzero with the least product (r - 1)(c - 1) of the other entries in its row and column
  - book: isbn:9780198508380
    title: Iain S. Duff, Albert M. Erisman and John K. Reid, Direct Methods for Sparse Matrices, second edition, Oxford University Press, 2017
    locator: Chapter 7, local pivotal strategies for sparse matrices (the Markowitz count, threshold pivoting and its stability bound, and the search for the pivot)
  - paper: "Kenneth S. Kundert, Sparse matrix techniques, in Albert E. Ruehli (editor), Circuit Analysis, Simulation and Design, Part 1, North-Holland, 1986"
    title: Kenneth S. Kundert, Sparse matrix techniques, in A. E. Ruehli (editor), Circuit Analysis, Simulation and Design, North-Holland, 1986
    locator: the chapter on sparse LU for circuit matrices, with Markowitz pivoting, the threshold test and the data structures of the Sparse package
  - book: isbn:9780470538715
    title: Farid N. Najm, Circuit Simulation, Wiley-IEEE Press, 2010
    locator: Chapter 3, solution of linear algebraic circuit equations (Gaussian elimination, sparse matrices, fill-in and pivot ordering)
  - paper: doi:10.1137/0602010
    title: Mihalis Yannakakis, Computing the minimum fill-in is NP-complete, SIAM Journal on Algebraic and Discrete Methods 2(1), 77 to 79, 1981
    locator: the NP-completeness of minimum fill for symmetric elimination
  - paper: doi:10.1109/PROC.1967.6011
    title: William F. Tinney and John W. Walker, Direct solutions of sparse network equations by optimally ordered triangular factorization, Proceedings of the IEEE 55(11), 1801 to 1809, 1967
    locator: the ordering schemes for sparse network matrices, among them the scheme that takes the node with the fewest connections
---

Markowitz pivoting is a rule for choosing the pivots of a sparse [LU factorization](/lu-decomposition/). At each elimination step it takes, among the entries of the remaining submatrix that are large enough to be stable, the one with the least *Markowitz count* $(r_i - 1)(c_j - 1)$, where $r_i$ and $c_j$ are the numbers of nonzeros in its row and its column. The count is an upper bound on the [fill-in](/fill-in/) that the step creates, so the rule is a greedy way to keep the factors sparse. It is a general method of sparse linear algebra, proposed by Markowitz in 1957 for linear programming, and this page frames it for the circuit simulation half of the logic and circuit simulation sub-area, where every Newton iteration of a simulator solves one [modified nodal analysis](/modified-nodal-analysis/) system with it.

## In plain words

To solve a system of equations by elimination, you pick one equation and one unknown, use that equation to remove the unknown from all the other equations, and repeat. When most coefficients are zero, as in a circuit, the order of these choices matters a lot. A bad choice spreads nonzero coefficients over many equations that had none, and the later work grows.

The rule counts, for a candidate coefficient, the other nonzeros in its equation and the other equations that hold its unknown. Their product is the most new nonzeros the step can create. The rule picks the candidate with the smallest product. It skips a candidate that is tiny compared with the other coefficients of its unknown, because dividing by a tiny number magnifies rounding errors.

## When it applies

Use it to factor an unsymmetric [sparse matrix](/sparse-matrix/) when the pivot order is chosen during the numerical factorization, so that sparsity and numerical size are judged together. Circuit matrices fit this well: the MNA matrix of a transistor circuit is unsymmetric because of the transconductances, it has zero diagonal entries in the rows of voltage sources, and its values change from one Newton iteration to the next. For a symmetric positive definite matrix, such as the nodal matrix of a resistor network, no numerical pivoting is needed, and a symbolic order such as [minimum degree](/minimum-degree-ordering/) is cheaper. When the same pattern is factored many times, a simulator chooses the pivots once with this rule and reuses the order, see Variations.

## The template

**Notation.** At step $k$ the active submatrix $A^{(k)}$ is what remains of $A$ after $k - 1$ eliminations, with the pivot rows and columns removed. In $A^{(k)}$, $r_i$ is the number of nonzeros in row $i$ and $c_j$ the number in column $j$. The threshold is a number $u$ with $0 < u \le 1$. An entry $a_{ij}$ is *acceptable* when $|a_{ij}| \ge u \max_t |a_{tj}|$, the maximum taken over the active rows $t$.

```pseudo id=main
MARKOWITZ-LU(A, u)
L1  build the row and column patterns of A; all rows and columns are active
L2  for k ← 1 to n do
L3      for each active column j: m_j ← max over active rows t of |a_tj|; if m_j = 0 then return "singular"
L4      (p, q) ← the acceptable entry (|a_pq| ≥ u · m_q) with the least (r_p − 1)(c_q − 1)
L5      pivot k is (p, q); row k of U ← the active part of row p
L6      for each active row i ≠ p with a_iq ≠ 0 do
L7          l_ik ← a_iq / a_pq
L8          for each active column j ≠ q with a_pj ≠ 0 do
L9              a_ij ← a_ij − l_ik · a_pj          ▷ if a_ij was 0, this is a fill entry
L10     deactivate row p and column q
L11 return the row order p_1, ..., p_n, the column order q_1, ..., q_n, L and U
```

The result satisfies $PAQ = LU$, where $P$ puts row $p_k$ in place $k$, $Q$ puts column $q_k$ in place $k$, $L$ is unit lower triangular with the multipliers $l_{ik}$, and $U$ is upper triangular. Ties at line L4 can go to the larger $|a_{pq}|$, and then to the lower index.

**Theorem (the count bounds the fill of one step).** If step $k$ pivots on $(p, q)$, the number of entries of $A^{(k)}$ that are zero before the step and nonzero after it is at most $(r_p - 1)(c_q - 1)$. The step does exactly $(r_p - 1)(c_q - 1)$ multiply and subtract operations and $c_q - 1$ divisions.

*Proof.* Let $R = \{j \ne q : a_{pj} \ne 0\}$, the other nonzero columns of the pivot row, so $|R| = r_p - 1$, and let $C = \{i \ne p : a_{iq} \ne 0\}$, so $|C| = c_q - 1$. Line L7 runs once for each $i \in C$, which gives the $c_q - 1$ divisions. Line L9 runs once for each pair $(i, j) \in C \times R$, which gives the $(r_p - 1)(c_q - 1)$ multiply and subtract operations. An entry $a_{ij}$ with $i \notin C$ is not changed, because its row is not touched; and an entry with $j \notin R$ in a row $i \in C$ is not changed, because line L9 runs only for $j \in R$. Row $p$ and column $q$ leave the active submatrix. So every entry that changes from zero to nonzero lies in $C \times R$, a set of $(r_p - 1)(c_q - 1)$ positions. $\square$

The bound is reached when all positions of $C \times R$ are zero before the step and no update cancels to zero. It is an upper bound because some of these positions can already be nonzero. With $r_p = 1$ or $c_q = 1$ the step creates no fill at all, so the rule first takes singleton rows and columns, which is exactly what a triangular part of the matrix needs.

**Theorem (threshold and growth).** With threshold $u$, every multiplier has $|l_{ik}| \le 1/u$. If $\mu_k$ is the largest magnitude in $A^{(k)}$, then $\mu_{k+1} \le (1 + 1/u)\,\mu_k$, so all entries of $U$ are at most $(1 + 1/u)^{n-1}$ times the largest entry of $A$.

*Proof.* The pivot is acceptable, so $|a_{pq}| \ge u |a_{iq}|$ for every active row $i$, and $|l_{ik}| = |a_{iq}| / |a_{pq}| \le 1/u$. Line L9 gives $|a_{ij} - l_{ik} a_{pj}| \le \mu_k + \mu_k / u$. Apply this $n - 1$ times. $\square$

With $u = 1$ only the largest entry of a column is acceptable, as in [partial pivoting](/partial-pivoting/) with a free choice of the column. A smaller $u$ admits more candidates and so gives sparser factors, at the price of a weaker bound on the [growth factor](/growth-factor/). The bound is a worst case; in practice the growth is usually far smaller, which is a measured fact and not a theorem.

**Worked example.** A hub node joined by $1$ S to each of three leaf nodes, with $1$ S from each leaf to ground, has the nodal matrix below (hub first). Take $u = 1$.

$$A = \begin{pmatrix} 3 & -1 & -1 & -1 \\ -1 & 2 & 0 & 0 \\ -1 & 0 & 2 & 0 \\ -1 & 0 & 0 & 2 \end{pmatrix}$$

| step | candidate | $(r - 1)(c - 1)$ | choice and effect |
|---|---|---|---|
| 1 | hub diagonal $(1,1)$ | $3 \cdot 3 = 9$ | not chosen |
| 1 | leaf diagonal $(2,2)$ | $1 \cdot 1 = 1$ | chosen; the update hits only $(1,1)$, which is already nonzero: no fill |
| 1 | entry $(1,2)$ | $3 \cdot 1 = 3$ | not acceptable: $1 < 1 \cdot 2$ |
| 2 | leaf diagonal $(3,3)$ | $1$ | chosen; no fill |
| 3 | leaf diagonal $(4,4)$ | $1$ | chosen; no fill |
| 4 | hub diagonal $(1,1)$ | $0$ | chosen; its value is now $3 - 3 \cdot \tfrac{1}{2} = \tfrac{3}{2}$ |

The factors have no fill. In the natural order, the first step pivots on the hub, and its update writes all 6 off-diagonal positions of the $3 \times 3$ leaf block, which were zero. With $1$ A injected into the hub, both orders give the hub voltage $2/3$ V and the leaf voltages $1/3$ V. The same contrast holds for a hub with $m$ leaves: Markowitz gives no fill and the natural order gives $m(m - 1)$ fill entries.

On larger circuit-like matrices the rule does not reach zero fill, and the gain is a measured one. On the nodal matrices of square resistor grids with a conductance to ground at every node (row-major numbering, $u = 1/10$, exact arithmetic, the code of this page), the measured fill is:

| grid | unknowns | nonzeros of $A$ | fill, natural order | fill, Markowitz |
|---|---|---|---|---|
| $5 \times 5$ | 25 | 105 | 128 | 82 |
| $6 \times 6$ | 36 | 156 | 250 | 142 |
| $8 \times 8$ | 64 | 288 | 686 | 346 |

These are toy inputs, not benchmark results.

**Cost.** The arithmetic of step $k$ is $(r_p - 1)(c_q - 1)$ operations by the theorem, so the total arithmetic is the sum of the chosen counts plus the divisions. The search of lines L3 and L4 is the expensive part when it is done as written: it looks at every active entry, which costs $O(\mathrm{nnz}(A^{(k)}))$ per step and up to $O(n^3)$ in total on a matrix that fills in. Practical codes keep the rows and the columns in lists by their counts and look only at a few rows and columns of least count, which makes the search cheap in practice but no longer guarantees the least count. Finding an order with the least total fill is NP-hard already for symmetric matrices with diagonal pivots (Yannakakis 1981), so the greedy rule has no guarantee of optimal fill, and none is known for any fixed ratio.

## Classic examples

- **SPICE and its descendants.** Kundert's Sparse package, the solver of Berkeley SPICE3, factors the MNA matrix with Markowitz pivoting and a relative threshold. It chooses the order at the first factorization and reuses it in the later Newton iterations until a pivot becomes too small.
- **Linear programming.** Markowitz introduced the rule to keep the elimination form of the basis inverse sparse in the simplex method, which is still where it is used most in optimization codes.
- **Power network equations.** Tinney and Walker (1967) ordered the nodal equations of power systems by fewest connections. For a symmetric matrix with diagonal pivots the Markowitz count of the diagonal entry of a node of degree $d$ is $d^2$, so the rule becomes [minimum degree](/minimum-degree-ordering/).
- **Unsymmetric multifrontal and supernodal codes.** They choose pivots inside dense frontal matrices with a threshold test and Markowitz-like counts, see [multifrontal method](/multifrontal-method/).

Markowitz described the rule in 1957 in a paper on the elimination form of the inverse for linear programming, and Tinney and Walker (1967) used related orders for the nodal equations of power networks. Threshold pivoting, the Markowitz count together with a relative size test, is the form that Duff, Erisman and Reid present as standard. Kundert's Sparse package brought it to Berkeley SPICE3. Later circuit solvers such as KLU replaced the run-time search by a symbolic order and a column pivot test.

## Variations

- **Symbolic order, then numerical check.** Order the pattern once, for example by minimum degree on the pattern of $A + A^{\mathsf T}$, and during the factorization accept the planned diagonal pivot when it passes the threshold, else pivot inside its column. This is the approach of [KLU](/klu-solver/) with [Gilbert-Peierls LU](/gilbert-peierls-lu/), which does no Markowitz search at run time.
- **Reuse of the order.** In a transient simulation the pattern never changes and the values change slowly. The simulator keeps the pivot sequence and repeats only the arithmetic, and it falls back to a new Markowitz search when a reused pivot fails the threshold.
- **Restricted search.** Search only the rows and the columns with the fewest nonzeros. Duff, Erisman and Reid discuss searches limited to a few rows and columns of least count, which in their reported experience give orders close to those of the full search.
- **Rook and complete pivoting.** [Complete pivoting](/complete-pivoting/) takes the largest entry of the whole active matrix and ignores sparsity. Threshold rook pivoting asks that the pivot pass the threshold in its row and in its column.
- **Local minimum fill.** Count the exact fill of each candidate instead of the bound. This costs more and gives slightly better orders on some matrices; it is still greedy.

## Pitfalls

- **Using the counts of the original matrix.** The counts must be those of the active submatrix at each step. Counts from $A$ alone give a static order that ignores the fill created so far.
- **Forgetting the threshold.** The least count alone can pick a tiny pivot, and the factors then have huge entries and large rounding error. In a circuit this happens with a small conductance next to a large one, or with a gmin conductance of $10^{-12}$ S.
- **A zero diagonal is not a zero pivot.** The row of a voltage source has a zero diagonal in MNA, but the matrix is usually nonsingular. The rule handles it by choosing an off-diagonal pivot; a code that only looks at diagonal entries fails.
- **Cancellation.** The count bounds the structural fill. An update can cancel to an exact zero; a code that stores it keeps a structural nonzero, and a code that drops it must update the counts. The code of this page keeps it.
- **Reusing an order after the values change.** A pivot that passed the threshold in one Newton iteration can fail it in the next. Check the threshold during the refactorization, not only at the first factorization.

## Exercises

1. Show that a matrix whose pattern is upper triangular after a row and column permutation is factored by Markowitz pivoting with no fill, for every threshold for which the diagonal entries pass the test.
2. For the arrow matrix with a full first row and column and a nonzero diagonal, of order $n$, count the fill of the natural order and of the reverse order. (Answer: $(n - 1)(n - 2)$ and 0.)
3. Give a $3 \times 3$ matrix where the entry of least Markowitz count fails the threshold $u = 1/10$, and find the pivot that the rule takes instead.
4. Prove that for a symmetric pattern with diagonal pivots, the fill of eliminating a node of degree $d$ is at most $d(d - 1)$ entries, that is $d(d-1)/2$ symmetric pairs, and compare with the Markowitz count $d^2$.
5. Find a matrix on which the greedy rule gives more total fill than the best order.

## References
