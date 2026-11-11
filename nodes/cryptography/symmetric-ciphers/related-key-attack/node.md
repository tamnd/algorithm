---
tag: 3PCPX9
kind: technique
slug: related-key-attack
name: Related-key attack
area: cryptography/symmetric-ciphers
level: advanced
summary: An attack in which the attacker sees encryptions under several unknown keys with a known relation, such as a fixed XOR difference or a rotation. It targets weak key schedules.
prereqs: [block-cipher, key-schedule, chosen-plaintext-attack]
see_also: [slide-attack, boomerang-attack, differential-cryptanalysis, advanced-encryption-standard, feistel-network, birthday-paradox, tea, pseudorandom-permutation]
sources:
  - paper: doi:10.1007/3-540-48285-7_34
    title: Eli Biham, New types of cryptanalytic attacks using related keys, Eurocrypt 1993, LNCS 765, Springer, 1994
    locator: pp. 398-409, the related keys of LOKI and Lucifer whose subkeys are shifted by one round, the chosen key attacks and the remark that DES is not open to them
  - paper: doi:10.1007/BF00203965
    title: Eli Biham, New types of cryptanalytic attacks using related keys, Journal of Cryptology 7(4), 1994
    locator: pp. 229-246, the journal version with the abstract on attacks independent of the number of rounds
  - paper: doi:10.1007/3-540-57220-1_62
    title: Lars R. Knudsen, Cryptanalysis of LOKI 91, Auscrypt 1992, LNCS 718, Springer, 1993
    locator: pp. 196-208, the key relations of LOKI 91
  - paper: doi:10.1007/3-540-68697-5_19
    title: John Kelsey, Bruce Schneier and David Wagner, Key-schedule cryptanalysis of IDEA, G-DES, GOST, SAFER, and Triple-DES, Crypto 1996, LNCS 1109, Springer, 1996
    locator: pp. 237-251, related-key attacks on the ciphers of the title
  - paper: doi:10.1007/BFb0028479
    title: John Kelsey, Bruce Schneier and David Wagner, Related-key cryptanalysis of 3-WAY, Biham-DES, CAST, DES-X, NewDES, RC2, and TEA, ICICS 1997, LNCS 1334, Springer, 1997
    locator: pp. 233-246, related-key attacks on the ciphers of the title
  - paper: doi:10.1007/978-3-642-10366-7_1
    title: Alex Biryukov and Dmitry Khovratovich, Related-key cryptanalysis of the full AES-192 and AES-256, Asiacrypt 2009, LNCS 5912, Springer, 2009
    locator: pp. 1-18, the abstract (a related-key boomerang attack on AES-256 with time and data 2^99.5 for all keys, and the first attack on the full AES-192)
  - paper: doi:10.1007/978-3-642-03356-8_14
    title: Alex Biryukov, Dmitry Khovratovich and Ivica Nikolić, Distinguisher and related-key attack on the full AES-256, Crypto 2009, LNCS 5677, Springer, 2009
    locator: pp. 231-249, the related-key attack on AES-256 for a class of weak keys
  - paper: doi:10.1007/3-540-39200-9_31
    title: Mihir Bellare and Tadayoshi Kohno, A theoretical treatment of related-key attacks, RKA-PRPs, RKA-PRFs, and applications, Eurocrypt 2003, LNCS 2656, Springer, 2003
    locator: pp. 491-506, the definition of security against a class of key relations
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Note 7.6 (the related-key model) and the notes of Section 7.8 on LOKI'89 and LOKI'91 (related-key attacks, popularized by Biham, and the earlier ideas of Knudsen)
---

A related-key attack is an attack on a [block cipher](/block-cipher/) in which the attacker gets encryptions under several unknown keys, and knows or chooses a relation between them. For example, the second key may be the first key XOR a known value, or the first key with its words rotated. The attack targets the [key schedule](/key-schedule/). Eli Biham made such attacks widely known in 1993, and Lars Knudsen had used related ideas on LOKI 91 a little earlier. Some attacks of this kind do not depend on the number of rounds at all.

**Notation.** $E_K$ is the cipher under the key $K$. $\varphi$ is a known function on keys, and the related key is $K^* = \varphi(K)$. The attacker can ask for $E_K(P)$ and $E_{K^*}(P)$ for plaintexts of its choice, but does not know $K$ or $K^*$. In the toy example, the block is $(L, R)$ with two 16-bit halves, the key is four 16-bit words $w_0, w_1, w_2, w_3$, and $F$ is a fixed bijection on 16 bits. $m$ is the number of queries under each key.

## In plain words

A cipher makes a list of round keys from the main key. If the rule that makes this list is too simple, two different main keys can give lists that are almost the same, for example one list moved by one place. The attacker cannot see the keys, but can ask for encryptions under both of them.

Then the two encryptions do almost the same work, just one round apart. If the attacker finds two messages that line up in this way, the one round that differs is easy to undo, and it shows part of the key. A few hundred messages are enough to find such a pair by chance, however many rounds the cipher has.

## When it applies

- **The attacker can get encryptions under related keys.** This is the main question of the model. It fits when keys come from simple rules, such as a counter or an XOR with constants, and when a block cipher is used in a hash function, where the attacker controls the key input.
- **The key schedule is simple or regular.** Shifted subkeys, as in LOKI or the toy cipher, or a linear key schedule, let a key difference pass through the schedule in a predictable way.
- **A differential in the key helps.** Related-key differential and boomerang attacks put a difference in the key that cancels a difference in the state, which gives better trails than [differential cryptanalysis](/differential-cryptanalysis/) with one key.

## The template

The simplest form is Biham's attack with shifted subkeys. Suppose that $E$ is a [Feistel network](/feistel-network/) whose round $i$ uses the subkey $w_{i \bmod 4}$. The related key $K^* = (w_1, w_2, w_3, w_0)$ gives the same subkeys moved by one round. Let $G$ be one round with the subkey $w_0$, $G(L, R) = (R, L \oplus F(R \oplus w_0))$. Then

$$E_{K^*}(G(P)) = G(E_K(P)) \quad \text{for every } P,$$

since both sides apply the same sequence of rounds. A pair $(P, P^*)$ with $P^* = G(P)$ is a slid pair. Write $P = (L, r_0)$ and $P^* = (r_0, X)$. Then $X = L \oplus F(r_0 \oplus w_0)$. The ciphertexts $C = (a, b)$ and $C^* = (a^*, b^*)$ of a slid pair satisfy $a^* = b$ and $b^* = a \oplus F(b \oplus w_0)$.

```pseudo id=main
RELATED-KEY-SLIDE(E_K, E_K*, m)
L1  choose r₀; for m random L, store C = E_K(L ‖ r₀) by its right half
L2  for m random X do
L3      C* ← E_K*(r₀ ‖ X)
L4      for each stored (L, C) whose right half equals the left half of C* do
L5          w ← F⁻¹(X ⊕ L) ⊕ r₀
L6          w′ ← F⁻¹(C*_right ⊕ C_left) ⊕ C*_left
L7          if w = w′ then add w to the candidates
L8  return the candidates
```

**Why it works.** All $m$ plaintexts under $K$ have right half $r_0$ and all $m$ under $K^*$ have left half $r_0$, so a pair is slid when $X = L \oplus F(r_0 \oplus w_0)$, a 16-bit condition. There are $m^2$ pairs, so by the [birthday paradox](/birthday-paradox/) a slid pair is likely when $m^2$ is near $2^{16}$. Line L4 keeps the pairs with $a^* = b$, which every slid pair passes. Line L5 computes $w_0$ from the plaintexts and line L6 from the ciphertexts. For a slid pair they agree. For a random pair, they agree with probability $2^{-16}$.

**Cost.** For an $n$-bit block, the attack uses about $2^{n/4}$ queries under each key here, since half the block is fixed, and the number of rounds plays no part. In general, a related-key attack is measured by its data, its time and the number of related keys.

**About the code.** The Python code of this page attacks a toy Feistel cipher made for this page: 32 rounds on a 32-bit block, with $F$ equal to one round of the Heys toy cipher without its key, and the subkey $w_{i \bmod 4}$ in round $i$. It is for study only and is not constant time. Do not use any of it to protect real data. Use AES from a validated library such as OpenSSL instead.

## Classic examples

### The toy Feistel cipher

Take the key 1234 9ABC 5A5A 0F0F, so the related key is 9ABC 5A5A 0F0F 1234. With $L$ = 4321 and $r_0$ = 0000, the plaintext $P$ = 43210000 slides to $P^*$ = 00000F37. Their ciphertexts are $C$ = A6147FFF and $C^*$ = 7FFF759A. The left half of $C^*$ equals the right half of $C$, and lines L5 and L6 both give $w_0$ = 1234.

With $m = 512$ there are $2^{18}$ pairs, so about 4 slid pairs are expected. In 200 runs on random keys, 4 runs found no slid pair and had to start again, close to the Poisson value $e^{-4} \approx 0.018$, and no run returned a wrong word. Repeating the step with the keys rotated by 1, 2 and 3 places gives $w_1$, $w_2$ and $w_3$. The full 64-bit key costs about $4 \cdot 2 \cdot 512 = 4096$ queries, against $2^{64}$ for exhaustive search.

### LOKI and Lucifer

In LOKI89, the subkeys of the odd rounds are rotations of one half of the key, and those of the even rounds are rotations of the other half. Biham showed that the key with its halves swapped and rotated gives the same subkeys shifted by one round. His attacks on LOKI need two sets of $2^{16}$ chosen plaintexts, one under each key, or about $2^{32}$ known plaintexts under each key, and they work for any number of rounds. DES does not have this property, because its key schedule rotates by one place in some rounds and by two places in others.

### AES-192 and AES-256

The key schedule of AES-256 is fast and close to linear. In 2009, Biryukov, Khovratovich and Nikolić gave a related-key attack on the full AES-256 for a class of weak keys. Later in 2009, Biryukov and Khovratovich gave a related-key boomerang attack on the full AES-256 that works for all keys with time and data $2^{99.5}$, and the first attack on the full AES-192. Both attacks need encryptions under keys with chosen differences. They do not affect AES used with random independent keys.

### Other ciphers

Kelsey, Schneier and Wagner studied the key schedules of many ciphers. In 1996 they gave related-key attacks on IDEA, G-DES, GOST, SAFER and triple DES, and in 1997 on 3-WAY, Biham-DES, CAST, DES-X, NewDES, RC2 and [TEA](/tea/).

## Variations

- **Related-key differentials.** A difference in the key cancels a difference in the state, so some rounds have no active S-box at all.
- **Related-key boomerang and rectangle attacks** use four keys with fixed differences for the four texts of a quartet. See the [boomerang attack](/boomerang-attack/).
- **The slide attack** uses the same slid pairs with a single key, when all the rounds are equal. See the [slide attack](/slide-attack/).
- **Formal security.** Bellare and Kohno defined security against a class of key relations. A cipher can be secure against one class and not another, so a claim of related-key security must state the class.

## Pitfalls

- **The model is debated.** Many designers count a related-key attack as a certificational weakness, and not as a break in practice. A protocol that uses random, independent keys does not give the attacker related keys. A protocol that derives keys by simple rules, or a hash function built from a block cipher, can.
- **Not every relation is fair.** If the attacker may set any bit of the key to 0, it can compare $E_K(P)$ with the encryption under the changed key and read the key bit by bit, for any cipher. The class of relations must exclude such cases.
- **Key schedules in hash functions.** In a hash function built from a block cipher, the message is often the key, so the attacker controls all keys. Use ciphers that resist related-key attacks there.
- **Real ciphers.** Run such experiments only on toy ciphers or reduced rounds that you are allowed to attack.

## Exercises

1. Prove that $E_{K^*}(G(P)) = G(E_K(P))$ for the toy cipher when the number of rounds is a multiple of 4, and find where the proof fails for 30 rounds.
2. Show that a wrong pair passes line L4 and line L7 with probability about $2^{-32}$, and find the expected number of wrong candidates for $m = 512$.
3. Find the related key for a cipher whose round $i$ uses the subkey $w_{i \bmod 2}$, and the number of queries the attack needs.
4. Describe how a related-key attack on a block cipher gives a collision attack on a hash function that uses the cipher with the message as the key.
5. Show how the attacker who may set key bits to 0 recovers a 128-bit key with 129 queries.

## References
