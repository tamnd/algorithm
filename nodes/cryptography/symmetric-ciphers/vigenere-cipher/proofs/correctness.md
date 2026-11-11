---
title: Vigenère and autokey decryption invert encryption, and each column of a periodic ciphertext is a Caesar cipher
proves: [correctness]
status: full
---

We identify A to Z with $\mathbb{Z}_{26}$. Let $P$ be a string, and let $p_0, p_1, \ldots, p_{n-1}$ be its letters in order; other characters are copied unchanged by every procedure below. Let $k = k_0 \ldots k_{m-1}$ be a key with $m \ge 1$.

**Claim 1.** VIGENERE-ENCRYPT replaces $p_j$ by $c_j = (p_j + k_{j \bmod m}) \bmod 26$ for each $j$, and keeps every other character at its place.

*Proof.* We show by induction on the number of characters read that, after line L1 has read $t$ characters, the counter $j$ equals the number of letters among them, and the output is the correct prefix. At the start, $t = 0$, $j = 0$ and the output is empty. If the next character is a letter, it is the letter $p_j$ by the induction hypothesis, line L3 outputs $(p_j + k_{j \bmod m}) \bmod 26$, and line L4 raises $j$ by one. Otherwise it is copied and $j$ does not change. In both cases the claim holds after $t + 1$ characters. Line L5 returns the full output. $\square$

**Claim 2.** Decryption with the same key returns $P$.

*Proof.* Decryption is the same procedure with subtraction. Encryption copies non-letters and maps letters to letters, so the ciphertext has the same characters at the same places, and its $j$-th letter is $c_j$. By Claim 1 applied to decryption, the $j$-th letter of the output is $(c_j - k_{j \bmod m}) \bmod 26 = (p_j + k_{j \bmod m} - k_{j \bmod m}) \bmod 26 = p_j$, because $p_j \in \{0, \ldots, 25\}$. Other characters are copied twice and so are unchanged. $\square$

**Claim 3 (autokey).** Let the key stream be $z_j = k_j$ for $j < m$ and $z_j = p_{j-m}$ for $j \ge m$, and let $c_j = (p_j + z_j) \bmod 26$. The autokey decryption returns $P$.

*Proof.* We show by induction on $j$ that the decryption knows $z_j$ when it reads $c_j$ and outputs $p_j$. For $j < m$, $z_j = k_j$ is the primer. For $j \ge m$, $z_j = p_{j-m}$, and $j - m < j$, so by the induction hypothesis the decryption has already output $p_{j-m}$ and appended it to the key stream. In both cases it outputs $(c_j - z_j) \bmod 26 = p_j$. $\square$

**Claim 4 (columns).** For $0 \le i < m$, let $C_i$ be the sequence of the letters $c_j$ with $j \equiv i \pmod m$, and let $P_i$ be the sequence of the letters $p_j$ with $j \equiv i \pmod m$. Then $C_i$ is the Caesar encryption of $P_i$ with shift $k_i$.

*Proof.* If $j \equiv i \pmod m$, then $j \bmod m = i$, so $c_j = (p_j + k_i) \bmod 26$. The two sequences list the same indices $j$ in the same order. $\square$

Claims 1 to 3 prove that decryption inverts encryption, for the periodic cipher and for the autokey variant. Claim 4 is the fact that VIGENERE-BREAK uses: with the right period, subtracting $k_i$ from the column $C_i$ gives a part of the plaintext, so the shift that makes the column look most like English is $k_i$ whenever the statistics of the column are close enough to those of English. That last condition is statistical, so the attack is a heuristic and the claims prove only the correctness of the cipher and of the column split. $\blacksquare$
