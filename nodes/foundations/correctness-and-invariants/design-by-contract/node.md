---
tag: 3AE0G6
kind: technique
slug: design-by-contract
name: Design by contract
aliases:
- Contract-based programming
area: foundations/correctness-and-invariants
level: intro
summary: Specifying each routine by preconditions, postconditions and invariants, which the code is checked against.
prereqs: [precondition, postcondition, representation-invariant]
see_also: [assertion, hoare-triple, hoare-logic, loop-invariant, specification, property-based-testing, binary-heap]
sources:
  - url: "https://en.wikipedia.org/wiki/Design_by_contract"
    locator: article Design by contract, sections History and Description
  - book: isbn:9780136291558
    title: Bertrand Meyer, Object-Oriented Software Construction, second edition, Prentice Hall (1997)
    locator: Chapter 11 (Design by Contract, building reliable software) for assertions, the class invariant and the precondition availability rule; Chapter 12 (When the contract is broken, exception handling) for rescue and retry; Chapter 16 for contracts and inheritance
  - paper: doi:10.1109/2.161279
    title: Bertrand Meyer, Applying "Design by Contract", IEEE Computer 25(10), 1992
    locator: pp. 40 to 51
  - paper: doi:10.1145/363235.363259
    title: C. A. R. Hoare, An axiomatic basis for computer programming, Communications of the ACM 12(10), 1969
    locator: pp. 576 to 580
  - paper: doi:10.1090/psapm/019/0235771
    title: R. W. Floyd, Assigning meanings to programs, Proceedings of Symposia in Applied Mathematics 19, AMS (1967)
    locator: pp. 19 to 32
  - paper: doi:10.1145/62138.62141
    title: Barbara Liskov, Data abstraction and hierarchy, keynote address, Addendum to the Proceedings of OOPSLA '87 (1987)
    locator: pp. 17 to 34, the section on type hierarchy (the substitution property)
  - paper: doi:10.1145/197320.197383
    title: Barbara Liskov and Jeannette Wing, A behavioral notion of subtyping, ACM Transactions on Programming Languages and Systems 16(6), 1994
    locator: pp. 1811 to 1841, the subtype requirement and the rules for preconditions, postconditions and invariants
---

Design by contract is a way to specify and build software in which each routine has a contract with its callers. The contract has a [precondition](/precondition/) that the caller must make true, a [postcondition](/postcondition/) that the routine must make true, and, for a class, a class invariant (a [representation invariant](/representation-invariant/)) that every public routine keeps. Bertrand Meyer named the method in the 1980s and built it into the language Eiffel. It rests on the [assertions](/assertion/) of Floyd (1967) and the triples of Hoare (1969). The conditions are written in the code, so tools can check them while the program runs, or prove them.

## In plain words

A routine and its caller make a deal. The caller promises that the input is fit for the routine. The routine promises that the result has certain properties, if the input was fit. Each side has a duty and a gain. The duty of the caller is the gain of the routine, because the routine may assume the input is fit. The duty of the routine is the gain of the caller, because the caller may rely on the result.

When a promise is broken and the checks are on, the program stops with an error at the first place where the break is seen, and the error says who broke the promise. If the input was bad, the caller has a bug. If the input was good and the result is bad, the routine has a bug. This makes errors easy to find.

## When it applies

- A data structure or a class has operations that must keep a shape, such as the heap order of a [binary heap](/binary-heap/). The shape is a [representation invariant](/representation-invariant/).
- A routine is correct only for some inputs, and you want to say which. A binary search needs a sorted array.
- Many people write code that calls the same routine, and the rules of use must be written down and checked.
- You want tests that need no expected output: the contract judges each run. This works well together with [property-based testing](/property-based-testing/).

## The template

For each routine $r$ of a class with the invariant $\mathit{INV}$, write the following.

1. **Precondition $\mathit{Pre}_r$.** A condition on the arguments and on the state at the call. The caller must make it true. Every feature that it uses must be available to every client that may call the routine, so that the caller can check it (Meyer's precondition availability rule). For a stack, "not full" is available through a query `is_full`.
2. **Postcondition $\mathit{Post}_r$.** A condition on the state and the result at return. It may refer to the values that the state had at entry, written $\mathit{old}\ e$ in Eiffel.
3. **Class invariant $\mathit{INV}$.** A condition on the fields, true after each constructor and at the entry and the exit of each public routine. The invariant is required only at calls from clients (qualified calls in Eiffel). A routine of the class that calls another of its own routines may do so while the invariant is false, if it restores the invariant before it returns to its client. This is why private helper routines need not keep the invariant.

The contract of $r$ is then the [Hoare triple](/hoare-triple/)

$$ \{\, \mathit{INV} \wedge \mathit{Pre}_r \,\}\ \ r\ \ \{\, \mathit{INV} \wedge \mathit{Post}_r \,\}. $$

If every constructor establishes $\mathit{INV}$ and every public routine meets its triple, then every state that a client can reach by legal calls satisfies $\mathit{INV}$. This is the induction of the page on [representation invariant](/representation-invariant/). Hoare's 1969 paper is the source of the triples.

```pseudo id=main
CALL(r, args)
L1  check INV                        (if false: the class has a bug, or its fields were changed from outside)
L2  check PRE_r(args)                (if false: the caller has a bug)
L3  old ← save the values that POST_r needs
L4  result ← BODY_r(args)
L5  check POST_r(args, result, old)  (if false: the routine has a bug)
L6  check INV                        (if false: the routine, and so the class, has a bug)
L7  return result
```

The holes are $\mathit{PRE}_r$, $\mathit{POST}_r$, $\mathit{INV}$ and $\mathit{BODY}_r$.

In Eiffel the contract is part of the text of the routine:

```eiffel
push (x: G)
    require
        not_full: count < capacity
    do
        -- store x on the stack
    ensure
        pushed: item = x
        one_more: count = old count + 1
    end

invariant
    count_in_range: 0 <= count and count <= capacity
```

The same contract in Python, with checks written by hand:

```python
class ContractError(AssertionError):
    pass

def require(cond, msg):
    if not cond:
        raise ContractError("precondition failed: " + msg)

def ensure(cond, msg):
    if not cond:
        raise ContractError("postcondition failed: " + msg)

class BoundedStack:
    def __init__(self, capacity):
        require(capacity > 0, "capacity > 0")
        self._items = []
        self._cap = capacity
        self._check_invariant()

    def _check_invariant(self):
        if not (0 <= len(self._items) <= self._cap):
            raise ContractError("class invariant failed: 0 <= count <= capacity")

    def push(self, x):
        self._check_invariant()
        require(len(self._items) < self._cap, "stack is not full")
        old_count = len(self._items)
        self._items.append(x)
        ensure(self._items[-1] is x, "top is x")
        ensure(len(self._items) == old_count + 1, "count grew by 1")
        self._check_invariant()

    def pop(self):
        self._check_invariant()
        require(self._items, "stack is not empty")
        old_count = len(self._items)
        x = self._items.pop()
        ensure(len(self._items) == old_count - 1, "count shrank by 1")
        self._check_invariant()
        return x

s = BoundedStack(2)
s.push(1); s.push(2)
try:
    s.push(3)
except ContractError as e:
    print(e)
print(s.pop(), s.pop())
try:
    s.pop()
except ContractError as e:
    print(e)
```

The program prints `precondition failed: stack is not full`, then `2 1`, then `precondition failed: stack is not empty`.

### What happens when a contract fails

- **A precondition is false at a call.** The caller has a bug. The body of the routine does not run. In Eiffel, with checking on, the call raises an exception.
- **A postcondition is false at return.** The routine has a bug: either its body is wrong, or it relied on more than the contracts of the routines it calls promise.
- **The invariant is false at entry or at exit.** The class has a bug, or some code changed the fields without the public routines. A false invariant at entry often means that the fields were exposed.

A failed check raises an exception. In Eiffel, a routine can have a `rescue` clause. The clause either repairs the state and retries the routine with `retry`, or it ends and the routine fails, and the exception goes to the caller. In both cases the rescue clause must restore the class invariant, so that the object stays valid after the failure (OOSC, Chapter 12). A contract is not an input check: code that must handle bad input from users or files uses ordinary tests and reports, and does not use a contract.

## Classic examples

- **Heap insertion.** For INSERT in a [binary heap](/binary-heap/) with the state $(a, n)$ and capacity $L$: the precondition is $n < L$. The postcondition is that the new size is $n + 1$, that the multiset of the first $n + 1$ cells is the old multiset plus $x$, and that the invariant $I(a, n+1)$ holds, that is $0 \le n+1 \le L$ and every cell is at least its parent (see [representation invariant](/representation-invariant/)). The last part uses the [abstraction function](/abstraction-function/) for the multiset.
- **[Binary search](/binary-search/).** The precondition is that the array is sorted. The postcondition is that $-1 \le i < n$ for the result $i$ and the length $n$ of the array, that $a[i] = x$ when $i \ge 0$, and that $x$ does not occur in $a$ when $i = -1$. Without the precondition, the postcondition is false for some inputs.
- **Sorting.** For the [sorting problem](/sorting-problem/), and so for [merge sort](/merge-sort/), the postcondition has two parts: the output is in non-decreasing order, and the output is a permutation of the input. The first part alone is not enough. A routine that returns an empty list always meets it.
- **Loops.** A [loop invariant](/loop-invariant/) is a contract for the loop body, checked at each test of the loop condition. Eiffel also lets a loop state a `variant`, an integer expression that stays non-negative and decreases at each iteration; it proves that the loop ends.

## Variations

- **Runtime checking.** The conditions run as code. Eiffel has compiler options to enable or disable the checks of each kind. Python has [assertions](/assertion/) in the form of `assert` statements, which the option `-O` removes.
- **Static checking.** A verifier proves that the contracts hold for all inputs. Dafny, with `requires` and `ensures`, and Why3 work in this way. Other contract systems exist: JML for Java, the `Pre` and `Post` aspects of Ada 2012 with SPARK, and the contract assertions (`pre`, `post` and `contract_assert`) of C++26. Some of them check at run time, some prove statically, and some do both.
- **Contracts and inheritance.** A redefinition of a routine in a subclass must work wherever the old one worked. So it may weaken the precondition and may strengthen the postcondition. This is the rule of behavioral subtyping, also called the Liskov substitution principle (Liskov 1987, made exact by Liskov and Wing 1994). In Eiffel the clauses are `require else` and `ensure then`. With $\mathit{Pre}$ and $\mathit{Post}$ for the old routine and $\mathit{Pre}'$ and $\mathit{Post}'$ for the new one, the rule is $\mathit{Pre} \Rightarrow \mathit{Pre}'$ and $\mathit{Post}' \Rightarrow \mathit{Post}$. The invariant of a subclass includes the invariant of its parent.
- **Contracts as test oracles.** A random test generator calls routines with inputs that meet the precondition. The postcondition and the invariant decide whether each run is correct.

## Pitfalls

- **Checks that cost too much.** The heap invariant needs $\Theta(n)$ time to check. INSERT takes $O(\log n)$ time. A check of the full invariant at each call changes the cost of $n$ inserts from $O(n \log n)$ to $\Theta(n^2)$. For $n = 10^6$, a call does about 20 steps of work and $10^6$ steps of checking. Use the full check in tests, and cheap partial checks otherwise.
- **Checks with side effects.** A condition that changes the state makes the program behave in a different way when checks are on and off.
- **Logic in the contract.** A program that needs its contracts to run correctly, such as one that catches a contract error to handle bad input, breaks when checks are turned off.
- **A weak postcondition.** A contract that the wrong code also meets gives false confidence. The sorting example shows this.
- **Exposed fields.** If a client can change the fields, or keeps a reference to an internal list, the invariant can break between calls. Copy mutable arguments, and do not return internal structures.
- **Callbacks.** If a routine calls client code while the invariant is false, the client code can observe or call into an invalid state. Restore the invariant before the call.
- **A precondition that the caller cannot test.** The caller then cannot meet its duty on purpose. Offer a query for it.
- **Checking the same fact twice.** If the body repeats a precondition test and handles the failure, then the precondition does not help to find the bug in the caller.

## Exercises

1. Write a contract for `isqrt(n)`, the largest integer $r$ with $r^2 \le n$. Give the precondition and the postcondition, and then write the routine with `require` and `ensure` calls. Which condition would let a wrong routine pass if you wrote only $r^2 \le n$?
2. For BoundedStack, `pop` returns the top item. Add the postcondition "the result is the item that was on top at entry" by saving the old top. Then change `pop` to return the second item and show that the check fails.
3. A routine `f(x)` has the precondition $x > 0$ and the postcondition $\mathit{result} \ge x$. For each redefinition in a subclass, say whether the rule for contracts and inheritance allows it. (a) Precondition $x \ge 0$, postcondition $\mathit{result} \ge x + 1$. (b) Precondition $x > 5$, postcondition $\mathit{result} \ge x$. (c) Precondition $x > 0$, postcondition $\mathit{result} \ge 0$.
   <details><summary>Hint</summary>The precondition may become weaker, never stronger. The postcondition may become stronger, never weaker. Test (a) first.</details>
4. A class stores the list that its constructor receives, and its invariant says that the list is sorted. Show a sequence of calls, with a client that does not break any precondition, after which the invariant is false. Then change the constructor to repair this.
5. Give a check for the end of heap INSERT that takes $O(\log n)$ time and finds the error of a version that has no swap loop. Say which errors of other kinds it can miss.
6. Write a contract for `binary_search(a, x)` in Python, with the precondition that `a` is sorted. How long does the check of the precondition take? Explain why you may want to check it only in tests.
7. Write the postcondition of a `sort` routine as a Python function `is_correct(inp, out)` of two lists. Show that your function rejects the routine that returns an empty list.

## References
