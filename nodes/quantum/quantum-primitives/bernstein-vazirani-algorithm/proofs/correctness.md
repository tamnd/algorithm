---
title: The Bernstein-Vazirani algorithm returns s with probability 1
proves: [correctness]
status: full
---

We write $N = 2^n$ and $x \cdot y = \sum_j x_j y_j \bmod 2$. Qubit $j$ holds bit $j$, the input register is qubits $0$ to $n - 1$ and the ancilla is qubit $n$. The oracle is $U_f |x\rangle|b\rangle = |x\rangle|b \oplus f(x)\rangle$ with $f(x) = s \cdot x \oplus c$.

**Lemma 1 (Hadamard transform).** $H^{\otimes n} |x\rangle = N^{-1/2} \sum_y (-1)^{x \cdot y} |y\rangle$ for each $x$.

*Proof.* $H|b\rangle = 2^{-1/2} \sum_{c} (-1)^{bc} |c\rangle$ for one qubit. Take the tensor product over the $n$ qubits; the signs multiply to $(-1)^{\sum_j x_j y_j} = (-1)^{x \cdot y}$. $\square$

**Lemma 2 (orthogonality of characters).** For $z \in \{0,1\}^n$, $\sum_x (-1)^{z \cdot x} = N$ if $z = 0$ and $0$ if $z \ne 0$.

*Proof.* If $z = 0$ each term is $1$. If $z \ne 0$, pick $j$ with $z_j = 1$. The map $x \mapsto x \oplus e_j$ is a bijection of $\{0,1\}^n$ that changes $z \cdot x$ by $1$, so it pairs each term $+1$ with a term $-1$, and the sum is $0$. $\square$

**Lemma 3 (phase kickback).** With $|-\rangle = (|0\rangle - |1\rangle)/\sqrt{2}$, $U_f(|x\rangle \otimes |-\rangle) = (-1)^{f(x)} |x\rangle \otimes |-\rangle$.

*Proof.* The ancilla becomes $(|f(x)\rangle - |1 \oplus f(x)\rangle)/\sqrt{2}$, which is $|-\rangle$ if $f(x) = 0$ and $-|-\rangle$ if $f(x) = 1$. $\square$

**Theorem.** Line L5 returns $s$ with probability $1$.

*Proof.* Line L1 gives $|0\rangle \otimes |1\rangle$, and line L2 gives $N^{-1/2} \sum_x |x\rangle \otimes |-\rangle$ by Lemma 1. By Lemma 3 and linearity, line L3 gives $N^{-1/2} \sum_x (-1)^{f(x)} |x\rangle \otimes |-\rangle$. By Lemma 1, line L4 gives $\sum_y a_y |y\rangle \otimes |-\rangle$ with
$$a_y = \frac{1}{N} \sum_x (-1)^{f(x) + x \cdot y} = \frac{(-1)^c}{N} \sum_x (-1)^{(s \oplus y) \cdot x},$$
because $s \cdot x + x \cdot y \equiv (s \oplus y) \cdot x \pmod 2$. By Lemma 2, $a_s = (-1)^c$ and $a_y = 0$ for $y \ne s$. So the state before line L5 is $(-1)^c |s\rangle \otimes |-\rangle$. The factor $(-1)^c$ is a global phase, and the measurement of the input register gives $s$ with probability $|a_s|^2 = 1$. $\blacksquare$

**The cost.** Line L3 is the only query. Lines L1, L2 and L4 use one $X$ gate and $2n + 1$ Hadamard gates.

**For any $f$.** The same computation, without the promise, shows that the outcome $y$ has probability $a_y^2$, where $a_y$ is the Walsh-Hadamard coefficient of $(-1)^f$ at $y$. The promise is used only in the step from $a_y$ to $(-1)^c [y = s]$.
