---
title: Sliding-window exponentiation returns x^e and uses at most t - 2 + ceil(t/k) + 2^(k-1) products
proves: [correctness, termination]
status: full
---

Let $x$ be an element of a monoid with identity 1, let $k \ge 1$, and let $e \ge 1$ have binary digits $e_{t-1} \ldots e_0$ with $e_{t-1} = 1$. For $-1 \le i \le t - 1$ write $P_i = \lfloor e / 2^{i+1} \rfloor$, the number formed by the digits above position $i$; so $P_{t-1} = 0$ and $P_{-1} = e$.

**Theorem.** SLIDING-WINDOW-POWER$(x, e, k)$ terminates and returns $x^e$. It uses at most $t - 1$ squarings in the main loop and at most $\lceil t/k \rceil - 1$ products by table entries, besides the at most $2^{k-1}$ products of line L1.

**1. The table.** Line L1 sets $T[1] = x$ and $T[u] = T[u-2] \cdot x^2$ for odd $u$ from 3 to $2^k - 1$. By induction on $u$, $T[u] = x^{u-2} x^2 = x^u$, by associativity. It uses one squaring and $2^{k-1} - 1$ products.

**2. The window is well defined.** At line L5, $e_i = 1$, so the set of indices $j$ with $\max(i - k + 1, 0) \le j \le i$ and $e_j = 1$ contains $i$ and is not empty; let $j$ be its least element. Then $1 \le i - j + 1 \le k$, the number $u = (e_i \ldots e_j)_2$ satisfies $2^{i-j} \le u < 2^{i-j+1} \le 2^k$, and $u$ is odd since its last digit is $e_j = 1$. So $T[u]$ exists.

**3. The invariant.** At each test of line L3, $y = x^{P_i}$.

*Proof.* At the first test, $i = t - 1$ and $y = 1 = x^0 = x^{P_{t-1}}$. Suppose $y = x^{P_i}$ at a test with $i \ge 0$.

- If $e_i = 0$, then $P_{i-1} = 2P_i + e_i = 2P_i$, and line L4 sets $y$ to $x^{P_i} x^{P_i} = x^{P_{i-1}}$ and $i$ to $i - 1$.
- If $e_i = 1$, let $j$ and $u$ be as in part 2 and $\ell = i - j + 1$. Then $P_{j-1} = \lfloor e/2^j \rfloor = 2^\ell \lfloor e/2^{i+1} \rfloor + (e_i \ldots e_j)_2 = 2^\ell P_i + u$. After $\ell$ squarings, $y = x^{2^\ell P_i}$, and after the product with $T[u] = x^u$, $y = x^{P_{j-1}}$, with $i$ set to $j - 1$.

In both cases the invariant holds at the next test. $\square$

**4. Termination and result.** Each pass through the loop decreases $i$ by at least 1, and the loop runs while $i \ge 0$, so it stops after at most $t$ passes, with $i = -1$, since a window never goes below index 0. By part 3, $y = x^{P_{-1}} = x^e$, which line L6 returns. Skipping squarings of $y = 1$ and replacing $1 \cdot T[u]$ by $T[u]$ does not change any value, since $1 \cdot 1 = 1$ and $1 \cdot z = z$. $\square$

**5. The counts.** Let the passes that take line L5 be windows $1, \ldots, W$, from the top. The first window starts at $i = t - 1$, since $e_{t-1} = 1$; while $y = 1$ nothing is counted, so the first window costs nothing. Every later digit is squared exactly once, at line L4 or within a window, so the main loop makes $t - \ell_1 \le t - 1$ squarings, where $\ell_1 \ge 1$ is the length of the first window, and $W - 1$ products by table entries.

To bound $W$, consider a window from $i$ to $j$. If $j > j_0 = \max(i - k + 1, 0)$, the digits $e_{j-1}, \ldots, e_{j_0}$ are all 0 by the choice of $j$ as the least index with a 1, so they are read at line L4 before the next window starts. Hence each window starts at least $k$ positions below the previous one: if a window starts at $i$, the next starts at an index at most $i - k$. Since the first starts at $t - 1$ and every start is at least 0, the starts $t - 1, \le t - 1 - k, \le t - 1 - 2k, \ldots$ give $(W - 1)k \le t - 1$, so $W \le \lfloor (t-1)/k \rfloor + 1 \le \lceil t/k \rceil$. Adding part 1, the total is at most $(t - 1) + (\lceil t/k \rceil - 1) + 2^{k-1}$. $\blacksquare$
