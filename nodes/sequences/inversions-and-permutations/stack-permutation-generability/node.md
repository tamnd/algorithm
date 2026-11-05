---
tag: W8ZW19
kind: problem
slug: stack-permutation-generability
name: Stack permutation generability
aliases:
- Stack generability
area: sequences/inversions-and-permutations
level: core
summary: Asks which output permutations can be produced from an input sequence using a single stack, and characterizes them by forbidden patterns.
prereqs: [permutation, stack]
see_also: [stack-sortable-permutations, catalan-numbers, permutation-pattern-avoidance, balanced-parentheses, deque, bipartiteness-testing, permutation-inverse, shunting-yard-algorithm]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.2.1 (stacks, queues and deques; the exercises on the permutations obtainable with a stack and with input-restricted and output-restricted deques)
  - paper: "Robert E. Tarjan, Sorting using networks of queues and stacks, Journal of the ACM 19(2) (1972) 341-346"
    locator: permutations realizable by networks of stacks and queues
  - paper: "Vaughan R. Pratt, Computing permutations with double-ended queues, parallel stacks and parallel queues, Proceedings of the 5th ACM Symposium on Theory of Computing (1973) 268-277"
    locator: characterizations by forbidden patterns for deques and for parallel stacks
---

Stack permutation generability asks whether a given output sequence can be produced from the input $1, 2, \ldots, n$ by a single [stack](/stack/): read the input in order, push each item, and pop items to the output at any time. A greedy simulation decides it in $\Theta(n)$ time, and Knuth's characterization says that the producible outputs are exactly the [permutations](/permutation/) that avoid the pattern $312$, that is, that have no $i < j < k$ with $p_j < p_k < p_i$. There are $C_n$ of them, the [Catalan numbers](/catalan-numbers/), because each corresponds to a unique balanced sequence of pushes and pops. The same questions for deques, queues and several stacks give a family of problems that Knuth, Tarjan, Even and Itai, and Pratt studied around 1970.

## In plain words

Railway cars numbered 1 to $n$ arrive in order on a track that leads into a dead-end siding. A car can be driven into the siding, and the car nearest the exit can be driven out onto the departure track. Which orders of departure are possible?

Some are easy: drive each car in and straight out, and they leave in the same order. Drive all of them in first, and they leave in reverse. Some orders are impossible. To send car 3 out first, cars 1 and 2 must already be in the siding with 2 in front of 1, so 1 cannot leave before 2. The departure order 3 1 2 can never happen. It turns out that this one shape, a big car followed later by a small one and then a middle one, is the only thing that ever goes wrong.

## Definition

**Machine.** The input is $1, 2, \ldots, n$ in this order, with an initially empty stack. The operation S pushes the next input item, and X pops the top of the stack to the end of the output. A run is a word in S and X with $n$ of each, in which no prefix has more X than S.

**Question.** Given a permutation $p = p_1 \cdots p_n$ of $[n]$, is there a run whose output is $p$? If so, give the run.

**Answer by pattern.** $p$ is producible exactly when it avoids $312$: there are no positions $i < j < k$ with $p_j < p_k < p_i$.

*Why the pattern is forbidden.* When $p_i$ leaves, every smaller item has been pushed, and the items that are smaller and still waiting sit in the stack in increasing order from bottom to top. So $p_j < p_k$, both still waiting, leave in the order $p_k$ before $p_j$, contradicting $j < k$.

*Why it is enough.* The greedy run below pushes only as far as the next output needs, and it fails only when the next output $p_j$ is in the stack but not on top. The stack increases from bottom to top, so its top $t$ is larger than $p_j$, and $t = p_k$ for some $k > j$ since $t$ has not left yet. The item $t$ was pushed while serving some earlier output $p_i$ with $i \le j$, so $t \le p_i$. If $i = j$, the pushes would have stopped at $p_j < t$, so $i < j$, and $p_i \ne t$ because $t$ is still in the stack. So $p_i > p_k > p_j$ with $i < j < k$, a $312$.

## Variants

- **Stack-sortable permutations.** Reverse the roles: which inputs can a stack turn into $1, 2, \ldots, n$? These are the inverses of the producible outputs, the $231$-avoiding permutations, treated on the page on [stack-sortable permutations](/stack-sortable-permutations/).
- **Queue.** A queue outputs items in the order they arrive, so only the identity is producible.
- **Deques.** With a [deque](/deque/) that allows pushes at both ends but pops at one end (output-restricted), or pushes at one end and pops at both (input-restricted), the numbers of producible permutations of $[n]$ for $n = 1, \ldots, 6$ are $1, 2, 6, 22, 90, 394$ in both cases, the large Schröder numbers, though the two sets differ. An unrestricted deque produces $1, 2, 6, 24, 116, 634$ of them, and Pratt showed that the deque class is described by an infinite set of forbidden patterns.
- **Two stacks in parallel.** Each item is pushed onto one of two stacks. A permutation can be handled this way exactly when a conflict graph on the items, joining two items that cannot share a stack, is [bipartite](/bipartiteness-testing/), a result of Even and Itai. Counted as sortable inputs, there are $1, 2, 6, 23, 103, 513, 2760$ of them for $n = 1, \ldots, 7$.
- **Stacks in series.** Two stacks in series are much harder to characterize. Applying the greedy [stack sorting](/stack-sortable-permutations/) pass twice, West's two-stack sorting, sorts $1, 2, 6, 22, 91, 408, 1938$ permutations for $n = 1, \ldots, 7$, which is $2(3n)!/((n+1)!(2n+1)!)$ by a theorem of Zeilberger.
- **Producing a given output from a given input.** For an input $a$ and an output $b$ that are both permutations of the same items, rename the items by their positions in $a$. The question becomes the standard one for $b$ renamed.

## Examples

**A producible output.** $p = 3\,2\,4\,1$ avoids $312$. The greedy run pushes 1, 2, 3, pops 3, pops 2, pushes 4, pops 4 and pops 1, the word SSSXXSXX.

**An impossible one.** $p = 3\,1\,2$. After pushing 1, 2, 3 and popping 3, the top is 2, but 1 is needed, and the input is empty. The triple $3, 1, 2$ itself is the $312$ pattern.

**Counting.** For $n = 1, \ldots, 7$ there are $1, 2, 5, 14, 42, 132, 429$ producible outputs, the Catalan numbers $C_n = \frac{1}{n+1}\binom{2n}{n}$. For $n = 3$ all permutations except $312$ are producible.

**The run as a bracket word.** Writing S as "(" and X as ")" turns every run into a [balanced parentheses](/balanced-parentheses/) word. Different runs give different outputs, which is why the count is the Catalan number.

## Known algorithms

**Greedy simulation.** Keep the next input item $c$ and the stack. For each output value $p_j$ in turn, push items while the stack is empty or its top is not $p_j$ and input remains, then pop if the top is $p_j$ and report failure otherwise. Each item is pushed and popped at most once, so the time is $\Theta(n)$ and the space is $O(n)$. On success the sequence of operations is the run, and it is the only one: an item must be popped exactly when it is the next output, and pushed only when it is needed or something after it is.

```pseudo
STACK-PRODUCIBLE(p[1 .. n])
1  S ← empty stack, c ← 1, run ← empty word
2  for j ← 1 to n do
3      while (S is empty or top(S) ≠ p[j]) and c ≤ n do
4          push c on S, c ← c + 1, append S to run
5      if S is empty or top(S) ≠ p[j] then return "impossible"
6      pop S, append X to run
7  return run
```

**Pattern test.** The greedy run is in effect a linear-time test for the pattern $312$. Any [pattern matching](/permutation-pattern-matching/) routine for patterns of length 3 gives the same answer, also in linear time.

**Two parallel stacks.** Build the conflict graph and 2-color it. Naively this is $O(n^2)$ edges; more careful methods avoid building all edges.

## Bounds

- **Time.** $\Theta(n)$: every item must be read, and the simulation does $2n$ stack operations.
- **Count.** $C_n \sim 4^n / (n^{3/2}\sqrt{\pi})$ producible outputs out of $n!$ permutations, so a uniform random permutation is producible with a probability that tends to 0 faster than any exponential $c^{-n}$.
- **Information.** A run is a word of $2n$ letters, so a producible permutation is described in $2n$ bits, against $\lg n! \approx n \lg n$ bits for a general permutation.

## Reductions

- **To and from stack sorting.** $p$ is producible from $1 \cdots n$ exactly when $p^{-1}$ can be sorted by one stack, because running the same S and X word with the input relabeled by $p^{-1}$ produces the identity. So each problem reduces to the other through the [inverse](/permutation-inverse/) in $O(n)$ time.
- **To pattern avoidance.** Generability is avoidance of $312$, a special case of [pattern avoidance](/permutation-pattern-avoidance/).
- **To balanced words.** The producible permutations are in bijection with balanced words of $n$ pairs of brackets, and hence with binary trees of $n$ nodes and the other Catalan families.

## Applications

- **Railway shunting.** Rearranging cars with a dead-end siding is the classic picture of the problem, used by Knuth.
- **Parsing and evaluation.** An operator-precedence parser such as the [shunting-yard algorithm](/shunting-yard-algorithm/) reorders tokens through a stack, so the orders it can produce are stack permutations.
- **Testing a stack implementation.** Given a log of pushes and the order of pops, the greedy check tells whether the log is consistent with a correct stack.
- **Combinatorics.** The bijection with bracket words is a standard way to count Catalan families and to generate them uniformly at random.

## References
