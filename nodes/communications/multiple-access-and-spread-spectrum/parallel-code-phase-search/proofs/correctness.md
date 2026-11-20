---
title: Parallel code phase search computes every cell of the search grid and returns the largest
proves: [correctness]
status: full
---

The input is a block $x \in \mathbb{C}^N$, a code $c \in \mathbb{C}^N$ and carrier offsets $\nu_1, \ldots, \nu_F$ in cycles per block. For each cell $(i, t)$ of the grid, the target value is the correlation
$$S_i[t] = \sum_{n=0}^{N-1} x[n]\, e^{-j 2\pi \nu_i n / N}\, \overline{c[(n - t) \bmod N]}.$$
Write $W_N = e^{-j 2\pi / N}$, $\mathcal{F}$ for the DFT, $(\mathcal{F} u)[k] = \sum_n u[n] W_N^{kn}$, and $\mathcal{F}^{-1}$ for its inverse, $(\mathcal{F}^{-1} U)[n] = \frac{1}{N} \sum_k U[k] W_N^{-kn}$. All indices are taken modulo $N$.

**Lemma 1 (the FFT computes the DFT).** For every $N \ge 1$, `fft` returns $\mathcal{F} x$, and `ifft` returns $\mathcal{F}^{-1} X$.

*Proof.* By strong induction on $N$. For $N = 1$ both sides are $x[0]$. If $N$ is prime, the routine evaluates the defining sum directly. Otherwise let $p$ be the smallest prime factor and $N = p m$ with $m < N$. Split the index as $n = p s + r$ with $0 \le r < p$ and $0 \le s < m$. Then
$$(\mathcal{F} x)[k] = \sum_{r=0}^{p-1} W_N^{r k} \sum_{s=0}^{m-1} x[p s + r]\, W_N^{p s k} = \sum_{r=0}^{p-1} W_N^{r k}\, F_r[k \bmod m],$$
because $W_N^{p s k} = W_m^{s k}$, which depends on $k$ only modulo $m$. Here $F_r$ is the DFT of length $m$ of the part $x[r], x[r + p], \ldots$, which the recursive call computes correctly by the induction hypothesis. The routine evaluates exactly the right-hand side. For the inverse, $\overline{\mathcal{F} \overline{X}}[n] = \sum_k X[k] W_N^{-kn}$, and dividing by $N$ gives $\mathcal{F}^{-1} X$. $\square$

**Lemma 2 (correlation theorem).** For $y, c \in \mathbb{C}^N$, let $\rho[t] = \sum_n y[n]\, \overline{c[n - t]}$. Then $\mathcal{F} \rho = (\mathcal{F} y) \cdot \overline{\mathcal{F} c}$, so $\rho = \mathcal{F}^{-1}\big((\mathcal{F} y) \cdot \overline{\mathcal{F} c}\big)$.

*Proof.*
$$(\mathcal{F} \rho)[k] = \sum_t \sum_n y[n]\, \overline{c[n - t]}\, W_N^{k t} = \sum_n y[n] W_N^{k n} \sum_t \overline{c[n - t]\, W_N^{k (n - t)}},$$
since $\overline{W_N^{a}} = W_N^{-a}$ gives $W_N^{kt} = W_N^{kn}\, \overline{W_N^{k(n-t)}}$. As $t$ runs over all residues, so does $n - t$, so the inner sum is $\overline{(\mathcal{F} c)[k]}$ for every $n$. $\square$

**Lemma 3 (each row is a full correlation).** For each $i$, the row computed in L3 and L4 equals $S_i$.

*Proof.* L1 stores $C = \overline{\mathcal{F} c}$, once. L3 forms $y[n] = x[n] e^{-j 2\pi \nu_i n / N}$. L4 computes $\mathcal{F}^{-1}((\mathcal{F} y) \cdot C)$, which by Lemmas 1 and 2 is $\rho[t] = \sum_n y[n]\, \overline{c[n - t]} = S_i[t]$. $\square$

**Theorem.** The search returns a cell $(i, t)$ with $|S_i[t]|^2 = \max_{i', t'} |S_{i'}[t']|^2$, together with all the rows $S_i$.

*Proof.* By Lemma 3 the rows are the correct correlations. L5 picks in row $i$ a phase $t_i$ with the largest $|S_i[t]|$, and the running comparison keeps the row with the largest $|S_i[t_i]|^2$, with ties resolved by the first index. After the loop the kept cell has the largest value over all rows, and L6 returns it. $\square$

**Proposition (loss from a carrier error).** Let $x[n] = A\, e^{j 2\pi \nu n / N}\, c[(n - \tau) \bmod N]$ with $|c[n]|^2 = 1/N$ for all $n$, and let $\delta = \nu - \nu_i$. Then
$$|S_i[\tau]| = |A|\, D_N(\delta), \qquad D_N(\delta) = \left|\frac{\sin(\pi \delta)}{N \sin(\pi \delta / N)}\right|,$$
with $D_N(0) = 1$. As $N \to \infty$, $D_N(\delta) \to |\sin(\pi\delta)/(\pi\delta)|$.

*Proof.* At $t = \tau$, each term is $A\, e^{j 2\pi \delta n / N}\, |c[(n - \tau) \bmod N]|^2 = (A/N)\, e^{j 2\pi \delta n / N}$. The sum of the geometric series is $\frac{A}{N} \frac{1 - e^{j 2\pi \delta}}{1 - e^{j 2\pi \delta / N}}$ for $\delta / N \notin \mathbb{Z}$, and $|1 - e^{j\theta}| = 2 |\sin(\theta/2)|$ gives the formula. For the limit, $N \sin(\pi\delta/N) \to \pi \delta$. $\square$

**Cost.** Let $N = p_1 p_2 \cdots p_k$ with primes $p_1 \le \cdots \le p_k$. The FFT does $O(N p_j)$ work at the level that splits off $p_j$, so its cost is $O(N (p_1 + \cdots + p_k))$, which is $O(N \log N)$ when the prime factors are bounded, for example when $N$ is a power of two. The search does one FFT of the code and, for each of the $F$ offsets, $N$ products in L3, two FFTs and $N$ products in L4, and $N$ comparisons in L5. With bounded prime factors the total is $O(F N \log N)$, against $\Theta(F N^2)$ for the direct sums. It stores $O(N)$ values per row, and $O(N)$ in all if the rows are not kept.
