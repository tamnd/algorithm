---
title: HAAR computes the Haar coefficients, and INVERSE-HAAR inverts it
proves: [correctness, complexity]
status: full
---

**Statement.** Let $n = 2^t$ with $t \ge 0$, let $x^{\mathrm{in}} \in \mathbb{R}^n$, and let $c \ne 0$. After HAAR$(x, c)$, $x[0] = (2c)^t \cdot \mu$ where $\mu$ is the mean of $x^{\mathrm{in}}$, and for $0 \le j < t$ and $0 \le k < 2^j$,

$$x[2^j + k] = (2c)^{t-j} \cdot \frac{\mu^-_{j,k} - \mu^+_{j,k}}{2},$$

where $\mu^-_{j,k}$ and $\mu^+_{j,k}$ are the means of $x^{\mathrm{in}}$ on the left half $B^-_{j,k}$ and the right half $B^+_{j,k}$ of the block $B_{j,k} = [kL_j, (k+1)L_j)$, $L_j = n/2^j$. INVERSE-HAAR$(x, c)$ then gives back $x^{\mathrm{in}}$. With $c = 1/2$ these are the coefficients by averages. With $c = 1/\sqrt 2$, $(2c)^{t-j} = \sqrt{L_j}$ and $(2c)^t = \sqrt n$, so the outputs are $\langle x^{\mathrm{in}}, \varphi \rangle$ and $\langle x^{\mathrm{in}}, \psi_{j,k} \rangle$: indeed $\sqrt{L_j}(\mu^- - \mu^+)/2 = (\sum_{B^-} x - \sum_{B^+} x)/\sqrt{L_j}$ because each half has $L_j/2$ entries, and $\sqrt n \mu = \sum x / \sqrt n$.

**Setup.** Write $M(i, L)$ for the mean of $x^{\mathrm{in}}$ on $[iL, (i+1)L)$. The pass number $q = 0, 1, \ldots$ starts when line L2 tests $m = n/2^q$; let $L = 2^q$.

**Invariant (I).** When line L2 tests $m = n/2^q$:

1. $x[i] = (2c)^q M(i, 2^q)$ for $0 \le i < m$;
2. for each level $j$ with $2^j \ge m$ (that is, $j \ge t - q$) and each $0 \le k < 2^j$, $x[2^j + k]$ has the value of the statement.

*Initialization.* $q = 0$, $m = n$, $M(i, 1) = x^{\mathrm{in}}_i$ and $(2c)^0 = 1$, so part 1 holds. No level $j < t$ has $2^j \ge n$, so part 2 is empty.

*Maintenance.* Assume (I) at $m \ge 2$, and let $h = m/2$, so $h = 2^{t-q-1}$ and the new pass makes level $j = t - q - 1$. For $0 \le i < h$, lines L4 and L5 read $x[2i]$ and $x[2i+1]$, which by part 1 are $(2c)^q M(2i, 2^q)$ and $(2c)^q M(2i+1, 2^q)$. These positions are below $m$, and lines L4 and L5 write only into $T$, so every read sees the old values. The two blocks $[2i \cdot 2^q, (2i+1)2^q)$ and $[(2i+1)2^q, (2i+2)2^q)$ are the halves of the block $[i \cdot 2^{q+1}, (i+1) 2^{q+1})$, which is $B_{j,i}$ since $L_j = n/2^j = 2^{q+1}$. The mean of a block is the average of the means of its halves, so

$$T[i] = c \cdot (2c)^q \bigl(M(2i, 2^q) + M(2i+1, 2^q)\bigr) = (2c)^{q+1} M(i, 2^{q+1}),$$

$$T[h + i] = c \cdot (2c)^q \bigl(\mu^-_{j,i} - \mu^+_{j,i}\bigr) = (2c)^{t-j} \cdot \frac{\mu^-_{j,i} - \mu^+_{j,i}}{2},$$

using $q + 1 = t - j$. Line L6 copies $T[0 \ldots m-1]$ into $x$ and does not touch $x[m \ldots n-1]$, which keeps the old part 2 for the levels $j' > j$. The new part 1 is the first line for $i < h$, and the new part 2 adds level $j$ at the positions $2^j + i = h + i$. Line L7 sets $m = h = n/2^{q+1}$, so (I) holds for $q + 1$.

*Termination.* $m$ halves in each pass and starts at $n = 2^t$, so after exactly $t$ passes $m = 1$ and the loop stops. Then part 1 gives $x[0] = (2c)^t M(0, n) = (2c)^t \mu$, and part 2 covers all levels $0 \le j < t$. This proves the claim about HAAR.

**Inverse.** We show that the pass of INVERSE-HAAR with length $m$ undoes the pass of HAAR with length $m$. That pass of HAAR maps the old front $v[0 \ldots m-1]$ to $s_i = c(v_{2i} + v_{2i+1})$ at $i$ and $d_i = c(v_{2i} - v_{2i+1})$ at $h + i$. Then $s_i + d_i = 2c\, v_{2i}$ and $s_i - d_i = 2c\, v_{2i+1}$, so lines L11 and L12 recover $v_{2i}$ and $v_{2i+1}$ (here $c \ne 0$ is used), and line L13 writes them back to the front, leaving $y[m \ldots n-1]$ unchanged. HAAR runs the passes with $m = n, n/2, \ldots, 2$, and INVERSE-HAAR runs the inverse passes with $m = 2, 4, \ldots, n$, the reverse order. A composition of maps undone in reverse order is the identity, so INVERSE-HAAR gives back $x^{\mathrm{in}}$. For $n = 1$ both loops do nothing, which is correct since then the transform is the identity.

**Operation count.** The pass with length $m$ does $m/2$ additions (line L4), $m/2$ subtractions (line L5) and $m$ multiplications by $c$. The passes have $m = 2^t, 2^{t-1}, \ldots, 2$, and $\sum_{q=1}^{t} 2^q = 2^{t+1} - 2 = 2n - 2$. So HAAR does exactly $2n - 2$ additions and subtractions and $2n - 2$ multiplications, for every input. The number of steps of all lines is proportional to this sum plus $t + 1$ loop tests, so the time is $\Theta(n)$ in the best and the worst case. The buffer $T$ has $n$ entries, and no other storage grows with $n$, so the extra space is $\Theta(n)$. $\blacksquare$
