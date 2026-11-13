---
title: The Deutsch-Jozsa algorithm is always right with one query
proves: [correctness]
status: full
---

We write $N = 2^n$, $x \cdot y = \sum_j x_j y_j \bmod 2$ and $|f| = |\{x : f(x) = 1\}|$. Qubit $j$ holds bit $j$ of the basis index, the input register is qubits $0$ to $n - 1$, and the ancilla is qubit $n$. We write a state of all $n + 1$ qubits as $|x\rangle \otimes |b\rangle$, with $x$ the input register and $b$ the ancilla.

**Lemma 1 (Hadamard transform).** For each $x \in \{0,1\}^n$,
$$H^{\otimes n} |x\rangle = \frac{1}{\sqrt{N}} \sum_{y \in \{0,1\}^n} (-1)^{x \cdot y} |y\rangle.$$

*Proof.* For one qubit, $H|b\rangle = (|0\rangle + (-1)^b |1\rangle)/\sqrt{2} = 2^{-1/2} \sum_{c \in \{0,1\}} (-1)^{bc} |c\rangle$. The map $H^{\otimes n}$ acts on each qubit apart, so
$$H^{\otimes n} |x\rangle = \bigotimes_{j} \Big( 2^{-1/2} \sum_{y_j} (-1)^{x_j y_j} |y_j\rangle \Big) = N^{-1/2} \sum_y (-1)^{\sum_j x_j y_j} |y\rangle,$$
and $(-1)^{\sum_j x_j y_j} = (-1)^{x \cdot y}$. $\square$

**Lemma 2 (phase kickback).** With $|-\rangle = (|0\rangle - |1\rangle)/\sqrt{2}$, $U_f (|x\rangle \otimes |-\rangle) = (-1)^{f(x)} |x\rangle \otimes |-\rangle$.

*Proof.* $U_f (|x\rangle \otimes |-\rangle) = |x\rangle \otimes (|f(x)\rangle - |1 \oplus f(x)\rangle)/\sqrt{2}$. If $f(x) = 0$ this is $|x\rangle \otimes |-\rangle$. If $f(x) = 1$ it is $|x\rangle \otimes (|1\rangle - |0\rangle)/\sqrt{2} = -|x\rangle \otimes |-\rangle$. $\square$

**Lemma 3 (the final state).** Before line L5 the state is
$$\Big( \sum_{y} a_y |y\rangle \Big) \otimes |-\rangle, \qquad a_y = \frac{1}{N} \sum_x (-1)^{f(x) + x \cdot y}.$$

*Proof.* Line L1 gives $|0\rangle \otimes |1\rangle$. Line L2 gives $H^{\otimes n}|0\rangle \otimes H|1\rangle$, which is $N^{-1/2} \sum_x |x\rangle \otimes |-\rangle$ by Lemma 1 with $x = 0$. Line L3 is linear, so by Lemma 2 it gives $N^{-1/2} \sum_x (-1)^{f(x)} |x\rangle \otimes |-\rangle$. Line L4 applies $H^{\otimes n}$ to the input register only. By Lemma 1 and linearity the state is
$$\frac{1}{N} \sum_x (-1)^{f(x)} \sum_y (-1)^{x \cdot y} |y\rangle \otimes |-\rangle = \sum_y a_y |y\rangle \otimes |-\rangle. \qquad \square$$

**Theorem.** If $f$ is constant, line L6 returns "constant" with probability $1$. If $f$ is balanced, it returns "balanced" with probability $1$.

*Proof.* By Lemma 3 the state is a product of a state of the input register and the ancilla state $|-\rangle$. So measuring the input register in line L5 gives $y$ with probability $a_y^2$. (The $a_y$ are real.) For $y = 0$, $x \cdot 0 = 0$ for all $x$, so
$$a_0 = \frac{1}{N} \sum_x (-1)^{f(x)} = \frac{(N - |f|) - |f|}{N} = \frac{N - 2|f|}{N}.$$
If $f$ is constant, $|f| = 0$ or $|f| = N$, so $a_0 = \pm 1$ and $\Pr[y = 0] = 1$; line L6 returns "constant". If $f$ is balanced, $|f| = N/2$, so $a_0 = 0$ and $\Pr[y = 0] = 0$; every outcome has $y \ne 0$, and line L6 returns "balanced". $\blacksquare$

**The cost.** Line L3 is the only use of $U_f$, so the algorithm makes one query. Lines L1, L2 and L4 use one $X$ gate and $(n + 1) + n = 2n + 1$ Hadamard gates.

**Remarks.** The vector $(a_y)_y$ is a unit vector, because the map from the state after line L3 to the state after line L4 is unitary. This gives Parseval's identity $\sum_y a_y^2 = 1$ for the Walsh-Hadamard coefficients. For a function outside the promise with a fraction $w = |f|/N$ of ones, the same computation gives $\Pr[y = 0] = (1 - 2w)^2$.
