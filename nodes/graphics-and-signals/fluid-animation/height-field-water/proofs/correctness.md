---
title: The line solves, the volume and the energy of the height field step
proves: [correctness]
status: full
---

We use the notation of the page, with exact real arithmetic.
For one direction, $(A q)_k = \sum_l e_{kl}(q_k - q_l)$, where $l$ runs over the neighbors of $k$ in that direction, $e_{kl} = e_{lk} \ge 0$, and $e_{kl} = 0$ if $k$ or $l$ is dry.
Lines L3 and L4 solve $(I + A_x)z = r$ and $(I + A_y)h' = z$.
We write $\langle p, q\rangle = \sum_k p_k q_k$.

## The line solves

**Claim 1.** On each line, the matrix of $I + A$ is tridiagonal and strictly diagonally dominant, and the Thomas algorithm of the code computes its solution without a division by 0.

*Proof.*
Row $k$ has the diagonal $a_k = 1 + \sum_l e_{kl}$ and the entries $-e_{kl}$ for its at most two neighbors on the line, so $|a_k| = 1 + \sum_l e_{kl} > \sum_l e_{kl}$.
Write $b_k$ for the entry left of the diagonal and $c_k$ for the one right of it, so $|a_k| > |b_k| + |c_k|$.
The forward sweep computes $\gamma_0 = c_0/a_0$ and $\mu_k = a_k - b_k\gamma_{k-1}$, $\gamma_k = c_k/\mu_k$.
By induction $|\gamma_{k-1}| < 1$, so $|\mu_k| \ge |a_k| - |b_k| > |c_k| \ge 0$, so $\mu_k \ne 0$ and $|\gamma_k| < 1$.
The sweep is Gaussian elimination without pivoting: row $k$ minus $b_k/\mu_{k-1}$ times the reduced row $k-1$ removes the entry left of the diagonal and leaves the pivot $\mu_k$.
The back substitution then solves the upper bidiagonal system. $\square$

## Volume

**Claim 2.** $\sum_k (Aq)_k = 0$ for every $q$, so each of lines L3 and L4 keeps the sum of the values.

*Proof.*
Each unordered pair $\{k, l\}$ adds $e_{kl}(q_k - q_l)$ to row $k$ and $e_{lk}(q_l - q_k)$ to row $l$, and these cancel because $e_{kl} = e_{lk}$.
From $(I + A)z = r$, $\sum_k z_k = \sum_k r_k - \sum_k (Az)_k = \sum_k r_k$. $\square$

**Claim 3.** If $\sum_k h_k = \sum_k h^-_k = V$, then $\sum_k h'_k = V$, for any depths and any $\tau$. So the volume of every later step is $V\Delta x^2$.

*Proof.*
By line L1, $\sum_k r_k = V + (1 - \tau)(V - V) = V$.
By Claim 2 for lines L3 and L4, $\sum_k h'_k = V$.
The next step gets the pair $(h', h)$, which again has two equal sums, and induction gives the rest. $\square$

## Energy

**Claim 4.** Let every cell have the same depth $d > 0$, and let $\tau = 0$. Let $M = A_x + A_y + A_x A_y$ and $E(p, q) = |p - q|^2 + \frac12(\langle Mp, p\rangle + \langle Mq, q\rangle)$. Then $E(h', h) \le E(h, h^-)$, for any $\Delta t$.

*Proof.*
$\langle A q, q\rangle = \sum_{\{k, l\}} e_{kl}(q_k - q_l)^2 \ge 0$ and $A$ is symmetric, so $A_x$ and $A_y$ are symmetric positive semidefinite.
With one depth, $e_{kl} = 2sd$ for every pair, so $A_x = L_x\otimes I$ and $A_y = I\otimes L_y$ for the 1D matrices $L_x$ and $L_y$ of a line.
These commute, and $A_x A_y = L_x\otimes L_y$ is symmetric positive semidefinite, because the eigenvalues of a Kronecker product are the products of the eigenvalues.
So $M$ is symmetric positive semidefinite.
Lines L3 and L4 give $(I + A_x)(I + A_y)h' = r$, which is $(I + M)h' = 2h - h^-$, or

$$(h' - h) - (h - h^-) = -Mh'.$$

Take the inner product with $(h' - h) + (h - h^-) = h' - h^-$.
The left side is $|h' - h|^2 - |h - h^-|^2$.
For a symmetric $M$, $\langle Mh', h' - h^-\rangle = \frac12(\langle Mh', h'\rangle - \langle Mh^-, h^-\rangle) + \frac12\langle M(h' - h^-), h' - h^-\rangle$.
So

$$E(h', h) - E(h, h^-) = |h' - h|^2 - |h - h^-|^2 + \tfrac12\langle Mh', h'\rangle - \tfrac12\langle Mh^-, h^-\rangle = -\tfrac12\langle M(h' - h^-), h' - h^-\rangle \le 0. \qquad\square$$

$E$ bounds $|h' - h|^2$ and $\langle Mh, h\rangle$ for all steps, so the differences of neighbor heights and the change per step stay bounded for every $\Delta t$: this is the unconditional stability of the page.
The loss $\frac12\langle M(h' - h^-), h' - h^-\rangle$ is the damping of the implicit step; it is larger for larger $\Delta t$ and for short waves, where $M$ is large.
For a depth that varies, $A_x$ and $A_y$ do not commute in general, $M$ is not symmetric, and the proof does not apply.

## Rest

**Claim 5.** Let $h = h^-$, let $h$ have the same value on all wet cells of each connected wet region, and let the dry cells have any heights. Then $h' = h$.

*Proof.*
Then $r = h$.
For a dry cell, every $e_{kl}$ is 0, so its row is $z_k = r_k$.
For a wet cell, its neighbors with $e_{kl} > 0$ are wet and in the same region, so they have the same value of $r$, and $z = r$ satisfies the row.
By Claim 1 the system has one solution, so $z = r$, and in the same way $h' = z = h$. $\blacksquare$
