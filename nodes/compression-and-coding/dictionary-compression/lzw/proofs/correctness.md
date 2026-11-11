---
title: LZW decoding inverts LZW encoding, including the KwKwK case
proves: [correctness]
status: full
---

Let $T = T[1..n]$ with $n \ge 1$ over the alphabet $\{0, \ldots, \sigma - 1\}$. Let LZW-ENCODE output the codes $c_1, \ldots, c_m$. For $k = 1, \ldots, m$ let $u_k$ be the string $w$ whose code is written as $c_k$ (in line L6 or line L9), and for $k < m$ let $a_k$ be the symbol $T[i]$ of the round in which $c_k$ is written. Write $E_k$ for the dictionary of the encoder just after $c_k$ is written and line L7 has run (for $k < m$).

**Lemma 1 (the encoder).**

1. $T = u_1 u_2 \cdots u_m$, and for $k < m$, $a_k$ is the first symbol of $u_{k+1}$.
2. Code $\sigma + k - 1$ is assigned in the round of $c_k$ to the string $u_k a_k$, for $k = 1, \ldots, m - 1$. So $E_k$ holds the single symbols and the codes $\sigma, \ldots, \sigma + k - 1$.
3. $c_k$ is the code of $u_k$ in the dictionary at the time it is written, which is $E_{k-1}$ (with $E_0$ the single symbols).

*Proof.* The variable $w$ is always a string of $D$: it starts as $T[1]$, line L4 extends it only to a string in $D$, and line L8 sets it to one symbol. A phrase ends in line L6 when $w \cdot T[i] \notin D$; then $u_k = w$, $a_k = T[i]$, line L7 adds $u_k a_k$ with code $next$, and line L8 starts the next phrase with $T[i] = a_k$. Line L9 writes the last phrase. The phrases are consecutive, so (1) holds. Codes are assigned in order from $\sigma$, one per phrase but the last, which gives (2). Line L6 runs before line L7, so $c_k$ is looked up in $E_{k-1}$, which gives (3). $\square$

**Lemma 2 (the decoder).** For $k = 1, \ldots, m$, after the decoder has handled $c_k$ (line L11 for $k = 1$, lines L13 to L17 for $k \ge 2$):

1. its output is $u_1 \cdots u_k$, and $prev = u_k$;
2. its dictionary holds the single symbols and, for $1 \le t \le k - 1$, the code $\sigma + t - 1$ with the string $u_t a_t$; so it equals $E_{k-1}$, and its $next$ is $\sigma + k - 1$.

*Proof.* By induction on $k$. For $k = 1$: $u_1$ is a single symbol, since $E_0$ has only single symbols, so line L11 sets $prev = D[c_1] = u_1$ and outputs it; the dictionary is $E_0$ and $next = \sigma$.

Let $k \ge 2$ and assume the claim for $k - 1$: the dictionary is $E_{k-2}$, $next = \sigma + k - 2$ and $prev = u_{k-1}$. By Lemma 1(3), $c_k$ is a code of $E_{k-1}$, which is $E_{k-2}$ plus the one code $\sigma + k - 2$ for $u_{k-1} a_{k-1}$. Two cases.

- If $c_k < next$, then $c_k$ is in $E_{k-2}$ and the decoder has the same string for it, so line L13 sets $cur = u_k$.
- If $c_k = next = \sigma + k - 2$, then $u_k = u_{k-1} a_{k-1}$. By Lemma 1(1), $a_{k-1}$ is the first symbol of $u_k$, which is the first symbol of $u_{k-1}$ since $u_{k-1}$ is a nonempty prefix of $u_k$. So $u_k = u_{k-1} \cdot u_{k-1}[1] = prev \cdot prev[1]$, which line L14 builds. This is the KwKwK case.

There is no other case, since $c_k \le \sigma + k - 2$. Line L15 outputs $u_k$, so the output is $u_1 \cdots u_k$. Line L16 adds code $\sigma + k - 2$ with $prev \cdot cur[1] = u_{k-1} \cdot (\text{first symbol of } u_k) = u_{k-1} a_{k-1}$, so the dictionary becomes $E_{k-1}$ and $next = \sigma + k - 1$. Line L17 sets $prev = u_k$. $\square$

**Theorem.** LZW-DECODE(LZW-ENCODE$(T)$) $= T$.

*Proof.* By Lemma 2 with $k = m$ the decoder outputs $u_1 \cdots u_m$, which is $T$ by Lemma 1(1). $\square$

**Remark (the phrases are longest matches).** Every string in the encoder's dictionary is a single symbol or an earlier entry plus one symbol, so the set of entries is closed under prefixes. Line L4 extends $w$ as long as $w \cdot T[i]$ is an entry, so each $u_k$ is the longest entry of $E_{k-1}$ that is a prefix of the rest of $T$. Correct decoding does not need this fact.

**Remark (bit streams).** With codes packed in a stream, the decoder must also read each code with the width that the encoder used. In the format of the reference implementation, $c_k$ is written with the bit length of $\sigma' + k - 2$, the largest code the encoder has assigned, where $\sigma'$ is the first free code; by Lemma 2 the decoder's $next$ at that moment is $\sigma' + k - 2$, and it reads with the bit length of that value. The first code, and the first code after a clear, is read with the bit length of $\sigma' - 1$, the largest reserved code, as the encoder wrote it. So both sides use the same width for every code.
