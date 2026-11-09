---
title: The prefix exclusive or inverts the Gray code map
proves: [correctness]
status: full
---

For an integer $x \ge 0$ we write $x_j$ for bit $j$ of $x$, so $x = \sum_j x_j 2^j$, and $x_j = 0$ for all large $j$. The map $g(b) = b \oplus \lfloor b/2 \rfloor$ gives the entry of rank $b$ in the reflected Gray code (see the proof on the page of [binary to Gray conversion](/binary-to-gray-conversion/)). Define $h(a)$ as the integer whose bit $j$ is $\bigoplus_{i \ge j} a_i$, the exclusive or of the bits of $a$ at position $j$ or higher. This sum is finite, because $a$ has finitely many one bits.

**Lemma 1.** For all $b \ge 0$, $h(g(b)) = b$. For all $a \ge 0$, $g(h(a)) = a$. So $h$ is the inverse of $g$, and $h(a) < 2^n$ when $a < 2^n$.

*Proof.* Let $a = g(b)$. Bit $i$ of $\lfloor b/2 \rfloor$ is $b_{i+1}$, so $a_i = b_i \oplus b_{i+1}$. Let $m$ be larger than the bit length of $b$, so $b_m = 0$. For $j < m$, bit $j$ of $h(a)$ is $\bigoplus_{i=j}^{m-1} (b_i \oplus b_{i+1})$, because $a_i = 0$ for $i \ge m$. Each $b_i$ with $j < i < m$ appears twice and cancels, so the sum is $b_j \oplus b_m = b_j$. For $j \ge m$, both bits are 0. So $h(g(b)) = b$.

Now let $c = h(a)$. Bit $i$ of $g(c)$ is $c_i \oplus c_{i+1} = \bigoplus_{r \ge i} a_r \oplus \bigoplus_{r \ge i+1} a_r = a_i$. So $g(h(a)) = a$. If $a < 2^n$ then $a_i = 0$ for $i \ge n$, so $c_j = 0$ for $j \ge n$ and $c < 2^n$. $\square$

**FROM-GRAY (lines L1 to L5).** Let $\alpha$ be the input and $\ell$ its bit length, so $\alpha < 2^{\ell}$ and $\ell = 0$ when $\alpha = 0$.

*Invariant.* At the test of line L2, after $t$ rounds of the loop, $a = \lfloor \alpha / 2^t \rfloor$ and $b = \bigoplus_{r=0}^{t-1} \lfloor \alpha / 2^r \rfloor$. At the first test, $t = 0$, line L1 gives $b = 0$, the empty sum, and $a = \alpha$. A round with $a = \lfloor \alpha/2^t \rfloor$ sets $b \leftarrow b \oplus \lfloor \alpha / 2^t \rfloor$ in line L3 and $a \leftarrow \lfloor \lfloor \alpha/2^t \rfloor / 2 \rfloor = \lfloor \alpha / 2^{t+1} \rfloor$ in line L4. So the invariant holds with $t + 1$.

*Termination.* $\lfloor \alpha/2^t \rfloor = 0$ exactly when $t \ge \ell$. So the loop runs exactly $\ell$ rounds and stops, and at the end $b = \bigoplus_{r=0}^{\ell-1} \lfloor \alpha/2^r \rfloor$.

*Result.* Bit $j$ of $\lfloor \alpha / 2^r \rfloor$ is $\alpha_{j+r}$. So bit $j$ of $b$ is $\bigoplus_{r=0}^{\ell-1} \alpha_{j+r}$. Every $\alpha_i$ with $i \ge j + \ell$ is 0, so this equals $\bigoplus_{i \ge j} \alpha_i$, and $b = h(\alpha)$. By Lemma 1, line L5 returns the rank of $\alpha$.

**FROM-GRAY-FAST (lines L6 to L10).** Let $\alpha < 2^w$ be the input and $w \ge 1$.

*Invariant.* At each test of line L7, $s$ is a power of 2, and bit $j$ of $a$ is $\bigoplus_{i=j}^{j+s-1} \alpha_i$ for each $j \ge 0$. At the first test, $s = 1$ (line L6) and $a = \alpha$, so bit $j$ is $\alpha_j$. Assume the invariant before a round. Bit $j$ of $\lfloor a/2^s \rfloor$ is bit $j + s$ of $a$, which is $\bigoplus_{i=j+s}^{j+2s-1} \alpha_i$. So after line L8, bit $j$ of $a$ is $\bigoplus_{i=j}^{j+s-1} \alpha_i \oplus \bigoplus_{i=j+s}^{j+2s-1} \alpha_i = \bigoplus_{i=j}^{j+2s-1} \alpha_i$. Line L9 doubles $s$, so the invariant holds again.

*Termination.* Each round doubles $s$, so after $\lceil \lg w \rceil$ rounds $s \ge w$ and the loop stops.

*Result.* At the end $s \ge w$. For each $j$, the window $j, \ldots, j + s - 1$ contains all positions $i \ge j$ with $i < w$, and $\alpha_i = 0$ for $i \ge w$. So bit $j$ of $a$ is $\bigoplus_{i \ge j} \alpha_i$, and line L10 returns $h(\alpha)$, the rank of $\alpha$ by Lemma 1. $\blacksquare$
