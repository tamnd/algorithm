---
tag: ZWN0YD
kind: concept
slug: greedy-choice-property
name: Greedy-choice property
aliases:
- greedy choice property
area: techniques/greedy
level: intro
summary: Some globally optimal solution contains the locally greedy choice, so the choice can be committed to.
prereqs: [greedy-algorithm, optimal-substructure]
see_also: [greedy-algorithm, optimal-substructure, exchange-argument, greedy-stays-ahead, matroid-greedy-theorem, canonical-coin-system, activity-selection, fractional-knapsack]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 15.2, Elements of the greedy strategy (greedy-choice property, optimal substructure)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Chapter 4, Greedy Algorithms
---

The greedy-choice property holds for an optimization problem and a greedy rule when, for every instance, some optimal solution contains the first choice made by the rule. It is one of the two ingredients that make a [greedy algorithm](/greedy-algorithm/) exact, the other being [optimal substructure](/optimal-substructure/): after the greedy choice is committed, the rest of the problem is a smaller instance of the same kind. Together they let an induction show that the whole greedy solution is optimal. The property is about a rule, not only a problem: earliest finish time has it for activity selection, while shortest interval first does not.

## In plain words

A greedy algorithm makes a choice and never takes it back. That is only safe if the choice cannot hurt. The greedy-choice property says exactly this: there is a best answer that agrees with the greedy choice. So committing to it loses nothing.

If the property holds at every step, the greedy algorithm keeps the door to a best answer open the whole way, and it ends at one.

To prove the property, start from any best answer that does not contain the greedy choice. Then change it a little, so that it does contain the greedy choice, and show that it is still feasible and still best. If no such change works, look for a small example where every best answer avoids the greedy choice. Then the rule is wrong.

## The idea

**Statement.** Let $P$ be an optimization problem and let $g(I)$ be the choice that a greedy rule makes on instance $I$. The rule has the greedy-choice property if, for every instance $I$, some optimal solution of $I$ contains $g(I)$.

**With optimal substructure.** Let $I'$ be the instance that remains after $g(I)$ is committed. Optimal substructure means that $g(I)$ together with an optimal solution of $I'$ is an optimal solution of $I$. Then induction on the size of the instance proves the greedy algorithm optimal: it commits to $g(I)$, which some optimal solution contains, and then solves $I'$ the same way, optimally by induction.

**How to prove it.** The usual proof is a single [exchange](/exchange-argument/): let $O$ be an optimal solution, and if $g(I) \notin O$, remove some element $o$ of $O$ and add $g(I)$, and show that the result $O'$ is feasible and $\mathrm{val}(O') \ge \mathrm{val}(O)$ for a maximization problem. Then $O'$ is optimal and contains $g(I)$.

**Contrast with dynamic programming.** Dynamic programming also uses optimal substructure, but it does not know which first choice is right, so it tries all of them and compares the subproblem values. The greedy-choice property is what lets a greedy algorithm make the choice first and solve only one subproblem.

**On matroids.** If the feasible sets form a [matroid](/matroid/) and the objective is a sum of weights, the heaviest element that is independent on its own belongs to some maximum-weight basis. So "take the heaviest element that still fits" has the greedy-choice property for every weight function, which is the core of the [matroid greedy theorem](/matroid-greedy-theorem/).

## Examples

**Activity selection, earliest finish.** Let $a$ be the activity that finishes first and let $O$ be a largest set of compatible activities. If $a \notin O$, replace the activity of $O$ that finishes first by $a$. Since $a$ finishes no later, $a$ is compatible with the rest of $O$, and the new set has the same size. So some optimal solution contains $a$. The remaining instance is the set of activities that start after $a$ finishes. See [activity selection](/activity-selection/).

**Fractional knapsack, best ratio.** The item of the largest value per unit of weight is taken as fully as possible in some optimal solution: moving weight to it from any other item does not decrease the value. See [fractional knapsack](/fractional-knapsack/).

**Huffman coding.** The two least frequent symbols are siblings at the deepest level in some optimal code tree, so merging them first is safe. See [Huffman coding](/huffman-coding/).

**Non-example: 0-1 knapsack.** Capacity 50 and items $(v, w) = (60, 10), (100, 20), (120, 30)$. The item of the largest ratio is the first one. The only optimal solution is the second and third items, with value 220, and every solution that contains the first item has value at most 180. So "best ratio first" does not have the greedy-choice property here.

**Non-example: coins 1, 3, 4.** To pay 6, the greedy rule takes the coin 4 first. The only way to pay 6 with two coins is $3 + 3$, which does not use 4. So the property fails for this coin system, which is not a [canonical coin system](/canonical-coin-system/). For coins $1, 5, 10, 25$ it holds for every amount.

**Non-example: shortest interval first.** For the intervals $[0, 5)$, $[4, 6)$, $[5, 10)$, the shortest one is $[4, 6)$, but the only optimal solution is $\{[0, 5), [5, 10)\}$, which does not contain it.

## Where it is used

- **Designing greedy algorithms.** To decide whether a candidate rule can work, test whether some optimal solution always contains its first choice, on small instances by brute force.
- **Proving greedy algorithms.** The greedy-choice property plus optimal substructure is the proof outline of CLRS for activity selection, fractional knapsack and Huffman codes.
- **Explaining failures.** A counterexample to a greedy rule is an instance in which no optimal solution contains the greedy choice.
- **Bridge to other proof methods.** The [exchange argument](/exchange-argument/) proves the property one choice at a time, and [greedy stays ahead](/greedy-stays-ahead/) proves the whole greedy solution optimal at once without isolating the first choice.

## References
