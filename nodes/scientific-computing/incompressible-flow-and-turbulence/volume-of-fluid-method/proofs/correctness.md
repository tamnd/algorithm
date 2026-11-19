---
title: The donor-acceptor VOF update conserves volume, keeps 0 <= F <= 1, and moves a band exactly
proves: [correctness]
status: full
---

We use the notation of the page. The grid has $N \times N$ cells of side $\Delta x = 1/N$ and is periodic. A sweep in the $x$ direction treats each row of cells on its own; in row $j$ the face velocity is the constant $w = u(y_j)$, and the Courant number of the sweep is $c = |w|\Delta t/\Delta x$. The $y$ sweep is the same with the roles of the indices exchanged. For a face with donor fraction $f_D$, acceptor fraction $f_A$ and chosen fraction $f_{AD} \in \{f_A, f_D\}$, line L6 gives the flux

$$q = \min\bigl(f_{AD}c + \max((1 - f_{AD})c - (1 - f_D), 0),\ f_D\bigr),$$

measured as a fraction of the cell volume. We claim, in exact arithmetic, for $0 \le c \le 1$ and fractions in $[0, 1]$:

1. $\max(0, c - (1 - f_D)) \le q \le \min(c, f_D)$.
2. A sweep keeps the sum of the fractions, and if all fractions are in $[0, 1]$ before the sweep, they are in $[0, 1]$ after it. So a run of `vof_advect` conserves the total volume $\Delta x^2\sum F$ exactly and keeps $0 \le F \le 1$.
3. If the fluid is a band $x_0 < x < x_1$ (all $y$) and both the band and the gap have width at least $2\Delta x$, then an $x$ sweep with constant velocity gives the exact volume fractions of the band moved by $w\Delta t$.

**Claim 1.** Write $C = \max((1 - f_{AD})c - (1 - f_D), 0)$ and $P = f_{AD}c + C$, so $q = \min(P, f_D)$.

Upper bound. Clearly $q \le f_D$. Also $C \le (1 - f_{AD})c$, because $(1 - f_{AD})c \ge 0$ and $1 - f_D \ge 0$. So $P \le f_{AD}c + (1 - f_{AD})c = c$, and $q \le c$.

Lower bound. $P \ge 0$ and $f_D \ge 0$, so $q \ge 0$. For the other bound we need $P \ge c - (1 - f_D)$ and $f_D \ge c - (1 - f_D)$. The first holds because $P \ge f_{AD}c + (1 - f_{AD})c - (1 - f_D) = c - (1 - f_D)$. The second is $c \le 1$, the Courant condition. So $q \ge \max(0, c - (1 - f_D))$.

The claim says that the donor gives at most the fluid it holds, $q \le f_D$, and at most the void it holds, $c - q \le 1 - f_D$, where $c$ is the total volume that crosses the face.

**Claim 2.** In a row, $w$ is the same at every face, so every face of the row has the same Courant number $c$ and the same direction. Each cell is the donor for exactly one face (its downstream face) and the acceptor for exactly one face (its upstream face). Line L7 subtracts each flux from its donor and adds it to its acceptor, so the sum over the row does not change, and the sum over the grid does not change. For cell $i$, the new value is $F'_i = F_i - q_{\text{out}} + q_{\text{in}}$. By Claim 1 applied to both faces, $q_{\text{out}} \le F_i$ and $q_{\text{in}} \ge 0$, so $F'_i \ge 0$. Also $q_{\text{out}} \ge c - (1 - F_i)$ and $q_{\text{in}} \le c$, so $F'_i \le F_i - c + 1 - F_i + c = 1$. Both fluxes are computed from the values before the sweep, so the bounds hold for all cells at once. The claim for a run follows by induction over the sweeps. A $y$ sweep with $v = v(x)$ is the same argument with columns in place of rows. This is where the restriction $u = u(y)$, $v = v(x)$ is used: if the velocity changed along a row, a cell could receive more than it gives and the bound $F' \le 1$ could fail.

**Claim 3.** Take $w > 0$; the case $w < 0$ is the mirror image. In the row, the fractions depend only on $i$, so $\partial F/\partial y = 0$ and line L5 picks $f_{AD} = f_A$ for every face. Each cell $[a, a + \Delta x]$ is one of four kinds, and in each case we compare $q$ with the exact flux, which is the volume of fluid in $[a + \Delta x - c\Delta x, a + \Delta x]$, the part of the cell that crosses the face in time $\Delta t$.

- Empty donor, $f_D = 0$: then $q = \min(\cdot, 0) = 0$, which is exact.
- Full donor, $f_D = 1$: $C = \max((1 - f_A)c, 0)$, so $P = c$ and $q = \min(c, 1) = c$, which is exact.
- Donor that contains the front edge $x_1$: the fluid fills $[a, a + f_D\Delta x]$. The gap is at least $2\Delta x$ wide, so the acceptor is empty, $f_{AD} = 0$, $C = \max(c - 1 + f_D, 0)$, and $q = \min(\max(c - 1 + f_D, 0), f_D) = \max(c - 1 + f_D, 0)$, since $c \le 1$. The exact flux is the length of the part of $[a, a + f_D\Delta x]$ that lies beyond $a + \Delta x - c\Delta x$, divided by $\Delta x$, which is $\max(f_D - (1 - c), 0)$. They agree.
- Donor that contains the back edge $x_0$: the fluid fills $[a + (1 - f_D)\Delta x, a + \Delta x]$. The band is at least $2\Delta x$ wide, so the acceptor is full, $f_{AD} = 1$, $C = 0$, and $q = \min(c, f_D)$. The exact flux is $\min(c, f_D)$. They agree.

(If an edge falls exactly on a face, the cells on both sides are full or empty and the first two cases apply.) So every flux equals the exact one, and since the exact fluxes move the band by $c\Delta x = w\Delta t$, the new fractions are those of the moved band. The moved band again has widths of at least $2\Delta x$, so the claim repeats at every step; the $y$ sweeps with $v = 0$ do nothing.

These are exact statements. The accuracy of the scheme for shapes that are not aligned with the grid, such as the rotating disk on the page, is measured, not proved. $\blacksquare$
