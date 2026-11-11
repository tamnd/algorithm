---
title: RC5 decryption inverts RC5 encryption
proves: [correctness]
status: full
---

Fix $w$, $r$ and a table $S[0 \ldots 2r+1]$ of $w$-bit words. The proof holds for any table, so it does not depend on the key expansion. All arithmetic is modulo $2^w$.

**Two facts about the operations.**

1. For a fixed $k$, the map $x \mapsto x + k$ is a bijection with inverse $y \mapsto y - k$.
2. For a fixed $s$, the map $x \mapsto x \lll s$ is a bijection with inverse $y \mapsto y \ggg s$: a rotation to the left by $s \bmod w$ places moves bit $j$ to bit $(j + s) \bmod w$, and a rotation to the right by the same amount moves it back. XOR with a fixed word is its own inverse.

**One half-round.** Line L4 maps $(A, B)$ to $(A', B)$ with $A' = ((A \oplus B) \lll B) + S[2i]$. It does not change $B$. Given $(A', B)$, the value $B$ is known, so the facts above give

$$((A' - S[2i]) \ggg B) \oplus B = ((A \oplus B) \lll B) \ggg B \oplus B = (A \oplus B) \oplus B = A.$$

So line L4 is a bijection on pairs, with the inverse $A \leftarrow ((A - S[2i]) \ggg B) \oplus B$. The same argument with $A$ and $B$ exchanged shows that line L5 is a bijection that does not change $A$, with the inverse $B \leftarrow ((B - S[2i+1]) \ggg A) \oplus A$. The rotation amount $A$ in this inverse is the value of $A$ after line L5, which is the same value line L5 used.

**The whole cipher.** Encryption is the composition: line L1, line L2, then for $i = 1, \ldots, r$ line L4 and line L5. Each step is a bijection on pairs, so the composition is a bijection, and its inverse applies the inverse steps in reverse order: for $i = r$ down to 1, first the inverse of line L5 and then the inverse of line L4, then the inverse of line L2 ($B \leftarrow B - S[1]$) and of line L1 ($A \leftarrow A - S[0]$). This is the decryption of the page. $\square$

**Termination.** The loop of line L3 runs $r$ times. The loop of line L11 runs exactly $3 \max(2r + 2, c)$ times. Each step does a fixed amount of work.

**Why the key loop runs $3 \max(t, c)$ times.** This is not needed for correctness. The count makes each word of $S$ and each word of $L$ change at least three times, so that every key byte affects every word of $S$.
