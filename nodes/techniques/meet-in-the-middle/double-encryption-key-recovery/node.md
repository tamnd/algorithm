---
tag: WJ6SCW
kind: problem
slug: double-encryption-key-recovery
name: Double-encryption key recovery
aliases:
- double-DES key recovery
area: techniques/meet-in-the-middle
level: intro
summary: Recover both keys of a two-fold block cipher encryption from known plaintext-ciphertext pairs.
prereqs: [block-cipher, known-plaintext-attack, exhaustive-key-search]
see_also: [meet-in-the-middle-attack, triple-des, data-encryption-standard, parallel-collision-search, ideal-cipher-model, time-memory-tradeoff, horowitz-sahni-algorithm]
sources:
  - paper: doi:10.1109/C-M.1977.217750
    title: Whitfield Diffie and Martin E. Hellman, Exhaustive cryptanalysis of the NBS Data Encryption Standard, Computer 10(6) (1977), 74-84
    locator: the discussion of multiple encryption with DES
  - paper: doi:10.1145/358699.358718
    title: Ralph C. Merkle and Martin E. Hellman, On the security of multiple encryption, Communications of the ACM 24(7) (1981), 465-467
    locator: the attacks on double encryption and on triple encryption with two keys
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography
    locator: Chapter 7 (block ciphers), the part on multiple encryption
  - paper: doi:10.1007/PL00003816
    title: Paul C. van Oorschot and Michael J. Wiener, Parallel collision search with cryptanalytic applications, Journal of Cryptology 12(1) (1999), 1-28
    locator: the application to meet-in-the-middle attacks
---

Double-encryption key recovery asks for the two keys $k_1, k_2$ of a double encryption $C = E_{k_2}(E_{k_1}(P))$ of a [block cipher](/block-cipher/), given a few [known plaintext-ciphertext pairs](/known-plaintext-attack/). With $k$-bit keys, [exhaustive search](/exhaustive-key-search/) over the key pairs costs about $2^{2k}$ encryptions, but the [meet-in-the-middle attack](/meet-in-the-middle-attack/) solves it with about $2^{k+1}$ encryptions and memory for $2^k$ blocks. This gap is the reason why double DES is not used and why [triple DES](/triple-des/) has three stages.

## In plain words

A message is locked twice, first with one secret key and then with a second secret key. You know some messages and their locked forms. You want the two keys.

The obvious way tries every first key with every second key. That is the number of keys times itself. A better way starts from both ends and looks for a value that both sides reach in the middle, so the work is about twice the number of keys, but it needs a large table.

One known message is often not enough to fix the keys, because many wrong pairs of keys can lock that message in the same way by chance. Each extra known message removes most of the wrong pairs.

## Definition

**Input.** A block cipher with key space $\mathcal{K} = \{0,1\}^k$ and block space $\mathcal{B} = \{0,1\}^n$: for each key $\kappa$, a permutation $E_\kappa$ of $\mathcal{B}$ and its inverse $D_\kappa$, both computable. And $t \ge 1$ pairs $(P_1, C_1), \ldots, (P_t, C_t) \in \mathcal{B}^2$ with distinct $P_i$, made with unknown keys $k_1, k_2$: $C_i = E_{k_2}(E_{k_1}(P_i))$ for each $i$.

**Output.** The set of consistent key pairs

$$R = \{(\kappa_1, \kappa_2) \in \mathcal{K}^2 : E_{\kappa_2}(E_{\kappa_1}(P_i)) = C_i \text{ for } i = 1, \ldots, t\},$$

or, in the search form, one element of $R$. The true pair $(k_1, k_2)$ is in $R$, so $R$ is not empty. The cost is counted in evaluations of $E$ and $D$ and in memory, in blocks.

## Variants

- **One pair or several.** With one pair, $R$ is large in general. In the [ideal cipher model](/ideal-cipher-model/), each wrong key pair passes $t$ pairs with distinct plaintexts with probability $1/(N(N-1)\cdots(N-t+1))$, where $N = 2^n$. So the expected number of wrong pairs in $R$ is about $2^{2k - tn}$. The true pair is likely to be the only one when $t n > 2k$.
- **Search or listing.** Return one consistent pair, or all of them. The meet-in-the-middle attack lists all of them at no extra cost beyond the size of the list.
- **Known or chosen plaintext.** With chosen plaintexts the attacker picks the $P_i$. The meet-in-the-middle attack on double encryption needs only known plaintexts. Chosen plaintexts matter for triple encryption with two keys.
- **Triple encryption with three keys.** $C = E_{k_3}(E_{k_2}(E_{k_1}(P)))$, or the form $E_{k_3} D_{k_2} E_{k_1}$ of [triple DES](/triple-des/). A table on one side and a search over the two keys on the other side cost about $2^{2k}$ encryptions and $2^k$ memory.
- **Triple encryption with two keys.** The form $E_{k_1} D_{k_2} E_{k_1}$. Merkle and Hellman give a chosen-plaintext attack with about $2^k$ operations, $2^k$ words of memory and about $2^k$ chosen plaintexts.
- **Different ciphers.** The two stages can use two different ciphers. Nothing in the problem or in the attacks needs the same cipher twice.

## Examples

The toy cipher of the [meet-in-the-middle attack](/meet-in-the-middle-attack/) page has 8-bit blocks and 4-bit keys: with $\kappa = 17k$, $E_k(x) = (\mathrm{rotl}_3(x \oplus \kappa) + \kappa) \bmod 256$. There are 256 key pairs. The secret keys are $k_1 = 3$ and $k_2 = 10$.

| known pairs $(P_i, C_i)$ | consistent key pairs $(\kappa_1, \kappa_2)$ |
|---|---|
| (42, 52) | (1, 9), (3, 10), (10, 5) |
| (85, 16) | (0, 14), (1, 6), (2, 4), (2, 15), (3, 10), (6, 2), (7, 3), (9, 2) |
| (85, 16), (42, 52) | (3, 10) |
| (42, 52), (100, 228) | (3, 10) |
| (42, 52), (42, 53) | none: the pairs are not from one key pair |

An ideal cipher with these sizes gives on average $1 + 255/256 \approx 2$ consistent pairs for one known pair. This toy cipher is far from ideal: over the 256 plaintexts with the secret keys $(3, 10)$, the average is about 2.79, and the plaintext 85 gives 8.

For DES, $k = 56$ and $n = 64$. One known pair leaves about $2^{112 - 64} = 2^{48}$ wrong key pairs, and two known pairs leave about $2^{-16}$ in expectation. So two known pairs are almost always enough to fix the keys.

## Known algorithms

| algorithm | cipher calls | memory | notes |
|---|---|---|---|
| [Exhaustive search](/exhaustive-key-search/) over pairs | about $2^{2k+1}$ | $O(1)$ | tries each $(\kappa_1, \kappa_2)$ on the first pair |
| [Meet-in-the-middle attack](/meet-in-the-middle-attack/) | $2^{k+1}$ plus the filter | $2^k$ entries | Diffie and Hellman, 1977 |
| Meet in the middle with $r$ partial tables | about $(r + 1) 2^k$ | $2^k / r$ entries | the time-memory product stays near $2^{2k}$ |
| [Parallel collision search](/parallel-collision-search/) | more than $2^{k+1}$ | much less than $2^k$ | van Oorschot and Wiener, 1999; runs on many processors |

The filter of the meet-in-the-middle attack checks each candidate of the first pair on the other pairs. With an ideal cipher and $t$ pairs it costs about $2(t - 1)(1 + 2^{2k - n})$ cipher calls in expectation.

## Bounds

**Upper bound.** The meet-in-the-middle attack solves the problem with $2^{k+1}$ cipher calls, plus $2(t-1)c$ for the filter, where $c$ is the number of key pairs that match the first pair, and with a table of $2^k$ entries. With a hash table, the other work is $O(2^k + c)$ expected time. In the ideal cipher model, $\mathbb{E}[c] = 1 + (2^{2k} - 1)/2^n$.

**A data lower bound.** Fix the plaintexts $P_1, \ldots, P_t$. The map from a key pair to its ciphertext tuple $(C_1, \ldots, C_t)$ has $2^{2k}$ inputs and at most $2^{nt}$ values. By the pigeonhole principle, some ciphertext tuple is consistent with at least $\lceil 2^{2k - nt} \rceil$ key pairs. So when $t < 2k/n$, no algorithm can always name the true pair: for some keys, $R$ has more than one element and the data cannot tell them apart. For double DES, $2k/n = 112/64 = 1.75$, so one known pair is never enough for every key pair.

**Time and memory.** For exhaustive search, for the meet-in-the-middle attack and for its partial-table form, the product of the number of cipher calls and the memory is about $2^{2k}$ or more. The methods with less than $2^k$ memory pay with more time.

## Reductions

- **Single-key recovery is a special case.** In the variant with two different ciphers, let the second cipher be the identity for every key. Then the problem is key recovery for one encryption, which [exhaustive key search](/exhaustive-key-search/) solves with about $2^k$ cipher calls.
- **It reduces to a collision search.** Define $f_1(\kappa) = E_\kappa(P_1)$ and $f_2(\kappa) = D_\kappa(C_1)$. A candidate pair is a pair $(\kappa_1, \kappa_2)$ with $f_1(\kappa_1) = f_2(\kappa_2)$: a claw between two functions. [Collision finding](/collision-finding/) methods, such as parallel collision search, find such claws with little memory.
- **The same split as subset sum.** The [Horowitz-Sahni algorithm](/horowitz-sahni-algorithm/) for subset sum splits the items in two halves and matches sums in the middle, in the same way as the attack matches blocks in the middle.

## Applications

- **Why double DES gives about 57 bits, not 112.** Double DES has a 112-bit key, but the meet-in-the-middle attack recovers it with about $2^{57}$ DES operations and $2^{56}$ blocks of memory. So double encryption adds about one bit of security against an attacker with a large memory.
- **Why triple DES has three stages.** With three stages, the middle can be met only after a search over two keys on one side. So three-key [triple DES](/triple-des/) costs about $2^{112}$ operations to attack this way. Merkle and Hellman showed that the two-key form $E_{k_1} D_{k_2} E_{k_1}$ is weaker than its 112-bit key suggests, under a chosen-plaintext attack.
- **Key size of a cascade.** In general, a cascade of two ciphers with $k$-bit keys does not give $2k$ bits of security against generic attacks. A designer who needs a longer key uses a cipher with a longer key, such as [AES](/advanced-encryption-standard/), not two stages of a short one.

## References
