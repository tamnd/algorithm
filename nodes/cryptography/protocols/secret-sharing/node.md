---
tag: P8BB3K
kind: problem
slug: secret-sharing
name: Secret sharing
aliases:
- threshold secret sharing
- secret splitting
area: cryptography/protocols
level: intro
summary: Split a secret into shares so that only qualifying subsets of shareholders can recover it.
prereqs: [perfect-secrecy, one-time-pad]
see_also: [shamir-secret-sharing, verifiable-secret-sharing, threshold-cryptography, secure-multiparty-computation, bgw-protocol, linear-code, gaussian-elimination, attribute-based-encryption]
sources:
  - paper: doi:10.1145/359168.359176
    title: Adi Shamir, How to share a secret, Communications of the ACM 22(11), 1979, 612-613
    locator: the definition of a (k, n) threshold scheme and the polynomial construction
  - paper: "G. R. Blakley, Safeguarding cryptographic keys, Proceedings of the AFIPS National Computer Conference, vol. 48, 1979, 313-317"
    title: G. R. Blakley, Safeguarding cryptographic keys
    locator: the threshold scheme with hyperplanes that meet in one point
  - paper: "Ehud D. Karnin, Jonathan W. Greene and Martin E. Hellman, On secret sharing systems, IEEE Transactions on Information Theory 29(1), 1983, 35-41"
    title: Ehud D. Karnin, Jonathan W. Greene and Martin E. Hellman, On secret sharing systems
    locator: the information-theoretic definition of perfect schemes and the bound that each share is at least as large as the secret
  - paper: "Mitsuru Ito, Akira Saito and Takao Nishizeki, Secret sharing scheme realizing general access structure, Proceedings of IEEE Globecom 1987, 99-102"
    title: Mitsuru Ito, Akira Saito and Takao Nishizeki, Secret sharing scheme realizing general access structure
    locator: the first perfect scheme for every monotone access structure
  - paper: "Josh Benaloh and Jerry Leichter, Generalized secret sharing and monotone functions, CRYPTO 1988, LNCS 403, 27-35"
    title: Josh Benaloh and Jerry Leichter, Generalized secret sharing and monotone functions
    locator: the scheme for a monotone formula of AND and OR gates, and the access structures that need large shares
  - paper: "Amos Beimel, Secret-sharing schemes, a survey, IWCC 2011, LNCS 6639, 11-46"
    title: Amos Beimel, Secret-sharing schemes, a survey
    locator: definitions, linear schemes and monotone span programs, and the upper and lower bounds on share size
---

Secret sharing is the problem of splitting a secret among $n$ parties so that some sets of parties, the *authorized* ones, can put their shares together and recover the secret, while every other set learns nothing about it. The most common case is the *threshold* case: any $t$ of the $n$ parties can recover the secret, and $t - 1$ cannot. Shamir and Blakley found threshold schemes in 1979, independently of each other. Secret sharing protects keys against loss and theft at the same time, and it is the basic tool of [threshold cryptography](/threshold-cryptography/) and of [secure multiparty computation](/secure-multiparty-computation/).

**Notation.** $\mathcal{P} = \{1, \ldots, n\}$ is the set of parties. $s$ is the secret, from a finite set $S$, often a field $\mathbb{F}_p$. $s_i$ is the share of party $i$, and $s_A = (s_i)_{i \in A}$ is the vector of shares of a set $A$. $\Gamma \subseteq 2^{\mathcal{P}}$ is the access structure, the family of authorized sets. $H$ is Shannon entropy.

## In plain words

A bank vault has a lock that opens with any three of the five managers' keys, but not with two. Secret sharing does the same for a number, such as a cryptographic key, without a lock: each manager gets a share, a number that by itself looks random. Any three shares give the key by a fixed computation. Any two shares are consistent with every possible key, with the same probability for each, so they give no information, not even a hint.

The simplest scheme is for the case where all $n$ parties must work together. Give the first $n - 1$ parties random numbers and give the last party the secret minus their sum. The sum of all shares is the secret, and any $n - 1$ shares are just random numbers. This is the [one-time pad](/one-time-pad/) used $n - 1$ times.

## Definition

**Access structure.** A family $\Gamma$ of subsets of $\mathcal{P}$ is monotone if $A \in \Gamma$ and $A \subseteq B$ imply $B \in \Gamma$. The threshold structure with threshold $t$ is $\Gamma_t = \{A : |A| \ge t\}$.

**Secret sharing scheme.** A randomized dealer algorithm $\mathrm{Share}(s; r) = (s_1, \ldots, s_n)$ such that:

1. **Correctness.** For each $A \in \Gamma$ there is a function $\mathrm{Rec}_A$ with $\mathrm{Rec}_A(s_A) = s$ for all $s$ and $r$.
2. **Perfect secrecy.** For each $B \notin \Gamma$ and any two secrets $s, s'$, the vectors $s_B$ for $s$ and for $s'$ have the same distribution over the dealer's randomness $r$. Equivalently, for each distribution of the secret, $s_B$ is independent of $s$ ([perfect secrecy](/perfect-secrecy/) in Shannon's sense).

The *information rate* is $\log |S| / \max_i \log |S_i|$, where $S_i$ is the set of possible values of share $i$. A scheme with rate 1 is *ideal*.

The model assumes an honest dealer and honest parties at reconstruction. If the dealer may cheat or parties may give wrong shares, one needs [verifiable secret sharing](/verifiable-secret-sharing/).

## Variants

- **Threshold ($t$-of-$n$).** The main case. [Shamir's scheme](/shamir-secret-sharing/) and Blakley's scheme solve it with shares of the same size as the secret.
- **$n$-of-$n$.** Additive sharing $s = s_1 + \cdots + s_n$ in a group, or XOR sharing of bit strings.
- **General access structures.** Any monotone $\Gamma$, for example "the CEO with one vice president, or any three vice presidents".
- **Ramp schemes.** Sets of size at least $t$ recover the secret, sets of size at most $t - k$ learn nothing, and sets in between learn part of it. In exchange, each share is $1/k$ of the size of the secret.
- **Computational secret sharing.** Secrecy only against efficient adversaries. Krawczyk (1993) encrypts the secret with a short key, shares the key with Shamir's scheme and spreads the ciphertext with an erasure code, so a share has size about $|s|/t$ plus the key length.
- **Verifiable and proactive sharing.** [Verifiable secret sharing](/verifiable-secret-sharing/) lets parties check their shares against public commitments; proactive sharing refreshes the shares from time to time (see [Shamir's scheme](/shamir-secret-sharing/)).

## Examples

All examples use $p = 11$ and the secret $s = 7$, with the dealer's random values written in.

**Additive 3-of-3.** With random values $4$ and $9$, the shares are $4$, $9$ and $7 - 4 - 9 \equiv 5$. The sum is $18 \equiv 7$. Any two shares, for example $(4, 9)$, appear for each secret with the same probability $1/121$.

**Blakley 2-of-3.** The secret is the first coordinate of the point $x = (7, 4)$, where $4$ is random. The public normals are $a_1 = (1, 2)$, $a_2 = (1, 3)$, $a_3 = (1, 5)$, and party $i$ gets $b_i = a_i \cdot x$: the shares are $b = (4, 8, 5)$, so party $i$ holds the line $a_i \cdot x = b_i$. Parties 1 and 3 solve $x_1 + 2x_2 = 4$, $x_1 + 5x_2 = 5$: then $3x_2 = 1$, so $x_2 = 4$ and $x_1 = 7$. One party alone knows only a line, and each line meets each value of $x_1$ in exactly one point, so it learns nothing. This needs the condition that $e_1 = (1, 0)$ is not a normal of any single party. In general, with dimension $t$, the dealer must pick the normals so that any $t$ are independent and $e_1$ is not in the span of any $t - 1$. If that fails, for example with normals $(1, 1, 0)$ and $(0, 1, 0)$ in dimension 3, then $b_1 - b_2 = x_1 = s$ and two parties find the secret.

**A general access structure.** Let $\Gamma$ be generated by $\{1, 2\}$, $\{1, 3\}$ and $\{3, 4\}$, which is the monotone formula $(1 \wedge 2) \vee (3 \wedge (1 \vee 4))$. The Benaloh-Leichter scheme walks the formula: an OR gate passes its value to each child, and an AND gate splits it additively. With random values $4$ for the first AND and $9$ for the second, the leaves get $1 \gets 4$, $2 \gets 3$, $3 \gets 9$, $1 \gets 9$, $4 \gets 9$. Party 1 holds two values, $(4, 9)$. The set $\{1, 2\}$ adds $4 + 3 = 7$; the set $\{3, 4\}$ adds $9 + 9 \equiv 7$. The set $\{2, 3\}$ is not authorized: its shares $(3, 9)$ are two independent uniform values whatever the secret.

**Code.** The Python file `secret_sharing.py` implements additive sharing, Blakley's scheme over $\mathbb{F}_p$ (the dealer draws random normals and checks the two rank conditions by Gaussian elimination mod $p$), and the Benaloh-Leichter scheme for a monotone formula. Shamir's scheme has its own page and code. The tests check reconstruction for every authorized set and check perfect secrecy exactly: for $p = 5$ or $p = 7$ they enumerate all the dealer's random choices and verify that the shares of each unauthorized set have the same distribution for every secret. They also show the leak of Blakley's scheme with bad normals. There are no official test vectors for these schemes. The code is for study only, is not constant time, and must not be used to protect real data; use a reviewed implementation built on libsodium or a FIPS 140 validated module.

## Known algorithms

| scheme | access structure | share size (in units of the secret) |
|---|---|---|
| additive or XOR | $n$-of-$n$ | 1 |
| [Shamir (1979)](/shamir-secret-sharing/) | threshold | 1 |
| Blakley (1979), with the dealer's conditions | threshold | 1 (plus a public normal) |
| Ito, Saito and Nishizeki (1987) | any monotone $\Gamma$ | one $n$-of-$n$ sharing per maximal unauthorized set, so up to exponential |
| Benaloh and Leichter (1988) | monotone formula | the number of leaves labeled with the party |
| monotone span programs (Karchmer and Wigderson, 1993) | any $\Gamma$ with a span program | the number of rows labeled with the party |

Ito, Saito and Nishizeki take each maximal unauthorized set $B$, share $s$ additively among the parties outside $B$, and give the shares to them; an authorized set is not inside any $B$, so it holds every part. Benaloh and Leichter's scheme is the same idea for any formula, and the threshold structure written as a formula of size about $\binom{n}{t}$ shows why threshold-specific schemes such as Shamir's are much better. All these schemes are *linear*: the shares are linear functions of $s$ and $r$, and reconstruction is a linear map.

## Bounds

**Shares are at least as large as the secret.** In a perfect scheme, $H(s_i) \ge H(s)$ for each party $i$ that is in some minimal authorized set (Karnin, Greene and Hellman, 1983). Proof: let $A$ be minimal authorized with $i \in A$, and $B = A \setminus \{i\}$. Then $B$ is unauthorized, so $H(s \mid s_B) = H(s)$, and $A$ is authorized, so $H(s \mid s_B, s_i) = 0$. Hence $H(s_i) \ge H(s_i \mid s_B) \ge I(s; s_i \mid s_B) = H(s) - 0$. So threshold schemes with shares of the size of the secret, such as Shamir's, are optimal.

**General access structures.** Not every access structure has an ideal scheme. For some, any perfect scheme has a share of size $\Omega(n / \log n)$ times the secret (Csirmaz, 1997). The best upper bound for every structure is exponential in $n$, about $2^{0.585 n}$ since the work of Applebaum and Nir (2021). The gap between these bounds is one of the main open problems of the area.

**Fields.** Shamir's scheme over $\mathbb{F}_p$ needs $p > n$, because the parties need distinct nonzero points. For binary secrets one uses $\mathrm{GF}(2^8)$ byte by byte.

## Reductions

- **Linear schemes and span programs.** Linear secret sharing schemes for $\Gamma$ correspond to monotone span programs that compute $\Gamma$, with share size equal to the program size (Karchmer and Wigderson).
- **Codes.** A linear scheme is a [linear code](/linear-code/) whose first coordinate is the secret. Shamir's scheme is a Reed-Solomon code (McEliece and Sarwate, 1981), and so reconstruction with wrong shares is error correction.
- **One-time pad.** Additive 2-of-2 sharing is the one-time pad: the ciphertext and the key are the two shares.

## Applications

- **Key backup and key escrow.** Split a master key, for example a hardware root key or a wallet seed, among several people or devices.
- **Threshold cryptography.** Sign or decrypt with a shared key without putting it together; see [threshold cryptography](/threshold-cryptography/) and [threshold signatures](/threshold-signature/).
- **Secure multiparty computation.** The [BGW protocol](/bgw-protocol/) computes on Shamir shares: additions are local, and multiplications need one round of interaction.
- **Attribute-based encryption.** Keys are tied to access structures with linear secret sharing ([attribute-based encryption](/attribute-based-encryption/)).

## References
