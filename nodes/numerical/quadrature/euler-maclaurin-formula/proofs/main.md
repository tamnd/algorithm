---
title: The Euler-Maclaurin formula for the composite trapezoidal rule, with integral and mean value remainders
proves: [statement]
status: full
---

We use the notation and hypotheses of the statement: $a < b$, $m \ge 1$, $h = (b - a)/m$, $x_i = a + ih$, $p \ge 1$ and $f \in C^{2p}[a, b]$.

## Step 1: properties of the Bernoulli polynomials

The conditions $B_0 = 1$, $B_k' = kB_{k-1}$ and $\int_0^1B_k = 0$ ($k \ge 1$) determine each $B_k$ uniquely: the derivative fixes $B_k$ up to a constant, and the integral fixes the constant. So $B_1(t) = t - \frac12$ and $B_2(t) = t^2 - t + \frac16$.

(a) *Equal end values.* For $k \ge 2$, $B_k(1) - B_k(0) = \int_0^1B_k' = k\int_0^1B_{k-1} = 0$. Write $b_k = B_k(0) = B_k(1)$.

(b) *Symmetry.* The polynomials $C_k(t) = (-1)^kB_k(1 - t)$ satisfy $C_0 = 1$, $C_k' = (-1)^{k-1}kB_{k-1}(1 - t) = kC_{k-1}$ and $\int_0^1C_k = (-1)^k\int_0^1B_k = 0$, so $C_k = B_k$ by uniqueness: $B_k(1 - t) = (-1)^kB_k(t)$.

(c) *Odd Bernoulli numbers vanish.* For odd $k \ge 3$, (a) and (b) give $b_k = B_k(0) = -B_k(1) = -b_k$, so $b_k = 0$. Also $B_k(\frac12) = -B_k(\frac12) = 0$ for odd $k$.

(d) *Zeros.* For every $k \ge 0$, $B_{2k+1}$ has exactly one zero in $(0, 1)$, namely $\frac12$; and for every $k \ge 1$, $D_k(t) = B_{2k}(t) - b_{2k}$ has no zero in $(0, 1)$.

*Proof of (d), by induction on $k$.* $B_1 = t - \frac12$ has the single zero $\frac12$. Suppose $B_{2k-1}$ has only the zero $\frac12$ in $(0, 1)$, for some $k \ge 1$. Then $D_k' = 2kB_{2k-1}$ is nonzero on $(0, \frac12)$ and on $(\frac12, 1)$, so $D_k$ is strictly monotone on $[0, \frac12]$ and on $[\frac12, 1]$. Since $D_k(0) = D_k(1) = 0$ by (a), $D_k \ne 0$ on $(0, \frac12]$ and on $[\frac12, 1)$. Next, suppose $B_{2k+1}$ had a zero $t_0 \in (0, 1)$ other than $\frac12$. By (b), $1 - t_0$ is also a zero, and with $0$, $\frac12$, $1$ (by (a), (c)) $B_{2k+1}$ has at least five distinct zeros in $[0, 1]$. By Rolle's theorem $B_{2k+1}' = (2k + 1)B_{2k}$ has at least four zeros in $(0, 1)$, and again $B_{2k}' = 2kB_{2k-1}$ has at least three, contradicting the hypothesis. So $B_{2k+1}$ has only the zero $\frac12$ in $(0, 1)$, which completes the induction.

Since $\int_0^1D_k = -b_{2k}$ and $D_k$ has constant sign on $(0, 1)$, that sign is the sign of $-b_{2k}$, and $b_{2k} \ne 0$.

## Step 2: one panel

Let $g \in C^{2p}[0, 1]$. Since $B_1' = 1$,
$$\int_0^1g = \bigl[B_1g\bigr]_0^1 - \int_0^1B_1g' = \frac{g(0) + g(1)}{2} - \int_0^1B_1g'.$$
For $j \ge 1$, integrating by parts with $\bigl(\frac{B_{j+1}}{(j+1)!}\bigr)' = \frac{B_j}{j!}$ and (a),
$$\frac{1}{j!}\int_0^1B_jg^{(j)} = \frac{b_{j+1}}{(j+1)!}\bigl(g^{(j)}(1) - g^{(j)}(0)\bigr) - \frac{1}{(j+1)!}\int_0^1B_{j+1}g^{(j+1)}.$$
Applying this for $j = 1, \ldots, 2p - 1$ and collecting signs gives, by induction on the number of steps,
$$\int_0^1B_1g' = \sum_{j=2}^{2p}\frac{(-1)^jb_j}{j!}\bigl(g^{(j-1)}(1) - g^{(j-1)}(0)\bigr) + \frac{(-1)^{2p+1}}{(2p)!}\int_0^1B_{2p}g^{(2p)}.$$
(For $2p = 2$ this is the identity above with $j = 1$. Each further step replaces $\frac{(-1)^{j+1}}{j!}\int B_jg^{(j)}$ by $\frac{(-1)^{j+1}b_{j+1}}{(j+1)!}[g^{(j)}]_0^1 + \frac{(-1)^{j+2}}{(j+1)!}\int B_{j+1}g^{(j+1)}$.) By (c) only even $j$ survive in the sum, and for them $(-1)^j = 1$. With $j = 2k$:
$$\frac{g(0) + g(1)}{2} - \int_0^1g = \sum_{k=1}^{p}\frac{b_{2k}}{(2k)!}\bigl(g^{(2k-1)}(1) - g^{(2k-1)}(0)\bigr) - \frac{1}{(2p)!}\int_0^1B_{2p}g^{(2p)}.\tag{1}$$

## Step 3: all panels (part 1)

For panel $i$, let $g_i(t) = f(x_i + th)$. Then $g_i^{(j)}(t) = h^jf^{(j)}(x_i + th)$ and $\int_{x_i}^{x_{i+1}}f = h\int_0^1g_i$. Multiply (1) for $g_i$ by $h$:
$$h\frac{f(x_i) + f(x_{i+1})}{2} - \int_{x_i}^{x_{i+1}}f = \sum_{k=1}^{p}\frac{b_{2k}h^{2k}}{(2k)!}\bigl(f^{(2k-1)}(x_{i+1}) - f^{(2k-1)}(x_i)\bigr) - \frac{h^{2p}}{(2p)!}\int_{x_i}^{x_{i+1}}B_{2p}\Bigl(\frac{x - x_i}{h}\Bigr)f^{(2p)}(x)\,dx,$$
where the last integral used $x = x_i + th$, $h^{2p+1}\,dt = h^{2p}\,dx$. On $[x_i, x_{i+1})$, $\frac{x - x_i}{h} = \frac{x - a}{h} - i$ is the fractional part of $\frac{x - a}{h}$, so $B_{2p}(\frac{x - x_i}{h}) = \tilde B_{2p}(\frac{x - a}{h})$ there. Summing over $i = 0, \ldots, m - 1$, the left sides add to $T_h(f) - I(f)$, each derivative difference telescopes to $f^{(2k-1)}(b) - f^{(2k-1)}(a)$, and the integrals combine into $\int_a^b$. This is part 1.

## Step 4: mean value form (parts 2 and 3)

Since $\int_a^bf^{(2p)} = f^{(2p-1)}(b) - f^{(2p-1)}(a)$, the $k = p$ boundary term equals $\frac{b_{2p}h^{2p}}{(2p)!}\int_a^bf^{(2p)}$. Adding it to $R_p$ gives
$$T_h(f) - I(f) = \sum_{k=1}^{p-1}\frac{b_{2k}h^{2k}}{(2k)!}\bigl(f^{(2k-1)}(b) - f^{(2k-1)}(a)\bigr) - \frac{h^{2p}}{(2p)!}\int_a^b\tilde D_p\Bigl(\frac{x - a}{h}\Bigr)f^{(2p)}(x)\,dx,$$
with $\tilde D_p = \tilde B_{2p} - b_{2p}$. By Step 1(d), $\tilde D_p(\frac{x - a}{h})$ has one sign on $[a, b]$ (it is zero only at the nodes). As $f^{(2p)}$ is continuous, the mean value theorem for integrals gives $\xi \in [a, b]$ with
$$\int_a^b\tilde D_p\Bigl(\frac{x - a}{h}\Bigr)f^{(2p)}(x)\,dx = f^{(2p)}(\xi)\int_a^b\tilde D_p\Bigl(\frac{x - a}{h}\Bigr)dx = f^{(2p)}(\xi)\cdot m h\int_0^1D_p = -(b - a)\,b_{2p}\,f^{(2p)}(\xi).$$
Substituting gives part 2. Part 3 follows by bounding $\lvert f^{(2p)}(\xi)\rvert$ by its maximum.

## Step 5: the summation form

With $a = 0$, $b = n$, $m = n$ and $h = 1$, $T_1(f) = \sum_{k=0}^nf(k) - \frac{f(0) + f(n)}{2}$, and part 1 rearranges to the summation form in the statement. $\blacksquare$
