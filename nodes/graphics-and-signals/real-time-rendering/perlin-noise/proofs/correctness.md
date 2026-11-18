---
title: Improved Perlin noise is a C2 sum of lattice kernels that vanishes at the lattice points
proves: [correctness]
status: full
---

We use the pseudocode and the notation of the page, in $n = 3$ dimensions. The proofs for other dimensions are the same with $2^n$ corners. Let $f(t) = 6t^5 - 15t^4 + 10t^3$ be the fade, and for each lattice point $q \in \mathbb{Z}^3$ let $g_q \in G$ be the gradient that the permutation gives to $q$ (the function `corner_gradient` of the code). Arithmetic is exact (real-ram).

**Lemma 1 (the fade).** $f(0) = 0$, $f(1) = 1$, $f(1 - t) = 1 - f(t)$ for all $t$, and $f'(0) = f'(1) = f''(0) = f''(1) = 0$. On $[0, 1]$, $f$ is nondecreasing, so $0 \le f(t) \le 1$.

*Proof.* $f'(t) = 30 t^4 - 60 t^3 + 30 t^2 = 30 t^2 (t - 1)^2$ and $f''(t) = 60 t (t - 1)(2t - 1)$. Both vanish at 0 and 1. The values at 0 and 1 follow by substitution. The polynomial $f(t) + f(1 - t) - 1$ has the derivative $f'(t) - f'(1 - t) = 30 t^2 (t-1)^2 - 30 (1-t)^2 t^2 = 0$, so it is constant, and its value at $t = 0$ is $0 + 1 - 1 = 0$. Last, $f' \ge 0$ everywhere. $\square$

**Lemma 2 (the nested lerps are a tensor product sum).** Let $p$ lie in the cell $c + [0, 1)^3$ with $c = \lfloor p \rfloor$, and let $t = p - c$. Lines L3 to L8 return
$$N(p) = \sum_{a, b, e \in \{0, 1\}} W_a(t_x)\, W_b(t_y)\, W_e(t_z)\; g_{c + (a, b, e)} \cdot (t - (a, b, e)),$$
with $W_0(s) = 1 - f(s)$ and $W_1(s) = f(s)$.

*Proof.* Line L5 computes the hash of the corner $c + (a, b, e)$, and line L6 its value $n_{abe} = g_{c + (a,b,e)} \cdot (t - (a, b, e))$, because GRAD returns the dot product with the gradient of index $h \bmod 16$ (the code test `test_grad_matches_table` lists all 16 cases). $\mathrm{lerp}(s, A, B) = W_0(s) A + W_1(s) B$. Line L7 applies the lerp in $x$ to each of the four pairs, then in $y$, then in $z$. Expanding the three levels gives each corner value exactly once, multiplied by one weight per axis. $\square$

**Lemma 3 (one kernel per lattice point).** Let $s(r) = 1 - f(|r|)$ for $|r| \le 1$ and $s(r) = 0$ for $|r| > 1$, and let $K(d) = s(d_x)\, s(d_y)\, s(d_z)$. Then for every $p \in \mathbb{R}^3$
$$N(p) = \sum_{q \in \mathbb{Z}^3} K(p - q)\; g_q \cdot (p - q).$$

*Proof.* Fix $p$ in the cell of $c$ with $t = p - c$. A lattice point $q$ with $|p_x - q_x| > 1$ in some axis has $K(p - q) = 0$. A point with $|p_x - q_x| = 1$ exactly also gives $s = 1 - f(1) = 0$. So only the 8 corners $q = c + (a, b, e)$ remain, with $0 \le t_x < 1$. For $a = 0$, $s(t_x) = 1 - f(t_x) = W_0(t_x)$. For $a = 1$, $s(t_x - 1) = 1 - f(1 - t_x) = f(t_x) = W_1(t_x)$ by Lemma 1. The same holds in $y$ and $z$, so the sum is the sum of Lemma 2. $\square$

**Theorem 1 (zeros at the lattice).** $N(q) = 0$ for every $q \in \mathbb{Z}^3$.

*Proof.* By Lemma 3, a lattice point $q' \ne q$ differs from $q$ by at least 1 in some axis, so $K(q - q') = 0$. The term of $q$ itself is $K(0)\, g_q \cdot 0 = 0$. $\square$

**Theorem 2 (smoothness).** $N$ is twice continuously differentiable on $\mathbb{R}^3$, and $\nabla N(q) = g_q$ at every lattice point $q$.

*Proof.* The function $s$ is $C^2$ on $\mathbb{R}$. On $(0, 1)$ it is the polynomial $1 - f(r)$, and on $(-1, 0)$ the polynomial $1 - f(-r)$. At $r = 0$ both pieces have the value 1, the first derivative $\mp f'(0) = 0$ and the second derivative $-f''(0) = 0$. At $r = \pm 1$ the pieces have the value $1 - f(1) = 0$, the first derivative $\mp f'(1) = 0$ and the second derivative $-f''(1) = 0$, which match the zero function outside. So $K$ is $C^2$, each term $K(p - q)\, g_q \cdot (p - q)$ is $C^2$, and on any bounded set only finitely many terms are not zero. So $N$ is $C^2$. At a lattice point $q$, every other term $q'$ has $K(q - q') = 0$ and $\nabla K(q - q') = 0$, because $s$ and $s'$ vanish at $\pm 1$ and $s(0) = 1$, so each component of $\nabla K$ holds one factor $s(\pm 1)$ or $s'(\pm 1)$. The term of $q$ has the gradient $K(0) g_q + (g_q \cdot 0) \nabla K(0) = g_q$. $\square$

With the cubic fade $3t^2 - 2t^3$ of Perlin's 1985 noise, $f''(0) = 6$ and $f''(1) = -6$. Then $s''(r) = -f''(1) = 6$ just inside $r = \pm 1$ and $0$ outside, so $s''$ jumps by 6 there. So $N$ is only $C^1$, and its second derivative jumps on the cell faces. This is the reason for the quintic fade.

**Theorem 3 (a bound on the range).** $|N(p)| \le 2$ for every $p$.

*Proof.* Each gradient $g \in G$ has two components equal to $\pm 1$ and one equal to 0. Each offset $t - (a, b, e)$ has components in $[-1, 1]$. So each corner value is at most $1 + 1 = 2$ in absolute value. By Lemma 1 the weights $W_0, W_1$ are in $[0, 1]$ and $W_0 + W_1 = 1$, so the 8 products in Lemma 2 are nonnegative and sum to 1. A convex combination of numbers in $[-2, 2]$ lies in $[-2, 2]$. $\square$

The bound is not tight. A corner value of 2 needs an offset with two components of absolute value 1, and where an offset component has absolute value 1, the weight of that corner is 0.

**Theorem 4 (the period).** $N(p + 256\, e_i) = N(p)$ for each unit axis vector $e_i$.

*Proof.* Line L1 reduces the cell index modulo 256, and line L2 does not change under an integer shift. The table $P$ has 512 entries with $P[i + 256] = P[i]$, so the hashes of line L5 depend only on the cell index modulo 256. So every quantity in lines L3 to L8 is the same at $p$ and at $p + 256\, e_i$. $\square$

**Cost.** Lines L1 to L3 take $O(n)$ operations. The loop runs over $2^n$ corners. Each corner takes $n$ table lookups and a dot product of length $n$, so $O(n)$. Line L7 takes $2^n - 1$ lerps. The total is $\Theta(n 2^n)$ operations per point, which is $O(1)$ for the fixed $n = 3$ of the code.
