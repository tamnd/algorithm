---
tag: W2TG3Y
kind: definition
slug: amortized-cost
name: Amortized cost
aliases:
- amortised cost
area: foundations/amortized-analysis
level: intro
summary: The per-operation charge in an amortized analysis, which can differ from the actual cost of that operation.
prereqs: [asymptotic-notation, worst-case-analysis]
see_also: [aggregate-method, accounting-method, potential-method, amortized-vs-worst-case, amortized-vs-expected-cost, stack-with-multipop, binary-counter-increment, array-doubling]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 16, Amortized Analysis (introduction and Sections 16.1 to 16.3)
  - paper: doi:10.1137/0606031
    title: Robert E. Tarjan, Amortized computational complexity, SIAM Journal on Algebraic and Discrete Methods 6(2), 1985
    locator: pp. 306 to 318, Sections 1 and 2
  - book: isbn:9780521663502
    title: Chris Okasaki, Purely Functional Data Structures, Cambridge University Press (1998)
    locator: Chapter 5, Fundamentals of Amortization
---

The amortized cost of an operation is a charge that an analysis assigns to each operation of a data structure, such that over every sequence of operations the sum of the charges is at least the sum of the actual costs. One operation can cost much more than its charge, if earlier operations paid more than their actual cost. The idea comes from the analysis of [dynamic arrays](/dynamic-array/), [splay trees](/splay-tree/) and union-find, where a single operation is slow but a long run of operations is fast. Tarjan made the notion standard in 1985. The three usual ways to prove an amortized cost are the [aggregate method](/aggregate-method/), the [accounting method](/accounting-method/) and the [potential method](/potential-method/).

## Definition

Fix a data structure with a start state $D_0$ and a set of operation types. A *legal sequence* is a sequence of operations $o_1, o_2, \ldots, o_m$ that the structure accepts from $D_0$ (for example, no pop on an empty stack). Let $D_i$ be the state after $o_i$, and let $c_i \ge 0$ be the *actual cost* of $o_i$ in a fixed cost model, such as the number of steps of the [unit-cost RAM](/unit-cost-model/).

An assignment of *amortized costs* gives each operation $o_i$ a number $\hat c_i$. The value $\hat c_i$ may depend on the type of $o_i$, on its arguments and on the size of the structure before $o_i$, but not on the operations that come after $o_i$. The assignment is **valid** when, for every legal sequence and every $m \ge 0$,

$$\sum_{i=1}^{m} c_i \;\le\; \sum_{i=1}^{m} \hat c_i. \tag{1}$$

Each prefix of a legal sequence is a legal sequence, so (1) holds for each prefix. This is important: the charges must cover the actual cost at each moment, not only at the end of a sequence that you choose.

An operation type $X$ **has amortized cost $O(f(n))$** when there is a valid assignment and a constant $C$ such that each operation of type $X$ on a structure of size $n$ gets a charge $\hat c_i \le C f(n)$. If each operation type has amortized cost $O(1)$, then each legal sequence of $m$ operations costs $O(m)$ in total.

Three facts follow at once from the definition.

- **A bound on the total.** If $\hat c_i \le a$ for each $i$, then $m$ operations cost at most $a m$. This is the only promise that an amortized bound makes.
- **No bound on one operation.** The definition allows one $c_i$ to be much larger than $\hat c_i$. The [worst-case](/worst-case-analysis/) cost of one operation can be $\Theta(n)$ while the amortized cost is $O(1)$. See [amortized versus worst-case cost](/amortized-vs-worst-case/).
- **Not unique.** A structure has many valid assignments. For the stack below, both "push 2, pop 0" and "push 1, pop 1, multipop $\min(k, s)$" are valid. An analysis picks one that gives a simple bound.

The amortized cost of an operation is not the average of the actual costs of the operations of that type. In the stack below, a pop has actual cost 1 and amortized cost 0, and a push has actual cost 1 and amortized cost 2. The charge moves cost from one operation type to another.

## Examples and non-examples

**Stack with multipop.** On a [stack with multipop](/stack-with-multipop/), push and pop cost 1, and MULTIPOP$(k)$ on a stack of size $s$ costs $\min(k, s)$. The charges $\hat c = 2$ for push and $\hat c = 0$ for pop and multipop are valid: each popped item was pushed before, and its push paid 1 for the pop. For the sequence of 5 pushes, MULTIPOP(3), 2 pushes, a pop and MULTIPOP(10), the actual costs are $1,1,1,1,1,3,1,1,1,3$ (total 14) and the charges are $2,2,2,2,2,0,2,2,0,0$ (total 14). Each prefix sum of the charges is at least the prefix sum of the actual costs.

**Binary counter.** A [binary counter](/binary-counter-increment/) that starts at 0 flips exactly $2n - s_2(n)$ bits in $n$ increments, where $s_2(n)$ is the number of 1 bits of $n$. So the charge 2 for each increment is valid. One increment can flip all $k$ bits. The constant 2 is the smallest constant that works for all $n$: for $n = 2^j$ the total is $2^{j+1} - 1$, and $(2^{j+1} - 1)/2^j = 2 - 2^{-j}$ is larger than each constant below 2 when $j$ is large.

**Array doubling.** An append to a [doubling array](/array-doubling/) that starts empty has amortized cost 3, while one append can copy $n - 1$ items. For $n = 1025$ appends the total cost is $3072 = 3n - 3$, so no constant below 3 is valid for all $n$.

**Non-example: a charge that is too small on one prefix.** Charge 1 for each stack operation, including multipop. The sequence of $k$ pushes and then MULTIPOP$(k)$ costs $2k$ but gets the charge $k + 1$. For $k \ge 2$ condition (1) fails, so the assignment is not valid, although many other sequences satisfy (1).

**Non-example: a bound that holds only for some sequences.** A counter with both increment and decrement does not have amortized cost $O(1)$. From the value $2^{k-1} - 1$, the sequence increment, decrement, increment, and so on flips all $k$ bits at each step. For $k = 8$, 1000 such operations flip 8000 bits. An average over one sequence that you like does not give an amortized bound.

**Non-example: an expected cost.** Insert into a hash table with chaining has expected cost $O(1)$ under [simple uniform hashing](/simple-uniform-hashing/). This is an average over a random choice (of the keys, or of the hash function in [universal hashing](/universal-hashing/)), not over the operations of a sequence. For a fixed hash function that sends all keys to one slot, $n$ inserts followed by $n$ searches cost $\Theta(n^2)$. See [amortized versus expected cost](/amortized-vs-expected-cost/).

## Related definitions

- The [aggregate method](/aggregate-method/) bounds the total $T(m)$ directly and charges $T(m)/m$ to each operation.
- The [accounting method](/accounting-method/) chooses the charges first and stores the surplus $\hat c_i - c_i$ as credit on parts of the structure. The credit must never be negative.
- A [potential function](/potential-function/) $\Phi$ on the states defines the charges $\hat c_i = c_i + \Phi(D_i) - \Phi(D_{i-1})$. The [potential method](/potential-method/) shows that these charges are valid when $\Phi(D_i) \ge \Phi(D_0)$ for all $i$.
- [Amortized update time](/amortized-update-time/) is the same notion for the updates of a dynamic graph algorithm, and [worst-case update time](/worst-case-update-time/) is its worst-case counterpart.
- [Constant amortized time generation](/constant-amortized-time-generation/) uses the notion for algorithms that list combinatorial objects.

### Terms

Tarjan (1985) introduced two names for the two styles of proof: the *banker's view* (credits stored on the structure, the accounting method) and the *physicist's view* (a potential of the whole state, the potential method). Okasaki uses the same names in his book on functional data structures.

## References
