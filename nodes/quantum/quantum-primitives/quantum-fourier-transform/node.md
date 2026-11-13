---
tag: 9X30GG
kind: algorithm
slug: quantum-fourier-transform
name: Quantum Fourier transform
aliases:
- QFT
area: quantum/quantum-primitives
level: core
summary: The Fourier transform of the 2^n amplitudes of an n-qubit state, with n Hadamard gates, n(n-1)/2 controlled phase gates and floor(n/2) swaps. The output cannot be read out, only sampled.
model: quantum-circuit-model
complexity:
  vars: {n: the number of qubits}
  gates: {worst: Θ(n^2)}
  qubits: {worst: n}
  depth: {worst: 2n}
  time: {worst: Θ(n^2)}
properties: {exact: true, randomized: false, recursive: false}
history:
  year: 1994
  people: [Don Coppersmith, Peter Shor]
  note: Coppersmith gave the circuit of Hadamard and controlled phase gates and its approximate form in 1994, for the Fourier transform modulo a power of 2 in Shor's factoring algorithm.
prereqs: [discrete-fourier-transform, quantum-state, hadamard-gate, phase-and-t-gates, quantum-circuit-model, unitary-operator]
see_also: [dft-matrix, fast-fourier-transform, bit-reversal-permutation, butterfly-operation, walsh-hadamard-transform, quantum-phase-estimation, fourier-sampling, shor-algorithm]
sources:
  - url: https://arxiv.org/abs/quant-ph/0201067
    title: "Don Coppersmith, An approximate Fourier transform useful in quantum factoring, IBM Research Report RC 19642, 1994, arXiv:quant-ph/0201067"
    locator: the circuit of Hadamard and controlled phase gates for the Fourier transform modulo 2^n, and the approximate transform that drops the small rotations
  - paper: doi:10.1137/S0097539795293172
    title: "Peter W. Shor, Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer, SIAM Journal on Computing 26(5):1484-1509, 1997"
    locator: the section on the quantum Fourier transform modulo a power of 2
  - paper: doi:10.1103/PhysRevA.54.139
    title: "Adriano Barenco, Artur Ekert, Kalle-Antti Suominen and Päivi Törmä, Approximate quantum Fourier transform and decoherence, Physical Review A 54(1):139-146, 1996"
    locator: the error of the approximate QFT and its behaviour under decoherence
  - paper: doi:10.1103/PhysRevLett.76.3228
    title: "Robert B. Griffiths and Chi-Sheng Niu, Semiclassical Fourier transform for quantum computation, Physical Review Letters 76(17):3228-3231, 1996"
    locator: the QFT followed by measurement with one-qubit gates and classical control only
  - url: https://arxiv.org/abs/quant-ph/9511026
    title: "A. Yu. Kitaev, Quantum measurements and the Abelian Stabilizer Problem, arXiv:quant-ph/9511026, 1995"
    locator: the quantum Fourier transform for an arbitrary finite abelian group
  - url: https://arxiv.org/abs/quant-ph/0006004
    title: "Richard Cleve and John Watrous, Fast parallel circuits for the quantum Fourier transform, arXiv:quant-ph/0006004, 2000"
    locator: approximate QFT circuits of depth O(log n + log log(1/ε))
  - book: isbn:9781107002173
    title: Michael A. Nielsen and Isaac L. Chuang, Quantum Computation and Quantum Information, 10th anniversary edition, Cambridge University Press, 2010
    locator: Section 5.1 (the quantum Fourier transform, its product form and its circuit)
  - url: https://arxiv.org/abs/1907.09415
    title: Ronald de Wolf, Quantum Computing, Lecture Notes, arXiv:1907.09415, version 6 (2026)
    locator: Chapter 4 (the Fourier transform, the QFT circuit and its inverse)
---

The quantum Fourier transform (QFT) on $n$ qubits is the unitary map $F_N |j\rangle = N^{-1/2} \sum_{k=0}^{N-1} e^{2\pi i jk/N} |k\rangle$ with $N = 2^n$. It applies the [discrete Fourier transform](/discrete-fourier-transform/) to the $N$ amplitudes of the state. The circuit below uses $n$ [Hadamard gates](/hadamard-gate/), $n(n-1)/2$ controlled phase gates and $\lfloor n/2 \rfloor$ swaps, so $\Theta(n^2)$ gates, against $\Theta(N \log N) = \Theta(n 2^n)$ operations for the [fast Fourier transform](/fast-fourier-transform/) of a vector of length $N$. The comparison is not fair: the result is a quantum state, and one measurement gives only one index $k$, with probability equal to the squared modulus of the $k$-th Fourier coefficient. The QFT is the step that turns a periodic state into peaks that a measurement can find. It is the core of [quantum phase estimation](/quantum-phase-estimation/), of [Fourier sampling](/fourier-sampling/) and of [Shor's algorithm](/shor-algorithm/). If the rotations by angles below about $\varepsilon/n$ are dropped, the approximate QFT uses $O(n \log(n/\varepsilon))$ gates and has error at most $\varepsilon$ in operator norm.

## In plain words

A register of qubits holds a long list of numbers, one for each string of bits. The Fourier transform rewrites such a list as a mix of waves that repeat at different speeds. A classical computer must touch each entry of the list to do this. A quantum computer does it to the whole list at once, with a number of gates near the square of the number of qubits.

The catch is that you cannot read the new list. A measurement gives you one wave speed, picked at random, and the strong waves come up more often. That is enough when the list repeats with a fixed period, because then only a few speeds are strong, and each sample tells you a lot about the period.

## The problem

The input is an $n$-qubit state $\sum_{j=0}^{N-1} x_j |j\rangle$, and the output is the state $\sum_{k=0}^{N-1} y_k |k\rangle$ with

$$y_k = \frac{1}{\sqrt{N}} \sum_{j=0}^{N-1} x_j \, \omega^{jk}, \qquad \omega = e^{2\pi i/N}, \quad N = 2^n.$$

We use the qubit order of [quantum state](/quantum-state/): qubit $l$ holds bit $j_l$ of $j = \sum_l j_l 2^l$, qubit $0$ is the least significant bit and the rightmost symbol in a ket.

**Sign.** The [DFT matrix](/dft-matrix/) of the pages on fast transforms uses $e^{-2\pi i/N}$. The QFT uses $e^{+2\pi i/N}$, as most quantum texts do. So $F_N$ is $N^{-1/2}$ times the complex conjugate of that matrix, which is $\sqrt{N}$ times the matrix of the [inverse DFT](/inverse-discrete-fourier-transform/). Both are unitary, and the inverse QFT uses $e^{-2\pi i/N}$.

**Product form.** Write $e(t) = e^{2\pi i t}$. Since $jk/N = \sum_l k_l \, j 2^l / N$ and $e(j 2^l/N)$ depends only on $j \bmod 2^{n-l}$,

$$F_N |j\rangle = \bigotimes_{l=n-1}^{0} \frac{|0\rangle + e\big(\tfrac{j \bmod 2^{n-l}}{2^{n-l}}\big) |1\rangle}{\sqrt{2}}.$$

So the QFT of a basis state is a product state. Output qubit $l$ holds the phase $(j \bmod 2^{n-l})/2^{n-l}$: qubit $n-1$ holds $j_0/2$, and qubit $0$ holds $j/N$.

## The algorithm

The gates are $H$, the swap, and the controlled phase gate $\mathrm{CR}_k = \mathrm{diag}(1, 1, 1, e(1/2^k))$ on two qubits. $\mathrm{CR}_k$ adds the phase $1/2^k$ when both qubits are $1$. It is symmetric in its two qubits, and it is the controlled form of the phase gate $R_\varphi$ with $\varphi = 2\pi/2^k$ (see [phase and T gates](/phase-and-t-gates/)). The parameter $m$ gives the approximate QFT; $m = n$ gives the exact one.

```pseudo id=main
QFT-CIRCUIT(n, m)                          ▷ m = n gives the exact QFT
L1  G ← empty list of gates
L2  for q ← n-1 downto 0
L3      append H on qubit q to G
L4      for p ← q-1 downto 0
L5          k ← q - p + 1
L6          if k ≤ m then append CR_k on qubits p, q to G
L7  for q ← 0 to ⌊n/2⌋ - 1
L8      append SWAP on qubits q, n-1-q to G
L9  return G                               ▷ apply the gates in list order
```

On $|j\rangle$, the loop of line L2 treats the qubits from the top. When it reaches qubit $q$, that qubit and all qubits $p < q$ still hold their bits $j_q$ and $j_p$. Line L3 gives qubit $q$ the phase $j_q/2$, and each gate of line L6 adds $j_p 2^p/2^{q+1}$. After its turn, qubit $q$ holds the phase $(j \bmod 2^{q+1})/2^{q+1}$, which is the phase that the product form puts on qubit $n - 1 - q$. Lines L7 and L8 reverse the order of the qubits. This reversal is the [bit-reversal permutation](/bit-reversal-permutation/), as in an iterative FFT. The inverse QFT is the list in reverse order with $\mathrm{CR}_k$ replaced by $\mathrm{CR}_k^\dagger = \mathrm{diag}(1, 1, 1, e(-1/2^k))$.

## Example

Take $n = 3$ and $j = 5 = 101_2$, so $j_2 = 1$, $j_1 = 0$ and $j_0 = 1$. The circuit is $H_2$, $\mathrm{CR}_2(1, 2)$, $\mathrm{CR}_3(0, 2)$, $H_1$, $\mathrm{CR}_2(0, 1)$, $H_0$ and $\mathrm{SWAP}(0, 2)$, so $7$ gates.

| step | gates | phase on the qubit |
|---|---|---|
| $q = 2$ | $H_2$ gives $j_2/2 = 1/2$; $\mathrm{CR}_2(1,2)$ adds $0$ since $j_1 = 0$; $\mathrm{CR}_3(0,2)$ adds $1/8$ | qubit 2: $5/8$ |
| $q = 1$ | $H_1$ gives $0$; $\mathrm{CR}_2(0,1)$ adds $1/4$ | qubit 1: $1/4$ |
| $q = 0$ | $H_0$ gives $1/2$ | qubit 0: $1/2$ |
| swap | qubits 0 and 2 change places | qubit 2: $1/2$, qubit 1: $1/4$, qubit 0: $5/8$ |

This matches the product form: qubit $l$ holds $(5 \bmod 2^{3-l})/2^{3-l}$, which is $1/2$, $1/4$ and $5/8$ for $l = 2, 1, 0$. The amplitude of $|k\rangle$ is $e(5k/8)/\sqrt{8}$, and the simulator in the implementation gives, for $k = 0, \ldots, 7$, the values $0.3536$, $-0.25 - 0.25i$, $0.3536i$, $0.25 - 0.25i$, $-0.3536$, $0.25 + 0.25i$, $-0.3536i$ and $-0.25 + 0.25i$. All have modulus $1/\sqrt{8}$, so a measurement gives a uniform $k$.

A periodic input shows why the transform is useful. The state $(|1\rangle + |5\rangle)/\sqrt{2}$ has period $r = 4$ and offset $1$. Its QFT has $y_k = e(k/8)(1 + (-1)^k)/4$, so a measurement gives $k \in \{0, 2, 4, 6\}$, the multiples of $N/r = 2$, each with probability $1/4$. The offset changes only the phases, not the probabilities.

## Correctness

The proof below shows by induction on the loop of line L2 that after the turn of qubit $q$, qubit $q$ holds $(|0\rangle + e((j \bmod 2^{q+1})/2^{q+1})|1\rangle)/\sqrt{2}$ and qubits $p < q$ still hold $|j_p\rangle$. The key facts are that $H|b\rangle = (|0\rangle + e(b/2)|1\rangle)/\sqrt{2}$, that $\mathrm{CR}_k$ with a qubit $p$ in $|j_p\rangle$ multiplies the $|1\rangle$ part of qubit $q$ by $e(j_p/2^k)$, and that no later gate changes qubit $q$ except the swap. After the swaps the state is the product form, so the circuit is $F_N$ on each basis state and, by linearity, on each state. The same proof bounds the error of the approximate QFT by the sum of $|e(1/2^k) - 1| = 2\sin(\pi/2^k)$ over the dropped gates.

## Complexity

The exact costs, for use by other algorithms:

- **Gates.** $n$ Hadamard gates, $n(n-1)/2$ controlled phase gates ($n - k + 1$ copies of $\mathrm{CR}_k$ for $k = 2, \ldots, n$) and $\lfloor n/2 \rfloor$ swaps, so $n(n+1)/2 + \lfloor n/2 \rfloor$ gates. For $n = 3, 4, 8, 16, 32$ this is $7, 12, 40, 144, 544$. In CNOT gates, a controlled $R_\varphi$ is $2$ CNOT gates and $3$ one-qubit phase gates, and a swap is $3$ CNOT gates.
- **Depth.** If each gate starts as soon as its qubits are free, the circuit in list order has depth $2n$ for $n \ge 2$, and $2n - 1$ without the swaps. The swaps cost nothing if the program renames the qubits instead.
- **Qubits.** $n$, with no ancilla.
- **Inverse.** The same counts and depth.
- **Exactness.** The circuit is exact in exact arithmetic. With a finite gate set such as Clifford and $T$, each rotation must itself be approximated, see [Solovay-Kitaev theorem](/solovay-kitaev-theorem/).

**The approximate QFT.** With $m < n$, line L6 keeps $\mathrm{CR}_k$ only for $k \le m$. That leaves $\sum_{k=2}^{m} (n - k + 1) = (m-1)n - m(m-1)/2$ controlled phase gates, and the error satisfies

$$\| F_N - F_N^{(m)} \| \le \sum_{k=m+1}^{n} (n - k + 1) \cdot 2\sin(\pi/2^k) < \frac{2\pi (n - m)}{2^m} \le \frac{2\pi n}{2^m}.$$

So $m = \lceil \log_2(2\pi n/\varepsilon) \rceil$ gives error at most $\varepsilon$ with $O(n \log(n/\varepsilon))$ gates. Then the two output states differ by at most $\varepsilon$ in norm, so every outcome distribution moves by at most $\varepsilon$ in total variation distance. The table compares the bound with the operator norm of the difference, estimated by power iteration in the test code.

| $n$ | $m$ | gates $\mathrm{CR}_k$ kept | in the exact QFT | bound | measured norm |
|---|---|---|---|---|---|
| 4 | 2 | 3 | 6 | 1.9209 | 1.6629 |
| 4 | 3 | 5 | 6 | 0.3902 | 0.3902 |
| 6 | 3 | 9 | 15 | 1.6607 | 1.4819 |
| 6 | 4 | 12 | 15 | 0.4902 | 0.4860 |
| 6 | 5 | 14 | 15 | 0.0981 | 0.0981 |

At scale the savings are large. For $n = 1024$, the exact QFT has $523776$ controlled phase gates; $m = 14$ keeps $13221$ with error bound $0.387$, and $m = 20$ keeps $19266$ with bound $0.006$. For $n = 2048$, $m = 21$ keeps $40750$ of $2096128$, with bound $0.0061$.

## Properties

- **Exact and deterministic.** The circuit is a fixed list of gates that depends only on $n$ and $m$.
- **Product output.** On a basis state the output is a product state, so the QFT creates no entanglement on basis inputs. Entanglement appears only from superpositions at the input.
- **Shifts change only phases.** If the input is shifted by $c$, that is $x_j \to x_{j-c \bmod N}$, then $y_k \to \omega^{ck} y_k$. So the outcome distribution does not depend on the offset of a periodic state.
- **Peaks at multiples.** If $r$ divides $N$ and the input is the uniform superposition of $c, c + r, c + 2r, \ldots$, the output is supported on the $r$ multiples of $N/r$, each with probability $1/r$.
- **Powers.** $F_N^2 |j\rangle = |{-j} \bmod N\rangle$ and $F_N^4 = I$, so the eigenvalues of $F_N$ are among $1, i, -1, -i$.
- **The FFT inside.** The circuit is the radix-2 FFT in another form: $H$ is the [butterfly](/butterfly-operation/) of size $2$, the controlled phase gates are the twiddle factors, and the swaps are the bit reversal. The difference is that each gate acts on all $N$ amplitudes at once.
- **Over $\mathbb{Z}_2^n$.** The Fourier transform of the group $\mathbb{Z}_2^n$ is $H^{\otimes n}$, the [Walsh-Hadamard transform](/walsh-hadamard-transform/). It uses only $n$ gates and is the transform in the Deutsch-Jozsa, Bernstein-Vazirani and Simon algorithms.

## Variants and improvements

- **Approximate QFT.** Drop the rotations with $k > m$, as above. Coppersmith (1994) proposed it, and Barenco, Ekert, Suominen and Törmä (1996) showed that under decoherence the approximate form can do better than the exact one, because it has fewer gates that can fail.
- **Semiclassical QFT.** If all qubits are measured right after the transform, each controlled phase gate whose control is already measured can be replaced by a one-qubit phase gate chosen from the classical outcome. Griffiths and Niu (1996) gave this form. It needs only one-qubit gates, measurements and classical control. In phase estimation it lets one control qubit be measured and reused $t$ times.
- **Inverse QFT.** Reverse the list and negate the angles. Phase estimation uses this form.
- **Other moduli.** For $N$ not a power of $2$, and for any finite abelian group, Kitaev (1995) gave approximate Fourier transforms with a number of gates polynomial in $\log N$ and $\log(1/\varepsilon)$.
- **Low depth.** Cleve and Watrous (2000) gave approximate QFT circuits of depth $O(\log n + \log\log(1/\varepsilon))$.

## When to use it

Use the QFT, or its inverse, as the last step before a measurement when the state carries a period or a phase in its amplitudes: in [phase estimation](/quantum-phase-estimation/), in [order finding](/order-finding/), in [Shor's algorithm](/shor-algorithm/) and in [Fourier sampling](/fourier-sampling/) over $\mathbb{Z}_N$. Use the approximate form with $m \approx \log_2(n/\varepsilon)$ in practice, since the dropped rotations are smaller than the noise of any device.

Do not use it to compute the DFT of classical data. Loading $N$ numbers into amplitudes costs $\Omega(N)$ in general, and reading the $N$ output amplitudes needs a number of measurements that grows with $N$. Use the [fast Fourier transform](/fast-fourier-transform/) for that.

## Pitfalls

- **The sign.** The QFT uses $e^{+2\pi i/N}$. A circuit with the opposite sign is the inverse QFT. For a periodic state this only maps the peak $k$ to $N - k$, but in phase estimation it turns the estimate of $\varphi$ into an estimate of $1 - \varphi$.
- **The swaps.** Without lines L7 and L8 the output is in bit-reversed order. Many programs drop the swaps and rename the qubits; then each later gate must use the new names.
- **Qubit order.** Nielsen and Chuang draw qubit $1$, the most significant bit, at the top. In the order of these pages, qubit $0$ is the least significant bit. A circuit copied from one order into the other without a change gives a bit-reversed transform.
- **Controlled $R_\varphi$ and controlled $R_z$.** The two one-qubit gates differ by a global phase, but their controlled forms differ by a phase gate on the control. The QFT needs the controlled $R_\varphi = \mathrm{diag}(1, 1, 1, e^{i\varphi})$.
- **Too few rotations.** With $m = \log_2 n + c$ for a fixed $c$, the error bound is a constant near $2\pi/2^c$, not a value that goes to $0$. For error $\varepsilon$, take $m \approx \log_2(n/\varepsilon) + 3$.
- **Expecting the coefficients.** One run gives one sample $k$. To learn the Fourier coefficients themselves you need [state tomography](/quantum-state-tomography/), which costs far more than the transform.

## Implementations

## History

Peter Shor's factoring algorithm of 1994 needed a Fourier transform modulo a large number. Shor took the modulus to be a power of $2$, and Don Coppersmith, in an IBM research report of the same year, gave the circuit of Hadamard and controlled phase gates with $O(n^2)$ gates and the approximate form with $O(n \log n)$ gates. In 1995 Alexei Kitaev gave efficient Fourier transforms for any finite abelian group, together with phase estimation. In 1996 Barenco, Ekert, Suominen and Törmä studied the approximate QFT under decoherence, and Griffiths and Niu showed that a transform that is measured at once needs only one-qubit gates and classical control. Cleve and Watrous gave circuits of logarithmic depth in 2000.

## References
