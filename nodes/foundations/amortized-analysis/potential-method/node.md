---
tag: 84QF3M
kind: technique
slug: potential-method
name: Potential method
aliases:
- potential function method
area: foundations/amortized-analysis
level: intro
summary: Defines a potential function on the data structure state and sets amortized cost as actual cost plus change in potential.
prereqs: [amortized-cost, potential-function, accounting-method]
see_also: [aggregate-method, stack-with-multipop, binary-counter-increment, array-doubling, dynamic-table-contraction, splay-tree, fibonacci-heap, union-find-amortized-bound]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 16.3, The potential method, and Section 16.4, Dynamic tables
  - paper: doi:10.1137/0606031
    title: Robert E. Tarjan, Amortized computational complexity, SIAM Journal on Algebraic and Discrete Methods 6(2), 1985
    locator: pp. 306 to 318
  - paper: doi:10.1145/3828.3835
    title: Daniel D. Sleator and Robert E. Tarjan, Self-adjusting binary search trees, Journal of the ACM 32(3), 1985
    locator: pp. 652 to 686, Section 2 (access lemma)
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press (1998)
    locator: Chapter 5 (the physicist's method) and Chapter 6 (amortization and persistence)
---

The potential method proves an [amortized cost](/amortized-cost/) with a [potential function](/potential-function/) $\Phi$ on the states of a data structure: the amortized cost of an operation is its actual cost plus the change in $\Phi$ that it causes. If $\Phi$ starts at 0 and never becomes negative, the sum of the amortized costs bounds the sum of the actual costs over each sequence. It is the most general of the three methods, after the [aggregate method](/aggregate-method/) and the [accounting method](/accounting-method/), and it is the method behind the bounds for [splay trees](/splay-tree/), [Fibonacci heaps](/fibonacci-heap/) and [union-find](/union-find-amortized-bound/).

## In plain words

Give the data structure a score that says how much trouble is stored up in it: how many items wait to be popped, how many bits are set, how full the array is. A cheap operation that adds trouble raises the score, and you count that rise as part of its cost. An expensive operation removes trouble and lowers the score, and the drop pays for its extra work. Its cost in the analysis becomes small. If the score starts at zero and never goes below zero, then the costs in the analysis, added over the run, are at least the real costs. The skill is to find a score for which each operation, cheap or expensive, has a small cost in the analysis.

## When it applies

- The cost of an expensive operation depends on a quantity of the state that cheap operations build up: the size of a stack, the number of 1 bits, the free space of an array, the number of roots of a heap.
- The stored work is a property of the whole state, not of single objects. Then a formula is easier than coins on objects.
- The amortized cost depends on the size, as in $O(\log n)$ for a splay tree, or on the state in a way that is hard to express as coins.
- The structure is used ephemerally: each operation acts on the newest state. For persistent use, see the pitfalls.

## The template

```pseudo id=main
POTENTIAL-BOUND(structure, operation types)
L1  choose Φ(D) as a function of the state D                    ▷ hole: the potential
L2  prove Φ(D_0) = 0 and Φ(D) ≥ 0 for each reachable state D    ▷ the potential is valid
L3  for each operation type X and each case of X:               ▷ hole: the case split
L4      write its actual cost c in terms of the state
L5      compute ΔΦ = Φ(after) − Φ(before)
L6      bound ĉ = c + ΔΦ ≤ a_X
L7  conclude: each legal sequence costs at most Σ a_{X_i}
```

**Why line L7 follows.** Add $\hat c_i = c_i + \Phi(D_i) - \Phi(D_{i-1})$ over $i = 1, \ldots, m$. The sum telescopes to $\sum \hat c_i = \sum c_i + \Phi(D_m) - \Phi(D_0)$. With line L2 this gives $\sum_{i \le m} c_i \le \sum_{i \le m} \hat c_i \le \sum_{i \le m} a_{X_i}$ for each $m$. The lemma and its proof are on the page [potential function](/potential-function/).

**How to find $\Phi$.** Look at the expensive case of each operation. Its extra work must be paid by a drop of $\Phi$ of the same size. So $\Phi$ must be large in the states just before an expensive operation, and small just after it. For the stack, MULTIPOP$(k)$ removes $k$ items, so $\Phi$ should drop by $k$: take the number of items. For array doubling, an expansion of a full array of capacity $c$ copies $c$ items, so $\Phi$ should be about $c$ when the array is full and about 0 just after the expansion: $2n - c$ goes from $c$ to 2. Then check the cheap cases: they must not raise $\Phi$ by more than a constant.

**Start in another state.** If the structure starts in a state with $\Phi(D_0) > 0$, the identity gives $\sum c_i = \sum \hat c_i + \Phi(D_0) - \Phi(D_m) \le \sum \hat c_i + \Phi(D_0)$. A counter that starts with $b_0$ ones and ends with $b_n$ ones flips at most $2n - b_n + b_0$ bits in $n$ increments. So the amortized bound holds after a start-up cost of $\Phi(D_0)$, and it is $O(n)$ in total once $n = \Omega(\Phi(D_0))$.

## Classic examples

The three examples of CLRS, each with all three methods, are on their own pages. Here is the potential argument for each, in one line, and three harder examples.

- **[Stack with multipop](/stack-with-multipop/).** $\Phi$ = the number of items. Push: $1 + 1 = 2$. Pop: $1 - 1 = 0$. MULTIPOP$(k)$ on $s$ items: $\min(k,s) - \min(k,s) = 0$.
- **[Binary counter increment](/binary-counter-increment/).** $\Phi$ = the number of 1 bits. An increment that resets $t$ ones and sets one bit costs $t + 1$ and changes $\Phi$ by $1 - t$, so $\hat c = 2$.
- **[Array doubling](/array-doubling/).** $\Phi = 2n - c$ for $n$ items in capacity $c$. An append without expansion costs 1 and raises $\Phi$ by 2: $\hat c = 3$. An append into a full array of capacity $c$ costs $c + 1$, and $\Phi$ goes from $c$ to $2(c+1) - 2c = 2$: $\hat c = c + 1 + 2 - c = 3$.
- **[Dynamic table with contraction](/dynamic-table-contraction/).** A two-piece potential, $2n - c$ above load $\tfrac12$ and $c/2 - n$ below it, gives insert at most 3 and delete at most 2, with contraction at load $\tfrac14$. The page has the full case analysis and the bad case of contraction at load $\tfrac12$.
- **[Splay tree](/splay-tree/).** $\Phi = \sum_x \lg s(x)$, where $s(x)$ is the number of nodes in the subtree of $x$. The access lemma of Sleator and Tarjan (1985) says that a splay of $x$ in a tree with root $t$ costs at most $3(\lg s(t) - \lg s(x)) + 1$ rotations amortized, so at most $3 \lg n + 1$.
- **[Fibonacci heap](/fibonacci-heap/).** $\Phi = t + 2m$, the number of roots plus twice the number of marked nodes. Insert adds a root and costs $O(1)$ amortized. Extract-min consolidates the root list, and the drop of $t$ pays for the work, so the amortized cost is $O(\log n)$. A cascading cut of $k$ nodes unmarks about $k$ nodes, and the drop of $2m$ pays for the cuts, so decrease-key costs $O(1)$ amortized.
- **[Union-find with union by rank and path compression](/union-find-amortized-bound/).** Tarjan's bound $O(m\,\alpha(m, n))$ has a proof with a potential on each node that depends on its rank and on the rank of its parent.

## Variations

- **Potential per object.** If $\Phi = \sum_x \phi(x)$ over the objects of the structure, the method is the [accounting method](/accounting-method/) with $\phi(x)$ coins on $x$.
- **Several potentials.** Add a potential for each source of future work, with weights chosen so that the expensive cases balance. The Fibonacci heap uses weight 1 for roots and 2 for marks.
- **Amortized cost as a function of the state.** In a splay tree, $\hat c$ depends on the ranks of the nodes on the access path. The bound per operation is then written in terms of $n$, or in terms of weights, which gives the static optimality and working-set theorems of the same paper.
- **Lower bounds.** If you can show $\hat c_i \ge a$ for each operation and $\Phi(D_m) \le \Phi(D_0) + B$, then $\sum c_i \ge a m - B$. The same identity proves lower bounds on the total.
- **Persistence and laziness.** Okasaki's physicist's method for lazy structures charges the change in a potential of *unevaluated* work and gives bounds that hold for persistent use, with memoized suspensions.

## Pitfalls

- **A potential that goes negative.** Line L2 is not a formality. The doubling potential $2n - c$ is negative for an array that is less than half full. It is valid only because doubling keeps each reachable non-empty array at least half full. If you add contraction at load $\tfrac14$, the array can be a quarter full, and $2n - c$ goes negative; that is why the [contraction page](/dynamic-table-contraction/) needs a second piece. Always check $\Phi \ge 0$ on each reachable state, not on the states that you have in mind.
- **A potential that is not a function of the state.** $\Phi$ must be computable from the current state alone. A quantity that depends on the past (how many operations have been done) or on the future (how many pops will come) does not give the telescoping identity for all sequences.
- **Forgetting a case.** Each operation type has a cheap case and an expensive case, and often edge cases: the first insert into an empty table, an increment of a counter that is all ones, a multipop of more items than the stack has. Bound $\hat c$ in each case.
- **Units.** The actual cost and $\Phi$ must count the same unit. If one copy costs 5 steps in your model, the potential for doubling must be $5(2n - c)$ or the charges must be scaled.
- **Persistent use.** In a [persistent](/persistent-data-structure/) structure, an old version $D$ with large $\Phi(D)$ can be the input of many operations. Each of them uses the same drop of potential, but it was paid only once. For the [banker's queue](/banker-queue/) with $n$ items in the rear list, $n$ dequeues on the same old version cost $n(n+1)$ steps in total, not $O(n)$. The bound of the potential method holds only for sequences in which each operation acts on the latest state.
- **Real-time use.** An $O(1)$ amortized bound allows one operation of cost $\Theta(n)$. In a game loop, an interrupt handler or a network switch, one append that copies $2^{20}$ items is a missed deadline. Use a worst-case structure, or de-amortize with [global rebuilding](/global-rebuilding/).

## Exercises

1. A stack supports PUSH, POP and MULTIPOP, its size never exceeds $k$, and the whole stack is copied for a backup after each $k$ operations, at a cost equal to its size. Find a potential that shows an amortized cost of $O(1)$ per operation, including the backups.
2. Show that $\Phi = 3n - c$ also proves an $O(1)$ amortized bound for array doubling, and find its constant. Why is the smaller coefficient 2 better?
3. A heap supports INSERT in $O(\log n)$ and EXTRACT-MIN in $O(\log n)$ worst-case time. Find a potential that makes EXTRACT-MIN cost $O(1)$ amortized while INSERT stays $O(\log n)$.

## References
