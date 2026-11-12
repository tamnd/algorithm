---
title: The grid walk visits distinct face-adjacent cells met by the segment, in order, and stops
proves: [correctness, termination]
status: full
---

**Setting.** The grid has cells $C(c) = \prod_a [\ell_a + c_a s, \ell_a + (c_a + 1) s]$ for integer $c_a \in \{0, \dots, n_a - 1\}$. The segment is $r(t) = o + t d$, $d \ne 0$, for $t \in [t_0, t_1]$. Line L1 gives $[t_\text{enter}, t_\text{end}]$, the part of $[t_0, t_1]$ where $r(t)$ lies in the closed grid box $B$; if it is empty, the walk visits nothing, which is correct. We use exact arithmetic. For an axis $a$ with $d_a \ne 0$, let $\tau_a(c)$ be the parameter at which the ray reaches the boundary plane of the slab $\ell_a + c_a s \le x_a \le \ell_a + (c_a + 1)s$ in the direction of motion: the upper plane when $d_a > 0$, the lower plane when $d_a < 0$. For $d_a = 0$ set $\tau_a(c) = \infty$.

**Invariant.** At each arrival at line L6, with current cell $c$ and entry value $t_\text{in}$:

1. $t_\text{in} \le t_\text{end}$, $t_\text{in} \le \tau_a(c)$ for every axis, and $r(t_\text{in}) \in C(c)$;
2. $t_{\max}[a] = \tau_a(c)$ for every axis $a$.

**Lemma 1 (the start).** The invariant holds at the first arrival.

*Proof.* Let $p = r(t_\text{enter}) \in B$. Line L2 sets $c_a = \lfloor (p_a - \ell_a)/s \rfloor$, clamped to $[0, n_a - 1]$. Without the clamp, $\ell_a + c_a s \le p_a < \ell_a + (c_a + 1)s$. The clamp only changes the index when $p_a = \ell_a + n_a s$, on the top face of $B$, and then $p_a$ is the upper bound of the cell $n_a - 1$. So $p \in C(c)$. Line L3 computes $t_{\max}[a]$ from the formula for $\tau_a(c)$. Since $p_a$ lies in the slab of $c$ on axis $a$ and the ray moves toward the plane that defines $\tau_a(c)$, $t_\text{enter} \le \tau_a(c)$. $\square$

**Lemma 2 (the piece in the cell).** Under the invariant, $r(t) \in C(c)$ for every $t \in [t_\text{in}, t_\text{out}]$, where $t_\text{out} = \min(\min_b \tau_b(c), t_\text{end})$.

*Proof.* On axis $a$ with $d_a \ne 0$, $r_a(t)$ is monotone. At $t_\text{in}$ it lies in the slab of $c$, and it does not leave the slab before it reaches the plane in the direction of motion, at $\tau_a(c) \ge t_\text{out}$. On an axis with $d_a = 0$, $r_a(t) = r_a(t_\text{in})$. $\square$

Line L5 picks an axis $a$ with $t_{\max}[a] = \min_b t_{\max}[b]$: the first comparison and the second compare the three values so that the chosen value is not larger than either other value. So line L6 reports $t_\text{out} = \min(t_{\max}[a], t_\text{end})$, and by Lemma 2 the segment meets the reported cell on $[t_\text{in}, t_\text{out}]$.

**Lemma 3 (the step).** If the walk does not stop at line L7 or L9, the invariant holds at the next arrival.

*Proof.* Not stopping at L7 means $\tau_a(c) \le t_\text{end}$, so $\tau_a(c)$ is finite and $d_a \ne 0$. Line L8 moves to $c' = c + \operatorname{sign}(d_a) e_a$, and line L9 confirms that $c'$ is a grid cell. The new entry value is $t'_\text{in} = \tau_a(c) \le t_\text{end}$. At that parameter, $r_a$ is on the plane shared by the slabs of $c$ and $c'$ on axis $a$, and for $b \ne a$, $r_b(t'_\text{in})$ is in the slab of $c$ on axis $b$, by Lemma 2, which is also the slab of $c'$. So $r(t'_\text{in}) \in C(c')$. For $b \ne a$, $\tau_b(c') = \tau_b(c) \ge t'_\text{in}$ because the slabs agree. On axis $a$ the next plane in the direction of motion is one width $s$ farther, which the ray reaches after $s/|d_a| = t_\Delta[a]$ more units of $t$, so line L10 gives $t_{\max}[a] = \tau_a(c) + t_\Delta[a] = \tau_a(c') \ge t'_\text{in}$. $\square$

**Lemma 4 (termination and count).** The walk stops after at most $n_x + n_y + n_z - 2$ steps. The visited cells are distinct, consecutive cells share a face, and the number of visited cells is $1 + \sum_a |c^\text{last}_a - c^\text{first}_a|$.

*Proof.* Each step changes one index by $\operatorname{sign}(d_a)$, a fixed sign for each axis. So each index is monotone, and on axis $a$ it can change at most $n_a - 1$ times before line L9 stops the walk. Two visited cells with the same indices would need every index to return, which a monotone sequence with a strict change between them cannot do. The cells $c$ and $c'$ of a step differ by one in one index, so they share a face. The number of steps on axis $a$ is $|c^\text{last}_a - c^\text{first}_a|$, which gives the count. $\square$

**Lemma 5 (coverage).** The pieces $[t_\text{in}, t_\text{out}]$ of the visited cells are consecutive and their union is $[t_\text{enter}, t_\text{end}]$. Every cell whose interior the segment meets is visited.

*Proof.* By Lemma 3, each piece starts where the previous one ended. The walk stops at L7 when $t_\text{out} = t_\text{end}$. It stops at L9 when the step on axis $a$ leaves the grid; then $r(\tau_a(c))$ lies on a face of $B$ and the ray leaves $B$ there, so $\tau_a(c) = t_\text{end}$ by the definition of the clip. So the pieces cover $[t_\text{enter}, t_\text{end}]$. If the segment meets the interior of a cell $C$ at a parameter $t$, then $r(t)$ is in no other closed cell, and $t$ lies in the piece of some visited cell, which by Lemma 2 contains $r(t)$; that cell is $C$. $\square$

**Lemma 6 (exact list in the generic case).** Call the planes $x_a = \ell_a + m s$, $m = 0, \dots, n_a$, the grid planes. Suppose $r(t_0)$ and $r(t_1)$ lie on no grid plane, and no two grid planes are crossed at the same parameter in $(t_0, t_1)$. Then the visited cells are exactly the cells that the segment meets, and the piece of each cell is the whole interval of $t$ where the segment is in that cell. So the cells come in order of first contact.

*Proof.* If $d_a = 0$, then $r_a$ is constant and equal to $r_a(t_0)$, which is on no grid plane. So at each $t$, a coordinate $r_a(t)$ is on a grid plane only if the ray crosses that plane at $t$, and by the assumption this happens for at most one axis. Let $C$ be a grid cell and $r(t_c) \in C$ with $t_c \in [t_\text{enter}, t_\text{end}]$. If no coordinate of $r(t_c)$ is on a grid plane, $r(t_c)$ is in the interior of $C$. Otherwise exactly one coordinate $a$ is on a plane and the other coordinates are strictly inside their slabs, also for all $t$ near $t_c$. Then $C$ is one of the two cells on the sides of that plane. If $t_c$ is inside $(t_\text{enter}, t_\text{end})$, the ray is in the interior of one of them just before $t_c$ and in the interior of the other just after. If $t_c = t_\text{enter}$, then $t_c > t_0$ because $r(t_0)$ is on no plane, so the plane is a face of $B$ and only the cell on the inside is a grid cell; the ray is in its interior just after $t_c$. The case $t_c = t_\text{end}$ is the same. In each case the segment meets the interior of $C$ at parameters arbitrarily close to $t_c$. By Lemma 5, $C$ is visited, and its closed piece contains all those parameters, so it contains $t_c$. With Lemma 2, the piece of $C$ is exactly the set of $t$ where $r(t) \in C$. The pieces are in increasing order of $t$. $\square$

**Theorem.** The walk terminates. It reports distinct, face-adjacent grid cells, each met by the segment, in increasing order of their entry parameter, with the parameter interval of each piece. It reports every cell whose interior the segment meets, and in the generic case of Lemma 6 it reports exactly the cells met.

*Proof.* Lemmas 1 to 6. $\blacksquare$

**The closest-hit rule.** Let the walk test the objects of each cell and accept a hit at parameter $t$ only when $t \le t_\text{out}$ of the current cell; let it stop at the first cell with an accepted hit, returning the smallest one. Suppose each object is stored in every cell that its closed extent overlaps, and let the hit parameter of an object be its first parameter on the segment. Let $t_h$ be the smallest hit parameter over all objects, on an object $X$. The parameter $t_h$ lies in the piece of some visited cell $C$ (Lemma 5), $X$ contains $r(t_h) \in C$, so $X$ is stored in $C$ and its hit is accepted there because $t_h \le t_\text{out}$. So the walk stops at $C$ or at an earlier cell. Every hit parameter is at least $t_h$. In a cell before $C$, an accepted hit has $t \le t_\text{out} \le t_h$, so $t = t_h$. In $C$, the smallest accepted hit is at most $t_h$, so it is $t_h$. In both cases the walk returns a hit at $t_h$, a closest hit. Without the check $t \le t_\text{out}$, a cell before $C$ can return an object whose hit lies beyond $C$, which the tests of the implementation show. The mailbox does not change the result, because the stored value of an object is its hit parameter on the whole segment, which is the same in every cell.
