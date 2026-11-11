---
title: The bit-by-bit register computes the CRC, and an error is missed exactly when the generator divides it
proves: [correctness, termination]
status: full
---

Notation. $G(x) = x^r + P(x)$ with $\deg P < r$ is the generator, and `poly` is $P$ as an $r$-bit word. The message bits, in the order in which they enter the register (after the reflection of each byte when refin is true), are $m_0, m_1, \ldots, m_{k-1}$. The prefix polynomial is $M_j(x) = \sum_{i < j} m_i x^{j-1-i}$, so $M_{j+1} = x M_j + m_j$ and $M = M_k$. A register word $R$ of $r$ bits is the polynomial with bit $i$ as the coefficient of $x^i$.

**Lemma 1 (one step).** If the register holds $R$ with $\deg R < r$ and the next bit is $b$, then after lines L6 to L8 it holds $(x R + b x^r) \bmod G$.

*Proof.* Let $t$ be the coefficient of $x^{r-1}$ in $R$ (the top bit). Then $x R + b x^r = (t + b) x^r + x (R - t x^{r-1})$. The second term has degree less than $r$, and as a word it is $(R \ll 1)$ masked to $r$ bits, which is line L7. Since $G = x^r + P$, we have $x^r \equiv P \pmod G$, so $x R + b x^r \equiv (t \oplus b) P + x(R - t x^{r-1})$. Both terms have degree less than $r$, so this sum is the remainder. Line L6 computes $t \oplus b$, and line L8 adds $P$ exactly when it is 1. $\square$

**Lemma 2 (invariant).** After $j$ message bits, the register holds $(I x^j + M_j x^r) \bmod G$, where $I$ is the polynomial of init.

*Proof.* By induction on $j$. For $j = 0$, line L2 sets the register to $I$, and $\deg I < r$, so $I = I \bmod G$. Assume the claim for $j$. By Lemma 1 with $b = m_j$, the new register is $(x (I x^j + M_j x^r) + m_j x^r) \bmod G = (I x^{j+1} + (x M_j + m_j) x^r) \bmod G = (I x^{j+1} + M_{j+1} x^r) \bmod G$. The reduction of the old register before the multiplication by $x$ does not change the result, because reduction modulo $G$ commutes with multiplication by $x$ and with addition. $\square$

**Theorem 1 (the CRC).** The function `crc` returns $\rho\big((I x^k + M x^r) \bmod G\big) \oplus X$, where $\rho$ reverses the $r$ bits when refout is true and is the identity otherwise, and $X$ is xorout. This is the CRC of the Rocksoft model. When $k \ge r$, the term $I x^k$ equals $I x^{k-r} \cdot x^r$, so init is the same as an XOR of $I$ into the first $r$ message bits.

*Proof.* Lemma 2 with $j = k$, then lines L9 and L10. $\square$

**Termination.** The loop of line L3 runs once for each byte and the loop of line L5 eight times for each byte, so the number of steps is exactly $8n$ for $n$ bytes.

**Lemma 3 (a byte at a time).** Assume $r \ge 8$. Feeding the byte $v$ (as 8 bits, top bit first) to the register $R$ gives the same result as: XOR $v$ into the top 8 bits of $R$, then run 8 steps with input bit 0.

*Proof.* By Lemma 2 applied to 8 bits, feeding $v$ gives $(x^8 R + v x^r) \bmod G = x^8 (R + v x^{r-8}) \bmod G$. The word $R \oplus (v \ll (r-8))$ is the polynomial $R + v x^{r-8}$, and 8 steps with input 0 multiply it by $x^8$ modulo $G$, by Lemma 1 with $b = 0$. $\square$

**Lemma 4 (the reflected register).** Let $\bar R$ be the bit reversal of an $r$-bit word $R$, and $\bar P$ the reversal of `poly`. The function `crc_reflected` keeps $\bar R$, where $R$ is the register of `crc_register`.

*Proof.* Bit reversal maps the top bit of $R$ to the low bit of $\bar R$, maps $(R \ll 1)$ masked to $r$ bits to $\bar R \gg 1$, and maps an XOR with $P$ to an XOR with $\bar P$. So one step of Lemma 1 with input 0 on $R$ is the step `reg = (reg >> 1) ^ rpoly if reg & 1 else reg >> 1` on $\bar R$. With refin true, the byte that enters is the reversal $\bar v$ of the stored byte $v$, and an XOR of $\bar v$ into the top 8 bits of $R$ is an XOR of $v$ into the low 8 bits of $\bar R$. By Lemma 3 the two loops agree byte by byte. At the start, $\bar R = \bar I$, which is the initial value in the code. At the end, refout reverses $R$, which gives $\bar R$, so no final reversal is necessary. $\square$

**Theorem 2 (which errors are missed).** Take refin and refout false. Send the codeword $T = M x^r + C$, where $C$ is the CRC word, written after the message. Let the channel add an error $E(x)$ of degree less than $k + r$, so the receiver gets $T + E$, with message part $M'$ and check part $C'$. The receiver accepts if the CRC of $M'$ equals $C'$. It accepts if and only if $G$ divides $E$.

*Proof.* Write $E = E_M x^r + E_C$ with $\deg E_C < r$. Then $M' = M + E_M$ and $C' = C + E_C$, and $M'$ has the same length $k$. By Theorem 1, $\mathrm{crc}(M') = (I x^k + M x^r + E_M x^r) \bmod G \oplus X = C \oplus (E_M x^r \bmod G)$. So the receiver accepts if and only if $E_M x^r \bmod G = E_C$. Since $\deg E_C < r$, this holds if and only if $E_M x^r + E_C \equiv 0 \pmod G$, that is, $G \mid E$. $\square$

With reflection, the same holds after a fixed permutation of the bit positions: refin reverses each byte, and the CRC written least significant byte first with refout reverses the check field. A fixed permutation does not change the weight of an error, and a burst on a serial line that sends each byte least significant bit first stays a burst.

**Theorem 3 (any value can be reached).** For each message $M$ and each target $t$, there is a suffix $S$ of $r$ bits with $\mathrm{crc}(M \Vert S) = t$.

*Proof.* By Lemma 2, the register after $M \Vert S$ is $(R + S) x^r \bmod G$, where $R$ is the register after $M$. Since $G(0) = 1$, $\gcd(x, G) = 1$, so $x^r$ has an inverse modulo $G$, and $S \mapsto (R + S) x^r \bmod G$ is a bijection of the polynomials of degree less than $r$. Take the $S$ that maps to the register value whose output is $t$. $\square$
