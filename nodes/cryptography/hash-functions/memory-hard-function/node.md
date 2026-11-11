---
tag: BP7QJN
kind: concept
slug: memory-hard-function
name: Memory-hard function
aliases:
- memory-hard key derivation
- MHF
- sequential memory-hard function
area: cryptography/hash-functions
level: advanced
summary: A function that a computer evaluates in time n with about n memory, and that no parallel circuit evaluates with much less area times time. It makes password guessing costly on custom hardware.
prereqs: [password-hashing, random-oracle-model, pebbling-lower-bound]
see_also: [time-memory-tradeoff, red-blue-pebble-game, directed-acyclic-graph, proof-of-work, pbkdf2, bcrypt, cryptographic-hash-function, rainbow-table]
sources:
  - paper: "Colin Percival, Stronger key derivation via sequential memory-hard functions, BSDCan 2009"
    locator: Section 2 (Definition 1, memory-hard algorithm, and the cost in dollar-seconds), Section 4 (Definition 2, sequential memory-hard function)
  - paper: "Joël Alwen and Vladimir Serbinenko, High parallel complexity graphs and memory-hard functions, STOC 2015"
    locator: the parallel random oracle model, cumulative memory complexity, and the reduction from MHFs to parallel pebbling of graphs
  - paper: "Joël Alwen and Jeremiah Blocki, Efficiently computing data-independent memory-hard functions, CRYPTO 2016, LNCS 9815"
    locator: the attack on every data-independent MHF through depth-reducible graphs, with cumulative cost O(n^2 log log n / log n)
  - paper: "Joël Alwen, Jeremiah Blocki and Krzysztof Pietrzak, Depth-robust graphs and their cumulative memory complexity, EUROCRYPT 2017, LNCS 10212"
    locator: depth-robust graphs and a data-independent MHF with cumulative memory complexity Ω(n^2 / log n)
  - paper: "Joël Alwen, Binyi Chen, Krzysztof Pietrzak, Leonid Reyzin and Stefano Tessaro, Scrypt is maximally memory-hard, EUROCRYPT 2017, LNCS 10212"
    locator: the lower bound of order n^2 times the block size on the cumulative memory complexity of scrypt in the parallel random oracle model
  - paper: "Dan Boneh, Henry Corrigan-Gibbs and Stuart Schechter, Balloon hashing, a memory-hard function providing provable protection against sequential attacks, ASIACRYPT 2016, LNCS 10031"
    locator: the Balloon construction, its data-independent access pattern, and the sequential space-time lower bound
  - url: "https://www.rfc-editor.org/rfc/rfc9106"
    title: "A. Biryukov, D. Dinu, D. Khovratovich and S. Josefsson, RFC 9106, Argon2 Memory-Hard Function for Password Hashing and Proof-of-Work Applications, September 2021"
    locator: Section 1 (memory-hard functions and the three Argon2 types), Section 7.2 (security against time-space trade-off attacks)
---

A memory-hard function (MHF) is a function that an honest computer evaluates with $n$ steps and about $n$ blocks of memory, such that any algorithm that evaluates it, even with many cores or a custom chip, must pay close to $n \cdot n$ in memory times time. Password hashing and key derivation use MHFs to make guessing expensive on GPUs and ASICs: an attacker can put thousands of small hash circuits on one chip, but not thousands of copies of a large memory. [scrypt](/scrypt/) (2009) was the first widely used MHF, and [Argon2](/argon2/) won the Password Hashing Competition in 2015.

**Notation.** $n$ is the number of sequential steps of the honest algorithm, each a call to a hash function $H$ with $w$-bit output; $S$ is memory and $T$ time. The cost measures are the area-time product $AT$ (memory times time, Percival's "dollar-seconds") and the cumulative memory complexity $\mathrm{cmc} = \sum_t |\sigma_t|$, the sum over time steps of the memory in use. The model is the parallel random oracle model (pROM): the attacker makes any number of queries to $H$ per step, and its state between steps is counted. A graph $G$ on $n$ nodes is the data dependency of the function; its pebbling cost bounds the cmc.

## In plain words

To check a password, a server runs a slow function on it. An attacker who has stolen the stored values runs the same function on billions of guesses. If the function is only slow, like many rounds of SHA-256, the attacker builds a chip with thousands of small SHA-256 units and tries thousands of guesses at once. Each unit needs almost no memory, so the chip is cheap per guess.

A memory-hard function also needs a large amount of memory, for example 64 MiB, for the whole time it runs. Memory takes area on a chip and costs money, so the attacker's cost per guess grows with memory times time. The aim is that no clever trick gets the result with much less memory without paying in much more time. Then the attacker's advantage over a normal computer stays small.

## The idea

**Memory-hard and sequential memory-hard.** Percival (2009) called an algorithm memory-hard if it uses $S(n)$ space and $T(n)$ operations with $S(n) = \Omega(T(n)^{1 - \epsilon})$, so it uses almost as much memory as it can touch. A function is sequential memory-hard if it has such an algorithm and no parallel machine with $S^{*}$ processors and $S^{*}$ space computes it in time $T^{*}$ with $S^{*} T^{*} = O(T(n)^{2 - x})$ for any $x > 0$. The honest cost is about $n^2$ in area times time, and the attacker cannot get much below it.

**Cumulative memory complexity.** The $AT$ measure lets an attacker amortize: it can share one large memory between several guesses whose memory peaks come at different times. Alwen and Serbinenko (STOC 2015) therefore measure the sum of memory over all steps, the cmc, in the pROM, and they ask for the cmc of evaluating many instances. They show that for an MHF defined by a graph (each node is $H$ of its parents), the cmc is at least $w$ times the parallel cumulative pebbling cost of the graph, up to small error terms. So questions about MHFs become questions about pebble games on directed acyclic graphs: a pebble on a node is a value in memory, a node can get a pebble only when all its parents have one, and the cost is the number of pebbles summed over time. The best possible is $\Theta(n^2)$ for a graph on $n$ nodes with constant in-degree.

**Data-independent and data-dependent.** In a data-independent MHF (iMHF), the memory addresses that the function reads do not depend on the password. Examples are Argon2i, Balloon hashing and Catena. An attacker who watches cache timing learns nothing about the password. In a data-dependent MHF (dMHF), the addresses depend on values computed from the password, as in scrypt and Argon2d. Then the graph is not known in advance, which makes tradeoffs harder for the attacker, but the access pattern can leak through side channels. Argon2id runs the first half of its first pass data-independently and the rest data-dependently.

**What is proved.**

| function or class | type | best known cmc lower bound | best known attack |
|---|---|---|---|
| any graph with constant in-degree | iMHF | none in general | $O(n^2 \log \log n / \log n)$ (Alwen and Blocki, 2016) |
| depth-robust graph constructions | iMHF | $\Omega(n^2 / \log n)$ (Alwen, Blocki and Pietrzak, 2017) | matches up to a $\log \log n$ factor |
| scrypt | dMHF | $\Omega(n^2 w)$ (Alwen, Chen, Pietrzak, Reyzin and Tessaro, 2017) | the naive algorithm, so the bound is tight |
| Balloon hashing | iMHF | a space-time bound against sequential attackers (Boneh, Corrigan-Gibbs and Schechter, 2016) | the general attack of Alwen and Blocki on every iMHF |

So no iMHF can reach the full $n^2$, while scrypt does reach it in the pROM. The bounds hold in an idealized model where $H$ is a random oracle; they say nothing about attacks that use the structure of the real $H$.

**Related notions.** Bandwidth-hard functions bound the memory traffic, not the memory size, because traffic is what costs energy on a chip. Memory-hard [proof-of-work](/proof-of-work/) puzzles, such as Equihash, need memory to solve a puzzle but little to check a solution. A [time-memory trade-off](/time-memory-tradeoff/) attack is the generic way to compute an MHF with less memory and more time; a good MHF makes every such trade-off lose in area times time.

## Examples

**Why iterated hashing is not memory-hard.** PBKDF2 with $c$ iterations computes $u_i = H(u_{i-1})$. The graph is a path, which a single pebble walks from start to end, so the cmc is $c$ blocks times 1 pebble: about $c$, not $c^2$. An attacker's chip needs only one hash unit and one register per guess.

**scrypt's ROMix.** Fill $V_0, \ldots, V_{N-1}$ with $V_i = H(V_{i-1})$, then do $N$ steps $X \gets H(X \oplus V_j)$ with $j$ taken from $X$. An attacker that keeps only every $k$-th $V_i$ must recompute each needed $V_j$ from the nearest stored one, about $k/2$ hashes on average. So the memory drops by a factor $k$ and the second phase grows by a factor of about $k/2$, and the area-time product does not drop. With $N = 16$ and $k = 4$, the scrypt page of this site counts 61 calls to BlockMix instead of 32, for a quarter of the memory.

**Argon2 and depth-robust graphs.** Argon2i fills a matrix of 1 KiB blocks, each the compression of the previous block and a reference block chosen by a pseudorandom sequence that does not depend on the password. The resulting graph is not depth-robust enough to resist the Alwen and Blocki attack fully, which lowers the cmc of Argon2i below $n^2$ for large $n$. This is one reason RFC 9106 recommends Argon2id, which uses the data-dependent mode after its first half pass.

## Where it is used

- **Password hashing**: Argon2id and scrypt are the methods recommended first by OWASP; see [password hashing](/password-hashing/).
- **Key derivation from passwords**: disk encryption (LUKS2 supports Argon2), password managers, and wallet files.
- **Proof of work**: scrypt in Litecoin, and memory-hard puzzles such as Equihash, to reduce the advantage of ASICs.
- **Theory**: graph pebbling, depth-robust graphs and the pROM grew into a research area through the study of MHFs.

## References
