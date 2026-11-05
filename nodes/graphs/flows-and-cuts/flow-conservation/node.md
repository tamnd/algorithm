---
tag: PHKC70
kind: definition
slug: flow-conservation
name: Flow conservation
aliases:
- conservation constraint
area: graphs/flows-and-cuts
level: intro
summary: At every vertex other than s and t, incoming flow equals outgoing flow.
prereqs: [flow-network]
see_also: [s-t-flow, cut, cut-capacity, flow-decomposition, circulation-problem, preflow, max-flow-problem]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 24.1, Flow networks (the capacity constraint and flow conservation), and Section 24.2 (the net flow across a cut equals the value of the flow)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 7.1 (the conservation conditions) and Section 7.2 (the flow across a cut)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 10, Maximum Flows and Minimum Cuts, Section 10.2 (flows, the conservation constraint and the value of a flow)
---

Flow conservation is the rule that, at each vertex other than the source $s$ and the sink $t$ of a [flow network](/flow-network/), the flow that enters the vertex equals the flow that leaves it. Together with the capacity constraint it defines an [s-t flow](/s-t-flow/). It is what makes the flow behave like a physical flow of water or goods: nothing is created or lost on the way, so the amount that leaves $s$ is the amount that arrives at $t$, and it is the amount that crosses every [cut](/cut/).

## Definition

Let $N = (G, c, s, t)$ be a flow network with $G = (V, E)$, and let $f : E \to \mathbb{R}$ assign a value to each edge. For a vertex $v$ write

$$f^{\text{in}}(v) = \sum_{(u, v) \in E} f(u, v), \qquad f^{\text{out}}(v) = \sum_{(v, w) \in E} f(v, w), \qquad \operatorname{exc}_f(v) = f^{\text{in}}(v) - f^{\text{out}}(v).$$

The number $\operatorname{exc}_f(v)$ is the **excess** (or net inflow) of $v$. The function $f$ satisfies **flow conservation** if

$$\operatorname{exc}_f(v) = 0 \qquad \text{for each } v \in V \setminus \{s, t\}.$$

In words: for each vertex other than $s$ and $t$, the sum over the edges into $v$ equals the sum over the edges out of $v$. Edges are counted with multiplicity, so parallel edges each count, and a self-loop $(v, v)$ adds the same amount to both sums and so never changes $\operatorname{exc}_f(v)$. An antiparallel pair $(u, v), (v, u)$ is two separate edges: $f(u, v)$ counts in $f^{\text{out}}(u)$ and $f(v, u)$ counts in $f^{\text{in}}(u)$.

**Value.** The value of $f$ is $|f| = f^{\text{out}}(s) - f^{\text{in}}(s)$, the net flow out of $s$.

**The excess of the terminals.** Summing the excesses over all vertices counts each edge once with $+$ (at its head) and once with $-$ (at its tail), so

$$\sum_{v \in V} \operatorname{exc}_f(v) = 0.$$

Under conservation all terms vanish except two, so $\operatorname{exc}_f(t) = -\operatorname{exc}_f(s) = |f|$: the net flow into $t$ equals the net flow out of $s$.

**Flow across a cut.** For a set $S \subseteq V$ write $f(S, \bar S)$ for the total flow on edges from $S$ to $\bar S = V \setminus S$, and $f(\bar S, S)$ for the reverse. Summing the excess over $S$, each edge with both ends in $S$ cancels, so

$$\sum_{v \in S} \operatorname{exc}_f(v) = f(\bar S, S) - f(S, \bar S).$$

If $f$ satisfies conservation, $s \in S$ and $t \notin S$, the left side is $\operatorname{exc}_f(s) = -|f|$. Hence $f(S, \bar S) - f(\bar S, S) = |f|$ for each [s-t cut](/cut/) $(S, \bar S)$. With $0 \le f \le c$ this gives $|f| \le f(S, \bar S) \le c(S, \bar S)$, the weak duality between flows and [cut capacities](/cut-capacity/).

**Variants of the rule.**

- **Circulation.** Conservation holds at every vertex, $s$ and $t$ included. This is the setting of the [circulation problem](/circulation-problem/).
- **Supplies and demands.** Each vertex has a number $b(v)$ and the rule is $\operatorname{exc}_f(v) = b(v)$, with $\sum_v b(v) = 0$. A vertex with $b(v) < 0$ is a source of $-b(v)$ units and one with $b(v) > 0$ is a sink. Sign conventions differ between books; Ahuja, Magnanti and Orlin write supplies as positive numbers.
- **Preflow.** A [preflow](/preflow/) asks only $\operatorname{exc}_f(v) \ge 0$ at each $v \ne s$. The [push-relabel](/push-relabel/) algorithm keeps a preflow and restores conservation at the end.
- **Skew-symmetric form.** CLRS (second and third editions) and many papers use a function on all ordered pairs with $f(u, v) = -f(v, u)$. Conservation then reads $\sum_{w} f(v, w) = 0$. This form merges the flow on an antiparallel pair into one net value, so it cannot keep $f(u, v) = 3$ and $f(v, u) = 1$ apart; it sees only the net 2. The fourth edition of CLRS and this site use the nonnegative form above.

## Examples and non-examples

The network is the running example of [flow network](/flow-network/): $s a$ 10, $s c$ 10, $a b$ 4, $a c$ 2, $a d$ 8, $c d$ 9, $d b$ 6, $b t$ 10, $d t$ 10.

**A conserving flow.** Set $f(s, a) = 10$, $f(s, c) = 9$, $f(a, b) = 4$, $f(a, c) = 0$, $f(a, d) = 6$, $f(c, d) = 9$, $f(d, b) = 5$, $f(b, t) = 9$, $f(d, t) = 10$. The excess at each inner vertex is:

| vertex | in | out | excess |
|---|---|---|---|
| $a$ | 10 | $4 + 0 + 6 = 10$ | 0 |
| $b$ | $4 + 5 = 9$ | 9 | 0 |
| $c$ | $9 + 0 = 9$ | 9 | 0 |
| $d$ | $6 + 9 = 15$ | $5 + 10 = 15$ | 0 |

The value is $|f| = 10 + 9 = 19$, and the net flow into $t$ is $9 + 10 = 19$. Across the cut $S = \{s, a\}$ the forward flow is $f(s, c) + f(a, b) + f(a, c) + f(a, d) = 9 + 4 + 0 + 6 = 19$ and the backward flow is 0, as the identity predicts.

**Non-example: a leak.** Change only $f(d, t)$ to 9. Then $\operatorname{exc}_f(d) = 15 - 14 = 1$, so conservation fails at $d$. The function is still a [preflow](/preflow/), because no excess is negative.

**Non-example: a flow created at a vertex.** Change only $f(s, a)$ to 8. Then $\operatorname{exc}_f(a) = 8 - 10 = -2$. This is neither a flow nor a preflow.

**Zero edges and a network with no path.** A zero-capacity edge forces $f(e) = 0$, so it adds nothing to either sum. In the network $s \to a$ (5), $t \to a$ (5), with no path from $s$ to $t$, no edge leaves $a$, so conservation at $a$ says $f(s, a) + f(t, a) = 0$. Both values are nonnegative, so both are 0, and the only flow has value 0.

**Flow into the source.** In the network $s \to a$ (2), $a \to s$ (2), $a \to t$ (1), the function $f(s, a) = 2$, $f(a, s) = 1$, $f(a, t) = 1$ conserves at $a$ ($2 = 1 + 1$). Its value is $|f| = 2 - 1 = 1$: the definition of the value subtracts the flow that comes back into $s$.

**Antiparallel edges.** In $s \to a$ (3), $a \to b$ (2), $b \to a$ (1), $b \to t$ (2), $s \to b$ (1), the flow $f(s, a) = 1$, $f(a, b) = 2$, $f(b, a) = 1$, $f(s, b) = 1$, $f(b, t) = 2$ conserves at $a$ (in $1 + 1$, out $2$) and at $b$ (in $2 + 1$, out $1 + 2$). Its value is 2. The pair carries flow both ways: 2 units from $a$ to $b$ and 1 unit back. The net flow from $a$ to $b$ is 1, and the skew-symmetric form would record only this net 1.

## Related definitions

- An [s-t flow](/s-t-flow/) is a function that satisfies conservation and the capacity constraint $0 \le f(e) \le c(e)$.
- A [preflow](/preflow/) relaxes conservation to a nonnegative excess.
- A [cut](/cut/) and its [capacity](/cut-capacity/) bound the value of a conserving flow by the identity above.
- [Flow decomposition](/flow-decomposition/) writes a conserving flow as a sum of paths from $s$ to $t$ and cycles.
- The [circulation problem](/circulation-problem/) asks for conservation at every vertex, with lower and upper bounds.
- In linear algebra terms, conservation says that $Bf$ is zero outside $s$ and $t$, where $B$ is the [incidence matrix](/incidence-matrix/) of $G$.

## References
