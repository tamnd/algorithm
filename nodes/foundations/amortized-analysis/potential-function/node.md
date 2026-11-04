---
tag: 8R7E9B
kind: definition
slug: potential-function
name: Potential function
aliases:
- potential
area: foundations/amortized-analysis
level: intro
summary: A map from data structure states to non-negative reals, nonnegative and zero at the start, used in the potential method.
prereqs: [amortized-cost, accounting-method, telescoping-sum]
see_also: [potential-method, aggregate-method, splay-tree, fibonacci-heap, dynamic-table-contraction, potential-function-reduced-costs]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 16.3, The potential method, and Section 16.4, Dynamic tables
  - paper: doi:10.1137/0606031
    title: Robert E. Tarjan, Amortized computational complexity, SIAM Journal on Algebraic and Discrete Methods 6(2), 1985
    locator: pp. 306 to 318, the physicist's view of amortization
  - paper: doi:10.1145/3828.3835
    title: Daniel D. Sleator and Robert E. Tarjan, Self-adjusting binary search trees, Journal of the ACM 32(3), 1985
    locator: pp. 652 to 686, Section 2 (the potential of a splay tree and the access lemma)
---

A potential function is a map $\Phi$ from the states of a data structure to the real numbers, with $\Phi(D_0) = 0$ in the start state and $\Phi(D) \ge 0$ in each state that a legal sequence can reach. It measures the work that the structure has "stored up" for the future, like potential energy in physics. The [potential method](/potential-method/) uses it to define the [amortized cost](/amortized-cost/) of an operation as its actual cost plus the change in $\Phi$. Tarjan (1985) calls this the *physicist's view* of amortization.

## Definition

Let a data structure start in the state $D_0$, and let $\mathcal{R}$ be the set of states that some legal sequence of operations reaches from $D_0$. A **potential function** is a function $\Phi : \mathcal{R} \to \mathbb{R}$ with

$$\Phi(D_0) = 0 \quad\text{and}\quad \Phi(D) \ge 0 \text{ for all } D \in \mathcal{R}. \tag{1}$$

$\Phi$ depends only on the current state. It may use the size of the structure and any field of the state, but not the past or the future operations.

For an operation $o_i$ that takes $D_{i-1}$ to $D_i$ and has actual cost $c_i$, the **amortized cost with respect to $\Phi$** is

$$\hat c_i = c_i + \Phi(D_i) - \Phi(D_{i-1}). \tag{2}$$

**Lemma.** For each legal sequence of $m$ operations,

$$\sum_{i=1}^{m} c_i = \sum_{i=1}^{m} \hat c_i - \Phi(D_m) + \Phi(D_0). \tag{3}$$

If (1) holds, then $\sum_{i=1}^{m} c_i \le \sum_{i=1}^{m} \hat c_i$, so the charges (2) are valid amortized costs.

*Proof.* Add (2) over $i = 1, \ldots, m$. The terms $\Phi(D_i)$ for $1 \le i \le m - 1$ appear once with the sign $+$ and once with the sign $-$, so the sum is a [telescoping sum](/telescoping-sum/): $\sum_i \hat c_i = \sum_i c_i + \Phi(D_m) - \Phi(D_0)$. This is (3). By (1), $\Phi(D_m) \ge 0 = \Phi(D_0)$, so $-\Phi(D_m) + \Phi(D_0) \le 0$, and the inequality follows. The argument works for each $m$, so it covers each prefix. $\square$

The condition $\Phi(D_0) = 0$ is a convention. The lemma only needs $\Phi(D) \ge \Phi(D_0)$ for all reachable $D$. If the start state has a positive potential, identity (3) still holds and adds $\Phi(D_0)$ to the bound.

A function $\Phi$ that breaks (1) still gives charges by (2), and identity (3) is still true. Only the inequality is lost: a negative $\Phi(D_m)$ adds $|\Phi(D_m)|$ of cost that no charge pays for.

If $\Phi_1$ and $\Phi_2$ are potential functions and $a, b \ge 0$, then $a \Phi_1 + b \Phi_2$ is also a potential function. Its amortized costs are the same combination of the two amortized costs, minus $(a + b - 1)$ times the actual cost. Proofs often add a potential for each part of the structure.

## Examples and non-examples

Each line names the structure, the potential and the amortized costs that it gives. The pages of the structures have the full proofs.

| structure | potential $\Phi$ | amortized costs |
|---|---|---|
| [stack with multipop](/stack-with-multipop/) | the number of items $s$ | push 2, pop 0, multipop 0 |
| [binary counter](/binary-counter-increment/) | the number of 1 bits | increment at most 2 |
| [array doubling](/array-doubling/), $n$ items, capacity $c$ | $2n - c$ (and 0 for the empty array) | append at most 3 |
| [dynamic table with contraction](/dynamic-table-contraction/) at load $\tfrac14$ | $2n - c$ if $n \ge c/2$, else $c/2 - n$ | insert at most 3, delete at most 2 |
| [queue from two stacks](/two-stacks-queue/) | twice the size of the in-stack | enqueue 3, dequeue 1 |
| [splay tree](/splay-tree/) | $\sum_x \lg s(x)$, with $s(x)$ the size of the subtree of $x$ | access at most $3 \lg n + 1$ rotations |
| [Fibonacci heap](/fibonacci-heap/) | $t + 2m$: roots plus twice the marked nodes | insert $O(1)$, extract-min $O(\log n)$, decrease-key $O(1)$ |

**Example in numbers: the binary counter.** Let $\Phi$ be the number of 1 bits, and let an increment reset $t$ trailing ones and set one bit, so $c = t + 1$ and $\Delta\Phi = 1 - t$. Then $\hat c = 2$. After the 8 increments from 0000 to 1000, the actual costs are $1, 2, 1, 3, 1, 2, 1, 4$ (total 15), the charges are $8 \cdot 2 = 16$, and $\Phi(D_8) = 1$. Identity (3) reads $15 = 16 - 1 + 0$.

**Example: the potential of array doubling is not negative.** Before the first append, the array is empty and $\Phi = 0$ by definition. After that, the array is at least half full: after the expansion of a full array of capacity $c$ to $2c$ and the write of one new item, it holds $c + 1 > c$ items. So $2n - c \ge 0$ in each reachable state, although $2n - c$ is negative for other states, such as an empty array of capacity 8. Condition (1) is only about reachable states.

**Non-example: a potential that goes negative.** For the stack, take $\Phi = -s$. Then push gets $\hat c = 1 - 1 = 0$ and MULTIPOP$(k)$ gets $\hat c = 2k$. The "bound" says that $n$ pushes cost 0, but they cost $n$. Identity (3) shows the gap: $\sum c_i = \sum \hat c_i - \Phi(D_n) = 0 + n$.

**Non-example: a potential that looks at the future.** "Let $\Phi$ be the number of items that will be popped later" makes each pop cheap, but it is not a function of the state: two runs can reach the same stack and have different futures. The lemma does not apply.

**Non-example: a potential that does not start at its minimum.** For a $k$-bit counter, the number of 0 bits is non-negative, but it starts at $k$ and drops to 0 at the value $2^k - 1$. So $\Phi(D) \ge \Phi(D_0)$ fails, and the charges that it gives are not valid without the extra term $\Phi(D_0) - \Phi(D_m) = k$.

## Related definitions

- The [potential method](/potential-method/) is the technique of proving bounds with a potential function. It has the template and the pitfalls.
- In the [accounting method](/accounting-method/), the coins stored on the structure, added up, form a potential function when their number depends only on the state.
- [Reduced costs with a potential](/potential-function-reduced-costs/) in shortest-path algorithms use a function $h$ on the vertices and the same telescoping: along a path, $\sum (w(u,v) + h(u) - h(v)) = w(P) + h(s) - h(t)$.
- [Potential-based reward shaping](/potential-based-reward-shaping/) in reinforcement learning adds $\gamma \Phi(s') - \Phi(s)$ to each reward, and the sum over an episode telescopes in the same way.

## References
