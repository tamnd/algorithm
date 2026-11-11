---
tag: B6HWGP
kind: algorithm
slug: tree-based-group-diffie-hellman
name: Tree-based group Diffie-Hellman
aliases:
- TGDH
- tree-based group key agreement
area: cryptography/key-exchange
level: research
summary: Members sit at the leaves of a binary tree; each inner node key is the Diffie-Hellman key of its children. Join and leave cost O(log n) exps. Kim, Perrig and Tsudik, 2000.
solves: [group-key-agreement-problem]
model: word-ram
complexity:
  vars: {n: the number of members, h: the height of the key tree, m: the number of binary digits of the modulus p}
  time: {worst: O(h m^3), average: O(h m^3), best: O(h m^3)}
  space: {extra: Θ(n m)}
properties: {deterministic: false, randomized: true}
history:
  year: 2000
  people: [Yongdae Kim, Adrian Perrig, Gene Tsudik]
  note: Kim, Perrig and Tsudik gave TGDH at ACM CCS 2000 and the full version in ACM TISSEC in 2004. ART (2018) and TreeKEM in MLS (RFC 9420, 2023) descend from its key tree.
prereqs: [group-key-agreement-problem, diffie-hellman, binary-tree]
see_also: [group-diffie-hellman, burmester-desmedt, ingemarsson-tang-wong, complete-binary-tree, broadcast-encryption, secure-messaging, perfect-forward-secrecy, key-ratchet]
sources:
  - paper: "Yongdae Kim, Adrian Perrig and Gene Tsudik, Simple and fault-tolerant key agreement for dynamic collaborative groups, ACM CCS 2000"
    locator: the key tree, the blinded keys, the join, leave, merge and partition protocols with a sponsor, and the costs
  - paper: "Yongdae Kim, Adrian Perrig and Gene Tsudik, Tree-based group key agreement, ACM Transactions on Information and System Security 7(1), 2004"
    locator: the full version with the security argument under the decisional Diffie-Hellman assumption, the choice of the insertion point (the shallowest rightmost node) and the sponsor rules
  - paper: "Chung Kei Wong, Mohamed Gouda and Simon S. Lam, Secure group communications using key graphs, ACM SIGCOMM 1998"
    locator: the centralized key tree (logical key hierarchy) with O(log n) cost for a membership change
  - paper: "Katriel Cohn-Gordon, Cas Cremers, Luke Garratt, Jon Millican and Kevin Milner, On ends-to-ends encryption: asynchronous group messaging with strong security guarantees, ACM CCS 2018"
    locator: Asynchronous Ratcheting Trees (ART), a Diffie-Hellman key tree for asynchronous groups
  - url: "https://www.rfc-editor.org/rfc/rfc9420"
    title: Richard Barnes, Benjamin Beurdouche, Raphael Robert, Jon Millican, Emad Omara and Katriel Cohn-Gordon, RFC 9420, The Messaging Layer Security (MLS) Protocol, July 2023
    locator: Section 7 (the ratchet tree, path secrets and the TreeKEM update of a path), Section 12 (add, remove and update proposals and commits)
  - url: "https://www.rfc-editor.org/rfc/rfc5054"
    title: David Taylor, Thomas Wu, Nikos Mavrogiannopoulos and Trevor Perrin, RFC 5054, Using the Secure Remote Password (SRP) Protocol for TLS Authentication, November 2007
    locator: Appendix A, the 1024-bit group, used by the code as a safe prime
---

Tree-based group Diffie-Hellman (TGDH) is a protocol for the [group key agreement problem](/group-key-agreement-problem/) in groups whose members join and leave. The members sit at the leaves of a [binary tree](/binary-tree/). Each inner node has a secret key, which is the [Diffie-Hellman](/diffie-hellman/) key of its two children, and a public blinded key $g^{k}$. A member knows the secret keys on the path from its leaf to the root, and the root key is the group key. When a member joins or leaves, one member, the sponsor, picks a new leaf key and publishes the new blinded keys on its path; the others then recompute the keys on their paths. With a balanced tree, each change costs $O(\log n)$ exps. Kim, Perrig and Tsudik gave TGDH in 2000.

**Notation.** $p = 2q + 1$ is a safe prime, and $g$ generates the subgroup $G$ of quadratic residues modulo $p$, of prime order $q$. Each node $v$ of the tree has a secret key $k_v \in [1, q)$ and a blinded key $BK_v = g^{k_v} \bmod p$. For an inner node with children $l$ and $r$, $k_v = f(g^{k_l k_r})$, where $f(x) = x \bmod q$, or 1 if that is 0, maps a group element to an exponent. The path of a member is the list of nodes from its leaf to the root; the co-path is the list of their siblings. $h$ is the height of the tree. An exp is one modular exponentiation.

## In plain words

Pair the members up. Each pair makes a Diffie-Hellman key, so now there are half as many "virtual members". Pair these up and repeat, until one key is left at the top. That is the group key.

To compute the keys on its way to the top, a member needs its own secret and one public value at each level: the public form of the key next to it. So every member computes the group key with about $\log_2 n$ steps.

When someone joins or leaves, only the keys on one path from a leaf to the top change. One member near the change picks a new secret, computes the new keys on its path, and publishes their public forms. Everyone else redoes its own short path. A member who left does not know the new secret, and a new member does not know the old keys.

## The problem

A dynamic group must keep a common key that depends on contributions of its members. When the membership changes, the new key must be unknown to members who left (forward secrecy) and the old keys unknown to members who joined (backward secrecy), at low cost. Rerunning [GDH](/group-diffie-hellman/) or [Burmester-Desmedt](/burmester-desmedt/) costs $\Omega(n)$ work or messages for each change; TGDH aims at $O(\log n)$ exps.

## The algorithm

```pseudo id=main
TGDH key tree                        ▷ Kim, Perrig and Tsudik, CCS 2000
    keys:
L1    for the child c of v on my path:  k_v ← f(BK_sibling(c)^(k_c))     ▷ = f(g^(k_l k_r))
L2    publish BK_v ← g^(k_v) for every inner node v except the root
L3    a member M picks k_M ← random in [1, q) and publishes BK_M ← g^(k_M) at its leaf
    join(M_new):                             ▷ M_new broadcasts BK of its leaf (L3)
L4    s ← the shallowest rightmost leaf; replace s by a new inner node with children s and M_new
L5    sponsor ← the member at s:  k_s ← random in [1, q),  BK_s ← g^(k_s)
L6    the sponsor walks its path to the root with L1 and L2, and broadcasts the new blinded keys
    leave(M_gone):
L7    replace the parent of M_gone's leaf by the sibling subtree of M_gone
L8    sponsor ← the rightmost leaf of that subtree; then run L5 and L6
    all members:
L9    each member walks from its leaf to the root with L1; the root key is the group key
```

Line L1 is two-party Diffie-Hellman at one node: the member knows the secret key $k_c$ of the child on its path and reads the public blinded key of the other child, so it computes $g^{k_c k_{\text{sib}}}$, the same value that a member on the other side computes. Line L2 publishes the blinded keys that members in other subtrees need. The root's blinded key is never needed, so it is not published.

A join (lines L4 to L6) adds a new inner node at a shallow leaf, so the tree stays balanced as it grows. The sponsor refreshes its leaf key in line L5; this supports backward secrecy, since every key on the changed path now depends on a value the new member never saw. A leave (lines L7 and L8) removes the leaf and its parent, and the sponsor in the sibling subtree refreshes its key, which supports forward secrecy, since every key on the changed path now depends on a value the old member never saw. In both cases the changed nodes are exactly the ancestors of the change, and they all lie on the sponsor's path.

**About the code.** The Python code is for study only. It is not constant time and must not protect real data. It uses the 1024-bit safe prime of RFC 5054, Appendix A, with $g = 4$, and the protocol is unauthenticated. It simplifies two things, which the page states plainly: the join inserts at the shallowest rightmost leaf, while the paper inserts at the shallowest rightmost node, which may be an inner node; and $f$ is a reduction modulo $q$. Messages are modelled as one shared public tree. There are no official test vectors for TGDH.

## Example

Take $p = 23$, $q = 11$, $g = 4$, so $f(x) = x \bmod 11$. Three members $A$, $B$, $C$ have leaf keys 2, 3, 5 and blinded keys $16, 18, 12$. The tree is $\mathrm{root}(A, v(B, C))$.

- Node $v$: $B$ computes $f(BK_C^{k_B}) = f(12^3 \bmod 23) = f(3) = 3$, and $C$ computes $f(18^5 \bmod 23) = 3$. So $k_v = 3$ and $BK_v = 4^3 = 18$.
- Root: $A$ computes $f(BK_v^{k_A}) = f(18^2 \bmod 23) = 2$, and $B$ and $C$ compute $f(BK_A^{k_v}) = f(16^3 \bmod 23) = 2$. The group key is 2.

Now $D$ joins with leaf key 4 and $BK_D = 3$. The shallowest rightmost leaf is $A$ at depth 1, so $A$ is replaced by $u(A, D)$, and $A$ is the sponsor. It picks a new leaf key 6 ($BK_A = 4^6 = 2$), computes $k_u = f(3^6 \bmod 23) = f(16) = 5$ and $BK_u = 4^5 = 12$, then the root key $f(18^5 \bmod 23) = 3$. It publishes $BK_A = 2$ and $BK_u = 12$. $D$ computes $k_u = f(2^4) = 5$ and the root $f(18^5) = 3$; $B$ and $C$ compute $f(BK_u^{k_v}) = f(12^3) = 3$. The new group key is 3. The sponsor did 4 exps, $2h$ for its depth $h = 2$. With $q = 11$ such small numbers collide easily; the code uses the 1024-bit group.

## Correctness

**Claim.** After any sequence of joins and leaves, every member computes the same root key. The key of each inner node is symmetric in its two children: $f(BK_r^{k_l}) = f(g^{k_l k_r}) = f(BK_l^{k_r})$. By induction on the height of a node, every member below it computes the same $k_v$, and the published $BK_v$ equals $g^{k_v}$. A join or a leave changes only the ancestors of the change, and these all lie on the sponsor's path, so line L6 republishes all the blinded keys that changed. The full proof is on the proof page.

**Security.** Kim, Perrig and Tsudik argue that, against a passive adversary, the group key is indistinguishable from random under the [decisional Diffie-Hellman](/decisional-diffie-hellman/) assumption, and that the refresh of the sponsor's leaf key gives forward and backward secrecy and key independence. The tests check, for this code, that a new member cannot get the old key from its leaf key and the public tree, and that a member who left cannot get the new key from all the keys it knew and the new public tree.

## Complexity

A member at depth $d$ computes the group key with $d$ exps (line L1 once per level). The sponsor does $2d$ exps on a change: one for its blinded leaf key, $d$ for the keys and $d - 1$ for the blinded keys. Every other member does at most $h$ exps. A join takes 2 rounds (the request and the sponsor's broadcast) and a leave 1 round, each with $O(1)$ broadcast messages of $O(h)$ blinded keys. If only joins happen, the insertion at the shallowest leaf keeps $h = \lceil \log_2 n \rceil$; the tests check height 3 for 6 and 8 members and height 4 after the 9th. Leaves can unbalance the tree, up to $h = n - 1$ in the worst case. With schoolbook arithmetic, the time per member is $O(h m^3)$. Each member stores the tree of blinded keys, $\Theta(n m)$.

| Protocol | Cost of a join or leave per member | Rounds |
|---|---|---|
| Rerun [Burmester-Desmedt](/burmester-desmedt/) | 3 exps, $2n$ messages | 2 |
| Cliques / [GDH](/group-diffie-hellman/) | $O(n)$ exps for the controller | 1 or 2 |
| TGDH | $O(\log n)$ exps if balanced | 1 or 2 |

## Properties

- **Contributory.** Every leaf key enters the root key.
- **Forward and backward secrecy** for membership changes, from the sponsor's fresh leaf key, and key independence.
- **Logarithmic cost** for each change when the tree is balanced.
- **Fault tolerant.** Any member who holds the public tree can act as sponsor; merge and partition, for example after a network split, are handled by the same tree operations.
- **Unauthenticated** in its basic form; messages must be signed in practice.
- **Synchronous.** Members must be online to update their paths; this is what ART and TreeKEM relax.

## Variants and improvements

- **Insertion at a node.** The paper inserts a new member at the shallowest rightmost node where the join does not increase the height, or at the root; this can be an inner node, which keeps the tree flatter than the leaf rule of the code.
- **Merge and partition.** Two trees merge by joining the smaller tree at the insertion point of the larger. A partition removes many leaves at once; sponsors refresh in several rounds.
- **STR** (Kim, Perrig and Tsudik, 2001): a tree of maximal height, a chain, with cheap joins and costly leaves, for small groups on high-latency networks.
- **Logical key hierarchy** (Wong, Gouda and Lam, 1998): the same tree with keys chosen by a central controller, not contributory.
- **ART** (Cohn-Gordon and others, 2018): a TGDH-like tree for asynchronous group messaging, in which a member updates its path with Diffie-Hellman against stored public keys.
- **TreeKEM** in MLS (RFC 9420): the path is updated with public-key encryption of path secrets to the co-path, so a member can update while others are offline.

## When to use it

Use TGDH, or a descendant, for a contributory group key in a group whose membership changes often and where all members are online, such as a collaborative session. For a static group, [Burmester-Desmedt](/burmester-desmedt/) is simpler. For asynchronous messaging, use MLS (RFC 9420). In every case, add authentication of the broadcast messages.

## Pitfalls

- **No refresh by the sponsor.** If the sponsor keeps its old leaf key, keys repeat: when a member joins and then leaves, the tree returns to its old shape with the old leaf keys, so the group key returns to its old value, and key independence fails. Line L5 must pick a fresh $k_s$, not reuse the old one.
- **Wrong sponsor.** The sponsor's path must contain every changed node. After a leave, choose the sponsor inside the promoted sibling subtree, as in line L8, not any member of the group.
- **Publishing the root's blinded key.** It gives no secret away by itself, but it is not needed; line L2 publishes blinded keys only for nodes below the root.
- **Keys used as exponents without a map.** $g^{k_l k_r}$ is a group element, not an exponent; line L1 applies $f$. A different $f$ on two sides gives different keys.
- **No membership check.** Blinded keys from other members must be checked to be in $G$.
- **Letting the tree degrade.** Leaves can make the tree deep; the paper's insertion rule and occasional rebalancing keep $h$ near $\log_2 n$.

## Implementations

The Python code has `Member` with `group_key` (line L1, walked as in line L9) and `refresh` (lines L5, L6 and L2), and `Tree` with `join` (line L4) and `leave` (lines L7 and L8); `all_keys` is line L9. The tests check agreement after 6 joins, height 3 for 8 members and 4 after a 9th, the cost of a member's walk, backward secrecy on a join, and that a member who left cannot compute the new key from everything it knew.

## History

Wong, Gouda and Lam (1998) used a key tree with a central controller. Kim, Perrig and Tsudik (2000) made the tree contributory with Diffie-Hellman at each node, and gave the full protocol suite with merge and partition in ACM TISSEC (2004). The idea came back for asynchronous messaging in ART (2018) and in TreeKEM, the core of Messaging Layer Security (RFC 9420, 2023).

## References
