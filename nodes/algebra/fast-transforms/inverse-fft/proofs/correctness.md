---
title: INVERSE-FFT computes the inverse DFT with n lg n additions and (n/2) lg n + n multiplications
proves: [correctness, complexity]
status: full
---

**Statement.** Let $R$ be a commutative ring, $n = 2^t$ with $t \ge 0$, $\omega \in R$ a principal $n$-th root of unity, and suppose $n \cdot 1$ is a unit of $R$. For each $X \in R^n$, INVERSE-FFT$(X, \omega)$ ends with $X$ replaced by the unique $x \in R^n$ with $\mathrm{DFT}_\omega(x) = X$, that is $x_j = \frac{1}{n} \sum_k X_k \omega^{-jk}$. Without line L13 it ends with $n x$. It does exactly $n \lg n$ additions and subtractions and $\frac{n}{2}\lg n + n$ multiplications, besides the at most $n/2$ multiplications of line L2.

**The forward stages.** For $1 \le h \le n/2$ a power of two, let $W_h = \omega^{n/(2h)}$ and let $S_h : R^n \to R^n$ be the map that, for each block start $s \in \{0, 2h, 4h, \ldots\}$ and each $0 \le k < h$, replaces the pair $(y_{s+k}, y_{s+k+h}) = (u, v)$ by $(u + W_h^k v,\ u - W_h^k v)$. The pairs for different $(s, k)$ are disjoint and cover all positions, so $S_h$ is well defined and $R$-linear. Let $P$ be the bit-reversal permutation of the positions, $(Py)_j = y_{\mathrm{rev}_t(j)}$. The iterative FFT computes $P$ and then $S_1, S_2, \ldots, S_{n/2}$, and its correctness (proved on the page of the fast Fourier transform) is the identity

$$S_{n/2} \circ \cdots \circ S_2 \circ S_1 \circ P = F_n, \qquad (F_n)_{kj} = \omega^{jk}. \tag{1}$$

**One inverse stage.** Fix $h$, and let $I_h$ be the map of lines L5 to L9 for this $h$. Line L9 reads $V[k \cdot n/(2h)] = \omega^{-kn/(2h)} = W_h^{-k}$, which exists since $\omega$ is a unit ($\omega \cdot \omega^{n-1} = 1$). Lines L7 to L9 read the two cells of one pair and write only those two cells, and different $(s, k)$ touch disjoint pairs, so $I_h$ acts on each pair separately, by $(a, b) \mapsto (a + b,\ W_h^{-k}(a - b))$. It is $R$-linear. For the pair $(a, b) = (u + W_h^k v,\ u - W_h^k v)$ produced by $S_h$,

$$a + b = 2u, \qquad W_h^{-k}(a - b) = W_h^{-k} \cdot 2 W_h^k v = 2v.$$

Hence

$$I_h \circ S_h = 2 \cdot \mathrm{id}. \tag{2}$$

**The whole loop.** Line L3 sets $h = n/2$, line L10 halves $h$, and line L4 stops when $h < 1$. So the loop runs $I_{n/2}$ first and $I_1$ last, $t$ stages in all (none when $n = 1$). Lines L11 and L12 swap $j$ and $\mathrm{rev}_t(j)$ once for each pair $j < \mathrm{rev}_t(j)$ and leave the fixed points alone; since $\mathrm{rev}_t$ is an involution, this applies $P$, and $P \circ P = \mathrm{id}$. Write $G = P \circ I_1 \circ I_2 \circ \cdots \circ I_{n/2}$ for the map of lines L3 to L12. By (1) and then (2) applied $t$ times from the inside out, using that $2 \cdot \mathrm{id}$ commutes with every linear map,

$$G \circ F_n = P \circ I_1 \circ \cdots \circ I_{n/2} \circ S_{n/2} \circ \cdots \circ S_1 \circ P = 2^t \cdot P \circ P = n \cdot \mathrm{id}.$$

**Conclusion.** Since $n$ is a unit and $\omega$ is principal, $F_n$ is invertible with inverse $\frac{1}{n}(\omega^{-jk})_{j,k}$; this is the inverse formula, proved on the DFT page from $\sum_k \omega^{rk} = 0$ for $1 \le r \le n - 1$. Multiplying $G \circ F_n = n \cdot \mathrm{id}$ on the right by $F_n^{-1}$ gives $G = n F_n^{-1}$. So after line L12 the array holds $n F_n^{-1} X = n x$, and line L13 multiplies by $n^{-1}$, leaving $x$. Uniqueness of $x$ is the injectivity of $F_n$. Without line L13 the array holds $n x$. Since $n F_n^{-1} = (\omega^{-jk})_{j,k}$, this is the unnormalized inverse $X \mapsto (\sum_k X_k \omega^{-jk})_j$.

**Operation count.** In the stage with half length $h$ there are $n/(2h)$ blocks with $h$ butterflies each, so $n/2$ butterflies. Each does one addition (line L8), one subtraction and one multiplication (line L9). Over $t = \lg n$ stages this is $n \lg n$ additions and subtractions and $\frac{n}{2}\lg n$ multiplications, for every input. Line L13 adds $n$ multiplications. Line L2 needs at most $n/2$ multiplications for the powers of $\omega^{-1}$, once per length. The loops of lines L4 to L12 take $O(n \log n)$ index steps, so the time is $\Theta(n \log n)$ for every input. The table $V$ and the table of reversed indices take $\Theta(n)$ space, and the transform itself writes only into $X$. $\blacksquare$
