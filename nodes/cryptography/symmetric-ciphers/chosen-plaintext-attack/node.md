---
tag: Z2PZM6
kind: definition
slug: chosen-plaintext-attack
name: Chosen-plaintext attack
aliases:
- CPA
area: cryptography/symmetric-ciphers
level: intro
summary: An attack model in which the adversary gets the encryptions of plaintexts of its choice. Its formal security goal for encryption is IND-CPA.
prereqs: [symmetric-encryption]
see_also: [known-plaintext-attack, ciphertext-only-attack, chosen-ciphertext-attack, semantic-security, ind-cpa-security, ind-cca-security, hybrid-argument, differential-cryptanalysis]
sources:
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Chapter 3, CPA security and CPA security for multiple encryptions; Chapter 5, CCA security
  - url: "https://toc.cryptobook.us/"
    title: Dan Boneh and Victor Shoup, A Graduate Course in Applied Cryptography, version 0.6, 2023
    locator: Chapter 5, chosen plaintext attack
  - paper: "Mihir Bellare, Anand Desai, Eron Jokipii and Phillip Rogaway, A concrete security treatment of symmetric encryption, Proceedings of the 38th IEEE Symposium on Foundations of Computer Science (FOCS), 1997"
    locator: the left-or-right, real-or-random and find-then-guess definitions and the relations between them
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 1, Section 1.13 (classes of attacks on encryption schemes)
---

A chosen-plaintext attack (CPA) is an attack model in which the adversary may obtain the ciphertexts of plaintexts that it chooses, possibly one at a time after seeing earlier answers. It is stronger than a [known-plaintext attack](/known-plaintext-attack/), where the adversary only sees pairs it did not choose, and weaker than a [chosen-ciphertext attack](/chosen-ciphertext-attack/), where it may also ask for decryptions. For [symmetric encryption](/symmetric-encryption/), the security goal under this model is IND-CPA, which is the same as [semantic security](/semantic-security/).

## Definition

**Notation.** $\lambda$ is the security parameter, $k$ the key, $\mathcal{A}$ the adversary, $q$ (or $q_e$) its number of encryption queries and $t$ its running time. The model is the standard model.

**The attack model.** The adversary has an oracle that, on input a plaintext $m$, returns $\mathsf{Enc}_k(m)$ under the secret key $k$. In an *adaptive* CPA, each query may depend on the earlier answers; in a *non-adaptive* (batch) CPA, all queries are fixed in advance. For a block cipher $E$, the oracle is $E_K$, and the number of queries is the *data complexity* of the attack.

**The IND-CPA game.** Let $\Pi = (\mathsf{Gen}, \mathsf{Enc}, \mathsf{Dec})$. For $b \in \{0,1\}$, the game $\mathrm{IND\text{-}CPA}^b_\Pi(\mathcal{A})$ runs as follows.

1. The challenger draws $k \leftarrow \mathsf{Gen}(1^\lambda)$.
2. $\mathcal{A}$ gets the oracle $\mathsf{Enc}_k(\cdot)$. Each call runs $\mathsf{Enc}$ with fresh coins.
3. $\mathcal{A}$ outputs $m_0, m_1$ with $|m_0| = |m_1|$ and gets $c^* \leftarrow \mathsf{Enc}_k(m_b)$.
4. $\mathcal{A}$ may call the oracle again, also on $m_0$ or $m_1$, and then outputs a bit $b'$.

$$\mathrm{Adv}^{\mathrm{ind\text{-}cpa}}_\Pi(\mathcal{A}) = \bigl|\Pr[\mathrm{IND\text{-}CPA}^1_\Pi(\mathcal{A}) = 1] - \Pr[\mathrm{IND\text{-}CPA}^0_\Pi(\mathcal{A}) = 1]\bigr|.$$

$\Pi$ is IND-CPA secure if the advantage is negligible for each probabilistic polynomial-time $\mathcal{A}$. With a uniform bit $b$, the advantage equals $|2\Pr[b' = b] - 1|$.

**The left-or-right form.** In $\mathrm{LOR}^b$, the adversary gets an oracle $\mathrm{LR}_k(m_0, m_1) = \mathsf{Enc}_k(m_b)$ that it may call $q$ times, always with $|m_0| = |m_1|$; plain encryption queries are the case $m_0 = m_1$. Bellare, Desai, Jokipii and Rogaway use this form for concrete bounds.

**Claim.** For each $\mathcal{A}$ in the LOR game with $q$ oracle calls, there is $\mathcal{B}$ in the IND-CPA game with $q - 1$ encryption queries and about the same time, such that $\mathrm{Adv}^{\mathrm{lor}}_\Pi(\mathcal{A}) \le q \cdot \mathrm{Adv}^{\mathrm{ind\text{-}cpa}}_\Pi(\mathcal{B})$.

*Proof.* A [hybrid argument](/hybrid-argument/). For $0 \le i \le q$, let $H_i$ be the world in which the first $i$ calls of $\mathcal{A}$ return $\mathsf{Enc}_k(m_1)$ and the other calls return $\mathsf{Enc}_k(m_0)$. Then $H_0$ is $\mathrm{LOR}^0$ and $H_q$ is $\mathrm{LOR}^1$. Let $p_i = \Pr[\mathcal{A} = 1 \text{ in } H_i]$. $\mathcal{B}$ draws $j$ uniform in $\{1, \ldots, q\}$ and runs $\mathcal{A}$. It answers call $i < j$ with an oracle query on $m_1$, call $i > j$ with an oracle query on $m_0$, and call $j$ with its own challenge on $(m_0, m_1)$. It outputs what $\mathcal{A}$ outputs. If its challenge bit is $b$, $\mathcal{A}$ runs in $H_{j-1+b}$. So $\Pr[\mathcal{B} = 1 \mid b = 1] - \Pr[\mathcal{B} = 1 \mid b = 0] = \frac{1}{q} \sum_{j=1}^{q} (p_j - p_{j-1}) = \frac{1}{q}(p_q - p_0)$, which gives the claim. $\square$

The loss factor $q$ is the price of the single challenge. The converse holds with no loss, because the IND-CPA game is the LOR game with one call that has $m_0 \ne m_1$.

## Examples and non-examples

- **Deterministic encryption fails.** If $\mathsf{Enc}_k$ is deterministic and stateless, $\mathcal{A}$ asks for $\mathsf{Enc}_k(m_0)$, sends the challenge $(m_0, m_1)$ with $m_0 \ne m_1$ and outputs $b' = 0$ exactly when $c^*$ equals the answer. Its advantage is 1 with one query. The proof is on the page [semantic security](/semantic-security/).
- **Differential cryptanalysis of DES.** Biham and Shamir recover the DES key from $2^{47}$ chosen plaintexts. It is a key-recovery attack in the CPA model, with data complexity $2^{47}$. See [differential cryptanalysis](/differential-cryptanalysis/) and [DES](/data-encryption-standard/).
- **Even-Mansour.** Daemen's attack on the two-key [Even-Mansour cipher](/key-whitening/) uses chosen plaintext pairs with a fixed difference. The slide attack of Dunkelman, Keller and Shamir on the one-key variant needs only known plaintexts.
- **Public-key encryption.** Each public-key scheme faces a CPA by design, because anyone can encrypt with the public key. See [IND-CPA security](/ind-cpa-security/) for that setting.
- **Non-example: a known-plaintext attack.** Matsui's linear cryptanalysis of DES uses $2^{43}$ known plaintexts. The adversary does not choose them, so it needs only the weaker model. See [linear cryptanalysis](/linear-cryptanalysis/).
- **Non-example: an attack with decryption queries.** The distinguisher for the 3-round Feistel network on the page [Luby-Rackoff theorem](/luby-rackoff-theorem/) asks one decryption query. It is a chosen-ciphertext attack, not a CPA.

## Related definitions

- **[Ciphertext-only attack](/ciphertext-only-attack/).** The adversary sees ciphertexts only.
- **[Known-plaintext attack](/known-plaintext-attack/).** The adversary sees plaintext and ciphertext pairs that it did not choose.
- **[Chosen-ciphertext attack](/chosen-ciphertext-attack/).** The adversary may also ask for decryptions. IND-CCA1 allows them only before the challenge, and IND-CCA2 also after it, except on $c^*$. CCA security is strictly stronger than CPA security; the randomized counter scheme on the page [symmetric encryption](/symmetric-encryption/) is IND-CPA, but flipping one bit of $c^*$ and decrypting reveals the message. See [IND-CCA security](/ind-cca-security/).
- **[Semantic security](/semantic-security/).** The simulation form of the same goal, equivalent to IND-CPA.
- **PRP and PRF games.** For a block cipher, the CPA model gives the [pseudorandom permutation](/pseudorandom-permutation/) game, and the CCA model gives the strong PRP game.

## References
