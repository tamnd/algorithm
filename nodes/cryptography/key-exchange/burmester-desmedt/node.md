---
tag: BRF2MN
kind: algorithm
slug: burmester-desmedt
name: Burmester-Desmedt protocol
aliases:
- BD protocol
- Burmester-Desmedt conference key distribution
area: cryptography/key-exchange
level: advanced
summary: Two-round group key agreement. Each member broadcasts z_i = g^x_i, then X_i = (z_{i+1}/z_{i-1})^x_i; all compute g^(x_1 x_2 + ... + x_n x_1) with 3 exps each. 1994.
solves: [group-key-agreement-problem]
model: word-ram
complexity:
  vars: {n: the number of members, m: the number of binary digits of the modulus p}
  time: {worst: O(n m^3 + n^2 m^2), average: O(n m^3 + n^2 m^2), best: O(n m^3 + n^2 m^2)}
  space: {extra: Θ(n m)}
properties: {deterministic: false, randomized: true}
history:
  year: 1994
  people: [Mike Burmester, Yvo Desmedt]
  note: Burmester and Desmedt gave the two-round conference key protocol at EUROCRYPT 1994. Katz and Yung (2003) proved it secure under DDH and made it authenticated with a compiler.
prereqs: [group-key-agreement-problem, diffie-hellman]
see_also: [ingemarsson-tang-wong, group-diffie-hellman, tree-based-group-diffie-hellman, decisional-diffie-hellman, authenticated-key-exchange, digital-signature, modular-exponentiation, safe-prime]
sources:
  - paper: "Mike Burmester and Yvo Desmedt, A secure and efficient conference key distribution system, EUROCRYPT 1994, LNCS 950"
    locator: the broadcast protocol with z_i = g^(x_i), X_i = (z_(i+1)/z_(i-1))^(x_i), and the key g^(x_1 x_2 + x_2 x_3 + ... + x_n x_1)
  - paper: "Jonathan Katz and Moti Yung, Scalable protocols for authenticated group key exchange, CRYPTO 2003, LNCS 2729"
    locator: the proof that the unauthenticated BD protocol is secure against a passive adversary under the decisional Diffie-Hellman assumption, and the compiler that adds a round of nonces and signatures on every message
  - paper: doi:10.1145/238168.238182
    title: Michael Steiner, Gene Tsudik and Michael Waidner, Diffie-Hellman key distribution extended to group communication, ACM CCS 1996
    locator: the comparison of BD with the GDH protocols in rounds, messages and exponentiations
  - url: "https://www.rfc-editor.org/rfc/rfc5054"
    title: David Taylor, Thomas Wu, Nikos Mavrogiannopoulos and Trevor Perrin, RFC 5054, Using the Secure Remote Password (SRP) Protocol for TLS Authentication, November 2007
    locator: Appendix A, the 1024-bit group, used by the code as a safe prime
---

The Burmester-Desmedt (BD) protocol solves the [group key agreement problem](/group-key-agreement-problem/) in two rounds of broadcast, whatever the number of members. The members sit on a logical ring. In round 1, each member broadcasts a [Diffie-Hellman](/diffie-hellman/) share $z_i = g^{x_i}$; in round 2, each broadcasts the quotient of its neighbors' shares raised to its secret. Each member then computes $K = g^{x_1 x_2 + x_2 x_3 + \cdots + x_n x_1}$, the product of the Diffie-Hellman keys of all neighbor pairs on the ring, with 3 exps and about $2n$ multiplications. Burmester and Desmedt published it in 1994; in its basic form it resists only a passive attacker.

**Notation.** $p = 2q + 1$ is a [safe prime](/safe-prime/), and $g$ generates the subgroup $G$ of quadratic residues modulo $p$, of prime order $q$. Members $M_1, \ldots, M_n$, $n \ge 2$, sit on a ring, so indices are taken modulo $n$. $x_i \in [1, q)$ is the secret of $M_i$. We write $k_i = g^{x_i x_{i+1}}$ for the Diffie-Hellman key of the neighbors $M_i$ and $M_{i+1}$. An exp is one modular exponentiation.

## In plain words

The members sit in a circle. Each pair of neighbors could make a Diffie-Hellman key, and the group key is the product of all these neighbor keys. The problem is that each member can compute only the two keys next to it.

So in a second step, each member publishes one extra value: the ratio between its key with the right neighbor and its key with the left neighbor. These ratios reveal nothing useful alone, but with them a member can walk around the circle. From the key on its left, it multiplies by its own ratio to get the key on its right, then by the next member's ratio to get the next key, and so on. Multiplying all the keys it meets gives the group key.

Every member does the same small work, and there are only two rounds, however large the group is.

## The problem

$n$ members must agree on a key to which each contributes, in a way that a passive eavesdropper cannot compute; see [group key agreement](/group-key-agreement-problem/). BD aims at a constant number of rounds and a constant number of exps per member, at the cost of $2n$ broadcast messages and $O(n)$ multiplications per member.

## The algorithm

```pseudo id=main
BD(M_1, ..., M_n; p, q, g)          ▷ Burmester and Desmedt, EUROCRYPT 1994
    round 1:
L1    each M_i: x_i ← random in [1, q);  broadcast z_i ← g^(x_i)
    round 2, after checking that every z_j is in G:
L2    each M_i: broadcast X_i ← (z_(i+1) / z_(i−1))^(x_i)       ▷ X_i = k_i / k_(i−1)
    key, after checking that every X_j is in G (or X_j = 1 when n = 2):
L3    y ← z_(i−1)^(x_i);  K ← y                               ▷ y = k_(i−1)
L4    for j = 1 to n − 1:
L5      y ← y · X_(i+j−1)                                      ▷ y = k_(i+j−1)
L6      K ← K · y
    output K
```

Line L2 is the key step. Since $z_{i+1}^{x_i} = g^{x_i x_{i+1}} = k_i$ and $z_{i-1}^{x_i} = k_{i-1}$, the value $X_i$ is the ratio $k_i / k_{i-1}$ of the two neighbor keys of $M_i$. Line L3 computes the neighbor key on the left, $k_{i-1}$. Each pass through line L5 moves one step to the right: $k_{i+j-2} \cdot X_{i+j-1} = k_{i+j-1}$. After $n - 1$ passes, line L6 has multiplied $k_{i-1}, k_i, \ldots, k_{i+n-2}$, which are all $n$ neighbor keys, each once. So $K = \prod_{j=1}^{n} k_j = g^{x_1 x_2 + x_2 x_3 + \cdots + x_n x_1}$.

The paper writes the same key as $K_i = z_{i-1}^{n x_i} \cdot X_i^{n-1} \cdot X_{i+1}^{n-2} \cdots X_{i+n-2}$, which costs more exps; the loop of lines L4 to L6 replaces them with $2(n - 1)$ multiplications. With $n = 2$, $z_{i+1} = z_{i-1}$, so $X_i = 1$, and the key is $g^{2 x_1 x_2}$; the check after round 2 must accept 1 in that case.

**About the code.** The Python code is for study only. It is not constant time and must not protect real data. It simulates all members, with the 1024-bit safe prime of RFC 5054, Appendix A, and $g = 4$, which is too small for new systems. It checks each broadcast value once, since all members receive the same broadcast. It is the unauthenticated protocol; there are no official test vectors.

## Example

Take $p = 23$, $q = 11$, $g = 4$, and three members with $x_1 = 2$, $x_2 = 3$ and $x_3 = 5$. The key exponent is $x_1 x_2 + x_2 x_3 + x_3 x_1 = 6 + 15 + 10 = 31 \equiv 9 \pmod{11}$, so $K = 4^9 \bmod 23 = 13$.

| Member | $z_i$ (L1) | $X_i$ (L2) |
|---|---|---|
| $M_1$ | $4^2 = 16$ | $(18 / 12)^2 = 13^2 = 8$ |
| $M_2$ | $4^3 = 18$ | $(12 / 16)^3 = 18^3 = 13$ |
| $M_3$ | $4^5 = 12$ | $(16 / 18)^5 = 6^5 = 2$ |

The inverses modulo 23 are $12^{-1} = 2$, $16^{-1} = 13$ and $18^{-1} = 9$. Note that $8 \cdot 13 \cdot 2 = 208 \equiv 1 \pmod{23}$: the product of all $X_i$ is always 1. $M_1$ computes $y = z_3^{x_1} = 12^2 = 6 = k_3$ (line L3), then $y = 6 \cdot X_1 = 2 = k_1$ and $y = 2 \cdot X_2 = 3 = k_2$ (line L5), and $K = 6 \cdot 2 \cdot 3 = 36 \equiv 13$. $M_2$ and $M_3$ also get 13; the code gives the same values on this group.

## Correctness

**Claim.** In an honest run, every member outputs $K = g^{\sum_{j=1}^{n} x_j x_{j+1}}$. For $n \ge 3$, $X_i = g^{x_i x_{i+1} - x_{i-1} x_i} = k_i / k_{i-1}$. By induction, after $j$ passes of line L5, $y = k_{i+j-1}$, so line L6 multiplies $k_{i-1}, k_i, \ldots, k_{i+n-2}$, which are $n$ consecutive neighbor keys on a ring of $n$, so each $k_j$ once. For $n = 2$ the same steps give $k_1 k_2 = g^{2 x_1 x_2}$. The full proof is on the proof page.

**Security.** An eavesdropper sees $z_1, \ldots, z_n$ and $X_1, \ldots, X_n$. Katz and Yung (2003) prove that the key is indistinguishable from random under the [decisional Diffie-Hellman](/decisional-diffie-hellman/) assumption against a passive adversary. The product of the $X_i$ is always 1, so round 2 gives only $n - 1$ independent values.

## Complexity

Each member does 3 exps (lines L1, L2 and L3) and one inversion modulo $p$ for line L2, independent of $n$; with $n$ members the total is $3n$ exps. Lines L4 to L6 cost $2(n - 1)$ multiplications modulo $p$ per member, so $O(n m^2)$ per member and $O(n^2 m^2)$ in total, beside $O(n m^3)$ for all exps. Each member checks the $2n$ broadcast values for membership in $G$, which costs more exps if done with $v^q \equiv 1$; cheaper tests exist for safe primes with the Legendre symbol. There are 2 rounds and $2n$ broadcast messages of one group element each. A member stores the $2n$ received values, $\Theta(n m)$ space.

## Properties

- **Constant rounds.** Two rounds of broadcast for any $n$.
- **Constant exps.** Three per member, the same for every member.
- **Contributory.** Changing one $x_i$ changes the key; a test checks this.
- **Needs broadcast.** Every member must receive all $2n$ values; on a network without cheap broadcast, the cost is $\Theta(n^2)$ point-to-point messages.
- **Different key from ITW and GDH.** The exponent is a sum of products of neighbors, not the product of all secrets.
- **Not robust.** A member who sends a wrong $X_i$ makes the others compute different keys, and the basic protocol does not show who did it.
- **No efficient join or leave.** Any change of membership needs a new run.

## Variants and improvements

- **Authenticated BD (Katz and Yung, 2003).** A first round sends fresh nonces; each later message carries the member list, the nonces and a [digital signature](/digital-signature/). The result has 3 rounds and is secure against an active adversary, with forward secrecy, in the standard model if DDH holds and the signature is secure.
- **Exponent form.** The paper's formula $z_{i-1}^{n x_i} X_i^{n-1} \cdots X_{i+n-2}$ gives the same key with more exps; the telescoping product of lines L4 to L6 is cheaper.
- **Consistency check.** Each member can check $\prod_j X_j = 1$; this detects one wrong $X_j$, but not changes that cancel out.
- **Elliptic curves.** The protocol works in any group where DDH is hard, for example an elliptic curve group, with point negation in place of inversion.

## When to use it

Use BD when the group is static, all members are online, broadcast is cheap, and low latency matters: it has the fewest rounds and the least work per member among the classic protocols. Use the authenticated version of Katz and Yung in any real setting. For a group that changes often, use a tree-based protocol such as [TGDH](/tree-based-group-diffie-hellman/), and for asynchronous messaging use MLS (RFC 9420).

## Pitfalls

- **Swapped neighbors.** If a member computes $X_i = (z_{i-1}/z_{i+1})^{x_i}$, it publishes $k_{i-1}/k_i$, and the other members' walks go the wrong way. Line L2 must divide the right neighbor's share by the left one's, $z_{i+1}/z_{i-1}$, and line L3 must start from the left neighbor, $z_{i-1}^{x_i}$.
- **Wrong start of the walk.** If line L3 starts from $z_{i+1}^{x_i} = k_i$ while line L5 still begins with $X_i$, the walk is one step out of phase, the values of $y$ are no longer neighbor keys, and the members get different results. Start with $y = z_{i-1}^{x_i}$ as in line L3.
- **Rejecting 1 for two members.** With $n = 2$, $X_i = 1$ in every honest run. A check that rejects 1 always makes the protocol fail; the check after round 2 must allow 1 when $n = 2$.
- **No membership check.** Without checks on $z_j$ and $X_j$, an attacker can send values of small order; check every received value before line L2 and line L3.
- **No authentication.** The basic protocol is open to a man in the middle; use the Katz-Yung compiler.
- **Using K directly.** Hash $K$ with the member list and the transcript before use.

## Implementations

The Python code has `round1` (line L1), `round2` (line L2), `key` (lines L3 to L6), `check_broadcast`, called once for each round, and `run`. The tests check agreement with $g^{x_1 x_2 + \cdots + x_n x_1}$ for $n$ in $\{2, 3, 4, 7\}$, that the product of the $X_i$ is 1, that a value outside the subgroup is rejected, and that a change of one secret changes the key.

## History

Ingemarsson, Tang and Wong (1982) gave a ring protocol with $n - 1$ rounds. Burmester and Desmedt (1994) reduced it to two rounds with the telescoping idea. Steiner, Tsudik and Waidner (1996) compared it with GDH. Katz and Yung (2003) proved the passive security of BD under DDH and made it the base of their compiler for authenticated group key exchange.

## References
