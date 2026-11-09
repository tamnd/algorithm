---
title: Sattolo's algorithm gives each n-cycle with probability 1/(n − 1)!
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. The calls of RANDOM are independent, and the call RANDOM$(0, i - 1)$ is uniform on $\{0, \ldots, i-1\}$. As on the [Fisher-Yates page](/fisher-yates-shuffle/), we follow positions: the output is the arrangement $\sigma$ when the item that started at position $\sigma(p)$ ends at position $p$, for each $p$. Let $C_n$ be the set of permutations of $\{0, \ldots, n-1\}$ that are one cycle of length $n$.

**Termination.** The loop of line L1 runs for $i = n-1, \ldots, 1$, so it makes exactly $\max(n-1, 0)$ iterations, each with one call of RANDOM and one swap. The range of the call has $i \ge 1$ values, so the call is defined.

**Counting $C_n$.** For $n \ge 1$, $|C_n| = (n-1)!$. Each $n$-cycle can be written in exactly one way as $(0\ x_1\ x_2\ \cdots\ x_{n-1})$, with 0 first, where $(x_1, \ldots, x_{n-1})$ is an order of $\{1, \ldots, n-1\}$. Each order gives a different cycle, and there are $(n-1)!$ orders.

**Theorem.** For $n \ge 1$ and each $\tau \in C_n$, $\Pr[\sigma = \tau] = 1/(n-1)!$. For each $\tau \notin C_n$, $\Pr[\sigma = \tau] = 0$.

## The output as a product of transpositions

Let $j_i$ be the value that line L2 returns in the iteration for $i$, so $0 \le j_i \le i - 1$. The run is fixed by the choice sequence $c = (j_{n-1}, \ldots, j_1)$. There are $(n-1)(n-2) \cdots 1 = (n-1)!$ choice sequences, and by independence each has probability $\prod_{i=1}^{n-1} \frac{1}{i} = \frac{1}{(n-1)!}$.

Let $t_i = (i\ j_i)$, the transposition of positions $i$ and $j_i$. Since $j_i \ne i$, each $t_i$ is a real transposition. If an array $C$ becomes $C'$ by the swap of positions $i$ and $j$, then $C'[p] = C[t(p)]$ with $t = (i\ j)$. The first swap is for $i = n - 1$, so by induction on the number of swaps,
$$\sigma = t_{n-1} \circ t_{n-2} \circ \cdots \circ t_1 .$$
Let $\rho = t_{n-2} \circ \cdots \circ t_1$. Each of these transpositions moves only positions in $\{0, \ldots, n-2\}$, so $\rho$ fixes $n - 1$. On $\{0, \ldots, n-2\}$, $\rho$ is the output permutation of the same algorithm on $n - 1$ positions with the choices $(j_{n-2}, \ldots, j_1)$.

## Step 1: each output is an n-cycle

We use induction on $n$. For $n = 1$ the loop does not run, and $\sigma$ is the identity on $\{0\}$, which is the one cycle of length 1.

Let $n \ge 2$, and let $j = j_{n-1} \le n - 2$. By the induction hypothesis, $\rho$ restricted to $\{0, \ldots, n-2\}$ is one cycle of length $n - 1$. Let $x$ be the position with $\rho(x) = j$. Then $\sigma = t_{n-1} \circ \rho$ acts as follows.

- $\sigma(n-1) = t_{n-1}(\rho(n-1)) = t_{n-1}(n-1) = j$.
- $\sigma(x) = t_{n-1}(j) = n - 1$.
- For each other $y \le n - 2$, $\rho(y) \ne j$ and $\rho(y) \ne n - 1$, so $\sigma(y) = t_{n-1}(\rho(y)) = \rho(y)$.

So $\sigma$ is the cycle of $\rho$ with the arrow $x \to j$ replaced by the two arrows $x \to n-1 \to j$. That is, $n - 1$ is inserted into the cycle just before $j$. The result is one cycle that contains all $n$ positions, so $\sigma \in C_n$. (For $n = 2$: $\rho$ is the identity on $\{0\}$, $x = j = 0$, and $\sigma = (0\ 1)$.)

## Step 2: different choices give different cycles

We use induction on $n$. For $n = 1$ there is one choice sequence, the empty one. Let $n \ge 2$. From Step 1, $\sigma(n-1) = j_{n-1}$, so $\sigma$ determines $j_{n-1}$ and $t_{n-1}$. A transposition is its own inverse, so $\rho = t_{n-1} \circ \sigma$ is also determined. On $\{0, \ldots, n-2\}$, $\rho$ is the output of the algorithm on $n - 1$ positions with the choices $(j_{n-2}, \ldots, j_1)$, and by the induction hypothesis these choices are determined by $\rho$. So $\sigma$ determines the whole choice sequence.

## Conclusion

The map $c \mapsto \sigma$ goes from the $(n-1)!$ choice sequences into $C_n$ (Step 1), and it is one to one (Step 2). Since $|C_n| = (n-1)!$, it is a bijection onto $C_n$. Each $\tau \in C_n$ comes from exactly one choice sequence, which has probability $1/(n-1)!$. No permutation outside $C_n$ is an output. $\blacksquare$

**A direct inverse.** The proof also gives the inverse map. Given $\tau \in C_n$ with $n \ge 2$, set $j_{n-1} = \tau(n-1)$. Remove $n - 1$ from the cycle: replace the arrows $x \to n-1 \to j_{n-1}$ by the arrow $x \to j_{n-1}$. The result is an $(n-1)$-cycle on $\{0, \ldots, n-2\}$, and the rest of the choices come from it in the same way. In the example of the page, $\tau = (0\ 3\ 1\ 5\ 2\ 4)$ gives $j_5 = \tau(5) = 2$. Removing 5 gives $(0\ 3\ 1\ 2\ 4)$, so $j_4 = 0$; removing 4 gives $(0\ 3\ 1\ 2)$, so $j_3 = 1$; removing 3 gives $(0\ 1\ 2)$, so $j_2 = 0$; removing 2 gives $(0\ 1)$, so $j_1 = 0$. These are the choices $2, 0, 1, 0, 0$ of the trace.

**Why Fisher-Yates and Sattolo differ only in one range.** In Fisher-Yates, $j_i = i$ is allowed, and then $t_i$ is the identity, and $i$ becomes a fixed point, a cycle of its own. The insertion step above then either inserts $n-1$ into an existing cycle (if $j < n-1$) or starts a new cycle (if $j = n-1$). Sattolo forbids the second case at each step, so all positions end in one cycle.
