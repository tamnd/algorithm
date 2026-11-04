---
title: SMAWK returns the leftmost minimum of each row
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. $A$ is totally monotone: for rows $i < i'$ and columns $j < j'$, $A[i][j] > A[i][j'] \implies A[i'][j] > A[i'][j']$. The contrapositive is: $A[i'][j] \le A[i'][j'] \implies A[i][j] \le A[i][j']$. For a list of rows $R$ and a list of columns $C$, both in increasing order and with $C$ not empty, let $\lambda_C(r)$ be the leftmost column $c \in C$ with the least value $A[r][c]$ among the columns of $C$.

**Fact 1 (monotone minima).** If $r < r'$ are rows, then $\lambda_C(r) \le \lambda_C(r')$.

*Proof.* Let $j = \lambda_C(r)$ and suppose $j' = \lambda_C(r') < j$. Since $j$ is the leftmost minimum of row $r$ in $C$ and $j' \in C$ is to its left, $A[r][j'] > A[r][j]$. Total monotonicity with $r < r'$ and $j' < j$ gives $A[r'][j'] > A[r'][j]$, so $j'$ is not a minimum of row $r'$ in $C$, a contradiction. $\square$

**Fact 2 (removing losers).** Let $D \subseteq C$ with $\lambda_C(r) \in D$. Then $\lambda_D(r) = \lambda_C(r)$.

*Proof.* Let $j = \lambda_C(r)$. Each column of $D$ is in $C$, so $A[r][j] \le A[r][c]$ for $c \in D$, and each $c \in D$ with $c < j$ has $A[r][c] > A[r][j]$. So $j$ is the leftmost minimum of row $r$ in $D$. $\square$

**Lemma 3 (REDUCE).** Let $R = (r_0, \ldots, r_{p-1})$ with $p \ge 1$, and let $C$ be nonempty. REDUCE$(A, R, C)$ stops and returns a list $S$ of columns of $C$, in increasing order, with $1 \le |S| \le p$, such that $\lambda_C(r) \in S$ for each $r \in R$.

*Proof.* The stack only receives columns in the order of $C$, so it is increasing from bottom to top. Line L14 pushes only when $|S| < p$, so $|S| \le p$ always. Each pass of the loop of line L13 pops one column, and each column is pushed at most once, so the loop stops. After the first column, the stack is never empty at the end of an iteration of line L12: if line L13 empties it, line L14 pushes $c$ because $0 < p$.

Write $S = (s_0, \ldots, s_{q-1})$ from the bottom. We show this invariant, which holds after each iteration of line L12:

> **(I)** For each position $t$ with $1 \le t < q$ and each $u < t$, the column $s_t$ is not $\lambda_C(r_u)$. More exactly, $A[r_u][s_{t-1}] \le A[r_u][s_t]$ and $s_{t-1} < s_t$.

It holds for the empty stack. A pop removes the top and leaves the rest of the stack, with the same positions, so (I) stays true. A push of $c$ at position $q$ happens after the loop of line L13 ended. If $q = 0$, there is nothing to show. If $q \ge 1$, the loop ended because $A[r_{q-1}][s_{q-1}] \le A[r_{q-1}][c]$. Since $s_{q-1} < c$, the contrapositive of total monotonicity gives $A[r_u][s_{q-1}] \le A[r_u][c]$ for each $u \le q - 1$. So $c$ has a column to its left with a value at most as large on each of these rows, and it is not their leftmost minimum. This is (I) for position $q$.

Now take a column $c$ that is not in the final $S$. Then either it was popped or it was never pushed. We show that $c \ne \lambda_C(r_u)$ for each $u$.

- *Popped.* Some later column $c' > c$ arrived when $c$ was at position $t$, and line L13 found $A[r_t][c] > A[r_t][c']$. Total monotonicity gives $A[r_u][c] > A[r_u][c']$ for each $u \ge t$, so $c$ is not a minimum of these rows. For $u < t$, (I) at the time of the pop says that $c$ is not $\lambda_C(r_u)$.
- *Not pushed.* Then the loop of line L13 ended with $|S| = p$ and $A[r_{p-1}][s_{p-1}] \le A[r_{p-1}][c]$, with $s_{p-1} < c$. The contrapositive gives $A[r_u][s_{p-1}] \le A[r_u][c]$ for each $u \le p - 1$, so $c$ is not the leftmost minimum of any row.

So every $\lambda_C(r_u)$ stays in $S$. $\square$

**Theorem.** For $R$ nonempty or empty and $C$ nonempty, SMAWK$(A, R, C)$ stops and returns $M$ with $M[r] = \lambda_C(r)$ for each $r \in R$.

*Proof.* By induction on $|R|$. If $|R| = 0$, line L1 returns the empty map, which is correct. Let $|R| = p \ge 1$ and assume the claim for all shorter row lists.

Line L2 replaces $C$ by $D = $ REDUCE$(A, R, C)$. By Lemma 3, $D$ is nonempty and holds $\lambda_C(r)$ for each $r \in R$, so by Fact 2, $\lambda_D(r) = \lambda_C(r)$. It remains to compute $\lambda_D$.

The list $R'$ of line L3 has $\lfloor p/2 \rfloor < p$ rows, so by the hypothesis line L4 stops and gives $M[r] = \lambda_D(r)$ for $r \in R'$. The submatrix on the rows $R'$ and the columns $D$ is totally monotone, since each of its $2 \times 2$ submatrices is one of $A$.

Lines L5 to L9 treat the rows $R[0], R[2], \ldots$ in order. We claim that before the pass for the even position $i$, $D[k] = \lambda_D(R[i-1])$ if $i \ge 2$, and $k = 0$ if $i = 0$. Line L5 makes this true for $i = 0$, and line L9 sets $k$ to the position of $M[R[i+1]] = \lambda_D(R[i+1])$, which is the claim for $i + 2$. In the pass for $i$, let $j = \lambda_D(R[i])$. By Fact 1, $\lambda_D(R[i-1]) \le j$ when $i \ge 2$, and $j \le \lambda_D(R[i+1])$ when $i + 1 < p$. So $j$ lies in $D[k], \ldots, D[stop]$, with $stop = |D| - 1$ when $i + 1 = p$. Each column of $D$ left of $D[k]$ is not $j$, and each column right of $D[stop]$ is not $j$. Line L8 returns the leftmost column of least value in this range, and since $j$ is in the range and is the leftmost minimum of the whole row in $D$, line L8 returns $j$. Line L8 also never reads outside $D$, because $0 \le k \le stop \le |D| - 1$, where $k \le stop$ follows from Fact 1.

So line L10 returns $\lambda_D(r) = \lambda_C(r)$ for every $r \in R$. Each loop runs over a finite list, so the call stops. $\blacksquare$
