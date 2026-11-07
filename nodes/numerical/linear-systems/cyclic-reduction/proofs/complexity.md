---
title: Cost of cyclic reduction
proves: [time.worst, time.best, space.extra, flops.worst, span.worst]
status: full
---

Let the levels have orders $N_0 = n$, $N_{j+1} = \lfloor N_j/2 \rfloor$, until $N_L = 1$, so $L = \lfloor \log_2 n \rfloor$.

**Flops per row.** A reduced row with both neighbours costs $2$ divisions ($\alpha$, $\gamma$), $6$ multiplications and $4$ additions: $12$ flops. A reduced row without a right neighbour (when $N_j$ is even, the last odd row) costs $6$. Recovering an even unknown costs $5$ flops with two neighbours, $3$ with one, and the final $1 \times 1$ solve costs $1$.

**Exact count for $n = 2^k - 1$.** Then $N_j = 2^{k-j} - 1$ is odd for all $j$, so every reduced row has both neighbours. The reduced rows number $\sum_{j \ge 1} N_j = \sum_{i=1}^{k-1}(2^i - 1) = n - k$, costing $12(n - k)$. The recovered unknowns number $\sum_{j < L} (N_j - N_{j+1}) = n - 1$; at each of the $k - 1$ levels two of them are at the ends, so they cost $5(n - 1) - 4(k - 1)$. With the final division, the total is $12(n - k) + 5(n - 1) - 4(k - 1) + 1 = 17 n - 16 k$.

**General $n$.** Every row costs at most its two-neighbour price, so the flops are at most $12 \sum_{j \ge 1} N_j + 5(n - 1) + 1$. Since $\sum_{j \ge 1} \lfloor n/2^j \rfloor = n - s(n)$, where $s(n) \ge 1$ is the number of ones in the binary expansion of $n$, this is at most $12(n - 1) + 5(n - 1) + 1 \le 17 n$. Each level has at most $2$ end unknowns at $3$ flops and at most one reduced row at $6$, so at most $4 + 6 = 10$ flops fewer than the full price $12(n - s(n)) + 5(n - 1) + 1$. With $s(n) \le \log_2 n + 1$ and $L \le \log_2 n$, the count is at least $17 n - 22 \log_2 n - 16$, which is $17 n - O(\log n)$. (For $n < 400$ the tests observe the sharper lower bound $17 n - 16(\lfloor \log_2 n \rfloor + 1)$.)

**Time.** Each flop is $O(1)$ work, and the bookkeeping per row is $O(1)$, so the time is $\Theta(n)$ in every case (every row is touched at least once).

**Space.** Level $j \ge 1$ stores four arrays of length $N_j$, and the back substitution an array of length $N_j$; $\sum_{j \ge 1} N_j < n$, so the extra storage is at most $5 n + O(1)$ numbers plus the copy of the input, $\Theta(n)$.

**Span.** With one processor per row, the rows of a level in lines L3 to L6 depend only on the previous level, so a level takes $O(1)$ parallel steps; the same holds for lines L10 to L11. There are $2L + 1 = \Theta(\log n)$ such phases, and they are sequential since each uses the previous one. So the span is $\Theta(\log n)$. $\blacksquare$
