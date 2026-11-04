---
tag: 6RA926
kind: technique
slug: fast-and-slow-pointers
name: Fast and slow pointers
aliases:
- tortoise and hare
- Floyd's cycle detection
area: techniques/two-pointers-and-windows
level: intro
summary: Two pointers moving at different speeds detect cycles or find midpoints in a sequence or functional graph.
prereqs: [two-pointers, linked-list, functional-graph]
see_also: [floyd-cycle-detection, brent-cycle-detection, cycle-detection, functional-graph, pollard-rho, brent-pollard-rho, singly-linked-list, duplicate-detection]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition
    locator: Section 3.1, exercise 6 (Floyd's method of finding a period with two sequences x_n and x_2n) and its answer
  - paper: doi:10.1007/BF01933190
    title: Richard P. Brent, An improved Monte Carlo factorization algorithm, BIT 20, 1980
    locator: pp. 176 to 184 (cycle finding with powers of two, compared with Floyd's method)
  - url: https://cp-algorithms.com/others/tortoise_and_hare.html
    title: cp-algorithms, Floyd's linked list cycle finding algorithm
    locator: sections Proposed algorithm and Why does it work
  - url: https://cp-algorithms.com/algebra/factorization.html
    title: cp-algorithms, Integer factorization
    locator: section Pollard's rho algorithm (Floyd's and Brent's cycle detection)
---

The fast and slow pointers technique runs two pointers along the same sequence at different speeds, usually one step and two steps at a time. On a sequence $x_{i+1} = f(x_i)$ over a finite set, which must end in a cycle, the two pointers meet inside the cycle; this is Floyd's "tortoise and hare" [cycle detection](/floyd-cycle-detection/), and from the meeting point the start and the length of the cycle follow. On a linked list without a cycle, the slow pointer is at the middle when the fast one reaches the end. The technique uses $O(1)$ extra memory, where a table of visited items would need memory for every item. It is the different-speed form of the [two-pointer technique](/two-pointers/).

## In plain words

Two runners start at the same place on a track. One runs twice as fast as the other. If the track is a straight road with an end, the fast runner reaches the end first, and at that moment the slow runner is halfway. If the track ends in a loop, the fast runner goes round and round and catches up with the slow runner from behind, inside the loop. So a meeting proves that there is a loop.

The trick is that you never have to remember where you have been. Two markers are enough, whatever the length of the road or the loop.

## When it applies

- **Sequences given by a function.** $x_0$ is given and $x_{i+1} = f(x_i)$, over a finite set. The sequence must repeat, and it has the shape of the letter $\rho$: a tail of $\mu$ items, then a cycle of $\lambda$ items. The structure of all such sequences is a [functional graph](/functional-graph/).
- **Linked lists.** Each node has one next pointer. The list ends at a null pointer or runs into a cycle; see [singly linked list](/singly-linked-list/).
- **Memory is the limit.** A [hash table](/hash-table/) of visited items finds the cycle with about $\mu + \lambda$ evaluations of $f$, but it stores $\mu + \lambda$ items. Fast and slow pointers store two.
- **Only equality tests.** The method needs only to test $x = y$. It needs no order and no hashing.
- **Signals that it does not apply.** If $f$ is not a function of the current item alone (the next step depends on history), or if the sequence can be infinite without repeats, the method gives no guarantee.

## The template

Let $\mu$ be the smallest index such that $x_\mu$ occurs again later, and $\lambda \ge 1$ the smallest number with $x_{\mu + \lambda} = x_\mu$. Then $x_0, \ldots, x_{\mu + \lambda - 1}$ are distinct, and for $i < j$:
$$ x_i = x_j \iff i \ge \mu \text{ and } \lambda \mid (j - i). $$

```pseudo id=main
FLOYD(f, x0)
L1  t ← f(x0); h ← f(f(x0))                       ▷ t = x_1, h = x_2
L2  while t ≠ h do t ← f(t); h ← f(f(h))           ▷ t = x_i, h = x_2i
L3  t ← x0; μ ← 0
L4  while t ≠ h do t ← f(t); h ← f(h); μ ← μ + 1   ▷ t = x_j, h = x_(ν+j)
L5  λ ← 1; h ← f(t)
L6  while t ≠ h do h ← f(h); λ ← λ + 1
L7  return (μ, λ)
```

**The invariant of the first loop.** After line L1 and after each iteration of line L2, for some $i \ge 1$:

> **(H)** $t = x_i$ and $h = x_{2i}$, and $x_{i'} \ne x_{2i'}$ for all $1 \le i' < i$.

**Why the pointers never skip the meeting.** The gap between the two indices is $2i - i = i$, and it grows by exactly 1 per iteration. So the loop tests every $i = 1, 2, 3, \ldots$ in turn; the fast pointer cannot jump over the slow one, because the test is on the pair of indices $(i, 2i)$, not on positions in the cycle. By the rule above, $x_i = x_{2i}$ holds exactly when $i \ge \mu$ and $\lambda \mid i$. So the loop stops at
$$ \nu = \text{the smallest multiple of } \lambda \text{ with } \nu \ge \max(\mu, 1), $$
and $\mu \le \nu \le \mu + \lambda$. (Knuth, Vol. 2, Section 3.1, exercise 6, states this bound.) The loop of line L2 always ends, after $\nu - 1 \le \mu + \lambda - 1$ iterations.

**Finding $\mu$.** Line L3 puts $t$ at $x_0$, while $h = x_\nu$. Both move one step at a time, so $t = x_j$ and $h = x_{\nu + j}$. Since $\nu > 0$ and $\lambda \mid \nu$, the rule gives $x_j = x_{\nu + j}$ if and only if $j \ge \mu$. So the first meeting is at $j = \mu$, the start of the cycle, and the loop of line L4 counts exactly $\mu$ steps.

**Finding $\lambda$.** From $x_\mu$, line L6 steps $h$ around the cycle until it comes back to $x_\mu$, which takes exactly $\lambda$ steps.

**Cost.** Line L1 and the loop of line L2 make $3\nu$ evaluations of $f$, the loop of line L4 makes $2\mu$, and line L5 with the loop of line L6 make $\lambda$. In total at most $3(\mu + \lambda) + 2\mu + \lambda$, which is $O(\mu + \lambda)$. The memory is a constant number of items.

**The middle of a list.** With `slow ← head`, `fast ← head`, and the loop "while fast ≠ NIL and next(fast) ≠ NIL: slow ← next(slow); fast ← next(next(fast))", after $k$ iterations slow is at node $k$ and fast at node $2k$. The loop stops at the first $k$ with $2k \ge n - 1$, so slow ends at node $\lfloor n/2 \rfloor$ (counting from 0): the middle for odd $n$, the second of the two middles for even $n$.

## Classic examples

- **Cycle in a linked list.** Run lines L1 and L2 with $f = $ next; a null pointer on the fast side means no cycle. Lines L3 and L4 return the first node of the cycle.
- **Middle of a linked list.** As above, in one pass and without the length. Used to split a list for merge sort on lists.
- **Palindrome linked list.** Find the middle, reverse the second half, compare the halves.
- **Find the duplicate number.** An array $A[0 \ldots n]$ with values in $1, \ldots, n$ has a repeated value. Take $f(i) = A[i]$ and $x_0 = 0$. No value is 0, so $x_0$ has no predecessor and $\mu \ge 1$. The start of the cycle $x_\mu$ has two predecessors in the sequence, $x_{\mu - 1}$ in the tail and $x_{\mu + \lambda - 1}$ in the cycle. They are different indices with $A[x_{\mu-1}] = A[x_{\mu+\lambda-1}] = x_\mu$, so $x_\mu$ is the repeated value. Floyd's method finds it in $O(n)$ time and $O(1)$ space without changing $A$.
- **Example of the $\rho$ shape.** Let $f(2) = 0$, $f(0) = 6$, $f(6) = 3$, $f(3) = 1$, $f(1) = 6$, and $x_0 = 2$. The sequence is $2, 0, 6, 3, 1, 6, 3, 1, \ldots$, so $\mu = 2$ and $\lambda = 3$. The first loop stops at $\nu = 3$, where $x_3 = x_6 = 3$; the second loop meets at $x_2 = 6$. The whole run makes 16 evaluations of $f$.
- **Pollard's rho method.** To factor $N$, iterate $x \mapsto x^2 + c \bmod N$; modulo an unknown prime factor $p$, the sequence enters a cycle after about $\sqrt{p}$ steps on average. Floyd's or Brent's method finds the cycle without storing the sequence, and a gcd test detects the meeting modulo $p$. See [Pollard's rho](/pollard-rho/).
- **Period of a pseudo-random generator.** The generator $x_{i+1} = f(x_i)$ has tail $\mu$ and period $\lambda$, which the method measures with constant memory. This is the setting of Knuth's exercise.

## Variations

- **Brent's method.** Instead of a pointer at half speed, keep a saved item and move one pointer; save the current item each time the number of steps since the last save reaches a power of two. The pointer meets the saved item within the first block whose length is at least $\lambda$ and that starts at or after index $\mu$, and the number of steps since the last save is $\lambda$ itself. Brent (1980) reports that this needs on average about 36 percent fewer evaluations of $f$ than Floyd's method, and that it speeds up Pollard's rho method by about 24 percent. See [Brent's cycle detection](/brent-cycle-detection/) and [Brent's variant of Pollard's rho](/brent-pollard-rho/).
- **Other speeds.** Speeds 1 and $k$ also meet: the gap $(k - 1) i$ then runs over the multiples of $k - 1$, and a meeting happens at the first $i \ge \mu$ with $\lambda \mid (k - 1) i$. Speeds 1 and 2 are the usual choice because they evaluate each index of the gap.
- **Gosper's method and stack-based methods.** Store a small number of items, for example $O(\log(\mu + \lambda))$, to find $\lambda$ with fewer evaluations; these trade a little memory for speed.
- **Hash table of visited items.** About $\mu + \lambda$ evaluations, the fewest possible, with $\mu + \lambda$ items of memory.
- **Fixed gap.** Two pointers at the same speed with a fixed gap $k$: the slow pointer is $k$ nodes behind the end when the fast one reaches it, which finds the $k$-th node from the end of a list in one pass.

## Pitfalls

- **Null checks.** On a list that may end, test that the fast pointer and its next node exist before moving it two steps.
- **Testing before moving.** If both pointers start at $x_0$ and the test comes first, the loop stops at once. Move first, then test, as in line L1.
- **Meeting point is not the start of the cycle.** The first meeting is at $x_\nu$, which is in the cycle but in general not $x_\mu$. The second phase is needed for $\mu$.
- **Wrong reset in the second phase.** Only one pointer goes back to $x_0$; the other stays at $x_\nu$. Both must then move at speed 1.
- **Equality of values versus identity.** On linked lists compare node identities, not stored values: two different nodes can hold the same value.
- **Changing the structure.** Methods that mark visited nodes by changing them, such as reversing pointers, also use $O(1)$ memory, but they destroy the input; fast and slow pointers only read.

## Exercises

1. Prove that the first loop of FLOYD stops at the smallest multiple of $\lambda$ that is at least $\max(\mu, 1)$, and give an input with $\nu = \mu + \lambda$.
2. Show that if the fast pointer moves 3 steps per iteration, the pointers still meet, and find the first meeting index in terms of $\mu$ and $\lambda$.
3. Return the node where two singly linked lists without cycles first share a node, in $O(m + n)$ time and $O(1)$ space. (Hint: two pointers that switch lists at the end.)
4. A number is *happy* if repeatedly replacing it by the sum of the squares of its digits reaches 1. Decide if a number is happy with $O(1)$ memory, and prove that the sequence always enters a cycle.
5. Prove that Brent's method finds $\lambda$ exactly, and bound its number of evaluations of $f$ by a constant times $\mu + \lambda$.
6. Explain why, in the find-the-duplicate example, $x_0 = 0$ must be in the tail, and what goes wrong if the values may include 0.

## References
