---
title: The decimation-in-frequency and decimation-in-time stages compute the DFT in bit-reversed and natural order, and their pairing computes the cyclic convolution
proves: [correctness, complexity]
status: full
---

**Setting.** $R$ is a commutative ring, $n = 2^t$ with $t \ge 0$, and $\omega \in R$ satisfies $\omega^n = 1$ and, if $t \ge 1$, $\omega^{n/2} = -1$. This implies that $\omega$ is a principal $n$-th root of unity (proved on the page on roots of unity). Conversely, a principal root has $\omega^{n/2} = -1$ whenever $\frac{n}{2} \cdot 1$ is not a zero divisor, for then $\sum_{j<n} (\omega^{n/2})^j = \frac{n}{2}(1 + \omega^{n/2}) = 0$ forces $\omega^{n/2} = -1$; this covers every field of characteristic other than $2$, every $\mathbb{Z}/p\mathbb{Z}$ with $p$ odd, and every ring in which $n$ is a unit. (Without it the radix-2 split fails: in $\mathbb{Z}/4\mathbb{Z}$, $\omega = 1$ is a principal $4$-th root, but $\omega^2 \ne -1$.) If $t \ge 2$, the element $\omega^2$ has the same two properties for $n/2$, since $(\omega^2)^{n/4} = \omega^{n/2} = -1$; this is what the inductions use. For $0 \le i < 2^t$ let $\mathrm{rev}_t(i)$ be $i$ with its $t$ binary digits reversed, and let $(Py)_i = y_{\mathrm{rev}_t(i)}$. Since $\mathrm{rev}_t$ is an involution, $P^{-1} = P$. Two facts about digits are used: for $0 \le q < 2^{t-1}$,

$$\mathrm{rev}_t(q) = 2\,\mathrm{rev}_{t-1}(q), \qquad \mathrm{rev}_t(2^{t-1} + q) = 2\,\mathrm{rev}_{t-1}(q) + 1, \tag{1}$$

because the top digit of $q$ is $0$ and that of $2^{t-1} + q$ is $1$, and reversal moves the top digit to the bottom. Also, $\mathrm{rev}_t(2q) = \mathrm{rev}_{t-1}(q)$ and $\mathrm{rev}_t(2q + 1) = 2^{t-1} + \mathrm{rev}_{t-1}(q)$ by the same reasoning.

**Lemma 1 (decimation in frequency).** Let $D_t^\omega$ be the map of lines L3 to L10 on an array of length $2^t$, with $W[k] = \omega^k$. Then $D_t^\omega(x) = P\,\mathrm{DFT}_\omega(x)$.

*Proof.* Induction on $t$. For $t = 0$ the loop does nothing and $P$ is the identity. Let $t \ge 1$ and $n = 2^t$. The first pass has $h = n/2$, one block $s = 0$, and stride $n/(2h) = 1$; its butterflies touch the disjoint pairs $(k, k + n/2)$, read both cells before writing, and produce

$$u_j = x_j + x_{j + n/2}, \qquad v_j = \omega^j (x_j - x_{j + n/2}), \qquad 0 \le j < n/2.$$

Split the sum for $X_k$ at $n/2$ and use $\omega^{(j + n/2)k} = \omega^{jk} (-1)^k$:

$$X_k = \sum_{j < n/2} \bigl(x_j + (-1)^k x_{j+n/2}\bigr) \omega^{jk}.$$

For $k = 2m$ this is $\sum_j u_j (\omega^2)^{jm}$, and for $k = 2m + 1$ it is $\sum_j (x_j - x_{j + n/2}) \omega^j (\omega^2)^{jm} = \sum_j v_j (\omega^2)^{jm}$. So $(X_{2m})_m = \mathrm{DFT}_{\omega^2}(u)$ and $(X_{2m+1})_m = \mathrm{DFT}_{\omega^2}(v)$.

The later passes have $h \le n/4$, so every block of length $2h$ lies inside one half of the array, and no butterfly mixes the halves. On each half, the pass with half length $h$ reads $W[k \cdot n/(2h)] = \omega^{k n/(2h)} = (\omega^2)^{k \cdot (n/2)/(2h)}$, which is the twiddle factor of the pass with half length $h$ of $D_{t-1}^{\omega^2}$. So the later passes apply $D_{t-1}^{\omega^2}$ to $u$ and to $v$ separately. By the induction hypothesis, for $0 \le q < n/2$, position $q$ ends with $X_{2\,\mathrm{rev}_{t-1}(q)}$, and position $n/2 + q$ ends with $X_{2\,\mathrm{rev}_{t-1}(q) + 1}$. By (1) these are $X_{\mathrm{rev}_t(q)}$ and $X_{\mathrm{rev}_t(n/2 + q)}$. $\square$

**Correctness of ITERATIVE-FFT.** Lines L11 and L12 visit each pair $\{j, \mathrm{rev}_t(j)\}$ with $j \ne \mathrm{rev}_t(j)$ once, at its smaller element, and swap it, so they apply $P$. By Lemma 1 the result is $P P\, \mathrm{DFT}_\omega(x) = \mathrm{DFT}_\omega(x)$.

**Lemma 2 (decimation in time).** Let $T_t^\omega$ be the map of lines L16 to L22 on an array of length $2^t$ with $V[k] = \omega^k$. Then $T_t^\omega(P z) = \mathrm{DFT}_\omega(z)$ for each $z \in R^{2^t}$.

*Proof.* Induction on $t$; $t = 0$ is trivial. Let $t \ge 1$, $n = 2^t$, and $y = Pz$. The passes with $h \le n/4$ never mix the halves, and on each half they are the passes of $T_{t-1}^{\omega^2}$, by the same computation of the twiddle factors as in Lemma 1. By the facts after (1), for $q < n/2$, $y_q = z_{\mathrm{rev}_t(q)} = z_{2\,\mathrm{rev}_{t-1}(q)}$ and $y_{n/2 + q} = z_{2\,\mathrm{rev}_{t-1}(q) + 1}$. So the first half of $y$ is $P_{t-1} e$ with $e_m = z_{2m}$, and the second half is $P_{t-1} o$ with $o_m = z_{2m+1}$. By the induction hypothesis, after the first $t - 1$ passes the halves hold $E = \mathrm{DFT}_{\omega^2}(e)$ and $O = \mathrm{DFT}_{\omega^2}(o)$. The last pass, $h = n/2$, maps $(E_k, O_k)$ to $(E_k + \omega^k O_k,\ E_k - \omega^k O_k)$. Splitting $X_k$ by the parity of $j$ gives $X_k = E_{k \bmod n/2} + \omega^k O_{k \bmod n/2}$, and $\omega^{k + n/2} = -\omega^k$, so these two values are $X_k$ and $X_{k + n/2}$. $\square$

**Correctness of CYCLIC-CONVOLUTION.** By Lemma 1, after line L13, $a$ and $b$ hold $P\hat a$ and $P\hat b$, where $\hat a = \mathrm{DFT}_\omega(a)$. Since $(P y)_i = y_{\mathrm{rev}_t(i)}$, line L14 gives $c = P(\hat a \odot \hat b)$ with the entrywise product $\odot$. The element $\omega^{-1} = \omega^{n-1}$ is again a principal $n$-th root of unity (its powers are those of $\omega$ in another order), so Lemma 2 applies with the root $\omega^{-1}$ and gives $\mathrm{DFT}_{\omega^{-1}}(\hat a \odot \hat b)$ after line L22. By the convolution theorem, $\hat a \odot \hat b = \mathrm{DFT}_\omega(a \ast b)$, where $(a \ast b)_m = \sum_j a_j b_{(m-j) \bmod n}$: indeed $\sum_m (a \ast b)_m \omega^{mk} = \sum_j a_j \omega^{jk} \sum_m b_{(m-j) \bmod n} \omega^{(m - j)k}$, and the inner sum is $\hat b_k$ because $\omega^n = 1$. Finally, $\mathrm{DFT}_{\omega^{-1}}(\mathrm{DFT}_\omega(y)) = n y$, since its entry $j$ is $\sum_m y_m \sum_k \omega^{(m - j)k} = n y_j$ by the definition of a principal root. So after line L22, $c = n (a \ast b)$, and since $n$ is a unit, line L23 returns $a \ast b$.

**Operation count.** In every pass there are $n/(2h)$ blocks of $h$ butterflies, so $n/2$ butterflies, each with one addition, one subtraction and one multiplication. There are $t = \lg n$ passes. So lines L3 to L10, and also lines L16 to L22, do exactly $n \lg n$ additions and subtractions and $\frac{n}{2}\lg n$ multiplications, for every input, and ITERATIVE-FFT does no further ring operation except at most $n/2$ multiplications for the table of line L2. CYCLIC-CONVOLUTION does three such transforms, $n$ multiplications in line L14 and $n$ in line L23: $3 n \lg n$ additions and $\frac{3}{2} n \lg n + 2n$ multiplications, besides the two tables. The index work is proportional to the number of butterflies plus $O(n)$ for the permutation, so the time is $\Theta(n \log n)$ for every input. The transforms write only into the arrays they are given; the tables take $\Theta(n)$ extra space. $\blacksquare$
