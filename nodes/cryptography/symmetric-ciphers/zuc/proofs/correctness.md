---
title: ZUC decrypts correctly, its cells stay in range, and its working-stage clock is a bijection
proves: [correctness]
status: full
---

Write $p = 2^{31} - 1$ and $\sigma = (s_0, \ldots, s_{15}, R_1, R_2)$ for the state. Let $\Phi$ be one clock of lines L8 to L10 of the page (the working stage).

**Lemma 1 (cells stay in range).** After line L1 and after each use of line L14, every cell $s_i$ is an integer in $\{1, \ldots, p\}$.

*Proof.* Line L1 sets $s_i = k_i \cdot 2^{23} + d_i \cdot 2^8 + iv_i$ with $k_i, iv_i < 2^8$ and $d_i < 2^{15}$, so $s_i < 2^{31}$, that is $s_i \le p$. Each of the 16 constants $d_i$ is not zero (Section 3.5 of the specification lists them), so $s_i \ge 2^8 > 0$. Line L14 computes $v$ modulo $p$, so $0 \le v \le p - 1$, and it replaces $v = 0$ with $p$. So the new cell is in $\{1, \ldots, p\}$. Line L15 only moves cells. By induction on the number of clocks the claim holds. $\square$

So each cell is a 31-bit value, and the halves read by line L8 (bits 30 to 15 and bits 15 to 0) are defined. Because $p \equiv 0 \pmod p$, storing $p$ in place of 0 does not change the cell as an element of $\mathrm{GF}(p)$.

**Lemma 2 (determinism).** The keystream $Z_1, \ldots, Z_n$ is a function of $(k, iv, n)$ only.

*Proof.* Line L1 sets $\sigma$ from $k$, $iv$ and the constants $d_i$. Every later line applies a fixed map to $\sigma$: the bit selections of line L8, XOR, addition modulo $2^{32}$, the fixed maps $L_1$, $L_2$ and $S$, a right shift, the sum of line L14 modulo $p$, and a shift of the cell list. By induction on the number of clocks, each state and each output $Z_t$ is a function of $(k, iv)$. $\square$

**Theorem 1 (correctness).** For each key, IV and message $m$ of $n$ words, the receiver recovers $m$ from $c = m \oplus Z$.

*Proof.* By Lemma 2 the receiver computes the same $Z$, and $(m_t \oplus Z_t) \oplus Z_t = m_t$ for each word, since $Z_t \oplus Z_t = 0$. $\blacksquare$

**Lemma 3.** $L_1$, $L_2$ and $S$ are bijections of the 32-bit words.

*Proof.* Identify a word with a polynomial of degree below 32 in the ring $A = \mathrm{GF}(2)[x]/(x^{32} + 1)$. A left rotation by $j$ is multiplication by $x^j$, so $L_1$ is multiplication by $a_1 = 1 + x^2 + x^{10} + x^{18} + x^{24}$ and $L_2$ by $a_2 = 1 + x^8 + x^{14} + x^{22} + x^{30}$. Over GF(2), $x^{32} + 1 = (x + 1)^{32}$, so an element $a$ of $A$ is a unit if and only if $x + 1$ does not divide $a$, that is, if and only if $a(1) \ne 0$. Each of $a_1$ and $a_2$ has five terms, so $a_1(1) = a_2(1) = 1$. So both are units, and multiplication by a unit is a bijection of $A$. $S$ applies $S_0$ or $S_1$ to each byte, and both tables are permutations of the 256 bytes (the test file checks this), so $S$ is a bijection. $\square$

**Theorem 2 ($\Phi$ is a bijection).** The working-stage clock $\Phi$ is a permutation of the set of states with cells in $\{1, \ldots, p\}$.

*Proof.* Let $\sigma' = \Phi(\sigma)$. We recover $\sigma$ from $\sigma'$. Line L15 gives $s_i = s'_{i-1}$ for $1 \le i \le 15$. Line L13 and Lemma 3 give $L_1^{-1}(S^{-1}(R'_1)) = W_{1L} \| W_{2H}$ and $L_2^{-1}(S^{-1}(R'_2)) = W_{2L} \| W_{1H}$, so $W_1$ and $W_2$ are known. Line L8 reads $X_1$ and $X_2$ only from $s_5, s_7, s_9, s_{11}$, which are known. Line L12 then gives $R_1 = W_1 \boxminus X_1$ and $R_2 = W_2 \oplus X_2$. Last, line L14 with $u = 0$ gives $(1 + 2^8) s_0 \equiv s'_{15} - 2^{15} s_{15} - 2^{17} s_{13} - 2^{21} s_{10} - 2^{20} s_4 \pmod p$. Since $p$ is prime and $1 + 2^8 = 257$ is not a multiple of $p$, the factor is invertible modulo $p$, so $s_0$ is known modulo $p$, and by Lemma 1 it is the unique value in $\{1, \ldots, p\}$ of that residue. So $\Phi$ is injective on a finite set, hence a bijection. $\blacksquare$

**Remark.** These are functional facts. In the initialization stage the input $u = W \gg 1$ also depends on $s_{15}$ and $s_{14}$, and Wu, Huang, Nguyen, Wang and Ling showed that the initialization of version 1.4 was not injective, which version 1.5 fixed. The security of ZUC rests on public analysis, not on a proof.
