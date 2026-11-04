---
tag: RTGKE6
kind: technique
slug: differential-testing
name: Differential testing
aliases:
- Back-to-back testing
- Pseudo-oracle testing
area: foundations/correctness-and-invariants
level: intro
summary: Compares the outputs of two implementations of the same specification on the same inputs to find discrepancies.
prereqs: [specification]
see_also: [property-based-testing, abstraction-function, design-by-contract, correctness, insertion-sort, quicksort]
sources:
  - paper: "William M. McKeeman, Differential testing for software, Digital Technical Journal 10(1) (1998)"
    title: William M. McKeeman, Differential testing for software, Digital Technical Journal 10(1) (1998)
    locator: pp. 100 to 107
  - paper: doi:10.1145/1993498.1993532
    title: Xuejun Yang, Yang Chen, Eric Eide and John Regehr, Finding and understanding bugs in C compilers, PLDI 2011
    locator: the sections on the design of Csmith and on the results
  - paper: "Martin D. Davis and Elaine J. Weyuker, Pseudo-oracles for non-testable programs, ACM '81 Conference, 1981"
    title: Martin D. Davis and Elaine J. Weyuker, Pseudo-oracles for non-testable programs, ACM '81 Conference, 1981
    locator: the definition of a pseudo-oracle
  - paper: "Andreas Zeller and Ralf Hildebrandt, Simplifying and isolating failure-inducing input, IEEE Transactions on Software Engineering 28(2), 2002"
    title: Andreas Zeller and Ralf Hildebrandt, Simplifying and isolating failure-inducing input, IEEE Transactions on Software Engineering 28(2), 2002
    locator: the delta debugging algorithm
  - paper: "T. Y. Chen, S. C. Cheung and S. M. Yiu, Metamorphic testing: a new approach for generating next test cases, Technical Report HKUST-CS98-01, 1998"
    title: "T. Y. Chen, S. C. Cheung and S. M. Yiu, Metamorphic testing: a new approach for generating next test cases, Technical Report HKUST-CS98-01, 1998"
    locator: whole report
  - paper: doi:10.1145/2254064.2254104
    title: John Regehr, Yang Chen, Pascal Cuoq, Eric Eide, Chucky Ellison and Xuejun Yang, Test-case reduction for C compiler bugs, PLDI 2012
    locator: the description of C-Reduce
  - paper: doi:10.1016/0950-5849(90)90044-R
    title: Mladen A. Vouk, Back-to-back testing, Information and Software Technology 32(1), 1990
    locator: pp. 34 to 45
  - paper: doi:10.1109/TSE.1985.231893
    title: Algirdas Avizienis, The N-version approach to fault-tolerant software, IEEE Transactions on Software Engineering SE-11(12), 1985
    locator: pp. 1491 to 1501
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 2 (insertion sort) and Chapter 7 (quicksort)
---

Differential testing runs two or more implementations of the same [specification](/specification/) on the same inputs and reports each input on which the outputs differ. It needs no table of expected results: one implementation serves as the oracle for the other, a pseudo-oracle. McKeeman (1998) named the method and applied it to compilers. The idea of a second program as a pseudo-oracle goes back to Davis and Weyuker (1981), and back-to-back testing of program versions was in use before McKeeman's paper (Vouk 1990). The method is cheap to start, and it works well for algorithms, because a slow and simple version of an algorithm is often easy to write.

## In plain words

You have a fast program that you do not trust. You also have a slow program that is so simple that you can read it and see that it is right. You make many inputs. You give each input to both programs and compare the answers. If the answers are the same, you learn nothing new. If they are different, one program has a bug, and you have an input that shows it.

The slow program does not need to be fast. It runs only in tests. It can be a naive loop, an old version of the code, a library routine, or the same algorithm written in another language by another person. The more the two programs differ in how they work, the less likely it is that both fail in the same way.

## When it applies

- You have a fast or complex implementation and a simple one for the same task. Examples: a tuned sort and insertion sort, a hash table and a list of pairs, a fast big-integer product and the schoolbook product.
- You have two versions of a program, and the new version must not change the results. This is back-to-back testing.
- You have several independent implementations of one standard, such as compilers for one language.
- Writing the expected output by hand is hard, but running a reference is easy.

It does not apply when no second implementation exists and none is easy to write, or when the specification allows many correct outputs and you cannot say when two outputs are equivalent.

## The template

Let $A$ be the implementation under test and $B$ the reference. Both implement the specification $S$.

1. **Reference.** Choose $B$ so that it is simple and independent of $A$. Read it with care: the test only shows that $A$ agrees with $B$.
2. **Generator.** Write a function $G$ that returns a random input of the kind that $S$ allows. Make it produce small inputs, edge cases and inputs with repeated values often.
3. **Equivalence.** Define a relation $\approx$ on outputs. It is equality when the output is unique. It is weaker when $S$ allows more than one output.
4. **Loop.** Repeat $N$ times: draw $x = G()$; compute $A(x)$ and $B(x)$; if $A(x) \not\approx B(x)$, return $x$ with the seed, or record $x$ and continue to collect more failures.
5. **Reduce.** Make the failing input smaller by hand or by a shrinking routine (see [property-based testing](/property-based-testing/)), or by an algorithm such as delta debugging (Zeller and Hildebrandt 2002). For C programs, C-Reduce plays this role (Regehr and others 2012).
6. **Judge.** Find out which of $A$, $B$ or $S$ is wrong. The cause can be any of the three.

```pseudo id=main
DIFF-TEST(A, B, G, ≈, N, seed)
L1  rng ← new generator from seed
L2  for t ← 1 to N do
L3      x ← G(rng)
L4      if not (A(x) ≈ B(x)) then return (x, seed, t)
L5  return NONE
```

The numbered list is the walk-through of these holes.

If a fraction $p$ of the inputs that $G$ draws makes $A$ and $B$ differ, and the draws are independent, then the probability to see a difference in $N$ draws is

$$ 1 - (1 - p)^N. $$

This is at least $c$ exactly when $N \ge \ln(1-c) / \ln(1-p)$. For $p = 0.001$ and $c = 0.99$, the bound is $N \ge 4602.9$, so 4603 draws suffice. The formula shows that a rare bug needs many draws, and that the generator decides $p$.

## Classic examples

### A fast sort against insertion sort

The reference is [insertion sort](/insertion-sort/), which is easy to check. The implementation under test is a [quicksort](/quicksort/) that switches to insertion sort for ranges of at most 4 items. It has an off-by-one error in the small-range sort: the loop stops one cell early, so it never places the last cell of the range.

```python
import random

def simple_sort(xs):
    """Reference: insertion sort."""
    out = []
    for x in xs:
        i = len(out)
        while i > 0 and out[i - 1] > x:
            i -= 1
        out.insert(i, x)
    return out

def fast_sort(xs):
    """Quicksort with an insertion-sort cutoff. It has a bug."""
    a = list(xs)
    def insertion(lo, hi):                 # sorts a[lo..hi], both included
        for i in range(lo + 1, hi):        # bug: should be range(lo + 1, hi + 1)
            x = a[i]
            j = i - 1
            while j >= lo and a[j] > x:
                a[j + 1] = a[j]
                j -= 1
            a[j + 1] = x
    def qs(lo, hi):
        if hi - lo < 4:
            insertion(lo, hi)
            return
        p = a[(lo + hi) // 2]
        i, j = lo, hi
        while i <= j:
            while a[i] < p: i += 1
            while a[j] > p: j -= 1
            if i <= j:
                a[i], a[j] = a[j], a[i]
                i += 1; j -= 1
        qs(lo, j); qs(i, hi)
    qs(0, len(a) - 1)
    return a

def random_list(rng):
    n = rng.randint(0, 8)
    return [rng.randint(0, 9) for _ in range(n)]

def find_difference(trials, seed=0):
    rng = random.Random(seed)
    for _ in range(trials):
        xs = random_list(rng)
        if fast_sort(xs) != simple_sort(xs):
            return xs
    return None

xs = find_difference(1000)
print(xs is not None, fast_sort([2, 1, 0]), simple_sort([2, 1, 0]))
```

The program prints `True [1, 2, 0] [0, 1, 2]`. The input $[2, 1, 0]$ is small enough to trace by hand: the range has 3 cells, so the cutoff sort runs, and its loop handles the cell at index 1 only. About half of the lists that this generator draws expose the bug. A bug that shows up so often is found at once.

### Compilers

McKeeman (1998) used the method on compilers: a generator writes programs, several compilers or settings translate each one, and the programs must behave in the same way. Yang, Chen, Eide and Regehr (2011) used the same plan with a generator of C programs that avoids undefined behavior, and they report bugs in widely used C compilers.

### Data structures against a model

A [hash table](/hash-table/), a balanced tree or a [binary heap](/binary-heap/) can be tested against a plain list or multiset that receives the same operations. After each step, the test reads the structure through its [abstraction function](/abstraction-function/) and compares it with the model. The binary-heap program on the page [abstraction function](/abstraction-function/#a-binary-heap-as-a-priority-queue) is of this kind.

## Variations

- **Back-to-back testing.** The two programs are two versions of one program. A difference is a change of behavior, which may be wanted.
- **Voting.** With three or more implementations, the majority output is taken as correct, and the others are suspect. This is the test-time form of N-version programming (Avizienis 1985), where independently written versions run in production and vote. This helps to find which one is wrong, but it fails when the majority share a bug.
- **Configurations.** The same program is run with different settings that must not change the result, such as optimization levels of a compiler or the number of threads.
- **With a coverage-guided generator.** A fuzzer generates inputs that reach new code, and the harness compares the implementations on them.
- **Metamorphic testing.** With no second implementation, compare the program with itself on related inputs (Chen, Cheung and Yiu 1998). For example, the sort of a list must equal the sort of a permutation of the list. In a graph with non-negative weights, a shortest-path distance must not grow when an edge is added.
- **With properties.** Where the output can be checked without a reference, a property is cheaper than a second implementation. See [property-based testing](/property-based-testing/).

## Pitfalls

- **A bug in both.** If both programs have the same misunderstanding of the specification, they agree and the test passes. Write the reference from the specification, not from the code under test. Use another author, another language or another method when you can.
- **No unique output.** A sort that is not stable may order equal keys in different ways. Compare the output in the way that the specification allows: for records, compare the list of keys, and compare the multiset of records. Hash iteration order and the order of threads cause the same problem.
- **Floating point.** The sum of ten copies of 0.1, computed by a loop of additions, is 0.9999999999999999, and a correctly rounded sum gives 1.0. An exact comparison reports a difference that is not a bug. Use a tolerance that the specification justifies.
- **Undefined behavior.** If the specification leaves some inputs open, as the C language does, then two correct implementations may differ on them. The generator must not draw such inputs.
- **A weak generator.** Eight values drawn from the range 0 to $10^9$ contain a repeated value with probability about $2.8 \times 10^{-8}$. A bug in the handling of equal keys then never shows. Draw from a small range, and add the cases empty, one item, sorted, reverse sorted and all equal.
- **A reference that is too slow.** An $O(n^2)$ reference limits the size of the inputs. Bugs that need large inputs, such as an overflow or a rare resize, are missed.
- **Not repeatable.** Print the seed with each failure, and keep failing inputs as fixed regression tests.
- **A pass is not a proof.** A test of $N$ random inputs shows no difference. It does not show that the programs agree on all inputs.

## Exercises

1. Correct the loop bound in `fast_sort` to `range(lo + 1, hi + 1)`. Run the comparison on 100000 random lists and report how many differ. Then change the generator to lists of length up to 40 with values from 0 to 3, and run again.
2. A bug makes the two programs differ on a fraction $p = 0.0005$ of the generated inputs. How many independent draws give a probability of at least 0.95 to see a difference?
   <details><summary>Hint</summary>Use $N \ge \ln(0.05) / \ln(1 - 0.0005)$. The bound is 5989.97, so you need 5990 draws.</details>
3. Write a generator for lists of integers in which repeated values are likely. Compute, for your generator, the probability that a list of 8 items has at least one repeated value, and compare it with $2.8 \times 10^{-8}$ for the range 0 to $10^9$.
4. Write a differential test of your own binary search, which returns the index of the first cell that is at least the key, against `bisect.bisect_left` from the standard library. Say what the generator must produce for the array so that the precondition of both functions holds.
5. A function sorts records `(key, tag)` by key. Define an equivalence $\approx$ for which every correct sort passes, stable or not. Then state a second check that tests stability, and say what the first equivalence alone cannot detect.
6. Two sums of the same list of floats, a plain loop and `math.fsum`, are compared with a tolerance. For the list of ten copies of 0.1, compute the difference of the two results. Then choose a tolerance for lists of length up to 1000 with values between 0 and 1, and justify it.
7. Three programs $A$, $B$ and $C$ run on one input. $A$ and $B$ give the same output and $C$ gives another. Give two different causes of this event, one in which $C$ is wrong and one in which $C$ is right.

## References
