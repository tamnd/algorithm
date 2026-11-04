---
tag: 888KHH
kind: problem
slug: stack-with-multipop
name: Stack with multipop
aliases:
- multipop stack
area: foundations/amortized-analysis
level: intro
summary: A stack supporting push, pop and multipop(k); each element is popped at most once, giving O(1) amortized cost.
prereqs: [stack, amortized-cost]
see_also: [aggregate-method, accounting-method, potential-method, binary-counter-increment, monotonic-stack, two-stacks-queue, persistent-stack]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 16.1 (stack operations), Section 16.2 and Section 16.3 (the same example with credits and with a potential)
  - paper: doi:10.1137/0606031
    title: Robert E. Tarjan, Amortized computational complexity, SIAM Journal on Algebraic and Discrete Methods 6(2), 1985
    locator: pp. 306 to 318
---

The stack with multipop is a [stack](/stack/) with a third operation, MULTIPOP$(k)$, which pops the top $k$ items, or all items when the stack holds fewer than $k$. One MULTIPOP can cost as much as the size of the stack, but each item is popped at most once after it is pushed, so each sequence of $n$ operations from an empty stack costs at most $2n$. It is the first example of [amortized cost](/amortized-cost/) in CLRS, and the simplest place to compare the [aggregate method](/aggregate-method/), the [accounting method](/accounting-method/) and the [potential method](/potential-method/).

## In plain words

A stack is a pile: you put items on top and take them from the top. Add an operation that takes many items from the top at once. One such call can take the whole pile, so a single call can be slow. But a call can only take items that are there, and each item got there by one put. So over a long run of operations, the number of items taken is at most the number of items put. If you count the work of a run and not of a single call, each operation does at most two units of work on average, however you mix the operations.

## Definition

The state is a sequence $S = (x_1, \ldots, x_s)$ of items, with $x_s$ on top; the start state is empty. The operations are:

- PUSH$(x)$: append $x$ on top. Cost 1.
- POP: remove and return the top item. Legal only when $s \ge 1$. Cost 1.
- MULTIPOP$(k)$ for an integer $k \ge 1$: remove the top $\min(k, s)$ items. Cost $\min(k, s)$.

```pseudo id=main
MULTIPOP(S, k)
L1  while not EMPTY(S) and k > 0 do
L2      POP(S)
L3      k ← k − 1
```

The cost model counts the pops of line L2: one unit for each item that leaves the stack. This is the model of CLRS. If the call itself also costs one unit, the cost is $1 + \min(k, s)$; see the variants.

**The problem.** Bound the total cost $T$ of each legal sequence of $n$ operations from the empty stack.

**Theorem.** Each legal sequence of $n$ operations from the empty stack costs at most $2n$. So each operation has amortized cost at most 2, and MULTIPOP has amortized cost 0 if PUSH is charged 2.

*Proof by the aggregate method.* Let $p$ be the number of PUSH operations in the sequence. An item can be removed only after it was pushed, and only once. The cost of all POP and MULTIPOP operations is the number of items they remove, so it is at most $p$. Then $T \le p + p \le 2n$. $\square$

*Proof by the accounting method.* Charge 2 for PUSH and 0 for POP and MULTIPOP. Keep this invariant: each item on the stack holds 1 coin. A PUSH pays 1 for its work and puts 1 coin on the new item. A POP or a MULTIPOP pays for each item that it removes with the coin of that item. No coin is used twice, and no item has a negative number of coins, so the total charge, at most $2n$, is at least the total cost. $\square$

*Proof by the potential method.* Let $\Phi(S) = s$, the number of items. Then $\Phi = 0$ at the start and $\Phi \ge 0$ always. The amortized costs $\hat c = c + \Delta\Phi$ are: PUSH $1 + 1 = 2$; POP $1 - 1 = 0$; MULTIPOP$(k)$ $\min(k,s) - \min(k,s) = 0$. By the lemma of the [potential function](/potential-function/) page, $T \le \sum \hat c \le 2n$. $\square$

The three proofs are the same argument in three forms. In the accounting proof the coins are on the items, in the potential proof their number $s$ is the potential, and in the aggregate proof the count "pops $\le$ pushes" is the statement that the bank of coins never goes below 0.

## Variants

- **A cost for the call.** If MULTIPOP$(k)$ costs $1 + \min(k, s)$, charge PUSH 2, POP 0 and MULTIPOP 1. The bound becomes $T \le 2n$ still, since each operation is charged at most 2.
- **A start state that is not empty.** If the stack starts with $s_0$ items, then $T \le 2n + s_0$, from the identity $\sum c_i = \sum \hat c_i + \Phi(D_0) - \Phi(D_n)$ with $\Phi(D_0) = s_0$.
- **MULTIPUSH.** If there is an operation that pushes $k$ items at cost $k$, no constant amortized bound holds for it: the sequence MULTIPUSH$(k)$, MULTIPOP$(k)$ repeated $n/2$ times costs $nk$. The amortized cost of MULTIPUSH$(k)$ is $2k$, which is still $O(1)$ for each item.
- **Bounded size and backups.** If the size never exceeds $k$ and the whole stack is copied after each $k$ operations, the copies add at most 1 per operation, and the amortized cost stays $O(1)$ (an exercise of CLRS).
- **Persistent stack.** In a [persistent stack](/persistent-stack/) stored as a linked list, an old version can be used again. Push $n$ items, then apply MULTIPOP$(n)$ $n$ times to that same version. Each call walks $n$ cells, so the $2n$ operations cost $n + n^2$, which is $1{,}001{,}000$ for $n = 1000$. The amortized bound needs each operation to act on the newest version.

## Examples

The sequence 5 pushes, MULTIPOP(3), 2 pushes, POP, MULTIPOP(10) from the empty stack:

| op | actual cost | size after | $\Phi$ after | amortized cost $\hat c$ |
|---|---|---|---|---|
| PUSH ×5 | 1 each | 1, 2, 3, 4, 5 | 1, 2, 3, 4, 5 | 2 each |
| MULTIPOP(3) | 3 | 2 | 2 | 0 |
| PUSH | 1 | 3 | 3 | 2 |
| PUSH | 1 | 4 | 4 | 2 |
| POP | 1 | 3 | 3 | 0 |
| MULTIPOP(10) | 3 | 0 | 0 | 0 |

The total actual cost is 14 and the total amortized cost is 14. They are equal because the stack is empty at the end, so $\Phi(D_{10}) = 0$. The largest single cost is 3, from a MULTIPOP.

**The worst case of one sequence.** The bound $2n$ is almost tight. For $n \ge 2$, the largest total cost of a legal sequence of $n$ operations is exactly $2n - 2$: push $n - 1$ items, then MULTIPOP$(n-1)$. The bound cannot be larger, since each sequence with a removal has at most $n - 1$ pushes and the cost is at most twice the pushes. A sequence of only pushes costs $n$. For $n = 1$ to 7 the largest totals are 1, 2, 4, 6, 8, 10, 12.

**The naive bound.** One MULTIPOP can cost $n - 1$. Adding the worst case of each operation gives the bound $O(n^2)$, which is far from the truth.

## Known algorithms

- **Array with a top index.** PUSH and POP take $O(1)$ time. MULTIPOP$(k)$ pops one item at a time in $\Theta(\min(k, s))$ time, which matches the cost model, and $O(1)$ amortized time. If the items need no clean-up (no destructor, no release of a reference), MULTIPOP can set the top index to $\max(s - k, 0)$ in $O(1)$ worst-case time; then the amortized analysis is not needed at all.
- **Linked list.** The same bounds. MULTIPOP walks $\min(k, s)$ cells.
- **Return the popped items.** If MULTIPOP must return the $\min(k,s)$ items, the output alone takes $\Theta(\min(k,s))$ time, so the amortized bound of 2 per operation (counting each returned item as work) is the best possible.

## Bounds

In the cost model above, $n$ operations from an empty stack cost at most $2n$ (upper bound, by the theorem) and some sequence costs $2n - 2$ (lower bound, by the example). So the amortized cost per operation is 2 in the limit, and the worst-case cost of one MULTIPOP is $\Theta(n)$.

## Reductions

- **A queue from two stacks.** The [queue from two stacks](/two-stacks-queue/) moves all items of one stack to the other when the out-stack is empty. That move is a MULTIPOP of the whole in-stack plus pushes, and the same "each item moves once" argument gives $O(1)$ amortized time per queue operation.
- **The binary counter.** The [binary counter](/binary-counter-increment/) has the same shape: an increment resets a run of trailing ones (a MULTIPOP of the run) and sets one bit (a PUSH). The potential "number of ones" plays the role of "number of items".

## Applications

- **Monotonic stack loops.** The loop "while the stack is not empty and its top is smaller than $x$, pop" is a MULTIPOP with a data-dependent $k$. The [monotonic stack](/monotonic-stack/) and the [Graham scan](/graham-scan/) are linear for this reason.
- **Shift-reduce parsing.** A reduce step pops the right side of a rule, which can be long, but each symbol is pushed once by a shift or a reduce.
- **Undo of several steps.** An editor that keeps an undo stack and undoes $k$ steps at once does $O(1)$ amortized work for each recorded edit.

## References
