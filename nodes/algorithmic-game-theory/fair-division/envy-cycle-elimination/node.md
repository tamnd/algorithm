---
tag: 0PA93X
kind: algorithm
slug: envy-cycle-elimination
name: Envy-cycle elimination
aliases:
- Lipton-Markakis-Mossel-Saberi algorithm
area: algorithmic-game-theory/fair-division
level: core
summary: Gives each good to an agent no one envies, rotating bundles along envy cycles to create one. It returns an EF1 allocation for monotone valuations.
model: word-ram
complexity:
  vars: {n: the number of agents, m: the number of goods}
  time: {worst: O(m n^3)}
  space: {extra: O(n^2 + m)}
properties: {deterministic: true, recursive: false, online: false}
prereqs: [envy-freeness-up-to-one-good, cycle-detection]
see_also: [round-robin-allocation, envy-freeness-up-to-any-good, efx-existence-for-three-agents, indivisible-goods-allocation, submodular-function, depth-first-search, greedy-algorithm]
sources:
  - paper: "Richard J. Lipton, Evangelos Markakis, Elchanan Mossel and Amin Saberi, On approximately fair allocations of indivisible goods, Proceedings of the 5th ACM Conference on Electronic Commerce (EC 2004), 125-131"
    locator: the envy-graph algorithm and its bound on envy by the largest marginal value of a single good
  - paper: doi:10.1145/3616009
    title: "Bhaskar Ray Chaudhury, Jugal Garg and Kurt Mehlhorn, EFX exists for three agents, Journal of the ACM 71(1) (2024), 1-27 (conference version EC 2020; arXiv:2002.05119)"
    locator: Fact 5 (the envy graph can be made acyclic, after Lipton et al.)
---

Envy-cycle elimination gives indivisible goods to agents one at a time, always to an agent that nobody envies. If every agent is envied, the envy graph has a cycle, and the bundles move one step along the cycle, which makes every agent on it better off and removes envy edges; then some agent is unenvied. Lipton, Markakis, Mossel and Saberi gave it in 2004. For every monotone valuation, not only additive ones, the output is [envy-free up to one good](/envy-freeness-up-to-one-good/) (EF1), and it uses $O(m n^3)$ value queries. This makes it the standard way to get EF1 beyond additive valuations, where [round-robin allocation](/round-robin-allocation/) can fail.

## In plain words

Goods arrive one by one. Each new good goes to a person whom nobody envies. Then nobody can complain much about that person: before the gift, nobody wanted that person's share, so after the gift the envy is about one good at most.

Sometimes everybody is envied by somebody. Follow the envy from person to person and you come back to where you started: Ann wants Bob's share, Bob wants Cid's share, and Cid wants Ann's share. Pass the shares around the circle so that each of them gets the share they wanted. Everyone on the circle is now happier, and nobody else notices any change. Repeat until someone is unenvied, and give the good to that person.

## The problem

There are $n$ agents and $m$ indivisible goods $g_1, \dots, g_m$. Agent $i$ has a valuation $v_i$ on sets of goods with $v_i(\emptyset) = 0$, given by a value oracle. The valuations are monotone: $S \subseteq T$ implies $v_i(S) \le v_i(T)$. The goal is an EF1 allocation $A = (A_1, \dots, A_n)$ of all goods: for all agents $i, j$ with $A_j \ne \emptyset$, some $g \in A_j$ has $v_i(A_i) \ge v_i(A_j \setminus \{g\})$.

The **envy graph** of a partial allocation has the agents as vertices and an edge $i \to j$ when $v_i(A_j) > v_i(A_i)$.

## The algorithm

```pseudo id=main
ENVY-CYCLE-ELIMINATION(v_1, ..., v_n, g_1, ..., g_m)   ▷ monotone valuations, value oracle
L1  A_i ← ∅ for every agent i
L2  for each good g in the order g_1, ..., g_m do
L3      G ← the envy graph of A
L4      while every agent has an incoming edge in G do
L5          C ← a cycle c_0, c_1, ..., c_(k-1) of G in which c_(t+1) envies c_t (indices mod k)
L6          give the bundle A_(c_t) to agent c_(t+1) for every t
L7          G ← the envy graph of the new A
L8      i ← the agent of smallest index with no incoming edge in G
L9      A_i ← A_i ∪ {g}
L10 return A
```

Line L4 tests for a source of the envy graph. When there is none, every vertex has an incoming edge, so walking backward along incoming edges must repeat a vertex, and line L5 finds a cycle in $O(n^2)$ time, as in [cycle detection](/cycle-detection/). Line L6 hands each envied bundle on the cycle to the agent that envies it. Line L8 breaks ties by index. The allocation is partial until the last good.

## Example

Three agents value five goods $a, \dots, e$ additively:

| | $a$ | $b$ | $c$ | $d$ | $e$ |
|---|---|---|---|---|---|
| agent 1 | 5 | 6 | 9 | 1 | 8 |
| agent 2 | 4 | 1 | 3 | 2 | 6 |
| agent 3 | 8 | 4 | 7 | 9 | 2 |

1. Good $a$: nobody envies anybody, so agent 1 gets $a$.
2. Good $b$: agents 2 and 3 envy agent 1, so agent 2, the first unenvied agent, gets $b$.
3. Good $c$: agent 3 has nothing and is unenvied, so it gets $c$. Now $A = (\{a\}, \{b\}, \{c\})$.
4. Good $d$: agent 1 envies 2 and 3 (values 6 and 9 against 5), agent 2 envies 1 and 3 (4 and 3 against 1), and agent 3 envies 1 (8 against 7). Every agent is envied. Line L5 finds the cycle of agents 1 and 2, which envy each other, and line L6 swaps their bundles: $A = (\{b\}, \{a\}, \{c\})$. Now nobody envies agent 1, which values $\{b\}$ at 6, so agent 1 gets $d$: $A = (\{b, d\}, \{a\}, \{c\})$.
5. Good $e$: agent 1 envies 3 (9 against 7), agent 3 envies 1 and 2 (13 and 8 against 7), and agent 2 envies nobody. Every agent is envied again. Agents 1 and 3 envy each other, so they swap: $A = (\{c\}, \{a\}, \{b, d\})$. Now nobody envies anybody, and agent 1 gets $e$.

The output is $A_1 = \{c, e\}$, $A_2 = \{a\}$, $A_3 = \{b, d\}$, worth 17, 4 and 13 to their owners, after 2 rotations. Agent 2 values $\{c, e\}$ at 9; without $e$ it is worth $3 \le 4$, so the envy is within EF1.

## Correctness

The partial allocation is EF1 before every step. A rotation in line L6 keeps the same bundles and gives each agent on the cycle a bundle it strictly prefers, while the others keep theirs; the EF1 test of an agent against a bundle only gets easier when its own value rises. Line L9 gives $g$ to an agent $i$ that nobody envies, so for every other agent $k$, $v_k((A_i \cup \{g\}) \setminus \{g\}) = v_k(A_i) \le v_k(A_k)$, and removing $g$ meets EF1. The loop of line L4 stops because each rotation removes at least two edges from the envy graph, while each new good adds at most $n - 1$. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

Count the edges of the envy graph. Line L9 can add only edges into $i$, at most $n - 1$, and cannot add edges out of $i$, because $v_i$ is monotone. A rotation over a cycle of $k \ge 2$ agents keeps the out-degree of every agent off the cycle and lowers the out-degree of every agent on it by at least 1, so it removes at least 2 edges. Hence the whole run makes at most $m(n - 1)/2$ rotations. Each envy graph costs $n^2$ value queries and $O(n^2)$ time; with $m$ graphs in line L3 and one per rotation in line L7, the run uses $O(m n^3)$ value queries and $O(m n^3)$ other steps. The extra space is $O(n^2)$ for the graph plus the bundles.

## Properties

- **EF1 for monotone valuations.** For any monotone valuations, not only additive ones.
- **Envy bounded by one marginal value.** The proof gives more: when $i$ envies the owner of a bundle $B$, the envy $v_i(B) - v_i(A_i)$ is at most the marginal value $v_i(B) - v_i(B \setminus \{g\})$ of the last good $g$ that joined $B$. This is the form of the guarantee in Lipton et al.
- **Not Pareto optimal.** The rule ignores efficiency. For two agents and goods worth $(1, 0)$ and $(0, 1)$, the order $g_2, g_1$ gives $g_2$ to agent 1; then agent 2 is unenvied (agent 1 values its own good at 0 and the empty bundle at 0) and gets $g_1$, and both agents have 0 while the swap would give both 1.
- **No rotations with identical valuations.** With one common valuation, an edge $i \to j$ means $v(A_j) > v(A_i)$, so the envy graph has no cycle and line L4 never loops.
- **The order of the goods matters.** It changes the output, but not the guarantee.

## Variants and improvements

- **Goods in decreasing order.** For identical additive valuations, giving the goods in decreasing order of value makes line L8 choose a bundle of least value, which gives an [EFX](/envy-freeness-up-to-any-good/) allocation; the EFX page has the proof.
- **Making the envy graph acyclic.** The rotations of lines L4 to L7, run until no cycle is left, turn any allocation into one with an acyclic envy graph and with every agent at least as well off. The EFX algorithms of Chaudhury, Garg and Mehlhorn use this step (Fact 5 in their paper), as on the [EFX existence for three agents](/efx-existence-for-three-agents/) page.
- **Additive valuations.** [Round-robin allocation](/round-robin-allocation/) is simpler and faster, at $O(n m \log m)$ time.

## When to use it

Use it when valuations are monotone but not additive, such as [submodular](/submodular-function/) or coverage valuations, and EF1 is the goal; it needs only a value oracle. Use it also when goods are handed out one at a time and the partial allocation must stay EF1 after each good. For additive valuations, round-robin is enough.

## Pitfalls

- **Giving the good to any agent.** If line L8 picks an envied agent, the new good adds to a bundle that someone already prefers to its own, and EF1 can fail after one more good. The receiver must have no incoming edge.
- **Rotating in the wrong direction.** In line L6 each agent $c_{t+1}$ must receive the bundle of the agent $c_t$ that it envies. Moving bundles the other way lowers values and can break EF1.
- **Not rebuilding the graph.** Line L7 must recompute the envy graph after a rotation, because every edge out of a cycle agent can change. Reusing the old graph can rotate along a cycle that no longer exists.
- **Non-monotone valuations.** The step in line L9 uses $v_i(A_i \cup \{g\}) \ge v_i(A_i)$. If adding a good can lower a value, the receiver may start to envy others beyond one good, and the output can fail EF1.

## Implementations

## History

Lipton, Markakis, Mossel and Saberi introduced the envy graph and its cycle rotations at EC 2004, with the guarantee that envy is at most the largest marginal value of one good. The same envy-graph step is a building block of later EFX algorithms, such as the one for three agents by Chaudhury, Garg and Mehlhorn.

## References
