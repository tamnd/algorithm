---
tag: 0Y6C78
kind: definition
slug: representation-invariant
name: Representation invariant
aliases:
- Data structure invariant
- Class invariant
area: foundations/correctness-and-invariants
level: intro
summary: A condition that every valid instance of a data structure must satisfy, such as heap order or balance.
prereqs: [invariant]
see_also: [abstraction-function, inductive-invariant, loop-invariant, design-by-contract, heap-property, binary-heap]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 6, Section 6.1 (the heap property)
  - paper: doi:10.1007/BF00289507
    title: C. A. R. Hoare, Proof of correctness of data representations, Acta Informatica 1(4) (1972)
    locator: pp. 271 to 281
  - book: isbn:9780136291558
    title: Bertrand Meyer, Object-Oriented Software Construction, second edition
    locator: Chapter 11 (class invariants)
  - book: isbn:9780201657685
    title: Barbara Liskov and John Guttag, Program Development in Java
    locator: Chapter 5 (data abstraction, representation invariants, exposing the representation)
---

A representation invariant is a condition on the stored fields of a data structure that the constructors establish and every public operation preserves, so it holds between any two calls of the operations. It is an [invariant](/invariant/) of the whole life of the object. The operations assume the condition: their correctness proofs use it, and without it they may return wrong results. The same idea is called a class invariant in [design by contract](/design-by-contract/).

## Definition

Let a data type be implemented by a set $C$ of concrete states, the possible values of its fields. A representation invariant is a predicate $I : C \to \{\text{true}, \text{false}\}$ with two properties.

- Each constructor, called with arguments that meet its [precondition](/precondition/), returns a state $c$ with $I(c)$.
- Let $f$ be a public operation, let $c \in C$ with $I(c)$, and let $x$ be an argument that meets the [precondition](/precondition/) of $f$. Then the state $c'$ that $f$ leaves satisfies $I(c')$.

A state $c$ with $I(c)$ is valid. Suppose the fields are encapsulated, so that no code outside the operations can change them. Then, by induction on the number of calls, every state that the constructors and the public operations produce from valid states is valid. The condition is allowed to be false inside an operation, between two of its steps. It must be true when the operation returns. It must also be true before the operation calls any public operation of the same object, or any outside code that might call back into the object.

The invariant is a property of the representation only. It says nothing about which abstract value a state denotes. That is the job of the [abstraction function](/abstraction-function/).

## Examples and non-examples

### A binary min-heap

Let $L \ge 0$ and let $(U, \le)$ be a totally ordered set. A state is a pair $(a, n)$: an array $a[0 \ldots L-1]$ of items of $U$ and a size $n$. The array positions are 0-based, so the parent of position $i \ge 1$ is $\lfloor (i-1)/2 \rfloor$. The representation invariant of a [binary heap](/binary-heap/) is

$$ I(a, n) \;\equiv\; 0 \le n \le L \;\wedge\; \forall i \in \{1, \ldots, n-1\} : a\left[\left\lfloor \tfrac{i-1}{2} \right\rfloor\right] \le a[i]. $$

The second part is the [heap property](/heap-property/). It does not constrain $a[n \ldots L-1]$: those cells are free space.

Valid states: $([2,5,4,9,6,\ast,\ast], 5)$ is valid, where $\ast$ is any value. The state $([7,1], 0)$ is valid, because the range $1 \le i \le -1$ is empty. The state $([1,2,3,4], 3)$ is valid, and the cell $a[3]$ is free.

Invalid states: $([2,5,1,9,6], 5)$ is not valid, because position 2 has parent 0 and $2 > 1$. The state $([1,2,3], 4)$ is not valid, because $n > L$.

### An operation that keeps the invariant

The operation INSERT$(x)$ has the precondition $n < L$. It writes $x$ at position $n$, then moves it up while it is smaller than its parent.

```python
def insert(a, n, x):
    a[n] = x
    k = n
    while k > 0 and a[(k - 1) // 2] > a[k]:
        a[(k - 1) // 2], a[k] = a[k], a[(k - 1) // 2]
        k = (k - 1) // 2
    return n + 1
```

For $([2,5,4,9,6,\ast,\ast], 5)$ and $x = 3$, the item goes to position 5. Its parent is position 2, which holds 4, so the two swap. The new parent is position 0, which holds 2, and $2 \le 3$, so the loop stops. The result is $([2,5,3,9,6,4,\ast], 6)$, and it is valid.

The proof uses a [loop invariant](/loop-invariant/), named $J(k)$ for the loop variable $k$. Let $p(i) = \lfloor (i-1)/2 \rfloor$, and let $m = n + 1$ be the new size. $J(k)$ says:

- (J1) for every $i$ with $1 \le i < m$ and $i \ne k$: $a[p(i)] \le a[i]$;
- (J2) if $k > 0$, then for every $i$ with $p(i) = k$ and $i < m$: $a[p(k)] \le a[i]$.

The proof has four steps.

1. Start. Before the loop, $k = n = m - 1$. Position $k$ has no child below $m$, so J2 is empty. For $i < k$ the cells and their parents are unchanged, so J1 follows from $I(a, n)$.
2. Step. Suppose $J(k)$ holds, $k > 0$ and $v = a[k] < w = a[p(k)]$. Write $q = p(k)$. The loop swaps the two cells, so now $a[q] = v$ and $a[k] = w$, and the new loop variable is $q$. The pairs that involve $q$ or $k$ are as follows.
   - The pair $(q, k)$ holds: $a[q] = v \le w = a[k]$.
   - For a child $c$ of $k$: $a[k] = w \le a[c]$ by J2 before the swap.
   - For the other child $s$ of $q$ (if it exists and $s < m$): $a[q] = v < w \le a[s]$, and $w \le a[s]$ held before the swap by J1.
   - The pair $(p(q), q)$ is excluded from J1 for the new variable $q$.
   - J2 for $q$ asks that $a[p(q)] \le a[i]$ for the children $i$ of $q$. For $i = k$ it is $a[p(q)] \le w$, which is J1 for the pair $(p(q), q)$ before the swap. For $i = s$ it follows from $a[p(q)] \le w \le a[s]$.
   - All other pairs are unchanged.
3. Termination. Each pass sets $k$ to $\lfloor (k-1)/2 \rfloor \le k - 1$, so $k$ falls by at least 1, and $k \ge 0$ always.
4. End. The loop stops with $k = 0$ or $a[p(k)] \le a[k]$. In both cases the pair at $k$ holds, so J1 holds for all $i$. Together with $0 \le m \le L$, this is $I(a, m)$.

### A second operation: EXTRACT-MIN

The operation EXTRACT-MIN has the precondition $n > 0$. It removes and returns $a[0]$. It moves the last item to position 0 and moves it down, each time swapping with the smaller child, while that child is smaller.

```python
def extract_min(a, n):
    m = a[0]
    n -= 1
    a[0] = a[n]
    k = 0
    while 2 * k + 1 < n:
        c = 2 * k + 1
        if c + 1 < n and a[c + 1] < a[c]:
            c += 1
        if a[k] <= a[c]:
            break
        a[k], a[c] = a[c], a[k]
        k = c
    return m, n
```

Let $m = n - 1$ be the new size. The loop invariant $K(k)$ says:

- (K1) for every $i$ with $1 \le i < m$ and $p(i) \ne k$: $a[p(i)] \le a[i]$;
- (K2) if $k > 0$, then for every child $c < m$ of $k$: $a[p(k)] \le a[c]$.

1. Start. At the start, $k = 0$. Only $a[0]$ has changed, so each pair $(p(i), i)$ with $p(i) \ne 0$ is a pair of old cells, and it holds by $I(a, n)$. K2 is empty.
2. Step. Suppose $K(k)$ holds, $k$ has a child below $m$, $c$ is its smaller child (the left one when the two are equal), and $v = a[k] > w = a[c]$. After the swap, $a[k] = w$, $a[c] = v$, and the new variable is $c$. The pairs that involve $k$ or $c$ are as follows.
   - The pair $(k, c)$ holds: $w \le v$.
   - The pair $(k, s)$ for the other child $s < m$ of $k$ holds: $w \le a[s]$, because $c$ is the smaller child.
   - The pair $(p(k), k)$, if $k > 0$, holds: $a[p(k)] \le w$ by K2 before the swap.
   - The pairs $(c, d)$ for the children $d$ of $c$ are excluded from K1 for the new variable. K2 for $c$ asks $a[k] \le a[d]$, that is $w \le a[d]$. It holds, because $(c, d)$ was a pair of K1 before the swap.
   - Other pairs are unchanged.
3. Termination. Each pass sets $k$ to a child of $k$, and $2k + 1 \ge k + 1$. So $k$ grows by at least 1 and stays below $m$ while the loop runs.
4. End. The loop stops when $k$ has no child below $m$, or when $a[k] \le a[c]$ for the smaller child $c$. In the first case K1 has all the pairs. In the second case the pairs $(k, c)$ and $(k, s)$ hold, since $a[k] \le a[c] \le a[s]$, and K1 has the rest. So $I(a, m)$ holds. If $n = 1$, then $m = 0$, and $I$ holds with no pair.

### Non-examples

Remove the loop from INSERT. The operation then writes $x$ at position $n$ and returns $n + 1$. Started from the valid state above with $x = 1$, it returns $([2,5,4,9,6,1,\ast], 6)$, and the pair at position 5 and parent 2 has $4 > 1$. The operation breaks the invariant. A later call of EXTRACT-MIN then returns the wrong item, because it trusts that $a[0]$ is the least.

A property that holds only for some clients is not a representation invariant. "The queue holds only positive numbers" depends on what one client inserts, and the operations do not establish it.

Representation exposure also breaks the invariant, with no operation at fault. Suppose a constructor stores the array that the caller passes, or a method returns the array $a$ itself. The client keeps a reference and writes $a[0] = 100$ in the valid state $([2,5,4,9,6], 5)$. The state is now invalid, because $a[0] = 100 > a[1] = 5$, and EXTRACT-MIN returns 100 as the minimum. The cure is a defensive copy: copy the array in the constructor, and never return the internal array.

### A sorted array with a size field

The same words fit a sorted array. A state is $(a, n)$ as before, and $I_s(a, n) \equiv 0 \le n \le L \wedge \forall i \in \{0, \ldots, n-2\} : a[i] \le a[i+1]$. Every state valid for $I_s$ is also valid for the heap invariant $I$, because a parent position is smaller than its child position. The converse is false: $([1,3,2], 3)$ is a valid heap and is not sorted. A stronger invariant gives a stronger guarantee to the reader of the fields and costs more work to keep, since INSERT into the sorted array shifts up to $n$ items, which is $\Theta(n)$ in the worst case, against $O(\log n)$ swaps for the heap.

### Checking the invariant at run time

Write the invariant as a Boolean function, here `rep_ok(a, n)`, which tests $0 \le n \le L$ and $a[\lfloor (i-1)/2 \rfloor] \le a[i]$ for $1 \le i < n$. During testing, assert it at the exit of each constructor and of each operation that changes the fields. One check takes $\Theta(n)$ time, so it is usually disabled in production.

## Related definitions

- The [abstraction function](/abstraction-function/) maps a valid state to the abstract value that it denotes. The invariant says which states have a meaning, and the function gives the meaning.
- A [loop invariant](/loop-invariant/) holds at each test of a loop. A representation invariant holds at each call boundary of a data type. The proof for INSERT above uses both.
- An [inductive invariant](/inductive-invariant/) is a predicate that holds at the start and is preserved by each step. A representation invariant is an inductive invariant for the transition system whose steps are the public operations.
- A class invariant is the same notion in [design by contract](/design-by-contract/): the condition is checked when a public routine starts and when it ends.

## References
