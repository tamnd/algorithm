---
title: The bit-parallel update computes the steps of each LCS column
proves: [correctness]
status: full
---

We use the pseudocode of the page. Let $c[i, j] = \mathrm{lcs}(X_i, Y_j)$ for $0 \le i \le m$, $0 \le j \le n$. Bit $i - 1$ of a word is called *row $i$*. For a column $j$ let $\delta_j(i) = c[i, j] - c[i - 1, j]$ for $1 \le i \le m$, and let $E_j$ be the $m$-bit word whose row $i$ is $1 - \delta_j(i)$. A row with $\delta_j(i) = 1$ is a *step* of column $j$.

**Lemma 1 (unit differences).** For all $i, j \ge 1$: $c[i, j] - c[i - 1, j] \in \{0, 1\}$ and $c[i, j] - c[i, j - 1] \in \{0, 1\}$. So $E_j$ is well defined.

*Proof.* Adding one item to one of the two sequences cannot lower the LCS length, and it raises it by at most 1, since deleting that item from a common subsequence of the longer prefixes leaves a common subsequence that is shorter by at most 1. $\square$

**Lemma 2 (block rule).** Fix $j \ge 1$, write $a_i = c[i, j - 1]$, $b_i = c[i, j]$ and $y = y_j$. Let $1 \le s \le e \le m$ be rows with $b_{s-1} = a_{s-1}$, no step of column $j - 1$ at rows $s, \ldots, e - 1$, and a step at row $e$. Let $f$ be the first row in $[s, e]$ with $x_f = y$, if there is one. Then in rows $s, \ldots, e$, column $j$ has exactly one step, at row $f$ if $f$ exists and at row $e$ otherwise, and $b_e = a_e$.

The same holds for a final run: if column $j - 1$ has no step at rows $s, \ldots, m$ and $b_{s-1} = a_{s-1}$, then column $j$ has exactly one step in these rows, at the first row $f$ with $x_f = y$, if there is one, and no step otherwise.

*Proof.* Let $A = a_{s-1}$. By the assumptions, $a_i = A$ for $s - 1 \le i \le e - 1$ and $a_e = A + 1$. The LCS recurrence in the form of the [LCS table](/lcs-dynamic-programming/) is $b_i = a_{i-1} + 1$ if $x_i = y$, and $b_i = \max(a_i, b_{i-1})$ otherwise. By Lemma 1, $a_i \le b_i \le a_i + 1$.

Rows before $f$ (or all rows $s, \ldots, e - 1$ if $f$ does not exist or $f = e$): they are not matches, so $b_i = \max(a_i, b_{i-1}) = \max(A, b_{i-1})$, and from $b_{s-1} = A$ we get $b_i = A$. No step.

If $f$ exists and $f \le e - 1$: $b_f = a_{f-1} + 1 = A + 1$, a step. For $f < i \le e - 1$, $A + 1 = b_f \le b_i \le a_i + 1 = A + 1$, so no step. At $e$: $b_e \ge b_{e-1} = A + 1$; if $x_e = y$, $b_e = a_{e-1} + 1 = A + 1$; otherwise $b_e = \max(a_e, b_{e-1}) = A + 1$. So no step at $e$, and $b_e = A + 1 = a_e$.

If $f = e$: $b_e = a_{e-1} + 1 = A + 1$, a step at $e$, and $b_e = a_e$.

If $f$ does not exist: $b_e = \max(a_e, b_{e-1}) = \max(A + 1, A) = A + 1$, a step at $e$, and $b_e = a_e$.

For a final run, the same argument without the row $e$ gives the claim. $\square$

**Lemma 3 (blocks cover the column).** Let column $j - 1$ have steps at rows $e_1 < \cdots < e_t$. Split the rows into the blocks $[1, e_1], [e_1 + 1, e_2], \ldots, [e_{t-1} + 1, e_t]$ and the final run $[e_t + 1, m]$ (empty if $e_t = m$). Then Lemma 2 applies to each of them, and so it describes all steps of column $j$.

*Proof.* The first block starts at $s = 1$ with $b_0 = a_0 = 0$. Each block ends with $b_e = a_e$ by Lemma 2, which is the condition $b_{s-1} = a_{s-1}$ for the next block or the final run. $\square$

**Lemma 4 (the word operations).** Let $V = E_{j-1}$, $M = M[y_j]$, $U = V \wedge M$, and $W = ((V + U) \vee (V \wedge \neg M)) \bmod 2^m$. Then $W = E_j$.

*Proof.* In $V$, a block $[s, e]$ of Lemma 3 is a run of 1 bits at rows $s, \ldots, e - 1$ and a 0 bit at row $e$; the final run is 1 bits at rows $s, \ldots, m$. Since $U \subseteq V$, $U$ has no bit at any row $e$.

*No carry between blocks.* Consider the part of $V + U$ formed by the bits of one block $[s, e]$. Its value in $V$ is $2^{e-1} - 2^{s-1}$ (bits $s - 1$ to $e - 2$), and in $U$ it is a subset of the same bits, so the sum is less than $2 \cdot 2^{e-1} - 2 \cdot 2^{s-1} < 2^e$. Its highest possible bit is $e - 1$, which is row $e$. So the block, with its carry entering from below equal to 0, produces no carry into row $e + 1$. By induction from the lowest block upward, the carry into each block is 0, and $V + U$ can be computed block by block.

*Inside a block $[s, e]$.* The block of $V$ has 1 bits at $s, \ldots, e - 1$ and 0 at $e$.

- If $U$ has no bit in the block, that is, no row of $[s, e - 1]$ is a match, then $V + U$ equals $V$ in the block: 1 at $s, \ldots, e - 1$ and 0 at $e$. $V \wedge \neg M$ is 0 at $e$, since $V$ is. So $W$ is 0 at row $e$ and 1 at rows $s, \ldots, e - 1$. By Lemma 2, $f$ is $e$ or does not exist, and in both cases the only step is at $e$. This matches.
- If $U$ has a bit in the block, let $f$ be its lowest row; it is the first match in $[s, e]$, since $V$ is 1 at all of $s, \ldots, e - 1$. Adding the bit at row $f$ to the 1 bits at rows $f, \ldots, e - 1$ makes them 0 and sets row $e$. The other bits of $U$, at rows in $(f, e - 1]$, then fall on 0 bits and are set with no carry. So $V + U$ is 1 at rows $s, \ldots, f - 1$, 0 at $f$, equal to $M$ at rows $f + 1, \ldots, e - 1$, and 1 at $e$. The word $V \wedge \neg M$ is 1 exactly at the rows of $[s, e - 1]$ that are not matches. The OR is 1 at all rows of $[s, e]$ except $f$, where both terms are 0 ($x_f = y_j$, and the sum is 0 there). By Lemma 2 the only step is at $f$. This matches.

*Final run $[s, m]$.* If $U$ has no bit there, $W$ is all 1 in the run, and by Lemma 2 there is no step. Otherwise, with $f$ the lowest bit of $U$, the carry from row $f$ runs through rows $f, \ldots, m$ and leaves the word, where the mod $2^m$ drops it; the rest is as in a block, without row $e$. So $W$ is 1 at all rows of the run except $f$, as Lemma 2 says.

Each row of $W$ therefore equals the row of $E_j$. $\square$

**Theorem.** BIT-PARALLEL-LCS returns $\mathrm{lcs}(X, Y)$.

*Proof.* Line L1 builds the masks. Column 0 of the table is all 0, so it has no step, and $E_0 = 2^m - 1$, which is line L2. By Lemma 4 and induction on $j$, after round $j$ of line L3, $V = E_j$. After round $n$, the number of 0 bits of $V$ is the number of steps of column $n$, which is $\sum_{i=1}^m \delta_n(i) = c[m, n] - c[0, n] = c[m, n]$. Line L6 returns $m$ minus the number of 1 bits, which is this number. $\blacksquare$

**Cost.** Each round does a constant number of operations on $m$-bit words, each of which is $\lceil m / w \rceil$ machine-word operations, with the carry of the addition passed from each machine word to the next. So the loop takes $\Theta(n \lceil m / w \rceil)$ time, and line L1 takes $\Theta(\sigma \lceil m / w \rceil + m)$.
