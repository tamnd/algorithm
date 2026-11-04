---
tag: 0XJN8M
kind: technique
slug: dynamic-table-contraction
name: Dynamic table contraction
aliases:
- table shrinking
area: foundations/amortized-analysis
level: core
summary: Shrink a table when its load factor drops below a threshold, keeping amortized cost O(1) for insertions and deletions.
prereqs: [array-doubling, potential-method, load-factor]
see_also: [dynamic-array, dynamic-array-resizing, hash-table, rehashing, accounting-method, aggregate-method, global-rebuilding, amortized-vs-worst-case]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 16.4.2, Table expansion and contraction
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.3 (resizing array that halves at one quarter full) and Section 1.4 (amortized analysis)
  - paper: doi:10.1137/0606031
    title: Robert E. Tarjan, Amortized computational complexity, SIAM Journal on Algebraic and Discrete Methods 6(2), 1985
    locator: pp. 306 to 318
---

Dynamic table contraction is the rule that a table halves its capacity when a deletion leaves its [load factor](/load-factor/) below $\tfrac14$, while it doubles its capacity when an insertion finds it full, as in [array doubling](/array-doubling/). With these two thresholds, each sequence of $m$ insertions and deletions from an empty table costs at most $3m$, and the capacity is never more than 4 times the number of items. The natural rule "halve when less than half full" is wrong: an alternating sequence near the threshold then resizes at every second operation and costs $\Theta(m^2)$. The proof is the standard two-piece potential of CLRS.

## In plain words

A table that grows when it is full should also shrink when most of it is empty, so that it does not waste memory. The question is when to shrink. If it shrinks as soon as it is less than half full, a table that just grew is only a little more than half full. Two deletions make it shrink, and two insertions make it grow again. Each change copies all items, so a short back-and-forth costs as much as the whole table at each step. The fix is a gap: grow at full, shrink only at a quarter full. After each resize the table is about half full, so many operations must happen before the next resize, and they pay for it.

## When it applies

- A container in one block of memory must support both insertions and deletions, and its memory must stay proportional to its current number of items.
- Growing and shrinking each cost time proportional to the capacity: a copy, a rehash of a [hash table](/hash-table/), a rebuild.
- The program can accept a rare slow operation. If not, use incremental resizing as in [global rebuilding](/global-rebuilding/).

## The template

The table has capacity $c$ (0 or a power of 2) and holds $n \le c$ items. Its load factor is $\alpha = n/c$, with $\alpha = 1$ for the empty table ($c = 0$). It starts empty.

```pseudo id=main
TABLE-INSERT(T, x)
L1  if T.n = T.c then                                ▷ full: expand
L2      resize T to capacity max(1, 2·T.c)            ▷ copies T.n items
L3  store x, T.n ← T.n + 1                            ▷ cost 1

TABLE-DELETE(T, x)
L4  remove x, T.n ← T.n − 1                           ▷ cost 1
L5  if T.n = 0 then free the table, T.c ← 0           ▷ no copy
L6  else if T.n < T.c / 4 then                        ▷ hole: the contraction threshold
L7      resize T to capacity T.c / 2                  ▷ copies T.n items
```

**Cost model.** An insertion or a deletion costs 1, plus 1 for each item copied by a resize. Allocation and freeing cost $O(1)$.

**Lemma (the table is never too empty).** In each reachable state with $n \ge 1$, $c$ is a power of 2 and $n \ge c/4$. So the capacity is at most $4n$.

*Proof.* By induction on the operations. Line L2 gives $c' = 2c$ with $n = c + 1 > c'/4$, or $c' = 1$ with $n = 1$. An insertion without expansion only raises $n$. A deletion that does not reach line L5 or L7 leaves $n \ge c/4$ by the test of line L6. For a contraction, $n$ was at least $c/4$ before the deletion and is less than $c/4$ after it. If $c \le 4$, then $c/4 \le 1$ and $n < c/4$ forces $n = 0$, which line L5 handles. So $c \ge 8$, $c/4$ is an integer, the count before was exactly $c/4$, and the count after is $n = c/4 - 1 \ge 1$. In the new capacity $c/2$ the load is $(c/4 - 1)/(c/2) = \tfrac12 - 2/c \ge \tfrac14$. $\square$

### Proof by the potential method

**Theorem.** With the potential

$$\Phi(T) = \begin{cases} 2n - c & \text{if } \alpha \ge \tfrac12, \\ c/2 - n & \text{if } \alpha < \tfrac12, \end{cases}$$

and $\Phi = 0$ for the empty table, each insertion has amortized cost at most 3 and each deletion at most 2. So $m$ operations from the empty table cost at most $3m$.

$\Phi$ is non-negative in both pieces and is 0 at the start. It is 0 when the table is exactly half full, and it grows as the table moves away from half full in either direction. So it stores the work for the next expansion when the table is above half load, and the work for the next contraction when it is below.

In each case below, $c$ is the capacity before the operation, and $\hat c = (\text{actual cost}) + \Phi_{\text{after}} - \Phi_{\text{before}}$. A non-empty table with $\alpha < \tfrac12$ has $c \ge 2$, so $c$ is even.

*Insertion.*

1. **Into the empty table.** Cost 1. $\Phi$ goes from 0 to $2 \cdot 1 - 1 = 1$. $\hat c = 2$.
2. **Expansion**, $n = c \ge 1$. Cost $c + 1$. Before: $\Phi = 2c - c = c$. After: $n = c + 1$ in capacity $2c$, load above $\tfrac12$, $\Phi = 2(c+1) - 2c = 2$. $\hat c = c + 1 + 2 - c = 3$.
3. **No expansion, $\alpha \ge \tfrac12$ before.** Cost 1. $\Phi$ rises by 2. $\hat c = 3$.
4. **No expansion, $\alpha < \tfrac12$ before and after.** Cost 1. $\Phi$ drops by 1. $\hat c = 0$.
5. **No expansion, $\alpha$ crosses $\tfrac12$.** Then $n$ goes from $c/2 - 1$ to $c/2$, and $\Phi$ goes from 1 to 0. $\hat c = 0$.

*Deletion.*

6. **$\alpha \ge \tfrac12$ before and after.** Cost 1. $\Phi$ drops by 2. $\hat c = -1$.
7. **$\alpha$ crosses below $\tfrac12$, no contraction, $n \ge 1$ after.** Then $n$ goes from $c/2$ to $c/2 - 1$, and $\Phi$ goes from 0 to 1. $\hat c = 2$.
8. **$\alpha < \tfrac12$ before, no contraction, $n \ge 1$ after.** Cost 1. $\Phi$ rises by 1. $\hat c = 2$.
9. **Contraction.** By the lemma, $c \ge 8$ and $n$ goes from $c/4$ to $c/4 - 1$. Cost $1 + (c/4 - 1) = c/4$. Before: $\alpha = \tfrac14$, $\Phi = c/2 - c/4 = c/4$. After: capacity $c/2$, load below $\tfrac12$, $\Phi = c/4 - (c/4 - 1) = 1$. $\hat c = c/4 + 1 - c/4 = 1$.
10. **The table becomes empty.** $n$ goes from 1 to 0, cost 1, and $\Phi$ becomes 0. By the lemma $c \in \{1, 2, 4\}$, with $\Phi$ before equal to 1, 0 and 1. $\hat c = 0$, 1 or 0.

These cases cover each operation. The largest amortized costs are 3 for an insertion and 2 for a deletion. With $\Phi \ge 0 = \Phi(T_0)$, the lemma of the [potential function](/potential-function/) page gives the total bound. $\square$

### Proof by the aggregate method

This proof gives a weaker constant but no formula. Take a resize that acts on a table of capacity $C \ge 1$. It copies at most $C$ items. The table got the capacity $C$ at the previous resize (or at the first insertion). Count the operations after that moment, up to and including this resize.

- If the table got capacity $C$ by an expansion, it then held $C/2 + 1$ items (or 1 item if $C = 1$). To expand again, $n$ must reach $C$; to contract, $n$ must fall below $C/4$. Each takes at least $C/4$ operations.
- If it got capacity $C$ by a contraction, it then held $C/2 - 1$ items. To expand, $n$ must rise by $C/2 + 1$; to contract, $n$ must fall by at least $C/4$.

So each resize that copies at most $C$ items comes after at least $\max(1, C/4)$ operations of its own window, and the windows do not overlap. Charge the copies to the window: at most 4 for each operation. The total over $m$ operations is at most $m + 4m = 5m$. $\square$

### Proof by the accounting method

Read the potential as coins. When $\alpha \ge \tfrac12$, the table holds 2 coins for each item above $c/2$. When $\alpha < \tfrac12$, it holds 1 coin for each item that is missing below $c/2$. Charge 3 for an insertion and 2 for a deletion. An insertion above half load stores 2 coins. An insertion below half load makes 1 coin of the bank unnecessary. A deletion below half load stores 1 coin, and a deletion above half load makes 2 coins unnecessary. The cases of the potential proof show that the coins are enough for each expansion ($c$ coins for $c$ copies) and each contraction ($c/4$ coins for $c/4 - 1$ copies), and that they never go negative.

### Example in numbers

8 insertions and then 7 deletions:

| op | $n$ | $c$ | actual cost | $\Phi$ | $\hat c$ |
|---|---|---|---|---|---|
| insert 1 to 8 | 1 to 8 | 1, 2, 4, 4, 8, 8, 8, 8 | 1, 2, 3, 1, 5, 1, 1, 1 | 1, 2, 2, 4, 2, 4, 6, 8 | 2, 3, 3, 3, 3, 3, 3, 3 |
| delete | 7 | 8 | 1 | 6 | $-1$ |
| delete | 6 | 8 | 1 | 4 | $-1$ |
| delete | 5 | 8 | 1 | 2 | $-1$ |
| delete | 4 | 8 | 1 | 0 | $-1$ |
| delete | 3 | 8 | 1 | 1 | 2 |
| delete | 2 | 8 | 1 | 2 | 2 |
| delete | 1 | 4 | 2 | 1 | 1 |

The last deletion leaves 1 item in a table of capacity 8, which is below a quarter, so the table halves to capacity 4 and copies 1 item.

Five rounds of 1000 insertions followed by 1000 deletions (10,000 operations) cost 17,625 in total, below the bound $3 \cdot 5000 + 2 \cdot 5000 = 25{,}000$. On 300 random sequences of 3000 operations each, no operation had an amortized cost above 3 and $\Phi$ was never negative.

### The bad case: contraction at load one half

Change line L6 to "else if $T.n < T.c/2$". Start with $N = 2^j$ insertions; the table is then full with capacity $N$. Then repeat insert, delete, delete, insert:

| op | $n$ | $c$ | actual cost |
|---|---|---|---|
| insert | $N + 1$ | $2N$ | $N + 1$ (expand) |
| delete | $N$ | $2N$ | 1 |
| delete | $N - 1$ | $N$ | $N$ (contract, copy $N - 1$) |
| insert | $N$ | $N$ | 1 |

After the four operations the table is full again with capacity $N$, so the cycle repeats. Each cycle of 4 operations costs $2N + 3$. With $m = 2N$ operations in total ($N$ insertions to fill, then $N/4$ cycles), the cost is

$$(m - 1) + \frac{m}{8}(m + 3) = \frac{m^2}{8} + \frac{11m}{8} - 1 = \Theta(m^2).$$

For $m = 64$ the cost is 599, for $m = 1024$ it is 132,479, and for $m = 4096$ it is 2,102,783. The same sequences with the threshold $\tfrac14$ cost 127, 2047 and 8191, that is $2m - 1$, and no operation has an amortized cost above 3.

No potential can rescue the rule at $\tfrac12$: the total cost of this sequence is $\Theta(m^2)$, and each valid set of amortized costs must cover it. The cause is that the state right after an expansion is also one deletion away from the contraction threshold, so there is no room to store the work for the next resize.

## Classic examples

- **[Dynamic array](/dynamic-array/) with removal at the end.** A stack in a resizing array halves when it is a quarter full; Sedgewick and Wayne use this rule.
- **[Hash table](/hash-table/) with deletions.** Shrink and [rehash](/rehashing/) when the load factor falls below a quarter of the maximum load; the same gap argument applies.
- **[Dynamic array resizing](/dynamic-array-resizing/)** in general: the rule "double when full, halve when a quarter full" keeps both the time per operation $O(1)$ amortized and the memory $O(n)$.
- **Buffers and queues in a [circular buffer](/circular-buffer/)** that must give memory back when they drain.

## Variations

- **Other thresholds.** With doubling at full and halving at load below a constant $\beta$ with $0 < \beta < \tfrac12$, each resize leaves the table at a load near $\tfrac12$ or near $2\beta$, so a constant fraction of the capacity must change before the next resize. The amortized cost stays $O(1)$, with a constant that grows as $\beta$ approaches 0 or $\tfrac12$. At $\beta = \tfrac12$ the gap is gone and the bad case above appears.
- **Other growth factors.** With growth by $\gamma$ and shrinking by $\gamma$, the contraction threshold must be below $1/\gamma$, the load right after an expansion, by a constant.
- **De-amortized resizing.** Move a few items at each operation to the new table, as in [global rebuilding](/global-rebuilding/), so that each operation takes $O(1)$ worst-case time.

## Pitfalls

- **Contraction at load $\tfrac12$.** The bad case above. It costs $\Theta(m^2)$.
- **A potential that goes negative.** The expansion potential $2n - c$ alone is negative when the table is less than half full, which contraction makes reachable. Using it here would "prove" a false bound for the bad case. The second piece $c/2 - n$ is needed.
- **Forgetting the small tables.** The threshold $n < c/4$ is a fraction for $c < 4$. The cases $c \in \{1, 2, 4\}$ must be handled (here by freeing the table at $n = 0$).
- **Latency.** The amortized bound allows one deletion to copy $c/4 - 1$ items. In a real-time program, use incremental resizing.
- **Persistence.** If an old version of the table can be used again, a version just above a resize threshold can trigger the same costly resize many times. The amortized bound holds only when each operation acts on the newest version.

## Exercises

1. Show that the potential $\Phi = |2n - c|$ also proves an $O(1)$ amortized bound for the rules of this page, and find its constants.
2. Repeat the potential proof for the thresholds "double when full, halve when $n < c/3$", and give the constants.
3. Show that for the threshold $\tfrac12$ the sequence above is the worst case up to a constant factor: each sequence of $m$ operations costs $O(m^2)$.

## References
