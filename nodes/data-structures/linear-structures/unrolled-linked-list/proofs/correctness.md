---
title: The unrolled linked list keeps its invariant and implements the list type
proves: [correctness]
status: full
---

**Claim.** Let $b \ge 2$ and $h = \lfloor b/2 \rfloor$. If the invariant (U1) to (U3) holds before an operation, then GET$(L, i)$ for $0 \le i < n$ returns $s_i$; INSERT$(L, i, x)$ for $0 \le i \le n$ leaves the sequence $(s_0, \dots, s_{i-1}, x, s_i, \dots, s_{n-1})$; DELETE$(L, i)$ for $0 \le i < n$ returns $s_i$ and leaves $(s_0, \dots, s_{i-1}, s_{i+1}, \dots, s_{n-1})$; and the invariant holds afterwards.

**Setup.** The nodes are $v_1, \dots, v_k$ with counts $c_1, \dots, c_k$, and $P_t = c_1 + \dots + c_{t-1}$ is the number of items before node $v_t$. By (U1), node $v_t$ holds the positions $P_t$ to $P_t + c_t - 1$ at its offsets 0 to $c_t - 1$. The invariant is:

> (U1) the arrays of $v_1, \dots, v_k$, read in order, form $s$; (U2) $1 \le c_t \le b$ for each $t$; (U3) if $k \ge 2$ then $c_t \ge h$ for each $t$.

Since $b \ge 2$, $h \ge 1$, and $b - h = \lceil b/2 \rceil \ge h$.

**Lemma 1 (FIND).** Let $L.head \ne \text{nil}$ and $0 \le i_0 \le n$. FIND$(L, i_0)$ returns $(p, v_t, j)$ with $p = v_{t-1}$ (nil for $t = 1$) and $i_0 = P_t + j$, where $0 \le j < c_t$ if $i_0 < n$, and $t = k$, $j = c_k$ if $i_0 = n$.

*Proof.* The loop of lines L2 and L3 keeps: $v = v_t$, $p = v_{t-1}$, $i = i_0 - P_t$, and $i \ge 0$. This holds at the start with $t = 1$, $P_1 = 0$. A step runs only when $i \ge c_t$, and it sets $i \leftarrow i - c_t = i_0 - P_{t+1} \ge 0$ and moves to $v_{t+1}$, so the statement holds for $t + 1$. Each step increases $t$ by 1 and the loop stops at the latest when $t = k$, since then $v.next = \text{nil}$; so it stops after at most $k - 1$ steps. At the exit, either $i < c_t$, so $j = i$ satisfies $0 \le j < c_t$; or $t = k$ and $i \ge c_k$, so $i_0 \ge P_k + c_k = n$, hence $i_0 = n$ and $j = c_k$. If $i_0 < n$, the second case is impossible, so $0 \le j < c_t$. If $i_0 = n$, the first case would give $n = P_t + j < P_t + c_t \le n$, a contradiction, so $t = k$ and $j = c_k$. $\square$

**GET and SET.** For $0 \le i < n$, Lemma 1 gives the node $v_t$ and an offset $j < c_t$ with $i = P_t + j$, which by (U1) is the cell of $s_i$. Line L5 returns it. Neither changes the structure of the nodes, so the invariant holds.

**Lemma 2 (INSERT).** If the list is empty, line L6 makes one node holding $x$, which satisfies (U1) to (U3) with $k = 1$. Else let FIND return $(p, v_t, j)$ with $i = P_t + j$ and $0 \le j \le c_t$ (by Lemma 1).

*Case 1, $c_t < b$.* Line L11 shifts the items at offsets $j$ to $c_t - 1$ up by one and writes $x$ at offset $j$. Read in order, the arrays now give $s_0, \dots, s_{P_t + j - 1}, x, s_{P_t + j}, \dots$, which is the new sequence. The count becomes $c_t + 1 \le b$, and no count drops, so (U2) and (U3) hold.

*Case 2, $c_t = b$.* Line L9 moves the last $h$ items of $v_t$ to a new node $w$ placed after $v_t$, so $v_t$ keeps $b - h$ items and the order of (U1) is unchanged. Both new counts $b - h$ and $h$ are at least $h \ge 1$. If $j \le b - h$, position $i$ is at offset $j$ of $v_t$, which now has $b - h$ items. If $j > b - h$, position $i$ is at offset $j - (b - h)$ of $w$, and $0 < j - (b - h) \le h$; line L10 selects this node. Then line L11 inserts as in Case 1, and the chosen node gets $b - h + 1 \le b$ or $h + 1 \le b$ items (because $h \ge 1$ and $b \ge 2$). The nodes $v_t$ and $w$ now hold between $h$ and $b$ items. Every other node keeps its old count, which is between $h$ and $b$ by (U2) and (U3), since the old list had $v_t$ and at least one more node; when the old $k$ was 1 there is no other node. So (U2) and (U3) hold with $k + 1 \ge 2$ nodes. $\square$

**Lemma 3 (DELETE).** Let FIND return $(p, v, j)$, with $v = v_t$, $0 \le j < c_t$, and $i = P_t + j$. Line L13 returns $s_i$ by (U1) and shifts the later items of $v$ down, so the arrays read in order give the new sequence, and the count of $v$ is $c_t - 1$.

*Case 1, $c_t - 1 \ge h$, or $k = 1$.* If $c_t - 1 \ge h \ge 1$, all counts are still between $h$ and $b$. If $k = 1$ (that is, $p = \text{nil}$ and $v.next = \text{nil}$) and $c_t - 1 \ge 1$, (U3) does not apply. If $k = 1$ and $c_t - 1 = 0$, line L14 removes the node and the list is empty with $k = 0$. In each case the invariant holds.

*Case 2, $c_t - 1 < h$ and $k \ge 2$.* Since $c_t \ge h$ by (U3), the count of $v$ is exactly $h - 1$. Line L15 picks two adjacent nodes $u$ before $r$, one of them $v$: the successor of $v$ if it exists, else the predecessor $p$, which exists since $k \ge 2$. Let $o$ be the other node of the pair; by (U3), $o$ has $c_o \ge h$ items.

If $(h - 1) + c_o \le b$, line L16 appends the items of $r$ to $u$. Since $r$ follows $u$, the order of (U1) is unchanged. The merged node has $h - 1 + c_o \ge 2h - 1 \ge h$ items (as $h \ge 1$) and at most $b$. The list now has $k - 1$ nodes; if $k - 1 \ge 2$ every count is still at least $h$, and if $k - 1 = 1$ (U3) does not apply. So the invariant holds.

If $(h - 1) + c_o > b$, then $c_o \ge b - h + 2 \ge h + 1$, because $b + 1 \ge 2h$. Line L17 moves one item from $o$ to $v$: the first item of $r$ to the end of $u$ when $u = v$, or the last item of $u$ to the front of $r$ when $r = v$. In both cases the moved item stays between the items of $u$ and the items of $r$, so the order of (U1) is unchanged. Now $v$ has $h$ items and $o$ has $c_o - 1 \ge h$ items, both at most $b$, so (U2) and (U3) hold. $\square$

**Conclusion.** The empty list (no node, $n = 0$) satisfies the invariant. By Lemmas 2 and 3 and the paragraph on GET, every operation returns the value the list type asks for and keeps the invariant. By induction on the number of operations, any sequence of operations from the empty list behaves as the abstract list. $\blacksquare$
