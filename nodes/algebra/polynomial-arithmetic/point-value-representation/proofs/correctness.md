---
title: The point-value operations, barycentric evaluation and divided differences are correct
proves: [correctness]
status: full
---

Let $F$ be a field, $n \ge 1$, and $U = (u_0, \ldots, u_{n-1})$ distinct points of $F$. Write $P_n$ for the set of polynomials in $F[x]$ of degree less than $n$, and $\operatorname{ev}_U(f) = (f(u_0), \ldots, f(u_{n-1}))$.

**Lemma 1 (interpolation is unique and exists).** The map $\operatorname{ev}_U : P_n \to F^n$ is a bijection. Its inverse is given by Lagrange's formula $L(y) = \sum_i y_i \ell_i$ with $\ell_i = \prod_{j \ne i} (x - u_j)/(u_i - u_j)$.

*Proof.* Each $\ell_i$ has degree $n - 1$, and $\ell_i(u_k)$ is $1$ for $k = i$ and $0$ for $k \ne i$, because the factor $x - u_k$ vanishes at $u_k$ and the denominators are nonzero since the points are distinct. So $L(y) \in P_n$ and $\operatorname{ev}_U(L(y)) = y$; the map is onto. If $f, g \in P_n$ have the same values, then $f - g \in P_n$ has the $n$ distinct roots $u_0, \ldots, u_{n-1}$. By the root bound of the factor theorem, a nonzero polynomial of degree less than $n$ has fewer than $n$ roots over a field, so $f - g = 0$; the map is one-to-one. $\square$

**Lemma 2 (ADD and MUL).** Let $y = \operatorname{ev}_U(f)$ and $z = \operatorname{ev}_U(g)$ with $f, g \in P_n$. Then ADD$(y, z) = \operatorname{ev}_U(f + g)$, and if $\deg f + \deg g < n$, MUL$(y, z) = \operatorname{ev}_U(fg)$. Without the degree condition, MUL$(y, z) = \operatorname{ev}_U(fg \bmod m)$ with $m = \prod_i (x - u_i)$.

*Proof.* Evaluation at $u_i$ is a ring homomorphism $F[x] \to F$, so $(f + g)(u_i) = f(u_i) + g(u_i) = y_i + z_i$ and $(fg)(u_i) = y_i z_i$. The sum $f + g$ is in $P_n$, so by Lemma 1 it is the polynomial that ADD$(y, z)$ represents. If $\deg f + \deg g < n$ then $fg \in P_n$, and the same argument applies. In general write $fg = qm + r$ with $\deg r < n$. Since $m(u_i) = 0$, $r(u_i) = (fg)(u_i) = y_i z_i$, and $r \in P_n$, so MUL$(y, z)$ represents $r = fg \bmod m$. $\square$

**Lemma 3 (EVALUATE-AT).** Let $w_i = 1/\prod_{j \ne i}(u_i - u_j)$, as computed by lines L1 to L3, and $f = L(y)$. For every $t \in F$, EVALUATE-AT$(y, t) = f(t)$.

*Proof.* If $t = u_k$, line L6 returns $y_k = f(u_k)$. Otherwise $t - u_i \ne 0$ for each $i$. Let $\ell(t) = \prod_j (t - u_j)$. For each $i$,

$$\ell_i(t) = \prod_{j \ne i} \frac{t - u_j}{u_i - u_j} = w_i \prod_{j \ne i} (t - u_j) = w_i \frac{\ell(t)}{t - u_i}.$$

So $f(t) = \sum_i y_i \ell_i(t) = \ell(t) \sum_i \frac{w_i y_i}{t - u_i}$, which lines L7 and L8 compute. $\square$

**Lemma 4 (divided differences).** For $0 \le j \le i \le n - 1$ let $p_{j,i} \in F[x]$ be the polynomial of degree at most $i - j$ with $p_{j,i}(u_l) = y_l$ for $j \le l \le i$ (it exists and is unique by Lemma 1 for the points $u_j, \ldots, u_i$), and let $f[u_j, \ldots, u_i]$ be the coefficient of $x^{i-j}$ in it. Then $f[u_i] = y_i$ and, for $j < i$,

$$f[u_j, \ldots, u_i] = \frac{f[u_{j+1}, \ldots, u_i] - f[u_j, \ldots, u_{i-1}]}{u_i - u_j}.$$

*Proof.* The constant $y_i$ interpolates at the single point $u_i$. For $j < i$ let

$$q = \frac{(x - u_j)\, p_{j+1,i} - (x - u_i)\, p_{j,i-1}}{u_i - u_j}.$$

Its degree is at most $i - j$. At $u_j$ the first term vanishes, and $q(u_j) = -(u_j - u_i) y_j / (u_i - u_j) = y_j$. At $u_i$ the second term vanishes, and $q(u_i) = (u_i - u_j) y_i / (u_i - u_j) = y_i$. At $u_l$ with $j < l < i$, both $p_{j+1,i}$ and $p_{j,i-1}$ take the value $y_l$, so $q(u_l) = y_l\, ((u_l - u_j) - (u_l - u_i))/(u_i - u_j) = y_l$. By uniqueness, $q = p_{j,i}$. The coefficient of $x^{i-j}$ in $q$ is the difference of the coefficients of $x^{i-j-1}$ in $p_{j+1,i}$ and $p_{j,i-1}$, divided by $u_i - u_j$, which is the recurrence. $\square$

**Lemma 5 (line L10).** After round $k$ of line L10 (and before round 1, for $k = 0$), $d[i] = f[u_{i-k}, \ldots, u_i]$ for $i \ge k$, and $d[i] = f[u_0, \ldots, u_i]$ for $i < k$.

*Proof.* Induction on $k$. For $k = 0$, $d = y$ and $f[u_i] = y_i$. Suppose the claim holds after round $k - 1$. Round $k$ updates $d[i]$ for $i = n - 1$ down to $k$, in decreasing order, so when $d[i]$ is updated, $d[i - 1]$ still holds the value from round $k - 1$. By the hypothesis, the new value is

$$\frac{f[u_{i-k+1}, \ldots, u_i] - f[u_{i-k}, \ldots, u_{i-1}]}{u_i - u_{i-k}} = f[u_{i-k}, \ldots, u_i]$$

by Lemma 4. The entry $d[k - 1]$ is not updated in round $k$ and equals $f[u_0, \ldots, u_{k-1}]$ from round $k - 1$; the entries below it were final before. $\square$

**Lemma 6 (Newton form).** Let $d_k = f[u_0, \ldots, u_k]$ and $f = L(y)$. Then

$$f = \sum_{k=0}^{n-1} d_k \prod_{j<k} (x - u_j).$$

*Proof.* Let $N_k = \sum_{l=0}^{k} d_l \prod_{j<l} (x - u_j)$. We show $N_k = p_{0,k}$ by induction. For $k = 0$, $N_0 = y_0 = p_{0,0}$. For $k \ge 1$, the polynomial $p_{0,k} - p_{0,k-1}$ has degree at most $k$ and vanishes at $u_0, \ldots, u_{k-1}$, so by the factor theorem it equals $c \prod_{j<k} (x - u_j)$ for a constant $c$. Comparing the coefficients of $x^k$ gives $c = d_k$, because $p_{0,k-1}$ has degree less than $k$. So $p_{0,k} = N_{k-1} + d_k \prod_{j<k}(x - u_j) = N_k$. For $k = n - 1$, $p_{0,n-1} = f$. $\square$

**Lemma 7 (lines L11 to L13).** Lines L11 and L12 compute $\sum_k d_k \prod_{j<k}(x - u_j)$, and line L13 returns its normalized coefficient list.

*Proof.* We claim that after the step of line L12 with index $i$ (and after line L11, with $i = n - 1$), $c = \sum_{k=i}^{n-1} d_k \prod_{j=i}^{k-1}(x - u_j)$. Line L11 sets $c = d_{n-1}$, the case $i = n - 1$. The step with index $i$ multiplies by $(x - u_i)$ and adds $d_i$:

$$\Bigl(\sum_{k=i+1}^{n-1} d_k \prod_{j=i+1}^{k-1}(x - u_j)\Bigr)(x - u_i) + d_i = \sum_{k=i}^{n-1} d_k \prod_{j=i}^{k-1}(x - u_j).$$

For $i = 0$ this is the Newton form. Line L13 removes only zero top entries, which does not change the polynomial. $\square$

**Theorem.** For distinct points $U$, every list in $F^n$ represents exactly one polynomial in $P_n$; ADD, MUL (under $\deg f + \deg g < n$), EVALUATE-AT and TO-COEFFICIENTS return the representation, the value, and the normalized coefficient list of the right polynomial.

*Proof.* Lemma 1 gives the representation, Lemma 2 the pointwise operations, Lemma 3 the evaluation, and Lemmas 5, 6 and 7 give TO-COEFFICIENTS$(y)$ $= L(y)$. $\blacksquare$
