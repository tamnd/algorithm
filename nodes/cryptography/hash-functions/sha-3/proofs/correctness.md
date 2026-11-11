---
title: The SHA3 procedure computes KECCAK[2d](M || 01, d)
proves: [correctness]
status: full
---

We prove that the procedure SHA3 of the page returns $\mathrm{KECCAK}[2d](M \| 01, d)$, the definition of SHA3-$d$ in FIPS 202 Section 6.1, for $d \in \{224, 256, 384, 512\}$ and a message of $n$ bytes. We take as given that KECCAK-F is Keccak-f[1600], which the [Keccak](/keccak/) page proves to be a permutation and which the NIST example values check. Nothing here claims that SHA-3 is secure.

By FIPS 202 Section 5.2, $\mathrm{KECCAK}[c](N, d) = \mathrm{SPONGE}[\text{Keccak-f}[1600], \mathrm{pad10^*1}, 1600 - c](N, d)$. With $c = 2d$ the rate is $1600 - 2d$ bits, which is $r = 200 - 2d/8$ bytes, the value of line L1. For the four values of $d$, $r$ is 144, 136, 104 and 72, all multiples of 8, so a block fills whole lanes.

**Lemma 1 (padding).** Lines L2 to L4 turn $M$ into $P$ with $|P|$ a positive multiple of $r$, and in the bit order of FIPS 202 Appendix B.1, $P = M \| 01 \| \mathrm{pad10^*1}(8r, 8n + 2)$.

*Proof.* In the bit order of Appendix B.1, bit $j$ of a byte is its bit of weight $2^j$. So the byte $\texttt{06}$ is the bit string 0, 1, 1, 0, 0, 0, 0, 0: the suffix 01, the first 1 of pad10*1, and 5 zeros. Line L3 adds zero bytes until $r$ divides $|P|$, and line L4 sets bit 7 of the last byte, which is the last bit of $P$. So, as bits, $P = M \| 01 \| 1 \| 0^k \| 1$ for some $k \ge 0$, and its length $8|P|$ is the least multiple of $8r$ that is at least $8n + 8$, because line L3 adds the fewest bytes.

Algorithm 9 with $x = 8r$ and $m = 8n + 2$ gives $\mathrm{pad10^*1} = 1 \| 0^j \| 1$ with $j = (-m - 2) \bmod x$. So $M \| 01 \| \mathrm{pad10^*1}$ has the form $M \| 01 \| 1 \| 0^j \| 1$, and its length is the least multiple of $8r$ that is at least $8n + 4$. Every multiple of $8r$ is a multiple of 8, and none of $8n + 4, \ldots, 8n + 7$ is a multiple of 8. So the least multiple of $8r$ that is at least $8n + 4$ is also the least that is at least $8n + 8$. The two strings have the same form and the same length, so $k = j$ and they are equal. $\square$

**Lemma 2 (absorbing).** After lines L5 to L8, $A$ is the state $S$ of Algorithm 8 after it has absorbed all blocks of $P$.

*Proof.* Algorithm 8 starts with $S = 0^{1600}$ and, for each block $P_i$, sets $S \leftarrow f(S \oplus (P_i \| 0^c))$. Line L5 sets $A = 0$. Line L7 XORs block $B$ into the first $r/8$ lanes, and, with the byte order of FIPS 202 Section 3.1, this is the XOR of $B \| 0^c$ into the 1600-bit state. Line L8 applies $f$. Induction on the number of blocks gives the claim. $\square$

**Lemma 3 (one squeeze is enough).** For each of the four values of $d$, $d/8 \le r$.

*Proof.* $d/8 \le 200 - d/4$ is the same as $3d/8 \le 200$, that is $d \le 533$, which holds for $d \le 512$. Concretely, $28 \le 144$, $32 \le 136$, $48 \le 104$ and $64 \le 72$. $\square$

**Theorem.** SHA3$(M, d)$ returns $\mathrm{KECCAK}[2d](M \| 01, d)$.

*Proof.* By Lemmas 1 and 2, after line L8 the state is the state of Algorithm 8 at the start of its squeezing phase, for the input $M \| 01$. Algorithm 8 then sets $Z = \mathrm{Trunc}_{8r}(S)$ and returns $\mathrm{Trunc}_d(Z)$ if $d \le |Z|$. By Lemma 3 this happens at once, so the output is the first $d$ bits of $S$. Lines L9 and L10 return the first $d/8$ bytes of the state, which are these bits in the byte order of Section 3.1. $\square$

The number of calls of KECCAK-F is the number of blocks, $|P|/r = \lfloor n/r \rfloor + 1$, because $n + 1 \le |P| < n + 1 + r$ and $r$ divides $|P|$.
