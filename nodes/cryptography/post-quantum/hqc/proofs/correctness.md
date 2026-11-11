---
title: HQC decryption returns the message whenever the public code corrects the noise x r2 + r1 y + e, and the KEM then returns the encapsulated key
proves: [correctness]
status: full
---

We use the notation of the page. $\mathcal{R} = \mathbb{F}_2[x]/(x^n - 1)$, $\mathrm{Trunc}$ keeps the first $n_1 n_2$ coordinates, and $\mathcal{C}$ is the public concatenated code with generator matrix $G$ of size $k \times n_1 n_2$. In characteristic 2, subtraction is addition.

**Lemma 1 (truncation is linear).** For $a, b \in \mathcal{R}$, $\mathrm{Trunc}(a + b) = \mathrm{Trunc}(a) + \mathrm{Trunc}(b)$.

*Proof.* Truncation is a coordinate projection, a linear map over $\mathbb{F}_2$. $\square$

**Lemma 2 (the noise).** For a key pair with $s = x + hy$ and a ciphertext $(u, v)$ made by ENCRYPT with $r_1, r_2, e$,

$$v - \mathrm{Trunc}(uy) = mG + \mathrm{Trunc}(x r_2 + r_1 y + e).$$

*Proof.* By Lemma 1, $v - \mathrm{Trunc}(uy) = mG + \mathrm{Trunc}(s r_2 + e + uy)$, where $mG$ already has length $n_1 n_2$. Now $s r_2 + uy = x r_2 + h y r_2 + r_1 y + h r_2 y = x r_2 + r_1 y$, because $\mathcal{R}$ is commutative and $hyr_2 + hr_2y = 0$ in characteristic 2. $\square$

**Lemma 3 (concatenated decoding).** Let $c = \mathcal{C}(m)$ and $z = c + \epsilon$. Split $z$ and $\epsilon$ into $n_1$ blocks of $n_2$ bits. If at most $\lfloor (n_1 - k_1)/2 \rfloor$ blocks are decoded to a wrong byte by the inner decoder, then $\mathcal{C}.\mathrm{Decode}(z) = m$. In particular this holds if at most $\lfloor (n_1 - k_1)/2 \rfloor$ blocks of $\epsilon$ have weight $\ge d_2/2$, where $d_2$ is the inner minimum distance.

*Proof.* The inner decoder returns the byte whose codeword is nearest to the block (it maximizes the correlation, which is $n_2 - 2\,\mathrm{dist}$). If a block of $\epsilon$ has weight below $d_2/2$, the correct inner codeword is the unique nearest one, so that byte is right. The outer Reed-Solomon code has minimum distance $n_1 - k_1 + 1$ and its decoder corrects any $\lfloor (n_1 - k_1)/2 \rfloor$ wrong symbols (syndromes, Berlekamp-Massey and Forney), so it returns the message. $\square$

**Theorem (correctness).** (1) If the noise $\mathrm{Trunc}(x r_2 + r_1 y + e)$ satisfies the condition of Lemma 3, then DECRYPT returns $m$. (2) If DECRYPT returns $m$ in line L11, then DECAPS returns the key $K$ of ENCAPS. Hence

$$\Pr[\mathrm{DECAPS}(sk, c) \ne K] \le \Pr[\mathcal{C}.\mathrm{Decode}(mG + \mathrm{Trunc}(x r_2 + r_1 y + e)) \ne m] = \mathrm{DFR}.$$

*Proof.* (1) is Lemmas 2 and 3. (2) If $m' = m$, then line L12 computes $\theta' = \mathbf{G}(\mathbf{H}(pk), m, \mathrm{salt}) = \theta$. ENCRYPT is a deterministic function of $(pk, m, \theta)$, because $r_1, r_2, e$ are derived from $\theta$, so the re-encryption equals $(u, v)$, and line L13 returns $\mathbf{K}(m, c) = K$. A failure therefore needs $m' \ne m$, which is a decoding failure. $\blacksquare$

**Remark.** For HQC-1 the noise has about 130 ones per 384-bit block, more than $d_2/2 = 96$, so the sufficient condition of Lemma 3 is not what makes HQC work. The inner decoder is a maximum likelihood decoder, and the HQC analysis computes the probability that it fails for the actual distribution of the noise, then bounds the probability that more than 15 of the 46 bytes fail. The theorem above holds for any noise that the decoder corrects; the probability is an analysis of the parameters, not part of the proof of correctness.
