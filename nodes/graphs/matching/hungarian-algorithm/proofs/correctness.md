---
title: The Hungarian algorithm returns a least-cost assignment
proves: [correctness, termination]
status: full
---

Let $C$ be an $n \times m$ matrix with $1 \le n \le m$ and finite entries. (The implementation replaces a missing entry by a large finite cost first; the last part of this proof covers that step.) Rows are $1 \ldots n$, columns are $1 \ldots m$, and column 0 is a dummy. For a row $k$ and a column $j \ge 1$, the *reduced cost* is $\bar c_{kj} = c_{kj} - u_k - v_j$. A pair $kj$ is *tight* if $\bar c_{kj} = 0$. Column $j \ge 1$ is *matched* if $p[j] \ne 0$, and *free* otherwise.

**Round invariant (R).** Before the round of row $i$ (line L3):

1. $p$ restricted to the columns $1 \ldots m$ is injective on its nonzero values, and its nonzero values are exactly the rows $1 \ldots i-1$;
2. $\bar c_{kj} \ge 0$ for each row $k < i$ and each column $j \ge 1$;
3. $v_j \le 0$ for each column $j \ge 1$, and $v_j = 0$ for each free column;
4. each matched pair $(p[j], j)$ is tight;
5. $u_k = 0$ for each row $k \ge i$.

Line L1 makes (R) true for $i = 1$: there are no matched columns and no rows $k < 1$.

**Pass invariant (P).** Fix a round $i$. In this round, call a column *used* when its mark is true, and call the rows $p[j]$ of the used columns $j$ the *tree rows*; $p[0] = i$, so row $i$ is a tree row as soon as column 0 is used. At the end of each pass (after line L12):

1. every used column other than 0 is matched, and the tree rows are distinct;
2. $\bar c_{kj} \ge 0$ for each row $k \le i$ and each column $j \ge 1$;
3. for each column $j \ge 1$ that is not used, $\text{minv}[j] = \min \{ \bar c_{kj} : k \text{ a tree row} \}$, and $\text{way}[j]$ is a used column with $\bar c_{p[\text{way}[j]], j} = \text{minv}[j]$;
4. for each used column $j \ge 1$, the pairs $(p[j], j)$ and $(p[\text{way}[j]], j)$ are tight, and $\text{way}[j]$ was used before $j$;
5. (R3) and (R4) hold, and the column $j_1$ chosen at line L9 satisfies $\text{minv}[j_1] = 0$.

*Proof that (P) holds after each pass.* Consider a pass. At line L5, column $j_0$ becomes used and its row $i_0 = p[j_0]$ becomes a tree row. In the first pass, $j_0 = 0$ and $i_0 = i$. In a later pass, $j_0$ is the column $j_1$ of the pass before, which is matched, since otherwise line L14 would have ended the loop; so $i_0$ is a row $k < i$ that is not yet a tree row, because $p$ is injective. This gives (P1).

Lines L6 to L8 lower $\text{minv}[j]$ to $\bar c_{i_0 j}$ when that is smaller, and record $\text{way}[j] = j_0$. So, before the shift, $\text{minv}[j]$ is the least reduced cost from a tree row to $j$, for each column $j$ that is not used, and $\text{way}[j]$ names a column whose row reaches it. Line L9 sets $\delta = \min \{ \text{minv}[j] : j \text{ not used} \}$ and $j_1$ to a column that reaches it. There is at least one column that is not used, because the used columns other than 0 are matched and there are at most $i - 1 < m$ matched columns. So $\delta$ is finite.

Lines L10 to L12 add $\delta$ to $u_k$ for each tree row $k$ and subtract $\delta$ from $v_j$ for each used column $j$. Look at the effect on $\bar c_{kj}$ for a row $k \le i$ and a column $j \ge 1$:

- $k$ a tree row and $j$ used: $\bar c_{kj}$ does not change.
- $k$ a tree row and $j$ not used: $\bar c_{kj}$ drops by $\delta$. Before the shift $\bar c_{kj} \ge \text{minv}[j] \ge \delta$, so after it $\bar c_{kj} \ge 0$. Line L12 lowers $\text{minv}[j]$ by $\delta$ too, so (P3) stays true, and $\text{minv}[j_1] = 0$.
- $k$ not a tree row and $j$ used: $\bar c_{kj}$ grows by $\delta$. In the first pass no column $j \ge 1$ is used, so this case does not occur. In a later pass, $\delta \ge 0$, because by (P2) and (P3) of the pass before, every $\text{minv}[j]$ is at least 0 before line L6 and line L6 only takes minima with reduced costs that are at least 0 by (P2). So $\bar c_{kj}$ stays at least 0.
- $k$ not a tree row and $j$ not used: $\bar c_{kj}$ does not change.

Before the first pass, (R2) gives $\bar c_{kj} \ge 0$ for $k < i$. Row $i$ is a tree row from the first pass on, so the second case covers it. This proves (P2).

(R3): only used columns change $v_j$. A used column $j \ge 1$ was used in a pass after the first, where $\delta \ge 0$, so $v_j$ only goes down, and $v_j \le 0$ stays true. A free column is never used, by (P1), so its $v_j$ stays 0. (R4): a matched pair $(p[j], j)$ has both ends in the tree or both outside, because the tree rows are exactly the rows of used columns, and row $i$ is not matched. So its reduced cost does not change, and it stays tight.

(P4): when a column $j$ becomes used, it was $j_1$ in the pass before, so the pair $(p[\text{way}[j]], j)$ became tight at that time, and $(p[j], j)$ is tight by (R4). Later shifts do not change pairs with both ends in the tree, and line L8 does not change $\text{way}[j]$ for a used column. $\square$

**Each round ends.** Each pass makes one more column used. By (P1), the used columns other than 0 are matched, and at most $i - 1$ columns are matched. So after at most $i$ passes, the column $j_1$ of line L13 is free and line L14 ends the loop.

**The augmentation keeps (R).** When the loop ends, $j_0$ is a free column with $\text{minv}[j_0] = 0$, and $(p[\text{way}[j_0]], j_0)$ is tight by (P3). Line L15 follows the chain $j_0, \text{way}[j_0], \text{way}[\text{way}[j_0]], \ldots$, which reaches 0, because each $\text{way}$ value is a column used strictly before (P4), and sets $p[j] \leftarrow p[\text{way}[j]]$ for each column $j$ on the chain other than 0. So each row on the chain moves from its column $\text{way}[j]$ to the next column $j$; row $i = p[0]$ moves to the first column after 0; and the free column $j_0$ gets a row. The new pairs are the pairs $(p[\text{way}[j]], j)$, which are tight by (P3) and (P4). After the round, the matched rows are $1 \ldots i$, $p$ is still injective, and (R2) to (R4) hold for $i + 1$ by (P2) and (P5). Row $i + 1$ was not a tree row, so $u_{i+1} = 0$. So (R) holds before the round of row $i + 1$.

**Theorem.** HUNGARIAN stops, and the pairs of line L16 form an assignment of all rows to distinct columns of least total cost.

*Proof.* Each of the $n$ rounds ends, and by (R) after the last round, every row has its own column. Let $\sigma$ be the result and $\tau$ any assignment of rows to distinct columns. By (R2), $c_{k\tau(k)} \ge u_k + v_{\tau(k)}$ for each $k$, so

$$\sum_k c_{k\tau(k)} \ge \sum_k u_k + \sum_k v_{\tau(k)} \ge \sum_k u_k + \sum_{j=1}^{m} v_j,$$

where the second step uses $v_j \le 0$ for the columns that $\tau$ does not use (R3). For $\sigma$ both steps are equalities: each pair $(k, \sigma(k))$ is tight by (R4), and the columns that $\sigma$ does not use are free, with $v_j = 0$ by (R3). So $\sum_k c_{k\sigma(k)} = \sum_k u_k + \sum_j v_j \le \sum_k c_{k\tau(k)}$. $\blacksquare$

**Missing entries.** Let $F$ be the set of finite entries, with least value $a$ and largest value $b$, and let $B > n(b - a) + |a|$ replace each missing entry. An assignment that uses only finite entries costs at most $nb$. An assignment that uses at least one replaced entry costs at least $B + (n - 1)a > n(b - a) + a + (n - 1)a = nb$. So if some assignment avoids the missing entries, every optimal assignment of the new matrix avoids them too, and it is optimal for the old matrix. If no assignment avoids them, the optimal assignment of the new matrix uses one, and the implementation reports that there is none.
