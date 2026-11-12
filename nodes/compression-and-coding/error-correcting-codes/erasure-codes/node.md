---
tag: KSMYGE
kind: concept
slug: erasure-codes
name: Erasure codes
aliases:
- erasure coding
- erasure-correcting codes
area: compression-and-coding/error-correcting-codes
level: core
summary: "Codes that rebuild data when some symbols are lost and the decoder knows which ones. An MDS code with k data symbols recovers from any k of its n symbols."
prereqs: [linear-code, minimum-distance, binary-erasure-channel]
see_also: [erasure-decoding, reed-solomon-code, singleton-bound, fountain-codes, regenerating-codes, ldpc-code, repetition-code, peeling-decoding]
sources:
  - book: isbn:9780444851932
    title: F. J. MacWilliams and N. J. A. Sloane, The Theory of Error-Correcting Codes, North-Holland, 1977
    locator: Chapter 11 (MDS codes, the equivalent conditions and the Cauchy and Vandermonde constructions)
  - url: https://www.kernel.org/pub/linux/kernel/people/hpa/raid6.pdf
    title: H. Peter Anvin, The mathematics of RAID-6, first version 20 January 2004, updated 20 December 2011
    locator: Section 1 (GF(2^8) with the polynomial 0x11D and the generator {02}) and Section 2, equations (1) to (20) (P, Q and the recovery of one or two lost disks)
  - paper: "J. Blömer, M. Kalfane, R. Karp, M. Karpinski, M. Luby and D. Zuckerman, An XOR-based erasure-resilient coding scheme, Technical Report TR-95-048, International Computer Science Institute, Berkeley, 1995"
    title: An XOR-based erasure-resilient coding scheme
    locator: The Cauchy matrix construction of an MDS code and the representation of each field element as a binary matrix, so that encoding and decoding use only XOR
  - paper: doi:10.1145/50202.50214
    title: David A. Patterson, Garth Gibson and Randy H. Katz, A case for redundant arrays of inexpensive disks (RAID), Proceedings of ACM SIGMOD 1988
    locator: The RAID levels, with level 5 as one parity block spread over all disks
  - paper: "Cheng Huang, Huseyin Simitci, Yikang Xu, Aaron Ogus, Brad Calder, Parikshit Gopalan, Jin Li and Sergey Yekhanin, Erasure coding in Windows Azure Storage, USENIX Annual Technical Conference, 2012"
    title: Erasure coding in Windows Azure Storage
    locator: The cost of repair with Reed-Solomon codes and the (12, 2, 2) local reconstruction code
---

## In plain words

Some data gets lost in a way that you can see. A disk stops working. A packet does not arrive. A server is down. You know which pieces are missing, but not what they held. An erasure code stores a few extra pieces, made from the data by fixed rules, so that the missing pieces can be rebuilt from the ones that are left.

The simplest one keeps a full copy, but that doubles the storage. A better one stores the XOR of all the data pieces as one extra piece: if any one piece is lost, the XOR of the rest gives it back. Stronger codes add more extra pieces and survive more losses. The best ones rebuild everything from any set of pieces as large as the original data.

## The idea

**Notation.** A code has length $n$ and dimension $k$ over the field $\mathrm{GF}(q)$ with $q$ elements, and $[n, k, d]_q$ means [minimum distance](/minimum-distance/) $d$. The rate is $R = k/n$ and the storage overhead is $n/k$. Vectors are rows. A [linear code](/linear-code/) has a [generator matrix](/generator-matrix/) $G$ ($k \times n$), and the codeword of the message $m$ is $c = mG$. It has a [parity-check matrix](/parity-check-matrix/) $H$ ($(n - k) \times n$) with $H c^T = 0$ for each codeword. $e$ is the number of erasures and $t$ the number of errors.

**Erasures are easier than errors.** An *erasure* is a symbol that the decoder knows to be missing, and an *error* is a wrong symbol in an unknown place. A code with minimum distance $d$ can correct each pattern of $e \le d - 1$ erasures. If two codewords agreed on all $n - e$ positions that are left, they would differ in at most $e < d$ positions, so they are equal. For errors the limit is $t \le \lfloor (d-1)/2 \rfloor$. Both at once work when $2t + e < d$. So an erasure costs half as much redundancy as an error.

**Recovery is linear algebra.** Let $S$ be the set of positions that are left. The decoder knows $c_S = m G_S$, where $G_S$ is the set of columns of $G$ in $S$. It finds $m$ if and only if $G_S$ has rank $k$. In terms of $H$: the erased symbols are found if and only if the columns of $H$ at the erased positions are linearly independent. The [erasure decoding](/erasure-decoding/) page proves this and gives the algorithms.

**MDS codes.** The [Singleton bound](/singleton-bound/) says $d \le n - k + 1$. A code with $d = n - k + 1$ is *maximum distance separable* (MDS). These conditions are equivalent for a linear code (MacWilliams and Sloane, Chapter 11):

- the code is MDS;
- each $k$ columns of $G$ are linearly independent, so the data comes back from any $k$ of the $n$ symbols;
- each $n - k$ columns of $H$ are linearly independent, so any $n - k$ erasures are correctable.

An MDS code makes the best possible use of its redundancy: $n - k$ extra symbols protect against any $n - k$ losses. [Reed-Solomon codes](/reed-solomon-code/) are MDS for each $k \le n \le q$. Over $\mathrm{GF}(2)$ the only MDS codes are the trivial ones: the [repetition code](/repetition-code/) $[n, 1, n]$, the single parity check code $[n, n-1, 2]$ and the full space. So practical MDS codes use symbols of 8 bits or more.

**Cauchy matrices.** Choose distinct field elements $x_0, \ldots, x_{m-1}, y_0, \ldots, y_{k-1}$ and let $C_{ij} = 1/(x_i + y_j)$. Each square submatrix of a Cauchy matrix is invertible. So the systematic generator $G = [\, I_k \mid C^T \,]$ gives an MDS $[k + m, k]$ code: any $k$ columns of $G$, after the identity columns are removed by elimination, leave a square submatrix of $C$. Blömer, Kalfane, Karp, Karpinski, Luby and Zuckerman (1995) used this construction over $\mathrm{GF}(2^L)$ and wrote each field element as an $L \times L$ binary matrix. Then encoding and decoding use only XORs of bit vectors. This is the *Cauchy Reed-Solomon* code.

**What a code costs.** An erasure code is chosen by four numbers:

- *storage overhead* $n/k$;
- *fault tolerance*, the number of losses it always survives, at most $n - k$;
- *repair traffic*, the amount of data read to rebuild one lost symbol;
- *compute*, the field operations per byte for encoding and decoding.

Replication with three copies has overhead 3, tolerance 2, and repairs a lost copy by reading one copy. A $[14, 10]$ MDS code has overhead 1.4 and tolerance 4, but rebuilding one lost symbol reads $k = 10$ symbols. [Regenerating codes](/regenerating-codes/) lower the repair traffic at the same tolerance, and locally repairable codes lower the number of symbols read for a single loss by giving up a little tolerance.

**Codes with fast decoders.** MDS decoding solves a $k \times k$ linear system. For large $k$, sparse codes such as [LDPC codes](/ldpc-code/) and [fountain codes](/fountain-codes/) need a few percent more than $k$ symbols but decode in linear time with the [peeling decoder](/peeling-decoding/).

## Examples

**RAID 5.** Store $k$ data blocks $D_0, \ldots, D_{k-1}$ and the parity block $P = D_0 \oplus \cdots \oplus D_{k-1}$ (bytewise XOR). This is the $[k + 1, k, 2]$ single parity check code. Any one lost block is the XOR of the other $k$ blocks.

**RAID 6 (P + Q).** Anvin's description of the Linux RAID-6 code works in $\mathrm{GF}(2^8)$ built with the polynomial $x^8 + x^4 + x^3 + x^2 + 1$ (0x11D). In this field $g = \{02\}$ generates all 255 nonzero elements, and $\{02\}^8 = \{1d\}$. The two check blocks are

$$P = \bigoplus_i D_i, \qquad Q = \bigoplus_i g^i D_i.$$

With data bytes $D = (\texttt{11}, \texttt{22}, \texttt{33}, \texttt{44})$ in hexadecimal, $P = \texttt{44}$ and $Q = \texttt{83}$. Suppose that disks $x = 1$ and $y = 3$ fail. Compute $P_{xy} = \texttt{22}$ and $Q_{xy} = \texttt{dd}$ from the disks that are left, with the lost ones read as zero. Anvin's equations (17) to (20) give

$$A = g^{y-x}(g^{y-x} + 1)^{-1} = \texttt{a6}, \quad B = g^{-x}(g^{y-x} + 1)^{-1} = \texttt{dd},$$

$$D_x = A(P + P_{xy}) + B(Q + Q_{xy}) = \texttt{22}, \qquad D_y = (P + P_{xy}) + D_x = \texttt{44}.$$

The loss of one data disk and $P$ uses $D_x = (Q + Q_x)\, g^{-x}$, his equation (5). The code works for up to 255 data disks, because $g^{y-x} + 1 \ne 0$ needs $y - x \not\equiv 0 \pmod{255}$. Anvin notes that this field is not the one of AES, which uses the polynomial 0x11B.

**Cauchy Reed-Solomon, $k = 4$, $m = 3$.** With $x_i = i$, $y_j = 3 + j$ in $\mathrm{GF}(2^8)$, the $[7, 4, 4]_{256}$ code rebuilds the 4 data blocks from each of the $\binom{7}{4} = 35$ sets of 4 blocks. The tests check all 35, and all square submatrices of the Cauchy matrix.

**A code that is not MDS.** The [Hamming code](/hamming-code/) $[7, 4, 3]_2$ corrects every pattern of 2 erasures. It also corrects 28 of the 35 patterns of 3 erasures: the 7 patterns that fail are the supports of the codewords of weight 3. An MDS code of the same length and dimension would correct all 35, but no binary one exists.

## Where it is used

- **Disk arrays.** RAID 5 and RAID 6 (Patterson, Gibson and Katz 1988 described the RAID levels). Linux md RAID-6 uses the P + Q code above.
- **Distributed storage.** Large storage systems keep cold data with Reed-Solomon or locally repairable codes in place of three copies. Windows Azure Storage uses a $(12, 2, 2)$ local reconstruction code: 12 data fragments in two groups of 6, one local parity per group, and 2 global parities (Huang et al. 2012).
- **Packet networks.** Lost packets are erasures, because each packet has a number and a checksum. Fountain codes such as [LT codes](/lt-codes/) and [Raptor codes](/raptor-codes/) are used for broadcast and file delivery.
- **Inside other decoders.** A [concatenated code](/concatenated-codes/) or a product code can mark an inner block it cannot decode as an erasure, so that the outer code spends half the redundancy on it.
- **Coded computation and secret sharing.** Shamir's secret sharing is a Reed-Solomon code in which any $k$ shares rebuild the secret, the same MDS property.

## References

- F. J. MacWilliams and N. J. A. Sloane, The Theory of Error-Correcting Codes, North-Holland, 1977, Chapter 11.
- H. Peter Anvin, "The mathematics of RAID-6", 2004, updated 2011.
- J. Blömer, M. Kalfane, R. Karp, M. Karpinski, M. Luby and D. Zuckerman, "An XOR-based erasure-resilient coding scheme", ICSI Technical Report TR-95-048, 1995.
- D. A. Patterson, G. Gibson and R. H. Katz, "A case for redundant arrays of inexpensive disks (RAID)", SIGMOD 1988.
- C. Huang et al., "Erasure coding in Windows Azure Storage", USENIX ATC 2012.
