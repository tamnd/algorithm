---
title: Kernighan's loop returns the number of 1-bits and runs once per 1-bit
proves: [correctness, termination]
status: full
---

Fix $w \ge 1$. A word is an integer $x$ with $0 \le x < 2^w$, with bits $x_i$ such that $x = \sum_{i=0}^{w-1} x_i 2^i$. Let $\nu(x) = \sum_i x_i$.

**Lemma.** For each word $x \ne 0$, the value $x \wedge (x - 1)$ is a word, and $\nu(x \wedge (x - 1)) = \nu(x) - 1$. More exactly, it is $x$ with its lowest 1-bit cleared.

*Proof.* Since $x \ne 0$, $x$ has a lowest 1-bit; call its position $j$. So $x_j = 1$ and $x_i = 0$ for $i < j$. Then $x = h + 2^j$ with $h = \sum_{i > j} x_i 2^i$, and $h$ is a multiple of $2^{j+1}$. Since $x \ge 1$, $x - 1 = h + 2^j - 1 = h + \sum_{i < j} 2^i$ is a word with no wrap-around. Its bits are: $x_i$ for $i > j$ (from $h$), 0 at position $j$, and 1 at each position $i < j$. The AND of $x$ and $x - 1$ has bit $x_i \wedge x_i = x_i$ at each $i > j$, bit $1 \wedge 0 = 0$ at $j$, and bit $0 \wedge 1 = 0$ at each $i < j$. So $x \wedge (x - 1) = h$, which is $x$ with bit $j$ cleared, and $\nu(h) = \nu(x) - 1$. $\square$

**Theorem.** For each word $x_0$, KERNIGHAN-POPCOUNT$(x_0)$ stops after exactly $\nu(x_0)$ iterations of the loop and returns $\nu(x_0)$.

*Proof.* We use this invariant of the loop of line L2.

> **(I)** $x$ is a word, $c \ge 0$, and $c + \nu(x) = \nu(x_0)$. Also, $c$ equals the number of iterations done so far.

*Initialization.* Before the first test, line L1 gives $c = 0$ and $x = x_0$, so (I) holds.

*Maintenance.* Assume (I) and that the test of line L2 is true, so $x \ne 0$. By the lemma, line L3 makes $x$ a word with $\nu$ one smaller. Line L4 makes $c$ one larger, and one more iteration is done. So $c + \nu(x)$ does not change, and (I) holds again.

*Termination.* By (I), $\nu(x) = \nu(x_0) - c$, and each iteration raises $c$ by exactly 1. Since $\nu(x) \ge 0$, at most $\nu(x_0)$ iterations can run. While $\nu(x) > 0$ we have $x \ne 0$ and the loop goes on, and $\nu(x) = 0$ holds exactly when $x = 0$. So the loop stops exactly when $c = \nu(x_0)$, after $\nu(x_0) \le w$ iterations. Line L5 returns $c = \nu(x_0)$. $\blacksquare$

**Remark on signed words.** The lemma needs $x - 1$ to be computed without overflow. For an unsigned word $x \ne 0$ this holds. In a signed $w$-bit type, $x = -2^{w-1}$ gives $x - 1 < -2^{w-1}$, which is outside the range; in C this is undefined behaviour. In arithmetic modulo $2^w$ the lemma applies to the bit pattern, which is why the algorithm is stated for unsigned words.
