---
title: Batch modular inverse returns every inverse, or a divisor of m when one does not exist
proves: [correctness]
status: full
---

**Claim.** Let $m \ge 1$ and let $x_1, \ldots, x_k$ be residues modulo $m$, with $k \ge 0$. If every $x_i$ is a unit modulo $m$, the algorithm returns $y_1, \ldots, y_k$ with $x_i y_i \equiv 1 \pmod m$ for each $i$, and it uses $3(k - 1)$ modular multiplications and one inversion for $k \ge 1$. If some $x_i$ is not a unit, line L6 stops with $g = \gcd(z_k, m) > 1$, a divisor of $m$.

**The empty case.** For $k = 0$, line L1 returns the empty list, which is correct.

**Forward pass.** Lines L2 to L4 set $z_1 = x_1$ and $z_i = z_{i-1} x_i \bmod m$. By induction on $i$, $z_i \equiv x_1 x_2 \cdots x_i \pmod m$ for $1 \le i \le k$. This uses $k - 1$ multiplications.

**When the product is invertible.** A product of units is a unit, and conversely, if $z_k$ is a unit with inverse $w$, then for each $i$
$$x_i \cdot \Big(w \prod_{j \ne i} x_j\Big) \equiv z_k w \equiv 1 \pmod m,$$
so $x_i$ is a unit. Hence $\gcd(z_k, m) = 1$ if and only if every $x_i$ is a unit modulo $m$. Line L5 computes $g = \gcd(z_k, m)$ and, when $g = 1$, $q \equiv z_k^{-1} \pmod m$ by the extended Euclidean algorithm. If some $x_i$ is not a unit, then $g > 1$ and $g \mid m$, and line L6 stops as claimed. From now on, every $x_i$ is a unit.

**Backward pass.** We show that at the start of the iteration of line L7 with index $i$, for $i = k, k - 1, \ldots, 2$, the invariant $q \equiv z_i^{-1} \pmod m$ holds.

- *Start.* For $i = k$, it holds by line L5.
- *Step.* Assume $q \equiv z_i^{-1}$ at the start of the iteration for $i$. Line L8 sets
$$y_i = q z_{i-1} \equiv \frac{x_1 \cdots x_{i-1}}{x_1 \cdots x_i} = x_i^{-1} \pmod m,$$
which is the correct output for position $i$. Line L8 reads $z_{i-1}$, which has not been overwritten yet, because the loop writes only positions $i, i+1, \ldots, k$ before it reaches index $i - 1$. Line L9 sets $q \leftarrow q x_i \equiv z_i^{-1} x_i \equiv z_{i-1}^{-1}$, which is the invariant for $i - 1$.

After the last iteration, $i = 2$, the invariant gives $q \equiv z_1^{-1} = x_1^{-1}$, and line L10 sets $y_1 = q$. If $k = 1$, the loop does not run and $q \equiv z_1^{-1} = x_1^{-1}$ directly by line L5. So every $y_i$ is the inverse of $x_i$. The backward pass makes two multiplications per iteration, $2(k - 1)$ in total.

**Count.** The two passes use $(k - 1) + 2(k - 1) = 3(k - 1)$ modular multiplications, and line L5 is the only inversion. $\blacksquare$
