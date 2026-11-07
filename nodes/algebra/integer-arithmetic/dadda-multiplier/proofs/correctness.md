---
title: The Dadda reduction is always possible and computes the product
proves: [correctness, termination]
status: full
---

Write a column state as heights $h_0, \ldots, h_{2n-1}$ and the value of the state as $\sum_{\text{bits}} \text{bit} \cdot 2^{\text{column}}$. Let $d_1 = 2$, $d_{j+1} = \lfloor 3 d_j / 2 \rfloor$ and $d_t$ the largest term below $n$; for $n \le 2$ there are no stages.

**Termination.** There are $t$ stages, each a single pass over $2n$ columns with at most $h_k$ cells per column, and one final addition.

**Lemma 1 (value).** Each stage keeps the value. A full adder on bits $x, y, z$ of column $k$ outputs $s = x \oplus y \oplus z$ in column $k$ and $c = \operatorname{maj}(x, y, z)$ in column $k + 1$, and $x + y + z = s + 2c$, so the value changes by $(s + 2c - x - y - z) 2^k = 0$. The same holds for a half adder with $x + y = s + 2c$. Bits that pass are unchanged. $\square$

**Lemma 2 (heights before a stage).** Before the stage with target $d = d_j$, every column has height at most $D$, where $D = n$ if $j = t$ and $D = d_{j+1}$ otherwise. In both cases $D \le \lfloor 3d/2 \rfloor$.

*Proof.* Initially $h_k = \min(k + 1, 2n - 1 - k) \le n$. Since $d_t < n \le d_{t+1} = \lfloor 3 d_t / 2 \rfloor$ by the choice of $t$, the claim holds for the first stage. A stage with target $d$ leaves every column with height at most $d$ (Lemma 3 shows that the stage can be built; then each column has $h_k + c_k - 2F_k - H_k = d$ bits when $e_k > 0$ and $h_k + c_k \le d$ bits otherwise), which is the bound $D$ of the next stage, and $d_{j+1} = \lfloor 3 d_j / 2 \rfloor$. $\square$

**Lemma 3 (enough bits).** In a stage with target $d$ and previous bound $D \le \lfloor 3d/2 \rfloor$, let $c_k$ be the number of carries into column $k$, $e_k = h_k + c_k - d$, $F_k = \lfloor e_k/2 \rfloor$ and $H_k = e_k \bmod 2$ when $e_k > 0$, and $F_k = H_k = 0$ otherwise. Then $c_k \le D - d$ and $3F_k + 2H_k \le h_k$ for every $k$.

*Proof.* By induction on $k$. For $k = 0$, $c_0 = 0$. Assume $c_k \le D - d$. If $e_k \le 0$ there are no adders and $c_{k+1} = 0$. Otherwise $c_{k+1} = F_k + H_k = \lceil e_k / 2 \rceil$, and $e_k \le D + (D - d) - d = 2(D - d)$, so $c_{k+1} \le D - d$. For the bits: if $e_k$ is even, $3F_k + 2H_k = 3e_k/2$, and $3e_k / 2 \le h_k$ is equivalent to $h_k + 3c_k \le 3d$. If $e_k$ is odd, $3F_k + 2H_k = (3e_k + 1)/2$, and the condition is $h_k + 3c_k \le 3d - 1$. Now $h_k + 3c_k \le D + 3(D - d) = 4D - 3d \le 3d$ since $D \le 3d/2$. Equality throughout needs $h_k = D$, $c_k = D - d$ and $D = 3d/2$; then $e_k = 2D - 2d$ is even. So when $e_k$ is odd the inequality is strict, $h_k + 3c_k \le 3d - 1$. $\square$

**No carry leaves the top.** Column $2n - 1$ starts empty and, as long as it has height 0, Lemma 3 gives $3F + 2H \le 0$, so it has no adders and sends no carry to column $2n$. Its height after a stage is at most $d$. If it ever had bits with adders, the value would still be $ab < 2^{2n}$ by Lemma 1; a bit of column $2n$ would make the value at least $2^{2n}$, so column $2n$ is always empty.

**Theorem.** DADDA-MULTIPLY returns the $2n$ bits of $ab$.

*Proof.* Initially the value is $\sum_{i,j} (a_i \wedge b_j) 2^{i+j} = ab$ (line L1). By Lemma 3 every stage can be built, by Lemma 1 it keeps the value, and by Lemma 2 after the last stage, with $d = d_1 = 2$, every column has at most two bits. Reading the bits of each column as two rows $r_1$ and $r_2$ (a missing bit is 0), $r_1 + r_2 = ab$, and line L8 returns $ab$, which is less than $2^{2n}$ and fits in the $2n$ output bits. $\blacksquare$

**Delay.** An AND gate has delay 1. The adders of a stage take only bits present before the stage, so if all of those arrive by time $s$, all bits after the stage arrive by time $s + 1$. By induction the two rows arrive by time $t + 1$. $\blacksquare$
