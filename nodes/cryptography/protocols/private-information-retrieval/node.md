---
tag: Q7ZEPD
kind: problem
slug: private-information-retrieval
name: Private information retrieval
aliases:
- PIR
area: cryptography/protocols
level: advanced
summary: A client reads bit i of an n-bit database held by one or more servers, and no server learns i. One server needs n bits for perfect privacy; replication or cryptography costs much less.
history:
  year: 1995
  people: [Benny Chor, Oded Goldreich, Eyal Kushilevitz, Madhu Sudan]
  note: Chor, Goldreich, Kushilevitz and Sudan defined PIR at FOCS 1995 with replicated servers. Kushilevitz and Ostrovsky gave the first single-server scheme in 1997.
prereqs: [goldwasser-micali-cryptosystem, quadratic-residuosity-problem]
see_also: [private-set-intersection, oblivious-transfer, communication-complexity, homomorphic-encryption, learning-with-errors, secure-multiparty-computation, jacobi-symbol, paillier-cryptosystem]
sources:
  - paper: doi:10.1145/293347.293350
    title: "Benny Chor, Oded Goldreich, Eyal Kushilevitz and Madhu Sudan, Private information retrieval, Journal of the ACM 45(6), 1998, pages 965 to 981 (FOCS 1995, pages 41 to 50)"
    locator: the definition, the lower bound of n bits for one server, the 2 to the d server cube schemes, and the 2-server scheme with O(n to the 1/3) bits
  - paper: "Eyal Kushilevitz and Rafail Ostrovsky, Replication is not needed, single database, computationally-private information retrieval, FOCS 1997, pages 364 to 373"
    locator: the single-server scheme from quadratic residuosity, with O(sqrt n) numbers and its recursive form with O(n to the epsilon)
  - paper: "Christian Cachin, Silvio Micali and Markus Stadler, Computationally private information retrieval with polylogarithmic communication, EUROCRYPT 1999, LNCS 1592, pages 402 to 414"
    locator: single-server PIR with polylogarithmic communication under the phi-hiding assumption
  - paper: "Amos Beimel, Yuval Ishai and Tal Malkin, Reducing the servers computation in private information retrieval, PIR with preprocessing, CRYPTO 2000, LNCS 1880, pages 55 to 73"
    locator: the bound that without preprocessing the servers must read the whole database
  - paper: "Sebastian Angel, Hao Chen, Kim Laine and Srinath Setty, PIR with compressed queries and amortized query processing, IEEE Symposium on Security and Privacy 2018, pages 962 to 979"
    locator: SealPIR, single-server PIR with lattice-based homomorphic encryption and query compression
  - paper: "Alexandra Henzinger, Matthew M. Hong, Henry Corrigan-Gibbs, Sarah Meiklejohn and Vinod Vaikuntanathan, One server for the price of two, simple and fast single-server private information retrieval, USENIX Security 2023"
    locator: SimplePIR and DoublePIR, LWE-based PIR with a database-dependent hint
  - paper: "Zeev Dvir and Sivakanth Gopi, 2-server PIR with sub-polynomial communication, STOC 2015, pages 577 to 584"
    locator: the 2-server scheme with communication n to the O(sqrt(log log n / log n))
  - paper: "Giovanni Di Crescenzo, Tal Malkin and Rafail Ostrovsky, Single database private information retrieval implies oblivious transfer, EUROCRYPT 2000, LNCS 1807, pages 122 to 138"
    locator: the reduction from oblivious transfer to single-server PIR with less than n bits
---

In private information retrieval (PIR), a server holds a database $x = x_1 \cdots x_n$ of bits, and a client wants $x_i$ without the server learning anything about $i$. The trivial solution is for the server to send all of $x$. Chor, Goldreich, Kushilevitz and Sudan (1995) defined the problem and proved that with one server and information-theoretic privacy the trivial solution is optimal: $n$ bits are needed. With two or more servers that hold copies of the database and do not talk to each other, much less is enough, with no assumption at all. Kushilevitz and Ostrovsky (1997) showed that with a computational assumption a single server suffices. Modern single-server PIR uses lattice-based [homomorphic encryption](/homomorphic-encryption/) and is fast enough for real databases of gigabytes. Unlike [oblivious transfer](/oblivious-transfer/), plain PIR protects only the client: the client may learn more of the database than $x_i$.

**Notation.** $n$ is the size of the database in bits, $i \in \{1, \ldots, n\}$ the index the client wants, and $k$ the number of servers. For a set $S \subseteq [n]$ and an index $j$, $S \oplus j$ is $S$ with $j$ added if it is absent and removed if it is present. $\lambda$ is the bit length of a modulus or ciphertext in the computational schemes.

## In plain words

You want one page from a library, but you do not want the librarian to know which page. You could borrow the whole library, but that is a lot to carry.

Suppose there are two librarians with the same books who never talk to each other. You give the first a random list of page numbers and ask for all those pages mixed together into one page (with XOR). You give the second the same list, with your page added or removed. Each librarian sees only a random-looking list. Mix the two answers, and every page cancels except yours.

With a single librarian, there is no way around taking all the pages unless you use cryptography. Then you send a locked question that the librarian can answer without opening it, and only you can open the answer.

## Definition

**$k$-server PIR.** Each of $k$ servers holds $x \in \{0,1\}^n$. A scheme has three algorithms. The client's query algorithm, on input $i$ and random coins $r$, outputs queries $q_1, \ldots, q_k$. Server $j$ outputs an answer $a_j = A_j(x, q_j)$. The reconstruction algorithm outputs $R(i, r, a_1, \ldots, a_k)$.

- **Correctness.** For all $x$ and $i$, $R(i, r, a_1, \ldots, a_k) = x_i$ with probability 1.
- **Information-theoretic privacy.** For each server $j$ and all $i, i'$, the distribution of $q_j$ for $i$ is the same as for $i'$. More generally, $t$-privacy asks this for the joint view of any $t$ servers.
- **Computational privacy.** The distributions are computationally indistinguishable.

The **communication** is the total number of bits of all queries and answers, as a function of $n$. The servers do not communicate with each other. The definition extends to records of $\ell$ bits instead of single bits.

## Variants

- **Symmetric PIR (SPIR).** The client must also learn nothing about $x$ other than $x_i$. This is 1-out-of-$n$ [oblivious transfer](/oblivious-transfer/) with sublinear communication. Gertner, Ishai, Kushilevitz and Malkin (1998) gave multi-server SPIR with shared randomness among the servers.
- **$t$-private PIR.** Privacy holds against coalitions of up to $t$ servers.
- **Keyword PIR.** The client asks for the value under a key, not an index.
- **Batch PIR.** The client retrieves many records at once, at less than the cost of separate queries.
- **PIR with preprocessing, or offline and online PIR.** Servers store an encoded database, or the client downloads a hint in advance, so that the online work becomes sublinear in $n$.
- **Byzantine-robust PIR.** Some servers return wrong answers, and the client must still decode.

## Examples

**The basic 2-server scheme.** $n = 8$ and $x = 10110010$, so $x_3 = 1$. The client picks the random set $S = \{2, 5, 7\}$. It sends $S$ to server 1 and $S \oplus 3 = \{2, 3, 5, 7\}$ to server 2.

| server | query | bits of $x$ in the query | answer (XOR) |
|---|---|---|---|
| 1 | $\{2, 5, 7\}$ | $x_2 = 0$, $x_5 = 0$, $x_7 = 1$ | 1 |
| 2 | $\{2, 3, 5, 7\}$ | $x_2 = 0$, $x_3 = 1$, $x_5 = 0$, $x_7 = 1$ | 0 |

The client outputs $1 \oplus 0 = 1 = x_3$. Each query alone is a uniform random subset of $\{1, \ldots, 8\}$, whatever $i$ is: $S$ is uniform, and so is $S \oplus i$. The cost is $n$ bits up and 1 bit down for each server.

**Kushilevitz-Ostrovsky on a toy modulus.** $N = 7 \cdot 11 = 77$; both primes are $3 \bmod 4$. The database is the $2 \times 2$ matrix with rows $(1, 0)$ and $(0, 1)$, and the client wants column 2. It sends $y_1 = 71 = 15^2 \bmod 77$, a quadratic residue, and $y_2 = 73 = -4 \bmod 77$, a non-residue. Both have [Jacobi symbol](/jacobi-symbol/) $+1$, so without the factors of $N$ the server cannot tell which is which. For each row $r$ the server computes $z_r = \prod_j w_{r,j}$ with $w_{r,j} = y_j$ if $x_{r,j} = 1$ and $w_{r,j} = y_j^2$ if $x_{r,j} = 0$:

| row | bits | $z_r \bmod 77$ | residue? | bit in column 2 |
|---|---|---|---|---|
| 1 | $(1, 0)$ | $71 \cdot 73^2 \equiv 71 \cdot 16 \equiv 58$ | yes ($58 \equiv 2 \bmod 7$, $58 \equiv 3 \bmod 11$) | 0 |
| 2 | $(0, 1)$ | $71^2 \cdot 73 \equiv 36 \cdot 73 \equiv 10$ | no ($10 \equiv 3 \bmod 7$) | 1 |

The squares and the residue $y_1$ never change residuosity, so $z_r$ is a non-residue exactly when $x_{r,2} = 1$. The client, who knows $p = 7$ and $q = 11$, reads the whole column $(0, 1)$. With an $s \times t$ matrix the cost is $t$ numbers up and $s$ numbers down, $\lambda(s + t)$ bits, so $2\lambda\sqrt n$ for a square matrix.

**The code.** The page's Python file implements the cube schemes of CGKS with $2^d$ servers (the basic 2-server scheme for $d = 1$, the square scheme with 4 servers for $d = 2$, and 8 servers for $d = 3$), the balanced 2-server scheme with a $\sqrt n \times \sqrt n$ matrix, and the Kushilevitz-Ostrovsky scheme with a local [Goldwasser-Micali](/goldwasser-micali-cryptosystem/) key of two 31-bit primes. The tests retrieve every position of random databases (64, 100 and 256 bits), check the counts $2n$ up and 2 bits down for the basic scheme, $4 \cdot 2\sqrt n$ up and 4 bits down for the square scheme, $2\sqrt n$ each way for the balanced scheme, and $\lambda t$ up and $\lambda s$ down for KO, check that a server's query is uniform for two different indices, and check that every KO query number has Jacobi symbol $+1$. A cost test shows that with $\lambda = 2048$, one level of KO costs more than the trivial scheme until $n > 4\lambda^2 \approx 2^{24}$. There are no official test vectors for PIR. The code is for study only and is not constant time; the modulus gives no security. For real data, use a maintained implementation such as SealPIR or the SimplePIR code.

## Known algorithms

| scheme | servers | privacy | communication |
|---|---|---|---|
| Trivial: send $x$ | 1 | perfect | $n$ |
| CGKS basic | 2 | perfect | $2n + 2$ |
| CGKS balanced | 2 | perfect | $4\sqrt n$ |
| CGKS cube with $2^d$ servers | $2^d$ | perfect | $O(2^d d\, n^{1/d})$ |
| CGKS covering codes | 2 | perfect | $O(n^{1/3})$ |
| Dvir and Gopi (2015) | 2 | perfect | $n^{O(\sqrt{\log\log n / \log n})}$ |
| Kushilevitz and Ostrovsky (1997) | 1 | quadratic residuosity | $O(\lambda \sqrt n)$, or $O(n^\varepsilon)$ recursively |
| Cachin, Micali and Stadler (1999) | 1 | $\phi$-hiding | polylogarithmic in $n$ |
| SealPIR, SimplePIR and other lattice schemes | 1 | RLWE or LWE | small queries; see below |

**The cube schemes.** Write $n = \ell^d$ and $i = (i_1, \ldots, i_d)$. The client picks random sets $S_1, \ldots, S_d \subseteq [\ell]$. For each $\sigma \in \{0,1\}^d$ server $\sigma$ gets $S_k \oplus i_k$ in the coordinates where $\sigma_k = 1$ and $S_k$ elsewhere, and returns the XOR of $x$ over the product of its sets. A point $j \ne i$ differs from $i$ in some coordinate $k$, and its membership does not depend on $\sigma_k$, so it is counted an even number of times; $i$ is counted once. So the XOR of the $2^d$ answers is $x_i$.

**Kushilevitz and Ostrovsky.** The scheme above uses the [quadratic residuosity problem](/quadratic-residuosity-problem/): Goldwasser-Micali encryptions of 0 and 1 look alike, and the server can compute with them. Applying the same step to the $s$ answers (each $\lambda$ bits) instead of sending them gives a recursion with communication $O(n^\varepsilon)$ for every $\varepsilon > 0$.

**Lattice-based PIR.** Modern single-server PIR encrypts the query with lattice-based homomorphic encryption: the client sends an encryption of the unit vector $e_i$, and the server computes the inner product with the database. SealPIR (Angel, Chen, Laine and Setty 2018) uses ring-LWE encryption and compresses the query to a single ciphertext that the server expands. SimplePIR (Henzinger, Hong, Corrigan-Gibbs, Meiklejohn and Vaikuntanathan 2023) uses plain [LWE](/learning-with-errors/): the database is a matrix $D$, the query is $A s + e + \Delta e_i$, and the answer is $D$ times the query. The client first downloads a hint $D A$ that depends on the database but not on the query, and the server's online work is then about one pass over the database at memory speed, several gigabytes per second per core.

## Bounds

- **One server, perfect privacy: $n$ bits.** The query distribution does not depend on $i$, so some query $q$ is possible for every $i$. For that $q$, the answer must let the client recover $x_i$ for every $i$, so different databases must give different answers, and there are $2^n$ databases. So the answer has at least $n$ bits (CGKS).
- **Server work: $\Omega(n)$.** Without preprocessing, each server must read every bit of $x$ for every query; a bit it does not read cannot be the one asked for, and that leaks information (Beimel, Ishai and Malkin 2000). Preprocessing, or a hint for the client, can move this work offline.
- **Multi-server.** The best known 2-server schemes have communication $n^{o(1)}$, and the best known lower bounds for 2 servers are only a small constant times $\log n$ bits; closing this gap is open. For 3 or more servers, schemes from matching vector codes have communication $n^{o(1)}$ as well.
- **Single-server computational.** Communication can be polylogarithmic in $n$ (Cachin, Micali and Stadler 1999) or of constant rate for long records.

## Reductions

- **Single-server PIR implies OT.** Di Crescenzo, Malkin and Ostrovsky (2000) showed that a single-server PIR with less than $n$ bits of communication gives [oblivious transfer](/oblivious-transfer/). So computational single-server PIR needs a public-key style assumption.
- **From homomorphic encryption.** Any additively homomorphic encryption, such as [Paillier](/paillier-cryptosystem/) or Goldwasser-Micali, gives single-server PIR by the inner product with an encrypted unit vector, and recursion reduces the communication.
- **Locally decodable codes.** A $k$-server PIR scheme gives a locally decodable code with $k$ queries, and some codes give PIR schemes back. Lower bounds for one transfer to the other.
- **To PSI and SPIR.** Keyword PIR is close to unbalanced [private set intersection](/private-set-intersection/) with one item, and SPIR is oblivious transfer with sublinear communication.

## Applications

Private lookups in large public databases: certificate transparency logs, compromised password lists, DNS and blocklists, and the public key directories of messaging apps. Private web search and private advertising research use it to hide which item a user reads. Anonymous messaging systems use PIR so that a client can fetch its messages from a server without revealing which mailbox is its own.

## References
