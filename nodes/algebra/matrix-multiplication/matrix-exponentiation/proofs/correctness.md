---
title: The left-to-right binary method computes A^k
proves: [correctness, termination]
status: full
---

Let $S$ be a semiring with a multiplicative unit (for example a ring), and let the matrix product over $S$ be associative, with identity $I_n$. For $q \ge 1$ write $A^q$ for the product of $q$ copies of $A$; by associativity, $A^{q} A^{r} = A^{q + r}$ for all $q, r \ge 1$, and $A^0 = I_n$.

**Claim.** For every $A \in S^{n \times n}$ and every integer $k \ge 0$, MATRIX-EXPONENTIATION$(A, k)$ stops and returns $A^k$. For $k \ge 1$ it makes exactly $\lfloor \lg k \rfloor + \nu(k) - 1$ matrix products, where $\nu(k)$ is the number of ones in the binary form of $k$.

**Case $k = 0$.** Line L1 returns $I_n = A^0$ and makes no product.

**Case $k \ge 1$.** Let $k = \sum_{i=0}^{t} b_i 2^i$ with $b_i \in \{0, 1\}$ and $b_t = 1$, so $t = \lfloor \lg k \rfloor$. For $-1 \le i \le t - 1$ let

$$q_i = \left\lfloor \frac{k}{2^{i+1}} \right\rfloor = \sum_{j=i+1}^{t} b_j 2^{j-i-1}.$$

Then $q_{t-1} = b_t = 1$, $q_{-1} = k$, and $q_{i-1} = 2 q_i + b_i$ for $0 \le i \le t - 1$, because shifting the digits $b_t \ldots b_{i+1}$ one place left and appending $b_i$ gives the digits $b_t \ldots b_i$.

*Invariant.* At the start of the iteration of line L4 with index $i$, $R = A^{q_i}$.

*Initialization.* Before the first iteration, $i = t - 1$ and line L3 set $R = A = A^{1} = A^{q_{t-1}}$.

*Maintenance.* Assume $R = A^{q_i}$ at the start of iteration $i$. Line L5 sets $R$ to $A^{q_i} A^{q_i} = A^{2 q_i}$. If $b_i = 1$, line L6 sets $R$ to $A^{2 q_i} A = A^{2 q_i + 1}$. In both cases $R = A^{2 q_i + b_i} = A^{q_{i-1}}$, which is the invariant for the next index $i - 1$.

*Termination.* The loop runs for $i = t - 1, t - 2, \ldots, 0$, that is $t$ iterations, and $i$ drops by exactly one each time, so it stops. After the last iteration ($i = 0$), the invariant for the index $-1$ gives $R = A^{q_{-1}} = A^k$, which line L7 returns. If $t = 0$ (so $k = 1$), the loop does not run and $R = A = A^1$.

*Count.* Line L5 runs once in each of the $t$ iterations. Line L6 makes a product exactly for the indices $i \le t - 1$ with $b_i = 1$; there are $\nu(k) - 1$ of them, since $b_t = 1$ is the only digit $1$ that the loop does not see. So the total is $t + \nu(k) - 1 = \lfloor \lg k \rfloor + \nu(k) - 1$. $\blacksquare$

**Remark.** Each product in lines L5 and L6 must be written to fresh storage. The proof treats $R \leftarrow R \cdot R$ as the assignment of the value $R \cdot R$, which needs the old $R$ until the product is complete.
