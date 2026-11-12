---
tag: VZN265
kind: algorithm
slug: attribute-closure-algorithm
name: Attribute closure algorithm
aliases:
- linear closure algorithm
- Beeri-Bernstein closure algorithm
area: systems/database-algorithms
level: core
summary: "Computes the closure X+ of an attribute set under functional dependencies in linear time, with one counter per FD for its left-side attributes not yet reached."
model: word-ram
complexity:
  vars: {n: the number of attributes, m: the total number of attribute occurrences in F}
  time: {worst: Θ(n + m), average: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1979
  people: [Catriel Beeri, Philip A. Bernstein]
  note: Beeri and Bernstein gave the linear-time closure algorithm in their 1979 paper on the design of normal form schemas.
prereqs: [attribute-closure-problem, loop-invariant]
see_also: [horn-sat-forward-chaining, unit-propagation, breadth-first-search, armstrongs-axioms, dependency-implication-problem, minimal-cover-problem, third-normal-form-synthesis]
sources:
  - paper: doi:10.1145/320064.320066
    title: Catriel Beeri and Philip A. Bernstein, Computational problems related to the design of normal form relational schemas, ACM Transactions on Database Systems 4(1), 30 to 59 (1979)
    locator: the linear-time membership algorithm for functional dependencies, with counters and attribute lists
  - book: isbn:9780881751888
    title: Jeffrey D. Ullman, Principles of Database and Knowledge-Base Systems, Volume I, Computer Science Press (1988)
    locator: Section 7.3 (computing closures; the simple algorithm and the linear-time version)
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Section 8.2 (the closure algorithm for functional dependencies)
  - paper: doi:10.1016/0743-1066(84)90014-1
    title: William F. Dowling and Jean H. Gallier, Linear-time algorithms for testing the satisfiability of propositional Horn formulae, Journal of Logic Programming 1(3), 267 to 284 (1984)
    locator: the same counter technique for Horn clauses
---

The attribute closure algorithm computes $X^+$, the set of attributes that a set $X$ determines under a set $F$ of [functional dependencies](/functional-dependency/). It keeps, for each FD, a counter of the left-side attributes that are not yet processed, and a list, for each attribute, of the FDs whose left side holds it. When a counter reaches zero, the FD fires and adds its right side. Beeri and Bernstein (1979) gave this version, which runs in time linear in the size of $F$. The plain fixpoint loop can take time $|U|$ times larger.

## In plain words

Each rule says "if you know all of these columns, you also know those". Give each rule a counter: the number of its needed columns that you have not handled yet. Keep a to-do list of known columns. Take a column from the list, and lower the counter of each rule that needs it. When a counter reaches zero, the rule is ready: add its new columns to the known set and to the to-do list. Stop when the list is empty. The known set is the answer. Each column is handled once, and each counter goes down once per needed column, so the work is about the size of the rules.

## The problem

The input is a finite attribute set $U$, a list $F$ of FDs $W_1 \to Z_1, \ldots, W_k \to Z_k$ over $U$, and a set $X \subseteq U$. The output is $X^+ = \{A \in U : F \models X \to A\}$. This is the [attribute closure problem](/attribute-closure-problem/). By [Armstrong's axioms](/armstrongs-axioms/), $X^+$ is the least set that holds $X$ and holds $Z_i$ whenever it holds $W_i$.

## The algorithm

The array $\mathit{count}[1..k]$ holds, for each FD, the number of attributes of its left side that have not yet left the queue. The list $\mathit{list}[A]$ holds the indices $i$ with $A \in W_i$. The queue holds the attributes that are in the closure and not yet processed.

```pseudo id=main
LINEAR-CLOSURE(F, X)                       ▷ F = W_1 → Z_1, ..., W_k → Z_k
L1  for i ← 1 to k do count[i] ← |W_i|
L2  for each attribute A do list[A] ← the indices i with A ∈ W_i
L3  closure ← X; queue ← the attributes of X
L4  for each i with count[i] = 0 do ADD(Z_i)
L5  while queue is not empty do
L6      A ← remove the first attribute of queue
L7      for each i in list[A] do
L8          count[i] ← count[i] − 1
L9          if count[i] = 0 then ADD(Z_i)
L10 return closure

ADD(Z)
L11 for each B in Z do
L12     if B ∉ closure then add B to closure; append B to queue
```

Line L4 fires the FDs with an empty left side, which hold before any attribute is processed. Store $\mathit{closure}$ as a bit array indexed by attribute, so that the test in line L12 takes constant time.

## Example

Take $U = \{C, T, H, R, S, G\}$ and the FDs

| $i$ | FD | $|W_i|$ |
| --- | --- | --- |
| 1 | $C \to T$ | 1 |
| 2 | $HR \to C$ | 2 |
| 3 | $HT \to R$ | 2 |
| 4 | $CS \to G$ | 2 |
| 5 | $HS \to R$ | 2 |

The lists are $\mathit{list}[C] = (1, 4)$, $\mathit{list}[T] = (3)$, $\mathit{list}[H] = (2, 3, 5)$, $\mathit{list}[R] = (2)$, $\mathit{list}[S] = (4, 5)$ and $\mathit{list}[G] = ()$. Compute $HS^+$:

| step | attribute removed | counters lowered | fired | closure | queue after |
| --- | --- | --- | --- | --- | --- |
| start | | | | $HS$ | $H, S$ |
| 1 | $H$ | 2 to 1, 3 to 1, 5 to 1 | | $HS$ | $S$ |
| 2 | $S$ | 4 to 1, 5 to 0 | 5: adds $R$ | $HSR$ | $R$ |
| 3 | $R$ | 2 to 0 | 2: adds $C$ | $HSRC$ | $C$ |
| 4 | $C$ | 1 to 0, 4 to 0 | 1: adds $T$; 4: adds $G$ | $HSRCTG$ | $T, G$ |
| 5 | $T$ | 3 to 0 | 3: $R$ is present | $HSRCTG$ | $G$ |
| 6 | $G$ | | | $HSRCTG$ | empty |

So $HS^+ = U$, and $HS$ is a superkey. The run made 9 decrements, which is the sum $1 + 2 + 2 + 2 + 2$ of the left-side sizes, and pushed each of the 6 attributes once.

## Correctness

The proof uses a [loop invariant](/loop-invariant/) of line L5. Let $P$ be the set of attributes already removed from the queue. At each test of line L5: (a) $\mathit{closure} \subseteq X^+$; (b) $P$ and the queue are disjoint and their union is $\mathit{closure}$; (c) $\mathit{count}[i] = |W_i - P|$ for each $i$; (d) each FD with $\mathit{count}[i] = 0$ has $Z_i \subseteq \mathit{closure}$. Part (a) gives soundness: an attribute is added only when the left side of its FD is inside the closure. When the loop stops, the queue is empty, so $P = \mathit{closure}$. By (c) and (d), each FD with $W_i \subseteq \mathit{closure}$ has $Z_i \subseteq \mathit{closure}$. So the closure is a set that holds $X$ and is closed under $F$, and it contains $X^+$, the least such set. The full proof is below.

## Complexity

Let $n = |U|$ and $m = \sum_i (|W_i| + |Z_i|)$.

- Lines L1 and L2 take $O(n + m)$: one pass over all left sides.
- Each attribute enters the queue at most once, because line L12 appends it only when it is new. So lines L5 and L6 run at most $n$ times.
- Line L8 runs once per pair $(A, i)$ with $A \in W_i$, so at most $\sum_i |W_i| \le m$ times in total.
- Each FD fires at most once: in line L4 if $W_i = \emptyset$, and otherwise in line L9 when its counter goes from 1 to 0. So ADD reads each $Z_i$ at most once, $O(m)$ in total.

The time is $\Theta(n + m)$ and the extra space is $\Theta(n + m)$ for the counters, the lists, the bit array and the queue. With attributes given as strings, a hash table maps them to integers first, in expected linear time.

**Comparison with the naive loop.** The naive algorithm scans all of $F$ and adds $Z_i$ when $W_i \subseteq \mathit{closure}$, and repeats until a scan adds nothing. Each scan costs $O(m)$, and each scan except the last adds an attribute, so the time is $O(n \cdot m)$. The bound is reached: on the chain $A_{n-1} \to A_n, \ldots, A_1 \to A_2$, listed in this order, with $X = \{A_1\}$, each scan adds one attribute. The implementation measures $n = 40$ passes for the naive loop and $39$ decrements for the counter algorithm.

## Properties

- **Deterministic.** The order of the queue does not change the result, only the order in which attributes enter the closure.
- **Each FD fires once.** This is the key difference from the naive loop, which tests each FD again in each pass.
- **The setup can be shared.** Lines L1 and L2 depend only on $F$. To compute many closures under one $F$, build the lists once and copy only the counters.
- **Monotone.** A larger $X$ gives a larger result, and so does a larger $F$.

## Variants and improvements

- **Membership test with early exit.** To decide $F \models X \to Y$, stop as soon as all of $Y$ is in the closure. Beeri and Bernstein state the algorithm in this form.
- **Horn satisfiability.** The same counters decide the satisfiability of a Horn formula in linear time: [forward chaining for Horn-SAT](/horn-sat-forward-chaining/) of Dowling and Gallier (1984). The closure is the least model, and the propagation is [unit propagation](/unit-propagation/) on Horn clauses.
- **Graph search.** If each left side has one attribute, the counters are all 1 and the algorithm is a [breadth-first search](/breadth-first-search/) from $X$.
- **Datalog.** Bottom-up evaluation of a propositional Datalog program is this algorithm. [Semi-naive evaluation](/semi-naive-evaluation/) applies the same idea, "use only the new facts", to rules with variables.
- **Incremental closure.** To add an FD $W \to Z$ to $F$ after the run, set its counter to $|W - \mathit{closure}|$, and continue the loop if it is 0.

## When to use it

Use the counter algorithm when $F$ is large or when the closure is a step in a larger computation, such as key finding, cover computation or 3NF synthesis, which call it many times. For a handful of FDs, the naive loop is simpler and fast enough, because it usually needs few passes.

## Pitfalls

- **Repeated attributes in a left side.** If a left side is stored as a list such as $(A, A, B)$, its counter starts at 3 but $\mathit{list}[A]$ holds the FD once, so the counter never reaches 0. Remove repeats first, so that the counter is the size of the set $W_i$.
- **Forgetting empty left sides.** An FD $\emptyset \to Z$ never has its counter lowered, so line L4 must fire it at the start. Without line L4, the algorithm misses $Z$ and all that follows from it.
- **Adding an attribute twice.** If line L12 does not test membership, an attribute can enter the queue more than once, and its FDs get decremented twice. A counter can then reach 0 too early, which gives a wrong answer.
- **Rebuilding the lists.** In a loop that computes many closures under one $F$, rebuilding the lists each time multiplies the cost by the number of calls with no need.

## Implementations

## History

Armstrong's axioms (1974) reduced implication of FDs to the closure $X^+$, and the early papers computed it by repeated scans of $F$. Beeri and Bernstein (1979) gave the linear-time algorithm with counters and attribute lists. They used it for the membership problem and as a step of Bernstein's [3NF synthesis](/third-normal-form-synthesis/). Dowling and Gallier (1984) published the same technique for Horn formulas. Ullman's textbook (1988) gives both the simple loop and the linear version.

## References
