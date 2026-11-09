---
title: b XOR floor(b/2) is the entry of rank b in the reflected Gray code
proves: [correctness]
status: full
---

The reflected Gray code is $\Gamma_0 = \varepsilon$ and $\Gamma_{m+1} = 0\Gamma_m,\ 1\Gamma_m^R$. Positions in a list start at 0. For an integer $b \ge 0$ we write $b_j$ for bit $j$ of $b$, so $b = \sum_j b_j 2^j$.

**Claim.** For each $m \ge 0$ and each $0 \le b < 2^m$, the entry of rank $b$ in $\Gamma_m$ is the string $a_{m-1} \ldots a_0$ with $a_j = b_j \oplus b_{j+1}$ for $0 \le j < m$.

*Proof.* By induction on $m$. For $m = 0$ the only rank is $b = 0$, and the entry is the empty string, which has no bits. So the claim holds.

Assume the claim for $m$, and let $0 \le b < 2^{m+1}$.

*Case $b < 2^m$.* The entry of rank $b$ in $\Gamma_{m+1}$ is $0$ followed by the entry of rank $b$ in $\Gamma_m$. Its top bit is $a_m = 0$, and $b_m \oplus b_{m+1} = 0 \oplus 0 = 0$, since $b < 2^m$. Its other bits are $b_j \oplus b_{j+1}$ for $j < m$ by the hypothesis.

*Case $b \ge 2^m$.* Let $c = 2^{m+1} - 1 - b$, so $0 \le c < 2^m$. The second half of $\Gamma_{m+1}$ is $1\Gamma_m^R$, so the entry of rank $b = 2^m + (2^m - 1 - c)$ is $1$ followed by the entry of rank $c$ in $\Gamma_m$. Since $c < 2^m$, the number $2^m - 1 - c$ has the bits of $c$ complemented in positions $0$ to $m-1$. So $b_m = 1$, $b_{m+1} = 0$, and $b_j = 1 - c_j$ for $j < m$, while $c_m = 0$.

- Top bit: $a_m = 1 = b_m \oplus b_{m+1}$.
- Bit $j$ with $j \le m - 2$: by the hypothesis it is $c_j \oplus c_{j+1}$. Since $(1 - x) \oplus (1 - y) = x \oplus y$ for bits $x, y$, this equals $b_j \oplus b_{j+1}$.
- Bit $m - 1$ (when $m \ge 1$): by the hypothesis it is $c_{m-1} \oplus c_m = c_{m-1}$, and $b_{m-1} \oplus b_m = (1 - c_{m-1}) \oplus 1 = c_{m-1}$.

So the claim holds for $m + 1$. $\square$

**Line L1.** Bit $j$ of $\lfloor b/2 \rfloor$ is $b_{j+1}$, because the right shift moves each bit down by one position. So bit $j$ of $b \oplus \lfloor b/2 \rfloor$ is $b_j \oplus b_{j+1}$ for every $j$. For $b < 2^n$ these bits are 0 for $j \ge n$, so the result is the $n$-bit string of the claim.

**Lines L2 to L5.** Line L2 sets $b_n = 0$, which is the true bit $n$ of $b < 2^n$. The loop of line L3 runs once for each $j$ from $0$ to $n - 1$, and line L4 sets $a_j = b_j \oplus b_{j+1}$, reading only $b_0, \ldots, b_n$. Line L5 returns these $n$ bits, which by the claim are the entry of rank $b$ in $\Gamma_n$. $\blacksquare$
