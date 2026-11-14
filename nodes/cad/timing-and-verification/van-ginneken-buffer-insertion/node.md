---
tag: 98230Y
kind: algorithm
slug: van-ginneken-buffer-insertion
name: Van Ginneken's buffer insertion
aliases:
- van Ginneken algorithm
- van Ginneken buffering
area: cad/timing-and-verification
level: core
summary: Places buffers on a routing tree to maximise slack at the source by dynamic programming over non-dominated pairs of load and required time, in O(n^2) time.
model: real-ram
complexity:
  vars: {n: "the number of nodes of the tree, sinks and candidate positions included", b: the number of buffer types}
  time: {one_buffer_type: O(n^2), b_types: O(b^2 n^2)}
  space: {extra: O(n^2)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1990
  people: [Lukas P. P. P. van Ginneken]
  note: Van Ginneken gave the algorithm at ISCAS 1990 for one buffer type and the Elmore delay. Lillis, Cheng and Lin extended it to a buffer library and to power in 1995 and 1996, and Shi and Li made it faster in 2003 and 2005.
prereqs: [elmore-delay, rc-tree, arrival-and-required-time, tree-dynamic-programming]
see_also: [static-timing-analysis, pareto-dominance, pareto-front, two-pointers, gate-sizing, rectilinear-steiner-arborescence, clock-tree-synthesis, nonlinear-delay-model]
sources:
  - paper: "Lukas P. P. P. van Ginneken, Buffer placement in distributed RC-tree networks for minimal Elmore delay, Proceedings of the IEEE International Symposium on Circuits and Systems (ISCAS) 1990, 865 to 868"
    locator: the bottom-up lists of load and required time, the pruning of dominated pairs, and the quadratic bound for one buffer type
  - paper: "John Lillis, Chung-Kuan Cheng and Ting-Ting Y. Lin, Optimal wire sizing and buffer insertion for low power and a generalized delay model, IEEE Journal of Solid-State Circuits 31(3), 437 to 447, 1996"
    locator: the extension to a library of buffer types, wire sizing and a power term
  - paper: doi:10.1109/TCAD.2005.847942
    title: Weiping Shi and Zhuo Li, A fast algorithm for optimal buffer insertion, IEEE Transactions on Computer-Aided Design 24(6), 879 to 891, 2005
    locator: the O(n log n) algorithm for 2-pin nets and the O(n log^2 n) algorithm for multi-pin nets, with balanced search trees for the candidate lists
  - paper: "Zhuo Li and Weiping Shi, An O(bn^2) time algorithm for optimal buffer insertion with b buffer types, IEEE Transactions on Computer-Aided Design 25(3), 484 to 489, 2006"
    locator: the improvement from O(b^2 n^2) to O(b n^2) for a library of b buffer types
  - book: isbn:9789048195909
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, Springer, 2011
    locator: Chapter 8, Timing Closure, Section 8.5.2, Buffering
  - book: isbn:9780849372421
    title: Charles J. Alpert, Dinesh P. Mehta and Sachin S. Sapatnekar (editors), Handbook of Algorithms for Physical Design Automation, CRC Press, 2008
    locator: Chapter 26, Buffer Insertion Basics, by Jiang Hu, Zhuo Li and Shiyan Hu
---

Van Ginneken's algorithm chooses where to put buffers on a fixed routing tree of a net so that the slack at the source is as large as possible, with the [Elmore delay](/elmore-delay/) on an [RC interconnect tree](/rc-tree/) as the delay model. It is a [dynamic program on the tree](/tree-dynamic-programming/): each node keeps a list of the pairs (load capacitance, [required time](/arrival-and-required-time/)) that some buffer choice below it can give, and drops every pair that another pair beats on both counts. Lukas van Ginneken published it in 1990. For one buffer type it is exact and takes $O(n^2)$ time, where $n$ counts the sinks and the candidate positions.

## In plain words

A long wire is slow, because its resistance must charge its own capacitance and everything behind it. A buffer cuts the wire in two: the gate before it sees only the small input of the buffer, and the buffer drives the rest. But each buffer adds its own delay, so the places must be chosen well.

Work from the sinks back to the source. At each point, keep a short list of options. Each option says how heavy the load is when you look down from this point, and how late the signal may arrive here so that every sink below is still on time. If one option is worse than another in both ways, throw it away. Moving up a wire, joining two branches and adding a buffer are simple rules on these lists. At the source, pick the best option.

## The problem

The input is a rooted tree. The root $0$ is the source, driven by a gate with resistance $R_d$ and intrinsic delay $D_d$. Every other node $v$ has a wire to its parent with resistance $R_v \ge 0$ and capacitance $W_v \ge 0$, in the pi model, with half of $W_v$ at each end. The leaves are the sinks: sink $s$ has load $c_s$ and required time $q_s$. A set of candidate nodes may take a buffer of type $b$, with input capacitance $C_b$, output resistance $R_b$ and intrinsic delay $D_b$. A buffer at $v$ drives the subtree of $v$, and its input is a load at $v$ for the stage above. The output is a placement of buffers that maximizes the slack at the source,
$$ \text{slack} = \min_{s} \,(q_s - a_s), $$
where the arrival time $a_s$ is the sum of the Elmore delays and the intrinsic delays of the stages on the path to $s$, with the input of the driver at time 0.

A *candidate* at a node $v$ is a pair $(c, q)$: the load seen from $v$ into its subtree, and the latest arrival time at $v$ that meets all sinks below. The pair $(c, q)$ *dominates* $(c', q')$ when $c \le c'$ and $q \ge q'$, the [Pareto dominance](/pareto-dominance/) order with one quantity to make small and one to make large.

## The algorithm

```pseudo id=main
VAN-GINNEKEN(T)
L1  for each node v of T in post-order do
L2      if v is a sink then L(v) ← [(c_v, q_v)]
L3      else
L4          L(v) ← nothing
L5          for each child u of v do
L6              M ← [(c + W_u, q − R_u (W_u / 2 + c)) for (c, q) in L(u)];  PRUNE(M)
L7              if L(v) is nothing then L(v) ← M else L(v) ← JOIN(L(v), M)
L8          if v is a candidate node then
L9              for each buffer type b do add (C_b, max over (c, q) in L(v) of q − D_b − R_b c) to L(v)
L10             PRUNE(L(v))
L11 return the largest q − D_d − R_d c over (c, q) in L(0)

JOIN(A, B)                         ▷ A and B sorted by load, without dominated pairs
J1  i ← 1;  j ← 1;  O ← empty list
J2  while i ≤ |A| and j ≤ |B| do
J3      append (A[i].c + B[j].c, min(A[i].q, B[j].q)) to O
J4      if A[i].q < B[j].q then i ← i + 1
J5      else if B[j].q < A[i].q then j ← j + 1
J6      else i ← i + 1;  j ← j + 1
J7  PRUNE(O);  return O
```

PRUNE sorts by load when needed and keeps a pair only if its required time is larger than that of every pair with a load no larger. After PRUNE the loads and the required times both increase strictly along the list. Line L6 is the wire rule, line L9 the buffer rule and JOIN the rule at a branch. Each pair also keeps a record of the buffers that make it, so the placement is read back from the best pair at the end.

## Example

The tree has the source $0$, a path $0 - 1 - 2$, and two branches at node $2$: one to sink $3$, and one through node $4$ to sink $5$. The wires into $1, 2, 3, 4, 5$ have resistances $2, 1, 1, 2, 2$ and every wire has capacitance $2$. The sinks have load 1, with $q_3 = 40$ and $q_5 = 60$. Nodes 1, 2 and 4 are candidates for one buffer type with $C_b = 1$, $R_b = 1$, $D_b = 2$. The driver has $R_d = 3$ and $D_d = 0$. Pairs are written (load, required time).

| step | list |
| --- | --- |
| sink 5 | (1, 60) |
| up the wire into 5 | (3, 56) |
| buffer at 4 | (1, 51), (3, 56) |
| up the wire into 4 | (3, 47), (5, 48) |
| sink 3, up the wire into 3 | (3, 38) |
| join at 2 | (6, 38) |
| buffer at 2 | (1, 30), (6, 38) |
| up the wire into 2 | (3, 28), (8, 31) |
| buffer at 1 | (1, 23), (3, 28), (8, 31) |
| up the wire into 1 | (3, 19), (5, 20) |

The join at node 2 makes only one pair. The branch of sink 3 has the smaller required time, 38, so the pointer on that side leaves its list after one step, and the branch of node 4 gives its lightest pair, (3, 47), which is enough to meet 38. The last wire turns (8, 31) into (10, 13), which (5, 20) dominates, so PRUNE drops it. At the source the slacks are $19 - 3 \cdot 3 = 10$ and $20 - 3 \cdot 5 = 5$. The best slack is 10, with buffers at 1, 2 and 4. Without buffers the slack is $-29$. The eight placements of buffers on the three candidates give slacks $-29, 4, 3, -17, 8, 5, 8, 10$, so 10 is the optimum.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Its key fact is that the part of the tree above a node sees the subtree below only through the pair (load, required time) of that subtree: the slack of the whole net is a nonincreasing function of the load and a nondecreasing function of the required time, because every Elmore delay outside the subtree is a linear function of the load with a nonnegative coefficient. So a dominated pair can never be part of a better solution, and the three rules (wire, buffer, join) map dominating pairs to dominating pairs. The join needs care: for any two pairs of the two branches, the two pointer loop reaches a pair of indices that is no heavier and has the same or a larger minimum required time.

## Complexity

With one buffer type, the list at a node has at most as many pairs as there are sinks and candidate nodes below it. A sink gives one pair, a buffer adds one pair, a wire never adds a pair, and the join of lists of lengths $k_1$ and $k_2$ makes at most $k_1 + k_2 - 1$ pairs, since each step of the loop moves a pointer. Every rule takes time linear in the lengths of the lists it reads, so the work at a node is $O(n)$ and the total is $O(n^2)$ in the worst case. The records of the pairs take $O(n^2)$ space in the worst case. With $b$ buffer types the list can grow by $b$ pairs at each candidate, and the bound of Lillis, Cheng and Lin is $O(b^2 n^2)$.

## Properties

- Exact for the given tree, the given candidate positions and the Elmore delay with the pi model of wires. It does not move the wires or add new candidate positions.
- Deterministic. The best slack does not depend on the order of the children at a node, but the placement that reaches it can, when two placements tie.
- The pruning stays valid for other delay models in which the rest of the net sees a subtree only through its load and its required time, and in which a heavier load never helps. Lillis, Cheng and Lin use such a generalized model. The table based [nonlinear delay model](/nonlinear-delay-model/) does not fit, because a stage delay there also depends on the input slew.
- The value at the source is the slack of the net with the arrival time of the driver input at 0. For a net inside a circuit, the required times of the sinks come from [static timing analysis](/static-timing-analysis/).

## Variants and improvements

- **Buffer library and power.** Lillis, Cheng and Lin allow $b$ buffer types, wire sizing, and a power term as a third value in each candidate, so that the lists hold the triples that no other triple beats on all three counts.
- **Faster lists.** Shi and Li keep the candidates in balanced search trees and add the effect of a wire lazily, which gives $O(n \log n)$ for a 2-pin net and $O(n \log^2 n)$ for a net with many sinks, for one buffer type. Li and Shi lowered the library bound from $O(b^2 n^2)$ to $O(b n^2)$.
- **Load limits.** A limit on the load that one stage may drive is a simple extra rule: drop every pair whose load is above the limit before a buffer or the driver must drive it. The dominance argument still holds, since the rule removes only heavy pairs.

## When to use it

Use it to buffer one net whose route is fixed, with a small buffer library and a few hundred candidate positions, for example after routing a long net or during timing closure. It is exact for the model, so it is also the reference that faster heuristics are compared with. For a clock net, where the aim is equal delays rather than the best slack, the zero-skew methods of [clock tree synthesis](/clock-tree-synthesis/) are the right tool. For very large nets with many sinks, the $O(n \log^2 n)$ variant of Shi and Li is faster.

## Pitfalls

- After a wire, a pair can become dominated, since the wire takes more time from a pair with a heavier load. PRUNE must run after the wire rule, not only after a join.
- The buffer rule takes the largest value of $q - D_b - R_b c$ over the whole list. The pair with the largest required time is not always the best, because a heavy load costs time through the buffer resistance.
- The join loop must advance the pointer of the smaller required time. Advancing the other pointer loses pairs that can be optimal.
- The result is optimal only for the candidate positions given. A long wire with no candidate node inside it cannot get a buffer, so split long wires into short segments first.
- The Elmore delay is an upper bound on the 50 percent delay of an RC tree, not the delay itself. The slack is exact for the model, not for the circuit.
- Floating point ties make the dominance test unstable. Two pairs that differ by rounding both survive, and the lists grow. Exact or carefully rounded arithmetic avoids it.

## Implementations

## History

Van Ginneken presented the algorithm at ISCAS 1990, for one buffer type, a fixed routing tree and the Elmore delay. Lillis, Cheng and Lin extended it to a buffer library, wire sizing and power at ICCAD 1995 and in the IEEE Journal of Solid-State Circuits in 1996. Shi and Li gave the $O(n \log n)$ and $O(n \log^2 n)$ versions at DAC 2003 and in IEEE Transactions on Computer-Aided Design in 2005, and Li and Shi gave the $O(b n^2)$ library bound in 2006. The method is the basis of the buffering step of physical synthesis in the textbook of Kahng, Lienig, Markov and Hu.

## References
