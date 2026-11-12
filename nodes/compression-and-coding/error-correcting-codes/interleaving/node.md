---
tag: E58STP
kind: technique
slug: interleaving
name: Interleaving
aliases:
- interleaver
area: compression-and-coding/error-correcting-codes
level: core
summary: "Send the symbols of several codewords in a mixed order, so that a burst of errors on the channel becomes a few scattered errors in each codeword, which a random-error code can correct."
prereqs: [burst-errors]
see_also: [burst-errors, concatenated-codes, reed-solomon-code, product-codes, convolutional-code, turbo-code, hamming-code, erasure-decoding]
sources:
  - paper: doi:10.1109/TIT.1970.1054443
    title: J. L. Ramsey, Realization of optimum interleavers, IEEE Transactions on Information Theory 16(3), 1970
    locator: The definition of interleavers that separate symbols by a given distance, and constructions with the least storage and delay, including the convolutional (type III) interleaver
  - paper: doi:10.1109/TCOM.1971.1090719
    title: G. David Forney, Jr., Burst-correcting codes for the classic bursty channel, IEEE Transactions on Communication Technology 19(5), 1971
    locator: The convolutional interleaver with branches of increasing delay, used with a random-error code on a channel with bursts
  - url: https://www.etsi.org/deliver/etsi_en/300400_300499/300421/01.01.02_60/en_300421v010102p.pdf
    title: ETSI EN 300 421 V1.1.2, Digital Video Broadcasting (DVB); Framing structure, channel coding and modulation for 11/12 GHz satellite services, 1997
    locator: The clause on convolutional interleaving (Forney approach, I = 12 branches, branch depth M = 17 = 204/12, branch j a FIFO of M j cells, sync bytes in branch 0) and the clause on the RS(204,188) outer code
  - book: isbn:9780780310254
    title: Stephen B. Wicker and Vijay K. Bhargava (editors), Reed-Solomon Codes and Their Applications, IEEE Press, 1994
    locator: Chapter by K. A. Schouhamer Immink, Reed-Solomon codes and the compact disc (the cross-interleaved Reed-Solomon code with the C1 and C2 codes)
---

Interleaving is a technique that changes the order of the coded symbols before they go on the channel and restores the order at the receiver. Symbols that are next to each other on the channel then belong to different codewords, so a burst of errors is shared out among many codewords, each of which sees only a few errors. With interleaving, a code built for random errors, such as a [Hamming code](/hamming-code/) or a [Reed-Solomon code](/reed-solomon-code/), works on a channel with [burst errors](/burst-errors/). The price is memory and delay at both ends.

## In plain words

A code can repair a few wrong symbols in each block. A burst puts many wrong symbols into one block, and that block is lost.

So do not send the blocks one after another. Take several blocks, send the first symbol of each block, then the second symbol of each block, and so on. The receiver puts the symbols back into their blocks. A burst on the line now hurts a run of neighbours on the line, and these neighbours come from different blocks. Each block gets only one or two wrong symbols, which its code can repair.

The more blocks you mix, the longer the burst you can survive. But the receiver must wait until all the mixed blocks have arrived before it can decode, and both ends must store them.

## When it applies

- The channel makes errors in bursts, or its quality changes slowly in time (fading, scratches, impulse noise), and the bursts are shorter than the interleaver can spread.
- A code that corrects $t$ random errors per codeword, or bursts of length $b$, is already at hand, and building a new code for long bursts is not worth it.
- The application can accept the delay of the interleaver: about $2 I n$ symbols for a block interleaver of depth $I$ and codeword length $n$, and $I(I - 1)J$ symbols for a convolutional interleaver.
- The decoder does not need to know where the bursts are. A decoder that can use the memory of the channel can do better than interleaving, which hides the memory.

## The template

The template sends $I$ messages $m_0, \ldots, m_{I-1}$ over a channel. The holes are the code (ENCODE gives a codeword of $n$ symbols, DECODE corrects every pattern of at most $t$ errors, or every burst of length at most $b$) and the interleaver PERMUTE, here a block interleaver of depth $I$. Indices are 0-based.

```pseudo id=main
INTERLEAVED-LINK(m_0, ..., m_{I−1})           ▷ holes: ENCODE, DECODE, PERMUTE
L1  for j = 0 to I − 1 do
L2      c_j ← ENCODE(m_j)                      ▷ n symbols
L3  x ← PERMUTE(c_0, ..., c_{I−1})              ▷ block: x[c·I + r] ← c_r[c]
L4  y ← CHANNEL(x)                              ▷ the errors come in bursts
L5  (r_0, ..., r_{I−1}) ← PERMUTE⁻¹(y)          ▷ r_j[c] ← y[c·I + j]
L6  for j = 0 to I − 1 do
L7      m̂_j ← DECODE(r_j)
L8  return m̂_0, ..., m̂_{I−1}
```

**The block interleaver.** Write the $I$ codewords as the rows of an $I \times n$ array and read the array out column by column. Symbol $c$ of codeword $r$ goes to channel position $cI + r$. The number $I$ is the **depth** of the interleaver.

**Why bursts are spread.** Let the channel errors lie in a window of $L$ consecutive positions $p, \ldots, p + L - 1$. The positions of row $r$ are $r, r + I, r + 2I, \ldots$, one in every $I$ consecutive positions, so the window holds at most $\lceil L/I \rceil$ of them, and these are in consecutive columns. So after line L5, row $r$ has an error pattern of burst length at most $\lceil L/I \rceil$. Two guarantees follow:

- If DECODE corrects $t$ random errors, every burst of length at most $I t$ is corrected.
- If DECODE corrects all bursts of length at most $b$, every burst of length at most $I b$ is corrected. A code for bursts of length $b$ becomes a code for bursts of length $I b$, at the same rate.

Both bounds are tight: a solid burst of length $I t + 1$ puts $t + 1$ errors into one row.

**Cost.** Lines L3 and L5 take $O(In)$ time. In the simple scheme that writes a whole array before it reads the array out, each side stores $I n$ symbols and the end-to-end delay is about $2In$ symbol times. The code, its rate and its random-error power are unchanged.

**Example.** The $[7, 4, 3]$ Hamming code corrects one error, so on its own a burst of two adjacent errors defeats it. With $I = 5$, five codewords give $35$ channel bits, and every one of the $511$ error patterns of burst length at most $5$ is corrected. A solid burst of length 6 puts two errors into the first codeword, and that codeword is decoded wrongly.

## Classic examples

- **Concatenated codes for deep space and broadcasting.** In a [concatenated code](/concatenated-codes/), the inner decoder of a [convolutional code](/convolutional-code/) makes its mistakes in bursts. A byte interleaver between the inner code and an outer Reed-Solomon code spreads these bursts over many Reed-Solomon codewords. In DVB-S (ETSI EN 300 421) the outer code is the shortened Reed-Solomon code $(204, 188)$ over $\mathrm{GF}(2^8)$, which corrects 8 byte errors, and the interleaver is a convolutional interleaver with $I = 12$ branches and branch unit $J = 17 = 204/12$. Each codeword starts in branch 0, so every burst of at most $12 \cdot 8 = 96$ bytes leaves at most 8 bytes in error in each codeword.
- **The compact disc.** The cross-interleaved Reed-Solomon code (CIRC, standardised in IEC 60908) takes 24 audio bytes per frame, encodes them with a shortened $(28, 24)$ Reed-Solomon code C2, delays the 28 bytes by different numbers of frames, and encodes the result with a shortened $(32, 28)$ Reed-Solomon code C1, so the rate is $24/32 = 3/4$. The C1 decoder corrects small errors and marks the codewords it cannot correct, and because of the delays, the bytes of a long burst reach the C2 decoder as marked bytes spread over many C2 codewords, where [erasure decoding](/erasure-decoding/) fills them. This page does not reproduce the delay values or test data from IEC 60908.
- **Interleaved codes are product codes.** Block interleaving a code $C$ to depth $I$ gives the [product](/product-codes/) of $C$ with the trivial code of length $I$. Replacing the trivial code by a real code gives a product code, whose column code also corrects bursts and erasures.
- **Interleavers inside turbo codes.** A [turbo code](/turbo-code/) encodes the data once in the given order and once after a permutation. There the purpose is not to spread channel bursts, but to make the two parity streams differ, so that an input that gives low-weight parity in one encoder rarely gives low-weight parity in the other.

## Variations

- **Convolutional interleaver.** Ramsey (1970) and Forney (1971) described interleavers that work on a stream. A commutator sends input symbol $u$ into branch $u \bmod I$, where branch $i$ is a first-in first-out line of $iJ$ cells, so the symbol leaves at channel time $u + IJ\,(u \bmod I)$. The deinterleaver has branches of $(I - 1 - i)J$ cells, so every symbol is delayed by the same $I(I - 1)J$ symbols in total. If $IJ \ge n + 1$, two symbols of one codeword are at least $n$ input positions apart whenever they are fewer than $I$ channel positions apart, so every burst of length at most $tI$ puts at most $t$ errors into each codeword, whatever the codeword boundaries. If $IJ = n$, the same holds when each codeword starts in branch 0. Each side stores $J \cdot I(I - 1)/2$ symbols, less than half of the $In$ of a block interleaver with $IJ \approx n$: for the DVB-S values, $1122$ cells against $2448$.
- **Interleaving in other dimensions.** Bits can be spread over frequency (subcarriers in multicarrier systems) or over space (antennas, disks), so that one bad carrier or one failed disk erases only a few symbols of each codeword.
- **Bit interleaving with modulation.** In bit-interleaved coded modulation, the coded bits are permuted before they are mapped to the symbols of a large signal set, so that the bits of one symbol, which fade together, belong to different parts of the code.
- **Pseudo-random interleavers.** A fixed pseudo-random permutation spreads bursts on average, without the regular structure that a periodic noise source can hit. Turbo codes use such permutations with a spread condition: inputs that are close together must be far apart after the permutation.
- **Variable depth.** Some systems choose the depth $I$ at run time, trading delay against the length of the bursts they must survive.

## Pitfalls

- **Bursts longer than the design.** A burst of length $It + 1$ already defeats a block interleaver of depth $I$ with a $t$-error-correcting code. Choose $I$ from the longest burst expected, with a margin.
- **Periodic errors.** In a block interleaver, the positions $p, p + I, p + 2I, \ldots$ all belong to the same codeword. Noise that repeats with period $I$ (or a multiple of it) hits one codeword again and again, while the other codewords stay clean.
- **Delay.** Real-time voice and control links have a delay budget. A deep interleaver can exceed it, which is why speech systems use shallow interleaving and accept some loss.
- **Alignment and synchronisation.** The deinterleaver must know where the array, or the commutator cycle, starts. A convolutional interleaver with $IJ = n$ needs the codeword boundaries on branch 0; DVB-S puts the packet sync byte there for this reason.
- **Lost channel memory.** The deinterleaver hides the memory of the channel from the decoder, which then treats the errors as independent. A decoder that tracks the state of a bursty channel, or uses the erasure marks from an inner decoder, can do better.
- **No gain on a memoryless channel.** If the errors are independent, interleaving changes nothing: the errors in each codeword are still independent with the same probability.

## Exercises

1. Show that the deinterleaver of a block interleaver of depth $I$ for codewords of length $n$ is a block interleaver of depth $n$ for words of length $I$.
2. A code of minimum distance $d$ corrects $e$ errors and $s$ erasures together whenever $2e + s < d$. Show that with block interleaving of depth $I$, one burst of errors of length at most $Ie$ and one burst of erasures of length at most $Is$ in the same array are always corrected.
3. Prove that in a convolutional interleaver with $IJ \ge n + 1$, two input symbols that are fewer than $I$ channel positions apart are at least $IJ - 1$ input positions apart.
4. Find the shortest periodic error pattern that defeats a block interleaver of depth 4 used with a code that corrects one error.

## References
