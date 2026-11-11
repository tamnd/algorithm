---
title: The SHAKE procedure returns a prefix of KECCAK[c](M || 1111), however the output is read
proves: [correctness]
status: full
---

We prove that the procedure SHAKE of the page returns the first $\ell$ bytes of $\mathrm{KECCAK}[c](M \| 1111)$ with $c = 2s$, which is the definition of SHAKE128 ($s = 128$) and SHAKE256 ($s = 256$) in FIPS 202 Section 6.2. We also prove that reading the output in pieces gives the same bytes. We take as given that KECCAK-F is Keccak-f[1600]; the [Keccak](/keccak/) page proves that it is a permutation, and the NIST example values check the code. Nothing here claims that SHAKE is secure.

Write $f$ for KECCAK-F. Line L1 sets $r = 200 - s/4$ bytes, which is $1600 - 2s = 1600 - c$ bits, the rate of KECCAK[$c$]: 168 bytes for $s = 128$ and 136 for $s = 256$.

**Lemma 1 (padding).** Lines L2 to L4 turn $M$ into $P$ with $|P|$ a positive multiple of $r$, and in the bit order of FIPS 202 Appendix B.1, $P = M \| 1111 \| \mathrm{pad10^*1}(8r, 8n + 4)$.

*Proof.* In the bit order of Appendix B.1, the byte $\texttt{1F}$ is the bit string 1, 1, 1, 1, 1, 0, 0, 0: the suffix 1111, the first 1 of pad10*1 and three zeros. As bits, $P = M \| 1111 \| 1 \| 0^k \| 1$, and $8|P|$ is the least multiple of $8r$ that is at least $8n + 8$. Algorithm 9 with $x = 8r$ and $m = 8n + 4$ gives $1 \| 0^j \| 1$ with $j = (-m - 2) \bmod x$, so $M \| 1111 \| \mathrm{pad10^*1}$ has the same form and its length is the least multiple of $8r$ that is at least $8n + 6$. No multiple of 8 lies in $8n + 6, 8n + 7$, so the two lengths are equal, $k = j$, and the strings are equal. $\square$

**Lemma 2 (absorbing).** After the loop of lines L5 and L6, $A = S_0$, the state of Algorithm 8 after it has absorbed $P$, and $buf$ holds $\mathrm{Trunc}_r(S_0)$.

*Proof.* Algorithm 8 starts with $S = 0^{1600}$ and sets $S \leftarrow f(S \oplus (P_i \| 0^c))$ for each block $P_i$. Lines L5 and L6 do the same, block by block, with the byte order of FIPS 202 Section 3.1. After the last block, line L6 has set $buf$ to the first $r$ bytes of $A = S_0$. $\square$

Let $S_{i+1} = f(S_i)$ and let $Z = \mathrm{Trunc}_r(S_0) \| \mathrm{Trunc}_r(S_1) \| \cdots$, an infinite string of bytes. By Algorithm 8, $\mathrm{KECCAK}[c](M \| 1111, 8\ell)$ is the first $\ell$ bytes of $Z$ for every $\ell$.

**Lemma 3 (the invariant).** Before and after each run of the body of the loop of lines L7 to L9, and between calls, there is a $k \ge 0$ such that $A = S_k$, the bytes produced so far (in all calls together) followed by $buf$ equal the first $(k + 1) r$ bytes of $Z$.

*Proof.* By Lemma 2 it holds at the start with $k = 0$ and nothing produced. If $buf$ is empty, line L8 sets $A = f(S_k) = S_{k+1}$ and $buf = \mathrm{Trunc}_r(S_{k+1})$, the bytes $(k + 1) r$ to $(k + 2) r - 1$ of $Z$; the invariant holds with $k + 1$. Line L9 moves bytes from the front of $buf$ to the end of the output, which does not change the output followed by $buf$. $\square$

**Theorem.** A call SHAKE$(M, s, \ell)$ returns the first $\ell$ bytes of $Z$, which is $\mathrm{SHAKE}s(M, 8\ell)$. If the output is instead read in calls of sizes $\ell_1, \ell_2, \ldots$, the concatenated result is the first $\ell_1 + \ell_2 + \cdots$ bytes of $Z$.

*Proof.* Each run of the loop body adds at least one byte to the output, because after line L8 the buffer is not empty, and $\min(\ell - |out|, |buf|) \ge 1$ while $|out| < \ell$. So the loop ends, and it ends with exactly $\ell$ bytes in this call, since line L9 never takes more than $\ell - |out|$. By Lemma 3, everything produced so far is a prefix of $Z$, so the call returns the next bytes of $Z$ after those produced by earlier calls. With one call, this is the first $\ell$ bytes. $\square$

The number of calls of $f$ is $\lfloor n/r \rfloor + 1$ for absorbing, by Lemma 1, and $\lceil \ell/r \rceil - 1$ for squeezing when $\ell \ge 1$, because line L8 runs only when the $r$ bytes already in $buf$ are used up.
