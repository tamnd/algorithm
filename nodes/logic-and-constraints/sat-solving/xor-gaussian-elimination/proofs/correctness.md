---
title: Gauss-Jordan elimination over GF(2) decides XOR-SAT and returns a solution
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The system is $A x = b$ over $\mathrm{GF}(2)$, with $m$ rows and $n$ columns. Row $i$ is the equation $\bigoplus_{c} A[i][c]\, x_c = b_i$. All sums are taken modulo 2. Rows are numbered from 0, and $r$ is the number of pivot rows found so far.

**Lemma 1 (row operations keep the solutions).** Swapping two rows, and adding row $r$ to row $j \ne r$ (with $b_j \gets b_j \oplus b_r$), do not change the set of solutions $x \in \{0,1\}^n$.

*Proof.* A swap only reorders the equations. For the addition, if $x$ satisfies rows $j$ and $r$, it satisfies their sum, so it satisfies the new row $j$. Each other row is unchanged. The addition is its own inverse, because adding row $r$ twice adds 0. So each solution of the new system is a solution of the old one, by the same argument applied to the inverse step. $\square$

**Invariant.** After the loop of line L2 has handled the columns $1, \ldots, c$:

> **(E1)** The rows $0, \ldots, r - 1$ have pivot columns $pivot[0] < pivot[1] < \cdots < pivot[r-1] \le c$. Row $i$ has a 1 in column $pivot[i]$, and each other row has a 0 there.
>
> **(E2)** The rows $r, \ldots, m - 1$ have a 0 in each column $1, \ldots, c$.
>
> **(E3)** The system has the same solutions as the input system.

*Initialization.* Before the first column, $r = 0$ and $c = 0$. (E1) and (E2) say nothing, and (E3) holds.

*Maintenance.* Take column $c$. By (E2), the rows $r, \ldots, m-1$ have zeros in the columns before $c$.

- If no row $i \ge r$ has a 1 in column $c$ (line L3), then the rows $r, \ldots, m - 1$ also have a 0 in column $c$. (E2) holds for $c$, and (E1) and (E3) do not change.
- Else line L4 swaps a row $i \ge r$ with a 1 in column $c$ into position $r$. Rows at positions $r$ and above are only reordered, so (E2) still holds for the columns before $c$. Now row $r$ has a 0 in each column before $c$, and in particular in each earlier pivot column. Lines L5 and L6 add row $r$ to each other row with a 1 in column $c$. This clears column $c$ in all rows except row $r$. It does not change any column before $c$ in any row, because row $r$ has zeros there. So each earlier pivot column still has its single 1, and the rows below $r$ keep their zeros before $c$. Line L7 records $pivot[r] = c$ and increases $r$. Now (E1) holds with the new pivot $c$, which is larger than the earlier ones, and (E2) holds for the rows from the new $r$ on, which have zeros in columns $1, \ldots, c$. (E3) holds by Lemma 1.

**Termination.** The loop of line L2 runs $n$ times, and each run does at most $m$ row operations. Lines L8 to L11 are loops over at most $m$ rows.

**Theorem.** XOR-GAUSS returns UNSAT if and only if the system has no solution. When it returns $x$, $x$ is a solution. The system has either no solution or exactly $2^{n - r}$ solutions, where $r$ is the final number of pivots, the rank of $A$.

*Proof.* At the end, $c = n$, so by (E2) the rows $r, \ldots, m - 1$ are zero on the left. Such a row says $0 = b_j$.

- If line L9 returns, some row says $0 = 1$, which no $x$ satisfies. By (E3) the input system has no solution.
- Else each zero row says $0 = 0$, which each $x$ satisfies. Call the columns that are not pivots *free*. By (E1), row $i < r$ has a 1 in column $pivot[i]$, a 0 in each other pivot column, and some entries in free columns. So row $i$ is the equation
$$x_{pivot[i]} = b_i \oplus \bigoplus_{c \text{ free}} A[i][c]\, x_c. \tag{1}$$
For each choice of the $n - r$ free variables, (1) gives exactly one value to each pivot variable, and the result satisfies each row. Every solution arises this way, since its free values determine its pivot values by (1). So there are exactly $2^{n - r}$ solutions of the final system, and by (E3) of the input system. Lines L10 and L11 take all free variables equal to 0, so (1) gives $x_{pivot[i]} = b_i$, which is what line L11 sets. So $x$ is a solution. $\blacksquare$

**Cost.** For each of the $n$ columns, line L3 scans at most $m$ rows. A pivot is found at most $\min(m, n)$ times, and each time lines L5 and L6 do at most $m$ additions of rows of $n$ entries. So the time is $O(nm + \min(m, n) \cdot m \cdot n) = O(m n \min(m, n))$ entry operations. With rows packed into words of $w$ entries, a row addition takes $\lceil n / w \rceil$ word operations, which divides the main term by about $w$.
