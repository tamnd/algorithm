---
title: The Jonker-Volgenant algorithm returns a minimum-cost assignment
proves: [correctness, termination]
status: full
---

Let $C = (c_{ij})$ be an $n \times n$ real matrix with $n \ge 2$ (the cases $n \le 1$ are handled directly). The algorithm keeps column prices $v_j$ and a partial assignment: $x_i$ is the column of row $i$ or nil, and $y_j$ is the row of column $j$ or nil, with $x_i = j$ exactly when $y_j = i$. For each row put $u_i = \min_j (c_{ij} - v_j)$. Then

$$u_i + v_j \le c_{ij} \quad \text{for all } i, j \tag{1}$$

holds for any prices. The invariant is

**(CS)** for each assigned row $i$, $c_{i x_i} - v_{x_i} = u_i$.

**Lemma 1 (the initialization keeps (CS)).** (CS) holds after lines L2 to L4, and every change of prices and of the assignment in lines L5 to L10 keeps it. Lines L7 to L10 stop.

*Proof.* After line L3 for every column, $v_j = \min_i c_{ij}$, so $c_{ij} - v_j \ge 0$ for all $i, j$, and $u_i \ge 0$. Line L4 assigns row $i^*$ to column $j$ only if $c_{i^* j} = v_j$, a reduced cost of 0, which is the least possible. So (CS) holds.

Lowering a price $v_k$ raises $c_{ik} - v_k$ for every row and changes nothing else. For an assigned row $i$ with $x_i \ne k$, its value at $x_i$ is unchanged and its other values do not go down, so $x_i$ stays a minimum.

At line L6, row $i$ was a minimum row of exactly one column $k = x_i$ in line L3, so $v_k = c_{ik}$ was set there. Line L6 changes only the price of the column of the row it treats, and different rows treated there have different columns, so $v_k$ is unchanged when row $i$ is treated, and $c_{ik} - v_k = 0$. Let $\delta = \min_{j \ne k}(c_{ij} - v_j) \ge 0$, with the current prices. After $v_k \leftarrow v_k - \delta$, the value of row $i$ at $k$ is $\delta$, which is the least of its values. So (CS) holds for $i$, and for the other rows by the first paragraph.

At line L9, row $i$ is free, $a = c_{ij_1} - v_{j_1} = u_i$ and $b = \min_{j \ne j_1}(c_{ij} - v_j)$. If $a < b$, the new price makes the value of $i$ at $j_1$ equal to $b$, which is the new minimum of row $i$, and line L10 assigns $i$ to $j_1$. If $a = b$, no price changes, and $i$ is assigned to $j_1$ or $j_2$, both of value $a = u_i$. The row $i_0$ that loses its column becomes free, so (CS) no longer speaks of it. Other rows are covered by the first paragraph.

Each pass makes at most $2n$ bids, and a row that is not allowed to bid goes to the list of free rows, so each pass stops. $\square$

After line L10, the free rows are exactly the rows with $x_i = $ nil: every row that loses its column at line L10 is put back on a list, and rows that were never assigned in L4 start on the list.

**Lemma 2 (one augmentation).** Suppose (CS) holds when line L12 starts for a free row $f$. Then lines L13 to L17 stop with a free column $\text{end}$, and after lines L18 and L19 (CS) holds, row $f$ is assigned, and every row assigned before is still assigned.

*Proof.* For an assigned row $i$ and any column $j'$, write $r_{ij'} = c_{ij'} - v_{j'} - u_i \ge 0$ for its reduced cost; by (CS), $r_{i x_i} = 0$. In line L17, with $i = y_j$, the quantity $(c_{ij'} - v_{j'}) - (c_{ij} - v_j)$ equals $r_{ij'} - r_{ij} = r_{ij'}$, so $h = d_j + r_{ij'}$. The prices do not change during lines L12 to L17.

*Invariants of the search.* While lines L13 to L17 run:

(a) a column enters $R$ with $d_j = \mu$ for the current $\mu$, and then $d_j$ never changes; the value $\mu$ never decreases;
(b) every column $j \notin R$ has $d_j \ge \mu$, and $T$ is a set of columns outside $R$ with $d_j = \mu$ whose values do not change while they are in $T$;
(c) a value $d_j$ and the row $\text{pred}[j]$ are always set together, and either $\text{pred}[j] = f$ and $d_j = c_{fj} - v_j$, or $\text{pred}[j] = y_k$ for a column $k$ that was in $R$ at that moment and $d_j = d_k + r_{y_k j}$.

Line L14 sets $\mu$ to the least $d_j$ outside $R$, so (b) holds after it, and the new $\mu$ is at least the old one by (b). Line L16 moves a column of $T$, with $d_j = \mu$, into $R$. Line L17 changes only columns outside $R \cup T$, and each new value is $h = d_j + r_{ij'} \ge d_j = \mu$; a value equal to $\mu$ puts the column into $T$. This gives (a), (b) and (c).

*Termination.* Each pass of the loop that does not stop moves one column into $R$. Only assigned columns enter $R$: a free column in $T$ stops the loop at line L15, and a free column that reaches $\mu$ at line L17 stops it at once. Row $f$ is free, so at most $n - 1$ columns are assigned, and at most $n - 1$ columns enter $R$. When $T$ is empty, some column is outside $R$, so line L14 is defined. So the loop stops, with a free column $\text{end} \notin R$ and $d_{\text{end}} = \mu$.

*A key inequality.* Put $\bar d_j = \min(d_j, \mu)$ with the final values; by (a) and (b), $\bar d_j = d_j$ for $j \in R \cup \{\text{end}\}$ and $\bar d_j = \mu$ for the other columns. We claim: for each $k \in R$, with row $i = y_k$, and each column $j$,
$$\bar d_j \le d_k + r_{ij}. \tag{2}$$
When $k$ was moved into $R$, the value of $\mu$ was $d_k$. If $j$ was already in $R$, then $d_j \le d_k$ by (a). If $j$ was in $T$, then $d_j = d_k$ and it does not change later. If line L17 then compared $j$, afterwards $d_j \le d_k + r_{ij}$, and values only go down. If line L17 stopped before comparing $j$, this was the last pass, so the final $\mu$ equals $d_k$ and $\bar d_j \le \mu = d_k$. In every case (2) holds, as $r_{ij} \ge 0$. Also, for every $j$,
$$\bar d_j \le d_j \le c_{fj} - v_j, \tag{3}$$
since line L12 sets $d_j$ to this value and it only decreases.

*New prices.* Line L18 sets $v'_j = v_j + \bar d_j - \mu$ for all $j$ (no change outside $R$). Then for any row $i$ that was assigned and any column $j$,
$$c_{ij} - v'_j = u_i + r_{ij} - \bar d_j + \mu.$$
Let $k = x_i$ before line L19. If $k \notin R$, then $\bar d_k = \mu \ge \bar d_j$ and $r_{ik} = 0$, so $c_{ik} - v'_k = u_i \le c_{ij} - v'_j$. If $k \in R$, (2) gives $c_{ij} - v'_j \ge u_i - d_k + \mu = c_{ik} - v'_k$. So every row keeps a minimum at its old column; we use this for the rows that line L19 does not move.

*The path.* By (c), following $\text{pred}$ from $\text{end}$ gives $j_t = \text{end}$, $i_{t-1} = \text{pred}[j_t] = y_{j_{t-1}}$, and so on, to a column $j_1$ with $\text{pred}[j_1] = f$; each $j_s$ with $s < t$ is in $R$, and it entered $R$ before $j_{s+1}$ received its $\text{pred}$, so the walk goes back in time and stops. The equalities of (c) hold with the final values, since values in $R$ do not change: $d_{j_1} = c_{f j_1} - v_{j_1}$ and $d_{j_{s+1}} = d_{j_s} + r_{i_s j_{s+1}}$, where $i_s = y_{j_s}$. Line L19 assigns $f$ to $j_1$ and each $i_s$ to $j_{s+1}$, and no other row changes.

For a moved row $i_s$: $c_{i_s j_{s+1}} - v'_{j_{s+1}} = u_{i_s} + r_{i_s j_{s+1}} - d_{j_{s+1}} + \mu = u_{i_s} - d_{j_s} + \mu$, which is the least value of row $i_s$ by (2) with $k = j_s$. For row $f$: $c_{f j_1} - v'_{j_1} = d_{j_1} - \bar d_{j_1} + \mu = \mu$, and for any $j$, $c_{fj} - v'_j = (c_{fj} - v_j) - \bar d_j + \mu \ge \mu$ by (3). So (CS) holds after line L19, $f$ is assigned, and the other rows keep a column. $\square$

**Theorem.** LAPJV stops and returns a permutation $x$ of least total cost, with $u$ and $v$ satisfying (1) and equality on the pairs $(i, x_i)$.

*Proof.* By Lemma 1, (CS) holds when line L11 starts. Line L11 treats each free row once, and by Lemma 2 each augmentation keeps (CS), assigns its row and unassigns no row. So at the end every row is assigned to a distinct column, and $x$ is a permutation. The returned $u_i = c_{i x_i} - v_{x_i}$ equals $\min_j (c_{ij} - v_j)$ by (CS), so (1) holds, with equality on the chosen pairs.

Let $\sigma$ be any permutation. By (1),
$$\sum_i c_{i \sigma(i)} \ge \sum_i (u_i + v_{\sigma(i)}) = \sum_i u_i + \sum_j v_j = \sum_i (u_i + v_{x_i}) = \sum_i c_{i x_i},$$
because $\sigma$ and $x$ are both bijections onto the columns. So $x$ has the least cost. $\blacksquare$
