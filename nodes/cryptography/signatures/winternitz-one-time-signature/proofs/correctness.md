---
title: Winternitz signatures verify, and the checksum blocks forward walks
proves: [correctness]
status: full
---

**Setting.** $w$ is the chain length, $\ell = \ell_1 + \ell_2$ is the number of chains, and $c^j(x)$ is the value after $j$ steps of the chain function from $x$ (line L4). In classic WOTS a step is $x \mapsto H(x)$. In WOTS+ step number $j$ is $x \mapsto F_k(x \oplus r_j)$, with the key $k$ and the bitmasks $r_1, \ldots, r_{w-1}$ fixed by the public key. CHAIN$(x, a, s)$ applies the steps $a+1, \ldots, a+s$ to $x$.

**Lemma 1 (chains compose).** For all $x$ and all $a, s, t \ge 0$ with $a + s + t \le w - 1$, CHAIN(CHAIN$(x, a, s), a + s, t)$ = CHAIN$(x, a, s + t)$.

*Proof.* The left side applies the steps $a+1, \ldots, a+s$ and then the steps $a+s+1, \ldots, a+s+t$. The right side applies the steps $a+1, \ldots, a+s+t$ in the same order. Each step is a fixed function of its position, so the results are equal. $\square$

**Lemma 2 (an honest signature verifies).** For every key pair made by lines L6 to L9 and every message $M$, VERIFY$(pk, M, \text{SIGN}(sk, pk, M))$ is true.

*Proof.* Let $b = (b_1, \ldots, b_\ell)$ = DIGITS$(M)$. Each $b_i$ is in $\{0, \ldots, w-1\}$: the message digits have $\lg w$ bits each, and the checksum digits are the base $w$ digits of a number below $w^{\ell_2}$. Line L11 gives $\sigma_i$ = CHAIN$(sk_i, 0, b_i)$. Line L12 computes the same $b$, and then CHAIN$(\sigma_i, b_i, w - 1 - b_i)$ = CHAIN$(sk_i, 0, w-1)$ by Lemma 1, which is $pk_i$ by line L8. So each chain ends at its public value, and line L13 returns true. $\square$

**Lemma 3 (the checksum).** Let $b \ne b'$ be the digit strings of two digests (message digits followed by checksum digits, lines L1 to L3). Then there is an index $i$ with $b'_i < b_i$.

*Proof.* Write $d, d'$ for the message parts and $C = \sum_i (w - 1 - d_i)$, $C' = \sum_i (w - 1 - d'_i)$ for the checksums. If some message digit has $d'_i < d_i$, we are done. Otherwise $d'_i \ge d_i$ for every $i \le \ell_1$. The message parts are not equal (if they were, the checksums and so $b$ and $b'$ would be equal), so at least one inequality is strict, and $C' < C$. The checksum digits are the base $w$ digits of $C$ and $C'$, written with the same number $\ell_2$ of digits and the most significant digit first. Two numbers with $C' < C$ differ at a first digit position, and at that position the digit of $C'$ is smaller. That position is an index $i > \ell_1$ with $b'_i < b_i$. $\square$

**Why Lemma 3 is the core of security.** From $\sigma_i$ = $c^{b_i}(sk_i)$ anyone can compute $c^j(sk_i)$ for all $j \ge b_i$ by Lemma 1. A forger who wants to sign $M' \ne M$ with digits $b'$ needs $c^{b'_i}(sk_i)$, or another value that walks to $pk_i$, at each $i$. If $b'_i \ge b_i$ for all $i$, the forger computes the whole signature by walking forward, with no secret. Lemma 3 says that this never happens for a digest with a valid checksum: at some index the forger must walk backward, from position $b_i$ to the lower position $b'_i$.

**Theorem 4 (EUF-1-CMA of WOTS+, Hülsing 2013, proof idea).** Let $A$ forge with chance $\varepsilon$ in time $t$ after one signing query. Then $\varepsilon$ is bounded by the advantages of adversaries of time about $t + 3\ell w$ against the one-wayness (OW), the second preimage resistance (SPR) and the undetectability (UD) of the function family $F$. The bound in the 2013 paper is $\varepsilon \le w \ell \cdot \max\{\mathrm{Adv}^{\mathrm{OW}}, w \cdot \mathrm{Adv}^{\mathrm{SPR}}\} + w \cdot \mathrm{Adv}^{\mathrm{UD}}$. Kudinov, Kiktenko and Fedorov (2020) found a flaw in that proof (an adversary can make the guessed chain position useless, for example by asking to sign a message with digit 0 there) and proved the corrected bound $\varepsilon < \ell w \cdot w \cdot \mathrm{Adv}^{\mathrm{UD}} + \mathrm{Adv}^{\mathrm{OW}} + w \cdot \mathrm{Adv}^{\mathrm{SPR}}$ (their Theorem 1).

*Proof idea.* Assume the message hash has no collision on the queried and the forged message. Let $M$ be the queried message with digits $b$, and let $(M', \sigma')$ be the forgery with digits $b' \ne b$. Take $i$ from Lemma 3, so $b'_i < b_i$. The verifier walks $\sigma'_i$ from position $b'_i$ to position $w - 1$ and reaches $pk_i$. The honest chain $c^{b'_i}(sk_i), \ldots, c^{w-1}(sk_i) = pk_i$ also ends there. Two cases are possible.

1. $\sigma'_i = c^{b'_i}(sk_i)$. Then $A$ found the chain value at position $b'_i < b_i$, below the value $\sigma_i$ that the signature showed. In particular, $A$ computed a preimage of $c^{b_i}(sk_i)$ under step $b_i$. A reduction that plants a one-wayness challenge $y = F_k(x)$ as the chain value at a guessed position, and a guessed chain, turns $A$ into an inverter of $F$. The planted value is $F_k$ of a uniform input and not a chain value, and *undetectability* says that $A$ cannot see the difference.
2. $\sigma'_i \ne c^{b'_i}(sk_i)$. The two walks start at different values and end at the same value, so they meet at a first step $j$, where the inputs $u \ne u'$ to $F_k$ differ and the outputs are equal. Here the bitmasks do the work. A reduction that gets a second preimage challenge $(k, x_c)$ guesses the chain $i$ and the step $j$, makes all secret values itself, and sets the bitmask $r_j = c^{j-1}(sk_i) \oplus x_c$. Then the honest input to $F_k$ at step $j$ of chain $i$ is $x_c$. The bitmask is uniform because $x_c$ is uniform, so the public key has the right distribution. The other input $u'$ is then a second preimage of $x_c$.

The reduction guesses the chain and the positions, and the analysis of these guesses gives the factors of the bound. The proof does not use collision resistance of $F$, so $F$ may have an output of $\lambda$ bits for $\lambda$ bits of security, where a collision resistant function would need $2\lambda$ bits. For classic WOTS, which has no bitmasks, the reduction cannot place the challenge in this way, and the known proofs need collision resistance of $H$ or a random oracle. $\blacksquare$

The theorem is not a full proof. The correctness lemmas above are complete, and the full security proof with the corrected bound is in Kudinov, Kiktenko and Fedorov (2020).
