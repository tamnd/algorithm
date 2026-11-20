---
title: The diamond difference sweep solves each direction, the converged S_N solution balances, the discrete solution is unique, and the spatial error is second order
proves: [correctness]
status: full
---

We assume exact arithmetic. The slab, the cross sections and the lines L1 to L10 are those of the page. Every cell has $\Sigma_{t,j} > 0$, $0 \le \Sigma_{s,j} \le \Sigma_{t,j}$ and $\Delta x_j > 0$. The directions $\mu_n$ and the weights $w_n$ are the $N$-point Gauss-Legendre rule with $N$ even, so every $\mu_n \ne 0$, the weights are positive and sum to 2, and the rule is symmetric: if $\mu_n$ is a node, then $-\mu_n$ is a node with the same weight ([Gauss-Legendre quadrature](/gauss-legendre-quadrature/)).

For one direction $n$ and one cell $j$, write $\psi_a$ for the incoming face value, $\psi_b$ for the outgoing face value and $\psi_c$ for the cell value. With $\tau = \Sigma_{t,j}\Delta x_j/|\mu_n|$ (the optical thickness of the cell along the direction) and the cell source $S_j$, the diamond difference equations of the cell are
$$|\mu_n|\,\frac{\psi_b - \psi_a}{\Delta x_j} + \Sigma_{t,j}\,\psi_c = S_j, \qquad \psi_c = \frac{\psi_a + \psi_b}{2}. \tag{1}$$
The first equation is the balance of the cell, and the second is the diamond relation.

**Lemma 1 (one cell).** For every $\psi_a$ and $S_j$, the equations (1) have exactly one solution, and it is the one of line L7:
$$\psi_c = \frac{S_j + (2|\mu_n|/\Delta x_j)\,\psi_a}{\Sigma_{t,j} + 2|\mu_n|/\Delta x_j}, \qquad \psi_b = 2\psi_c - \psi_a.$$

*Proof.* The diamond relation gives $\psi_b = 2\psi_c - \psi_a$. Put this into the balance: $|\mu_n|(2\psi_c - 2\psi_a)/\Delta x_j + \Sigma_{t,j}\psi_c = S_j$, that is $(\Sigma_{t,j} + 2|\mu_n|/\Delta x_j)\,\psi_c = S_j + (2|\mu_n|/\Delta x_j)\,\psi_a$. The factor on the left is positive, so $\psi_c$ is unique and equals the formula. Then $\psi_b$ is fixed by the diamond relation. Both equations hold by construction. $\square$

**Lemma 2 (one sweep).** Fix the sources $S_j$ and the incoming value at the face where direction $n$ enters. Lines L5 to L8 compute the unique solution of the equations (1) of direction $n$ in all cells, with the outgoing value of each cell equal to the incoming value of the next cell downstream.

*Proof.* Take $\mu_n > 0$; the case $\mu_n < 0$ is the mirror image, with the cells in the order $M, \ldots, 1$. We use induction on the cell index. Cell 1 has the incoming value of the boundary, so by Lemma 1 its equations have one solution, and line L7 computes it. If cells $1, \ldots, j - 1$ are solved, the incoming value of cell $j$ is the outgoing value of cell $j - 1$, which is now known, and Lemma 1 again gives the one solution. The equations of cell $j$ contain no unknown of a cell downstream, so the order of line L7 solves them all. $\square$

So one iteration of lines L4 to L9 is $\phi \mapsto T\phi + b$: it sweeps all directions with the source $(\Sigma_s \phi + q)/2$ of the last iterate and integrates with the weights. The map is affine in $\phi$, and its linear part $T$ is the sweep of the source $\Sigma_s\phi/2$ with zero incoming values.

**Theorem 3 (balance at the fixed point).** Let $\phi$ be a fixed point of the iteration, $\phi = T\phi + b$, with incoming face values given (vacuum or data). Let $J^{\mathrm{in}}$ be the incoming partial current $\sum_{\mu_n > 0} w_n \mu_n \psi_n(0) + \sum_{\mu_n < 0} w_n |\mu_n| \psi_n(L)$ and $J^{\mathrm{out}}$ the outgoing one, with the outgoing face values. Then
$$\sum_{j=1}^{M} (\Sigma_{t,j} - \Sigma_{s,j})\,\phi_j\,\Delta x_j + J^{\mathrm{out}} = \sum_{j=1}^{M} q_j\,\Delta x_j + J^{\mathrm{in}}.$$

*Proof.* Multiply the balance in (1) for direction $n$ and cell $j$ by $w_n \Delta x_j$ and sum over $n$. The source is the same for all directions, and $\sum_n w_n = 2$, so the right side is $2 S_j \Delta x_j = (\Sigma_{s,j}\phi_j + q_j)\Delta x_j$. The collision term gives $\Sigma_{t,j}\Delta x_j \sum_n w_n \psi_{n,j} = \Sigma_{t,j}\phi_j\Delta x_j$ by line L9, because at the fixed point the $\phi$ of line L9 is the $\phi$ of line L4. The streaming term is $\sum_n w_n |\mu_n|(\psi_{n,\mathrm{out}} - \psi_{n,\mathrm{in}})$ for cell $j$. Now sum over $j$. For a direction with $\mu_n > 0$, the outgoing value of cell $j$ is the incoming value of cell $j + 1$ (Lemma 2), so the sum over $j$ telescopes to $|\mu_n|(\psi_n(L) - \psi_n(0))$. For $\mu_n < 0$ it telescopes to $|\mu_n|(\psi_n(0) - \psi_n(L))$. The sum of these over $n$ with the weights is $J^{\mathrm{out}} - J^{\mathrm{in}}$. Move $\Sigma_s\phi$ to the left. $\square$

At a reflecting face, the incoming current equals the outgoing one at the fixed point, because the rule is symmetric and the mirror direction has the same weight and the same $|\mu|$, so the two terms of that face cancel. The page checks the balance with the leakages that the implementation returns.

**Theorem 4 (existence, uniqueness and convergence).** Let $c = \max_j \Sigma_{s,j}/\Sigma_{t,j} < 1$, and let the incoming face values be given (vacuum or data, not reflecting). Then the discrete $S_N$ equations have exactly one solution, and the iteration of lines L3 to L10 converges to it from every start, with
$$\|\phi^{(l)} - \phi\|_t \le c^{\,l}\, \|\phi^{(0)} - \phi\|_t, \qquad \|v\|_t^2 = \sum_{j} \Sigma_{t,j}\, v_j^2\, \Delta x_j .$$

*Proof.* It is enough to show $\|Tv\|_t \le c\|v\|_t$ for every vector $v$. Then $T$ is a contraction in this norm, the map $\phi \mapsto T\phi + b$ has exactly one fixed point by the contraction mapping theorem ([fixed-point iteration](/fixed-point-iteration/)), and the error of iterate $l$ is $T^l$ applied to the first error.

Fix $v$ and one direction $n$, and let $\psi$ be its sweep with the source $S_j = \Sigma_{s,j} v_j/2$ and zero incoming value. Multiply the balance in (1) by $\psi_c\,\Delta x_j$. With the diamond relation, $|\mu_n|(\psi_b - \psi_a)\psi_c = |\mu_n|(\psi_b^2 - \psi_a^2)/2$. The sum over the cells telescopes as in Theorem 3:
$$\frac{|\mu_n|}{2}\,\psi_{\mathrm{out}}^2 + \sum_j \Sigma_{t,j}\,\psi_{c,j}^2\,\Delta x_j = \sum_j S_j\,\psi_{c,j}\,\Delta x_j,$$
where $\psi_{\mathrm{out}}$ is the value that leaves the slab and the incoming value is 0. The first term is not negative. Write the right side as $\sum_j (S_j/\Sigma_{t,j})\,\psi_{c,j}\,\Sigma_{t,j}\Delta x_j$ and use the Cauchy-Schwarz inequality in the weighted inner product:
$$\|\psi_c\|_t^2 \le \|S/\Sigma_t\|_t\, \|\psi_c\|_t, \quad\text{so}\quad \|\psi_c\|_t \le \|S/\Sigma_t\|_t \le \frac{c}{2}\,\|v\|_t,$$
because $S_j/\Sigma_{t,j} = (\Sigma_{s,j}/\Sigma_{t,j})\, v_j/2$ and $\Sigma_{s,j}/\Sigma_{t,j} \le c$. Line L9 forms $Tv = \sum_n w_n \psi_{c}^{(n)}$, so by the triangle inequality $\|Tv\|_t \le \sum_n w_n (c/2)\|v\|_t = c\,\|v\|_t$, since the weights are positive and sum to 2. $\square$

The proof does not need the cell values to be positive, so it holds for diamond difference, which can give negative values (Theorem 6). The [source iteration](/source-iteration/) page shows that the factor $c$ is sharp in thick media and gives the Fourier analysis of the rate.

**Theorem 5 (second order in space along a direction).** Take a pure absorber with $\Sigma_t$ constant, no source, $M$ equal cells on $[0, L]$, a direction $\mu \ne 0$ and the incoming value 1. Let $\tau = \Sigma_t L/(|\mu| M)$ be the optical thickness of one cell along the direction. The exact transmitted value is $e^{-\Sigma_t L/|\mu|}$, and the diamond difference value $\psi_{\mathrm{out}}$ satisfies
$$|\psi_{\mathrm{out}} - e^{-\Sigma_t L/|\mu|}| \le \frac{(\Sigma_t L/|\mu|)^3}{12\, M^2},$$
and $\psi_{\mathrm{out}} \le e^{-\Sigma_t L/|\mu|}$ when $\tau \le 2$.

*Proof.* With $S = 0$, Lemma 1 gives $\psi_b = r(\tau)\,\psi_a$ with $r(\tau) = (2 - \tau)/(2 + \tau)$, so $\psi_{\mathrm{out}} = r(\tau)^M$. Let $f(\tau) = (2 + \tau)e^{-\tau} - (2 - \tau)$. Then $f(0) = 0$, $f'(\tau) = 1 - (1 + \tau)e^{-\tau}$ with $f'(0) = 0$, and $f''(\tau) = \tau e^{-\tau}$. By Taylor's formula with the integral remainder, $f(\tau) = \int_0^\tau (\tau - s)\, s e^{-s}\, ds$, so $0 \le f(\tau) \le \int_0^\tau (\tau - s)\, s\, ds = \tau^3/6$. Since $e^{-\tau} - r(\tau) = f(\tau)/(2 + \tau)$,
$$0 \le e^{-\tau} - r(\tau) \le \frac{\tau^3}{6(2 + \tau)} \le \frac{\tau^3}{12}.$$
Both $e^{-\tau}$ and $r(\tau)$ lie in $[-1, 1]$ for $\tau \ge 0$. For numbers $a, b$ in $[-1, 1]$, $a^M - b^M = (a - b)\sum_{i=0}^{M-1} a^i b^{M-1-i}$, so $|a^M - b^M| \le M|a - b|$. With $a = e^{-\tau}$ and $b = r(\tau)$ this gives $|e^{-M\tau} - r(\tau)^M| \le M\tau^3/12 = (\Sigma_t L/|\mu|)^3/(12M^2)$. If $\tau \le 2$, then $0 \le r(\tau) \le e^{-\tau}$, so $r(\tau)^M \le e^{-M\tau}$. $\square$

For a smooth problem with scattering, the same local error of order $\tau^3$ per cell gives a global error of order $\Delta x^2$; the page measures this order on a scattering slab and does not prove it in general.

**Theorem 6 (negative values).** In a pure absorber cell with $S_j = 0$ and $\psi_a > 0$, the outgoing value $\psi_b$ is negative if and only if $\tau > 2$, that is $\Sigma_{t,j}\Delta x_j > 2|\mu_n|$.

*Proof.* By Lemma 1, $\psi_b = r(\tau)\psi_a$ with $r(\tau) = (2 - \tau)/(2 + \tau)$, and $r(\tau) < 0$ exactly when $\tau > 2$. $\square$

The cell value $\psi_c = \psi_a/(1 + \tau/2)$ stays positive. The negative face value enters the next cell, and there it can make the cell value negative too.
