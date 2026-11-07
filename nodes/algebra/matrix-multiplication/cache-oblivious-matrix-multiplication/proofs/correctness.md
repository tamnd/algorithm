---
title: The recursion that halves the largest dimension computes AB, and its miss count
proves: [correctness, termination]
status: full
---

Let $R$ be a semiring: addition is associative and commutative with a zero, multiplication is associative and distributes over addition on both sides. Commutativity of the multiplication and subtraction are not used. The call $\mathrm{REC\text{-}MULT}(A, B, C)$ has $A$ of size $m \times n$, $B$ of size $n \times p$ and $C$ of size $m \times p$, all given as index ranges into larger row-major arrays.

## Correctness

**Claim.** For all $m, n, p \ge 1$ and $\mathit{base} \ge 1$, the call ends with $C$ replaced by $C + AB$, and it changes no other entry of the arrays.

*Proof by strong induction on $mnp$.* If $\max(m, n, p) \le \mathit{base}$, line L1 runs the triple loop, which adds $\sum_k a_{ik} b_{kj}$ to each $c_{ij}$ of the range and touches nothing else.

Otherwise $\max(m, n, p) \ge 2$. The tests of lines L2 to L4 pick a dimension that is a largest one: line L2 when $m$ is a maximum, line L3 when $m$ is not a maximum and $n \ge p$ (then $n$ is a maximum), and line L4 when $p$ is the unique maximum. The picked dimension $x \ge 2$ splits into halves of sizes $\lfloor x/2 \rfloor \ge 1$ and $\lceil x/2 \rceil < x$. So both calls have a smaller product of sides, and the induction hypothesis applies to them.

- *Line L2.* With $A = (A_1 ; A_2)$ and $C = (C_1 ; C_2)$ split at the same row, $AB = (A_1 B ; A_2 B)$. The first call adds $A_1 B$ to $C_1$ and touches only $C_1$; the second adds $A_2 B$ to $C_2$.
- *Line L3.* With $A = (A_1 \ A_2)$ and $B = (B_1 ; B_2)$ split at the same inner index, block multiplication gives $AB = A_1 B_1 + A_2 B_2$. The first call adds $A_1 B_1$ to $C$, the second adds $A_2 B_2$, and since addition is associative and commutative the result is $C + AB$.
- *Line L4.* With $B = (B_1 \ B_2)$ and $C = (C_1 \ C_2)$ split at the same column, $AB = (A B_1 \ A B_2)$, and the two calls add the two parts to $C_1$ and $C_2$.

In each case the factor from $A$ stays on the left. $\square$

Started with $C = 0$, the method returns $AB$. When $m$, $n$ or $p$ is $0$ there is nothing to do; the implementation returns the zero $m \times p$ matrix at once.

**Summation order.** Fix an entry $c_{ij}$. Lines L2 and L4 send it to exactly one of the two calls. Line L3 sends it to both, first with the lower half of the inner range, then with the upper half. By induction, the terms $a_{ik} b_{kj}$ reach $c_{ij}$ with $k$ increasing, in the same order as in the plain triple loop. So in floating point the two methods give the same result, provided the leaves use the same order.

## Termination and depth

Each call either stops at line L1 or makes two calls with a smaller product $mnp$, so the recursion is finite.

Along a path from the root, each split replaces one side $x$ by $\lfloor x/2 \rfloor$ or $\lceil x/2 \rceil$, both at most $\lceil x/2 \rceil$. Since $\lceil \lceil x/2 \rceil / 2 \rceil = \lceil x/4 \rceil$, a side that has been split $t$ times is at most $\lceil x/2^t \rceil$, which is $1$ once $t \ge \lceil \lg x \rceil$. A side of size $1$ is never split, since only a largest side of size at least $2$ is split. So each path has at most $\lceil \lg m \rceil + \lceil \lg n \rceil + \lceil \lg p \rceil$ splits, which bounds the depth. The stack therefore holds $O(\log(mnp))$ frames.

## The miss bound for square matrices

Let $n$ be a power of two and $m = n = p$, with $\mathit{base} = 1$. The cache is ideal: $M$ words, lines of $B$ words, fully associative, with the optimal offline replacement.

**Shape of the recursion.** For a cube of side $s \ge 2$, line L2 splits $m$ (all sides are equal), then line L3 splits $n$ (now $m = s/2 < n = p$), then line L4 splits $p$. After these three levels, there are $8$ cubes of side $s/2$. So the subproblems at depth $3t$ are $8^t$ cubes of side $n/2^t$, and the method is the sequence of their calls, in some order.

**Lemma 1 (footprint).** A subproblem on a cube of side $s$ reads and writes words of three $s \times s$ submatrices of row-major arrays. Each of the $3s$ rows is a run of $s$ consecutive words, which touches at most $\lceil s/B \rceil + 1$ lines. So the subproblem touches at most $3s(\lceil s/B \rceil + 1)$ lines. If $s \ge B$, this is at most $9s^2/B$ lines, that is $9s^2$ words.

*Proof.* For $s \ge B$, $\lceil s/B \rceil + 1 \le s/B + 2 \le 3s/B$. The count of lines for a run is shown on the [blocked multiplication](/blocked-matrix-multiplication/) proofs page, Lemma 1. $\square$

**Lemma 2 (a subproblem that fits).** If a subproblem touches at most $M/B$ distinct lines, the ideal cache serves it with at most that many misses, whatever the cache holds at the start.

*Proof.* The replacement rule that never evicts a line of the subproblem during it, and evicts other lines when room is needed, misses at most once per line. The optimal rule misses no more often. $\square$

**Lemma 3 (concatenation).** For any sequences $\sigma_1, \ldots, \sigma_r$ of accesses, the optimal number of misses of the concatenation, from any start state, is at most the sum of the optimal numbers for the pieces started from an empty cache.

*Proof.* Run, on each piece in turn, a copy of the optimal schedule for that piece started from an empty cache, and keep the invariant that every line held by the copy is also in the real cache. When the copy loads a line, the real cache loads it too unless it is already there, and if it must evict, it evicts a line that the copy does not hold. Such a line exists, because just before the load the copy holds fewer than $M/B$ lines and the real cache is full. So the real cache misses only when the copy misses, and the optimal schedule of the concatenation misses no more than this one. $\square$

**Theorem.** Let $M \ge 36B^2$. If $9n^2 \le M$ and $n \ge B$, the method makes at most $9n^2/B$ misses. If $9n^2 > M$, it makes at most $54\, n^3/(B\sqrt M)$ misses.

*Proof.* The first case is Lemma 1 and Lemma 2 for the whole problem.

In the second case let $s = n/2^t$ be the largest power of two with $9s^2 \le M$ and $s \le n$. Since $9n^2 > M$, we have $s < n$, so $2s \le n$ and $9(2s)^2 > M$ by the choice of $s$. So $s > \sqrt M/6$, and since $\sqrt M/6 \ge B$, also $s \ge B$. The computation is the sequence of the $(n/s)^3$ subproblems at depth $3t$, which are cubes of side $s$. By Lemma 1 each touches at most $9s^2/B \le M/B$ lines, so by Lemma 2 each costs at most $9s^2/B$ misses from an empty cache. By Lemma 3 the total is at most
$$\Big(\frac{n}{s}\Big)^3 \cdot \frac{9 s^2}{B} = \frac{9 n^3}{s B} < \frac{54\, n^3}{B \sqrt M}. \qquad \square$$

**LRU.** Sleator and Tarjan (1985) proved that LRU with $k$ lines misses at most $\frac{k}{k - h + 1}$ times as often as the optimal rule with $h$ lines, plus $h$. With $k = M/B$ and $h = M/(2B)$, LRU with $M$ words makes at most about twice the misses of the ideal cache with $M/2$ words. If $M/2 \ge 36B^2$, the theorem with $M/2$ in place of $M$ gives at most $108\sqrt 2\, n^3/(B\sqrt M)$ misses, up to the additive term, for LRU with $M$ words when $9n^2 > M/2$.

**General shapes.** For all $m$, $n$, $p$ with a tall cache, Frigo, Leiserson, Prokop and Ramachandran prove the bound $\Theta(m + n + p + (mn + np + mp)/B + mnp/(B\sqrt M))$. Their proof follows the same plan, with the first subproblems that fit in the cache in place of the cubes of side $s$; it is not reproduced here.
