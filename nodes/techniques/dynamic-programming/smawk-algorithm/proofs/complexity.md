---
title: SMAWK reads O(n + m) entries and takes O(n + m) time
proves: [time.worst, space.extra]
status: full
---

We count the entries of $A$ that SMAWK reads. Each other step is charged to a read or to a row or column, so the time is of the same order.

**REDUCE on $p$ rows and $c$ columns reads at most $4c$ entries.** Each test of line L13 reads two entries. A test that is true pops a column. A column is pushed at most once, so it is popped at most once, and there are at most $c$ true tests. A test that is false, or a loop that stops because the stack is empty, ends the loop for the current column, which happens at most once per column. So there are at most $2c$ tests and $4c$ reads.

**Lines L5 to L9 on $p$ rows and $d$ reduced columns read at most $d + \lceil p/2 \rceil$ entries.** Let $k_0 = 0, k_1, k_2, \ldots$ be the values of $k$ at the passes for the even positions $0, 2, 4, \ldots$, and let $stop_t = k_{t+1}$ be the stop of pass $t$, with the last stop at most $d - 1$. Pass $t$ reads $stop_t - k_t + 1$ entries. The sum telescopes to at most $(d - 1) - 0 + \lceil p/2 \rceil$.

**The recurrence.** Let $T(p, c)$ be the largest number of reads of SMAWK on $p \ge 1$ rows and $c \ge 1$ columns, and $T(0, c) = 0$. After line L2, the call works on $d \le \min(c, p)$ columns, so

$$T(p, c) \le 4c + T(\lfloor p/2 \rfloor, \min(c, p)) + \min(c, p) + \lceil p/2 \rceil \le 4c + 2p + T(\lfloor p/2 \rfloor, p).$$

Let $p_0 = n$ and $p_\ell = \lfloor p_{\ell - 1}/2 \rfloor$, so $p_\ell \le n / 2^\ell$. At the top level the cost outside the recursion is at most $4m + 2n$. At level $\ell \ge 1$, the call has $p_\ell$ rows and at most $p_{\ell - 1}$ columns, so its cost outside the recursion is at most $4p_{\ell - 1} + 2p_\ell \le 4n/2^{\ell - 1} + 2n/2^\ell = 5n / 2^{\ell - 1}$. Summing,

$$T(n, m) \le 4m + 2n + \sum_{\ell \ge 1} \frac{5n}{2^{\ell - 1}} = 4m + 12n.$$

So SMAWK reads $O(n + m)$ entries. The rest of the work is $O(1)$ per read, plus $O(p)$ per call to build $R'$ in line L3 and $O(d)$ to find the positions of line L7 (with an array from columns to positions, or by walking $D$ forward together with $k$). These are bounded by the same geometric sum, so the time is $O(n + m)$.

**Lower bound.** Let $n \ge 1$ and $m \ge 2$. Fix any matrix whose rows $1, \ldots, n-1$ are strictly decreasing from left to right, for example $A[i][j] = -j$, and let row 0 be arbitrary. For $i < i'$ and $j < j'$ with $i' \ge 1$ we have $A[i'][j] > A[i'][j']$, so the implication of total monotonicity holds, and the matrix is totally monotone for every choice of row 0. An algorithm that does not read some entry $A[0][j]$ cannot tell row 0 with that entry as its only minimum from the same row with that entry larger than all others, and the two answers differ. So every correct algorithm reads all $m$ entries of row 0 on some input. It also writes $n$ answers. The worst-case time is therefore $\Omega(n + m)$, and SMAWK is optimal up to a constant factor.

**Space.** The recursion has depth at most $\lfloor \lg n \rfloor + 1$. The lists at level $\ell$ have $O(n / 2^\ell)$ rows and columns, except the $m$ columns at the top, so all lists alive at one time have $O(n + m)$ entries, and the map $M$ has $n$ entries. $\blacksquare$
