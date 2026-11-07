---
title: Russian peasant multiplication computes the exact product
proves: [correctness, termination]
status: full
---

Let $x_0 \ge 0$ and $y_0 \ge 0$ be integers, the inputs of PEASANT-MUL.

**Theorem.** PEASANT-MUL$(x_0, y_0)$ terminates after exactly $N$ rounds of the loop of line L2, where $N = 0$ if $y_0 = 0$ and $N = \lfloor \log_2 y_0 \rfloor + 1$ otherwise, and it returns $x_0 y_0$.

*Proof.* Write $x_r, y_r, p_r$ for the values of $x, y, p$ after $r$ rounds, so $x_0, y_0$ are the inputs and $p_0 = 0$ by line L1. One round gives $p_{r+1} = p_r + (y_r \bmod 2)\, x_r$ (line L3), $x_{r+1} = 2x_r$ (line L4) and $y_{r+1} = \lfloor y_r / 2 \rfloor$ (line L5).

*Invariant.* We show $p_r + x_r y_r = x_0 y_0$ for every $r$ for which round $r$ is reached. For $r = 0$ this is $0 + x_0 y_0 = x_0 y_0$. Assume it for $r$, and that $y_r > 0$, so round $r + 1$ runs. Division with remainder by 2 gives $y_r = 2\lfloor y_r/2 \rfloor + (y_r \bmod 2) = 2 y_{r+1} + (y_r \bmod 2)$. Hence

$$p_{r+1} + x_{r+1} y_{r+1} = p_r + (y_r \bmod 2)\, x_r + 2 x_r y_{r+1} = p_r + x_r \big( 2 y_{r+1} + (y_r \bmod 2) \big) = p_r + x_r y_r = x_0 y_0 .$$

*Termination.* By induction, $y_r = \lfloor y_0 / 2^r \rfloor$, since $\lfloor \lfloor u / 2^r \rfloor / 2 \rfloor = \lfloor u / 2^{r+1} \rfloor$ for integers $u \ge 0$. If $y_0 = 0$ the loop does not run, and $N = 0$. If $y_0 \ge 1$, then $2^{N-1} \le y_0 < 2^N$, so $y_r \ge 1$ for $r \le N - 1$ and $y_N = 0$. The loop therefore runs exactly $N$ rounds and stops.

*Result.* When the loop stops, $y_N = 0$, and the invariant gives $p_N = x_0 y_0 - x_N \cdot 0 = x_0 y_0$, which line L6 returns. All values stay nonnegative integers, since $p$ only grows by nonnegative terms, $x$ is doubled and $y$ is halved with the floor.

*Limb arrays.* In the implementation on limb arrays in radix $\beta = 2^w$, the parity of $y$ is the lowest bit of its lowest limb, since $\beta$ is even; the doubling shifts each limb left by one bit and carries its top bit into the next limb, which computes $2x$ exactly because $2\sum_i x_i \beta^i = \sum_i (2x_i \bmod \beta)\beta^i + \sum_i \lfloor 2x_i/\beta \rfloor \beta^{i+1}$ with $\lfloor 2x_i / \beta \rfloor \in \{0, 1\}$; the halving is the reverse, $\lfloor y/2 \rfloor = \sum_i \big( \lfloor y_i / 2 \rfloor + (y_{i+1} \bmod 2)\,\beta/2 \big)\beta^i$; and line L3 uses an exact multiprecision addition. So each line computes the value the argument above uses. $\blacksquare$
