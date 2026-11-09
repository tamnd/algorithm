---
tag: 11JHSD
kind: technique
slug: rule-of-sum
name: Rule of sum
aliases:
- addition principle
- sum rule
area: combinatorics/counting-algorithms
level: intro
summary: A counting principle stating that if two actions cannot both happen, the number of ways to do either is the sum of their counts.
prereqs: []
see_also: [rule-of-product, inclusion-exclusion-principle, double-counting, bijective-proof, pascal-triangle-dp, union-bound, counting-problem]
sources:
  - book: isbn:9780073383095
    title: Kenneth H. Rosen, Discrete Mathematics and Its Applications, seventh edition
    locator: Section 6.1, The Basics of Counting (the sum rule, the subtraction rule and the password example)
  - book: isbn:9780136020400
    title: Richard A. Brualdi, Introductory Combinatorics, fifth edition
    locator: Section 2.1, Four Basic Counting Principles (the addition principle)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix C.1, Counting (rules of sum and product)
---

The rule of sum says that if a finite set is split into parts that do not overlap, then the size of the set is the sum of the sizes of the parts. In the language of choices: if a task can be done in one of $m$ ways or in one of $n$ ways, and no way is in both groups, then the task can be done in $m + n$ ways. It is the formal basis of a case analysis in counting, and of every counting recurrence that splits the objects by one property, for example [Pascal's rule](/pascal-triangle-dp/) for the [binomial coefficient](/binomial-coefficient/). When the parts overlap, the rule becomes the [inclusion-exclusion principle](/inclusion-exclusion-principle/).

## In plain words

A restaurant has three soups and four salads, and the lunch deal lets you take one soup or one salad. You have seven choices, because no dish is both a soup and a salad. That is the whole rule: when the options fall into groups that share nothing, you count each group and add the counts.

The rule is used most for a case split. You cut a hard counting question into cases that are easier, count each case, and add. The two things to check are that each object is in some case, and that no object is in two cases. If you skip the second check, you count some objects twice.

## When it applies

- The objects to count split by a property with a finite number of values: the length of a string, the first move, the size of a subset, the last part of a sum.
- Each object has exactly one value of the property. Then the cases are disjoint and they cover the whole set.
- Each case is easier to count than the whole set, often because it is a smaller instance of the same question. This gives a recurrence, and a [dynamic program](/dag-dynamic-programming/) evaluates it.

## The template

Notation: $|S|$ is the number of elements of a finite set $S$, and $[n] = \{1, \ldots, n\}$.

**Rule of sum.** Let $S_1, \ldots, S_k$ be finite sets with $S_i \cap S_j = \emptyset$ for all $i \ne j$. Then

$$\Bigl|\,\bigcup_{i=1}^{k} S_i\,\Bigr| = \sum_{i=1}^{k} |S_i|.$$

*Proof.* First let $k = 2$, with $|S_1| = m$ and $|S_2| = n$. By the definition of size, there are bijections $g : S_1 \to [m]$ and $h : S_2 \to \{1, \ldots, n\}$. Define $f$ on $S_1 \cup S_2$ by $f(x) = g(x)$ for $x \in S_1$ and $f(x) = m + h(x)$ for $x \in S_2$. Since the sets are disjoint, each $x$ falls under exactly one of the two cases, so $f$ is a function. It maps $S_1$ onto $\{1, \ldots, m\}$ and $S_2$ onto $\{m+1, \ldots, m+n\}$, one to one in each part, and the two images do not overlap. So $f$ is a bijection onto $[m+n]$, and $|S_1 \cup S_2| = m + n$. For $k \ge 3$, use induction on $k$: the set $S_1 \cup \cdots \cup S_{k-1}$ is disjoint from $S_k$, so the case $k = 2$ and the induction hypothesis give the sum. For $k = 1$ the claim is trivial, and for $k = 0$ both sides are $0$. $\square$

As a counting method, the rule takes this form.

```pseudo id=main
COUNT-BY-CASES(S)
L1  choose a property P with values v_1, ..., v_k          ▷ hole: the case split
L2  S_i ← the objects x of S with P(x) = v_i, for each i
L3  check: each x in S has exactly one value of P          ▷ disjoint and complete
L4  for i ← 1 to k do
L5      c_i ← |S_i|                                         ▷ hole: count one case
L6  return c_1 + c_2 + ... + c_k
```

Line L3 is the condition of the rule. If $P$ is a function on $S$, then each object has one value, so the cases are disjoint and they cover $S$. The cases are then the classes of the partition of $S$ that $P$ defines, and line L6 is correct by the rule of sum. Line L5 often calls the same method on a smaller instance. In this case the method is a recurrence, and the count of the whole set is computed bottom up from the base cases.

The **subtraction rule** is the same fact read the other way: if $A \subseteq S$, then $S$ is the disjoint union of $A$ and $S \setminus A$, so $|S \setminus A| = |S| - |A|$. Counting the complement is often easier than counting the set.

## Classic examples

**1. Passwords (Rosen, Section 6.1).** A password has 6 to 8 characters. Each character is an uppercase letter or a digit, and each password has at least one digit. Split by the length $L$. For each $L$, all strings over 36 symbols, minus the strings with no digit, gives $36^L - 26^L$ by the subtraction rule and the [rule of product](/rule-of-product/). The cases are disjoint because a string has one length. The total is

$$(36^6 - 26^6) + (36^7 - 26^7) + (36^8 - 26^8) = 1{,}867{,}866{,}560 + 70{,}332{,}353{,}920 + 2{,}612{,}282{,}842{,}880 = 2{,}684{,}483{,}063{,}360.$$

**2. Pascal's rule.** Split the $k$-element subsets of $[n]$ by whether they contain $n$. The subsets that contain $n$ match the $(k-1)$-subsets of $[n-1]$, and the others are the $k$-subsets of $[n-1]$. So $\binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k}$, the recurrence of [Pascal's triangle](/pascal-triangle-dp/).

**3. All subsets.** Split the subsets of $[n]$ by their size. The cases are disjoint, so $\sum_{k=0}^{n} \binom{n}{k} = 2^n$. The right side comes from the rule of product. This is one of the identities of the [binomial theorem](/binomial-theorem/), obtained here by counting.

**4. Compositions into parts 1 and 2.** Let $f(n)$ be the number of ways to write $n$ as an ordered sum of 1s and 2s. Split by the last part. If it is 1, the rest is a composition of $n - 1$. If it is 2, the rest is a composition of $n - 2$. So $f(n) = f(n-1) + f(n-2)$ with $f(0) = f(1) = 1$, which gives the Fibonacci numbers $1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89$ for $n = 0$ to $10$. See [counting integer compositions](/counting-integer-compositions/).

**5. Paths in a grid or a DAG.** The number of paths from the source to a vertex $v$ of a directed acyclic graph is the sum, over the edges $(u, v)$ that enter $v$, of the number of paths to $u$. The cases are disjoint because each path has one last edge. This is the recurrence of [DP on a DAG](/dp-on-dag/) and of [counting lattice paths](/counting-lattice-paths/).

**6. Catalan numbers.** Split the binary trees with $n$ nodes by the size $i$ of the left subtree of the root. With the rule of product inside each case, this gives $C_n = \sum_{i=0}^{n-1} C_i C_{n-1-i}$. See [Catalan numbers](/catalan-numbers/).

## Variations

- **Overlapping cases.** If the sets may overlap, the sum counts each object once for each set that holds it. The exact count is given by the [inclusion-exclusion principle](/inclusion-exclusion-principle/). The sum is still an upper bound: $|S_1 \cup \cdots \cup S_k| \le \sum_i |S_i|$, which in probability is the [union bound](/union-bound/).
- **Weights.** If each object $x$ has a weight $w(x)$, then the total weight of a disjoint union is the sum of the total weights of the parts. With $w(x)$ equal to a probability, this is the additivity of probability for disjoint events.
- **Counting with a generating function.** The rule of sum for classes of objects is the sum of their [generating functions](/generating-functions/). The disjoint union of two combinatorial classes has the generating function $A(z) + B(z)$.
- **Bijections.** Once a case is matched one to one with a known set, its size is known. See [bijective proof](/bijective-proof/).

## Pitfalls

- **Cases that overlap.** To count the integers from 1 to 100 that are divisible by 2 or by 3, the sum $50 + 33 = 83$ is wrong. The 16 multiples of 6 are in both cases. The correct count is $50 + 33 - 16 = 67$.
- **A split that is not a function.** For strings of length 3 over $\{a, b\}$ that contain $aa$, the cases "starts with $aa$" (2 strings) and "ends with $aa$" (2 strings) give 4. The string $aaa$ is in both cases, and the correct count is 3: $aaa$, $aab$, $baa$. Choose a property that each object has exactly one value of, for example "the position of the first $aa$".
- **A missing case.** In example 1, forgetting the length 6 or treating the range as 6 to 7 loses a whole case. Check that the values of the property cover every object.
- **The empty object.** A recurrence must count the empty object in exactly one case. In example 4, $f(0) = 1$ counts the empty composition. With $f(0) = 0$ every later value is wrong.

## Exercises

1. Count the strings of length $n$ over $\{0, 1\}$ with no two adjacent 1s, by a split on the last symbol. Show that the count is the Fibonacci number $f(n + 1)$ of example 4.
2. Count the integers from 1 to 999 whose decimal digits are all different, by a split on the number of digits. The answer is $9 + 81 + 648 = 738$.
3. Show that the number of subsets of $[n]$ with an even number of elements is $2^{n-1}$ for $n \ge 1$, by a split on whether the subset contains $n$.

## References
