---
tag: R8HB82
kind: algorithm
slug: mustang-state-assignment
name: MUSTANG state assignment
aliases:
- MUSTANG
- fanin and fanout oriented state assignment
area: eda/high-level-synthesis-and-scheduling
level: advanced
summary: Devadas, Ma, Newton and Sangiovanni-Vincentelli's encoder that gives close codes to states with common fanin or fanout to help multi-level logic sharing.
solves: [state-assignment]
model: word-ram
complexity:
  vars: {n: the number of states, R: the number of rows of the state table, o: the number of primary outputs}
  time: {worst: O(R o + n^2 (n + o + R))}
  space: {extra: O(n^2 + R)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1988
  people: [Srinivas Devadas, Hi-Keung Tony Ma, A. Richard Newton, Alberto L. Sangiovanni-Vincentelli]
  note: Devadas, Ma, Newton and Sangiovanni-Vincentelli published MUSTANG in IEEE Transactions on Computer-Aided Design in 1988, with fanout and fanin oriented attraction weights between states and a cube embedding that keeps heavy pairs close, aimed at multilevel logic.
prereqs: [state-assignment, hamming-distance]
see_also: [kiss-symbolic-minimization, nova-state-encoding, espresso, dfa-minimization, incompletely-specified-fsm-minimization, quadratic-assignment-problem, fsm-decomposition, partition-pair]
sources:
  - paper: doi:10.1109/43.16807
    title: Srinivas Devadas, Hi-Keung Tony Ma, A. Richard Newton and Alberto L. Sangiovanni-Vincentelli, MUSTANG, state assignment of finite state machines targeting multilevel logic implementations, IEEE Transactions on Computer-Aided Design 7(12), 1290 to 1300, 1988
    locator: the fanout and fanin oriented weight graphs, the embedding algorithm, and the literal counts measured on benchmark machines
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 9 (state encoding for multiple-level circuits)
  - paper: "Giovanni De Micheli, Robert K. Brayton and Alberto L. Sangiovanni-Vincentelli, Optimal state assignment for finite state machines, IEEE Transactions on Computer-Aided Design CAD-4(3), 269 to 285, 1985"
    title: Giovanni De Micheli, Robert K. Brayton and Alberto L. Sangiovanni-Vincentelli, Optimal state assignment for finite state machines, IEEE Transactions on Computer-Aided Design CAD-4(3), 269 to 285, 1985
    locator: the two-level encoding method (KISS) that MUSTANG compares with
---

MUSTANG is a method of [state assignment](/state-assignment/) for finite state machines whose logic is built as a multilevel network rather than a PLA. Its idea is that two states should get codes at a small [Hamming distance](/hamming-distance/) when their logic has something to share. In the fanout oriented mode, present states that go to the same next states or assert the same outputs attract each other, so that the product terms for them can merge or share a common factor. In the fanin oriented mode, next states that are reached from the same present states or under the same inputs attract each other. The weights form a graph on the states, and a greedy embedding places the states on the corners of the code cube one at a time, keeping heavy pairs close. Devadas, Ma, Newton and Sangiovanni-Vincentelli published it in 1988. The only thing this page proves is that the codes are valid. The rest is measured, and an exhaustive search over the codes shows that MUSTANG is not optimal for the final logic: on the example, the fanout code gives the most expensive two-level logic of all twelve classes of two-bit codes.

## In plain words

A code is a string of bits for each state. Codes that differ in few bits make logic that can share parts. MUSTANG counts, for each pair of states, how much their rows of the table have in common: the same next state, the same output, the same source state or the same input. A large count means the pair should get codes that differ in few bits. It then puts the states on the corners of a cube, one by one. Each time, it takes the state most tied to the states already placed, and puts it on the free corner nearest to them, counting the ties.

## The problem

The input is a reduced finite state machine with $n$ states, given as a table of rows (input, present state, next state, output), and a code length $k$, by default $\lceil \log_2 n \rceil$. The output is an injective code $\mathrm{enc}$ from the states to $\{0, 1\}^k$. The aim is small multilevel logic for the encoded next-state and output functions. That cost depends on the multilevel optimizer, so MUSTANG works on a proxy: for a weight $w(s, t) \ge 0$ on each pair of states, it tries to make the embedding cost
$$\sum_{\{s, t\}} w(s, t)\, d_H(\mathrm{enc}(s), \mathrm{enc}(t))$$
small, where $d_H$ is the Hamming distance. Minimizing this cost over injective codes is a [quadratic assignment problem](/quadratic-assignment-problem/) on the corners of the cube. MUSTANG does not solve it exactly.

## The algorithm

This page uses simplified weights. For states $s, t$, let $a(s, u)$ be the number of rows from present state $s$ to next state $u$, $b(s, j)$ the number of rows of $s$ that assert output $j$, $c(p, s)$ the number of rows from $p$ to $s$, and $d(x, s)$ the number of rows with input $x$ that go to $s$. A shared next state counts $k$ times because all $k$ of its code bits are shared.

```pseudo id=main
MUSTANG(M, mode)
L1  k ← ⌈log2 n⌉
L2  if mode = fanout then w(s, t) ← k · Σ_u a(s, u) a(t, u) + Σ_j b(s, j) b(t, j) for each pair of states
L3  else w(s, t) ← k · Σ_p c(p, s) c(p, t) + Σ_x d(x, s) d(x, t) for each pair of states
L4  enc ← empty
L5  while some state is not placed do
L6      s ← the unplaced state with the largest total weight to the placed states; ties to the largest total weight to all states, then to the first state
L7      enc(s) ← the free corner c with the least Σ over placed t of w(s, t) · d_H(c, enc(t)); ties to the smallest c
L8  return enc
```

The weights of the paper are more detailed than lines L2 and L3; they were not checked against the paper here, and the forms above keep only the two ideas, fanout and fanin. The paper also has more than one embedding method. The greedy of lines L5 to L7 is a simple one in the same spirit.

## Example

Take the machine $M_1$ of the [KISS](/kiss-symbolic-minimization/) page, with one input $x$, one output $z$ and four states:

| present | $x = 0$ | $x = 1$ |
| --- | --- | --- |
| $s_0$ | $s_2$ / 1 | $s_2$ / 0 |
| $s_1$ | $s_2$ / 0 | $s_2$ / 1 |
| $s_2$ | $s_3$ / 0 | $s_1$ / 1 |
| $s_3$ | $s_1$ / 1 | $s_3$ / 0 |

**Fanout weights** ($k = 2$). The states $s_0$ and $s_1$ both go to $s_2$ twice, which gives $2 \cdot 4 = 8$, and both assert $z$ once, which gives 1, so $w(s_0, s_1) = 9$. The states $s_2$ and $s_3$ share the next states $s_1$ and $s_3$ once each and $z$ once, so $w(s_2, s_3) = 2 \cdot 2 + 1 = 5$. Every other pair shares only $z$ and has weight 1.

The greedy starts with $s_0$, whose total weight 11 ties with $s_1$, at corner $00$. Then $s_1$, tied to $s_0$ by 9, goes to $01$. Then $s_2$ goes to $10$ (corners $10$ and $11$ tie at 3), and $s_3$ to $11$. The embedding cost is $9 + 1 + 2 + 2 + 1 + 5 = 20$, which equals the least cost over all 24 codes. So the greedy solves its own problem exactly here.

**Fanin weights.** The state $s_0$ is never a next state, so all its weights are 0. The pair $s_1, s_3$ is reached from $s_2$ and from $s_3$, which gives $2 \cdot 2 = 4$, and under each input once, which gives 2, so $w(s_1, s_3) = 6$. The pairs $s_1, s_2$ and $s_2, s_3$ share only inputs and get weight 4 each. The greedy gives $s_1 = 00$, $s_3 = 01$, $s_2 = 10$, $s_0 = 11$, with embedding cost 18, again the least possible.

**The final logic.** An exact two-level minimization, with the unused codes as don't cares, gives these costs over the 12 classes of two-bit codes (24 codes up to swapping the bits), in cubes and literals:

| code | cubes | literals |
| --- | --- | --- |
| best of the 12 classes ($s_0 = 01$, $s_1 = 10$, $s_2 = 11$, $s_3 = 00$) | 4 | 8 |
| MUSTANG, fanin | 6 | 14 |
| MUSTANG, fanout | 7 | 19 |
| worst of the 12 classes | 7 | 19 |

The fanout code, optimal for its embedding cost, gives the worst two-level logic of all. The best code puts $s_0$ and $s_1$ at distance 2, the opposite of what their weight asks. The reason is visible in the table: $s_0$ and $s_1$ share their next state, but they assert $z$ under opposite inputs, and the weights do not see which input a shared output belongs to. Two-level cost is only a proxy for the multilevel logic that MUSTANG aims at, and the multilevel cost is not measured here. But the example shows that a small embedding cost does not ensure small logic.

## Correctness

The [full proof](proofs/correctness.md) shows that the loop stops after $n$ rounds, and that the result is an injective code of $k$ bits: each round places one new state on a free corner, and a free corner exists because $2^k \ge n$. That is all that is proved. The weights are a heuristic, the greedy embedding need not minimize the embedding cost, and the embedding cost need not track the logic.

All other claims are measurements. On 100 random machines with 4 states, one input bit and one output bit, every entry specified (seed 1988), the greedy reached the least embedding cost on 84 machines in the fanout mode and on 87 in the fanin mode. The exact two-level logic matched the best two-bit code on 33 machines (fanout), 47 (fanin) and 57 (the better of the two), with 87, 68 and 47 extra cubes in total, and the better of the two lost at most 2 cubes on one machine. On 8 random weight graphs on 5 states with 3 bits (seed 7), the greedy reached the least embedding cost on 6. The two-level cube count is a proxy, chosen because it can be computed exactly on small machines. MUSTANG targets multilevel logic, and the paper measures literal counts after multilevel optimization on benchmark machines.

## Complexity

Lines L2 and L3 count the rows in $O(R o)$ time and then compute $O(n^2)$ pair weights, each in $O(n + o)$ time for fanout and $O(n + R)$ for fanin. In the loop, line L6 takes $O(n^2)$ time per round with running sums or $O(n)$ per candidate, and line L7 tries at most $2^k < 2n$ corners with $O(n)$ work each. Over $n$ rounds this is $O(n^3)$. The total is $O(R o + n^2 (n + o + R))$ time and $O(n^2 + R)$ space for the weights and the counts. The multilevel optimization that follows, and that decides the real cost, is not counted.

## Properties

- **Valid codes.** The codes are injective, of the requested length.
- **Not optimal.** Neither the embedding cost nor the final logic is minimized. On the example the fanout code gives the worst two-level logic of all codes. None of [KISS](/kiss-symbolic-minimization/), [NOVA](/nova-state-encoding/) and MUSTANG is optimal for the final logic: on the example machines of the three pages, an exhaustive search over all codes finds cheaper logic than each of them gives.
- **Two modes.** Fanout weights aim at sharing in the logic that reads the present state. Fanin weights aim at sharing in the next-state logic. Running both and keeping the better result costs twice the time, and on the measured machines it matched the best code more often than either mode alone.
- **Fast.** The method is polynomial, with no two-level minimization in the loop, unlike [KISS](/kiss-symbolic-minimization/) and [NOVA](/nova-state-encoding/).
- **Deterministic.** The tie rules fix the result.

## Variants and improvements

- **Better embeddings.** Any heuristic for the quadratic assignment problem on the hypercube, such as local search with swaps of two codes, can replace lines L5 to L7.
- **Longer codes.** More bits give more room to place heavy pairs at distance 1, at the cost of more flip-flops.
- **Two-level targets.** For a PLA, [KISS](/kiss-symbolic-minimization/) and [NOVA](/nova-state-encoding/) use face constraints from symbolic minimization, which see the inputs under which rows agree.
- **Later encoders.** De Micheli's book (Chapter 9) describes encodings for multilevel logic that use symbolic factoring rather than pairwise weights.

## When to use it

Use MUSTANG when the controller will be built as multilevel logic and the machine is too large for methods that run a minimizer for each candidate code. Try both modes and keep the better result after multilevel optimization. For small machines, an exhaustive search over codes with the real cost measure is better, and it shows how far the weights are from the logic.

## Pitfalls

- **Taking the embedding cost as the cost.** The example has the least embedding cost and the worst logic.
- **Unreduced machines.** Equivalent states attract each other strongly, and they waste code space. Reduce the machine first with [DFA minimization](/dfa-minimization/) or [incompletely specified FSM minimization](/incompletely-specified-fsm-minimization/).
- **Ties.** Small machines have many equal weights, so the tie rules decide much of the result.
- **Measuring with the wrong cost.** MUSTANG aims at multilevel logic. A two-level result after [Espresso](/espresso/) says little about the multilevel result, and the reverse.
- **Input values.** The weights of lines L2 and L3 count shared outputs and next states without asking under which inputs they occur, which is how the example goes wrong.

## Implementations

## History

De Micheli, Brayton and Sangiovanni-Vincentelli (1985) gave KISS for two-level logic. Devadas, Ma, Newton and Sangiovanni-Vincentelli (1988) gave MUSTANG for multilevel logic, with fanout and fanin oriented weight graphs and an embedding into the code cube, and reported literal counts after multilevel optimization on a set of benchmark machines, a measurement rather than a bound. Villa and Sangiovanni-Vincentelli (1990) returned to the two-level case with NOVA. De Micheli's 1994 textbook surveys the two-level and multilevel encoders together.

## References
