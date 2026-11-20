---
tag: YJEATG
kind: technique
slug: sparse-code-multiple-access
name: Sparse code multiple access
aliases:
- SCMA
area: communications/multiple-access-and-spread-spectrum
level: research
summary: Maps each user's bits to sparse multidimensional codewords and detects them jointly by message passing.
prereqs: [non-orthogonal-multiple-access, factor-graph, message-passing]
see_also: [belief-propagation, code-division-multiple-access, multiuser-detection, optimum-multiuser-detector, orthogonal-frequency-division-multiple-access, ldpc-code, max-log-demapping, superposition-coding]
sources:
  - paper: doi:10.1109/PIMRC.2013.6666156
    title: Hosein Nikopour and Hadi Baligh, Sparse code multiple access, IEEE 24th International Symposium on Personal, Indoor and Mobile Radio Communications (PIMRC), London, 2013
    locator: pp. 332 to 336 (the sparse codebooks, the factor graph of users and resources, the message passing detector and the link-level results)
  - paper: doi:10.1109/TSP.2007.909320
    title: Reza Hoshyar, Ferry P. Wathan and Rahim Tafazolli, Novel low-density signature for synchronous CDMA systems over AWGN channel, IEEE Transactions on Signal Processing 56(4), 2008
    locator: pp. 1616 to 1626 (low-density spreading signatures detected by message passing, the forerunner of SCMA)
  - paper: doi:10.1109/18.910572
    title: Frank R. Kschischang, Brendan J. Frey and Hans-Andrea Loeliger, Factor graphs and the sum-product algorithm, IEEE Transactions on Information Theory 47(2), 2001
    locator: pp. 498 to 519 (the sum-product rules used by the SCMA detector, exact on trees and approximate on graphs with cycles)
---

Sparse code multiple access (SCMA) lets $K$ users share $R$ orthogonal resources, such as OFDM subcarriers, with $K > R$. Each user maps a group of its bits directly to a codeword of length $R$ from its own codebook, and every codeword of that user is zero on the same $R - D$ resources. So each user touches only $D$ resources, and each resource carries only a few users. The receiver detects all users jointly with a message passing algorithm (MPA) on the sparse bipartite graph of users and resources. SCMA was proposed by Nikopour and Baligh at Huawei in 2013. It is a code-domain form of [non-orthogonal multiple access](/non-orthogonal-multiple-access/): power-domain NOMA separates users by power and successive cancellation, while SCMA separates users by the sparse pattern and the shape of their codebooks and needs no power gap. It grew out of low-density spreading CDMA, which spreads a QAM symbol with a sparse signature; SCMA replaces the symbol and the signature with one multidimensional codeword, which adds a shaping gain.

## In plain words

There are more users than slices of the band. Each user is allowed to use only a few slices, for example 2 out of 4, and the users' choices overlap in a planned way. On each slice, only a few users add up.

Each user does not send a plain symbol on its slices. It picks one word from its own small book of words, and the word says what to send on each of its slices at once. The books of different users are shaped differently, so that their sums are easy to tell apart.

The receiver solves a puzzle. On each slice it asks: which words of the users on this slice could give this value? It passes these guesses between the slices and the users, a few times back and forth, until each user's most likely word stands out.

## When it applies

- The system must carry more users than orthogonal resources, for example many machine-type devices with small packets. SCMA supports overloads such as 150 percent.
- The receiver can run joint detection. The cost per resource grows as $M^F$ for $M$ codewords per user and $F$ users per resource, so $M$ and $F$ must be small, typically $M = 4$ and $F = 3$.
- The users' signals arrive roughly synchronized and on a known grid, as in an OFDMA uplink with timing advance, or in a downlink.
- The channel of each user on each resource is known to the receiver, from pilots.
- A power gap between the users is not available or not wanted. Unlike power-domain NOMA, SCMA works with users of similar strength.

## The template

Fix $K$ users, $R$ resources, $D$ nonzero entries per codeword, and $M$ codewords per user, so each user sends $\log_2 M$ bits per block of $R$ resources. A binary $R \times K$ **factor graph matrix** $F$ has a 1 in row $r$ and column $k$ if user $k$ uses resource $r$. Each column has $D$ ones. Each row has $d_f$ ones, the number of users that collide on a resource. Codebook $k$ is a set of $M$ complex vectors $c_k(m)$ of length $R$ that are zero outside the support of column $k$. The overload is $K / R$.

The receiver sees, on each resource $r$,

$$y_r = \sum_{k : F_{rk} = 1} h_{rk}\, c_{k,r}(m_k) + w_r, \qquad w_r \sim \mathcal{CN}(0, N_0),$$

with the channel gain $h_{rk}$ of user $k$ on resource $r$. Define the SNR as $E_s/N_0$ for the average energy $E_s$ per user codeword per resource it uses. The receiver wants the codeword index $m_k$ of every user. Brute-force joint ML searches all $M^K$ combinations. The MPA uses the sparsity: it is the sum-product algorithm of [belief propagation](/belief-propagation/) on the [factor graph](/factor-graph/) with one variable node per user and one factor node per resource.

```pseudo id=main
SCMA-MPA(y, h, codebooks, N0, iterations I)
L1  for each edge (r, k): q[k→r](m) ← 1/M for every m          ▷ uniform priors
L2  repeat I times
L3      for each resource r and each user k on r do             ▷ factor node update
L4          p[r→k](m) ← Σ over the codeword indices of the other users on r of
                exp(-|y_r - Σ_j h_rj c_{j,r}(m_j)|^2 / N0) · Π_{j≠k} q[j→r](m_j),  with m_k = m
L5      for each user k and each resource r of k do             ▷ variable node update
L6          q[k→r](m) ← normalize(Π_{r' of k, r' ≠ r} p[r'→k](m))
L7  for each user k: m̂_k ← argmax_m Π_{r of k} p[r→k](m)
L8  return m̂ (or bit LLRs from the beliefs, for a channel decoder)
```

The likelihood in line L4 is that of complex Gaussian noise of variance $N_0$, so it uses $\exp(-|e|^2/N_0)$. Line L4 sums over $M^{d_f - 1}$ combinations per message, so one iteration costs $O(R\, d_f\, M^{d_f})$ evaluations of the likelihood, against $O(M^K)$ for brute-force ML. The graph has cycles, so the MPA is an approximation of ML, not ML itself; in practice it converges in a few iterations, but no general convergence theorem holds (a heuristic). In the log domain, the max-log form replaces the sums in L4 by maximums, as [max-log demapping](/max-log-demapping/) does for one user.

## Classic examples

**The 6-user, 4-resource code.** The standard example of Nikopour and Baligh has $K = 6$, $R = 4$, $D = 2$, $M = 4$ and

$$F = \begin{pmatrix} 1 & 1 & 1 & 0 & 0 & 0 \\ 1 & 0 & 0 & 1 & 1 & 0 \\ 0 & 1 & 0 & 1 & 0 & 1 \\ 0 & 0 & 1 & 0 & 1 & 1 \end{pmatrix}.$$

Each user uses 2 of the 4 resources, and each of the $\binom{4}{2} = 6$ pairs of resources belongs to exactly one user. Each resource carries $d_f = 3$ users. The overload is $6/4 = 150$ percent. Each user sends 2 bits per block, so the block carries 12 bits on 4 resources, against 8 bits for OFDMA with one QPSK user per resource. Brute-force ML tests $4^6 = 4096$ combinations per block. The MPA computes, per iteration, $4 \times 4^3 = 256$ likelihoods (one per resource for each combination of its 3 users) and 12 outgoing messages of 4 values each. These counts follow from $F$.

**Why sparsity helps.** Two users share at most one resource in this $F$. So each pair of users interferes only on one resource, and on the other resource of each user there is a different set of users. The detector combines the evidence from the two resources of each user, which is a diversity of order $D = 2$ against fading of the resources.

**Codebook shape.** A typical design starts from a mother constellation in $D = 2$ complex dimensions, for example two rotated QPSK components, and gives each user a different rotation or phase of it on its two resources. The rotation is chosen so that the sum of the users on one resource keeps large distances. This design step is where SCMA gains over low-density spreading with plain QAM.

## Variations

- **Low-density spreading (LDS-CDMA, LDS-OFDM).** The same sparse graph, but each user repeats one QAM symbol with a sparse signature. SCMA generalizes it.
- **Max-log and list MPA.** Max-log MPA uses maximums in the log domain. Other forms keep only the most likely combinations per resource, which cuts the $M^{d_f}$ term.
- **Joint detection and decoding.** The MPA outputs bit LLRs to an [LDPC](/ldpc-code/) or turbo decoder, and the decoder's output can be fed back as priors in line L1, as in turbo receivers.
- **Grant-free SCMA.** Users send without a schedule. The receiver must also detect which codebooks are active, which links SCMA to random access; see [unsourced random access](/unsourced-random-access/).
- **Downlink SCMA.** The base station sends the sum of the users' sparse codewords, and each user runs the MPA for the users on its resources.
- **Other code-domain schemes.** Pattern division multiple access and multiuser shared access use other sparse or short codes with a joint or SIC receiver; see [multiuser detection](/multiuser-detection/).

## Pitfalls

- **Exponential cost in $d_f$.** Line L4 costs $M^{d_f}$ per resource. Doubling $d_f$ from 3 to 6 at $M = 4$ raises it from 64 to 4096. Keep $d_f$ small.
- **Cycles in the graph.** The 6-user graph has short cycles (users 1 and 2 share resource 1, users 2 and 4 share resource 3, users 4 and 1 share resource 2). MPA on a graph with cycles is not exact, and its errors can differ from ML at high SNR.
- **Channel knowledge.** The likelihoods need $h_{rk}$ for every user on every resource. Channel estimation errors enter every message.
- **Synchronization.** The model assumes that all users arrive aligned within the cyclic prefix and without carrier offset. Uplink timing errors break it, as in OFDMA.
- **Numerical underflow.** The products in L4 and L6 underflow for long blocks or high SNR. Normalize every message, or work in the log domain with log-sum-exp.
- **Comparing schemes.** Compare at the same total rate and the same receiver complexity. SCMA with MPA against OFDMA with a one-tap equalizer is not a like-for-like comparison of the access schemes alone.

## Exercises

1. Build the $4 \times 6$ matrix $F$ for $R = 4$ and $D = 2$ from the 6 pairs of resources. Show that every resource has $d_f = 3$.
2. For $R = 5$ and $D = 2$, how many users can have distinct pairs of resources, what is $d_f$, and what is the overload? (Answer: 10 users, $d_f = 4$, 200 percent.)
3. Count the likelihood evaluations per MPA iteration for the code of exercise 2 with $M = 4$, and compare with $M^K$.
4. Show that on a factor graph without cycles, the MPA beliefs after enough iterations equal the exact marginal posteriors of each user's codeword.
5. Write lines L4 and L6 in the log domain with the max-log approximation, and say which sums become maximums.

## References
