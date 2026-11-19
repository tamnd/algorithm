---
title: The MRT collision conserves mass and momentum, and equal rates give BGK
proves: [correctness]
status: full
---

We use the D2Q9 velocities $c_0 = (0,0)$, $c_1 = (1,0)$, $c_2 = (0,1)$, $c_3 = (-1,0)$, $c_4 = (0,-1)$, $c_5 = (1,1)$, $c_6 = (-1,1)$, $c_7 = (-1,-1)$, $c_8 = (1,-1)$ and the weights $w_0 = \frac49$, $w_{1..4} = \frac19$, $w_{5..8} = \frac1{36}$. The rows of $M$ are, in order, $\rho$, $e$, $\epsilon$, $j_x$, $q_x$, $j_y$, $q_y$, $p_{xx}$ and $p_{xy}$, as in the implementation. We claim four things, all in exact arithmetic:

1. $M$ is invertible and $M^{-1} = M^T D^{-1}$ with $D = \mathrm{diag}(9, 36, 36, 6, 12, 6, 12, 4, 4)$.
2. $M f^{\mathrm{eq}}(\rho, u) = m^{\mathrm{eq}}(\rho, u)$, the closed form used on line L5.
3. Lines L3 to L6 keep the density of a node and add exactly $g$ to its momentum $\sum_i c_i f_i$, whatever the rates of the conserved moments are. If every rate equals $1/\tau$, lines L3 to L6 give the same $f^*$ as BGK collision with Guo forcing.
4. Line L7 keeps the total mass. On a lattice that is periodic in both directions, it also keeps the total momentum. So the total mass is constant over a run, and on a periodic lattice the total momentum grows by exactly $n_x n_y g$ per step.

**Claim 1.** Each row of $M$ has integer entries, and a direct computation of the 36 products of pairs of distinct rows gives 0 (the test `test_rows_of_m_are_orthogonal` does all 81 products). For example, the rows $e = (-4,-1,-1,-1,-1,2,2,2,2)$ and $\epsilon = (4,-2,-2,-2,-2,1,1,1,1)$ give $-16 + 4 \cdot 2 + 4 \cdot 2 = 0$. The squared lengths of the rows are the entries of $D$. So $M M^T = D$, and $M^{-1} = M^T D^{-1}$.

**Claim 2.** Write $f_i^{\mathrm{eq}} = w_i \rho (1 + 3 c_i \cdot u + \frac92 (c_i \cdot u)^2 - \frac32 |u|^2)$. Over the four axis velocities, $\sum (c_i \cdot u) = 0$ and $\sum (c_i \cdot u)^2 = 2|u|^2$; over the four diagonal velocities, $\sum (c_i \cdot u) = 0$ and $\sum (c_i \cdot u)^2 = 4|u|^2$. So the rest, axis and diagonal sums are

$$f_0^{\mathrm{eq}} = \tfrac49 \rho (1 - \tfrac32 |u|^2), \qquad A = \sum_{i=1}^4 f_i^{\mathrm{eq}} = \tfrac19 \rho (4 + 3|u|^2), \qquad B = \sum_{i=5}^8 f_i^{\mathrm{eq}} = \tfrac19 \rho (1 + 3|u|^2).$$

The rows $\rho$, $e$ and $\epsilon$ take the values $(1,1,1)$, $(-4,-1,2)$ and $(4,-2,1)$ on the rest, axis and diagonal groups. Hence $\rho$-row: $f_0 + A + B = \rho$; $e = -4 f_0 - A + 2B = \rho(-\frac{16}9 - \frac49 + \frac29) + \rho|u|^2 (\frac{24}9 - \frac39 + \frac69) = -2\rho + 3\rho|u|^2$; $\epsilon = 4 f_0 - 2A + B = \rho(\frac{16}9 - \frac89 + \frac19) - \rho|u|^2(\frac{24}9 + \frac69 - \frac39) = \rho - 3\rho|u|^2$.

For the odd rows only the term $3 c_i \cdot u$ survives, because the even terms are equal for $c_i$ and $-c_i$. The axis part is $f_1 - f_3 = \frac19 \rho \cdot 6 u_x = \frac23 \rho u_x$, and the diagonal part is $f_5 - f_6 - f_7 + f_8 = \frac1{36} \rho \cdot 3 \cdot 4 u_x = \frac13 \rho u_x$. So $j_x = \frac23 \rho u_x + \frac13 \rho u_x = \rho u_x$ and $q_x = -2 \cdot \frac23 \rho u_x + \frac13 \rho u_x = -\rho u_x$. The $y$ rows follow by symmetry. For the stress rows only the term $\frac92 (c_i \cdot u)^2$ survives: $p_{xx} = f_1 - f_2 + f_3 - f_4 = \frac19 \rho \cdot \frac92 (2u_x^2 - 2u_y^2) = \rho(u_x^2 - u_y^2)$, and $p_{xy} = f_5 - f_6 + f_7 - f_8 = \frac1{36}\rho \cdot \frac92 \bigl(2(u_x+u_y)^2 - 2(u_x-u_y)^2\bigr) = \rho u_x u_y$. This is the closed form $m^{\mathrm{eq}} = (\rho, -2\rho + 3\rho|u|^2, \rho - 3\rho|u|^2, \rho u_x, -\rho u_x, \rho u_y, -\rho u_y, \rho(u_x^2 - u_y^2), \rho u_x u_y)$.

**Claim 3.** Let $F_i = w_i \bigl(3(c_i - u) + 9 (c_i \cdot u) c_i\bigr) \cdot g$. The lattice sums $\sum w_i = 1$, $\sum w_i c_i = 0$, $\sum w_i c_{i\alpha} c_{i\beta} = \frac13 \delta_{\alpha\beta}$ and $\sum w_i c_{i\alpha} c_{i\beta} c_{i\gamma} = 0$ give $\sum_i F_i = -3 u \cdot g + 9 \cdot \frac13 u \cdot g = 0$ and $\sum_i c_{i\alpha} F_i = 3 \cdot \frac13 g_\alpha = g_\alpha$. So the $\rho$, $j_x$ and $j_y$ entries of $M F$ are $0$, $g_x$ and $g_y$.

Line L3 sets $\rho = m_0$ and $\rho u = j + \frac12 g$, where $j = (m_3, m_5)$. By Claim 2, $m_0^{\mathrm{eq}} = \rho = m_0$ and $(m_3^{\mathrm{eq}}, m_5^{\mathrm{eq}}) = \rho u = j + \frac12 g$. With any rate $s$ on the $j_x$ row, line L5 gives

$$m_3^* = m_3 - s\bigl(m_3 - m_3 - \tfrac12 g_x\bigr) + \bigl(1 - \tfrac s2\bigr) g_x = m_3 + g_x,$$

and in the same way $m_5^* = m_5 + g_y$ and $m_0^* = m_0$ for any rate on the $\rho$ row. Line L6 inverts $M$ exactly by Claim 1, so $\sum_i f_i^* = m_0$ and $\sum_i c_i f_i^* = j + g$.

If $S = \frac1\tau I$, line L5 reads $m^* = (1 - \frac1\tau) M f + \frac1\tau m^{\mathrm{eq}} + (1 - \frac1{2\tau}) M F$. By Claim 2, $m^{\mathrm{eq}} = M f^{\mathrm{eq}}$, so line L6 gives $f^* = M^{-1} m^* = f - \frac1\tau (f - f^{\mathrm{eq}}) + (1 - \frac1{2\tau}) F$, which is BGK collision with Guo forcing, term by term.

**Claim 4.** Line L7 moves the value $f_i^*(x)$ into one slot of the new array: slot $(x + c_i, i)$ if $x + c_i$ is inside the lattice (with $x$ taken modulo $n_x$, and $y$ modulo $n_y$ when there are no walls), else slot $(x, \bar\imath)$ with $c_{\bar\imath} = -c_i$. We show that this map from old slots to new slots is a bijection. Take a new slot $(z, k)$. If $z - c_k$ is inside, the only old slot that maps to it is $(z - c_k, k)$, because a bounced value at $z$ would need $z + c_{\bar k} = z - c_k$ to lie beyond a wall. If $z - c_k$ lies beyond a wall, then $(z - c_k, k)$ does not exist, and the only old slot that maps to $(z, k)$ is $(z, \bar k)$, whose target $z + c_{\bar k} = z - c_k$ is beyond the wall. So every new slot gets exactly one value, and streaming permutes the values. The total mass $\sum_{x,i} f_i(x)$ is therefore the same before and after line L7. Without walls the permutation keeps the index $i$ of every value, so $\sum_{x,i} c_i f_i(x)$ is also kept.

Together with Claim 3, each step keeps the total mass exactly, and on a fully periodic lattice each step adds $g$ at each of the $n_x n_y$ nodes and nothing else to the total momentum. The walls take momentum out (they exert the wall shear force), so with walls only the mass is conserved.

These are exact statements about the update. The claim that the scheme approximates the Navier-Stokes equations with $\nu = \frac13(\frac1{s_\nu} - \frac12)$ is a consistency result from the Chapman-Enskog expansion (Lallemand and Luo 2000), not part of this proof. $\blacksquare$
