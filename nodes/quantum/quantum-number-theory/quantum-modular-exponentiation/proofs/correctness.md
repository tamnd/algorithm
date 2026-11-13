---
title: The modular exponentiation circuit computes y a^x mod N and resets its ancillas
proves: [correctness]
status: full
---

We use the pseudocode of the page. $N \ge 3$, $\gcd(a, N) = 1$, $n$ is the bit length of $N$, so $N < 2^n$, and $b$ has $n + 1$ qubits. "$b \leftarrow b \pm k$" means addition modulo $M = 2^{n+1}$, and $\mathrm{top}(b)$ is bit $n$ of $b$. For an integer $z$ with $-2^n \le z < 2^n$, the value $z \bmod M$ has top bit 1 exactly when $z < 0$ (two's complement). All circuits are permutations of basis states, so it is enough to prove each claim on basis states; a unitary that permutes basis states acts on a superposition term by term.

**Lemma 0 (the constant adder).** The adder of Cuccaro, Draper, Kutin and Moulton maps $|p\rangle|q\rangle|0\rangle$ to $|p\rangle|(p + q) \bmod M\rangle|0\rangle$ on two registers of $n + 1$ qubits and one carry qubit. Loading $k$ into the zeroed constant register with gates controlled by $C$, adding, and unloading with the same gates therefore maps $b$ to $(b + k) \bmod M$ when all of $C$ are 1 and to $b$ otherwise, and returns the constant register to 0. Its inverse maps $b$ to $(b - k) \bmod M$ under the same condition.

*Proof.* The adder statement is the main result of Cuccaro et al. If some control is 0, the load and unload do nothing and the adder adds 0. The loads are NOT gates, so the unload undoes the load. $\square$

**Lemma 1 (MODADD).** For $0 \le b < N$ and $0 \le k < N$, with $f = 0$, lines L1 to L7 end with $b' = (b + k) \bmod N$ if all of $C$ are 1 and $b' = b$ otherwise, and with $f = 0$.

*Proof.* Let $s = 1$ if all of $C$ are 1 and $s = 0$ otherwise, and let $u = b + s k$, so $0 \le u \le 2N - 2 < 2^{n+1}$. After line L1, $b = u$. After line L2, $b$ holds $u - N \bmod M$, and $-N \le u - N < N \le 2^n$, so $\mathrm{top}(b) = 1$ exactly when $u < N$. Line L3 sets $f = [u < N]$. Line L4 adds $N$ when $f = 1$, so $b = u$ if $u < N$ and $b = u - N$ if $u \ge N$. In both cases $b = (b_0 + s k) \bmod N$, where $b_0$ is the input; call this value $w$, with $0 \le w < N$.

Line L5 gives $w - s k$. If $u < N$, then $w = u$ and $w - sk = b_0 \ge 0$. If $u \ge N$, then $s = 1$ and $w - k = b_0 - N < 0$, with $b_0 - N \ge -N > -2^n$. So $\mathrm{top}(b) = 1$ exactly when $u \ge N$, that is, exactly when $f = 0$. Line L6 adds $1 \oplus \mathrm{top}(b) = f$ to $f$, so $f = 0$. Line L7 adds $sk$ back, so $b = w$. $\square$

**Lemma 2 (CMULT).** For $0 \le y < N$ and $0 \le b < N$, lines L8 and L9 map $b$ to $(b + a y) \bmod N$ if ctrl is 1 and leave $b$ unchanged otherwise; $y$, ctrl and all ancillas other than $b$ are unchanged.

*Proof.* No gate of MODADD targets ctrl or $y$, so they keep their values. By Lemma 1 with $C = \{\mathrm{ctrl}, y_i\}$, each step keeps $0 \le b < N$ and adds $y_i (2^i a \bmod N)$ when ctrl is 1. After all $n$ steps, $b = b_0 + \sum_i y_i 2^i a = b_0 + a y \pmod N$. $\square$

**Lemma 3 (CU).** For $0 \le y < N$ and $b = 0$, lines L10 to L12 map $y$ to $a y \bmod N$ if ctrl is 1 and leave it unchanged otherwise, and end with $b = 0$.

*Proof.* If ctrl is 0, Lemma 2 shows that CMULT$(a)$ and CMULT$(a^{-1} \bmod N)$ fix the state, so the inverse of the second one fixes it too, and the swap of line L11 does nothing. Let ctrl be 1. After line L10, $b = a y \bmod N < N < 2^n$, so the top bit of $b$ is 0, and line L11 gives $y' = a y \bmod N$ and $b = y$. Let $a' = a^{-1} \bmod N$. The circuit CMULT$(a')$ maps $(y', \beta)$ to $(y', (\beta + a' y') \bmod N)$ for all $0 \le \beta < N$; this map is a bijection of $\{0, \dots, N-1\}$ in $\beta$, so its inverse maps $\beta$ to $(\beta - a' y') \bmod N$ on the same range. Line L12 applies it with $\beta = y$, giving $b = y - a' a y = 0 \pmod N$, so $b = 0$. $\square$

**Theorem.** For $0 \le x < 2^t$ and $0 \le y < N$, MODEXP maps $|x\rangle|y\rangle|0\rangle$ to $|x\rangle|y\,a^x \bmod N\rangle|0\rangle$.

*Proof.* Write $x = \sum_j x_j 2^j$. Line L15 keeps $c = a^{2^j} \bmod N$ at the start of step $j$, and $\gcd(c, N) = 1$. By Lemma 3, step $j$ multiplies $y$ by $c^{x_j}$ modulo $N$, keeps $y < N$ and leaves $b = 0$; the other ancillas are 0 by Lemmas 0 and 1, and $x$ is never a target. After $t$ steps,

$$y = y_0 \prod_{j} a^{2^j x_j} = y_0\, a^{x} \pmod N. \qquad \blacksquare$$

**Corollary (superpositions).** For any amplitudes $\alpha_x$, the circuit maps $\sum_x \alpha_x |x\rangle|1\rangle|0\rangle$ to $\sum_x \alpha_x |x\rangle|a^x \bmod N\rangle|0\rangle$. The ancilla register factors out as $|0\rangle$, so it is not entangled with $x$.
