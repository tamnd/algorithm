---
tag: 417CHM
kind: algorithm
slug: hyperloglog-plus-plus
name: HyperLogLog++
aliases:
- HLL++
- HyperLogLog in practice
- HyperLogLogPlusPlus
area: online-and-streaming/streaming-sketches
level: advanced
summary: Improves HyperLogLog with sparse representation and bias correction for small cardinalities.
solves: [distinct-elements-problem]
model: word-ram
complexity:
  vars: {m: the number of registers, n: the universe size}
  time: {worst: O(m), average: O(1)}
  space: {extra: O(m log log n)}
properties: {online: true, deterministic: false, mergeable: true}
history:
  year: 2013
  people: [Stefan Heule, Marc Nunkesser, Alexander Hall]
  note: Heule, Nunkesser and Hall of Google described HyperLogLog++ at EDBT 2013, as the form of HyperLogLog used in their production systems.
prereqs: [hyperloglog, linear-counting, k-nearest-neighbors]
see_also: [hyperloglog, loglog-counting, linear-counting, kmv-sketch, pcsa, mergeable-summaries, cardinality-estimation, distinct-elements-problem]
sources:
  - paper: doi:10.1145/2452376.2452456
    title: Stefan Heule, Marc Nunkesser and Alexander Hall, HyperLogLog in practice, algorithmic engineering of a state of the art cardinality estimation algorithm, EDBT 2013
    locator: pp. 683 to 692 (Section 5, the three changes; Figures 6 and 7, the algorithm)
  - paper: doi:10.46298/dmtcs.3545
    title: Philippe Flajolet, Éric Fusy, Olivier Gandouet and Frédéric Meunier, HyperLogLog, the analysis of a near-optimal cardinality estimation algorithm, AofA 2007
    locator: Theorem 1; Figure 3; Section 4
  - paper: doi:10.1145/78922.78925
    title: Kyu-Young Whang, Brad T. Vander-Zanden and Howard M. Taylor, A linear-time probabilistic counting algorithm for database applications, ACM Transactions on Database Systems 15(2), 1990
    locator: pp. 208 to 229
---

HyperLogLog++ is the engineered form of [HyperLogLog](/hyperloglog/) that Heule, Nunkesser and Hall (2013) built at Google. It makes three changes. It uses a 64-bit hash, so hash collisions do not matter for any practical count and the large range correction goes away; the registers then need 6 bits. It corrects the bias of the raw estimate for counts up to $5m$ with a table of measured biases, read by $k$-nearest neighbour interpolation. And it starts with a sparse representation: while there are few distinct items it stores only the pairs (index, value) for a much finer precision $p' = 25$, which is nearly exact, and it switches to the $m$ dense registers when the sparse form would take more memory. The dense part, the merge and the $1.04/\sqrt m$ error for large counts are those of HyperLogLog. The bias tables and the switch thresholds are empirical. On this page $m = 2^p$ is the number of dense registers, $m' = 2^{p'}$ is the sparse precision, $d$ is the number of distinct items, $n$ is the universe size, and the stream is in the [cash register model](/cash-register-model/).

## In plain words

HyperLogLog is very good for large counts, but it has two practical weak spots. For small counts its raw estimate is off, and the fix of the original paper leaves a jump in the error. And its full set of registers costs the same memory whether the count is ten or ten million, which hurts when you keep millions of sketches and most of them are small. HyperLogLog++ measures the error of the raw estimate in advance, by simulation, and subtracts it. For small sketches it keeps a short list of the few registers that are in use, at a much finer resolution, which gives an almost exact count. When the list grows past the size of the full set of registers, it changes to the full form, with no loss.

## The problem

The input is a stream of items from a universe of size $n$, with repeats. The output is an estimate of the number $d$ of distinct items, accurate over the whole range from very small to very large $d$, with small memory for small $d$. This is the [distinct elements problem](/distinct-elements-problem/) as it appears in [cardinality estimation](/cardinality-estimation/) for databases.

## The algorithm

Let $h$ map items to 64-bit integers, and let $p \in \{4, \ldots, 18\}$ and $p' = 25$. For a hash value $y$, the dense pair is $(\mathrm{idx}, \rho)$ with $\mathrm{idx}$ the first $p$ bits and $\rho$ the position of the leftmost 1 in the other $64 - p$ bits. The sparse pair is $(\mathrm{idx}', \rho')$ with $\mathrm{idx}'$ the first $p'$ bits and $\rho'$ the position of the leftmost 1 in the other $64 - p'$ bits. Positions count from 1, and $\rho(0)$ is the number of bits plus 1.

```pseudo id=main
HLL++(σ, h, p)
L1  S ← empty map from idx′ to ρ′;  sparse ← true
L2  for each item x of σ do
L3      y ← h(x)
L4      if sparse then S[idx′(y)] ← max(S[idx′(y)], ρ′(y))
L5          if the size of S exceeds 6m bits then convert S to M[0..m−1]; sparse ← false
L6      else M[idx(y)] ← max(M[idx(y)], ρ(y))
L7  if sparse then return m′ ln(m′ / (m′ − |S|))            ▷ linear counting at precision p′
L8  E ← α_m m² / Σ_j 2^(−M[j]);  if E ≤ 5m then E′ ← E − BIAS_p(E) else E′ ← E
L9  V ← the number of j with M[j] = 0;  if V ≠ 0 then H ← m ln(m/V) else H ← E′
L10 if H ≤ THRESHOLD_p then return H else return E′
```

**Conversion of line L5.** A sparse pair decodes to the dense pair of the same hash value. Let $s = p' - p$ and let $\ell$ be the last $s$ bits of $\mathrm{idx}'$. Then $\mathrm{idx} = \lfloor \mathrm{idx}'/2^s \rfloor$, and $\rho = s - \mathrm{bitlen}(\ell) + 1$ if $\ell \ne 0$, else $\rho = s + \rho'$. Each register of the dense form is the maximum of the decoded values of its sparse pairs.

**The bias table of line L8.** For each $p$, the authors ran HyperLogLog on 5000 random data sets at each of about 200 values of $d$ up to $5m$, and stored the mean raw estimate and its mean bias at each value. $\mathrm{BIAS}_p(E)$ is the mean bias of the 6 stored points whose raw estimates are nearest to $E$.

**The threshold of line L10.** For each $p$, the count below which linear counting on the dense registers is more accurate than the bias corrected estimate. It was found by simulation; for $p = 14$ it is 11500, and the values for other $p$ are in an appendix of the paper published online.

**The sparse encoding.** The paper stores the sparse pairs as sorted integers, with $\rho'$ only when $\ell = 0$, as differences in a variable length code, and with a small unsorted buffer for new pairs that is merged in from time to time. At $p = 14$ an entry then takes about 8.12 bits on average. Line L5 compares the encoded size with the $6m$ bits of the dense form.

## Example

Let $p = 4$, so $m = 16$ and $s = 21$. Take two items with these hash values.

- Item $a$: $\mathrm{idx} = 3$, the next 21 bits are $\ell = 2^{18}$, so $\mathrm{idx}' = 3 \cdot 2^{21} + 2^{18} = 6553600$.
- Item $b$: $\mathrm{idx} = 7$, the next 21 bits are 0, so $\mathrm{idx}' = 7 \cdot 2^{21} = 14680064$, and the last 39 bits are $2^{36}$, so $\rho' = 39 - 37 + 1 = 3$.

The stream $a, b, a, b$ leaves 2 entries in $S$. Line L7 returns $2^{25}\ln(2^{25}/(2^{25} - 2)) \approx 2.00000006$, against $d = 2$. If the sketch converts, $a$ decodes to register 3 with $\rho = 21 - 19 + 1 = 3$, since $\ell = 2^{18}$ has bit length 19, and $b$ decodes to register 7 with $\rho = 21 + 3 = 24$. These are the dense pairs of the two hash values: the 60 bits after the index of $a$ start with two zeros and a 1, and those of $b$ start with 21 zeros, then 2 more, then a 1. With 32 bits per entry and no encoding, the switch of line L5 happens at the fourth entry, since $6m = 96 < 4 \cdot 32$.

## Correctness

The proof page proves two facts in full. First, the sparse form loses nothing: the conversion of line L5 gives exactly the registers that the dense update of line L6 would have built from the same stream, at any time, so the switch does not change any later answer of lines L8 to L10. Second, merges are exact in every mode: two sparse sketches merge by the maximum per key, a sparse and a dense sketch merge by converting and then taking the maximum per register, and the result is the sketch of the union. The sparse estimate of line L7 is the [linear counting](/linear-counting/) estimate with $m' = 2^{25}$ bits, whose bias and variance are proved on that page; for $d \ll m'$ its relative standard error is about $1/\sqrt{2m'} \approx 1.2 \cdot 10^{-4}$.

The dense raw estimate of line L8 is the HyperLogLog estimate, and its asymptotic error for large $d$ is the cited result of Flajolet, Fusy, Gandouet and Meunier for an ideal hash. The bias table, the range $E \le 5m$ for the correction, and the thresholds of line L10 are empirical; there is no proof that the corrected estimate is better at every $d$, only the measurements of the paper.

## Complexity

- **Update time.** $O(1)$ in dense mode. In sparse mode $O(1)$ expected with a hash map; with the sorted, encoded list of the paper, $O(1)$ amortized into the buffer and $O(|S|)$ for each merge of the buffer. The conversion of line L5 happens once and costs $O(m + |S|)$, which is the worst case of an update.
- **Query time.** $O(1)$ in sparse mode, if $|S|$ is kept. $O(m)$ in dense mode for the sum of line L8 and the count $V$, plus $O(\log K)$ or $O(K)$ for the bias lookup in a table of $K \approx 200$ points.
- **Space.** Dense: $6m$ bits, since $\rho \le 64 - p + 1 \le 61$. Sparse: at most $6m$ bits by line L5. The bias tables and thresholds are constants of the code, shared by all sketches. The seed of $h$ is extra.
- **Accuracy.** For large $d$, about $1.04/\sqrt m$ as for HyperLogLog (cited, ideal hash). For small $d$ in sparse mode, nearly exact (proved through linear counting). In between, the paper reports a smaller measured error than the corrections of the original HyperLogLog (empirical).

## Properties

- **Mergeable in all modes.** See the proof page and [mergeable summaries](/mergeable-summaries/).
- **Compatible with HyperLogLog.** The dense registers are HyperLogLog registers for a 64-bit hash, so the dense state can be read by any HyperLogLog estimate with 64-bit values.
- **Memory grows with the count.** Small sketches stay small, which matters when there are millions of them.
- **Duplicate-insensitive.** Both forms are functions of the set of distinct items.
- **No large range correction.** With 64-bit hash values, collisions are rare until $d$ is far beyond any count of interest.
- **No deletions.** As for HyperLogLog.

## Variants and improvements

- **Different $p'$.** A smaller $p'$ makes sparse entries shorter but the sparse estimate less exact. The paper uses $p' = 25$.
- **Without the bias table.** Later estimators that use the histogram of the register values reach a similar small range accuracy with no empirical table.
- **Without the encoding.** A plain sorted array or hash map of 32-bit entries is simpler and switches to dense earlier, at $6m/32$ entries.
- **Precision reduction.** A sketch with precision $p$ can be turned into one with a smaller precision, so sketches with different $p$ can be merged at the smaller one.
- **[HyperLogLog](/hyperloglog/).** The original, with a 32-bit hash, 5-bit registers and the threshold rule.

## When to use it

Use HyperLogLog++ when you keep many count distinct sketches and many of them are small, as in per-user, per-key or per-group counts, or when you need good accuracy across the whole range of counts. Use the dense HyperLogLog form when all counts are large. Use the [KMV sketch](/kmv-sketch/) when you need intersections or an unbiased estimate.

## Pitfalls

- **A bias table for the wrong $p$ in line L8.** The table depends on $p$ and on the 64-bit hash. A table from another precision, or from a 32-bit hash, corrects the wrong bias.
- **Correcting above $5m$ in line L8.** The table covers raw estimates up to $5m$. Above that, the correction is not defined, and the paper uses $E$ unchanged.
- **The wrong threshold in line L10.** The thresholds are empirical and depend on $p$. Using 11500 for every $p$ is wrong for small $p$. The implementation here scales 11500 by $m/2^{14}$ when no threshold is given, which is a simple default, not the table of the paper.
- **A wrong decode in line L5.** When the $s$ bits of $\ell$ are 0, the dense $\rho$ is $s + \rho'$, not $\rho'$. Forgetting the offset makes the converted registers too small.
- **Switching back.** There is no way back from line L5 to sparse; the dense form does not keep the fine indices.
- **Merging different precisions.** Two sketches with different $p$ must first be reduced to the same $p$.

## Implementations

## History

Stefan Heule, Marc Nunkesser and Alexander Hall published "HyperLogLog in practice" at EDBT 2013. They described the changes that Google made to HyperLogLog for its data analysis systems, where very many sketches are kept and most counts are small. The paper measured the bias of the original estimate, replaced the 32-bit hash, and added the sparse form. HyperLogLog++ and its descendants are the count distinct sketches of many query engines.

## References
