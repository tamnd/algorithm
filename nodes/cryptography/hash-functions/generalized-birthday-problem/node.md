---
tag: 26NYPE
kind: problem
slug: generalized-birthday-problem
name: Generalized birthday problem
aliases:
- k-XOR problem
- k-list problem
area: cryptography/hash-functions
level: advanced
summary: Given k lists of random n-bit strings, pick one from each so that all k XOR to zero. Solutions exist once the lists have 2^(n/k) entries; finding one takes more time.
history:
  year: 2002
  people: [David Wagner]
  note: Wagner stated the k-list problem in general and gave the tree algorithm at CRYPTO 2002; Camion and Patarin (1991) and Blum, Kalai and Wasserman (2000) had used the same idea.
prereqs: [birthday-attack]
see_also: [wagners-algorithm, collision-finding, k-sum, 3sum, subset-sum-problem, bkw-algorithm, learning-parity-with-noise, blind-signature]
sources:
  - paper: "David Wagner, A generalized birthday problem, CRYPTO 2002, LNCS 2442, pages 288 to 304"
    locator: Section 2 (the k-list problem), Section 3 (the tree algorithm, k = 4 in 2^(n/3) and k = 2^l in 2^(n/(1+l))), and Section 4 (applications)
  - paper: doi:10.1145/792538.792543
    title: "Avrim Blum, Adam Kalai and Hal Wasserman, Noise-tolerant learning, the parity problem, and the statistical query model, Journal of the ACM 50(4), 2003, pages 506 to 519"
    locator: the BKW algorithm for learning parity with noise, which cancels bits in stages in the same way
  - paper: "Paul Camion and Jacques Patarin, The knapsack hash function proposed at Crypto'89 can be broken, EUROCRYPT 1991, LNCS 547, pages 39 to 53"
    locator: an early use of the merge-in-stages idea against a knapsack hash
  - paper: "Lorenz Minder and Alistair Sinclair, The extended k-tree algorithm, SODA 2009, pages 586 to 595"
    locator: the algorithm and its analysis when the lists are smaller than Wagner needs
  - paper: "Itai Dinur, An algorithmic framework for the generalized birthday problem, Designs, Codes and Cryptography 87, 2019, pages 1897 to 1926"
    locator: time-memory tradeoffs for the k-XOR problem with less memory than the tree algorithm
  - paper: "Alex Biryukov and Dmitry Khovratovich, Equihash: asymmetric proof-of-work based on the generalized birthday problem, NDSS 2016"
    locator: the proof of work that asks for 2^k values of one list with XOR zero
  - paper: "Fabrice Benhamouda, Tancrede Lepoint, Julian Loss, Michele Orru and Mariana Raykova, On the (in)security of ROS, EUROCRYPT 2021, LNCS 12696, pages 33 to 53"
    locator: the ROS problem behind blind Schnorr signatures, solved by Wagner's method for many parallel sessions and in polynomial time for more
---

The generalized birthday problem, also called the $k$-list or $k$-XOR problem, asks for one element from each of $k$ lists of $n$-bit strings such that the $k$ elements XOR to zero. For $k = 2$ it is the usual collision search of the [birthday attack](/birthday-attack/). Wagner stated the general form in 2002. This page is about the problem itself: when solutions exist, what is known about its cost, and where it shows up. The tree algorithm that solves it for $k = 2^\ell$ in time and memory about $2^{n/(1+\ell)}$ has its own page, [Wagner's algorithm](/wagners-algorithm/). For $k \ge 4$ the problem is much easier than the birthday bound $2^{n/2}$, which has broken knapsack hashes, incremental hashes and blind signatures.

## In plain words

You have several long lists of random numbers written in binary. You must take one number from each list so that, bit by bit, each column holds an even number of ones.

With two lists, you just need the same number in both, which is the birthday problem. With four or more lists, there are many more ways to choose, so a good choice is easier to find.

The question is how long the lists must be for a choice to exist, and how fast you can find one.

## Definition

**Input.** Lists $L_1, \ldots, L_k$ of $n$-bit strings. Usually each $L_i$ is filled with $f_i(x)$ for inputs $x$ of the solver's choice, where $f_i$ is a random function or a hash, so the solver also picks the list sizes.

**Output.** Elements $x_1 \in L_1, \ldots, x_k \in L_k$ with $x_1 \oplus x_2 \oplus \cdots \oplus x_k = 0$.

**Existence.** Each choice of one element per list has XOR zero with probability $2^{-n}$. So the expected number of solutions is $|L_1| \cdots |L_k| / 2^n$. A solution is likely only when the product is at least $2^n$, for example when every list has $2^{n/k}$ entries. This is the information-theoretic limit for query cost: a solver with fewer values in total cannot expect a solution.

**Cost.** The time and memory to output a solution, with the lists given or with $f_i$ as an oracle. The gap between the list sizes for which solutions exist and the time needed to find one is what makes the problem interesting.

## Variants

- **Other groups.** Replace XOR with addition modulo $2^n$ or modulo any $m$. The tree algorithm adapts, and the bounds are the same up to small factors.
- **One list.** Find $k$ distinct elements of one list with XOR zero. Equihash asks for this, with extra rules on the order of the indices.
- **Worst-case inputs.** With integers and adversarial lists, the problem is [$k$-SUM](/k-sum/) of fine-grained complexity, and [3SUM](/3sum/) is its best-known case. The random version on this page is far easier for $k \ge 4$.
- **Subset sum.** Choose any subset of one list with a given sum. A random [subset sum](/subset-sum-problem/) of density near 1 can be split into a $k$-list problem.
- **Parity with noise.** In the [learning parity with noise](/learning-parity-with-noise/) problem, XORs of samples cancel all but one bit of the secret. The [BKW algorithm](/bkw-algorithm/) is a $k$-list merge on the samples.
- **3-XOR.** For $k = 3$ the tree method gives nothing, and the best known algorithms only gain small factors over $2^{n/2}$, with lists of size $2^{n/3}$ that are too short for the birthday method.

## Examples

**Four lists of 30 bits.** With $n = 30$ and four lists of $L = 2^{11}$ random values, the expected number of solutions is $L^4/2^{30} = 2^{14} = 16384$. Wagner's algorithm with $\ell = 10$ merges $L_1$ with $L_2$ and $L_3$ with $L_4$ on the low 10 bits, giving lists of 4117 and 4070 entries (expected 4096), and then matches the remaining 20 bits. It outputs 10 solutions, against an expected $L^4/2^{n+\ell} = 16$. One of them is the tuple of values `0x380e9079`, `0x39571879`, `0x2a23a019`, `0x2b7a2819`, which XOR to zero. The run is described on [Wagner's algorithm](/wagners-algorithm/).

The example shows the gap between the problem and the algorithm. More than 16000 solutions exist, but the tree algorithm finds only those whose pairs agree on the chosen 10 bits. It needs $2^{11}$ values per list, while lists of $2^{7.5}$ would already hold one solution on average.

**Two lists.** For $k = 2$, two lists of $2^{n/2}$ values contain one match on average. Here existence and search meet: sorting finds it in time $\tilde{O}(2^{n/2})$.

## Known algorithms

| $k$ | List size | Time | Memory | Method |
|---|---|---|---|---|
| 2 | $2^{n/2}$ | $2^{n/2}$ | $2^{n/2}$, or $O(1)$ with rho | birthday attack |
| 3 | $2^{n/2}$ | $2^{n/2}$, small gains known | $2^{n/2}$ | birthday on two lists, third fixed |
| 4 | $2^{n/3}$ | $2^{n/3}$ | $2^{n/3}$ | Wagner's tree with one merge level |
| $2^\ell$ | $2^{n/(1+\ell)}$ | $k \cdot 2^{n/(1+\ell)}$ | the same | Wagner's tree |
| any $k$ | $2^{n/(1+\lfloor \lg k \rfloor)}$ | the same | the same | the tree for the largest power of 2, other lists fixed |
| $2^\ell$, smaller lists | down to near $2^{n/k}$ | more than Wagner | | Minder and Sinclair, extended tree |
| $2^\ell$, small memory | | more time | less memory | Dinur's framework |

When $k$ may grow with $n$, taking $k = 2^{\sqrt{n}}$ gives time $2^{O(\sqrt{n})}$, subexponential in $n$.

## Bounds

- **Existence.** With lists of size $2^{n/k}$ a solution exists with constant probability. So no algorithm can use fewer than about $k \cdot 2^{n/k}$ queries.
- **Upper bounds.** Wagner's algorithm gives $O(k \cdot 2^{n/(1+\lfloor \lg k \rfloor)})$. For $k = 4$ that is $2^{n/3}$, against $2^{n/4}$ for the query lower bound.
- **Open gaps.** No algorithm is known that reaches the query bound $2^{n/k}$ for $k \ge 3$. For $k = 3$, no algorithm is known that beats $2^{n/2}$ by more than a factor polynomial in $n$. Lower bounds that match the tree algorithm hold only in restricted models.
- **Quantum.** Quantum search can speed up the merges of the tree algorithm, and quantum versions with smaller exponents are known. The exact exponents depend on the model of quantum memory.

## Reductions

- **From collision finding.** The case $k = 2$ is [collision finding](/collision-finding/) between two functions, a claw search.
- **More lists never make it harder.** Given $k + 1$ lists, fix one element $y$ of the last list and replace $L_1$ by $\{x \oplus y : x \in L_1\}$. A solver for $k$ lists then solves the problem for $k + 1$ lists.
- **To subset sum and knapsack.** Split the items into $k$ groups, form the list of partial sums of each group, and look for $k$ partial sums with the right total. This is how Camion and Patarin broke a knapsack hash.
- **From LPN.** Sample vectors with a noisy parity bit, and merge the samples $\ell$ times on blocks of coordinates. Each merge is one level of the tree, which gives the BKW algorithm.

## Applications

- **Incremental and additive hashes.** A hash of the form $H(x_1, \ldots, x_k) = h(1, x_1) + \cdots + h(k, x_k)$ in a group, as in the incremental hashes of Bellare and Micciancio, falls to a $k$-list attack: with many blocks, a collision or a preimage costs about $2^{n/(1+\lg k)}$, far less than $2^{n/2}$. Wagner showed that such designs, for example AdHash with addition modulo a large number, need much larger outputs than first proposed.
- **Blind signatures.** In the ROS problem behind blind Schnorr signatures, an attacker who opens $k$ sessions at once solves a $k$-list problem modulo the group order, and forges $k+1$ signatures from $k$ sessions. Wagner's method made this practical for large $k$, and Benhamouda and others (2021) gave a polynomial-time attack for $k$ above the bit length of the order.
- **Proof of work.** Equihash, used in Zcash, asks for $2^k$ values of one list that XOR to zero, a problem whose fastest known solution needs much memory, so that cheap specialized chips gain less.
- **Codes and lattices.** Decoding random linear codes and solving LPN and LWE with many samples use the same merge-in-stages idea.

## References
