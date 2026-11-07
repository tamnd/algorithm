---
title: The array multiplier computes the product of its inputs
proves: [correctness]
status: full
---

Let $n \ge 1$, $a = \sum_{i=0}^{n-1} a_i 2^i$ and $b = \sum_{j=0}^{n-1} b_j 2^j$ with all $a_i, b_j \in \{0, 1\}$. Line L1 sets $pp[j][i] = a_i b_j$, so $\sum_i pp[j][i]\, 2^i = a\, b_j$. A full adder satisfies $x + y + z = s + 2c$ with $s, c \in \{0, 1\}$, and we read $s[n] = 0$ in line L5.

For $j = 0, \ldots, n-1$ let $s^{(j)}$ and $c^{(j)}$ be the vectors $s$ and $c$ after row $j$ (after line L2 for $j = 0$, after line L6 for $j \ge 1$), and define

$$P_j = \sum_{k=0}^{j-1} p_k 2^k, \qquad V_j = \sum_{i=0}^{n-1} s^{(j)}[i]\, 2^{j+i} + \sum_{i=0}^{n-1} c^{(j)}[i]\, 2^{j+i+1} .$$

**Lemma.** For each $j$, (a) $P_j + V_j = a \cdot (b \bmod 2^{j+1})$, and (b) $c^{(j)}[n-1] = 0$.

*Proof.* By induction on $j$.

*Base, $j = 0$.* $P_0 = 0$, $s^{(0)} = pp[0]$ and $c^{(0)} = 0$, so $V_0 = a b_0 = a \cdot (b \bmod 2)$, and (b) holds.

*Step, from $j - 1$ to $j$, for $1 \le j \le n-1$.* Assume (a) and (b) for $j - 1$, and write $s = s^{(j-1)}$, $c = c^{(j-1)}$, $s' = s^{(j)}$, $c' = c^{(j)}$. Line L4 sets $p_{j-1} = s[0]$, so $P_j = P_{j-1} + s[0]\, 2^{j-1}$. Line L5 gives, for each $i$,

$$s'[i] + 2c'[i] = pp[j][i] + s[i+1] + c[i] .$$

Multiply by $2^{j+i}$ and sum over $i = 0, \ldots, n-1$. The left side is $V_j$. On the right side, $\sum_i pp[j][i]\, 2^{j+i} = a b_j 2^j$; $\sum_{i=0}^{n-1} s[i+1]\, 2^{j+i} = \sum_{i=1}^{n-1} s[i]\, 2^{j-1+i}$ because $s[n] = 0$; and $\sum_i c[i]\, 2^{j+i}$ is the $c$ part of $V_{j-1}$. So

$$V_j = a b_j 2^j + V_{j-1} - s[0]\, 2^{j-1} .$$

Adding the formula for $P_j$ gives $P_j + V_j = P_{j-1} + V_{j-1} + a b_j 2^j = a \cdot (b \bmod 2^j) + a b_j 2^j = a \cdot (b \bmod 2^{j+1})$, which is (a). For (b), the top cell $i = n - 1$ adds $pp[j][n-1] + s[n] + c[n-1] = pp[j][n-1] + 0 + 0 \le 1$ by the hypothesis (b), so its carry $c'[n-1]$ is 0. $\square$

**Theorem.** The bits $p_0, \ldots, p_{2n-1}$ computed by ARRAY-MULTIPLY satisfy $\sum_{k=0}^{2n-1} p_k 2^k = ab$.

*Proof.* Apply the lemma with $j = n - 1$, and write $s = s^{(n-1)}$, $c = c^{(n-1)}$. Since $b < 2^n$,

$$P_{n-1} + \sum_{i=0}^{n-1} s[i]\, 2^{n-1+i} + \sum_{i=0}^{n-2} c[i]\, 2^{n+i} = ab ,$$

where the term $c[n-1]$ is dropped by (b). Line L7 sets $p_{n-1} = s[0]$, so the left side is $P_n + 2^n (X + Y)$ with $P_n = P_{n-1} + s[0]\, 2^{n-1}$,

$$X = \sum_{i=1}^{n-1} s[i]\, 2^{i-1}, \qquad Y = \sum_{i=1}^{n-1} c[i-1]\, 2^{i-1} .$$

Lines L8 to L11 are a ripple-carry adder for the $(n-1)$-bit numbers $X$ and $Y$ with carry-in 0: by induction on $i$, after the step $i$ of line L10,

$$\sum_{k=1}^{i} p_{n-1+k}\, 2^{k-1} + \textit{carry} \cdot 2^{i} = \sum_{k=1}^{i} (s[k] + c[k-1])\, 2^{k-1},$$

since the step adds $(s[i] + c[i-1]) 2^{i-1}$ to the right side and replaces $\textit{carry} \cdot 2^{i-1}$ on the left by $p_{n-1+i}\, 2^{i-1} + \textit{carry}' \cdot 2^{i}$, which has the same value by the full adder equation. After $i = n - 1$ and line L11, $\sum_{k=1}^{n} p_{n-1+k}\, 2^{k-1} = X + Y$. Hence

$$\sum_{k=0}^{2n-1} p_k 2^k = P_n + 2^n (X + Y) = ab . \qquad \blacksquare$$

**Cell counts.** By (b), the top cell of each row has at most one live input. In row 1, $c^{(0)} = 0$, so cells $0, \ldots, n-2$ have two live inputs (half adders) and cell $n - 1$ has one (a wire). In rows $j \ge 2$, cell $i \le n - 2$ has three live inputs, because $c^{(j-1)}[i]$ comes from an adder of row $j - 1$; so these rows have $n - 1$ full adders each. The final adder has a half adder at $i = 1$ and full adders at $i = 2, \ldots, n-1$. This gives $(n-1)(n-2) + (n-2) = n^2 - 2n$ full adders and $(n - 1) + 1 = n$ half adders for $n \ge 2$.
