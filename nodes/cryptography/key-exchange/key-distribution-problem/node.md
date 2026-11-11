---
tag: TPGTPV
kind: problem
slug: key-distribution-problem
name: Key distribution problem
area: cryptography/key-exchange
level: intro
summary: Give each pair of n users in a network a shared secret key, when the users share no secret in advance, with little storage and few trusted parties.
prereqs: [session-key]
see_also: [key-distribution-center, key-agreement-problem, key-transport-problem, key-predistribution-problem, needham-schroeder-protocol, kerberos, diffie-hellman, blom-scheme]
sources:
  - paper: doi:10.1109/TIT.1976.1055638
    title: Whitfield Diffie and Martin E. Hellman, New directions in cryptography, IEEE Transactions on Information Theory 22(6), pages 644 to 654, 1976
    locator: Section I (Introduction, the cost of key distribution in large networks) and Section III (public key distribution systems)
  - paper: doi:10.1145/359657.359659
    title: Roger M. Needham and Michael D. Schroeder, Using encryption for authentication in large networks of computers, Communications of the ACM 21(12), pages 993 to 999, 1978
    locator: the protocols with an authentication server, for conventional and for public-key encryption
  - book: isbn:9780849385230
    title: Alfred J. Menezes, Paul C. van Oorschot and Scott A. Vanstone, Handbook of Applied Cryptography, CRC Press, 1996
    locator: Chapter 12, Section 12.3.2 (Kerberos and related server-based protocols), Definition 12.32 (key distribution system) and Fact 12.34 (storage bound); Chapter 13 (key management techniques)
  - paper: doi:10.1007/3-540-39757-4_22
    title: Rolf Blom, An optimal class of symmetric key generation systems, EUROCRYPT 1984, LNCS 209, pages 335 to 338
    locator: the scheme with a symmetric matrix and the storage bound
  - paper: doi:10.1145/586110.586117
    title: Laurent Eschenauer and Virgil D. Gligor, A key-management scheme for distributed sensor networks, ACM CCS 2002, pages 41 to 47
    locator: random key predistribution with key rings drawn from a common pool
  - book: isbn:9783662581452
    title: Colin Boyd, Anish Mathuria and Douglas Stebila, Protocols for Authentication and Key Establishment, second edition, Springer, 2020
    locator: Chapter 1 (the architecture of key establishment, with and without a trusted server) and the chapter on server-based protocols
---

The key distribution problem asks how $n$ users in a network can each get a secret key shared with every other user they talk to, when they share no secrets at the start. Giving every pair its own key in advance needs $\binom{n}{2}$ keys, which does not scale. The three classic answers are a trusted [key distribution center](/key-distribution-center/) that hands out [session keys](/session-key/), public-key methods such as [Diffie-Hellman](/diffie-hellman/) with certified public keys, and [key predistribution](/key-predistribution-problem/), where a trusted party loads each device with a small amount of secret data before deployment.

**Notation.** $n$ is the number of users, $U_1, \dots, U_n$. $K_{ij}$ is the key that $U_i$ and $U_j$ share. $S$ is a trusted server (a key distribution center, KDC), and $K_{iS}$ the long-term key that $U_i$ shares with $S$. $s$ is the number of keys that each user stores, and $k$ the largest coalition of dishonest users that a scheme must resist.

## In plain words

A company has a thousand computers, and any two of them may need to talk in secret. If every pair has its own key, there are about half a million keys, and each computer stores 999 of them. When a new computer joins, every other computer must get a new key.

There are three main ways out. A trusted key server can share one key with each computer and make a fresh key for each conversation when it is needed. Each computer can publish a public key, so that any two computers can make a key without help; then the problem is to make sure that a public key really belongs to its owner. Or a trusted party can load each device with a few secrets before use, so that any two devices can compute a key from them later.

## Definition

**Setting.** There are $n$ users. A set-up phase may give each user secret data over a private channel, and may publish authentic public data. After set-up, users talk only over an open network that an adversary reads and, in the active model, changes.

**Goal.** For any pair $\{U_i, U_j\}$ that wants to talk, both parties end with the same key $K_{ij}$, and an adversary that does not control $U_i$, $U_j$ or a trusted party cannot tell $K_{ij}$ from a uniform random key.

**Costs.** The measures are the storage $s$ per user, the number of messages and of online parties for each new key, the trust placed in a central party, the cost to add or remove a user, and the coalition size $k$ that the scheme can resist.

HAC (Definition 12.32) defines a key distribution system as a method in which a trusted server, at an initialization stage, gives secret pieces to users so that any pair can later compute a shared key unknown to all others except the server.

## Variants

- **Online center (KDC).** Each user shares one long-term key $K_{iS}$ with a server $S$. To talk with $U_j$, $U_i$ asks $S$, which picks a fresh $K_{ij}$ and sends it to both, encrypted under $K_{iS}$ and $K_{jS}$. This is server-based [key transport](/key-transport-problem/): [Needham-Schroeder](/needham-schroeder-protocol/), [Otway-Rees](/otway-rees-protocol/), [Kerberos](/kerberos/).
- **Key translation center.** $U_i$ picks the key and the server only re-encrypts it from $K_{iS}$ to $K_{jS}$ ([wide-mouthed frog](/wide-mouthed-frog-protocol/)).
- **Public keys with certificates.** Each user publishes a public key, signed by a certification authority. Any pair then runs [key agreement](/key-agreement-problem/) or key transport with no online center. The authority must be trusted, but it need not be online.
- **Key predistribution.** A trusted party loads each device once, and any pair later computes $K_{ij}$ with no messages ([key predistribution problem](/key-predistribution-problem/), [Blom's scheme](/blom-scheme/)).
- **Group keys.** A key for a whole group, as in [group key agreement](/group-key-agreement-problem/) or [broadcast encryption](/broadcast-encryption/).

## Examples

**Counting keys.** With $n = 1000$ users and one key per pair, the system holds $\binom{1000}{2} = 499{,}500$ keys, and each user stores 999. With a KDC, the system holds 1000 long-term keys, and each user stores one. With public keys, each user stores one private key and the system publishes 1000 public keys, plus the authority's verification key.

**Kerberos.** A user logs in and gets a ticket-granting ticket from the authentication server. For each service, the ticket-granting server makes a fresh session key and sends it to the user, with a ticket for the service that holds another copy of the key, encrypted under the service's long-term key.

**Non-example: a single network-wide key.** If all 1000 users share one key, storage is minimal, but any one user can read every conversation, and one stolen device exposes the whole network.

## Known algorithms

- **KDC protocols**: [Needham-Schroeder](/needham-schroeder-protocol/) (1978), [Otway-Rees](/otway-rees-protocol/), [Yahalom](/yahalom-protocol/), [Denning-Sacco](/denning-sacco-protocol/), [Kerberos](/kerberos/).
- **Public-key key establishment**: [Diffie-Hellman](/diffie-hellman/), [ECDH](/ecdh/), [X25519](/x25519/), [RSA-OAEP](/rsa-oaep/) key transport, each with authentic public keys.
- **Key predistribution**: [Blom's scheme](/blom-scheme/), the polynomial scheme of Blundo et al., and the random key predistribution of Eschenauer and Gligor for sensor networks.
- **Unauthenticated public channels only**: [Merkle's puzzles](/merkle-puzzles/), the first proposal for public key distribution.

## Bounds

**Pairwise keys.** Unconditional security against any coalition, with no online server, is possible by giving each pair its own key: $s = n - 1$ per user. Fact 12.34 of HAC (from Blom 1984) says that a scheme that resists every coalition of $k$ users needs each user to store at least $k + 1$ keys of the size of $K_{ij}$. With $k = n - 2$ (all other users collude), the bound is $n - 1$, so the pairwise scheme is optimal.

**Center.** With a KDC, $s = 1$, but the center must be online for every new pair, and it learns every key. With public keys, $s = 1$ secret key, no center learns the session keys, and the cost moves to public-key operations and to certificate checks.

**Authentication needs prior trust.** An adversary who controls the network can play every role of a party with no prior authentic data. So every solution against active adversaries starts from something trusted: a key shared with a center, an authority's public key, or keys loaded at set-up.

## Reductions

- **To key transport.** An online center reduces the problem for each pair to two instances of symmetric [key transport](/key-transport-problem/), one to each party.
- **To key agreement plus authentic public keys.** With a certificate for each user, the problem for each pair becomes authenticated [key agreement](/key-agreement-problem/).
- **Predistribution and secret sharing.** Blom's scheme and the polynomial scheme are built from a symmetric bivariate polynomial, the same tool as [Shamir secret sharing](/shamir-secret-sharing/): $k + 1$ shares fix it, and $k$ shares give no information.

## Applications

- Enterprise networks with Kerberos, as in Windows Active Directory.
- The web: TLS servers hold certified public keys, and each connection runs key agreement.
- Mobile networks: each SIM card shares a long-term key with its home network, which acts as a center for session keys.
- Wireless sensor networks, where devices are too small for public-key operations and use predistributed keys.

## References
