---
title: Transformation-based synthesis ends with a correct circuit of at most (n - 1) 2^n + 1 gates
proves: [correctness]
status: full
---

This file proves, for both the basic and the bidirectional form of the code, that the algorithm ends, that its output computes $f$ on the same $n$ lines with no extra line, and that the output has at most $(n - 1) 2^n + 1$ gates.

**Notation.** Values are numbers in $\{0, \dots, 2^n - 1\}$, and bit $t$ of $x$ is $x_t$. For $x, y$ write $x \supseteq y$ if $x$ has every 1-bit of $y$; then $x \ge y$ as numbers. $T(C; t)$ with $t \notin C$ flips bit $t$ of $x$ when $x \supseteq C$ (reading $C$ as a mask). Every such gate is a bijection and its own inverse. For $0 \le i < 2^n - 1$, let $h(i)$ be the position of the highest 0 bit of $i$. Products of maps are composed right to left: $(G \circ H)(x) = G(H(x))$.

## The row step

**Lemma 1.** Let $v > i$, and let $S$ be the gates of lines L5 and L6: first $T(\mathrm{ones}(v); t)$ for each $t$ with $i_t = 1, v_t = 0$, then $T(\mathrm{ones}(i); t)$ for each $t$ with $i_t = 0, v_t = 1$. Then:

1. no gate of $S$ has its target among its controls;
2. applied in order, $S$ maps $v$ to $i$;
3. $S$ fixes every $x < i$;
4. $|S| = d(v, i) \le h(i) + 1$.

*Proof.* (1) A gate of the first kind has target $t$ with $v_t = 0$, so $t \notin \mathrm{ones}(v)$; one of the second kind has $i_t = 0$, so $t \notin \mathrm{ones}(i)$.

(2) During the first part, the value of the row starts at $v$ and only gains bits, so it stays $\supseteq v$ and each gate fires and sets its bit. After the first part the value is $v \lor i$ (bitwise OR), which is $\supseteq i$. During the second part, each gate clears a bit $t$ with $i_t = 0$, so the value stays $\supseteq i$, and each gate fires. At the end the bits set are exactly those of $i$.

(3) Take $x < i$, and follow it through $S$. It is not changed by a gate of the first kind, since that would need $x \supseteq v$, so $x \ge v > i$. It is not changed by a gate of the second kind, since that would need $x \supseteq i$, so $x \ge i$. Since no gate changes it, every later gate sees the same $x$, and $x$ is fixed.

(4) Each gate changes one bit that differs between $v$ and $i$, and each differing bit gets one gate, so $|S| = d(v, i)$. Let $p$ be the highest bit where $v$ and $i$ differ. Since $v > i$, $v_p = 1$ and $i_p = 0$, so $p \le h(i)$. Every differing bit is at a position $\le p$, so $d(v, i) \le p + 1 \le h(i) + 1$. ∎

## The loop

Let $\mathit{out}_i$ and $\mathit{inv}_i$ be the tables at the start of iteration $i$ of line L2, and let $A_i$ and $B_i$ be the products of the gates found so far at the outputs and at the inputs: each output gate $G$ found makes $A \leftarrow G \circ A$, and each input gate makes $B \leftarrow B \circ G$. $A_0 = B_0 = \mathrm{id}$.

**Lemma 2 (invariant).** At the start of iteration $i$:

1. $\mathit{out}_i$ is a bijection and $\mathit{inv}_i$ is its inverse;
2. $\mathit{out}_i = A_i \circ f \circ B_i$;
3. $\mathit{out}_i[j] = j$ for every $j < i$.

*Proof.* By induction on $i$. At $i = 0$, (1) and (2) hold by line L1, and (3) is empty.

Suppose it holds at $i$. If $\mathit{out}_i[i] = i$, nothing changes and (3) now holds for $j \le i$. Otherwise, by (1) and (3), $\mathit{out}_i[j] = j$ and $\mathit{inv}_i[j] = j$ for $j < i$, so neither $\mathit{out}_i[i]$ nor $\mathit{inv}_i[i]$ is below $i$; neither equals $i$, since $\mathit{out}_i[i] \ne i$ and $\mathit{inv}_i$ is the inverse. So $v = a[i] > i$ on either side, and Lemma 1 applies.

*Output side* ($a = \mathit{out}$). Each gate $G$ of $S$ makes $\mathit{out} \leftarrow G \circ \mathit{out}$ and $A \leftarrow G \circ A$, so (2) holds after it. A composition of bijections is a bijection, and the code rebuilds $\mathit{inv}$ as its inverse, so (1) holds. By Lemma 1 (3), rows $j < i$ keep the value $j$, and by Lemma 1 (2), row $i$ ends with the value $i$.

*Input side* ($a = \mathit{inv}$). Each gate $G$ makes $\mathit{inv} \leftarrow G \circ \mathit{inv}$, and the code rebuilds $\mathit{out}$ as its inverse, so (1) holds and $\mathit{out} \leftarrow \mathit{inv}^{-1} \circ G^{-1} = \mathit{out} \circ G$, since $G = G^{-1}$; with $B \leftarrow B \circ G$, (2) holds. By Lemma 1 (3), $\mathit{inv}[j] = j$ for $j < i$, so $\mathit{out}[j] = j$; by Lemma 1 (2), $\mathit{inv}[i] = i$, so $\mathit{out}[i] = i$. ∎

**Theorem 3 (correctness).** The algorithm ends, and the circuit it returns computes $f$, on the $n$ lines of $f$, with no extra line.

*Proof.* The loop runs $2^n$ times, and each iteration adds at most $n$ gates (Lemma 1 (4)), each applied to two tables of size $2^n$, so it ends. By Lemma 2 at $i = 2^n$, $\mathit{out}[j] = j$ for every $j$, so $A \circ f \circ B = \mathrm{id}$ and $f = A^{-1} \circ B^{-1}$. Let the input gates be $G_1, \dots, G_m$ in the order found and the output gates $H_1, \dots, H_k$. Then $B = G_1 \circ \cdots \circ G_m$ and $A = H_k \circ \cdots \circ H_1$, so, as each gate is its own inverse,
$$f = H_1 \circ H_2 \circ \cdots \circ H_k \circ G_m \circ \cdots \circ G_1.$$
The rightmost factor acts first, so the circuit in time order is $G_1, \dots, G_m, H_k, \dots, H_1$, which is what line L9 returns. Every gate is a valid gate on the $n$ lines (Lemma 1 (1)), and the tables never have more than $2^n$ entries, so no line is added. ∎

## The gate bound

**Theorem 4.** Both forms use at most $(n - 1) 2^n + 1$ gates.

*Proof.* By Lemma 2 and the proof above, iteration $i$ adds $d(v, i)$ gates for some $v > i$, or none. For $i = 2^n - 1$ it adds none: by Lemma 2 (3) all other values are taken, so $\mathit{out}[2^n - 1] = 2^n - 1$. For $i < 2^n - 1$ it adds at most $h(i) + 1$ (Lemma 1 (4)). The values $i < 2^n$ whose highest 0 bit is at position $z$ have 1s above $z$, a 0 at $z$, and any bits below, so there are $2^z$ of them. So the total is at most
$$\sum_{z=0}^{n-1} (z + 1) 2^z = (n - 1) 2^n + 1.$$
The identity holds for $n = 1$ ($1 = 0 \cdot 2 + 1$), and if it holds for $n$, adding the term $(n + 1) 2^n$ gives $(n - 1) 2^n + 1 + (n + 1) 2^n = n 2^{n+1} + 1$, the value for $n + 1$. ∎

The bidirectional form changes only which value $v$ is used in a row, and both candidates are above $i$, so the same bound holds. For the basic form the bound is reached: Maslov, Dueck and Miller (TCAD 2005, Theorem 1) give a function for each $n$ on which the basic form uses exactly $(n - 1) 2^n + 1$ gates, and the test file checks their functions for $n = 3$ (17 gates) and $n = 4$ (49 gates). This says nothing about the best circuit for that function: for $n = 3$ the best circuit has 6 gates.

## What is not proved

Nothing here compares the output with an optimal circuit. The test file measures that gap on all 40,320 functions of 3 bits against a breadth-first search.
