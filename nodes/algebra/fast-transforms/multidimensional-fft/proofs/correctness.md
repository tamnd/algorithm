---
title: MULTIDIM-FFT computes the d-dimensional DFT with N lg N additions and (N/2) lg N multiplications
proves: [correctness, complexity]
status: full
---

**Statement.** Let $R$ be a commutative ring, $d \ge 1$, and $n_1, \ldots, n_d$ powers of two with product $N$. For each axis $a$ let $\omega_a \in R$ satisfy $\omega_a^{n_a} = 1$ and, when $n_a \ge 2$, $\omega_a^{n_a/2} = -1$ (over $\mathbb{C}$ with $\omega_a = e^{-2\pi i/n_a}$ both hold). For every array $x$ stored in row-major order, MULTIDIM-FFT ends with the array

$$X_{k_1, \ldots, k_d} = \sum_{j_1 = 0}^{n_1 - 1} \cdots \sum_{j_d = 0}^{n_d - 1} x_{j_1, \ldots, j_d}\, \omega_1^{j_1 k_1} \cdots \omega_d^{j_d k_d}$$

in the same layout. Lines L5 to L8 do exactly $N \lg N$ additions and subtractions and $\frac{N}{2} \lg N$ multiplications in $R$, the tables of line L4 do at most $\sum_a n_a/2$ more, and the extra space is $\Theta(m)$ with $m = \max_a n_a$.

**Lemma 1 (the lines partition the array).** Fix an axis $a$ and write $\sigma = \sigma_a = n_{a+1} \cdots n_d$. Every position $t$ with $0 \le t < N$ has a unique expression $t = q \cdot n_a \sigma + i \sigma + r$ with $0 \le q < N / (n_a \sigma)$, $0 \le i < n_a$ and $0 \le r < \sigma$: this is division of $t$ by $n_a \sigma$ with remainder, followed by division of the remainder by $\sigma$. So the lines $\{s + i\sigma : 0 \le i < n_a\}$ for the starts $s = q \cdot n_a \sigma + r$ of line L5 are disjoint and cover all $N$ positions. In row-major order the position $t$ holds the entry with indices $(j_1, \ldots, j_d)$ where $t = \sum_b j_b \sigma_b$; the mixed-radix digits of $t$ are exactly these indices, so on one line the indices $j_b$ with $b \ne a$ are fixed (they are the digits of $q$ and $r$) and $j_a = i$ runs over $0, \ldots, n_a - 1$. $\square$

**Lemma 2 (one line).** Let $n = 2^t$ and $\omega \in R$ with $\omega^n = 1$ and $\omega^{n/2} = -1$ when $n \ge 2$. The call FFT$(\ell, W)$ of line L7, with $W[k] = \omega^k$, replaces $\ell$ by $L_k = \sum_{i} \ell_i \omega^{ik}$, with $n \lg n$ additions and subtractions and $\frac{n}{2} \lg n$ multiplications. *Proof.* By induction on $t$. For $t = 0$ there is nothing to do and $L_0 = \ell_0$. For $t \ge 1$ write $E_k$ and $O_k$ for the DFTs, with root $\omega^2$, of the even and odd entries; $\omega^2$ satisfies the hypothesis for $n/2$, since $(\omega^2)^{n/4} = \omega^{n/2} = -1$ when $n \ge 4$. Splitting the sum by the parity of $i$ gives $L_k = E_k + \omega^k O_k$ for $0 \le k < n/2$, and since $E$ and $O$ have period $n/2$ and $\omega^{k + n/2} = -\omega^k$, also $L_{k + n/2} = E_k - \omega^k O_k$. The iterative radix-2 code computes exactly these butterflies after the bit-reversal permutation, stage by stage; this is the standard decimation-in-time FFT, proved in full on the page of the [iterative FFT](/iterative-fft/). Each of the $\lg n$ stages does $n/2$ butterflies of one multiplication, one addition and one subtraction, which gives the counts. $\square$

**Invariant.** Write $X^{(a)}$ for the array after the passes $1, \ldots, a$ of the loop at line L2. We prove by induction on $a$ that

$$X^{(a)}_{k_1, \ldots, k_a, j_{a+1}, \ldots, j_d} = \sum_{j_1, \ldots, j_a} x_{j_1, \ldots, j_d}\, \omega_1^{j_1 k_1} \cdots \omega_a^{j_a k_a}. \tag{1}$$

*Base.* For $a = 0$ the empty sum and product leave $X^{(0)} = x$, which is the array before the loop.

*Step.* Suppose (1) holds for $a - 1$. In pass $a$, line L5 visits each start once, line L6 copies the line into the buffer, line L7 transforms it, and line L8 writes it back to the same positions. By Lemma 1 the lines are disjoint, so the write of one line never changes an entry read by another line in the same pass, and every entry belongs to exactly one line. Fix the indices $b \ne a$; on that line the entry with $j_a = i$ is $X^{(a-1)}$ at $(k_1, \ldots, k_{a-1}, i, j_{a+1}, \ldots, j_d)$. By Lemma 2 the entry written back at $j_a = k_a$ is

$$\sum_{i=0}^{n_a - 1} X^{(a-1)}_{k_1, \ldots, k_{a-1}, i, j_{a+1}, \ldots, j_d}\, \omega_a^{i k_a} = \sum_{i} \sum_{j_1, \ldots, j_{a-1}} x_{j_1, \ldots, j_{a-1}, i, j_{a+1}, \ldots, j_d}\, \omega_1^{j_1 k_1} \cdots \omega_{a-1}^{j_{a-1} k_{a-1}}\, \omega_a^{i k_a},$$

using (1) for $a - 1$. Renaming $i$ as $j_a$ and using that finite sums in a commutative ring can be reordered, this is the right side of (1) for $a$.

*End.* For $a = d$, (1) is the definition of $X$, which proves correctness.

**Operation count.** In pass $a$ there are $N / n_a$ lines by Lemma 1, each costing $n_a \lg n_a$ additions and $\frac{n_a}{2} \lg n_a$ multiplications by Lemma 2, so the pass costs $N \lg n_a$ additions and $\frac{N}{2} \lg n_a$ multiplications. Since $N = \prod_a n_a$, we have $\sum_a \lg n_a = \lg N$, and summing over $a$ gives $N \lg N$ additions and $\frac{N}{2} \lg N$ multiplications. Line L4 builds $n_a / 2$ table entries; taken as successive powers, each costs at most one multiplication, so the tables add at most $\sum_a n_a / 2 \le d m / 2$ multiplications. (The Python code instead evaluates each entry directly, by modular powering or from its exact angle over $\mathbb{C}$, which is more accurate in floating point and does not change the asymptotic cost.) Lines L6 and L8 move $N$ entries per pass and do no ring operations.

**Space.** Apart from the array, the pass for axis $a$ holds the buffer $\ell$ of $n_a$ entries, the table $W$ of $n_a / 2$ entries and $O(1)$ indices, and both are released before the next pass. The extra space is therefore at most $\frac{3}{2} m + O(1)$ entries, and at least $m$ for the buffer of the longest axis, so it is $\Theta(m)$. $\blacksquare$
