---
title: The QFT circuit computes F_N, and the approximate QFT has error at most 2 pi n / 2^m
proves: [correctness]
status: full
---

We write $N = 2^n$, $e(t) = e^{2\pi i t}$ and $j = \sum_{l=0}^{n-1} j_l 2^l$, with qubit $l$ holding bit $j_l$. The target map is $F_N |j\rangle = N^{-1/2} \sum_k e(jk/N) |k\rangle$. For a real $t$ let $|\theta(t)\rangle = (|0\rangle + e(t)|1\rangle)/\sqrt{2}$. The gate $\mathrm{CR}_k$ on qubits $p, q$ is $\mathrm{diag}(1, 1, 1, e(1/2^k))$: it multiplies a basis state by $e(1/2^k)$ if both bits are $1$ and does nothing otherwise.

**Lemma 1 (product form).** $F_N |j\rangle = \bigotimes_{l=n-1}^{0} |\theta(t_l)\rangle$ with $t_l = (j \bmod 2^{n-l})/2^{n-l}$, where the factor of index $l$ is on qubit $l$.

*Proof.* Expand the product: the coefficient of $|k\rangle$ is $2^{-n/2} \prod_l e(k_l t_l) = N^{-1/2} e(\sum_l k_l t_l)$. Now $j 2^l / N = j/2^{n-l}$, and it differs from $t_l$ by the integer $\lfloor j/2^{n-l} \rfloor$. So $e(k_l t_l) = e(k_l j 2^l/N)$, and the product is $e(j \sum_l k_l 2^l / N) = e(jk/N)$. $\square$

**Lemma 2 (one gate).** Let qubit $p$ be in $|b\rangle$ with $b \in \{0, 1\}$ and qubit $q$ be in $|\theta(t)\rangle$. Then $\mathrm{CR}_k$ on $p, q$ gives $|b\rangle \otimes |\theta(t + b/2^k)\rangle$. Also $H|b\rangle = |\theta(b/2)\rangle$.

*Proof.* For $b = 0$ no basis state has both bits $1$. For $b = 1$ the gate multiplies the $|1\rangle$ part of qubit $q$ by $e(1/2^k)$. For $H$: $H|b\rangle = (|0\rangle + (-1)^b |1\rangle)/\sqrt{2}$ and $(-1)^b = e(b/2)$. $\square$

**Lemma 3 (invariant).** Run the gates of lines L2 to L6 with $m = n$ on $|j\rangle$. After the turn of qubit $q$ (the body of line L2 for this $q$), the state is a product state in which qubit $r$ is in $|\theta((j \bmod 2^{r+1})/2^{r+1})\rangle$ for each $r \ge q$, and qubit $p$ is in $|j_p\rangle$ for each $p < q$.

*Proof.* By induction on the turns, in the order $q = n-1, \ldots, 0$. Before the first turn, every qubit $p$ is in $|j_p\rangle$. Assume the claim before the turn of $q$: qubits $r > q$ hold their final phases and qubits $p \le q$ hold their bits. The gates of the turn act only on qubit $q$ and on qubits $p < q$, so the qubits $r > q$ do not change. Line L3 puts qubit $q$ in $|\theta(j_q/2)\rangle$ by Lemma 2. Each gate of line L6, with $k = q - p + 1$, keeps qubit $p$ in $|j_p\rangle$ and, by Lemma 2, adds $j_p / 2^{q-p+1} = j_p 2^p / 2^{q+1}$ to the phase of qubit $q$. After the gates for $p = q-1, \ldots, 0$, the phase of qubit $q$ is
$$\frac{j_q 2^q + \sum_{p<q} j_p 2^p}{2^{q+1}} = \frac{j \bmod 2^{q+1}}{2^{q+1}}.$$
The state stays a product state, because each gate maps a product of a basis state and a $|\theta\rangle$ state to a state of the same kind. $\square$

**Theorem.** The circuit returned by QFT-CIRCUIT$(n, n)$ is equal to $F_N$.

*Proof.* By Lemma 3 with $q = 0$, after line L6 qubit $r$ is in $|\theta(s_r)\rangle$ with $s_r = (j \bmod 2^{r+1})/2^{r+1}$ for each $r$. Lines L7 and L8 swap qubit $r$ with qubit $n - 1 - r$, so qubit $l$ ends in $|\theta(s_{n-1-l})\rangle$, and $s_{n-1-l} = (j \bmod 2^{n-l})/2^{n-l} = t_l$. By Lemma 1 this is $F_N|j\rangle$. Both sides are linear maps that agree on the basis, so they are equal. $\blacksquare$

**Lemma 4 (dropped gates).** Let $U = U_L \cdots U_1$ and $V = V_L \cdots V_1$ be products of unitaries. Then $\|U - V\| \le \sum_i \|U_i - V_i\|$.

*Proof.* Telescope: $U - V = \sum_{i=1}^{L} U_L \cdots U_{i+1} (U_i - V_i) V_{i-1} \cdots V_1$, and each product of unitaries has norm $1$. $\square$

**Corollary (approximate QFT).** Let $F_N^{(m)}$ be the circuit of QFT-CIRCUIT$(n, m)$ with $2 \le m \le n$. Then
$$\|F_N - F_N^{(m)}\| \le \sum_{k=m+1}^{n} (n-k+1) \cdot 2\sin(\pi/2^k) < \frac{2\pi(n-m)}{2^m}.$$

*Proof.* Compare the two circuits gate by gate, with the identity in place of each dropped gate. A kept gate contributes $0$ to Lemma 4. A dropped $\mathrm{CR}_k$ contributes $\|\mathrm{CR}_k - I\| = |e(1/2^k) - 1| = 2\sin(\pi/2^k)$. The gate $\mathrm{CR}_k$ appears once for each pair $p < q$ with $q - p = k - 1$, so for $q = k-1, \ldots, n-1$, which is $n - k + 1$ times. This gives the first bound. For the second, $\sin x < x$ for $x > 0$, so the sum is less than $2\pi \sum_{k>m} (n-m) 2^{-k} = 2\pi(n - m)/2^m$. $\square$

**The count.** Line L3 runs $n$ times. Line L6 appends a gate for each pair $p < q$, so $n(n-1)/2$ times when $m = n$, and $\sum_{k=2}^{m}(n - k + 1) = (m-1)n - m(m-1)/2$ times in general. Line L8 runs $\lfloor n/2 \rfloor$ times.
