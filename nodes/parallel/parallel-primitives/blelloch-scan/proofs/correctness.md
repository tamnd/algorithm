---
title: The Blelloch scan returns the exclusive scan with 2(m − 1) combines in 2 lg m rounds
proves: [correctness]
status: full
---

**Statement.** Let $\oplus$ be an [associative operator](/associative-operator/) on a set $S$ with identity $e$, and let $A[0 \ldots n-1]$ be an array over $S$ with $n \ge 1$. Let $K = \lceil \lg n \rceil$ and $m = 2^K$. Then BLELLOCH-SCAN returns $x[j] = A[0] \oplus \cdots \oplus A[j-1]$ for $0 \le j < n$ (with $x[0] = e$) and the total $A[0] \oplus \cdots \oplus A[n-1]$. It applies $\oplus$ exactly $2(m - 1) < 4n$ times in exactly $2K$ rounds, and the updates of each round touch distinct cells.

**Notation.** After line L2, $x$ holds $A$ followed by $m - n$ copies of $e$; call this padded array $B[0 \ldots m-1]$. For $0 \le i \le j < m$, write $B[i..j] = B[i] \oplus \cdots \oplus B[j]$, and write $B[0..-1] = e$ for the empty prefix. Each bracketing in order gives the same value, and $B[i..k] \oplus B[k+1..j] = B[i..j]$. Since the padding is the identity, $B[0..j-1] = A[0..j-1]$ for $j \le n$ and $B[0..m-1] = A[0..n-1]$.

For $0 \le j < m$, let $h(j)$ be the largest $h \le K$ such that $2^h$ divides $j + 1$. Lay a complete binary tree over $B$: a node of height $h$ covers a block $[i, i + 2^h)$ with $2^h \mid i$. Cell $j$ is the right end of the nodes of heights $0, 1, \ldots, h(j)$ that end at $j$.

## 1. The up-sweep

The round with $h = 2^D$ (lines L3 to L5) updates each cell $r = i + 2^{D+1} - 1$ with $2^{D+1} \mid i$, which are exactly the cells with $h(r) \ge D + 1$. It reads the cell $\ell = r - 2^D$. Since $\ell + 1 = (r + 1) - 2^D$ and $2^{D+1} \mid r + 1$, we get $h(\ell) = D$. So no cell read in the round is written in the round, and the cells written are distinct. The round therefore has the same effect whether its updates run at the same time or in any order.

**Claim U.** After the rounds $D = 0, \ldots, t - 1$ of the up-sweep, $x[j] = B[j - 2^{\min(h(j), t)} + 1 .. j]$ for every $j$.

*Proof by induction on $t$.* For $t = 0$, $x[j] = B[j]$. Assume the claim for $t$ and run round $D = t$. A cell $r$ with $h(r) \ge t + 1$ held $B[r - 2^t + 1 .. r]$, and the cell $\ell = r - 2^t$, with $h(\ell) = t$, held $B[r - 2^{t+1} + 1 .. r - 2^t]$. The new value $x[\ell] \oplus x[r]$ is $B[r - 2^{t+1} + 1 .. r]$, which is the claim for $t + 1$. A cell with $h(j) \le t$ is not written, and $\min(h(j), t + 1) = h(j) = \min(h(j), t)$. $\square$

After all $K$ rounds, each cell $j$ holds the sum of the highest tree node that ends at $j$. In particular $x[m - 1] = B[0..m-1]$, which line L6 saves as the total.

## 2. The down-sweep

Line L6 sets $x[m - 1] = e$. The round with $h = 2^D$ (lines L7 to L11) handles each node $v$ of height $D + 1$, with block $[i, i + 2^{D+1})$. Write $\ell = i + 2^D - 1$ for the right end of its left child and $r = i + 2^{D+1} - 1$ for the right end of $v$ and of its right child. The round writes only these cells, and they are distinct for distinct nodes. Each node reads and writes only its own two cells.

**Claim D (Blelloch, Theorem 1.1).** Just before the round for height $D + 1$, for every node $v$ of height $D + 1$ with block $[i, i + 2^{D+1})$:

1. $x[r] = B[0..i-1]$, the sum of all items before $v$, and
2. $x[\ell] = B[i..\ell]$, the sum of the left child of $v$.

*Proof by induction downward on $D$, from $D = K - 1$.* For $D = K - 1$, $v$ is the root, $i = 0$ and $x[m - 1] = e = B[0..-1]$. The cell $\ell = 2^{K-1} - 1$ has $h(\ell) = K - 1$, it was not written since the up-sweep, and Claim U gives $x[\ell] = B[0..\ell]$.

Assume the claim before the round for height $D + 1$, with $D \ge 1$, and run that round. Line L9 saves $t = x[\ell]$, line L10 sets $x[\ell] \leftarrow x[r]$ and line L11 sets $x[r] \leftarrow x[r] \oplus t$. So after the round:

- the left child $u_1$ of $v$, with block $[i, i + 2^D)$ and right end $\ell$, has $x[\ell] = B[0..i-1]$, the sum before $u_1$;
- the right child $u_2$ of $v$, with block $[i + 2^D, i + 2^{D+1})$ and right end $r$, has $x[r] = B[0..i-1] \oplus B[i..i + 2^D - 1] = B[0..i + 2^D - 1]$, the sum before $u_2$.

So every node $u$ of height $D$ has the sum of the items before it at its right end, which is part 1 of the claim for the round for height $D$. For part 2, the left child of $u$ has height $D - 1$ and right end $\ell'$ with $h(\ell') = D - 1$. The down-sweep rounds so far wrote only cells with $h \ge D$, so $x[\ell']$ still has its value from the up-sweep, which by Claim U is the sum of the left child of $u$. $\square$

After the last round ($D = 0$), the same argument shows that every leaf $j$, which is a node of height 0 with block $[j, j + 1)$, has $x[j] = B[0..j-1]$. For $j < n$ this is $A[0..j-1]$, and line L12 returns these cells. The operand order on line L11, with the parent value on the left, matters: the parent value covers items before those of the left child. With $t$ on the left, the result is wrong for non-commutative operators.

For $n = 1$, $m = 1$, no round runs, the total is $A[0]$ and $x[0] = e$. For $n = 0$, line L1 returns the empty array and $e$.

## 3. The counts

The up-sweep round with $h = 2^D$ does one combine for each of the $m / 2^{D+1}$ nodes of height $D + 1$. Summed over $D = 0, \ldots, K - 1$, this is $m - 1$, the number of inner nodes of the tree. The down-sweep does one combine per inner node as well. So the work is $W = 2(m - 1)$. Since $m < 2n$, $W < 4n$, so the scan is [work-efficient](/work-efficiency/).

There are $K$ rounds in each sweep, so $2K = 2 \lceil \lg n \rceil$ rounds. In each round, a combine uses values from earlier rounds only, so a chain of dependent combines gains at most one combine per round. The value at cell $m - 1$ after the up-sweep is not used by the down-sweep, since line L6 overwrites it. So the longest chain of combines has exactly $2K - 1$ combines for $K \ge 1$. For the upper bound: after the up-sweep, a cell $j \ne m - 1$ ends a chain of $h(j) \le K - 1$ combines, cell $m - 1$ holds the constant $e$, and each of the $K$ down-sweep rounds adds at most one combine. For the lower bound: in the first down-sweep round, cell $m - 1$ gets $e \oplus x[2^{K-1} - 1]$, whose right operand ends a chain of $K - 1$ combines, so the cell ends a chain of $K$; each of the other $K - 1$ rounds then combines into cell $m - 1$ again.

With $m/2$ processors, each round takes $O(1)$ steps on an EREW PRAM, since the cells of a round are distinct, so the time is $O(\log n)$.

So BLELLOCH-SCAN computes the exclusive scan and the total with $2(m - 1)$ combines in $2 \lceil \lg n \rceil$ rounds. $\blacksquare$
