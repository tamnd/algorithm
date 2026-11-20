---
tag: 87FE21
kind: technique
slug: multilevel-coding
name: Multilevel coding
aliases:
- MLC
- Imai-Hirakawa multilevel coding
- multistage decoding
area: communications/modulation-and-detection
level: advanced
summary: Protects each bit level of a constellation with its own code and decodes the levels one after another.
prereqs: [trellis-coded-modulation, channel-capacity, signal-constellation, soft-demapping]
see_also: [trellis-coded-modulation, bit-interleaved-coded-modulation, polar-code, successive-cancellation-decoding, channel-capacity, probabilistic-constellation-shaping, ldpc-code, hamming-distance]
sources:
  - paper: doi:10.1109/TIT.1977.1055718
    title: Hideki Imai and Shuji Hirakawa, A new multilevel coding method using error-correcting codes, IEEE Transactions on Information Theory 23(3), 371-377, 1977
    locator: the multilevel construction with one code per level and the staged decoding
  - paper: doi:10.1109/18.771140
    title: Udo Wachsmann, Robert F. H. Fischer and Johannes B. Huber, Multilevel codes - theoretical concepts and practical design rules, IEEE Transactions on Information Theory 45(5), 1361-1391, 1999
    locator: the chain rule of mutual information, the capacity rule for the level rates, multistage decoding, and the comparison of labelings and design rules
---

Multilevel coding (MLC) splits the bit label of each constellation point into levels and protects each level with its own binary code. With a set-partitioning labeling, the levels see very different channels: the first bit separates points that are close, the last separates points that are far apart. So the first level gets a strong low-rate code and the last a weak high-rate code, or none. The receiver decodes the levels one after another, each with the decisions of the earlier levels. This is the multistage decoder. By the chain rule of mutual information, MLC with multistage decoding and the right level rates reaches the capacity of the constellation. Imai and Hirakawa proposed it in 1977. Wachsmann, Fischer and Huber in 1999 gave the design rules in terms of capacity.

## In plain words

The bits that pick a point are not equally safe. Some decide between neighbors that noise easily confuses; others decide between points far apart, which noise rarely mixes up. Multilevel coding gives each kind of bit the protection it needs: a lot for the weak bits, little for the strong bits. The receiver first decodes the weakest bits. Once it knows them, it knows which group of far-apart points was used, so the next bits become easy, and so on. The cost is several codes instead of one and a decoder that works in stages, where a mistake in one stage can spoil the next.

## When it applies

- The constellation has $2^m$ points with $m \ge 2$, and its labeling can be chosen. Set partitioning gives the largest differences between the levels.
- The system can use $m$ binary codes of different rates on the same block length, or a code family that has all the rates, such as [polar codes](/polar-code/) or [LDPC codes](/ldpc-code/).
- The latency of $m$ decoding stages in sequence is acceptable.
- The channel is close to AWGN. On fading channels the level capacities change with the fade, and [bit-interleaved coded modulation](/bit-interleaved-coded-modulation/) is often simpler.

## The template

1. **Label by set partitioning.** Label bit $b_0$ splits the constellation into two subsets with inner minimum distance $d_1$; bit $b_1$ splits each again ($d_2$); and so on, with $d_0 < d_1 < \cdots < d_{m-1}$. For 8-PAM with the points $-7, -5, \ldots, 7$, $b_0$ is the parity of the index of the point, and the raw distances are $2, 4, 8$.
2. **Choose the level rates.** With equally likely points, the chain rule gives
$$I(X; Y) = \sum_{i=0}^{m-1} I(B_i; Y \mid B_0, \ldots, B_{i-1}).$$
The capacity rule sets the rate of the code on level $i$ to $R_i = I(B_i; Y \mid B_0, \ldots, B_{i-1})$, the capacity of the channel that level $i$ sees when the lower levels are known. The total rate $\sum_i R_i$ is then $I(X; Y)$.
3. **Encode.** Split the information bits into $m$ streams, encode stream $i$ with a binary code $C_i$ of rate $R_i$ and length $N$, and send $N$ symbols; symbol $t$ takes bit $t$ of each codeword as its label.
4. **Decode in stages (multistage decoding).** Stage 0 computes the LLRs of $b_0$ from $y$, with the higher bits unknown, and decodes $C_0$. Stage $i$ computes the LLRs of $b_i$ with $b_0, \ldots, b_{i-1}$ fixed to the decisions of the earlier stages, so only the points of one subset of level $i$ enter the sums, and decodes $C_i$.
5. **Check the distance (for algebraic design).** If $C_i$ has minimum Hamming distance $\delta_i$, two different code sequences that first differ at level $i$ are at squared Euclidean distance at least $d_i^2\delta_i$. The minimum distance of the whole code is $\min_i d_i^2\delta_i$. The balanced distance rule chooses the codes so that these products are about equal.

## Classic examples

**8-ASK at 2 bits per dimension.** With uniform 8-ASK and set partitioning, at an SNR of $12.62$ dB, where $I(X; Y) = 2.00$ bits, numerical integration gives the level capacities $I(B_0; Y) = 0.176$, $I(B_1; Y \mid B_0) = 0.825$ and $I(B_2; Y \mid B_0, B_1) = 1.000$. So level 0 needs a code of rate about $0.18$, level 1 about $0.82$, and level 2 can stay almost uncoded. The sum is the full $2.00$ bits. For the same constellation, BICM reaches $1.985$ bits with Gray labels, but only $1.592$ with the set-partitioning labels, which shows that MLC and BICM need different labelings.

**Block-coded 8-PSK.** Take unit-energy 8-PSK with set partitioning ($d_0^2 = 0.586$, $d_1^2 = 2$, $d_2^2 = 4$), block length $8$, and the codes: the $(8, 1)$ repetition code on level 0 ($\delta_0 = 8$), the $(8, 7)$ single parity check code on level 1 ($\delta_1 = 2$), and no code on level 2 ($\delta_2 = 1$). The rate is $(1 + 7 + 8)/8 = 2$ bits per symbol, and the squared distance is $\min(8 \cdot 0.586, 2 \cdot 2, 1 \cdot 4) = 4$, against $2$ for uncoded QPSK: a gain of $3.01$ dB, as for the 4-state TCM code, with simple block codes.

**Polar coded modulation.** A polar code decoded by [successive cancellation](/successive-cancellation-decoding/) already decodes bit after bit with the earlier decisions known. Polar codes on the levels of a set-partitioned constellation fit multistage decoding well, and the frozen bits can be chosen across levels from the level capacities.

## Variations

- **Parallel decoding of the levels.** Decode all levels at once, each with the other bits unknown. Then each level only reaches $I(B_i; Y)$, and the total is the BICM capacity. With Gray labels the loss is small; this is close to BICM with $m$ codes in place of one.
- **Iterative multistage decoding.** Let later stages pass information back to earlier ones, which reduces the effect of errors in the first stages.
- **Other rate rules.** Besides the capacity rule and the balanced distance rule, the equal error probability rule chooses the rates so that each level has about the same error rate at the design SNR. It matters at short block lengths.
- **Shaping.** One or more extra levels can carry the shaping, for example with a nonuniform distribution on the amplitude bits as in [probabilistic constellation shaping](/probabilistic-constellation-shaping/).
- **Hybrid schemes.** Code only the first one or two levels and leave the rest uncoded, or protect the uncoded levels with a light outer code.

## Pitfalls

- **Error propagation.** A wrong decision at stage $i$ gives wrong subsets to all later stages. The design must make the early levels the most reliable, for example by the equal error probability rule.
- **Latency.** The stages run in sequence, and each stage waits for a full block. A system with tight latency may prefer BICM.
- **The labeling.** The chain rule holds for any labeling, but set partitioning makes the level capacities most unequal, which is what makes the stages useful. With Gray labels and parallel decoding, MLC turns into BICM.
- **The level rates depend on the SNR.** The capacity rule fixes the rates for one SNR. At another SNR they are no longer matched, and the levels fail one after another.
- **The name of the decoder.** "Multistage decoding" is the decoder of MLC, not the code. The same encoder can be decoded in parallel.

## Exercises

1. Prove the chain rule $I(X; Y) = \sum_i I(B_i; Y \mid B_0, \ldots, B_{i-1})$ for a one-to-one labeling.
2. Show that two different code sequences of an MLC that first differ at level $i$ are at squared distance at least $d_i^2\delta_i$ when the labeling is a set partitioning.
3. For 4-PAM with set partitioning, write the LLR of $b_1$ given $b_0 = 0$ as a function of $y$ and $N_0$.
4. Find the rates of the levels of the block-coded 8-PSK example and check that the code carries 16 bits per block of 8 symbols.
5. Explain why the level-2 capacity of 8-ASK in the example is close to one bit at $12.62$ dB, using the raw distance $8$ between the points of a level-2 subset.

## References
