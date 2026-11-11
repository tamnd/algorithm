---
tag: EHMDDS
kind: algorithm
slug: ingemarsson-tang-wong
name: Ingemarsson-Tang-Wong conference key protocol
aliases:
- ITW protocol
- ITW conference key distribution
area: cryptography/key-exchange
level: advanced
summary: n members on a ring; in each of n - 1 rounds every member raises the value from its left neighbor to its secret and passes it right. All end with g^(x_1 ... x_n). 1982.
solves: [group-key-agreement-problem]
model: word-ram
complexity:
  vars: {n: the number of members, m: the number of binary digits of the modulus p}
  time: {worst: O(n^2 m^3), average: O(n^2 m^3), best: O(n^2 m^3)}
  space: {extra: Θ(n m)}
properties: {deterministic: false, randomized: true}
history:
  year: 1982
  people: [Ingemar Ingemarsson, Donald T. Tang, Chak-Kuen Wong]
  note: Ingemarsson, Tang and Wong extended the Diffie-Hellman idea to a conference of n users in IEEE Transactions on Information Theory in 1982, the first group key agreement protocol.
prereqs: [group-key-agreement-problem, diffie-hellman]
see_also: [group-diffie-hellman, burmester-desmedt, tree-based-group-diffie-hellman, decisional-diffie-hellman, modular-exponentiation, man-in-the-middle-attack, safe-prime, quadratic-residue]
sources:
  - paper: "Ingemar Ingemarsson, Donald T. Tang and Chak-Kuen Wong, A conference key distribution system, IEEE Transactions on Information Theory 28(5), 1982"
    locator: the conference key system for n users on a ring, with the key g^(x_1 x_2 ... x_n) after n - 1 rounds
  - paper: doi:10.1145/238168.238182
    title: Michael Steiner, Gene Tsudik and Michael Waidner, Diffie-Hellman key distribution extended to group communication, ACM CCS 1996
    locator: the comparison of the ring protocol with GDH.1 to GDH.3 in rounds, messages and exponentiations, and the group decisional Diffie-Hellman problem
  - paper: "Mike Burmester and Yvo Desmedt, A secure and efficient conference key distribution system, EUROCRYPT 1994, LNCS 950"
    locator: the discussion of earlier conference key systems and a two-round protocol on the same ring of users
  - url: "https://www.rfc-editor.org/rfc/rfc5054"
    title: David Taylor, Thomas Wu, Nikos Mavrogiannopoulos and Trevor Perrin, RFC 5054, Using the Secure Remote Password (SRP) Protocol for TLS Authentication, November 2007
    locator: Appendix A, the 1024-bit group, used by the code as a safe prime
---

The Ingemarsson-Tang-Wong (ITW) protocol is the first protocol for the [group key agreement problem](/group-key-agreement-problem/), published in 1982. The $n$ members sit on a ring. Each member raises $g$ to a secret exponent and sends the result to its right neighbor; then, in each of $n - 1$ rounds, every member raises the value from its left neighbor to its own secret and passes the result on. After the last round, every member holds $K = g^{x_1 x_2 \cdots x_n}$. For $n = 2$ it is [Diffie-Hellman](/diffie-hellman/). The work is the same for all members, but the protocol needs $n - 1$ sequential rounds and $n(n - 1)$ messages.

**Notation.** $p = 2q + 1$ is a [safe prime](/safe-prime/), and $g$ generates the subgroup $G$ of [quadratic residues](/quadratic-residue/) modulo $p$, of prime order $q$. Members are $M_1, \ldots, M_n$ with $n \ge 2$ on a ring, so indices are taken modulo $n$ and $M_{i-1}$ is the left neighbor of $M_i$. $x_i \in [1, q)$ is the secret of $M_i$, and $h_i$ is the value that $M_i$ holds. For integers $a \le b$, $\pi(a, b) = x_a x_{a+1} \cdots x_b \bmod q$, the product of a run of consecutive secrets around the ring. An exp is one modular exponentiation.

## In plain words

Picture the members sitting in a circle. Each one has a secret number. At the start, each member locks a public number with its secret and passes the result to the person on its right.

Then, again and again, each member takes what it got from the left, adds its own lock, and passes it to the right. After each pass, a value carries one more lock. When everyone has passed $n - 1$ times, each value carries the locks of all $n$ members, so every member holds the same number, the key.

An eavesdropper sees values with fewer than $n$ locks. To get the key from them, it would have to remove or add a lock without the secret, which is a hard Diffie-Hellman problem.

## The problem

$n$ members with no shared secret must agree on one key that depends on a random secret of each member, while a passive eavesdropper cannot compute it. See [group key agreement](/group-key-agreement-problem/). ITW uses only messages between ring neighbors and gives every member the same work.

## The algorithm

```pseudo id=main
ITW(M_1, ..., M_n; p, q, g)         ▷ Ingemarsson, Tang and Wong, 1982
L1  each M_i: x_i ← random in [1, q)
L2  each M_i: h_i ← g^(x_i)
L3  repeat n − 1 times:                  ▷ one round; all members act at the same time
L4    each M_i: receive h_(i−1) from M_(i−1); abort unless it is in G
L5    each M_i: h_i ← h_(i−1)^(x_i)         ▷ uses the old h_(i−1); then send h_i to M_(i+1)
    output K_i = h_i
```

Line L2 gives each member $g^{x_i}$. In each round, line L4 delivers the value that the left neighbor held at the end of the previous round, and line L5 multiplies one more secret into the exponent. After $r$ rounds, $M_i$ holds $g^{\pi(i - r, i)}$: the product of the $r + 1$ secrets that end at its own position. After $n - 1$ rounds, the run has length $n$, which is the whole ring, so $h_i = g^{x_1 \cdots x_n}$ for every $i$.

The value that $M_i$ sends in the last round is not needed; the code does not send it. Each member checks that the value it receives is in $G$, which stops a value of small order from forcing the key into a small set.

**About the code.** The Python code is for study only. It is not constant time and must not protect real data. It simulates all members in one loop, with the 1024-bit safe prime of RFC 5054, Appendix A, and $g = 4$, which is too small for new systems. The 1982 paper describes a more general system; the code implements the Diffie-Hellman ring form that later papers call ITW. There are no official test vectors.

## Example

Take $p = 23$, $q = 11$ and $g = 4$, which has order 11 modulo 23, and three members with $x_1 = 2$, $x_2 = 3$ and $x_3 = 5$. The key is $4^{30 \bmod 11} = 4^8 \bmod 23 = 9$.

| After | $h_1$ | $h_2$ | $h_3$ |
|---|---|---|---|
| L2 | $4^2 = 16$ | $4^3 = 18$ | $4^5 = 12$ |
| round 1 | $12^2 = 6$ | $16^3 = 2$ | $18^5 = 3$ |
| round 2 | $3^2 = 9$ | $6^3 = 9$ | $2^5 = 9$ |

In round 1, $M_1$ raises the value of its left neighbor $M_3$; so $h_1 = g^{x_3 x_1}$. In round 2, it raises $h_3 = g^{x_2 x_3}$ and gets $g^{x_1 x_2 x_3}$. The eavesdropper sees $16, 18, 12$ and $6, 2, 3$, that is, $g^{x_i}$ and $g^{x_{i-1} x_i}$ for each $i$, but not 9. A test of the code checks the same fact for $n = 3$ in the 1024-bit group.

## Correctness

**Claim.** In an honest run, every member outputs $K = g^{x_1 \cdots x_n}$. By induction on $r$, after $r$ rounds $h_i = g^{\pi(i - r, i)}$: true for $r = 0$ by line L2, and line L5 gives $\bigl(g^{\pi(i - 1 - r, i - 1)}\bigr)^{x_i} = g^{\pi(i - (r + 1), i)}$. For $r = n - 1$, $\pi(i - n + 1, i)$ is the product of $n$ consecutive secrets on a ring of $n$, so it contains each $x_j$ once. The full proof is on the proof page.

**Security.** An eavesdropper sees $g^{\pi(i - r, i)}$ for all $i$ and all $r \le n - 2$, that is, $g$ raised to the products of all runs of fewer than $n$ consecutive secrets. Telling $K$ from random given these is an instance of the group decisional Diffie-Hellman problem, which Steiner, Tsudik and Waidner (1996) reduce to the two-party [decisional Diffie-Hellman](/decisional-diffie-hellman/) problem. The protocol has no authentication: a man in the middle on any link can replace values.

## Complexity

Each member does one exp in line L2 and one in each of $n - 1$ rounds: $n$ exps, $n^2$ in total. There are $n - 1$ rounds of $n$ messages each, so $n(n - 1)$ messages, each one group element. With schoolbook arithmetic an exp costs $O(m^3)$, so the total work is $O(n^2 m^3)$ and each member does $O(n m^3)$. Each member stores its secret and one value; the simulation of all $n$ members stores $\Theta(n)$ elements. The tests check $n - 1$ rounds, $n(n - 1)$ messages and $n$ exps per member for $n$ in $\{2, 3, 4, 6\}$.

| Protocol | Rounds | Messages | Exps per member |
|---|---|---|---|
| ITW | $n - 1$ | $n(n - 1)$ | $n$ |
| [GDH.2](/group-diffie-hellman/) | $n$ | $n$ | up to $n$ |
| [Burmester-Desmedt](/burmester-desmedt/) | 2 | $2n$ | 3 |

## Properties

- **Contributory and symmetric.** Every member contributes $x_i$ and does the same work.
- **Same key as GDH.** The key $g^{x_1 \cdots x_n}$ is the one of [group Diffie-Hellman](/group-diffie-hellman/); GDH gets it with $n$ messages instead of $n(n - 1)$.
- **Neighbor-only messages.** Each member talks only to its two neighbors, which fits a ring network.
- **Sequential.** The $n - 1$ rounds cannot overlap, and one silent member stops the run.
- **Unauthenticated.** Secure only against a passive attacker.
- **No efficient join or leave.** A change of membership needs a full new run.

## Variants and improvements

- **General ITW systems.** The original paper treats a broader class of conference systems; the ring of exponentiations is the form that later work uses.
- **GDH.1 to GDH.3** (1996) keep the key $g^{x_1 \cdots x_n}$ and cut the messages to $O(n)$.
- **Burmester-Desmedt** (1994) uses the same ring with a different key, $g^{x_1 x_2 + x_2 x_3 + \cdots + x_n x_1}$, and only 2 rounds.
- **Authentication.** Any authenticated channel or the Katz-Yung compiler (2003) turns the protocol into one that resists an active attacker.

## When to use it

Use ITW to learn the idea of group Diffie-Hellman and as a baseline. It is rarely the right choice in practice: [Burmester-Desmedt](/burmester-desmedt/) has constant rounds, [GDH.2](/group-diffie-hellman/) has fewer messages, and [TGDH](/tree-based-group-diffie-hellman/) handles joins and leaves. ITW fits only a static group on a ring network where each member can talk only to its neighbors and every member must do the same work.

## Pitfalls

- **Using the new value of the neighbor.** If $M_i$ raises the value that $M_{i-1}$ computed in the same round, the exponents grow by more than one secret per round and members get different keys. Line L5 must use the value $h_{i-1}$ from the end of the previous round, as line L4 delivers it.
- **One round too many.** Running line L5 $n$ times gives $M_i$ the value $g^{x_1 \cdots x_n \cdot x_i}$, which differs from member to member. Stop after $n - 1$ rounds, as line L3 says.
- **Mixed directions.** All members must receive from the left and send to the right. If one member receives from its right in line L4, the runs of secrets no longer cover the ring once each, and the members end with different values.
- **No membership check.** Line L4 must reject values outside $G$, else a value of small order makes the key fall into a small set.
- **No authentication.** A man in the middle on one link can run separate rings with the two sides.
- **Using K directly.** Hash $K$ with the member list before use.

## Implementations

The Python function `run` does lines L1 to L5 for all members at once, checks group membership in line L4, and counts rounds, messages and exps. The tests check agreement with $g^{x_1 \cdots x_n}$ and the counts for $n$ in $\{2, 3, 4, 6\}$, and that for $n = 3$ the key is not one of the values on the wire.

## History

Diffie and Hellman (1976) gave two-party key agreement. Ingemarsson, Tang and Wong (1982) extended it to a conference of $n$ users, the first group key agreement protocol. Burmester and Desmedt (1994) cut the rounds to two, and Steiner, Tsudik and Waidner (1996) cut the messages to $O(n)$ with GDH and gave the security reduction for the product key.

## References
