---
title: The averaged qDRIFT channel is within (2 lambda^2 t^2/N) e^(2 lambda t/N) of the exact evolution in half the diamond norm
proves: [correctness]
status: full
---

We use the pseudocode of the page. $H = \sum_{j=1}^L c_jP_j$ with real $c_j \ne 0$ and Pauli strings $P_j$, $\lambda = \sum_j |c_j|$ (line L1), $p_j = |c_j|/\lambda$, $\tau = \lambda t/N$ (line L2), and $s_j = \mathrm{sign}(c_j)$. Superoperators are linear maps on $2^n \times 2^n$ matrices. For a superoperator $\Phi$, $\|\Phi\|_\diamond = \sup_{X \ne 0}\|(\Phi \otimes \mathrm{id})(X)\|_1/\|X\|_1$, where $\mathrm{id}$ acts on a reference system of the same dimension and $\|\cdot\|_1$ is the trace norm.

**Facts about the diamond norm.** (a) It is a norm, and $\|\Phi\Psi\|_\diamond \le \|\Phi\|_\diamond\|\Psi\|_\diamond$, since it is an induced norm of the maps $\Phi \otimes \mathrm{id}$. (b) Every channel (completely positive and trace preserving map) $\Phi$ has $\|\Phi\|_\diamond = 1$. (c) For a Hermitian $A$ with $\|A\| \le a$, the map $\mathcal{L}(X) = -i[A, X]$ has $\|\mathcal{L}\|_\diamond \le 2a$, because $(\mathcal{L} \otimes \mathrm{id})(X) = -i((A \otimes I)X - X(A \otimes I))$ and $\|BX\|_1 \le \|B\|\|X\|_1$, $\|XB\|_1 \le \|B\|\|X\|_1$.

**Step 1: the average of the random circuit is $\mathcal{E}_1^N$.** Let $U_j = e^{-i\tau s_jP_j}$, the rotation that line L6 appends for draw $j$, and $\mathcal{E}_1(\rho) = \sum_j p_jU_j\rho U_j^\dagger$. Line L5 draws $j_1, \ldots, j_N$ independently with $\Pr[j_m = j] = p_j$, and the circuit is $V = U_{j_N}\cdots U_{j_1}$. By induction on $m$, the average of $U_{j_m}\cdots U_{j_1}\rho\,U_{j_1}^\dagger\cdots U_{j_m}^\dagger$ is $\mathcal{E}_1^m(\rho)$: for $m = 1$ it is the definition, and for $m > 1$ the draw $j_m$ is independent of the earlier ones, so averaging over it first gives $\mathcal{E}_1$ applied to the earlier average. So $\mathbb{E}[V\rho V^\dagger] = \mathcal{E}_1^N(\rho)$ for every $\rho$, and the same holds for $V \otimes I$ on inputs entangled with a reference.

**Step 2: generators.** Let $\mathcal{L}_j(X) = -i[s_jP_j, X]$. Then $e^{\tau\mathcal{L}_j}(X) = U_jXU_j^\dagger$, so $\mathcal{E}_1 = \sum_j p_je^{\tau\mathcal{L}_j}$. Let $\mathcal{L}(X) = -i[H, X]$, so that the exact channel is $\mathcal{U} = e^{t\mathcal{L}}$. Since $\lambda p_js_j = |c_j|s_j = c_j$,
$$\frac{t}{N}\mathcal{L} = \frac{t}{N}\sum_j c_j(-i[P_j, \cdot\,]) = \tau\sum_j p_j\mathcal{L}_j.$$
So one exact step is $\mathcal{U}_1 = e^{\tau\mathcal{M}}$ with $\mathcal{M} = \sum_j p_j\mathcal{L}_j$, and $\mathcal{U} = \mathcal{U}_1^N$. By fact (c), $\|\mathcal{L}_j\|_\diamond \le 2$ (since $\|P_j\| = 1$), and by the triangle inequality $\|\mathcal{M}\|_\diamond \le \sum_j p_j \cdot 2 = 2$.

**Step 3: one step.** Both maps are given by convergent power series:
$$\mathcal{E}_1 = \sum_{m \ge 0}\frac{\tau^m}{m!}\sum_j p_j\mathcal{L}_j^m, \qquad \mathcal{U}_1 = \sum_{m \ge 0}\frac{\tau^m}{m!}\mathcal{M}^m.$$
For $m = 0$ both terms are $\mathrm{id}$ (the $p_j$ add up to 1), and for $m = 1$ both are $\tau\mathcal{M}$. For $m \ge 2$, by facts (a) and (c), $\|\sum_jp_j\mathcal{L}_j^m\|_\diamond \le 2^m$ and $\|\mathcal{M}^m\|_\diamond \le 2^m$. Hence
$$\|\mathcal{E}_1 - \mathcal{U}_1\|_\diamond \le \sum_{m \ge 2}\frac{2 \cdot (2\tau)^m}{m!} = 2\big(e^{2\tau} - 1 - 2\tau\big) \le 2 \cdot \frac{(2\tau)^2}{2}e^{2\tau} = 4\tau^2e^{2\tau},$$
using $e^x - 1 - x = \sum_{m \ge 2}x^m/m! \le (x^2/2)\sum_{m \ge 0}x^m/m! = (x^2/2)e^x$ for $x \ge 0$, since $m! \ge 2(m-2)!$.

**Step 4: $N$ steps.** Telescoping,
$$\mathcal{E}_1^N - \mathcal{U}_1^N = \sum_{m=0}^{N-1}\mathcal{E}_1^{N-1-m}(\mathcal{E}_1 - \mathcal{U}_1)\,\mathcal{U}_1^{m}.$$
Both $\mathcal{E}_1$ and $\mathcal{U}_1$ are channels, so their powers have diamond norm 1 by fact (b), and by fact (a)
$$\|\mathcal{E}_1^N - \mathcal{U}\|_\diamond \le N \cdot 4\tau^2e^{2\tau} = \frac{4\lambda^2t^2}{N}e^{2\lambda t/N}.$$
Half of this is $(2\lambda^2t^2/N)e^{2\lambda t/N}$, the bound of the page.

**Step 5: the choice of $N$.** If $N \ge 2\lambda^2t^2/\epsilon$, the bound is at most $\epsilon e^{2\lambda t/N}$, and $e^{2\lambda t/N} \to 1$ as $N$ grows; the least $N$ with $(2\lambda^2t^2/N)e^{2\lambda t/N} \le \epsilon$ exists because the left side decreases to 0 in $N$. For $N \ge 2\lambda^2t^2/\epsilon$ and $\epsilon \le 1$, $2\lambda t/N \le \epsilon/(\lambda t)$, so the factor is $1 + O(\epsilon/(\lambda t))$ whenever $\lambda t \ge 1$. Then the cost is $N = O(\lambda^2t^2/\epsilon)$ and does not depend on $L$.

**Consequence for measurements.** For a density matrix $\rho$ and an observable $O$ with $\|O\| \le 1$, $|\mathrm{Tr}(O\,\mathcal{E}_1^N(\rho)) - \mathrm{Tr}(O\,\mathcal{U}(\rho))| \le \|\mathcal{E}_1^N(\rho) - \mathcal{U}(\rho)\|_1 \le \|\mathcal{E}_1^N - \mathcal{U}\|_\diamond \le 2\epsilon$. By Step 1 the left side is the bias of the average of the measured values over independent runs, each with a fresh draw. $\blacksquare$
