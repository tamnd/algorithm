---
tag: YAZFG4
kind: algorithm
slug: group-diffie-hellman
name: Group Diffie-Hellman
aliases:
- GDH
- GDH.2
- Steiner-Tsudik-Waidner protocol
area: cryptography/key-exchange
level: advanced
summary: n members compute g^(x_1 ... x_n) by passing a growing list of partial keys along a chain, then one broadcast. Steiner, Tsudik and Waidner (1996), GDH.1 to GDH.3.
solves: [group-key-agreement-problem]
model: word-ram
complexity:
  vars: {n: the number of members, m: the number of binary digits of the modulus p}
  time: {worst: O(n^2 m^3), average: O(n^2 m^3), best: O(n^2 m^3)}
  space: {extra: Θ(n m)}
properties: {deterministic: false, randomized: true}
history:
  year: 1996
  people: [Michael Steiner, Gene Tsudik, Michael Waidner]
  note: Steiner, Tsudik and Waidner gave GDH.1, GDH.2 and GDH.3 at ACM CCS 1996, and the Cliques toolkit for dynamic groups in 2000.
prereqs: [group-key-agreement-problem, diffie-hellman]
see_also: [ingemarsson-tang-wong, burmester-desmedt, tree-based-group-diffie-hellman, decisional-diffie-hellman, modular-exponentiation, authenticated-key-exchange, safe-prime, quadratic-residue]
sources:
  - paper: doi:10.1145/238168.238182
    title: Michael Steiner, Gene Tsudik and Michael Waidner, Diffie-Hellman key distribution extended to group communication, ACM CCS 1996
    locator: the protocols GDH.1, GDH.2 and GDH.3 with their costs in rounds, messages and exponentiations, and the reduction of the group decision problem to the two-party decisional Diffie-Hellman problem
  - paper: "Michael Steiner, Gene Tsudik and Michael Waidner, Key agreement in dynamic peer groups, IEEE Transactions on Parallel and Distributed Systems 11(8), 2000"
    locator: the Cliques protocol suite, initial key agreement IKA.1 and IKA.2, and the auxiliary operations for join, leave, merge and refresh
  - paper: "Giuseppe Ateniese, Michael Steiner and Gene Tsudik, Authenticated group key agreement and friends, ACM CCS 1998"
    locator: the authenticated variants A-GDH.2 and SA-GDH.2
  - paper: "Olivier Pereira and Jean-Jacques Quisquater, A security analysis of the Cliques protocols suites, IEEE Computer Security Foundations Workshop 2001"
    locator: attacks on the authenticated Cliques protocols A-GDH.2 and SA-GDH.2
  - paper: "Emmanuel Bresson, Olivier Chevassut, David Pointcheval and Jean-Jacques Quisquater, Provably authenticated group Diffie-Hellman key exchange, ACM CCS 2001"
    locator: a formal model for authenticated group key exchange and a proof for an authenticated form of GDH.2 in the random oracle model
  - url: "https://www.rfc-editor.org/rfc/rfc5054"
    title: David Taylor, Thomas Wu, Nikos Mavrogiannopoulos and Trevor Perrin, RFC 5054, Using the Secure Remote Password (SRP) Protocol for TLS Authentication, November 2007
    locator: Appendix A, the 1024-bit group, used by the code as a safe prime
---

Group Diffie-Hellman (GDH) is a family of three protocols by Steiner, Tsudik and Waidner (1996) that let $n$ members agree on the key $K = g^{x_1 x_2 \cdots x_n}$, where each member $M_i$ contributes a secret exponent $x_i$. It extends two-party [Diffie-Hellman](/diffie-hellman/) to the [group key agreement problem](/group-key-agreement-problem/). In GDH.2, the main version, the members form a chain: each member raises a growing list of values to its secret and passes the list on, and the last member broadcasts one value for each other member. The cost is $n$ rounds and $n$ messages. GDH protects only against a passive attacker; authentication must be added.

**Notation.** $p = 2q + 1$ is a [safe prime](/safe-prime/), and $g$ generates the subgroup $G$ of [quadratic residues](/quadratic-residue/) modulo $p$, of prime order $q$. Members are $M_1, \ldots, M_n$ with $n \ge 2$, and $x_i \in [1, q)$ is the secret of $M_i$. For a set $S$ of indices, $\pi(S) = \prod_{j \in S} x_j \bmod q$. We write $[i] = \{1, \ldots, i\}$. The cardinal value after $M_i$ is $c_i = g^{\pi([i])}$, and the partial values are $g^{\pi([i] \setminus \{k\})}$ for $k \in [i]$. An exp is one modular exponentiation.

## In plain words

Two people can make a shared secret with Diffie-Hellman: each one raises a public number to a private power, and the order does not matter. A group can do the same in a line. The first member raises the starting number to its power, the second raises the result to its power, and so on. The last member gets the number raised to all the powers, which is the key.

The other members also need the key. So each member, when it passes the number on, also passes a list of values that each lack one member's power. At the end, the last member raises each of these to its own power and sends one value to each member. Each member then adds its own power and gets the key.

## The problem

$n$ members, each with a private random input, must output the same key that depends on all inputs, while a passive eavesdropper who sees all messages cannot tell the key from a random group element. See [group key agreement](/group-key-agreement-problem/). GDH aims at few messages and a simple order of steps; the price is $n$ sequential rounds.

## The algorithm

```pseudo id=main
GDH2(M_1, ..., M_n; p, q, g)          ▷ Steiner, Tsudik and Waidner, CCS 1996
L1  flow ← (partials = (), card = g)     ▷ M_1 starts from g
    for i = 1 to n − 1:                    ▷ upflow
L2    M_i: P ← (v^(x_i) for v in flow.partials) ‖ (flow.card)
L3    M_i: c ← flow.card^(x_i)
L4    M_i → M_(i+1): flow ← (P, c)
L5  M_n: K ← flow.card^(x_n)
L6  M_n broadcasts B ← (v^(x_n) for v in flow.partials)    ▷ B[i] = g^(π([n] \ {i}))
L7  each M_i with i < n: K ← B[i]^(x_i)
```

In the upflow (lines L1 to L4), the message that $M_i$ sends to $M_{i+1}$ holds $i$ partial values and the cardinal value. Line L2 raises every partial value it receives to $x_i$ and adds the old cardinal value, which lacks exactly $x_i$, as a new partial value. Line L3 raises the cardinal value to $x_i$. So after $M_i$, the partial value at position $k$ is $g^{\pi([i] \setminus \{k\})}$, and the cardinal value is $c_i = g^{\pi([i])}$.

$M_n$ receives $n - 1$ partial values $g^{\pi([n-1] \setminus \{k\})}$ and the cardinal value $c_{n-1}$. Line L5 gives $K = c_{n-1}^{x_n}$. Line L6 raises every partial value to $x_n$, so $B[k] = g^{\pi([n] \setminus \{k\})}$, the key without $x_k$. Line L7 adds the missing factor. Each member checks, before each exp, that the value it received lies in $G$; the code rejects values outside the subgroup, such as $p - 4$.

**About the code.** The Python code is for study only. It is not constant time and must not protect real data. It uses the 1024-bit safe prime of RFC 5054, Appendix A, with $g = 4$, which is too small for new systems. The code counts only the exps of the protocol, not the exps of the membership checks. The protocol is unauthenticated, and there are no official test vectors for GDH.

## Example

Take $p = 23$, $q = 11$ and $g = 4$, which has order 11 modulo 23. Three members pick $x_1 = 2$, $x_2 = 3$ and $x_3 = 5$, so $\pi([3]) = 30 \equiv 8 \pmod{11}$ and $K = 4^8 \bmod 23 = 9$.

| Step | Who | Computes | Sends |
|---|---|---|---|
| L2, L3 | $M_1$ | partials $(4)$, card $4^2 = 16$ | $((4), 16)$ to $M_2$ |
| L2, L3 | $M_2$ | partials $(4^3, 16) = (18, 16)$, card $16^3 = 2$ | $((18, 16), 2)$ to $M_3$ |
| L5 | $M_3$ | $K = 2^5 = 9$ | |
| L6 | $M_3$ | $18^5 = 3$, $16^5 = 6$ | broadcast $(3, 6)$ |
| L7 | $M_1$ | $3^2 = 9$ | |
| L7 | $M_2$ | $6^3 = 9$ | |

All three hold 9. $B[1] = 3 = 4^{x_2 x_3} = 4^{15 \bmod 11}$, which lacks $x_1$, and $B[2] = 6 = 4^{x_1 x_3}$. The members did 2, 3 and 3 exps: $M_1$ two, $M_2$ three and $M_3$ three, which matches the counts below. The code gives the same values when run on this group.

## Correctness

**Claim.** In an honest run, every member outputs $K = g^{\pi([n])}$. The invariant of the upflow is: the flow sent by $M_i$ is $\bigl((g^{\pi([i] \setminus \{k\})})_{k=1}^{i},\ g^{\pi([i])}\bigr)$. It holds for $i = 1$, since $M_1$ outputs $((g), g^{x_1})$. If it holds for $i - 1$, then line L2 maps $g^{\pi([i-1] \setminus \{k\})}$ to $g^{\pi([i] \setminus \{k\})}$ for $k < i$ and adds $g^{\pi([i-1])} = g^{\pi([i] \setminus \{i\})}$, and line L3 gives $g^{\pi([i])}$. With $i = n - 1$, line L5 gives $g^{\pi([n])}$, line L6 gives $B[k] = g^{\pi([n] \setminus \{k\})}$, and line L7 gives $g^{\pi([n])}$. The full proof is on the proof page.

**Security.** Against a passive attacker, the transcript holds values $g^{\pi(S)}$ for many proper subsets $S$ of $[n]$. Steiner, Tsudik and Waidner show that telling $g^{\pi([n])}$ from random given all such values, the group decisional Diffie-Hellman problem, is as hard as the two-party [decisional Diffie-Hellman](/decisional-diffie-hellman/) problem, with a loss that grows with $n$.

## Complexity

Member $M_i$ with $i < n$ does $i$ exps in the upflow and one in line L7, so $i + 1$ exps; $M_n$ does $n$. The total is $\sum_{i=1}^{n-1}(i + 1) + n = (n^2 + 3n)/2 - 1$. There are $n$ rounds and $n$ messages: $n - 1$ upflow messages and one broadcast. The message from $M_i$ holds $i + 1$ group elements, so the total traffic is $\Theta(n^2)$ elements. With schoolbook arithmetic, an exp modulo an $m$-digit $p$ costs $O(m^3)$, so the total time is $O(n^2 m^3)$, and $M_{n-1}$ or $M_n$ store $\Theta(n)$ elements. The tests check the counts for $n$ in $\{2, 3, 5\}$: per member $(2, 2)$, $(2, 3, 3)$ and $(2, 3, 4, 5, 5)$.

| Version | Rounds | Messages | Exps of $M_i$ | Total exps |
|---|---|---|---|---|
| GDH.1 | $2(n - 1)$ | $2(n - 1)$ | $i + 1$, $M_n$: $n$ | $O(n^2)$ |
| GDH.2 | $n$ | $n$ | $i + 1$, $M_n$: $n$ | $(n^2 + 3n)/2 - 1$ |
| GDH.3 | $n + 1$ | $2n - 1$ | at most 4, $M_n$: $n$ | $O(n)$ |

## Properties

- **Contributory.** The key depends on every $x_i$; for a fixed $x_j$, $j \ne i$, the map $x_i \mapsto K$ is a bijection of $[1, q)$ onto $G \setminus \{1\}$.
- **Key independence across runs** when every member picks fresh secrets.
- **Unauthenticated.** An active attacker in the chain can replace values and share a key with each side; see [man-in-the-middle attack](/man-in-the-middle-attack/).
- **Sequential.** The rounds are strictly ordered, so the latency grows with $n$, and one member who does not answer stops the run.
- **Uneven load.** $M_n$ and the late members do $\Theta(n)$ exps; early members do few.
- **Same key as ITW.** The key $g^{x_1 \cdots x_n}$ is the one of [Ingemarsson-Tang-Wong](/ingemarsson-tang-wong/), with $n$ messages in place of $n(n - 1)$.

## Variants and improvements

- **GDH.1.** The upflow carries only the cardinal values $c_1, \ldots, c_i$; a downflow from $M_n$ back to $M_1$ then gives each member the value that lacks its exponent. $2(n - 1)$ rounds.
- **GDH.3.** The upflow carries only the cardinal value up to $M_{n-1}$, which broadcasts $c_{n-1}$. Each $M_i$ removes its own exponent with $x_i^{-1} \bmod q$ and sends $c_{n-1}^{1/x_i}$ to $M_n$, which raises each to $x_n$ and broadcasts them. Each member except $M_n$ does a constant number of exps.
- **Cliques** (2000). The protocols IKA.1 (from GDH.2) and IKA.2 (from GDH.3) for the first key, and auxiliary operations for join, leave, merge and refresh, in which the current controller keeps the last flow and updates it at a cost of $O(n)$ exps.
- **Authenticated GDH.** A-GDH.2 and SA-GDH.2 (Ateniese, Steiner and Tsudik, 1998) mix long-term pairwise keys into the flow; Pereira and Quisquater (2001) found attacks on them. Bresson, Chevassut, Pointcheval and Quisquater (2001) proved an authenticated GDH.2 with signatures, and the Katz-Yung compiler applies to GDH as to any passive protocol.
- **Tree-based protocols.** [TGDH](/tree-based-group-diffie-hellman/) replaces the chain with a binary tree, so a change costs $O(\log n)$ exps.

## When to use it

Use GDH.2 to learn group key agreement and as a baseline. For a fixed group that can afford $n$ sequential rounds, it has the fewest messages. For low latency, [Burmester-Desmedt](/burmester-desmedt/) needs 2 rounds. For a group that changes often, use a tree-based protocol, or MLS (RFC 9420) for asynchronous messaging. In any real use, add authentication, for example with the Katz-Yung compiler.

## Pitfalls

- **No membership check.** If $M_i$ raises a received value of small order, the key can fall into a small set. Check each received value is in $G$ before line L2, L5 or L7, as the code does.
- **Wrong element in the partial list.** If line L2 appends the new cardinal value $c_i$ in place of the old one, $M_i$ cannot later recover the key: the appended value must be the old `flow.card`, which lacks $x_i$, not `flow.card^(x_i)`.
- **Raising the wrong position.** In line L7, $M_i$ must use $B[i]$, the value that lacks $x_i$. Any other $B[k]$ gives $g^{\pi([n]) x_i / x_k}$.
- **No authentication.** Lines L4 and L6 have no signatures or MACs, so an active attacker can run a separate GDH with each part of the chain.
- **Reused secrets.** A member who uses the same $x_i$ in two groups lets members of one group help to compute keys of the other.
- **Using K directly.** Hash $K$ with the member list and the transcript before use.

## Implementations

The Python code has a `Member` class with `upflow` (lines L2 and L3), `last` (lines L5 and L6) and `finish` (line L7), and `run`, which does lines L1 and L4 and counts rounds and messages. Every exp checks that its base is in $G$. The tests check agreement with $g^{x_1 \cdots x_n}$ for $n$ in $\{2, 3, 4\}$, the exp counts, the rejection of a value outside the subgroup, and that no single public value $g^{x_i}$ is the key.

## History

Ingemarsson, Tang and Wong (1982) gave the first conference key protocol with the key $g^{x_1 \cdots x_n}$, in a ring with $n - 1$ rounds. Steiner, Tsudik and Waidner (1996) reduced the number of messages with GDH.1, GDH.2 and GDH.3 and proved that the group decision problem reduces to the two-party one. They built the Cliques toolkit for dynamic peer groups (2000). Authenticated versions followed in 1998, and attacks on them in 2001. Bresson, Chevassut, Pointcheval and Quisquater (2001) gave the first formal proof for an authenticated GDH.

## References
