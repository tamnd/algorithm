---
tag: ZKP16F
kind: algorithm
slug: wagners-algorithm
name: Wagner's algorithm
aliases:
- Wagner k-tree algorithm
- Wagner's k-tree algorithm
- generalized birthday algorithm
area: cryptography/hash-functions
level: research
summary: Find one value in each of k lists so that the k values XOR to zero, by merging lists in pairs on a few bits at a time. For k = 4 and n-bit values it takes about 2^(n/3) time.
solves: [generalized-birthday-problem]
model: query-model
complexity:
  vars: {n: the bit length of the values, k: the number of lists 2^t, t: the depth of the tree}
  time: {average: O(k 2^(n/(1+t)))}
  space: {extra: O(k 2^(n/(1+t)))}
properties: {deterministic: true}
history:
  year: 2002
  people: [David Wagner]
  note: Wagner gave the k-tree algorithm at CRYPTO 2002, with attacks on incremental hashing, blind signatures and other systems that rest on a k-sum being hard.
prereqs: [generalized-birthday-problem]
see_also: [generalized-birthday-problem, birthday-attack, schroeppel-shamir-algorithm, knapsack-problem, blind-signature, schnorr-signature, proof-of-work, meet-in-the-middle-attack]
sources:
  - paper: "David Wagner, A generalized birthday problem, CRYPTO 2002, LNCS 2442, pages 288 to 303"
    locator: Section 3 (the 4-list algorithm in 2^(n/3) and the k-tree algorithm for k = 2^t), Section 4 (applications to incremental hashing, blind signatures and knapsacks)
  - paper: "Alex Biryukov and Dmitry Khovratovich, Equihash: asymmetric proof-of-work based on the generalized birthday problem, NDSS 2016"
    locator: the Equihash puzzle, its parameters, and the algorithm-binding condition on the indices
  - paper: "Fabrice Benhamouda, Tancrede Lepoint, Julian Loss, Michele Orru and Mariana Raykova, On the (in)security of ROS, EUROCRYPT 2021, LNCS 12696, pages 33 to 53"
    locator: the polynomial-time attack on ROS with more than log p sessions, and its comparison with Wagner's subexponential attack
  - paper: "Claus-Peter Schnorr, Security of blind discrete log signatures against interactive attacks, ICICS 2001, LNCS 2229, pages 1 to 12"
    locator: the ROS problem and the reduction from blind Schnorr signatures
  - paper: "Avrim Blum, Adam Kalai and Hal Wasserman, Noise-tolerant learning, the parity problem, and the statistical query model, Journal of the ACM 50(4), 2003, pages 506 to 519"
    locator: the BKW algorithm, which cancels bits block by block in the same way
  - paper: "Lorenz Minder and Alistair Sinclair, The extended k-tree algorithm, Journal of Cryptology 25(2), 2012, pages 349 to 382"
    locator: the k-tree algorithm with lists smaller than 2^(n/(1+t))
  - paper: "Itai Dinur, An algorithmic framework for the generalized birthday problem, Designs, Codes and Cryptography 87, 2019, pages 1897 to 1926"
    locator: time-memory tradeoffs for the k-list problem below the memory of the k-tree
---

Wagner's algorithm, also called the k-tree algorithm, solves the [generalized birthday problem](/generalized-birthday-problem/): given $k$ lists of random $n$-bit values, find one value from each list so that all $k$ values XOR to zero. The plain [birthday attack](/birthday-attack/) solves the case $k = 2$ in $2^{n/2}$. Wagner showed in 2002 that for $k = 4$ the cost drops to about $2^{n/3}$, and for $k = 2^t$ to about $k \cdot 2^{n/(1+t)}$. The trick is to merge the lists in pairs and, at each merge, keep only the sums that are zero on a few more bits. The result broke several designs that assumed a sum of many hash values is as hard to control as one: incremental hashes, blind signatures, and some knapsack hashes. It is also the basis of the Equihash proof of work.

## In plain words

You have four bags of random numbers, each written as a string of ones and zeros. You want one number from each bag so that, combined bit by bit with exclusive or, they give all zeros.

Do not try all ways to pick four numbers. First pair up bag one and bag two. Keep only the pairs whose combination ends in, say, ten zeros. Do the same for bags three and four. Now you have two new bags, and all numbers in them already end in ten zeros. Find one number in each new bag that is equal on the remaining bits. That is a pair of pairs, so it gives four numbers that cancel.

Each step is a small birthday search. Splitting the work into steps makes it much cheaper.

## The problem

The input is $k$ lists $L_1, \ldots, L_k$ of $n$-bit values, each of size $L$, and the goal is indices $i_1, \ldots, i_k$ with

$$L_1[i_1] \oplus L_2[i_2] \oplus \cdots \oplus L_k[i_k] = 0.$$

In the attacks, $L_j[i] = H_j(i)$ for hash functions that can be queried, so the attacker can choose the list size. The cost counts list entries made and handled. For the analysis, the values are independent and uniform. See the [generalized birthday problem](/generalized-birthday-problem/) for the problem, its variants and its lower bounds. This page is the algorithm.

## The algorithm

The case $k = 4$, with $\ell = \lceil n/3 \rceil$ and $\mathrm{low}_\ell(x)$ the low $\ell$ bits of $x$:

```pseudo id=main
WAGNER-4(L1, L2, L3, L4, n)
L1  ℓ ← ⌈n/3⌉
L2  L12 ← {(x1 ⊕ x2, i1, i2) : x1 = L1[i1], x2 = L2[i2], low_ℓ(x1) = low_ℓ(x2)}
L3  L34 ← {(x3 ⊕ x4, i3, i4) : x3 = L3[i3], x4 = L4[i4], low_ℓ(x3) = low_ℓ(x4)}
L4  for each (u, i1, i2) ∈ L12 and (v, i3, i4) ∈ L34 with u = v do
L5      output (i1, i2, i3, i4)                 ▷ x1 ⊕ x2 ⊕ x3 ⊕ x4 = u ⊕ v = 0
```

Each line L2 to L4 is a join: put one list in a [hash table](/hash-table/) keyed on the bits that must match, then scan the other list. This is the merge step of a sort-merge join, and sorting works as well.

**General $k = 2^t$.** Use $\ell = \lceil n/(1+t) \rceil$. The leaves are the $k$ lists. At each of the levels $1, \ldots, t - 1$, join the lists in pairs and keep the XORs that are zero on the next $\ell$ bits. The values at level $j$ are zero on their low $j\ell$ bits. At the root, join the last two lists on all remaining $n - (t-1)\ell \le 2\ell$ bits.

The Python code for this page runs WAGNER-4 on lists of SHA-256 values cut to 30 and 36 bits, and the tree for 8 lists at 32 bits. It is for study only and it is not constant time. Its only targets are such toy lists.

## Example

Let $L_j[i]$ be the first 30 bits of SHA-256 of the byte $j$ followed by $i$ in 4 bytes, for $j = 0, 1, 2, 3$ and $i < 2^{11}$. So $n = 30$, $\ell = 10$ and $L = 2^{11}$.

- Line L2 keeps 4117 of the $2^{22}$ pairs from $L_0$ and $L_1$, and line L3 keeps 4070. The expected size is $L^2/2^\ell = 4096$.
- Line L4 then finds 10 solutions. The expected number is $L^4/2^{n+\ell} = 2^{44-40} = 16$.
- One solution is the index tuple (1246, 1661, 688, 41), with the values 0x380e9079, 0x39571879, 0x2a23a019 and 0x2b7a2819. The first two XOR to 0x1598800 and the last two XOR to the same value, which ends in 10 zero bits. So all four XOR to zero.
- The whole run handles about $4 \cdot 2^{11} + 2 \cdot 2^{12}$ entries. A plain birthday search for two lists at 30 bits needs about $2^{15}$ entries per list.

At $n = 36$ with $L = 2^{12} = 2^{n/3}$, the expected number of solutions per instance is 1. Over three instances the code found 2. The tree for 8 lists of $2^9$ values at $n = 32$ uses $\ell = 8$ and finds several solutions.

## Correctness

Each tuple output at line L5 is a solution: $u = x_1 \oplus x_2$ and $v = x_3 \oplus x_4$ for list entries with the stated indices, and $u = v$, so $x_1 \oplus x_2 \oplus x_3 \oplus x_4 = u \oplus v = 0$. The algorithm is sound for every input. It is not complete: it finds only solutions whose pair sums are zero on the low $\ell$ bits. For random lists, the expected number of solutions it finds is exactly $L^4/2^{n+\ell}$, which is 1 when $L = 2^\ell$ and $\ell = n/3$. The full proof is below.

## Complexity

For $k = 4$, lists of size $L = 2^\ell$ and $\ell = n/3$:

- **Merges.** Line L2 compares $L^2$ pairs in effect but costs only $O(L + |L_{12}|)$ with a hash table. $\mathbb{E}|L_{12}| = L^2/2^\ell = 2^\ell$.
- **Root.** Line L4 costs $O(|L_{12}| + |L_{34}| + \text{output})$. The expected output is $L^4/2^{n+\ell} = 2^{3\ell - n} = 1$.
- **Total.** $O(2^{n/3})$ time and memory, for one expected solution. With lists of size $c \cdot 2^{n/3}$, the expected number of solutions is $c^4$.

For $k = 2^t$ and $\ell = n/(1+t)$, each level keeps lists of expected size $2^\ell$, and there are $k - 1$ joins. So time and memory are $O(k \cdot 2^{n/(1+t)})$. The exponent drops from $n/2$ for $k = 2$ to $n/3$ for $k = 4$, $n/4$ for $k = 8$, and in the limit $k = 2^{\sqrt n}$ gives the subexponential cost $2^{O(\sqrt n)}$.

| $k$ | $t$ | $\ell = n/(1+t)$ | cost for $n = 128$ |
|---|---|---|---|
| 2 | 1 | $n/2$ | $2^{65}$ |
| 4 | 2 | $n/3$ | $2^{44.7}$ |
| 8 | 3 | $n/4$ | $2^{35}$ |
| 16 | 4 | $n/5$ | $2^{29.6}$ |
| 256 | 8 | $n/9$ | $2^{22.2}$ |

The cost column is $k \cdot 2^{n/(1+t)}$.

## Properties

- **Sound, not complete.** Every output is correct. The algorithm misses solutions whose partial sums are not zero on the chosen bits, and it may find none on a given instance.
- **Needs large lists.** It needs $L \ge 2^{n/(1+t)}$ values per list. With fewer values, the lists shrink at each merge. The extended k-tree of Minder and Sinclair handles smaller lists.
- **Memory as large as time.** The lists must be stored. This is the main obstacle in practice, and the basis of Equihash.
- **Any group with a join.** The same tree works for sums modulo $2^n$ or modulo $m$: at each level keep the sums that lie in a small interval around zero, in place of the sums with zero low bits.
- **Only for $k \ge 3$.** For $k = 2$ the algorithm is the plain birthday attack. For $k = 3$, Wagner's tree gives no gain over $k = 2$ in general.

## Variants and improvements

- **Arbitrary $k$.** For $k$ not a power of two, fix some lists to a single value and use the tree on the largest power of two below $k$.
- **Additive version.** For $\sum x_i \equiv 0 \pmod{2^n}$, merge on the low $\ell$ bits being zero after addition. For a general modulus $m$, keep the sums in an interval of size $m/2^\ell$ around zero.
- **Extended k-tree.** Minder and Sinclair (SODA 2009, J. Cryptology 2012) find a solution when the lists are smaller than $2^{n/(1+t)}$, by merging on fewer bits.
- **Time-memory tradeoffs.** Bernstein (2007) and Dinur (2019) give versions that use less memory, at more time. They matter for Equihash, whose designers chose the parameters so that memory cannot be cut cheaply.
- **[Schroeppel and Shamir](/schroeppel-shamir-algorithm/).** For $k = 4$ lists with only one solution, Schroeppel and Shamir find it in $2^{n/2}$ time and $2^{n/4}$ memory. Wagner's method is faster but needs many solutions to exist.
- **BKW.** The algorithm of Blum, Kalai and Wasserman for learning parity with noise cancels blocks of bits in the same way.

## When to use it

Use it when the attacker can make many values for each of $k$ positions and needs only one combination that sums to a target. Typical cases:

- **Incremental and additive hashes.** A hash $H(M) = h(1, M_1) \oplus \cdots \oplus h(k, M_k)$ is easy to update, but a collision or preimage is a $k$-list problem. Wagner showed that the additive hash AdHash of Bellare and Micciancio needs a much larger modulus than first proposed. The XOR version falls to linear algebra.
- **Knapsack hashes.** A hash that sums chosen vectors modulo $m$ is an instance of the additive problem.
- **Blind Schnorr signatures and ROS.** An attacker who opens $\ell$ signing sessions at once can forge $\ell + 1$ [blind signatures](/blind-signature/) from $\ell$ sessions if he solves the ROS problem of Schnorr (2001). Wagner's tree solves ROS in subexponential time, about $2^{\log p/(1+\log \ell)}$, by building $\ell$ lists of hash values modulo the group order $p$. Benhamouda, Lepoint, Loss, Orrù and Raykova (EUROCRYPT 2021) solved ROS in polynomial time when $\ell > \log p$, by a different method that writes the target in binary. So both attacks rest on the same problem: Wagner's tree works for any $\ell \ge 2$ but costs more as $\ell$ shrinks, and the polynomial attack needs many sessions. For a 256-bit group, about 256 parallel sessions suffice for the polynomial attack. Blind [Schnorr signatures](/schnorr-signature/) and some two-round multisignatures were affected.
- **[Proof of work](/proof-of-work/).** Equihash (Biryukov and Khovratovich, NDSS 2016) asks for $2^K$ hash values that XOR to zero, with an ordering rule on the indices. The best known solver is a k-tree, which needs much memory, so the puzzle resists cheap special hardware. Zcash uses $n = 200$ and $K = 9$: 512 values from a list of $2^{21}$.

## Pitfalls

- **One list or many.** With a single list, the $k$ values must be distinct entries. Equihash adds a rule on index order so that a solution is not reused.
- **Tuples, not values.** Keep the indices with each merged value. Without them, a solution cannot be checked or used.
- **Bit budget.** Merging on too many bits at a level empties the next list. Merging on too few makes the lists grow. Use $\ell = \lceil n/(1+t) \rceil$ and lists of at least $2^\ell$.
- **The final join.** At the root, match on all the remaining bits, not only $\ell$. In the code, the root uses the full mask.
- **Security levels.** A system whose security rests on a sum of $k$ hash values has at most about $n/(1+\lfloor \log_2 k \rfloor)$ bits of security, not $n$.

## Implementations

## History

Wagner presented the k-tree algorithm at CRYPTO 2002. Similar block-by-block cancellation had appeared in the BKW algorithm for learning parity with noise (STOC 2000). Wagner applied the method to incremental hashing, to the ROS problem behind blind Schnorr signatures, to low-weight parity checks for stream cipher attacks, and to knapsacks. Bernstein and later Minder and Sinclair improved its use of memory and list sizes. Biryukov and Khovratovich turned its memory demand into the Equihash proof of work in 2016, used by Zcash. In 2021 Benhamouda and others solved ROS in polynomial time for many sessions, which closed the gap between Wagner's attack and practice for blind signatures.

## References
