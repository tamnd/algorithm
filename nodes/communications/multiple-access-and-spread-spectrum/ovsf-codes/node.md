---
tag: MV4CVC
kind: definition
slug: ovsf-codes
name: OVSF codes
aliases:
- orthogonal variable spreading factor codes
area: communications/multiple-access-and-spread-spectrum
level: core
summary: "A binary tree of Walsh codes of lengths 1, 2, 4, ... Two codes stay orthogonal at different rates exactly when neither is an ancestor of the other in the tree."
model: word-ram
prereqs: [walsh-hadamard-transform, hadamard-code, direct-sequence-spread-spectrum, processing-gain]
see_also: [code-division-multiple-access, maximal-length-sequence, gold-sequences, kasami-sequences, rake-receiver, multipath-fading]
sources:
  - paper: doi:10.1049/el:19970022
    title: F. Adachi, M. Sawahashi and K. Okawa, Tree-structured generation of orthogonal spreading codes with different lengths for forward link of DS-CDMA mobile radio, Electronics Letters 33(1), 1997
    locator: pp. 27 to 28 (the code tree and the rule for choosing codes of different lengths)
  - url: https://www.3gpp.org/DynaReport/25213.htm
    title: 3GPP TS 25.213, Spreading and modulation (FDD)
    locator: The subclauses on channelisation codes (the code tree, the numbering C_ch,SF,k and the spreading factors of the physical channels)
  - book: isbn:9780201633740
    title: Andrew J. Viterbi, CDMA, Principles of Spread Spectrum Communication, Addison-Wesley, 1995
    locator: The material on orthogonal Walsh functions in the forward link
---

OVSF codes are $\pm 1$ spreading codes of lengths $1, 2, 4, 8, \ldots$, placed on a binary tree. The codes on one level are the rows of a Sylvester [Hadamard matrix](/hadamard-code/), so codes of the same length are orthogonal. A code of length $SF$ spreads one symbol over $SF$ chips, so at a fixed chip rate a short code carries a high symbol rate and a long code carries a low one. Codes of different lengths stay orthogonal for any data if and only if neither code is an ancestor of the other in the tree. This lets a CDMA downlink give users different rates on one chip stream without interference between them. Adachi, Sawahashi and Okawa described the tree in 1997, and WCDMA (UMTS) uses it for its channelization codes.

## Definition

Let $SF$ be a power of two, the **spreading factor**, and $0 \le k < SF$. The code $C_{SF,k}$ is a vector of $SF$ values in $\{+1, -1\}$, defined by

$$C_{1,0} = (1), \qquad C_{2N,2k} = (C_{N,k}, \ C_{N,k}), \qquad C_{2N,2k+1} = (C_{N,k}, \ -C_{N,k}).$$

This is the numbering of 3GPP TS 25.213. The **parent** of $C_{SF,k}$ is $C_{SF/2, \lfloor k/2 \rfloor}$, and its two **children** are $C_{2SF, 2k}$ and $C_{2SF, 2k+1}$. A code $C_{SF_1,k_1}$ is an **ancestor** of $C_{SF_2,k_2}$ (with $SF_1 \le SF_2$) if it lies on the path from the root to $C_{SF_2,k_2}$, that is, if $\lfloor k_2 / (SF_2/SF_1) \rfloor = k_1$.

**Same length.** The codes $C_{SF,0}, \ldots, C_{SF,SF-1}$ are the rows of the Sylvester-Hadamard matrix of order $SF$, in bit-reversed order: $C_{SF,k}$ is the row with index $\mathrm{rev}(k)$, the bits of $k$ reversed. So $\langle C_{SF,i}, C_{SF,k}\rangle = SF$ if $i = k$ and $0$ otherwise.

**Different lengths.** Let $SF_1 < SF_2$. Over the time of one symbol of the long code, the short code sends $SF_2/SF_1$ symbols $d_1, d_2, \ldots$, each spread by $C_{SF_1,k_1}$. Split $C_{SF_2,k_2}$ into $SF_2/SF_1$ blocks of length $SF_1$. By the recursion, each block is $\pm C_{SF_1,a}$, where $C_{SF_1,a}$ is the ancestor of $C_{SF_2,k_2}$ at level $SF_1$. The despreader output is

$$\sum_i d_i \, \langle C_{SF_1,k_1}, \ \pm C_{SF_1,a} \rangle.$$

If $a \ne k_1$, every term is $0$ by the same-length case, and the codes are orthogonal for every choice of data. If $a = k_1$, the code $C_{SF_1,k_1}$ is an ancestor, every inner product is $\pm SF_1$, and the output depends on the data. Then the two codes interfere. So two codes can be used at the same time if and only if neither is an ancestor of the other.

```pseudo id=main
OVSF(SF, k)                  ▷ SF a power of two, 0 ≤ k < SF
L1  if SF = 1 then return (1)
L2  p ← OVSF(SF/2, ⌊k/2⌋)
L3  if k is even then return (p, p)
L4  return (p, -p)

ORTHOGONAL(SF1, k1, SF2, k2)
L5  return neither code is an ancestor of the other
```

Making $C_{SF,k}$ costs $O(SF)$ operations in the [word RAM](/word-ram/) model, and the ancestor test costs $O(1)$ word operations.

## Examples and non-examples

**The first levels.** $C_{2,0} = (1, 1)$ and $C_{2,1} = (1, -1)$. On the next level, $C_{4,0} = (1,1,1,1)$, $C_{4,1} = (1,1,-1,-1)$, $C_{4,2} = (1,-1,1,-1)$ and $C_{4,3} = (1,-1,-1,1)$. The four codes are orthogonal. The Sylvester matrix of order 4 has the rows $(1,1,1,1)$, $(1,-1,1,-1)$, $(1,1,-1,-1)$ and $(1,-1,-1,1)$; the codes are its rows $0, 2, 1, 3$.

**Two users at different rates.** User A spreads with $C_{4,0}$ and user B spreads with $C_{8,4}$, whose ancestors are $C_{4,2}$, $C_{2,1}$ and $C_{1,0}$. Neither code is an ancestor of the other. If B is sent with amplitude $3$, despreading the sum of the two chip streams with $C_{4,0}$ gives exactly $4 d_A$ for each symbol of A, and despreading with $C_{8,4}$ gives exactly $24 d_B$ for each symbol of B. Neither user sees the other.

**Non-example: a code and its descendant.** $C_{2,0} = (1,1)$ and $C_{4,1} = (1,1,-1,-1)$ have inner product $0$ over one long symbol when the two short symbols are equal, but not when they differ: for short symbols $(1, -1)$ the despreader of $C_{4,1}$ gives $2 + 2 = 4$. The codes are not orthogonal for all data, because $C_{2,0}$ is the parent of $C_{4,1}$.

**Code blocking.** Suppose $C_{4,1}$ and $C_{4,2}$ are in use. Half of the tree capacity is free, since $1/4 + 1/4 = 1/2$, but no code of spreading factor $2$ can be given: $C_{2,0}$ is the parent of $C_{4,1}$ and $C_{2,1}$ is the parent of $C_{4,2}$. If $C_{4,0}$ and $C_{4,1}$ are in use instead, $C_{2,1}$ is free. A set of codes can be given without conflict whenever $\sum 1/SF \le 1$: assign the requests in order of increasing spreading factor, each to the leftmost free code. When codes come and go in any order, the tree can block, and a system must then move some users to other codes.

**WCDMA.** The chip rate is $3.84$ Mchip/s. The uplink data channel uses spreading factors from $4$ to $256$, which gives $960$ down to $15$ ksymbol/s, and the downlink goes up to spreading factor $512$, or $7.5$ ksymbol/s. The downlink common pilot channel uses $C_{256,0}$.

**Non-example: without synchronization.** OVSF codes are orthogonal only when the chip streams are aligned. A delayed copy of a code, for example from a second multipath, is in general not orthogonal to the other codes. The periodic cross-correlation $\sum_i C_{4,1}[i] \, C_{4,3}[(i+1) \bmod 4]$ at a shift of one chip is $-4$, as large in magnitude as the peak. This is why WCDMA also multiplies the chips by a long scrambling code and uses a [rake receiver](/rake-receiver/), and why multipath reduces the orthogonality of the downlink.

## Related definitions

- The [Walsh-Hadamard transform](/walsh-hadamard-transform/) correlates a block of chips with all codes of one level at once, in $O(SF \log SF)$ operations.
- The rows of a Sylvester-Hadamard matrix are the codewords of the first-order Reed-Muller code, up to sign; see [Hadamard code](/hadamard-code/).
- IS-95 uses fixed-length Walsh codes of length $64$ in the forward link. OVSF codes extend this to several lengths in one tree.
- Sequence families such as [Gold sequences](/gold-sequences/) and [Kasami sequences](/kasami-sequences/) keep low correlation at every shift, which OVSF codes do not. They suit asynchronous links, while OVSF codes suit synchronous ones.

## References
