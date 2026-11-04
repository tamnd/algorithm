---
tag: ZA3A91
kind: technique
slug: property-based-testing
name: Property-based testing
aliases:
- QuickCheck-style testing
area: foundations/correctness-and-invariants
level: intro
summary: Checks that a stated property holds for many randomly generated inputs, shrinking failures to minimal examples.
prereqs: [specification]
see_also: [differential-testing, design-by-contract, abstraction-function, representation-invariant, correctness]
sources:
  - paper: doi:10.1145/351240.351266
    title: Koen Claessen and John Hughes, QuickCheck, a lightweight tool for random testing of Haskell programs, ICFP 2000
    locator: whole paper
  - paper: doi:10.1007/978-3-540-69611-7_1
    title: John Hughes, QuickCheck testing for fun and profit, PADL 2007, LNCS 4354
    locator: the section on shrinking
  - paper: doi:10.21105/joss.01891
    title: "David R. MacIver, Zac Hatfield-Dodds and others, Hypothesis: a new approach to property-based testing, Journal of Open Source Software 4(43), 2019"
    locator: whole article
  - paper: doi:10.4230/LIPIcs.ECOOP.2020.13
    title: "David R. MacIver and Alastair F. Donaldson, Test-case reduction via test-case generation: insights from the Hypothesis reducer, ECOOP 2020"
    locator: whole paper
  - paper: doi:10.1145/1411286.1411292
    title: "Colin Runciman, Matthew Naylor and Fredrik Lindblad, SmallCheck and Lazy SmallCheck: automatic exhaustive testing for small values, Haskell Symposium 2008"
    locator: the sections on exhaustive testing of small values
  - paper: doi:10.1145/3360607
    title: Leonidas Lampropoulos, Michael Hicks and Benjamin C. Pierce, Coverage guided, property based testing, OOPSLA 2019
    locator: whole paper (the FuzzChick tool)
  - paper: doi:10.1145/3092703.3092711
    title: Andreas Löscher and Konstantinos Sagonas, Targeted property-based testing, ISSTA 2017
    locator: whole paper
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 1.1 (only for the specification of the sorting problem used in the example)
---

Property-based testing checks a property, a statement that must hold for all inputs of some kind, on many inputs that a program generates at random. Claessen and Hughes made the method popular with the Haskell tool QuickCheck (ICFP 2000), which pairs stated properties with random generators. When a test fails, a modern tool shrinks the failing input to a smaller one that still fails, so that the report is easy to read. Shrinking was added in later versions of QuickCheck and in Erlang QuickCheck (Hughes, PADL 2007). Libraries with the same plan now exist for many languages.

## In plain words

An ordinary test says: for this one input, the output is that one value. A property says something about every input. For a sort routine, a property is: the output is in order, and it has the same items as the input.

You do not choose the inputs. A generator makes them at random: short lists, long lists, lists with repeated items, and so on. The tool runs the property on a hundred of them. If one input breaks the property, the tool does not stop there. A random input that fails is usually large and full of noise. So the tool tries to make it smaller: it removes items and makes numbers closer to zero, and it keeps each change that still fails. At the end you see a small input, often with two or three items, that shows the bug.

## When it applies

- The function has a [specification](/specification/) that you can state as a law that holds for all inputs. Common forms:
  - **Round trip.** Decoding the encoding gives back the input.
  - **[Postcondition](/postcondition/).** The output is sorted and is a permutation of the input.
  - **Invariant.** After any sequence of operations, the [representation invariant](/representation-invariant/) holds.
  - **Model.** The structure agrees with a simple model, as in [differential testing](/differential-testing/).
  - **Idempotence.** Sorting a sorted list does nothing.
- The inputs have a structure that a program can generate: numbers, lists, trees, graphs, sequences of operations.
- You want tests that grow with the code, without a long list of examples to maintain.

## The template

1. **Property** ($\varphi$, with the precondition $\mathrm{pre}$). A function $\varphi$ from inputs to Boolean. It may have a [precondition](/precondition/): a test whose input does not meet it is skipped, not counted as a pass.
2. **Generator.** A function $G(s)$ that returns a random input of size at most about $s$. The size $s$ grows with the number of the test, so the first tests are small.
3. **Size measure and shrinker.** A function $\mu$ from inputs to the natural numbers, and a function $\mathrm{shrink}(x)$ that returns a finite list of candidates with $\mu(c) < \mu(x)$ for each candidate $c$.
4. **Run.** Draw inputs $x = G(s_t)$ with $t = 1, 2, \ldots$ until $N$ inputs have met the precondition, and give up after a fixed number of discards. If $\varphi(x)$ is false for some input, go to step 5. If all $N$ tests pass, report success. The default of QuickCheck is $N = 100$.
5. **Shrink.** While some candidate $c \in \mathrm{shrink}(x)$ meets the precondition and has $\varphi(c)$ false, set $x \leftarrow c$. When no candidate fails, report $x$ and the seed of the generator.

```pseudo id=main
CHECK(φ, pre, G, μ, shrink, N, maxDiscard, seed)
L1  rng ← new generator from seed
L2  passed ← 0; discarded ← 0; t ← 0
L3  while passed < N do
L4      t ← t + 1
L5      x ← G(rng, size(t))
L6      if not pre(x) then
L7          discarded ← discarded + 1
L8          if discarded > maxDiscard then return GAVE-UP
L9          continue
L10     if φ(x) then passed ← passed + 1
L11     else return (seed, x, SHRINK(φ, pre, shrink, x))
L12 return PASSED

SHRINK(φ, pre, shrink, x)
L13  loop
L14      found ← false
L15      for each c in shrink(x) do
L16          if pre(c) and not φ(c) then x ← c; found ← true; break
L17      if not found then return x
```

The numbered list gives the meaning of each hole.

The shrink loop stops. Each step lowers the natural number $\mu(x)$ by at least 1, and $\mu(x) \ge 0$, so there are at most $\mu(x_0)$ steps for the first failing input $x_0$. The result is a local minimum: no single candidate of the shrinker fails. It need not be the smallest failing input.

## Classic examples

### Sorting, with a worked run

The function under test is meant to [sort](/sorting/) a list of integers. Sorting fits well, because its specification is two easy checks: the output is in order, and it is a permutation of the input. It has a bug: it drops the repeated items.

```python
import random
from collections import Counter

def my_sort(xs):
    """Buggy: it drops duplicates."""
    return sorted(set(xs))

def prop_sorted(xs):
    ys = my_sort(xs)
    return all(ys[i] <= ys[i + 1] for i in range(len(ys) - 1))

def prop_permutation(xs):
    return Counter(my_sort(xs)) == Counter(xs)

def gen_list(rng, size):
    return [rng.randint(-size, size) for _ in range(rng.randint(0, size))]

def shrinks(xs):
    """Candidates that are smaller than xs, most aggressive first."""
    for i in range(len(xs)):                       # drop one item
        yield xs[:i] + xs[i + 1:]
    for i, x in enumerate(xs):                     # move one item toward 0
        for y in (0, x // 2, x - 1 if x > 0 else x + 1):
            if abs(y) < abs(x):
                yield xs[:i] + [y] + xs[i + 1:]

def shrink(prop, xs):
    while True:
        for c in shrinks(xs):
            if not prop(c):
                xs = c
                break
        else:
            return xs

def check(prop, gen, trials=100, seed=0):
    # this example leaves out preconditions and discards
    # (CHECK in the pseudocode with pre always true)
    rng = random.Random(seed)
    for t in range(trials):
        xs = gen(rng, 2 + t // 2)                  # sizes grow with t
        if not prop(xs):
            return seed, xs, shrink(prop, xs)
    return None

print(check(prop_sorted, gen_list))
print(check(prop_permutation, gen_list))
```

The program prints `None` and then `(0, [3, 3, -1], [3, 3])`: the seed, the first failing input and the shrunk input.

- The property "sorted" passes on all 100 inputs. The buggy function returns a sorted list, so this property is too weak to find the bug.
- The property "permutation" fails on the 4th input, $[3, 3, -1]$. This list has a repeated item.
- The shrinker tries the candidates in order. Dropping the item at index 0 gives $[3, -1]$, and dropping the item at index 1 gives the same list. Both pass. Dropping the item at index 2 gives $[3, 3]$, which fails, so $x \leftarrow [3, 3]$.
- From $[3, 3]$, the candidates are $[3]$, $[0, 3]$, $[1, 3]$, $[2, 3]$, $[3, 0]$, $[3, 1]$ and $[3, 2]$ (the list $[3]$ occurs twice). All of them pass, because none has a repeated item. The result is $[3, 3]$.

The size measure is $\mu(x) = |x| + \sum_i |x_i|$ for a list $x$ with the length $|x|$. Dropping an item lowers $|x|$ by 1 and does not raise the sum. Replacing an item by one with a smaller absolute value lowers the sum by at least 1 and keeps the length. So the measure falls by at least 1 at each step.

The failing input $[3, 3]$ is a local minimum, but not the smallest one: $[0, 0]$ also fails. Over 50 different seeds, this shrinker always ends in a list $[k, k]$, with $k$ taking many values. To reach $[0, 0]$, add a candidate that changes all copies of one value together:

```python
def shrinks_better(xs):
    yield from shrinks(xs)
    for x in set(xs):                              # change all copies of x together
        for y in (0, x // 2):
            if abs(y) < abs(x):
                yield [y if v == x else v for v in xs]
```

With this extra step, the result is $[0, 0]$ for each of the same 50 seeds. The fix to the function is to stop dropping duplicates: use `sorted(xs)`.

### Round trip

[Run-length encoding](/run-length-encoding/) turns a list into pairs of an item and a count. The property is $\mathrm{decode}(\mathrm{encode}(x)) = x$ for every list $x$. The generator makes lists with few distinct values, so that runs are likely. A typical bug is an encoder that drops the last run: the property fails on any non-empty list.

### Operations against a model

The generator makes a list of operations, such as insert and extract-min for a [binary heap](/binary-heap/). The property says: after each operation, the representation invariant $I(a, n)$ holds and $\alpha(a, n)$ equals a plain multiset that received the same operations ([abstraction function](/abstraction-function/)). A typical bug is a missing sift-down in extract-min: the invariant fails after the operations insert 1, insert 2, insert 3 and extract-min, which leave the array $[3, 2]$ with size 2. A failing list of operations shrinks by removing operations.

## Variations

- **Integrated shrinking.** The library builds the shrinker from the generator, so you write only the generator. Hedgehog does this with shrink trees. Hypothesis for Python goes further: it shrinks the sequence of random choices that the generator made, so shrunk inputs always meet the constraints of the generator.
- **Stateful testing.** The input is a sequence of operations on an object, and the property compares the object with a model.
- **Coverage guidance.** The generator uses feedback on which code each input reaches. FuzzChick (Lampropoulos, Hicks and Pierce, OOPSLA 2019) does this for QuickChick.
- **Targeted testing.** The search is guided by a utility value that the property reports for each input, and the tool tries to raise it (Löscher and Sagonas, ISSTA 2017).
- **Metamorphic properties.** The property relates the outputs on related inputs, and it needs no expected output. For sorting: $\mathrm{sort}(x \mathbin{++} y) = \mathrm{merge}(\mathrm{sort}(x), \mathrm{sort}(y))$, where $\mathrm{merge}$ merges two sorted lists.
- **Exhaustive small cases.** For small sizes, test all inputs of that size and not a random sample, as SmallCheck does.

## Pitfalls

- **A weak property.** The property "sorted" passes on the buggy sort above. Write the full specification: order and permutation.
- **A property that repeats the code.** If the property computes the answer by the same method as the function, then they fail together. Prefer a different way: a check of a relation, a simpler algorithm, or a model.
- **A generator that misses cases.** Values drawn from a very wide range rarely repeat. Eight values from 0 to $10^9$ have a repeat with probability about $2.8 \times 10^{-8}$, so a bug that needs a repeat is not found. Use small ranges, and add the cases empty, one item and all equal. Look at the distribution of the generated inputs; QuickCheck has functions to report it.
- **Filtering instead of building.** To get a sorted list, you can draw a list and discard it when it is not sorted. For 8 distinct values the chance of a sorted draw is $1/8! \approx 2.5 \times 10^{-5}$. Build the sorted list instead: draw a list and sort it.
- **A shrinker that produces invalid inputs.** A candidate must meet the precondition of the property. If it does not, the shrinker may report an input that the program never gets.
- **A shrinker that does not shrink.** If a candidate is not smaller in the measure $\mu$, the loop may never stop.
- **Slippage.** The shrunk input can fail for a different reason than the original. Read both failures.
- **Local minimum.** Shrinking may stop at a failing input that is not the smallest, as in the worked example.
- **Not repeatable.** Print the seed. A property that depends on time or on a global state makes the shrinking unreliable, because a candidate may pass and fail on two runs.
- **A pass is not a proof.** A hundred passes show no failure in a hundred samples.

## Exercises

1. Run the worked example with `shrinks_better` in place of `shrinks` and with the seeds 0 to 49. Confirm that the shrunk list is $[0, 0]$ each time.
2. A generator draws 8 integers independently and uniformly from 0 to 9. Compute the probability that the list is in non-decreasing order, and the expected number of draws until the first such list, counting that list. Then describe a generator that always gives a sorted list.
   <details><summary>Hint</summary>The number of non-decreasing lists of length 8 over 10 values is $\binom{17}{8} = 24310$. The probability is $24310 / 10^8 = 0.0002431$, so the expected number of draws is about 4113.5.</details>
3. Write `encode` and `decode` for run-length coding of a list, and the round-trip property. Run 1000 tests. Then break `decode` by an off-by-one error in the count and look at the shrunk input.
4. Show that the shrinker of the worked example stops: prove that each candidate has a smaller value of $\mu(x) = |x| + \sum_i |x_i|$ than $x$. Which line of the code makes this true for the candidate $x // 2$ when $x = -1$?
   <details><summary>Hint</summary>In Python, $-1 // 2 = -1$. The test `abs(y) < abs(x)` removes the candidate.</details>
5. Write a property for a binary heap that runs a random list of insert and extract-min operations against a model multiset. State the generator of operations, and say how the failing list of operations should shrink.
6. Give a function that meets the property "sorted and has the same length as the input" and is still wrong. What do you add to the property to catch it?
   <details><summary>Hint</summary>A function that replaces each item by the minimum of the list returns a sorted list of the right length.</details>

## References
