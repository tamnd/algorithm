---
title: Hirschberg's algorithm runs in Θ(mn) time and O(n + log m) extra space
proves: [time.worst, space.extra]
status: full
---

Let $m \ge n \ge 1$ be the lengths after the two sequences are exchanged if $y$ is the longer one, so the rows run over $y$, of length $n$. (If $n = 0$, line L7 returns $m$ gap columns in $O(m)$ time.) A *cell* is one evaluation of line L5, or one score $s(a, b)$ that line L8 looks at. For a call on $m'$ rows ($m' = i_1 - i_0$) and $n'$ columns ($n' = j_1 - j_0$), let $C(m', n')$ be the largest number of cells that the call and all the calls below it compute, over all inputs and all choices of $k$.

**The recurrence.** Lines L7 and L8 give $C(0, n') = 0$, $C(m', 0) = 0$ and $C(1, n') = n'$. For $m' \ge 2$ and $n' \ge 1$, lines L10 and L11 compute $(mid - i_0) n' + (i_1 - mid) n' = m' n'$ cells, and line L13 makes calls on $\lfloor m'/2 \rfloor$ rows with $k$ columns and on $\lceil m'/2 \rceil$ rows with $n' - k$ columns, so

$$C(m', n') = m' n' + \max_{0 \le k \le n'} \bigl(C(\lfloor m'/2 \rfloor, k) + C(\lceil m'/2 \rceil, n' - k)\bigr).$$

Define $R(1) = 1$ and $R(q) = q + R(\lceil q/2 \rceil)$ for $q \ge 2$.

**Lemma 1.** $R$ is nondecreasing.

*Proof.* We show $R(q + 1) \ge R(q)$ by induction on $q$. For $q = 1$, $R(2) = 3 \ge 1$. For $q \ge 2$, $R(q + 1) - R(q) = 1 + R(\lceil (q + 1)/2 \rceil) - R(\lceil q/2 \rceil)$. The two arguments are equal or differ by 1, and both are at most $q$, so by the induction hypothesis the difference of the $R$ terms is at least 0. $\square$

**Lemma 2.** $C(m', n') \le n' R(m')$ for all $m' \ge 1$, $n' \ge 0$, with equality when $m'$ is a power of 2, for every choice of $k$.

*Proof.* By induction on $m'$. For $m' = 1$ and for $n' = 0$ both sides agree: $n' = n' R(1)$, and $0 = 0$. For $m' \ge 2$ and $n' \ge 1$, both calls of line L13 have at least one row, and by the induction hypothesis and Lemma 1,

$$C(\lfloor m'/2 \rfloor, k) + C(\lceil m'/2 \rceil, n' - k) \le k R(\lfloor m'/2 \rfloor) + (n' - k) R(\lceil m'/2 \rceil) \le n' R(\lceil m'/2 \rceil).$$

So $C(m', n') \le m' n' + n' R(\lceil m'/2 \rceil) = n' R(m')$. If $m'$ is a power of 2, then $\lfloor m'/2 \rfloor = \lceil m'/2 \rceil$ is a power of 2, both inequalities are equalities for every $k$ by the induction hypothesis, and the count is exactly $n' R(m')$. $\square$

**Lemma 3.** $R(q) \le 2q + \lceil \lg q \rceil - 1$, and $R(2^t) = 2^{t + 1} - 1$.

*Proof.* For $q = 1$ both sides are 1. For $q \ge 2$, let $2^{t - 1} < q \le 2^t$ with $t \ge 1$, so $\lceil \lg q \rceil = t$. Then $2^{t - 2} < q/2 \le \lceil q/2 \rceil \le 2^{t - 1}$, so $\lceil \lg \lceil q/2 \rceil \rceil = t - 1$. By induction,

$$R(q) \le q + 2\lceil q/2 \rceil + (t - 1) - 1 \le q + (q + 1) + t - 2 = 2q + \lceil \lg q \rceil - 1.$$

For $q = 2^t$, $R(2^t) = 2^t + R(2^{t - 1}) = 2^t + 2^{t - 1} + \cdots + 1 = 2^{t + 1} - 1$. $\square$

**Time.** The top call alone computes $mn$ cells, and by Lemmas 2 and 3 all calls together compute at most $n(2m + \lceil \lg m \rceil - 1) \le 3mn$ cells. Every other step of a call, apart from its cells, takes $O(1 + n')$ time: the allocation of the rows, the scan of line L12, and the output of the base cases, which emit at most $1 + n'$ columns. Each call with $m' \ge 2$ makes two calls with at least one row each, so the calls form a binary tree with at most $m$ leaves and at most $2m - 1$ nodes. At one depth of the tree, the column ranges of the calls do not overlap, so their $n'$ sum to at most $n$; the depth is at most $\lceil \lg m \rceil$. The extra work is $O(m + n \log m) = O(mn)$. So the running time is $\Theta(mn)$ in the worst case, and also in the best case, because of the $mn$ cells of the top call.

**Space.** One call holds the rows $f$ and $b$ of $n' + 1 \le n + 1$ cells each, and LAST-ROW holds one row and $O(1)$ other words. The rows of a call are no longer needed once line L12 has chosen $k$, so at any time $O(n)$ words of rows are live. The implementation keeps the pending calls on an explicit stack. Popping a call with $m' \ge 2$ pushes its two parts, the left part on top, so the stack holds the left part being worked on and at most one waiting right part for each depth above it. The number of rows at least halves from one depth to the next, rounded up, so there are at most $\lceil \lg m \rceil + 1$ depths and $O(\log m)$ entries of 4 words each. The output list of at most $m + n$ columns is not counted as extra space. So the extra space is $O(n + \log m)$, which is $O(\min(m, n) + \log \max(m, n))$ for the original input. $\blacksquare$
