---
tag: Q97T2A
kind: algorithm
slug: bottom-up-enumerative-synthesis
name: Bottom-up enumerative synthesis
aliases:
- observational equivalence pruning
area: compilers-and-program-analysis/verification-and-synthesis
level: core
summary: Enumerates programs of growing size from smaller ones and keeps one program per distinct output vector on the examples.
model: word-ram
complexity:
  vars: {b: the number of kept programs, k: the number of examples}
  time: {binary rules only: O(k b^2), with if-then-else: O(k b^3) worst case}
  space: {all: O(k b)}
properties: {deterministic: true, recursive: false}
history:
  year: 2013
  people: [Abhishek Udupa, Arun Raghavan, Jyotirmoy V. Deshmukh, Sela Mador-Haim, Milo M. K. Martin, Rajeev Alur, Aws Albarghouthi, Sumit Gulwani, Zachary Kincaid]
  note: Observational equivalence was used in TRANSIT (PLDI 2013) and in Escher (CAV 2013). The enumerative solver of the first SyGuS competition was built on it.
prereqs: [programming-by-example]
see_also: [syntax-guided-synthesis, cegis, version-space-algebra, string-transformation-synthesis, type-directed-synthesis, superoptimization, equality-saturation, hash-consing]
sources:
  - paper: doi:10.1145/2491956.2462174
    title: Abhishek Udupa, Arun Raghavan, Jyotirmoy V. Deshmukh, Sela Mador-Haim, Milo M. K. Martin and Rajeev Alur, TRANSIT, specifying protocols with concolic snippets, Programming Language Design and Implementation (PLDI 2013)
    locator: pp. 287-296, the enumeration of expressions by size with pruning of expressions that agree on the concrete examples
  - paper: doi:10.1007/978-3-642-39799-8_67
    title: Aws Albarghouthi, Sumit Gulwani and Zachary Kincaid, Recursive program synthesis, Computer Aided Verification (CAV 2013)
    locator: pp. 934-950, the Escher algorithm, forward search over values with observational equivalence and goal graphs for conditionals
  - paper: doi:10.1109/FMCAD.2013.6679385
    title: Rajeev Alur, Rastislav Bodík, Garvit Juniwal, Milo M. K. Martin, Mukund Raghothaman, Sanjit A. Seshia, Rishabh Singh, Armando Solar-Lezama, Emina Torlak and Abhishek Udupa, Syntax-guided synthesis, Formal Methods in Computer-Aided Design (FMCAD 2013)
    locator: the enumerative solver with observational equivalence inside the CEGIS loop
  - paper: doi:10.1561/2500000010
    title: Sumit Gulwani, Oleksandr Polozov and Rishabh Singh, Program Synthesis, Foundations and Trends in Programming Languages 4(1-2), 2017
    locator: chapter 4, enumerative search, bottom-up and top-down enumeration and the pruning of equivalent programs
---

Bottom-up enumerative synthesis finds a program from input-output examples by building all programs of a grammar in order of size. Programs of size $s$ are built from kept programs of smaller sizes, so nothing is built twice. The key step is *observational equivalence*: two programs that give the same outputs on all example inputs are interchangeable inside any larger program, so only the first one is kept. The first program that gives the wanted outputs has the least size. It is the simplest complete method for [programming by example](/programming-by-example/) and for [syntax-guided synthesis](/syntax-guided-synthesis/), where it serves as the synthesizer inside [CEGIS](/cegis/).

## In plain words

Say you want a formula in x and y that gives 2 for the pair (1, 2) and 3 for (3, 1). Start with the smallest formulas: x, y, 0 and 1. Combine them with plus, minus and times to get the formulas with three symbols, then combine again, and so on. Stop at the first formula that gives the wanted answers.

Many formulas act the same on the examples. On these two pairs, "x + 0", "0 + x" and "x times 1" all give 1 and 3, just like x itself. Any larger formula that uses one of them gives the same answers as the one that uses x. So keep only the first formula for each list of answers and forget the rest. This cuts the search a lot, and it still finds a shortest formula.

## The problem

**Input.** A grammar with sorts, a start sort, examples $(i_1, o_1), \ldots, (i_k, o_k)$, and a size bound maxsize.

**Output.** A program $P$ of the start sort with $[\![P]\!](i_j) = o_j$ for all $j$ and of least size, or "none" if no such program has size at most maxsize.

The grammar on this page and in the code has two sorts:

- $I ::= x \mid y \mid 0 \mid 1 \mid I + I \mid I - I \mid I \times I \mid \mathrm{ite}(B, I, I)$
- $B ::= I \le I$

The size of a program is its number of nodes, so $x + y$ has size 3 and ite$(x \le y, y, x)$ has size 6. The *vector* of a program is the tuple of its outputs on $i_1, \ldots, i_k$.

## The algorithm

```pseudo id=main
SYNTHESIZE(examples, maxsize)
L1  seen[T] ← ∅ for each sort T          ▷ the vectors of the kept programs
L2  for s = 1, 2, …, maxsize do
L3      for each program P = r(Q1, …, Qm) of size s, with kept parts Q1, …, Qm, of sort T do
L4          v ← Fr(vec(Q1), …, vec(Qm))      ▷ the outputs of P on the example inputs
L5          if v ∈ seen[T] then continue      ▷ observationally equivalent to a kept program
L6          seen[T] ← seen[T] ∪ {v}; keep P with its vector v
L7          if T is the start sort and v = (o1, …, ok) then return P
L8  return none
```

**Building by size (lines L2 and L3).** For a binary rule, a program of size $s$ has parts of sizes $s_1$ and $s - 1 - s_1$. The loop goes over all splits and over all kept programs of these sizes. For ite, it goes over the sizes of the condition and of the two branches. The parts are always smaller, so they were kept in an earlier round.

**Vectors (line L4).** The algorithm never runs a whole program. It stores the vector of each kept program and computes the vector of a new program from the vectors of its parts, one example at a time: the vector of $P + Q$ is the sum of the two vectors, and the vector of ite$(B, P, Q)$ takes the entry of $P$ where $B$ is true and of $Q$ where it is false. This needs a semantics where the value of an operator depends only on the values of its arguments on the same input.

**Pruning (lines L5 and L6).** A hash set of vectors, one for each sort, finds a duplicate in expected constant time per vector. The first program with a vector is kept. Since rounds go by size, it is a smallest program with that vector.

## Example

Take the examples $(1, 2) \mapsto 2$ and $(3, 1) \mapsto 3$, so the wanted vector is $(2, 3)$.

- **Size 1.** The four leaves have the vectors $x = (1, 3)$, $y = (2, 1)$, $0 = (0, 0)$ and $1 = (1, 1)$. All four are kept.
- **Size 3.** There are 48 programs of sort $I$ with 3 nodes. They have 22 distinct vectors, and 4 of these are the vectors of the leaves: $x + 0$, $0 + x$, $x - 0$, $x \times 1$ and $1 \times x$ all have the vector of $x$, and 12 programs, from $x - x$ to $0 \times 1$, have the vector of $0$. So 18 are new. The vector $(2, 3)$ comes first from $x \times y$, and the search returns it.

This is the trap of [programming by example](/programming-by-example/): $x \times y$ is the smallest program that fits, but on $(2, 2)$ it gives 4. If the user wanted the maximum, the examples did not say so.

**A third example.** Add $(2, 2) \mapsto 2$. The wanted vector is now $(2, 3, 2)$.

| size | kept programs of sort $I$ | kept programs of sort $B$ | all programs of sort $I$ |
|---|---|---|---|
| 1 | 4 | 0 | 4 |
| 3 | 18 | 6 | 48 |
| 5 | 77 | 0 | 1,152 |
| 6 | hit | 0 | 256 |

No program of size at most 5 fits. At size 6 the search builds ite$(B, P, Q)$ with a condition of size 3 and two leaves, and the first hit is ite$(x \le y, y, x)$, the maximum. Over three examples a condition has at most $2^3 = 8$ vectors, and only 6 of them occur, so 6 conditions are kept out of 16. In all, the search builds 665 programs of both sorts before it returns. Without line L5 it builds 1,625. Adding the examples $(3, 5) \mapsto 5$ and $(5, 3) \mapsto 5$ gives the same program and the same counts. With no hit at all, an exhaustive run up to size 7 builds 4,500 programs with pruning and 47,940 without.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). The main lemma states that after round $s$, for every program $P$ of size at most $s$ there is a kept program of the same sort, no larger, with the same vector. It holds by induction on $P$: replace each part by its kept twin, which is no larger and has the same vector. The new program has the same vector as $P$ by compositionality, and either it is kept or a program with its vector was kept before. So if a correct program of size $r$ exists, a kept program with the wanted vector exists after round $r$, and line L7 returned it. The first return is therefore a smallest correct program, and "none" means that no program of size at most maxsize fits. The same proof works for any cost that is a positive integer weight per rule, summed over the nodes.

## Complexity

Let $b$ be the number of kept programs and $k$ the number of examples. A binary rule combines $O(b^2)$ pairs of kept programs, and ite combines $O(b^3)$ triples. Each new vector costs $O(k)$ time to compute and to look up in the hash set, in expectation. So the time is $O(k b^2)$ for binary rules and $O(k b^3)$ in the worst case with ite. The space is $O(k b)$ for the kept vectors.

The number $b$ is at most the number of distinct vectors. If each output can take $V$ values, that is at most $V^k$, and for a Boolean sort it is at most $2^k$. It is also at most the number of programs, which grows exponentially with the size: the grammar above has 4, 48, 1,152 and 34,560 programs of sort $I$ with 1, 3, 5 and 7 nodes. Pruning makes $b$ much smaller, but the search stays exponential in the size of the answer.

## Properties

- **Least size.** The result is a smallest program that fits, for the grammar and the cost model. It is not always the intended one.
- **Complete up to the bound.** If a program of size at most maxsize fits, the search finds one.
- **Needs only the examples.** It never calls a solver. In a CEGIS loop the verifier adds a new example after each wrong guess, and the search starts again with a finer equivalence.
- **Deterministic.** The order of rules and parts fixes which program of the least size is returned.

## Variants and improvements

- **Top-down enumeration.** Expand the grammar from the start symbol and prune partial programs that cannot fit. Pruning by vectors does not apply directly, because the parts of a partial program are not complete. [Type-directed synthesis](/type-directed-synthesis/) is a top-down method.
- **Divide and conquer.** The EUSolver of Alur, Radhakrishna and Udupa enumerates small terms that each fit some of the examples, and joins them with conditions learned as a decision tree.
- **Goal graphs.** Escher (Albarghouthi et al. 2013) splits a wanted vector into the parts where a condition is true and false, and searches for the branches as separate goals. It also allows recursion by looking up the values of recursive calls in the examples.
- **Equivalence by rewriting.** Instead of vectors, a search can keep one term per class of terms that are equal by rewrite rules, as [equality saturation](/equality-saturation/) does. This keeps terms that are equal for all inputs, not just on the examples.
- **Weighted grammars.** Give each rule a cost, or a probability learned from a corpus, and enumerate in order of cost.

## When to use it

Use it when the programs are small expressions over a fixed grammar, the examples are cheap to evaluate, and the semantics is compositional. It is the default synthesizer inside CEGIS for SyGuS tasks over integers and bit vectors, and a good baseline for any new synthesis problem. For strings with a known structure, a [version space algebra](/version-space-algebra/) such as the one in [string transformation synthesis](/string-transformation-synthesis/) holds all fitting programs at once. For large programs or deep conditionals, use a solver or a top-down method with stronger pruning.

## Pitfalls

- **The examples decide the answer.** Two examples gave $x \times y$ for a maximum. The smallest fitting program is often wrong, so add examples, ask the user about an input where two kept programs disagree, or use a verifier.
- **Exponential growth.** Each round can multiply the number of programs. Doubling the size bound does not double the time; it can make the search run out of memory.
- **Non-compositional operators.** Pruning is correct only if the value of an operator depends on the values of its arguments on the same input. Programs with side effects, a hidden state, or recursive calls to the program being built break this.
- **Errors and exceptions.** If a program fails on an input, its vector must record the failure as a value, such as a special marker. Dropping such programs is safe only if no operator can recover from the failure.
- **Floating point.** Two programs can give values that differ in the last bit and still mean the same function. Exact equality of vectors keeps both; rounding can merge two different functions.
- **Equivalence on the examples only.** Two kept programs can differ on other inputs. Pruning one of them is safe for the search, because the examples are the specification, but a new example can make them differ, and then the search must start again.

## Implementations

## History

Udupa, Raghavan, Deshmukh, Mador-Haim, Martin and Alur (2013) used enumeration by size with pruning of expressions that agree on the concrete examples in TRANSIT, a tool for completing cache coherence protocols. In the same year Albarghouthi, Gulwani and Kincaid built Escher, which searches forward over values with observational equivalence and adds goal graphs for conditionals and recursion. Alur and others (2013) defined syntax-guided synthesis, and the enumerative solver based on this pruning won the first SyGuS competition in 2014. The survey of Gulwani, Polozov and Singh (2017) describes bottom-up and top-down enumeration as one of the main search methods of program synthesis.

## References
