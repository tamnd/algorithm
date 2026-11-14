---
tag: 7HE5BF
kind: algorithm
slug: bus-invert-coding
name: Bus-invert coding
aliases:
- bus invert code
- Stan-Burleson coding
area: eda/power-reliability-and-manufacturability
level: core
summary: Stan and Burleson's code that adds one line to an n-bit bus and sends a word inverted when that toggles fewer lines, so at most ceil(n/2) of the n + 1 lines toggle per transfer.
model: word-ram
complexity:
  vars: {n: the number of data lines, T: the number of words sent, w: the machine word size in bits}
  time: {worst: "O(T (1 + n / w))"}
  space: {extra: "O(1 + n / w)"}
properties: {deterministic: true, exact: true, online: true, recursive: false}
history:
  year: 1995
  people: [Mircea R. Stan, Wayne P. Burleson]
  note: Stan and Burleson gave the code in IEEE Transactions on VLSI Systems in 1995, for off-chip buses with large capacitance, and showed that it bounds the peak and lowers the mean number of transitions per transfer.
prereqs: [dynamic-power-dissipation, switching-activity, hamming-distance]
see_also: [hamming-weight, gray-code, transition-density, crosstalk-noise, greedy-algorithm, clock-gating, operand-isolation]
sources:
  - paper: doi:10.1109/92.365453
    title: Mircea R. Stan and Wayne P. Burleson, Bus-invert coding for low-power I/O, IEEE Transactions on VLSI Systems 3(1), 49 to 58, March 1995
    locator: the code with one invert line, the decision by the Hamming distance against the bus value, the peak bound, the mean transitions for random data, and the partitioned bus
  - paper: doi:10.1109/4.126534
    title: Anantha P. Chandrakasan, Samuel Sheng and Robert W. Brodersen, Low-power CMOS digital design, IEEE Journal of Solid-State Circuits 27(4), 473 to 484, April 1992
    locator: the switching component of the power as activity times capacitance times the square of the supply times the clock frequency, the cost that the code lowers
---

Bus-invert coding is a code for a parallel bus that lowers the number of lines that change value per transfer. It adds one line, INV, to an $n$-bit bus. Before each transfer the encoder counts how many of the $n + 1$ lines would toggle if the word went out as it is with INV = 0. If that count $h$ is more than $n/2$, it sends the complement of the word with INV = 1, which toggles $n + 1 - h$ lines. The receiver complements the bus again when INV = 1. So at most $\lceil n/2 \rceil$ of the $n + 1$ lines toggle per transfer, against $n$ without the code, and for random data the mean also falls, from $4$ to $837/256 \approx 3.27$ toggles for $n = 8$. Stan and Burleson (1995) made it for off-chip buses, where each line drives a large capacitance and the [dynamic power](/dynamic-power-dissipation/) of the lines is a large part of the chip power.

## In plain words

Each wire of a bus costs energy when its value changes. Before you send the next word, compare it with what the wires show now. If more than half of the wires would change, send the opposite of every bit instead, so that fewer than half change. Then set one extra wire to say "this word is upside down", and the receiver flips it back.

The extra wire also counts, because it can change too. With it counted, no transfer ever changes more than about half of the wires.

## The problem

A bus has $n$ data lines and one line INV. Its state is a pair $(b, x)$ with $b \in \{0,1\}^n$ the values on the data lines and $x \in \{0, 1\}$ the value on INV. A stream of words $D_1, \ldots, D_T \in \{0,1\}^n$ must go over the bus, one word per transfer, so that the receiver recovers each $D_t$ from the state alone. The cost of a transfer from $(b, x)$ to $(b', x')$ is the number of lines that toggle, the [Hamming distance](/hamming-distance/)

$$ c\big((b, x), (b', x')\big) = |b \oplus b'| + (x \oplus x'), $$

where $|\cdot|$ is the [Hamming weight](/hamming-weight/). Each state that bus-invert coding may send for $D_t$ is either $(D_t, 0)$ or $(\overline{D_t}, 1)$, with $\overline{D}$ the bitwise complement. The goal is to choose one of the two for each word so that the total cost is least, and so that the cost of every single transfer is bounded.

The link to power uses the convention of the [dynamic power](/dynamic-power-dissipation/) page, $P = \alpha C V^2 f$ with $\alpha$ the number of rising (0 to 1) transitions of a line per cycle. On one line, rising and falling transitions alternate, so over a long run $\alpha$ is half the number of toggles per cycle. With equal capacitance $C$ per line, the bus power is $\frac{1}{2} \cdot (\text{mean toggles per transfer}) \cdot C V^2 f$. The model counts each line alone. It ignores the coupling capacitance between neighbor lines, which the Pitfalls come back to. The toggle counts and bounds of this page are exact and have no fitted parameter. Only the line capacitance $C$, extracted from the layout or measured for an off-chip bus, turns them into power.

## The algorithm

```pseudo id=main
BUS-INVERT-ENCODE(D_1, ..., D_T)
L1  (b, x) ← (0, 0), or the state that the bus has now
L2  for t ← 1 to T do
L3      h ← |b ⊕ D_t| + x                          ▷ toggles if (D_t, 0) is sent
L4      if 2h > n then (b, x) ← (not D_t, 1)       ▷ this toggles n + 1 − h lines
L5      else (b, x) ← (D_t, 0)
L6      send (b, x)

BUS-INVERT-DECODE(b, x)
L7  return b ⊕ (x, x, ..., x)
```

Line L3 is the whole decision. It counts INV too: if INV is 1 now and the plain word is sent, INV falls, which is one more toggle. In hardware, line L3 is $n + 1$ XOR gates and a majority voter over $n + 1$ bits, and the choice of lines L4 and L5 is $n$ XOR gates driven by the voter. The decoder is $n$ XOR gates.

## Example

Take $n = 8$, the start state $(00000000, 0)$, and the words below.

| $t$ | $D_t$ | $h$ (line L3) | sent $b$ | INV | toggles | toggles without the code |
|---|---|---|---|---|---|---|
| 1 | 11111110 | 7 | 00000001 | 1 | 2 | 7 |
| 2 | 11110000 | 5 + 1 = 6 | 00001111 | 1 | 3 | 3 |
| 3 | 00001111 | 0 + 1 = 1 | 00001111 | 0 | 1 | 8 |
| 4 | 00001110 | 1 + 0 = 1 | 00001110 | 0 | 1 | 1 |

At $t = 2$ the plain word would toggle 5 data lines and drop INV, 6 toggles, so the encoder sends the complement, which toggles $9 - 6 = 3$. At $t = 3$ the data lines already show the word, and the only toggle is INV falling. The total is 7 toggles with the code and 19 without it, and the peak is 3 against 8. The decoder gets back each word: $00000001 \oplus 11111111 = 11111110$, and so on.

## Correctness

Two facts carry the proofs, which are in [the proof file](proofs/correctness.md).

**Complement.** From any state $(b, x)$, the two candidates for a word $D$ toggle $h = |b \oplus D| + x$ and $|b \oplus \overline{D}| + (1 - x) = (n - |b \oplus D|) + 1 - x = n + 1 - h$ lines. Lines L4 and L5 pick the smaller of the two, so each transfer costs $\min(h, n + 1 - h)$.

**Bound.** So each transfer toggles at most $\lfloor (n+1)/2 \rfloor = \lceil n/2 \rceil$ lines. For even $n$ the bound is $n/2$, and it is met when $h = n/2$. For odd $n$ it is $(n+1)/2$, and it is met when $h = (n+1)/2$, where the two candidates tie. INV is counted in both cases. A rule that counts only the data lines, and inverts when $|b \oplus D| > n/2$, can toggle $\lfloor n/2 \rfloor + 1$ lines, which is more than $n/2$ for even $n$: with INV at 1 and $|b \oplus D| = n/2$ it keeps the plain word, and INV falls too.

**Whole sequences.** The greedy choice is also optimal over a whole stream, among all $2^T$ choices of the INV bits. The cost of transfer $t$ depends only on $D_{t-1} \oplus D_t$ and on $x_{t-1} \oplus x_t$, so the total is a sum of terms that each depend on one free bit, and lines L4 and L5 choose each of these bits at its best value.

Decoding is right because line L7 undoes the complement of line L4 and leaves the word of line L5 as it is.

## Complexity

Each word takes one XOR, one population count and one compare on $n$ bits, so $O(\lceil n/w \rceil)$ time on a word RAM with $w$-bit words and a constant-time population count, and $O(T \lceil n/w \rceil)$ for the stream. The state is one word of $n$ bits and one bit. The code is online: it needs only the current state and the next word. In hardware, the cost is the majority voter, whose depth grows as $O(\log n)$, plus one extra line and $2n$ XOR gates on the two sides.

## Properties

- **Peak bound, proved.** At most $\lceil n/2 \rceil$ of the $n + 1$ lines toggle per transfer, for every input, and the bound is tight.
- **Mean for random data, computed exactly.** If the words are independent and uniform, then $|b \oplus D|$ is binomial with parameters $n$ and $1/2$ whatever the state is, and the mean cost is $E[\min(B, n + 1 - B)]$ with $B \sim \mathrm{Bin}(n, 1/2)$. This gives 3.27 toggles for $n = 8$ (4 without the code, 18.3% less), 6.83 for $n = 16$ (8, 14.6% less), and 14.19 for $n = 32$ (16, 11.3% less). Stan and Burleson report the same trend. The gain falls as $n$ grows, because the binomial gets narrow around $n/2$.
- **Optimal among its codewords.** No other choice of INV bits for the same words toggles fewer lines in total.
- **Online and deterministic.** Each output depends only on the state and the next word.
- **Not a gain for every stream.** On data with few toggles, such as a counter on the address bus, $h$ is small, the code never inverts, and it only adds a line.

## Variants and improvements

- **Partitioned bus.** Split a wide bus into $k$ groups, each with its own INV line. For random data, a 32-bit bus with 4 groups of 8 has a mean of $4 \cdot 837/256 \approx 13.08$ toggles, against 13.66 with 2 groups of 16, 14.19 with one INV line and 16 without a code. Each group costs one more line and one more voter.
- **Codes for correlated data.** Address buses carry mostly consecutive values. A [Gray code](/gray-code/) on the address toggles one line per increment. Other address codes add a line that tells the receiver to increment its own copy, so that consecutive addresses toggle nothing.
- **Limited-weight codes.** Stan and Burleson also studied codes in which every codeword, or every transition, has a bounded Hamming weight. Bus-invert is the simplest such code with one extra line.
- **Coupling-aware codes.** On-chip wires in deep submicron processes have a coupling capacitance between neighbors that is larger than the capacitance to ground. A cost function that counts opposite toggles of neighbor lines gives other inversion rules, with the same structure of a choice between candidate codewords.

## When to use it

Use it on wide buses with a large load per line and data close to random: off-chip data buses, long on-chip global buses and wide memory interfaces. It also bounds the simultaneous switching current, since at most $\lceil n/2 \rceil$ drivers switch at once, which lowers ground bounce and the peak current that the [power grid](/power-grid-analysis/) must deliver. Do not use it where the energy of the encoder, the voter and the XOR gates is close to the energy saved, as on short local buses, or on streams with few toggles, where a code for correlated data fits better.

## Pitfalls

- **Forgetting INV in the count.** A rule that compares only the $n$ data lines with $n/2$ can toggle $\lfloor n/2 \rfloor + 1$ lines, as shown above. For even $n$ this breaks the bound $\lceil n/2 \rceil$ and wastes one toggle. For odd $n$ the two rules differ only on ties, so the slip stays hidden until the bus width changes.
- **Ties.** For odd $n$, $h = (n+1)/2$ makes the two candidates equal. Either choice is right, and by the argument for whole sequences it does not change the cost of later transfers either. A test that compares $h$ with the wrong half, such as $h > n/2 + 1$, is not right: it misses transfers where the complement is cheaper.
- **The encoder sits on the critical path.** The voter and the XOR gates add delay before the drivers. Pipelines put the encoder in the stage before the bus.
- **Counting toggles, not energy.** The bound is on toggles. With coupling between neighbors, a transfer with few toggles can still cost much, for example when two neighbors toggle in opposite directions. Check the real cost model of the wires.
- **Rising transitions.** The power formula of the [dynamic power](/dynamic-power-dissipation/) page counts rising transitions. A toggle count is twice that over a long run, not in each transfer.

## Implementations

## History

Stan and Burleson (1995) introduced the code for low-power input and output, at a time when off-chip buses took a large share of the power of a chip. They gave the peak bound, the mean for random data and the partitioned form, and they noted that the code also lowers the peak supply current. Later work on bus coding took two directions: codes for the correlated streams of address buses, and codes that count the coupling between on-chip wires.

## References
