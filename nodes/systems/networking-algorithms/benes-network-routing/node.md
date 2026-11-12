---
tag: ZPDNJR
kind: algorithm
slug: benes-network-routing
name: Benes network routing
aliases:
- Benes network
- looping algorithm for Benes networks
area: systems/networking-algorithms
level: advanced
summary: "The looping algorithm sets the N log2 N - N/2 switches of a Benes network so that any permutation is realized with no conflict, in O(N log N) time, by 2-coloring cycles and recursing on two halves."
solves: [permutation-routing]
model: word-ram
complexity:
  vars: {n: the number of lines (a power of 2)}
  time: {worst: Θ(n log n)}
  space: {extra: Θ(n log n)}
properties: {online: false, deterministic: true, recursive: true}
history:
  year: 1971
  people: [Václav E. Beneš, D. C. Opferman, N. T. Tsao-Wu, Abraham Waksman]
  note: Beneš showed in 1964 that his network is rearrangeable. Waksman (1968) and Opferman and Tsao-Wu (1971) gave the looping algorithm that sets the switches.
prereqs: [permutation, bipartite-graph, permutation-cycle-decomposition]
see_also: [sorting-network, bitonic-sort, odd-even-merge-sort, edge-coloring, fast-fourier-transform, dimension-order-routing, valiant-routing, switch-scheduling]
sources:
  - paper: "Václav E. Beneš, Permutation groups, complexes, and rearrangeable connecting networks, Bell System Technical Journal 43(4) (1964), 1619-1640"
    locator: the recursive network of 2 x 2 switches and the proof that it is rearrangeable
  - paper: doi:10.1145/321439.321449
    title: "Abraham Waksman, A permutation network, Journal of the ACM 15(1) (1968), 159-163"
    locator: the network with N log2 N - N + 1 switches, one switch per subnetwork fixed, and the routing by loops
  - paper: "D. C. Opferman and N. T. Tsao-Wu, On a class of rearrangeable switching networks, Part I: Control algorithm, Bell System Technical Journal 50(5) (1971), 1579-1600"
    locator: the looping algorithm for setting the switches
  - paper: "David Nassimi and Sartaj Sahni, Parallel algorithms to set up the Benes permutation network, IEEE Transactions on Computers C-31(2) (1982), 148-154"
    locator: setting the switches in parallel in polylogarithmic time
  - book: isbn:9781558601178
    title: F. Thomson Leighton, Introduction to Parallel Algorithms and Architectures, Arrays, Trees, Hypercubes, Morgan Kaufmann, 1992
    locator: Chapter 3, the section on the Beneš network (rearrangeability and the looping algorithm)
  - book: isbn:9780122007514
    title: William J. Dally and Brian Towles, Principles and Practices of Interconnection Networks, Morgan Kaufmann, 2004
    locator: Chapter 6, non-blocking networks (Clos networks and the Beneš network as a recursive Clos network)
---

A Beneš network on $N = 2^n$ lines is a network of $2 \times 2$ switches, each set either straight or crossed, that can connect the inputs to the outputs in any of the $N!$ permutations. It is called rearrangeable: every permutation can be realized, but a new permutation may need all switches to be set again. The looping algorithm finds the settings for a given permutation. It walks along cycles of a constraint graph and colors each input up or down, so that the two inputs of each first-column switch, and the two inputs bound for each last-column switch, take different halves. Then it recurses on the two halves. It runs in $O(N \log N)$ time, which is $O(1)$ per switch. The network has $N \log_2 N - N/2$ switches in $2 \log_2 N - 1$ columns, within $O(N)$ of the $\log_2 N!$ lower bound.

## In plain words

You want each of $N$ input wires to reach a chosen output wire. The network has a first column of small boxes, two smaller networks of the same kind (top and bottom), and a last column of boxes. Each box has two wires in and two out, and it either passes them straight or swaps them.

Each first box must send one wire to the top network and one to the bottom. Each last box must get one wire from each. So send some wire to the top. Its box partner must go to the bottom. The wire that shares a last box with that partner must go to the top, and so on. This chain comes back to its start and never asks a wire to go both ways. Then each half is a smaller problem of the same kind.

## The problem

**Input.** A permutation $\pi$ of $\{0, \ldots, N-1\}$, with $N = 2^n \ge 2$.

**Output.** A setting, straight or crossed, of every switch of the Beneš network $B_N$, such that the signal at input line $x$ leaves at output line $\pi(x)$ for every $x$.

The network $B_N$ is defined recursively. $B_2$ is one switch. For $N \ge 4$, $B_N$ has a first column of $N/2$ switches, an upper copy $U$ and a lower copy $L$ of $B_{N/2}$, and a last column of $N/2$ switches. Input switch $k$ takes lines $2k$ and $2k+1$ and sends its top output to line $k$ of $U$ and its bottom output to line $k$ of $L$. Output switch $k$ takes line $k$ of $U$ on top and line $k$ of $L$ at the bottom, and drives output lines $2k$ and $2k+1$. Unrolled, $B_N$ is two butterfly networks placed back to back, with the middle column shared.

## The algorithm

Write $x \oplus 1$ for the other line of the same switch ($x$ with its last bit flipped). Each input gets a color, up or down, which says the half that it passes through.

```pseudo id=main
BENES-ROUTE(π, N)
L1  if N = 2 then return one switch, crossed iff π(0) = 1
L2  make every input uncolored
L3  for each input x = 0, 1, ..., N - 1 that is uncolored do   ▷ start a new loop
L4      y ← x
L5      while y is uncolored do
L6          color y up and y ⊕ 1 down              ▷ the two inputs of one input switch
L7          y ← π⁻¹(π(y ⊕ 1) ⊕ 1)                 ▷ shares an output switch with y ⊕ 1, so it goes up
L8  set input switch k straight iff input 2k is up
L9  set output switch k straight iff input π⁻¹(2k) is up
L10 for each input x, put ⌊π(x)/2⌋ at position ⌊x/2⌋ of π_U if x is up, else of π_L
L11 BENES-ROUTE(π_U, N/2) for U and BENES-ROUTE(π_L, N/2) for L
L12 return all the settings
```

Line L7 is the heart of the method. The input $y \oplus 1$ was just colored down. Its output $\pi(y \oplus 1)$ shares an output switch with output $\pi(y \oplus 1) \oplus 1$, and the input bound for that output must come from the other half, so it is colored up in the next pass. The loop stops when it comes back to $x$.

## Example

Take $N = 8$ and $\pi = (5, 7, 2, 4, 0, 6, 1, 3)$, that is, input 0 goes to output 5, input 1 to output 7, and so on. The inverse is $\pi^{-1} = (4, 6, 2, 7, 3, 0, 5, 1)$.

| pass | $y$ (up) | $y \oplus 1$ (down) | $\pi(y \oplus 1)$ | partner output | next $y$ |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 7 | 6 | $\pi^{-1}(6) = 5$ |
| 2 | 5 | 4 | 0 | 1 | $\pi^{-1}(1) = 6$ |
| 3 | 6 | 7 | 3 | 2 | $\pi^{-1}(2) = 2$ |
| 4 | 2 | 3 | 4 | 5 | $\pi^{-1}(5) = 0$, colored: stop |

One loop colors all eight inputs: up $= \{0, 2, 5, 6\}$, down $= \{1, 3, 4, 7\}$. The input switches are (straight, straight, crossed, straight), because inputs 0, 2 and 6 are up and input 4 is down. The output switches look at the inputs bound for outputs 0, 2, 4 and 6, which are 4 (down), 2 (up), 3 (down) and 5 (up), so they are (crossed, straight, crossed, straight). The up inputs 0, 2, 5 and 6 sit on input switches 0, 1, 2 and 3 and go to output switches 2, 1, 3 and 0, so $\pi_U = (2, 1, 3, 0)$. The down inputs 1, 3, 4 and 7 give $\pi_L = (3, 2, 0, 1)$. The two recursive calls on 4 lines then set the 12 inner switches. The implementation checks the result by pushing the values through the network.

The network for $N = 8$ has $20$ switches in 5 columns. Waksman's form needs 17, and the counting lower bound is $\lceil \log_2 8! \rceil = 16$. For $N = 1024$, the numbers are 9728, 9217 and 8770.

## Correctness

The constraints form a graph on the inputs with two kinds of edges: $\{x, x \oplus 1\}$ for two inputs of the same input switch, and $\{x, \pi^{-1}(\pi(x) \oplus 1)\}$ for two inputs bound for the same output switch. Each input has one edge of each kind, so the graph is a union of even cycles in which the two kinds alternate. Lines L4 to L7 walk one such cycle and color it up, down, up, down, so every edge joins two colors, and the walk ends at its start. So each input switch sends one input to each half, and each output switch gets one cell from each half. Then $\pi_U$ and $\pi_L$ are permutations, and by induction the subnetworks realize them. A case check on lines L8 and L9 shows that each cell enters and leaves its half on the right lines. The full proof is in the correctness proof below. The tests check all $8! = 40320$ permutations of 8 lines and random permutations up to 4096 lines.

## Complexity

- **Time.** Each input is colored once, and lines L8 to L10 are linear, so $T(N) = 2T(N/2) + \Theta(N) = \Theta(N \log N)$ on the word RAM. This is constant time per switch, which is optimal for an algorithm that writes every setting.
- **Space.** The settings take $\Theta(N \log N)$ bits. The work arrays at one level take $\Theta(N)$ words.
- **Hardware.** $N \log_2 N - N/2$ switches in $2 \log_2 N - 1$ columns, against $N^2$ crosspoints in a crossbar. Every path has length $2 \log_2 N - 1$.
- **Parallel.** The loops are sequential walks, and a cycle can have length $N$, so the walk itself does not parallelize well. Parallel set-up needs other methods (see the variants).

## Properties

- **Rearrangeable, not strictly nonblocking.** Every permutation can be realized, but adding a connection to an existing set may require moving others.
- **Offline.** The whole permutation must be known before any switch is set.
- **Within $O(N)$ of optimal.** Any network of $s$ two-state switches has at most $2^s$ settings, so it needs $s \ge \log_2 N! = N \log_2 N - N \log_2 e + O(\log N)$ switches to realize all permutations.
- **Free choices.** Each cycle of the constraint graph can be colored in two ways. With $c$ cycles at the top level there are $2^c$ valid colorings, and the algorithm picks one.

## Variants and improvements

- **Waksman network.** The first loop always colors input 0 up, so input switch 0 is straight in every subnetwork. Replacing those switches by wires gives $N \log_2 N - N + 1$ switches.
- **Clos networks.** The Beneš network is a three-stage Clos network with $2 \times 2$ outer switches, applied recursively. Routing a general rearrangeable Clos network is an [edge coloring](/edge-coloring/) of a regular bipartite multigraph, and the looping algorithm is that coloring for degree 2.
- **Parallel set-up.** Nassimi and Sahni (1982) gave algorithms that set the switches on a parallel machine in polylogarithmic time, which matters when the permutation changes often.
- **Packet routing on butterflies.** Without global set-up, packets that follow paths of a butterfly or Beneš network can collide; [Valiant's](/valiant-routing/) random intermediate destinations are the packet-switched answer.

## When to use it

Use a Beneš network and the looping algorithm when one fixed permutation, or a short list of them, must be applied many times, so the set-up cost is paid once: data shuffles in a parallel computer, permutations in hardware for cryptographic circuits, and switching fabrics that are reconfigured rarely. When each packet must find its own path with no central controller, use a [sorting network](/sorting-network/) such as [bitonic sort](/bitonic-sort/) for self-routing, at a cost of $\Theta(N \log^2 N)$ comparators, or randomized packet routing.

## Pitfalls

- **Wrong partner in line L7.** The next input is the one bound for the *other output on the same output switch* as $y \oplus 1$, that is $\pi^{-1}(\pi(y \oplus 1) \oplus 1)$. Using $\pi(y) \oplus 1$ follows the wrong edge and breaks the alternation.
- **Inverse permutation confusion.** The network can be given as "input $x$ goes to output $\pi(x)$" or as "output $y$ takes input $\pi(y)$". Mixing the two realizes $\pi^{-1}$.
- **Wiring convention.** The proof depends on the rule that input switch $k$ feeds line $k$ of each subnetwork. With another wiring, such as the perfect shuffle of the butterfly drawing, the indices of $\pi_U$ and $\pi_L$ change.
- **Recursion in hardware.** The algorithm is fast on one processor, but each loop can be long, so a parallel controller needs a different method.

## Implementations

## History

Václav Beneš introduced the network in his work on telephone switching at Bell Labs and showed in 1964 that it is rearrangeable, as part of a mathematical theory of connecting networks published in book form in 1965. Abraham Waksman (1968) gave a permutation network with $N \log_2 N - N + 1$ switches and a routing method by loops. Opferman and Tsao-Wu (1971) described the looping algorithm for the Beneš network in the form used today. Nassimi and Sahni studied parallel set-up in the early 1980s. The network reappears in on-chip networks and in circuits for secure computation that must apply a secret permutation.

## References
