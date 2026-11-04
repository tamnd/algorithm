---
tag: RAN1JA
kind: concept
slug: abstraction-function
name: Abstraction function
aliases:
- Representation mapping
- Abstraction map
- Retrieve function
area: foundations/correctness-and-invariants
level: intro
summary: A mapping from a concrete representation to the abstract value it denotes, used to argue that a data structure is correct.
prereqs: [representation-invariant]
see_also: [binary-heap, priority-queue, refinement-calculus, specification, differential-testing, hoare-logic]
sources:
  - paper: doi:10.1007/BF00289507
    title: C. A. R. Hoare, Proof of correctness of data representations, Acta Informatica 1(4) (1972)
    locator: pp. 271 to 281
  - book: isbn:9780201657685
    title: Barbara Liskov and John Guttag, Program Development in Java
    locator: Chapter 5 (abstraction functions and representation invariants)
  - paper: doi:10.1007/3-540-16442-1_14
    title: He Jifeng, C. A. R. Hoare and J. W. Sanders, Data refinement refined, ESOP 1986
    locator: pp. 187 to 196
  - paper: doi:10.1016/0304-3975(91)90224-P
    title: "Martin Abadi and Leslie Lamport, The existence of refinement mappings, Theoretical Computer Science 82(2), 1991"
    locator: pp. 253 to 284
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 6.5 (priority queues)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 2.4 (priority queues)
---

An abstraction function maps each valid concrete state of a data structure to the abstract value that the state stands for. For a binary heap in an array, the abstract value is the multiset of the stored items. With this function, you can state what each operation must do on the abstract level and prove that the code does it. Together with the [representation invariant](/representation-invariant/), it is the standard tool to prove that a data structure is correct. In 1972 Hoare gave a proof method of this kind: a function from concrete to abstract values, an invariant of the concrete values, and a proof that each concrete operation simulates the abstract one.

## In plain words

A data structure has two views. The user sees an abstract thing, such as a bag of numbers from which you can take the smallest. The code sees fields, such as an array and a count. Many arrays can stand for the same bag, and some arrays stand for no bag at all.

The abstraction function is the rule that reads the fields and says which bag they stand for. It is only defined for fields that are in a valid shape. A shape rule, the representation invariant, says which fields are valid.

To prove the code correct, you do this for each operation. Take valid fields. Run the code on the fields. Read the result with the rule. The result must be the same as what the abstract operation gives when you start from the bag that the old fields stand for.

## The idea

Fix an abstract type with a set $V$ of abstract values and, for each operation, an abstract version $f_A$. Fix a representation with a set $C$ of concrete states, a [representation invariant](/representation-invariant/) $I$, and a concrete version $f_C$ of each operation. The abstraction function is a function

$$ \alpha : \{ c \in C \mid I(c) \} \to V. $$

It is a function: each valid state denotes exactly one abstract value. It is usually not injective. It is not defined for invalid states. It is a specification device: it need not be implemented, and when it is, as in the test below, only for checking.

A function does not always exist. A concrete state may stand for several abstract states, or the operations may be nondeterministic. Then one uses an abstraction relation $R \subseteq C \times V$ and proves a forward (downward) or a backward (upward) simulation. Together the two kinds are complete for data refinement (He, Hoare and Sanders 1986). Abadi and Lamport (1991) treat the same problem for refinement mappings, with history and prophecy variables.

The representation is correct when two conditions hold.

- Each constructor $\mathrm{new}_C$ gives a valid state $c$ with $\alpha(c) = \mathrm{new}_A$.
- For each operation $f$, each valid state $c$ and each argument $x$ that meets the [precondition](/precondition/) of $f_A$ at $\alpha(c)$: the state $c' = f_C(c, x)$ is valid, and $\alpha(c') = f_A(\alpha(c), x)$. When $f$ returns a value, the two versions return the same value.

This is a commuting square: run the code and then read the result, or read the state and then run the abstract operation, and you get the same abstract value. The first part of the second condition is the maintenance of the representation invariant. The second part is the simulation of the abstract operation.

The invariant and the function work as a pair. The function is allowed to assume the invariant, so it can be simple. Operations are allowed to assume the invariant on entry, but must restore it on exit.

Two consequences follow.

- **Benevolent side effects.** An operation, even one that only reads, may change the concrete state, as long as the new state $c'$ is valid and $\alpha(c') = \alpha(c)$. Caching, path compression in union-find and the restructuring of a splay tree on a lookup are of this kind. It is also a reason why $\alpha$ is not injective.
- **Representation exposure.** If a client holds an alias to the representation, for example to the array $a$, it can break $I$ between two calls. The proof above then fails, although each operation is correct.

## Examples

### A binary heap as a priority queue

The abstract type is a min [priority queue](/priority-queue/). The queue has a capacity $L$, the length of the array. Its values are multisets $S$ of a totally ordered set with $|S| \le L$. A multiset is a set that counts repeated items, and $S \uplus T$ is the multiset union, which adds the counts. The abstract operations are:

- $\mathrm{insert}_A(S, x) = S \uplus \{x\}$, for $|S| < L$;
- $\mathrm{extractMin}_A(S)$, for $S \ne \emptyset$, returns the pair $(m, S')$, where $m$ is the least item of $S$ and $S'$ is $S$ with one copy of $m$ removed.

The representation is a [binary heap](/binary-heap/): a state $(a, n)$ with the invariant $I(a, n)$ of the page on [representation invariant](/representation-invariant/): $0 \le n \le L$ and $a[\lfloor (i-1)/2 \rfloor] \le a[i]$ for $1 \le i < n$. The abstraction function is

$$ \alpha(a, n) = \{\!\{ a[0], a[1], \ldots, a[n-1] \}\!\}, $$

the multiset of the first $n$ cells. The cells from $n$ on are not read. After EXTRACT-MIN, the old last cell still holds a stale copy of an item, and $\alpha$ ignores it.

Insertion. The precondition $|S| < L$ of the abstract operation is the precondition $n < L$ of INSERT. INSERT writes $x$ at position $n$, then swaps cells inside the range $0 \ldots n$. A swap does not change the multiset of a set of cells. So the multiset of the first $n+1$ cells at the end is the multiset of the first $n$ cells at the start, plus $x$. That is $\alpha(a', n+1) = \alpha(a, n) \uplus \{x\}$.

Minimum. The abstract operation needs the least item, and the code returns $a[0]$. These agree because of the invariant. For $i \ge 1$ with $i < n$, the invariant gives $a[i] \ge a[p(i)]$ for $p(i) = \lfloor (i-1)/2 \rfloor$. Since $p(i) < i$, repeating this reaches position 0 after finitely many steps, so $a[i] \ge a[0]$. For an invalid state this fails: in $([5,1], 2)$ the function $\alpha$ gives $\{\!\{5,1\}\!\}$, and the code returns 5, not 1.

Extraction. EXTRACT-MIN with $n > 0$ saves $m = a[0]$, then writes $a[n-1]$ into $a[0]$, and then swaps cells only inside the range $0 \ldots n-2$. Before the swaps, the first $n-1$ cells hold the old cells $1 \ldots n-2$ and the old $a[n-1]$. That is the old multiset without the copy of $m$ at position 0. Swaps do not change a multiset. So $\alpha(a', n-1) = \alpha(a, n)$ with one copy of $m$ removed. The proof that sift-up restores $I$ in INSERT is on the page on [representation invariant](/representation-invariant/). The proof for sift-down in EXTRACT-MIN is on the same page, in the section on EXTRACT-MIN.

Not injective: $\alpha([1,2,3], 3) = \alpha([1,3,2], 3)$, and both states are valid. It is onto the multisets with at most $L$ items.

The next program checks both conditions on random runs. It keeps a plain multiset as the abstract model, runs INSERT and EXTRACT-MIN on the array, and after each step tests $I$ and $\alpha(a, n) = S$.

```python
import random
from collections import Counter

def p(i): return (i - 1) // 2

def rep_ok(a, n):
    return 0 <= n <= len(a) and all(a[p(i)] <= a[i] for i in range(1, n))

def alpha(a, n):
    return Counter(a[:n])

def insert(a, n, x):
    a[n] = x
    k = n
    while k > 0 and a[p(k)] > a[k]:
        a[p(k)], a[k] = a[k], a[p(k)]
        k = p(k)
    return n + 1

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

random.seed(1)
for _ in range(3000):
    a, n, S = [None] * 12, 0, Counter()
    for _ in range(random.randint(0, 40)):
        if n < 12 and (n == 0 or random.random() < 0.6):
            x = random.randint(0, 6)
            n = insert(a, n, x)
            S[x] += 1
        else:
            m, n = extract_min(a, n)
            assert m == min(S.elements())
            S[m] -= 1
        assert rep_ok(a, n) and alpha(a, n) == +S
print("ok")
```

### A set as a sorted array

The abstract type is a finite set. The state is $(a, n)$ with the invariant that $a[0] < a[1] < \cdots < a[n-1]$. The function is $\alpha(a, n) = \{a[0], \ldots, a[n-1]\}$. The invariant forbids duplicates, so $\alpha(a, n)$ has exactly $n$ items, and DELETE, which removes one cell, removes the item from the set. Membership by binary search uses the order in the invariant: on an unsorted array it can answer "absent" for an item that $\alpha$ says is present.

## Where it is used

- Proofs of data structures. Textbook proofs of heaps, balanced trees and hash tables fit this scheme, even when the text does not name the function.
- Refinement. A step-by-step development from a specification to code proves, at each step, that the new state simulates the old one through such a function. See [refinement calculus](/refinement-calculus/).
- Specifications of modules. A specification written for users states the abstract value and the operations. The abstraction function and the invariant are documentation for the implementer.
- Testing. A test that runs the structure and a simple model side by side, and compares them through $\alpha$, is a form of [differential testing](/differential-testing/). The program above is an example.
- Program verification tools. Tools for [program verification](/program-verification/), such as Dafny and Why3, can check such a proof, when the author writes the function and the invariant as specification code.

## References
