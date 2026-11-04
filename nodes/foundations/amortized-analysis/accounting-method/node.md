---
tag: QPNA4W
kind: technique
slug: accounting-method
name: Accounting method
aliases:
- banker's method
- credit method
area: foundations/amortized-analysis
level: intro
summary: Charges each operation a fixed amortized cost and stores prepaid credit on data objects to pay for later expensive operations.
prereqs: [amortized-cost, aggregate-method]
see_also: [potential-method, potential-function, stack-with-multipop, binary-counter-increment, array-doubling, two-stacks-queue, banker-queue]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 16.2, The accounting method
  - paper: doi:10.1137/0606031
    title: Robert E. Tarjan, Amortized computational complexity, SIAM Journal on Algebraic and Discrete Methods 6(2), 1985
    locator: pp. 306 to 318, the banker's view of amortization
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press (1998)
    locator: Chapter 5, Fundamentals of Amortization (the banker's method), and Chapter 6 for the version with debits
---

The accounting method proves an [amortized cost](/amortized-cost/) by giving each operation type a fixed charge and storing the part of the charge that the operation does not spend as *credit* on objects of the data structure. A later expensive operation pays for its extra work with the credit that it finds on the objects it touches. If the stored credit is never negative, the charges are valid amortized costs. Tarjan (1985) calls this the *banker's view*; the [potential method](/potential-method/) is the same idea with one number for the whole structure.

## In plain words

Think of each operation as a customer who pays a fixed price. A cheap operation pays more than its work costs. It leaves the extra coins on the parts of the structure that will cause work later: on an item that will be popped one day, or on a bit that will be reset one day. An expensive operation then uses these coins to pay for its extra work. If every coin that the expensive operation needs is already there, no operation ever runs into debt. Then the fixed prices, added over the whole run, pay for all the work. The skill is to decide where the coins go, so that each coin sits on the object that will need it.

## When it applies

- The expensive work of an operation is spread over objects (items, bits, slots), and each object can carry a fixed number of coins for the work it will cause.
- You want different charges for different operation types, for example a push that pays 2 and a pop that pays 0.
- You can say, for each operation, which objects it puts credit on and which credit it uses, in a local way.
- The structure is used in a single thread of updates. In a [persistent](/persistent-data-structure/) structure, one coin can be spent by many versions; see the pitfalls.

## The template

```pseudo id=main
ACCOUNTING-BOUND(structure, operation types)
L1  for each operation type X, choose a charge ĉ_X                 ▷ hole: the prices
L2  state a credit invariant: each object of kind K holds ≥ r_K coins ▷ hole: where the coins sit
L3  check the invariant in the start state D_0 (usually empty)
L4  for each operation type X and each state:
L5      pay the actual cost c from ĉ_X and from coins that the operation removes from objects
L6      put the rest of ĉ_X as coins on objects, so that the invariant holds again
L7      check that no object ends with a negative number of coins
L8  conclude: Σ c_i ≤ Σ ĉ_i for each legal sequence
```

**Why line L8 follows.** Let $\mathrm{bank}_i$ be the total number of coins on all objects after the $i$-th operation, with $\mathrm{bank}_0 = 0$. Operation $i$ receives $\hat c_i$ coins, spends $c_i$ coins on its work, and leaves the rest in the structure, so $\mathrm{bank}_i = \mathrm{bank}_{i-1} + \hat c_i - c_i$. Add these equalities for $i = 1, \ldots, m$:

$$\sum_{i=1}^{m} \hat c_i - \sum_{i=1}^{m} c_i = \mathrm{bank}_m - \mathrm{bank}_0 = \mathrm{bank}_m \ge 0.$$

The last step uses line L7: no object holds a negative number of coins, so the bank is not negative. This holds for each $m$, which is the definition of a valid amortized cost. Coins that sit on an object that the structure throws away are lost. This is allowed: it only makes the bound less tight.

The coins are a device of the proof. The program does not store them.

## Classic examples

**[Stack with multipop](/stack-with-multipop/).** Charge 2 for PUSH and 0 for POP and MULTIPOP. Invariant: each item on the stack holds 1 coin. A push pays 1 for its work and puts 1 coin on the new item. A pop or a multipop pays 1 for each item it removes with the coin of that item. So $n$ operations cost at most $2n$.

**[Binary counter increment](/binary-counter-increment/).** Charge 2 for each increment. Invariant: each bit that is 1 holds 1 coin. An increment resets the trailing ones and sets one bit. Each reset is paid by the coin on that bit. The one set costs 1, and the second coin goes on the new 1 bit. If the counter has $k$ bits and all are 1, the increment resets all of them and sets none; the coins pay for all $k$ resets, and the 2 coins of the charge are lost. So $n$ increments from 0 flip at most $2n$ bits.

| increment | value before | value after | flips | coins on ones after |
|---|---|---|---|---|
| 1 | 0000 | 0001 | 1 | 1 |
| 2 | 0001 | 0010 | 2 | 1 |
| 3 | 0010 | 0011 | 1 | 2 |
| 4 | 0011 | 0100 | 3 | 1 |
| 5 | 0100 | 0101 | 1 | 2 |
| 6 | 0101 | 0110 | 2 | 2 |
| 7 | 0110 | 0111 | 1 | 3 |
| 8 | 0111 | 1000 | 4 | 1 |

The 8 increments flip 15 bits and are charged 16. The one coin left is the coin on the bit that is 1 at the end.

**[Array doubling](/array-doubling/).** Charge 3 for each append. Invariant: right after an expansion to capacity $2c$, no item holds a coin, and each item appended since then holds 2 coins. An append without expansion pays 1 to write the item and puts 2 coins on it. When the array of capacity $2c$ is full, $c$ items were appended since the last expansion and they hold $2c$ coins, which pay for the $2c$ copies. (In words: an item pays for its own copy and for the copy of one old item that has no coin.) The first expansion, from capacity 0 to 1, copies nothing. The second, from 1 to 2, copies one item, and that item holds 2 coins.

**[Queue from two stacks](/two-stacks-queue/).** ENQUEUE pushes onto an in-stack; DEQUEUE pops from an out-stack, and when the out-stack is empty, it first moves all items from the in-stack to the out-stack. Charge 3 for ENQUEUE and 1 for DEQUEUE. Invariant: each item on the in-stack holds 2 coins. A move pops the item from the in-stack and pushes it on the out-stack, and its 2 coins pay for these 2 steps. So each sequence of $n$ operations costs at most $3n$ stack steps.

**[Dynamic table with contraction](/dynamic-table-contraction/).** With expansion at full and contraction below load $\tfrac14$, insert and delete each have a constant charge. The proof there uses a potential, which is the total of the coins written as one formula.

## Variations

- **The potential method.** If the bank depends only on the state, call it $\Phi(D_i)$. Then $\hat c_i = c_i + \Phi(D_i) - \Phi(D_{i-1})$ and the invariant is $\Phi \ge 0$. This is the [potential method](/potential-method/). Each accounting proof gives a [potential function](/potential-function/): the number of coins in the structure. The converse also holds when the coins are a function of the state.
- **Charges that depend on the size.** In a [splay tree](/splay-tree/) the charge of an access is $O(\log n)$, and the coins on a node depend on the size of its subtree. The proof is usually written with a potential.
- **Debits instead of credits.** Okasaki's banker's method for lazy structures puts *debits* on suspended computations. A computation may run only after enough operations have paid off its debit. This version stays valid under persistence, because a paid debit is paid in each version that shares the computation.
- **Charging to another object.** Some proofs move the cost of one operation to an earlier operation or to another object, as in the analysis of [Fibonacci heaps](/fibonacci-heap/), where a cut is paid by a mark that an earlier decrease-key set.

## Pitfalls

- **Spending a coin twice.** Each coin must pay for one unit of work only. In the doubling proof, a newly appended item pays for its own copy and for one old item. If you pay for the old item twice (once at each expansion), the bank runs out.
- **A coin that goes negative for a moment.** The invariant must hold after each operation, and inside an operation the coins taken from an object must already be there. "The bank is positive at the end of the sequence" is not enough.
- **Coins on the wrong object.** If the coin for a pop sits on the push operation and not on the item, a multipop cannot find it. Put coins on the objects that the expensive operation visits.
- **Persistence.** In a [persistent](/persistent-data-structure/) structure an old version can be used again, and the coins on it are spent each time. Take the [banker's queue](/banker-queue/) with an empty front list and $n$ items in the rear list, and dequeue from this same version $n$ times. Each dequeue reverses the rear list. For $n = 1000$ the $n$ enqueues and $n$ dequeues cost $1{,}002{,}000$ steps, not the $3000$ of the ephemeral queue. Okasaki's debit method fixes this.
- **Real-time use.** The method bounds the total, not the delay of one operation. A dequeue that moves $n$ items still takes $\Theta(n)$ time. Use a [real-time queue](/real-time-queue/) or [global rebuilding](/global-rebuilding/) when each operation must be fast.

## Exercises

1. Give an accounting proof that a stack with PUSH, POP and MULTIPOP, which starts with $s_0$ items, costs at most $2n + s_0$ for $n$ operations. What credit must the start state hold?
2. The life of one item in the two-stack queue costs 4 steps, so it is tempting to charge 2 for ENQUEUE and 2 for DEQUEUE. Give a short legal sequence for which these charges do not cover the actual cost.
3. A counter supports INCREMENT and RESET (set all bits to 0). Keep a pointer to the highest 1 bit, so that RESET costs the number of bits up to that pointer. Show that both operations have amortized cost $O(1)$.

## References
