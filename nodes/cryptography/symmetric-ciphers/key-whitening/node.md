---
tag: 89MK42
kind: technique
slug: key-whitening
name: Key whitening
aliases:
area: cryptography/symmetric-ciphers
level: advanced
summary: XOR secret keys into the block before and after a cipher or a public permutation, as in DESX (FX) and Even-Mansour. It costs two XORs and blocks plain key search up to about 2^((k+n)/2).
prereqs: [block-cipher, exhaustive-key-search, pseudorandom-permutation]
see_also: [data-encryption-standard, triple-des, ideal-cipher-model, slide-attack, advanced-encryption-standard, key-schedule, xts-mode, meet-in-the-middle-attack]
sources:
  - paper: doi:10.1007/s001450010015
    title: Joe Kilian and Phillip Rogaway, How to protect DES against exhaustive key search (an analysis of DESX), Journal of Cryptology 14(1), 2001; first version at CRYPTO 1996, LNCS 1109
    locator: the FX construction and the bound on effective key length kappa + n - 1 - lg m in the ideal cipher model
  - paper: doi:10.1007/s001459900025
    title: Shimon Even and Yishay Mansour, A construction of a cipher from a single pseudorandom permutation, Journal of Cryptology 10(3), 1997; first version at ASIACRYPT 1991, LNCS 739
    locator: the cipher K2 XOR P(x XOR K1) and the bound O(pq/2^n) on the success of an attacker
  - paper: "Joan Daemen, Limitations of the Even-Mansour construction, Advances in Cryptology, ASIACRYPT 1991, LNCS 739, Springer, 1993"
    locator: the chosen-plaintext attack with about 2^(n/2) queries and 2^(n/2) evaluations of the permutation
  - paper: "Orr Dunkelman, Nathan Keller and Adi Shamir, Minimalism in cryptography: the Even-Mansour scheme revisited, Advances in Cryptology, EUROCRYPT 2012, LNCS 7237, Springer, 2012"
    locator: the security of the one-key variant and the slide attack with known plaintexts
  - paper: "Shan Chen and John Steinberger, Tight security bounds for key-alternating ciphers, Advances in Cryptology, EUROCRYPT 2014, LNCS 8441, Springer, 2014"
    locator: the bound of about 2^(rn/(r+1)) queries for r rounds of iterated Even-Mansour
---

Key whitening is the technique of adding secret key material, with XOR, to the block before the first operation of a cipher and after the last. With a [block cipher](/block-cipher/) $E$ it gives the *FX construction* $\mathrm{FX}_{K, K_1, K_2}(x) = K_2 \oplus E_K(x \oplus K_1)$; with DES it is DESX, proposed by Ron Rivest in 1984. With a fixed public permutation $P$ in place of $E_K$, it gives the *Even-Mansour cipher* $K_2 \oplus P(x \oplus K_1)$, the simplest block cipher with a security proof. The cost is two XORs per block, and in the [ideal cipher model](/ideal-cipher-model/) the gain is large: Kilian and Rogaway proved that FX has an effective key length of at least $k + n - 1 - \lg m$ bits against an attacker with $m$ known pairs, where $k$ is the key length and $n$ the block length of $E$. The Even-Mansour bound $2pq/2^n$ is tight: Daemen's attack and the slide attack of Dunkelman, Keller and Shamir recover the keys with about $2^{n/2}$ queries and $2^{n/2}$ evaluations of $P$.

## In plain words

Suppose a lock has a key that is too short, so a thief could try every key. Key whitening adds two more secrets without changing the lock: the message is scrambled with a secret mask before it goes in, and the output is scrambled with another secret mask after it comes out. Each mask is a plain XOR, so it is almost free.

Now a thief who guesses the inner key cannot check the guess, because the masks hide both the real input and the real output. To check a guess of the inner key, the thief must also guess a mask.

There is a limit. The thief can play the encryption against the inner cipher and look for a match, as in a birthday search. So the masks help up to about the square root of the total number of keys, not to the full number.

## When it applies

- The core $E$ is believed strong in structure but has a short key, as DES had. FX is a cheap fix that keeps the hardware.
- The core is a fixed public permutation, as in sponge designs and in key-alternating ciphers such as AES, whose first and last AddRoundKey are whitening steps.
- The attacker is generic, that is, treats $E$ or $P$ as a black box. Whitening gives no protection against attacks that use the structure of $E$, such as differential and linear cryptanalysis, beyond what $E$ has already.
- It does not help against attacks with about $2^{n/2}$ data on an $n$-bit block, such as birthday collisions in a mode, since the block size does not change.

## The template

```pseudo id=main
FX-ENCRYPT(E, K, K1, K2, x)
L1  u ← x ⊕ K1                    ▷ pre-whitening
L2  v ← E_K(u)                    ▷ the core cipher, or P(u) for Even-Mansour
L3  return v ⊕ K2                 ▷ post-whitening
```

Decryption is $x = K_1 \oplus E_K^{-1}(y \oplus K_2)$. The total key is $(K, K_1, K_2)$ of $k + 2n$ bits. The Even-Mansour cipher is the case $k = 0$, with $E_K = P$. The one-key Even-Mansour cipher sets $K_1 = K_2$, and DESX uses one 56-bit DES key and two 64-bit whitening keys, 184 bits in all.

## Classic examples

**DESX.** $\mathrm{DESX}_{K, K_1, K_2}(x) = K_2 \oplus \mathrm{DES}_K(x \oplus K_1)$. Rivest proposed it in 1984, and it was used in the BSAFE library of RSA Data Security. It costs one DES call, against three for [Triple DES](/triple-des/). Kilian and Rogaway (1996, journal version 2001) modeled DES as an ideal cipher and proved that an attacker who makes $t$ queries to DES or its inverse and sees $m$ pairs of DESX succeeds with probability at most about $mt/2^{k + n - 1}$. So the effective key length is at least $k + n - 1 - \lg m = 119 - \lg m$ bits for DES. For example, with $m = 2^{30}$ known pairs, the attacker still needs about $2^{89}$ DES calls.

**The Even-Mansour cipher and its bound.** Let $P$ be a uniformly random permutation of $\{0,1\}^n$, public in the sense that the attacker can query $P$ and $P^{-1}$, and let $K_1, K_2$ be uniform and secret. The attacker makes $q$ queries to $E$ or $E^{-1}$, where $E(x) = K_2 \oplus P(x \oplus K_1)$, and $p$ queries to $P$ or $P^{-1}$.

**Theorem (Even and Mansour 1991, here with an explicit constant).** The advantage of any such attacker in telling $(E, P)$ apart from $(\Pi, P)$, where $\Pi$ is a random permutation independent of $P$, is at most $2pq/2^n$.

*Proof in outline.* Use lazy sampling: both $P$ and the cipher are built one point at a time as the attacker asks.

1. *The ideal game.* $\Pi$ and $P$ are independent random permutations. The keys $K_1, K_2$ play no part in the answers, so they can be chosen after the attacker stops. Call the run *bad* if some $E$ query $(x, y)$ and some $P$ query $(u, v)$ satisfy $x \oplus K_1 = u$ or $y \oplus K_2 = v$. For one fixed pair of queries, each equation holds with probability $2^{-n}$ over the late choice of keys. A union bound over the $pq$ pairs and the two equations gives $\Pr[\text{bad}] \le 2pq/2^n$.
2. *The real game, written with the same bookkeeping.* An $E$ query $x$ asks $P$ at the point $x \oplus K_1$. If neither this point nor its output meets a point of a $P$ query, the answer is a fresh random value of $P$, and so has the same distribution as an answer of $\Pi$. The same holds for $E^{-1}$ and for $P$ queries that do not meet an $E$ query. So the two games give the same answers until the bad event happens.
3. *The fundamental lemma of game playing.* If two games are the same until bad, the advantage is at most the probability of bad in one of them, here at most $2pq/2^n$.

A full proof must also check that fresh values in the real game avoid the outputs already used inside $P$, which costs no more than the same bad event. The original paper gives the bound as $O(pq/2^n)$. $\square$

So the attacker needs $pq \approx 2^n$, and the best balance is $p = q = 2^{n/2}$. The attacks below meet this bound, so it is tight.

**Daemen's attack (1991) on the two-key cipher.** Fix a nonzero $\Delta$. If $u = x \oplus K_1$, then

$$E(x) \oplus E(x \oplus \Delta) = P(u) \oplus P(u \oplus \Delta),$$

because $K_2$ cancels. Choose a set $X$ of $2^{n/2}$ plaintexts closed under $\oplus \Delta$ and a set $U$ of $2^{n/2}$ points such that every $n$-bit value is $x \oplus u$ for exactly one pair in $X \times U$. Query $E$ on $X$ and store $E(x) \oplus E(x \oplus \Delta)$. For each $u \in U$, compute $P(u) \oplus P(u \oplus \Delta)$ and look it up. The true pair $(x, u)$ with $x \oplus u = K_1$ always matches, and gives $K_1 = x \oplus u$ and $K_2 = E(x) \oplus P(u)$. Each candidate is checked on two more queries.

On the toy cipher of the tests, with $n = 16$, a random permutation $P$ from seed 1991, $X$ = the blocks with a high byte of zero, $U$ = the blocks with a low byte of zero and $\Delta = 1$, the keys $K_1$ = 3A5C and $K_2$ = C0DE are found after 256 chosen plaintexts and 118 calls of $P$. Over all of $U$, only 6 candidates match, against $2^{16}$ keys for $K_1$ alone.

**The slide attack on the one-key cipher (Dunkelman, Keller and Shamir 2012).** With $K_1 = K_2 = K$ and $u = x \oplus K$, the output is $E(x) = K \oplus P(u)$, so

$$x \oplus E(x) = u \oplus P(u).$$

The left side needs only known pairs, and the right side only $P$. Store $x \oplus E(x)$ for $2^{n/2}$ known plaintexts, compute $u \oplus P(u)$ for $2^{n/2}$ values of $u$, and match; a match gives the candidate $K = x \oplus u$. With random known plaintexts, a true match appears with constant probability by the [birthday](/birthday-paradox/) argument. The tests use the structured sets $X$ and $U$ above, which give a true match for sure. The key 7E57 is found after 256 known plaintexts and 127 calls of $P$, with 6 candidates in all.

The code that runs these attacks is for study only, is not constant time, and works only on a 16-bit toy. For real data, use AES from a FIPS 140 validated module or libsodium.

## Variations

- **Iterated Even-Mansour (key-alternating ciphers).** $k_r \oplus P_r(\cdots k_1 \oplus P_1(k_0 \oplus x))$. Chen and Steinberger (2014) proved security up to about $2^{rn/(r+1)}$ queries for $r$ rounds with independent keys, and this is tight. AES has this form with fixed rounds and a key schedule.
- **One-key Even-Mansour.** $K_1 = K_2$ saves $n$ key bits and keeps the same bound up to a constant, by Dunkelman, Keller and Shamir.
- **Whitening inside designs.** Twofish XORs whitening keys before the first round and after the last. PRINCE uses the FX form with $K_2$ derived from $K_1$ by a simple linear map.
- **Tweakable masks.** The XEX construction behind [XTS](/xts-mode/) and OCB uses masks that depend on a tweak or position, $E_K(x \oplus \Delta) \oplus \Delta$, with $\Delta$ derived from a secret.

## Pitfalls

- **Whitening is not extra rounds.** Differential and linear attacks on $E$ work through whitening with little extra cost, since an XOR does not change differences. DESX is about as weak as DES against these attacks.
- **The limit is the birthday bound.** Two whitening keys of $n$ bits do not give $k + 2n$ bits of security. The Daemen and slide attacks show about $(k + n)/2$ bits in the balanced case. For DESX, the generic bound $119 - \lg m$ assumes a limited number of pairs.
- **Related keys.** If $K_1$ and $K_2$ can be changed by known differences, the attacker can shift inputs and outputs freely. Use independent keys.
- **The same mask in both places.** One-key Even-Mansour is still secure up to the birthday bound, but a design with $K_2$ a simple function of $K_1$ must be checked against slide attacks, as for PRINCE.
- **A public permutation must be a good one.** The proof needs $P$ to behave like a random permutation. A permutation with structure, such as a linear map, gives no security.

## Exercises

1. Show that an attacker who knows $K$ in DESX can find $K_1$ and $K_2$ from about $2^{n/2}$ chosen plaintexts and $2^{n/2}$ DES calls. Hint: this is the Even-Mansour cipher with $P = \mathrm{DES}_K$.
2. Show that one-key Even-Mansour with $P$ an involution, $P(P(u)) = u$, is distinguished from a random permutation with two queries. Hint: compute $E(E(x))$.
3. In Daemen's attack, count the expected number of false candidates when $X$ and $U$ have size $2^{n/2}$ and $P$ is random. Compare with the 6 candidates of the toy run.
4. Prove that $E(x) = K \oplus P(x)$, with whitening only at the output, is broken by one query to $E$ and one to $P$.
5. Prove that if $P$ is linear over GF(2), then two-key Even-Mansour is distinguished from a random permutation with two queries to $E$, and that $K_1$ and $K_2$ cannot both be found from any number of queries. Hint: $E(x) = P(x) \oplus c$ for a constant $c$.

## References
