---
tag: DXY1X1
kind: problem
slug: key-predistribution-problem
name: Key predistribution problem
area: cryptography/key-exchange
level: advanced
summary: A trusted party loads each user with secret data in advance, so that any pair can later compute a shared key with no messages, safe against coalitions of up to k users.
prereqs: [key-distribution-problem]
see_also: [blom-scheme, key-distribution-problem, key-agreement-problem, shamir-secret-sharing, secret-sharing, erdos-renyi-model, broadcast-encryption, bilinear-pairing]
sources:
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 12, Definition 12.5 (key pre-distribution), Section 12.4 (Definition 12.32 key distribution system, Definition 12.33 j-secure, Fact 12.34 storage bound, Mechanism 12.35 Blom)
  - paper: doi:10.1007/3-540-39757-4_22
    title: Rolf Blom, An optimal class of symmetric key generation systems, EUROCRYPT 1984, LNCS 209, pages 335 to 338
    locator: the matrix scheme and the proof that its storage is optimal
  - paper: doi:10.1007/3-540-48071-4_33
    title: Carlo Blundo, Alfredo De Santis, Amir Herzberg, Shay Kutten, Ugo Vaccaro and Moti Yung, Perfectly-secure key distribution for dynamic conferences, CRYPTO 1992, LNCS 740, pages 471 to 486
    locator: the symmetric polynomial scheme and the lower bound on the storage of each user, for pairs and for conferences of t users
  - paper: doi:10.1145/586110.586117
    title: Laurent Eschenauer and Virgil D. Gligor, A key-management scheme for distributed sensor networks, ACM CCS 2002, pages 41 to 47
    locator: key rings drawn at random from a key pool, the probability that two rings share a key, and connectivity of the random key graph
---

The key predistribution problem asks a trusted authority to give each of $n$ users some secret data before deployment, so that any two users can later compute a shared key from their own data and the other's public identity, with no messages at all. The key of a pair must stay secret from a coalition of up to $k$ other users who pool their data. The trivial answer, one key per pair, needs $n - 1$ keys per user; [Blom's scheme](/blom-scheme/) and the polynomial scheme of Blundo et al. need only $k + 1$, which is optimal. It is a special case of the [key distribution problem](/key-distribution-problem/) with no online server.

**Notation.** $n$ is the number of users $U_1, \dots, U_n$ with public identities $1, \dots, n$. $s_i$ is the secret data of $U_i$. $K_{ij} = K_{ji}$ is the pairwise key, an element of a finite field $\mathbb{F}_q$. $k$ is the largest coalition the scheme must resist. $H(\cdot)$ is Shannon entropy, measured in units of $\log_2 q$ (one field element). $t$ is a conference size.

## In plain words

Before a set of small devices is sent out, a trusted factory writes some secret numbers into each one. Later, any two devices that meet must agree on a key without any help, and often without sending anything.

The simplest way is for the factory to give each pair its own key. Then each device must store one key for every other device, which is too much for a large network.

The clever schemes store far less. The price is a limit: if enough devices are captured and their secrets put together, the attacker can compute every key. A scheme is built to resist captures up to a chosen number, and the storage grows with that number, not with the size of the network.

## Definition

**Set-up.** A trusted authority $T$ picks secret randomness and gives $s_i$ to $U_i$ over a private channel.

**Key computation.** There is a function $f$ with $K_{ij} = f(s_i, j) = f(s_j, i)$ for all $i \ne j$. No messages are sent.

**Security.** The scheme is $k$-secure if for every pair $\{i, j\}$ and every coalition $C$ of at most $k$ users with $i, j \notin C$, the key $K_{ij}$ is uniform and independent of the coalition's data:

$$H(K_{ij} \mid s_c : c \in C) = H(K_{ij}) = 1.$$

This is HAC Definition 12.33 (there called $j$-secure). The security is information-theoretic: no computing power helps a coalition of size at most $k$.

**Cost.** The main measure is the storage $\max_i H(s_i)$. Others are the time to compute a key and the cost of adding users.

## Variants

- **Conferences.** Any group of $t$ users computes a common key; the case above is $t = 2$ (Blundo et al.).
- **Probabilistic.** Eschenauer and Gligor (CCS 2002) drop the requirement that every pair gets a key. Each device gets a random ring of $m$ keys from a pool of $P$ keys, and two devices that share a ring key use it. Security against capture is then measured as the fraction of links that an attacker can read.
- **Computational.** With public-key cryptography, static [Diffie-Hellman](/diffie-hellman/) gives non-interactive pairwise keys $g^{x_i x_j}$ from certified public keys. Identity-based schemes from [bilinear pairings](/bilinear-pairing/) give each user a secret that depends only on its identity. Security then rests on a hardness assumption instead of a coalition bound.
- **Broadcast encryption** solves the one-to-many version: a center sends a key that only a chosen set of users can recover ([broadcast encryption](/broadcast-encryption/)).

## Examples

**Polynomial scheme with $q = 17$ and $k = 1$.** The authority picks a random symmetric polynomial

$$f(x, y) = 3 + 5(x + y) + 7xy \bmod 17$$

and gives user $i$ the polynomial $g_i(y) = f(i, y)$, which is two field elements:

| user | $g_i(y)$ |
|---|---|
| 1 | $8 + 12y$ |
| 2 | $13 + 2y$ |
| 3 | $1 + 9y$ |

User 1 computes $K_{12} = g_1(2) = 8 + 24 = 32 \equiv 15$, and user 2 computes $g_2(1) = 13 + 2 = 15$. They agree, because $f$ is symmetric. User 3 alone learns nothing about $K_{12}$: it knows $a_0 + 3a_1 = 1$ and $a_1 + 3a_2 = 9$ for the coefficients $f = a_0 + a_1(x+y) + a_2 xy$, and every value of $a_1$ is consistent with these, giving $K_{12} = 1 + 6(18 - 2a_1) \bmod 17$, which takes all 17 values. Users 3 and 4 together know four equations in three unknowns and recover $f$, so the scheme is 1-secure and not 2-secure.

**The trivial scheme.** Give each pair a uniform key. Each user stores $n - 1$ keys and the scheme is $(n-2)$-secure, the most possible.

## Known algorithms

- **The trivial scheme**: storage $n - 1$, secure against every coalition.
- **[Blom's scheme](/blom-scheme/)** (1984): a random symmetric $(k+1) \times (k+1)$ matrix $D$ over $\mathbb{F}_q$ and public Vandermonde columns $g_i$; $U_i$ stores $D g_i$ and computes $K_{ij} = (D g_i)^\top g_j$. Storage $k + 1$, $k$-secure.
- **Blundo et al. polynomial scheme** (1992): a random symmetric polynomial of degree $k$ in each variable, as in the example. Storage $k + 1$, $k$-secure; it is Blom's scheme written with polynomials. With a symmetric polynomial in $t$ variables it serves conferences of size $t$.
- **Eschenauer and Gligor** (2002) random key rings, and later $q$-composite schemes that need several shared ring keys.

## Bounds

**Storage lower bound.** If a scheme is $k$-secure and $n \ge k + 2$, then every user stores at least $k + 1$ field elements: $H(s_i) \ge k + 1$ (HAC, Fact 12.34; Blom 1984; Blundo et al. 1992).

*Proof.* Fix user $U$ and $k + 1$ other users $W_0, \dots, W_k$. Write $K_r = K_{U W_r}$. For each $r \le k$, the coalition $\{W_0, \dots, W_{r-1}\}$ has $r \le k$ members and does not contain $U$ or $W_r$, so by $k$-security $K_r$ is independent of their data. Their data determine $K_0, \dots, K_{r-1}$. Hence

$$H(K_r \mid K_0, \dots, K_{r-1}) \ge H(K_r \mid s_{W_0}, \dots, s_{W_{r-1}}) = H(K_r) = 1.$$

By the chain rule, $H(K_0, \dots, K_k) \ge k + 1$. Each $K_r = f(s_U, W_r)$ is a function of $s_U$, so $H(s_U) \ge H(K_0, \dots, K_k) \ge k + 1$. $\blacksquare$

Blom's scheme and the polynomial scheme meet this bound, so they are optimal. With $k = n - 2$ the bound is $n - 1$, met by the trivial scheme. For conferences of $t$ users, Blundo et al. prove the bound $\binom{k + t - 1}{t - 1}$, met by the symmetric polynomial in $t$ variables.

**Coalitions beyond $k$.** In Blom's scheme and in the polynomial scheme, $k + 1$ users together recover the whole secret and so every key. The security has a sharp threshold, as in [secret sharing](/secret-sharing/).

**Random rings.** In the scheme of Eschenauer and Gligor, two rings of size $m$ from a pool of $P$ keys share at least one key with probability

$$p = 1 - \frac{\binom{P - m}{m}}{\binom{P}{m}}.$$

The graph whose edges are pairs with a common key is close to an [Erdős-Rényi random graph](/erdos-renyi-model/) with edge probability $p$, so it is connected with high probability once $p$ is a little above $\ln n / n$. For example, with $P = 10{,}000$ and $m = 75$ the formula gives $p \approx 0.43$, and with $m = 100$ it gives $p \approx 0.64$. Since $p \approx 1 - e^{-m^2/P}$, the ring size grows only like $\sqrt{P}$.

## Reductions

- **To secret sharing.** For a fixed user $j$, the values $K_{1j}, \dots, K_{nj}$ are evaluations $g_j(1), \dots, g_j(n)$ of a polynomial of degree $k$, so they form a $(k+1)$-out-of-$n$ [Shamir secret sharing](/shamir-secret-sharing/) of $g_j$. The security proof of the polynomial scheme is the security proof of Shamir's scheme.
- **To MDS codes.** HAC presents Blom's scheme with the generator matrix of a maximum distance separable [linear code](/linear-code/); any $k + 1$ columns are independent, and a [Reed-Solomon code](/reed-solomon-code/) is the usual choice.
- **From public-key key agreement.** Static Diffie-Hellman with a certificate for each user solves a computational version of the problem with storage one key and no coalition limit.

## Applications

- Wireless sensor networks and the Internet of Things, where devices are too weak for public-key cryptography (Eschenauer and Gligor; later work on Blom-based sensor schemes).
- Pay-TV and broadcast settings, where receivers hold predistributed keys.
- Military and tactical radio networks with keys loaded before a mission.

## References
