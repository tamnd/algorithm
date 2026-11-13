---
title: The swap test accepts with probability (1 + Tr(rho sigma))/2, and the estimate is within epsilon
proves: [correctness]
status: full
---

We write $A$ and $B$ for the two registers of $n$ qubits and $c$ for the ancilla. The swap operator $S$ on $A \otimes B$ is the linear map with $S(|x\rangle \otimes |y\rangle) = |y\rangle \otimes |x\rangle$ for all basis states $|x\rangle, |y\rangle$ of $n$ qubits. It is Hermitian and $S^2 = I$.

**Lemma 1 (the controlled swaps).** Lines L2 to L4 apply the unitary $W = (H \otimes I)\,C_S\,(H \otimes I)$, where $C_S = |0\rangle\langle 0| \otimes I + |1\rangle\langle 1| \otimes S$ is the swap of $A$ and $B$ controlled by $c$.

*Proof.* Let $S_j$ swap qubit $j$ of $A$ with qubit $j$ of $B$. The $S_j$ act on disjoint pairs of qubits, so they commute, and their product exchanges every qubit of $A$ with the qubit of $B$ at the same position, so $S_0 S_1 \cdots S_{n-1} = S$. The controlled forms multiply as $\prod_j \bigl(|0\rangle\langle0| \otimes I + |1\rangle\langle1| \otimes S_j\bigr) = |0\rangle\langle 0| \otimes I + |1\rangle\langle 1| \otimes \prod_j S_j$, because $|0\rangle\langle0|$ and $|1\rangle\langle1|$ are orthogonal projectors with sum $I$. So the loop of line L3 applies $C_S$, and lines L2 and L4 apply $H$ to $c$ before and after it. $\square$

**Lemma 2 (the two branches).** For every state $|\chi\rangle$ of $A \otimes B$,

$$W\bigl(|0\rangle \otimes |\chi\rangle\bigr) = |0\rangle \otimes P_+|\chi\rangle + |1\rangle \otimes P_-|\chi\rangle, \qquad P_\pm = \tfrac12(I \pm S).$$

*Proof.* $H|0\rangle = (|0\rangle + |1\rangle)/\sqrt2$, so after line L2 the state is $(|0\rangle|\chi\rangle + |1\rangle|\chi\rangle)/\sqrt2$. By Lemma 1, line L3 gives $(|0\rangle|\chi\rangle + |1\rangle S|\chi\rangle)/\sqrt2$. Line L4 maps $|0\rangle$ to $(|0\rangle + |1\rangle)/\sqrt2$ and $|1\rangle$ to $(|0\rangle - |1\rangle)/\sqrt2$, so the state becomes $\frac12|0\rangle(|\chi\rangle + S|\chi\rangle) + \frac12|1\rangle(|\chi\rangle - S|\chi\rangle)$. $\square$

Since $S$ is Hermitian with $S^2 = I$, both $P_+$ and $P_-$ are Hermitian and $P_\pm^2 = \frac14(I \pm 2S + S^2) = P_\pm$. So they are the orthogonal projectors onto the symmetric and the antisymmetric subspaces, and $P_+ + P_- = I$.

**Theorem 1 (the acceptance probability).** If register $A$ holds the density matrix $\rho$ and register $B$ holds $\sigma$, line L5 returns 0 with probability $\frac12\bigl(1 + \operatorname{Tr}(\rho\sigma)\bigr)$. For pure states $\rho = |\psi\rangle\langle\psi|$ and $\sigma = |\phi\rangle\langle\phi|$ this is $\frac12\bigl(1 + |\langle\psi|\phi\rangle|^2\bigr)$.

*Proof.* First let the input of $A \otimes B$ be a pure state $|\chi\rangle$. By Lemma 2 and the [Born rule](/born-rule/), outcome 0 has probability $\|P_+|\chi\rangle\|^2 = \langle\chi|P_+^\dagger P_+|\chi\rangle = \langle\chi|P_+|\chi\rangle$. Every density matrix $\tau$ of $A \otimes B$ is a mixture $\sum_m q_m |\chi_m\rangle\langle\chi_m|$ of pure states, and the probability of an outcome is the same mixture of the probabilities, so outcome 0 has probability $\operatorname{Tr}(P_+\tau)$. For $\tau = \rho \otimes \sigma$,

$$\operatorname{Tr}(P_+(\rho \otimes \sigma)) = \tfrac12\operatorname{Tr}(\rho)\operatorname{Tr}(\sigma) + \tfrac12\operatorname{Tr}(S(\rho \otimes \sigma)) = \tfrac12 + \tfrac12\operatorname{Tr}(S(\rho\otimes\sigma)).$$

Write $S = \sum_{i,j} |i\rangle\langle j| \otimes |j\rangle\langle i|$, which maps $|j\rangle|i\rangle$ to $|i\rangle|j\rangle$. Then $\operatorname{Tr}(S(\rho \otimes \sigma)) = \sum_{i,j} \operatorname{Tr}(|i\rangle\langle j|\rho)\operatorname{Tr}(|j\rangle\langle i|\sigma) = \sum_{i,j} \langle j|\rho|i\rangle\langle i|\sigma|j\rangle = \operatorname{Tr}(\rho\sigma)$. For pure states, $\operatorname{Tr}(|\psi\rangle\langle\psi|\phi\rangle\langle\phi|) = \langle\psi|\phi\rangle\langle\phi|\psi\rangle = |\langle\psi|\phi\rangle|^2$. $\square$

**Corollary.** If $|\psi\rangle = |\phi\rangle$ up to a global phase, the test returns 0 with probability 1. If $\rho$ and $\sigma$ have orthogonal supports, it returns 0 with probability exactly $\frac12$. In all cases the probability of 0 is between $\frac12$ and 1, because $0 \le \operatorname{Tr}(\rho\sigma) \le 1$.

**Theorem 2 (the estimate).** Let $x = \operatorname{Tr}(\rho\sigma)$, and let ESTIMATE-OVERLAP use $N = \lceil 2\ln(2/\delta)/\varepsilon^2 \rceil$ runs, each on a fresh copy of $\rho$ and a fresh copy of $\sigma$. Then the output $\hat x = \max(0, 2k/N - 1)$ satisfies $|\hat x - x| < \varepsilon$ with probability at least $1 - \delta$.

*Proof.* The copies are fresh and independent, so by Theorem 1 the $N$ outcomes are independent, and each is 0 with probability $p = (1 + x)/2$. Let $Y_r = 1$ if run $r$ returns 0 and $Y_r = 0$ otherwise, so $k = \sum_r Y_r$, each $Y_r \in [0, 1]$, and $\mathbb{E}[k/N] = p$. The [Hoeffding inequality](/hoeffding-inequality/) gives

$$\Pr\Bigl[\Bigl|\frac kN - p\Bigr| \ge \frac\varepsilon2\Bigr] \le 2\exp\Bigl(-2N\frac{\varepsilon^2}{4}\Bigr) = 2e^{-N\varepsilon^2/2} \le 2e^{-\ln(2/\delta)} = \delta,$$

where the last step uses $N \ge 2\ln(2/\delta)/\varepsilon^2$. Outside this event, $|(2k/N - 1) - x| = 2|k/N - p| < \varepsilon$. Finally $x \ge 0$, so replacing a negative value by 0 does not increase the distance to $x$: if $2k/N - 1 < 0 \le x$, then $|0 - x| \le |(2k/N - 1) - x|$. $\blacksquare$
