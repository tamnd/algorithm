---
tag: ZSECMK
kind: concept
slug: trellis
name: Code trellis
aliases:
- trellis representation
area: compression-and-coding/error-correcting-codes
level: advanced
summary: A layered graph whose paths from the start node to the end node are exactly the codewords. Viterbi and BCJR decoding run on it in time linear in its number of edges.
history:
  year: 1973
  people: [G. David Forney Jr., Lalit Bahl, John Cocke, Frederick Jelinek, Josef Raviv, Jack K. Wolf]
  note: Forney drew the trellis of a convolutional code in 1973. Bahl, Cocke, Jelinek and Raviv in 1974 and Wolf in 1978 built the trellis of any linear block code from its parity-check matrix.
prereqs: [convolutional-code, parity-check-matrix, linear-code]
see_also: [maximum-likelihood-sequence-estimation, bcjr-algorithm, syndrome, hamming-code, dag-shortest-paths, dag-dynamic-programming, viterbi-algorithm, hidden-markov-model]
sources:
  - paper: doi:10.1109/PROC.1973.9030
    title: G. D. Forney, Jr., The Viterbi algorithm, Proceedings of the IEEE 61(3), 1973, pages 268 to 278
    locator: The trellis diagram of a shift register process and of a convolutional encoder
  - paper: doi:10.1109/TIT.1974.1055186
    title: L. R. Bahl, J. Cocke, F. Jelinek and J. Raviv, Optimal decoding of linear codes for minimizing symbol error rate, IEEE Transactions on Information Theory 20(2), 1974, pages 284 to 287
    locator: The trellis of a linear block code whose states are partial syndromes
  - paper: "J. K. Wolf, Efficient maximum likelihood decoding of linear block codes using a trellis, IEEE Transactions on Information Theory 24(1), 1978, pages 76 to 80"
    title: Efficient maximum likelihood decoding of linear block codes using a trellis
    locator: The syndrome trellis of an (n, k) code with at most 2^(n-k) states, and Viterbi decoding on it
  - paper: "R. J. McEliece, On the BCJR trellis for linear block codes, IEEE Transactions on Information Theory 42(4), 1996, pages 1072 to 1092"
    title: On the BCJR trellis for linear block codes
    locator: The proof that the BCJR (syndrome) trellis is minimal, and the count of its states and edges
  - book: isbn:9780130426727
    title: Shu Lin and Daniel J. Costello, Jr., Error Control Coding, second edition, Pearson Prentice Hall, 2004
    locator: Chapter 9 (trellises for linear block codes, the state space dimension, minimal trellises) and Chapter 11 (the trellis of a convolutional code)
---

A code trellis is a layered directed graph with one start node and one end node, where each edge carries a code symbol and the label sequences of the start to end paths are exactly the codewords of the code. The layers are the times $0, 1, \ldots, n$, and the nodes of layer $i$ are the *states* that a decoder must remember after it has read $i$ symbols. A [convolutional code](/convolutional-code/) has a natural trellis from its shift register, and every [linear code](/linear-code/) has a minimal trellis made from its [parity-check matrix](/parity-check-matrix/). Decoding on the trellis is a [dynamic program on a DAG](/dag-dynamic-programming/): the Viterbi algorithm for [MLSE](/maximum-likelihood-sequence-estimation/) and the [BCJR algorithm](/bcjr-algorithm/) for bit posteriors.

## In plain words

Think of a map with columns of towns, one column for each position of the codeword. Each road goes from a town in one column to a town in the next column, and each road has a label, 0 or 1. A trip from the single town on the left to the single town on the right reads one label per road. The map is built so that the words you can read on a trip are exactly the codewords, each one on exactly one trip.

A decoder then does not need to list all codewords. It walks the map column by column and keeps, for each town, only the best way to get there. The work is the number of roads, which can be far less than the number of codewords.

## The idea

**Definition.** A trellis of depth $n$ over GF(2) is a directed graph with node layers $V_0, \ldots, V_n$, where $|V_0| = |V_n| = 1$, and with edges only from $V_i$ to $V_{i+1}$, each labeled by a symbol $c_{i+1} \in \{0, 1\}$. A trellis *represents* a code $C$ of length $n$ when the map from start to end paths to label sequences is a bijection onto $C$. The state profile is $(|V_0|, \ldots, |V_n|)$.

**The trellis of a convolutional code.** For a rate $1/n$ encoder of memory $m$, the state at time $t$ is the content of the shift register, so each layer has $2^m$ states. Each state has two outgoing edges, for the inputs 0 and 1, and each edge carries the $n$ output bits of that step. In this page an edge of a convolutional trellis carries a block of $n$ bits, and a section of the trellis is one input step. A terminated code adds $m$ tail steps with only the edges that shift in a zero, so all paths end in state 0. A tail-biting trellis lets a path start in any state $s$ and keeps only the paths that end in the same state $s$. It has no tail and no rate loss, but it is not a trellis with one start node: it is the union of $2^m$ trellises, one per start state.

**The syndrome trellis of a block code (Bahl, Cocke, Jelinek and Raviv 1974, Wolf 1978).** Let $H$ be an $r \times n$ parity-check matrix with columns $h_1, \ldots, h_n$, so $C = \{c : H c^T = 0\}$. The state of a word after $i$ symbols is the partial syndrome

$$s_i = c_1 h_1 + \cdots + c_i h_i \in \mathrm{GF}(2)^r, \qquad s_0 = 0,$$

and the edge from $s_{i-1}$ with label $c_i$ goes to $s_{i-1} + c_i h_i$. A forward pass keeps the states reachable from $s_0 = 0$, and a backward pass keeps those that reach $s_n = 0$. Then the paths are exactly the codewords: a path from 0 to 0 reads a word $c$ with $\sum_i c_i h_i = H c^T = 0$, and each codeword gives the path of its partial syndromes, whose states survive both passes because the path reaches them from 0 and goes on to 0. Two different words differ at some first position $i$, so their paths use different edges there, and the map is one to one. There are at most $2^r = 2^{n-k}$ states in each layer when $H$ has full rank.

**The number of states.** Let $C_{\text{past}}(i)$ be the subcode of the codewords that are zero after position $i$, and $C_{\text{future}}(i)$ the subcode of those that are zero in the first $i$ positions, with dimensions $k_p(i)$ and $k_f(i)$. Then the syndrome trellis has

$$|V_i| = 2^{\,k - k_p(i) - k_f(i)}$$

states at depth $i$. *Proof.* The map $c \mapsto s_i(c)$ is linear on $C$, and its image is $V_i$. A codeword $c$ is in the kernel when its first $i$ symbols have partial syndrome 0. Then $(c_1, \ldots, c_i, 0, \ldots, 0)$ is a codeword, and so is the rest $(0, \ldots, 0, c_{i+1}, \ldots, c_n)$. So the kernel is $C_{\text{past}}(i) \oplus C_{\text{future}}(i)$, of dimension $k_p + k_f$, and the image has $2^{k - k_p - k_f}$ elements. $\square$ McEliece (1996) proved that no trellis of $C$ for the same order of the positions has fewer states at any depth, so the syndrome trellis is *minimal*. The order of the positions matters: two equivalent codes can have different minimal profiles.

**Decoding on a trellis.** A decoder gives each edge a branch metric from the channel output, such as $-\ln P(y_i \mid c_i)$. The cost of a path is the sum of its edge metrics, so the most likely codeword is a least cost path, which a [shortest path in a DAG](/dag-shortest-paths/) finds with one pass over the edges. This is the Viterbi algorithm. Replace (min, +) by (+, ×) and the same pass, run in both directions, gives the posterior of each bit: this is BCJR. Both take $\Theta(E)$ operations for $E$ edges, so the size of the trellis is the cost of exact soft-decision decoding.

**How it differs from the trellis of a hidden Markov model.** The [Viterbi algorithm](/viterbi-algorithm/) and the [forward-backward algorithm](/forward-backward-algorithm/) of the machine learning area run on the time-unrolled states of a [hidden Markov model](/hidden-markov-model/), with transition probabilities that are part of the model. A code trellis is fixed by the code: each edge either exists or does not, all paths are equally likely a priori (or weighted only by the prior of the input bits), and the only probabilities come from the channel through the branch metrics.

## Examples

**The Hamming [7, 4] code.** Take the [Hamming code](/hamming-code/) with

$$H = \begin{pmatrix} 1&0&1&1&1&0&0 \\ 1&1&1&0&0&1&0 \\ 0&1&1&1&0&0&1 \end{pmatrix}.$$

The 16 codewords are 0000000, 0001101, 0010111, 0011010, 0100011, 0101110, 0110100, 0111001, 1000110, 1001011, 1010001, 1011100, 1100101, 1101000, 1110010 and 1111111. The dimensions of the past and future subcodes give the profile:

| depth $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $k_p(i)$ | 0 | 0 | 0 | 0 | 1 | 2 | 3 | 4 |
| $k_f(i)$ | 4 | 3 | 2 | 1 | 0 | 0 | 0 | 0 |
| $\lvert V_i \rvert$ | 1 | 2 | 4 | 8 | 8 | 4 | 2 | 1 |

The trellis has 30 states and $2 + 4 + 8 + 16 + 8 + 4 + 2 = 44$ edges, and its 16 paths read the 16 codewords. At depth 1 the two states are $0$ and $h_1 = (1, 1, 0)^T$. If the columns are put in the order of the numbers 1 to 7 in binary, the code is an equivalent Hamming code, and its profile is (1, 2, 4, 4, 8, 4, 2, 1).

**The (7, 5) convolutional code, terminated.** With 4 input bits and 2 tail steps, the trellis has 6 sections and the profile (1, 2, 4, 4, 4, 2, 1): the states fan out from state 0 while the register fills, stay at 4, and close during the tail. It has 16 paths, one per input word. The input 1011 follows the states 00, 10, 01, 10, 11, 01, 00 (newest bit on the left) and reads 11 10 00 01 01 11.

**Tail-biting.** The tail-biting (7, 5) code with 4 input bits has 16 codewords of length 8. Each starts and ends in the state of its last two input bits, and no tail is sent, so the rate stays 1/2 in place of the 4/12 = 1/3 of the terminated code.

## Where it is used

- [Maximum-likelihood sequence estimation](/maximum-likelihood-sequence-estimation/) with the Viterbi algorithm, for convolutional codes and for channels with intersymbol interference, where the trellis states are the last symbols that the channel remembers.
- The [BCJR algorithm](/bcjr-algorithm/) in the constituent decoders of [turbo decoding](/turbo-decoding/).
- Soft-decision maximum likelihood decoding of short block codes, where the syndrome trellis has at most $2^{n-k}$ states per layer, and the [Hamming code](/hamming-code/) or a short [Reed-Muller code](/reed-muller-code/) has a small trellis.
- Trellis coded modulation, where the edges carry points of a signal constellation in place of bits.

## References
