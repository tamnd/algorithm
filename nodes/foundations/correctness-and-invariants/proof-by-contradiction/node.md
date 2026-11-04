---
tag: GAZPHR
kind: technique
slug: proof-by-contradiction
name: Proof by contradiction
aliases:
- Reductio ad absurdum
- Indirect proof
area: foundations/correctness-and-invariants
level: intro
summary: Assumes the negation of the claim and derives a contradiction; common in lower-bound and optimality proofs.
prereqs: [induction]
see_also: [well-ordering-principle, exchange-argument, induction, termination-proof, adversary-argument, cut-and-paste-argument, halting-problem, comparison-sort-lower-bound]
sources:
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 0.4, Types of proof (proof by contradiction), and Section 4.2, Undecidability (the halting problem)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 8.1, Lower bounds for sorting
  - url: https://mathcs.clarku.edu/~djoyce/elements/bookIX/propIX20.html
    title: David E. Joyce, Euclid's Elements, Book IX, Proposition 20
    locator: Proposition IX.20
  - url: https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-spring-2015/mit6_042js15_textbook2.pdf
    title: Eric Lehman, F. Thomson Leighton and Albert R. Meyer, Mathematics for Computer Science (2015 version)
    locator: Section 1.8, Proof by contradiction
---

Proof by contradiction proves a statement $S$ by assuming that $S$ is false and deriving a statement that cannot be true. Because the assumption leads to an impossible result, the assumption is wrong, and $S$ holds. It is also called reductio ad absurdum. In algorithm analysis it appears in lower bounds, in proofs of optimality and in proofs that a certain object does not exist.

## In plain words

You want to show that something is true. You suppose that it is false, and you follow the logic. If you reach a result that is plainly impossible, such as a number that is both even and odd, then your supposition was wrong. So the thing is true.

This is a useful tool when the claim says "there is no" or "it is never". A direct proof must build the result from the hypotheses alone. A proof by contradiction also gives you a hypothetical bad case to work with. You can ask what that bad case looks like, and show that it cannot exist.

A related tool is the contrapositive. It is not the same. The contrapositive turns "if A then B" into "if not B then not A". It does not need an impossible result. Both tools appear below.

## When it applies

- The claim is a negative: there is no such object, the bound cannot be lower, the value is not rational.
- The claim says "for all" and the negation, "there is one that fails", gives you an object to inspect. A least counterexample is often available by the [well-ordering principle](/well-ordering-principle/).
- A direct proof would need a long list of cases, but one extra assumption removes the cases.
- The claim is about every algorithm in a class, as in a lower bound. You fix a hypothetical algorithm that beats the bound, and show a contradiction.

## The template

To prove a statement $S$, fill the named holes of this outline.

```
Claim: ⟨S⟩.
Proof. Assume, for a contradiction, ⟨¬S, with the quantifiers turned over⟩.
  Let ⟨witness⟩ be an object that makes ¬S true.        ▷ often the least one
  From ⟨¬S⟩ and ⟨facts already proved⟩, derive ⟨T⟩.
  From ⟨other steps⟩, derive ⟨¬T⟩.
  This is a contradiction, so ¬S is false, and ⟨S⟩ holds.  ∎
```

- **The negation.** Write $\neg S$ in full. The negation of $\forall x\, \exists y\, R(x,y)$ is $\exists x\, \forall y\, \neg R(x,y)$.
- **The witness.** When $S$ says "for all", $\neg S$ says "there is one that fails". Name that object, and choose an extreme one (least, largest, first) when this helps.
- **The contradiction.** $T$ and $\neg T$ can be any pair: the witness and a proved fact, or two facts that the steps derive.

In logic, the rule is: if $\neg S \Rightarrow \bot$ is proved, then $S$ holds. When $S$ is itself a negative claim $\neg P$, such as "$\sqrt{2}$ is not rational", the proof assumes $P$ and derives $\bot$. This is the rule of negation introduction, and it is valid in constructive logic too. Only the step from $\neg\neg S$ to a positive $S$ needs the law of excluded middle. A proof that uses this step is not constructive: it may show that an object exists without giving it.

**Difference from contraposition.** To prove $A \Rightarrow B$ by contraposition, you prove $\neg B \Rightarrow \neg A$. You assume $\neg B$ and you reach $\neg A$. The proof ends in the statement that you want, and no contradiction occurs. To prove $A \Rightarrow B$ by contradiction, you assume both $A$ and $\neg B$, and you reach some false statement. This false statement can be anything: it may be $\neg A$, or it may be a fact that has no link to $A$. Every proof by contraposition is also a proof by contradiction, because you can assume $A$ in addition and reach $\neg A$ next to $A$. The opposite does not hold. A proof by contradiction that reaches a false statement other than $\neg A$ is not a contraposition.

## Classic examples

The examples go from simple to hard. The first two are short proofs from number theory. The third is a lower bound for an algorithm, worked in full. The list at the end gives the standard uses in algorithms, each on its own page.

### The square root of 2 is irrational

**Claim.** There are no positive integers $a, b$ with $a^2 = 2b^2$ and $\gcd(a, b) = 1$. Hence $\sqrt{2}$ is not a quotient of integers.

**Proof.** Assume such $a, b$ exist. Then $a^2$ is even, so $a$ is even, because the square of an odd number is odd. Write $a = 2c$. Then $4c^2 = 2b^2$, so $b^2 = 2c^2$, and $b$ is even too. Both are even, so $\gcd(a, b) \ge 2$. This contradicts $\gcd(a, b) = 1$. If $\sqrt{2} = a/b$, we can reduce the quotient to lowest terms, which gives such a pair. So $\sqrt{2}$ is irrational. $\blacksquare$

### There are infinitely many primes

This proof is in Euclid's *Elements*, Book IX, Proposition 20.

**Claim.** The set of prime numbers is infinite.

**Proof.** Assume that the set is finite. It is not empty, because 2 is prime. Let the primes be $p_1, \ldots, p_k$ and let $N = p_1 p_2 \cdots p_k + 1$. Then $N \ge 3$. Every integer greater than 1 has a prime divisor (this is the claim of exercise 4 in [induction](/induction/)). So some prime $q$ divides $N$. By the assumption, $q = p_i$ for some $i$. Then $q$ divides $p_1 \cdots p_k$. Since $q$ divides both $N$ and $N - 1 = p_1 \cdots p_k$, it divides their difference $N - (N-1) = 1$. But a prime is at least 2, and so it does not divide 1. This is a contradiction. So the set of primes is infinite. $\blacksquare$

Note what the proof does not say: $N$ need not be prime. For the first six primes, $N = 2 \cdot 3 \cdot 5 \cdot 7 \cdot 11 \cdot 13 + 1 = 30031 = 59 \cdot 509$.

### Finding the minimum needs $n - 1$ comparisons

This is an algorithmic lower bound. The model is a deterministic algorithm that learns about its input only by comparing two keys, and that outputs the index of the least key.

**Claim.** Let $n \ge 1$. Let $\mathcal{A}$ be a deterministic comparison algorithm that is correct on each array of $n$ distinct keys. Then on each such array, $\mathcal{A}$ makes at least $n - 1$ comparisons.

**Proof.** Assume that on an input $x = (x_1, \ldots, x_n)$ of distinct keys, $\mathcal{A}$ makes fewer than $n - 1$ comparisons. Let $G$ be the graph on the vertices $\{1, \ldots, n\}$ that has an edge $\{i, j\}$ when $\mathcal{A}$ compares $x_i$ and $x_j$ on this input. $G$ has at most $n - 2$ edges. A connected graph on $n$ vertices has at least $n - 1$ edges, so $G$ is not connected. Let $m$ be the index that $\mathcal{A}$ outputs. Because $G$ has at least two components, there is a component $C$ that does not contain $m$. Let $D$ be a number larger than $\max_i x_i - \min_i x_i$ and define $x'$ by $x'_i = x_i - D$ for $i \in C$, and $x'_i = x_i$ for $i \notin C$.

Compare $\mathcal{A}$ on $x$ and on $x'$. Each comparison of $\mathcal{A}$ on $x$ is between two indices in the same component of $G$. Both indices are in $C$, or both are outside $C$, and in both cases the shift keeps their order. So each comparison gives the same answer on $x'$ as on $x$. The algorithm is deterministic and learns only the answers, so it runs the same way on $x'$ and outputs $m$. But $m \notin C$, and for any $c \in C$ we have $x'_c = x_c - D < \min_i x_i \le x'_m$ (the last step holds because $x'_m = x_m$). So $x'_m$ is not the least key, and $\mathcal{A}$ is wrong on $x'$. The keys of $x'$ are distinct, since all keys in $C$ shift by the same amount and $D$ is large enough that a key in $C$ is below each key outside $C$. This contradicts the correctness of $\mathcal{A}$. $\blacksquare$

The scan that keeps the best key so far makes exactly $n - 1$ comparisons, so the bound is tight. For $n = 4$ and $x = (7, 3, 9, 5)$, an algorithm that compares only $x_1$ with $x_2$ and $x_3$ with $x_4$ makes 2 comparisons, and $G$ has the components $\{1, 2\}$ and $\{3, 4\}$. If it outputs $m = 2$, shift $C = \{3, 4\}$ by $D = 7$: $x' = (7, 3, 2, -2)$ gives the same answers, and the least key is now at index 4. This is a fooling-input argument (also called an indistinguishability argument): it fixes one input and builds a second input that the algorithm cannot tell apart from it. See [max-finding lower bound](/max-finding-lower-bound/) for the same bound for the maximum.

### More classic uses in algorithms

- **[Optimal substructure](/optimal-substructure/).** Assume that an optimal solution contains a part that is not optimal for its subproblem. Replace the part by a better one, and the whole solution gets better, which contradicts its optimality. This is the [cut-and-paste argument](/cut-and-paste-argument/), as in [shortest-path optimal substructure](/shortest-path-optimal-substructure/).
- **[Cut property](/cut-property/) of minimum spanning trees.** Let $e$ be the unique lightest edge across a cut, and assume a [minimum spanning tree](/minimum-spanning-tree/) $T$ does not contain $e$. Adding $e$ to $T$ makes a cycle, and this cycle crosses the cut at a second edge $f$, with $w(f) > w(e)$. Then $T + e - f$ is a spanning tree that is lighter than $T$. This is a contradiction.
- **Correctness of [Dijkstra's algorithm](/dijkstra/).** Assume that some vertex leaves the queue with a wrong distance, and take the first such vertex $u$. On a shortest path to $u$, the first vertex $y$ that is still in the queue has the correct distance, and with non-negative weights this distance is at most the true distance of $u$, which is less than the key of $u$. So $y$ leaves the queue before $u$, a contradiction. See [Dijkstra correctness](/dijkstra-correctness/).
- **[Comparison sort lower bound](/comparison-sort-lower-bound/).** Assume a comparison sort whose [decision tree](/decision-tree-model/) has fewer than $n!$ leaves. Then two different orders of the input reach the same leaf, the algorithm permutes both in the same way, and it is wrong on one of them. So the height is at least $\lg(n!)$ (CLRS, Section 8.1).
- **The [halting problem](/halting-problem/).** Assume a program $H$ that decides whether any program halts on any input. Build $D$ that, on input $\langle M \rangle$, asks $H$ about $M$ on $\langle M \rangle$ and does the opposite. Then $D$ on $\langle D \rangle$ halts exactly when it does not halt. This is the [diagonalization argument](/diagonalization-argument/). Sipser, Section 4.2, gives the same proof for the acceptance problem of Turing machines.

## Variations

- **Least counterexample.** Assume the claim fails for some natural number. By the [well-ordering principle](/well-ordering-principle/), there is a least $n$ where it fails. Show that $n - 1$ or a smaller value also fails. This is [induction](/induction/) in another form.
- **Contraposition.** Prove $\neg B \Rightarrow \neg A$ in place of $A \Rightarrow B$. Use it when the negations are easier to work with. For example, "if $n^2$ is even, then $n$ is even" is proved by: if $n$ is odd, $n = 2k + 1$ and $n^2 = 2(2k^2 + 2k) + 1$ is odd.
- **Exchange arguments.** A proof that a [greedy algorithm](/greedy-algorithm/) is optimal can be written as contradiction: assume a better solution, and take the one that agrees with the greedy choice for the longest time. Most texts present the same idea as a direct [exchange argument](/exchange-argument/).
- **Adversary arguments.** The minimum proof above fixes the input first. In an [adversary argument](/adversary-argument/), the adversary picks the answers to the comparisons online, as the algorithm asks them, so that at least two inputs stay consistent with all the answers. If the algorithm stops too early, it gives the same output on two inputs that need different outputs.

## Pitfalls

- **Using an unproved fact.** The contradiction must come from $\neg S$ and from true facts. If you use an unproved fact, you prove nothing.
- **A wrong negation.** The negation of "all items are positive" is "some item is not positive", and not "all items are negative". Write the negation in full before you go on.
- **A direct proof in disguise.** If the contradiction only repeats the assumption, remove the contradiction and state the proof as a direct proof. The assumption of $\neg S$ should be used in a real step.
- **A proof that a thing exists.** A proof by contradiction may show only that an object exists. It may give no way to find it. A classic case: there are irrational numbers $a, b$ with $a^b$ rational. If $\sqrt{2}^{\sqrt{2}}$ is rational, take $a = b = \sqrt{2}$. If not, take $a = \sqrt{2}^{\sqrt{2}}$ and $b = \sqrt{2}$, so that $a^b = \sqrt{2}^2 = 2$. The proof does not say which case holds. In algorithms, such a proof shows that a solution exists but gives no algorithm to find it.
- **Wrong scope in a lower bound.** In the minimum example, the algorithm must be correct on all inputs, and the claim is about comparison algorithms. A different model, such as a model with arithmetic on keys, needs a new proof.
- **Dividing by a value that can be zero.** A step such as "divide by $x$" needs $x \ne 0$. Check each such step in the derivation.

## Exercises

1. Prove by contradiction that there is no largest integer.
2. Prove that $\log_2 3$ is irrational. (Assume $\log_2 3 = a/b$ with positive integers $a, b$, and look at $2^a$ and $3^b$.)
3. Prove that the sum of a rational number and an irrational number is irrational.
4. Prove that among any $n + 1$ distinct integers from $\{1, \ldots, 2n\}$, two are consecutive. Use a contradiction and the pigeonhole principle on the pairs $\{1,2\}, \{3,4\}, \ldots$
5. Prove by contradiction: if $a$ and $b$ are integers and $a^2 + b^2$ is divisible by 4, then $a$ and $b$ are both even. Then say whether your proof is also a proof by contraposition.
6. Prove that if $n$ items are put in $n - 1$ boxes, some box holds two items.
7. Prove that a finite simple graph with at least one vertex, in which every vertex has degree at least 2, contains a cycle. Show that the claim fails for the infinite path $\ldots, -1, 0, 1, \ldots$ on the integers. (Assume that it is acyclic, and take a longest path.)

## References
