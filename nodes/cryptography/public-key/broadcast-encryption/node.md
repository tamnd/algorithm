---
tag: FF58G6
kind: problem
slug: broadcast-encryption
name: Broadcast encryption
area: cryptography/public-key
level: advanced
summary: Send one ciphertext to n users so that all users outside a revoked set R can decrypt and the users in R, even together, learn nothing. Subset cover and pairing schemes solve it.
prereqs: [public-key-encryption, symmetric-encryption, complete-binary-tree]
see_also: [identity-based-encryption, attribute-based-encryption, functional-encryption, bilinear-diffie-hellman, group-key-agreement-problem, key-distribution-center, pseudorandom-function, authenticated-encryption]
sources:
  - paper: "Amos Fiat and Moni Naor, Broadcast encryption, Crypto 1993, LNCS 773, pages 480 to 491"
    locator: the definition of the problem, k-resilient schemes, and the schemes from one-way functions and perfect hash families
  - paper: "Dalit Naor, Moni Naor and Jeff Lotspiech, Revocation and tracing schemes for stateless receivers, Crypto 2001, LNCS 2139, pages 41 to 62"
    locator: the subset cover framework, the complete subtree method with header r log(n/r), the subset difference method with header 2r - 1, and subset tracing
  - paper: "Dani Halevy and Adi Shamir, The LSD broadcast encryption scheme, Crypto 2002, LNCS 2442, pages 47 to 60"
    locator: the layered subset difference method, which keeps an O(r) header with fewer keys per user than subset difference
  - paper: "Dan Boneh, Craig Gentry and Brent Waters, Collusion resistant broadcast encryption with short ciphertexts and private keys, Crypto 2005, LNCS 3621, pages 258 to 275"
    locator: the scheme with a constant-size header and private key and an O(n) public key, the sqrt(n) trade-off, and the n-BDHE assumption
  - paper: "Michael Luby and Jessica Staddon, Combinatorial bounds for broadcast encryption, Eurocrypt 1998, LNCS 1403, pages 512 to 526"
    locator: the lower bounds that trade the number of keys per user against the number of transmissions
  - paper: "Yevgeniy Dodis and Nelly Fazio, Public key broadcast encryption for stateless receivers, ACM Workshop on Digital Rights Management 2002, LNCS 2696, pages 61 to 80"
    locator: the public-key versions of the subset cover methods, from identity-based and hierarchical identity-based encryption
  - paper: "Benny Chor, Amos Fiat and Moni Naor, Tracing traitors, Crypto 1994, LNCS 839, pages 257 to 270"
    locator: the related problem of finding the users whose keys were used to build a pirate decoder
  - paper: "Dan Boneh and Mark Zhandry, Multiparty key exchange, efficient traitor tracing, and more from indistinguishability obfuscation, Crypto 2014, LNCS 8616, pages 480 to 499"
    locator: the broadcast encryption with header, keys and public key all polylogarithmic in n, from indistinguishability obfuscation
---

Broadcast encryption is the problem of sending one encrypted message over a shared channel to a large set of users so that only a chosen subset can read it. The typical case is revocation: there are $n$ users, a small set $R$ of them is revoked, and everybody else must decrypt. Amos Fiat and Moni Naor defined the problem in 1993. Naor, Naor and Lotspiech gave the subset cover methods in 2001, and one of them, subset difference, protects HD DVD and Blu-ray discs in the AACS system. Boneh, Gentry and Waters gave a pairing scheme in 2005 whose header has a constant size for any set.

**Notation.** $N = \{0, \ldots, n - 1\}$ is the set of users, $R \subseteq N$ the revoked users, $r = |R|$, and $S = N \setminus R$ the privileged users. $K$ is a fresh session key, $M$ the message, and $E_K(M)$ a [symmetric cipher](/symmetric-encryption/) under $K$. The **header** is the part of the ciphertext that lets members of $S$ find $K$; its length, counted in wrapped keys or group elements, is the main cost. $\log$ is to base 2.

## In plain words

A pay-TV station sends one signal to a million boxes. Some customers stop paying, and some boxes are hacked and their keys copied. The station wants to keep sending one signal that every paying box can decode and that the bad boxes cannot decode, even if the people who own them pool their keys.

Two simple answers exist. Give each box its own key and encrypt the content key once for each good box: the signal grows with the number of customers. Or give each box a key for every possible group: the signal is short, but each box stores an enormous number of keys. Broadcast encryption looks for schemes between these two, where the extra signal grows with the number of bad boxes and each box stores few keys. The boxes are stateless: their keys are fixed at the factory and never updated.

## Definition

A broadcast encryption scheme has three algorithms.

- **Setup$(n)$** gives each user $u$ a secret key $d_u$ and, for public-key schemes, outputs a public key $PK$.
- **Encrypt$(S, M)$** returns a ciphertext $(S, \mathrm{Hdr}, E_K(M))$. In the secret-key setting only the center can encrypt; in the public-key setting anybody can, with $PK$.
- **Decrypt$(u, d_u, S, \mathrm{Hdr}, C)$** returns $M$ if $u \in S$.

**Input to the problem.** $n$ and a security parameter $\lambda$.

**Output.** A scheme that is correct, meaning every $u \in S$ decrypts every ciphertext for $S$, and secure, meaning that a coalition of users outside $S$ learns nothing about $M$.

**Security.** An adversary picks a set $S^*$ and receives the keys $d_u$ of all $u \notin S^*$. It then gets an encryption for $S^*$ of one of two messages of its choice and must guess which. The scheme is secure if every efficient adversary guesses with probability at most $\frac{1}{2}$ plus a negligible amount. This is **full collusion resistance**: the coalition may contain every revoked user. In the **static** model the adversary chooses $S^*$ before it sees any key; in the **adaptive** model it can ask for keys one at a time and choose $S^*$ later. A scheme is **$k$-resilient** if security holds only for coalitions of at most $k$ users.

**Costs.** The header length, the number of keys each user stores, the decryption time, and, for public-key schemes, the size of $PK$.

## Variants

- **$k$-resilient broadcast.** Fiat and Naor (1993) solved the problem for coalitions of at most $k$ users. For $k = 1$, give each user $v$ a key $K_v$, give user $u$ every $K_v$ with $v \neq u$, and use as session key for $S$ the sum of the $K_v$ for $v \notin S$. Every member of $S$ has all these keys and every non-member lacks its own, but two non-members together have everything. They then reduced the storage with one-way functions and lifted the result to larger $k$ with perfect hash families.
- **Stateless and stateful receivers.** In the stateless model of this page the keys never change. Stateful receivers can take key updates; the logical key hierarchy of Wallner, Harder and Agee and of Wong, Gouda and Lam then rekeys a group after each change with $O(\log n)$ messages. This is closer to [group key agreement](/group-key-agreement-problem/) and to a [key distribution center](/key-distribution-center/).
- **Public-key broadcast encryption.** Anybody can encrypt to any set. Dodis and Fazio (2002) built the public-key forms of the subset cover methods from [identity-based encryption](/identity-based-encryption/) and its hierarchical form. The scheme of Boneh, Gentry and Waters is public key from the start.
- **Trace and revoke.** A pirate decoder built from leaked keys should lead back to at least one of those keys, which can then be revoked. This is traitor tracing (Chor, Fiat and Naor, 1994). The subset cover methods support a form of it called subset tracing.
- **Anonymous broadcast.** The ciphertext also hides $S$. The schemes above send $S$ or $R$ in the clear.
- **Broadcast as a policy.** [Attribute-based encryption](/attribute-based-encryption/) with an OR over user names, and [functional encryption](/functional-encryption/) for the function "$M$ if $u \in S$", both include broadcast encryption as a special case.

## Examples

**The complete subtree cover for $n = 8$.** Number the nodes of a complete binary tree as in a heap: the root is 1, the children of $v$ are $2v$ and $2v + 1$, and user $u$ sits at leaf $8 + u$. Each node $v$ has a key $L_v$, and user $u$ stores the keys on its path to the root. User 3, at leaf 11, stores $L_{11}, L_5, L_2, L_1$, which is $\log n + 1 = 4$ keys.

Revoke $R = \{2, 5\}$, at leaves 10 and 13. Their paths to the root are $10, 5, 2, 1$ and $13, 6, 3, 1$, and together these form the Steiner tree of $R$. The cover is every child of a Steiner tree node that is not itself in the Steiner tree.

| Steiner node | children | child off the tree | users below it |
|---|---|---|---|
| 1 | 2, 3 | none | |
| 2 | 4, 5 | 4 | 0, 1 |
| 3 | 6, 7 | 7 | 6, 7 |
| 5 | 10, 11 | 11 | 3 |
| 6 | 12, 13 | 12 | 4 |

The header is $E_{L_4}(K), E_{L_7}(K), E_{L_{11}}(K), E_{L_{12}}(K)$: four wrapped keys, which is $r \log(n / r) = 2 \log 4 = 4$. User 3 finds node 11 in the header and holds $L_{11}$. User 2 holds $L_{10}, L_5, L_2, L_1$ and user 5 holds $L_{13}, L_6, L_3, L_1$; none of these is a cover node, so even together they cannot unwrap $K$. The trivial scheme with one key per user would need $n - r = 6$ wrapped keys.

**The subset difference cover for the same case.** Subset difference uses the sets $S_{i,j}$, the leaves below node $i$ minus the leaves below its descendant $j$. For $R = \{2, 5\}$ the cover is $S_{2,10} = \{0, 1, 3\}$ and $S_{3,13} = \{4, 6, 7\}$: two wrapped keys, within the bound $2r - 1 = 3$.

**The code with this page.** The Python file implements the complete subtree method with the heap numbering above. The node keys come from a master secret through HMAC-SHA256, and the key wrap and body cipher are toys built from HMAC-SHA256 with a tag. The code is for study only and is not constant time. A real system wraps keys with AES key wrap (RFC 3394) or AES as AACS does, and encrypts the body with an [authenticated cipher](/authenticated-encryption/). There are no official test vectors for the complete subtree method; AACS uses subset difference with licensed keys. The tests check the table above, that the cover is exact and disjoint for every revoked set of 8 users and for random sets of 64 users, the bound $r \log(n / r)$ for $n = 1024$, that all users outside $R$ decrypt and the users in $R$, alone or together, do not, and that a changed body is rejected. The seeds are fixed.

## Known algorithms

| scheme | header | keys per user | public key | assumption |
|---|---|---|---|---|
| one key per user | $n - r$ | 1 | none or $n$ | any cipher |
| one key per subset | 1 | $2^{n-1}$ | none | any cipher |
| Fiat and Naor 1993, $k$-resilient | polynomial in $k$ and $\log n$ | polynomial in $k$ and $\log n$ | none | one-way functions |
| complete subtree (NNL 2001) | at most $r \log(n / r)$, and 1 if $r = 0$ | $\log n + 1$ | none | any cipher |
| subset difference (NNL 2001) | at most $2r - 1$ | $\frac{1}{2}\log^2 n + \frac{1}{2}\log n + 1$ | none | pseudorandom generator |
| layered subset difference (Halevy and Shamir 2002) | $O(r)$ | $O(\log^{3/2} n)$ | none | pseudorandom generator |
| Boneh, Gentry and Waters 2005 | 2 group elements | 1 group element | $O(n)$ | $n$-BDHE |
| BGW 2005, second scheme | $O(\sqrt{n})$ | 1 group element | $O(\sqrt{n})$ | $n$-BDHE |
| Boneh and Zhandry 2014 | polylog $n$ | polylog $n$ | polylog $n$ | indistinguishability obfuscation |

**Subset cover framework.** Naor, Naor and Lotspiech fix a family of subsets $S_1, S_2, \ldots$ of the users, each with a key $L_i$, and give each user what it needs to derive $L_i$ for every $S_i$ that contains it. To revoke $R$, the center covers $N \setminus R$ with disjoint sets of the family and sends $[i_1, \ldots, i_m, E_{L_{i_1}}(K), \ldots, E_{L_{i_m}}(K), E_K(M)]$. A member of $S$ finds its set in the list, derives the key, unwraps $K$ and decrypts. The complete subtree method computes its cover as follows.

```pseudo
CS-COVER(n, R)
1   if R is empty: return [root]
2   T ← the union of the paths from the leaves of R to the root
3   C ← empty list
4   for each inner node v in T:
5       for each child c of v:
6           if c ∉ T: append c to C
7   return C
```

The cover is disjoint and exact: a user $u \notin R$ lies below exactly one node where its path leaves $T$, and a user in $R$ lies below no node of $C$, since its whole path is in $T$. The same fact gives collusion resistance: no key on the path of a revoked user is a key of the cover, so even all of $R$ together holds none of the $L_v$ in the header. Finding one's own cover node takes $O(\log \log n)$ steps with a binary search on the depth.

**Subset difference.** The keys of the sets $S_{i,j}$ come from a tree of pseudorandom generator calls, so a user stores $O(\log^2 n)$ labels instead of the $O(n)$ keys of all sets that contain it, and decryption needs $O(\log n)$ generator calls. The header is at most $2r - 1$. AACS uses this method.

**Boneh, Gentry and Waters.** The public key is $g, g^{\alpha}, g^{\alpha^2}, \ldots$ up to $g^{\alpha^{2n}}$ without $g^{\alpha^{n+1}}$, plus $v = g^{\gamma}$, in a group with a [bilinear pairing](/bilinear-pairing/). User $i$ holds $g^{\gamma \alpha^i}$. The header for $S$ is two group elements, and the session key is $e(g, g)^{\alpha^{n+1} t}$ for a random $t$. Decryption needs the public key elements for every member of $S$, so it costs $O(|S|)$ group operations, and the public key grows with $n$. Security is static, under the decisional $n$-bilinear Diffie-Hellman exponent assumption, a $q$-type relative of [bilinear Diffie-Hellman](/bilinear-diffie-hellman/).

## Bounds

**The complete subtree bound.** The cover has at most $r \log(n / r)$ nodes. A cover node hangs off a Steiner tree node that has exactly one child in the Steiner tree, and the Steiner tree of $r$ leaves in a tree of depth $\log n$ has at most $r \log(n / r)$ such nodes. The bound is tight for this method: when $r$ is a power of 2 and the revoked users are evenly spaced, the top $\log r$ levels are full and each of the $r$ lower subtrees of depth $\log(n / r)$ adds one cover node per level. For $n = 8$ and $R = \{0, 4\}$ the cover is $\{5, 7, 9, 13\}$, again four nodes.

**The subset difference bound.** The header is at most $2r - 1$ for any $R$, and at most 1 if $R$ is empty. Naor, Naor and Lotspiech prove this by charging each set of the cover to a merge of two Steiner tree branches.

**Lower bounds.** Luby and Staddon (1998) showed that, in schemes where the header is made of encryptions under keys from a fixed pool, few keys per user force a long header and a short header forces many keys. Any scheme needs a header of at least about $\lambda$ binary digits for the session key, which BGW reaches up to a constant factor. No scheme with a constant header, constant user keys and a short public key is known from standard pairing assumptions; schemes with all three costs polylogarithmic in $n$ are known from indistinguishability obfuscation (Boneh and Zhandry 2014) and from newer lattice assumptions.

## Reductions

Write $P \le Q$ if an algorithm for $Q$ gives an algorithm for $P$ with polynomial overhead.

- **Broadcast encryption from any cipher.** One key per user and $E_{K_u}(K)$ for each $u \in S$ is correct and fully collusion resistant if the cipher is IND-CPA. The subset cover methods keep this security argument and shrink the header.
- **Security of subset cover.** Naor, Naor and Lotspiech reduce the security of a subset cover scheme to two properties: the key wrap and the body cipher are secure, and the key of each set looks random to all users outside that set together. With independent keys, as in the complete subtree method, the second property is immediate. With keys from a pseudorandom generator, as in subset difference, it reduces to the security of the generator.
- **Public key from IBE.** Treat each node $v$ as an identity and give user $u$ the [IBE](/identity-based-encryption/) keys of the nodes on its path. Anybody can then encrypt $K$ to the cover nodes with the IBE public parameters. This turns the complete subtree method into a public-key scheme with header $r \log(n / r)$ IBE ciphertexts. Subset difference needs hierarchical IBE (Dodis and Fazio 2002).
- **Broadcast from ABE and FE.** Give user $u$ the attribute "$u$" and encrypt under the policy "$u_1$ OR $u_2$ OR $\ldots$" over $S$ with ciphertext-policy ABE. The header then grows with $|S|$ in most such schemes, so this is correct but not efficient.

## Applications

- **Optical disc content protection.** AACS, the system of HD DVD and Blu-ray, puts a Media Key Block on each disc. The block is a subset difference header that gives the media key to every licensed player whose keys are not revoked. When keys of a software player were extracted and published in 2006 and 2007, new discs revoked those keys, and the players had to be updated with new keys.
- **Pay television and satellite radio.** Conditional access systems send one stream to many receivers and must cut off receivers that stop paying or are cloned. Most deployed systems use stateful receivers with key updates, but the cost model is the same.
- **Encrypted group storage and messaging.** A file or message encrypted once for a large group, with members removed over time, needs the same trade-off between header length and keys per member.
- **Revocation in public-key systems.** Public-key broadcast encryption lets any sender exclude a revoked set without a key update for the remaining users.

## References
