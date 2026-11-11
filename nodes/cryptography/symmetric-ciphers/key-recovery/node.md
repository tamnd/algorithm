---
tag: R1M6AW
kind: problem
slug: key-recovery
name: Key recovery
aliases:
- key recovery attack
area: cryptography/symmetric-ciphers
level: core
summary: Find the secret key of a cipher from access to its encryptions. Attacks are counted in data, time and memory. A distinguisher is easier to build, so PRP security is the stronger goal.
prereqs: [block-cipher, chosen-plaintext-attack]
see_also: [exhaustive-key-search, pseudorandom-permutation, known-plaintext-attack, differential-cryptanalysis, linear-cryptanalysis, related-key-attack, meet-in-the-middle-attack, hellman-time-memory-tradeoff]
sources:
  - url: "https://toc.cryptobook.us/"
    title: Dan Boneh and Victor Shoup, A Graduate Course in Applied Cryptography, version 0.6, 2023
    locator: Chapter 4, block ciphers (security against key recovery, exhaustive search, and why PRP security implies it)
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 7, block ciphers (attack models, data and work complexity, exhaustive key search)
  - paper: "Eli Biham and Adi Shamir, Differential cryptanalysis of the full 16-round DES, Advances in Cryptology, CRYPTO 1992, LNCS 740, Springer, 1993"
    locator: the attack on full DES with 2^47 chosen plaintexts
  - paper: "Mitsuru Matsui, The first experimental cryptanalysis of the Data Encryption Standard, Advances in Cryptology, CRYPTO 1994, LNCS 839, Springer, 1994"
    locator: the linear attack on full DES with 2^43 known plaintexts
  - paper: "Andrey Bogdanov, Dmitry Khovratovich and Christian Rechberger, Biclique cryptanalysis of the full AES, Advances in Cryptology, ASIACRYPT 2011, LNCS 7073, Springer, 2011"
    locator: the key recovery attacks on AES-128, AES-192 and AES-256 with time 2^126.1, 2^189.7 and 2^254.4
---

Key recovery is the problem of finding the secret key of a [block cipher](/block-cipher/), or of another keyed primitive, from access to the primitive under that key. It is the most complete break: with the key, the attacker can decrypt and forge everything. Every cipher with $k$-bit keys can be attacked by [exhaustive key search](/exhaustive-key-search/) in $2^k$ trials, so a key recovery result counts only if it is cheaper. Designers aim for the stronger goal of a [pseudorandom permutation](/pseudorandom-permutation/), because each key recovery attack gives a distinguisher at almost the same cost.

## In plain words

A safe has a secret combination. You may watch the owner open it, or even ask the owner to lock things of your choice inside it, but you never see the combination. Key recovery asks: can you find the combination from what you see?

You can always try every combination. The question is whether there is a faster way. A good lock design leaves no faster way.

People who build ciphers ask for more than this. They want the locked box to give away nothing at all, not even a small pattern. If an attacker cannot even see a pattern, the attacker surely cannot find the key, because the key would show many patterns. So "no pattern" is the harder test for the designer, and the stronger promise for the user.

## Definition

**Notation.** $E : \{0,1\}^k \times \{0,1\}^n \to \{0,1\}^n$ is a block cipher with $k$-bit keys and $n$-bit blocks, $K$ the secret key, $\mathcal{A}$ an adversary that makes $q$ queries and runs in time $t$, counted in evaluations of $E$. All results here are in the standard model unless a line says otherwise.

**The key recovery game.** The challenger draws a uniform $K \in \{0,1\}^k$. The adversary gets an oracle and outputs a key $K'$. Its advantage is

$$\mathrm{Adv}^{\mathrm{kr}}_E(\mathcal{A}) = \Pr\bigl[K' = K\bigr].$$

The oracle sets the attack model.

- **Known plaintext (KPA).** The adversary gets $q$ pairs $(x_i, E_K(x_i))$ with uniform $x_i$ that it does not choose. See [known-plaintext attack](/known-plaintext-attack/).
- **Chosen plaintext (CPA).** The oracle is $E_K$, and each query may depend on earlier answers. See [chosen-plaintext attack](/chosen-plaintext-attack/).
- **Chosen ciphertext (CCA).** The oracles are $E_K$ and $E_K^{-1}$.
- **Ciphertext only (COA).** The adversary sees $E_K(x_i)$ for plaintexts $x_i$ from a known distribution, such as English text. See [ciphertext-only attack](/ciphertext-only-attack/).

Two keys are *equivalent* if they define the same permutation. If a cipher has equivalent keys, success is defined as output of a key equivalent to $K$. For DES and AES no equivalent keys are known.

**How an attack is counted.** A key recovery result gives four numbers, and the comparison with exhaustive search uses all of them.

- **Data** $D$: the number of plaintext and ciphertext pairs, and their type (known or chosen).
- **Time** $T$: the work, in encryptions of the full cipher. Work on smaller units, such as one round or one table lookup, is converted to full encryptions.
- **Memory** $M$: the storage, in blocks of $n$ bits or in words.
- **Success probability** $p$: the chance that the attack outputs the key.

Precomputation that does not depend on $K$, as in a [time-memory tradeoff](/hellman-time-memory-tradeoff/), is counted apart from the online time.

## Variants

- **Partial key recovery.** Find some bits of the key, such as the last round key in [differential cryptanalysis](/differential-cryptanalysis/). The rest of the key is then found by a smaller search.
- **Multi-target key recovery.** There are $T$ keys $K_1, \ldots, K_T$, each with its own oracle, and the attacker wins if it finds any one of them. A single search finds one key after about $2^k/T$ trials.
- **[Related-key attack](/related-key-attack/).** The attacker may also query $E_{\phi(K)}$ for maps $\phi$ of its choice, such as $\phi(K) = K \oplus \Delta$. This is a stronger oracle, and it is relevant when keys are derived from each other.
- **Side-channel key recovery.** The attacker also measures time, power or cache state during encryption. See [timing attack](/timing-attack/).
- **Quantum key recovery.** With quantum access to the search, [Grover search](/grover-search/) needs about $2^{k/2}$ evaluations of $E$.

## Examples

**XOR with the key.** For $E_K(x) = x \oplus K$, one known pair gives $K = x \oplus E_K(x)$. So $D = 1$, $T = 1$ and $p = 1$.

**A 16-bit toy cipher.** The toy 6-round cipher with 16-bit key and block on the page [exhaustive key search](/exhaustive-key-search/) maps the plaintext 0x0000 to 0xB88A under both keys 0x0004 and 0x88CB. With one pair, the search cannot decide between them. The second pair, with plaintext 0xFFFF, gives 0xBA52 and 0xB5DC, which separates them. Over all $2^{16}$ keys and the plaintext 0x0000, the mean number of wrong keys that agree with one pair is 0.990, close to $(2^{16} - 1)/2^{16}$.

**Attacks on full DES and AES.** The table gives the main published key recovery attacks.

| cipher | attack | data | time | source |
|---|---|---|---|---|
| DES | exhaustive search | 1 known pair | $2^{56}$ | generic |
| DES | differential cryptanalysis | $2^{47}$ chosen plaintexts | about $2^{37}$ | Biham and Shamir 1992 |
| DES | linear cryptanalysis | $2^{43}$ known plaintexts | about $2^{43}$ | Matsui 1994 |
| AES-128 | biclique | $2^{88}$ chosen plaintexts | $2^{126.1}$ | Bogdanov, Khovratovich and Rechberger 2011 |
| AES-256 | biclique | $2^{40}$ chosen plaintexts | $2^{254.4}$ | same |

The biclique attacks are faster than exhaustive search only by a small factor and need much data, so they do not threaten AES in practice. The DES attacks show that the data cost matters: Matsui's attack needs $2^{43}$ pairs, which an attacker rarely gets, so in practice DES fell to exhaustive search (the EFF machine of 1998, see [DES](/data-encryption-standard/)).

## Known algorithms

- **[Exhaustive key search](/exhaustive-key-search/).** Generic, $2^k$ trials in the worst case and about $2^{k-1}$ on average.
- **[Time-memory tradeoffs](/hellman-time-memory-tradeoff/).** Hellman's method and [rainbow tables](/rainbow-table/) precompute in $2^k$ time and then recover a key for a fixed chosen plaintext in time and memory about $2^{2k/3}$ each.
- **[Meet-in-the-middle](/meet-in-the-middle-attack/).** For a cipher that is a composition of two independent parts, such as double encryption, about $2^{k_1} + 2^{k_2}$ time instead of $2^{k_1 + k_2}$. See [Triple DES](/triple-des/).
- **[Differential](/differential-cryptanalysis/) and [linear cryptanalysis](/linear-cryptanalysis/).** Statistical attacks that recover the last round key bits from many pairs.
- **[Slide attacks](/slide-attack/).** Attacks on ciphers with identical rounds, with cost that does not depend on the number of rounds. The slide attack on the [Even-Mansour cipher](/key-whitening/) is one example.
- **[Integral](/integral-cryptanalysis/) and [boomerang](/boomerang-attack/) attacks.** Used mainly on reduced-round versions of AES and other ciphers.

## Bounds

**Exhaustive search is always possible.** With $s$ known pairs, the wrong keys that agree with all pairs are false positives. If each wrong key acts like an independent random permutation, the expected number of false positives is

$$\frac{2^k - 1}{2^n (2^n - 1) \cdots (2^n - s + 1)} \approx 2^{k - sn}.$$

So $s = \lceil k/n \rceil + 1$ pairs make the key unique with high probability: one or two for DES ($2^{56 - 64} = 2^{-8}$ with one pair), two for AES-128, and three for AES-256.

**Key recovery is weaker than distinguishing.** Let $\mathcal{A}$ recover the key with probability $\varepsilon$ in time $t$ with $q$ queries. Build a PRP distinguisher $\mathcal{B}$ with oracle $O$: run $\mathcal{A}$ with $O$ to get $K'$, pick a point $x$ that $\mathcal{A}$ did not query, query $O(x)$, and output 1 if $O(x) = E_{K'}(x)$.

- If $O = E_K$, then $\mathcal{B}$ outputs 1 when $K' = K$, so with probability at least $\varepsilon$.
- If $O$ is a random permutation $\pi$, then $\pi(x)$ is uniform on the $2^n - q$ values that $\pi$ did not take on the queried points, and $K'$ is fixed before $\pi(x)$ is drawn. So $\mathcal{B}$ outputs 1 with probability at most $1/(2^n - q)$.

So $\mathrm{Adv}^{\mathrm{prp}}_E(\mathcal{B}) \ge \varepsilon - 1/(2^n - q)$, with $q + 1$ queries and time $t + 1$. The reduction is tight. Each PRP bound for $E$ is therefore also a key recovery bound.

**The converse is false.** Let $E$ be a good cipher on $n$-bit blocks and let $E'_K(x_1 \| x_2) = x_1 \| E_K(x_2)$ on $2n$-bit blocks. Key recovery on $E'$ is exactly as hard as on $E$, because the left half carries no information about $K$. But one query distinguishes $E'$ from a random permutation of $2n$-bit strings: output 1 if the left half of the answer equals $x_1$. This happens with probability 1 for $E'$ and $2^{-n}$ for a random permutation, so the advantage is $1 - 2^{-n}$. This is why the designer asks for PRP security: a cipher that resists every distinguisher resists every key recovery attack, but not the other way around.

**Quantum search.** [Grover search](/grover-search/) finds a key in about $2^{k/2}$ evaluations of $E$, run as a quantum circuit. The page on Grover search gives the matching lower bound for unstructured search.

## Reductions

- Key recovery for $E$ reduces to PRP distinguishing for $E$, with no loss, by the argument in Bounds.
- Key recovery for double encryption $E_{K_2} \circ E_{K_1}$ reduces to two searches of size $2^k$ by [meet-in-the-middle](/meet-in-the-middle-attack/), so it costs about $2^{k+1}$, not $2^{2k}$.
- Key recovery for the two-key [Even-Mansour cipher](/key-whitening/) $P(x \oplus K_1) \oplus K_2$ reduces to a collision search with about $2^{n/2}$ queries and $2^{n/2}$ evaluations of $P$.

## Applications

- **Key lengths.** Guidance such as NIST SP 800-57 Part 1 sets key lengths so that exhaustive search is out of reach. This is why 56-bit DES is broken and 128-bit AES is not.
- **Reporting cryptanalysis.** A new attack is stated as data, time, memory and success probability, and is compared with exhaustive search on the same key length.
- **Security margins.** Attacks on reduced-round versions measure how many rounds a cipher has to spare. For example, the best key recovery attacks on AES-128 reach far fewer than 10 rounds when the cost must be well below $2^{128}$.

## References
