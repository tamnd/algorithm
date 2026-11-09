---
tag: 69B3GH
kind: technique
slug: tseitin-transformation
name: Tseitin transformation
aliases:
- Tseitin encoding
- Tseytin transformation
- definitional CNF
area: logic-and-constraints/sat-solving
level: core
summary: Convert a Boolean circuit into an equisatisfiable CNF of linear size, with one new variable for each gate.
prereqs: [conjunctive-normal-form, boolean-circuit]
see_also: [plaisted-greenbaum-transformation, circuit-sat, cook-levin-theorem, bit-blasting, sat-based-bounded-model-checking, model-counting]
sources:
  - paper: doi:10.1007/978-3-642-81955-1_28
    title: G. S. Tseitin, On the complexity of derivation in propositional calculus, in Studies in Constructive Mathematics and Mathematical Logic, Part II, 1968; reprinted in Siekmann and Wrightson (eds.), Automation of Reasoning 2, Springer, 1983, 466-483
    locator: the definition of the extension rule, which introduces a new variable for a subformula
  - book: isbn:9781643681603
    title: Biere, Heule, van Maaren and Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 2 (Prestwich, CNF Encodings), the section on the Tseitin encoding
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2, 2022
    locator: Section 7.2.2.2, Satisfiability, the encoding of circuits into clauses
  - book: isbn:9783662504963
    title: Daniel Kroening and Ofer Strichman, Decision Procedures, second edition, Springer, 2016
    locator: Chapter 1, Tseitin's encoding
---

The Tseitin transformation turns a [Boolean circuit](/boolean-circuit/) or formula into a formula in [conjunctive normal form](/conjunctive-normal-form/) with one new variable for each gate. The result is not equivalent to the input, but it is *equisatisfiable*: it has a model if and only if the circuit has a satisfying input, and each model of the result restricts to a satisfying input. Its size is linear in the size of the circuit, while the textbook conversion by the distributive law can be exponential. It is the standard way to give a circuit or a formula to a [SAT](/sat/) solver, and the reason why [CIRCUIT-SAT](/circuit-sat/) reduces to SAT in linear time.

## In plain words

A SAT solver reads only a list of clauses. A circuit has gates that feed other gates. To turn the circuit into clauses, give each gate a new name, a fresh variable. Then write a few short clauses that say "this name has exactly the value that the gate computes from its inputs". An AND gate with two inputs needs three clauses, and an OR gate needs three clauses too. At the end, add one clause that says "the output name is true".

The new list of clauses is about as long as the circuit. Each satisfying input of the circuit gives exactly one way to fill in the gate names, so the clauses have a solution exactly when the circuit can output true.

## When it applies

Use the transformation when the input of a problem is a circuit, a formula with nested AND, OR, NOT and XOR, or a program that was unrolled into such a formula, and the target is a CNF solver. Typical signals:

- The formula is not in CNF, and converting it with the distributive law gives too many clauses.
- The formula has shared subformulas (a circuit, not a tree). The transformation gives each shared gate one variable, so the sharing stays.
- You need satisfiability, not logical equivalence. The new variables change the set of models, so the result is not a replacement for the formula inside a larger formula.

## The template

Notation: the circuit has $n$ inputs $x_1, \ldots, x_n$ and $s$ gates in topological order. Gate $i$ gets the variable $y = n + 1 + i$ and computes AND, OR (of any fan-in $k$) or XOR (of two inputs) of earlier literals. A literal is a variable or its negation, so a NOT gate needs no variable: its output is the literal $\neg v$. The output of the circuit is a literal $o$. We write $|F|$ for the number of literal occurrences of a CNF $F$, and $m$ for its number of clauses.

```pseudo id=main
TSEITIN(n, gates, o)                     ▷ gates in topological order
L1  for each gate i with operator op and argument literals a_1 .. a_k do
L2      y ← n + 1 + i                      ▷ the fresh variable of gate i
L3      add DEFINE(op, y, a_1 .. a_k) to F
L4  add the unit clause (o) to F; return F

DEFINE(op, y, a_1 .. a_k)                ▷ clauses of y ↔ op(a_1 .. a_k)
L5  if op = AND: return (¬y ∨ a_j) for j = 1 .. k, and (y ∨ ¬a_1 ∨ … ∨ ¬a_k)
L6  if op = OR:  return (y ∨ ¬a_j) for j = 1 .. k, and (¬y ∨ a_1 ∨ … ∨ a_k)
L7  if op = XOR: return (¬y ∨ a ∨ b), (¬y ∨ ¬a ∨ ¬b), (y ∨ ¬a ∨ b), (y ∨ a ∨ ¬b)
```

The holes of the template are the gate set and the clauses of DEFINE. Any gate type works if DEFINE returns a CNF that is equivalent to $y \leftrightarrow op(a_1, \ldots, a_k)$. For AND, the $k$ binary clauses of line L5 say $y \to a_j$ for each $j$, and the long clause says $a_1 \wedge \cdots \wedge a_k \to y$. Line L6 is the dual for OR. The four clauses of line L7 exclude the four rows of the truth table where $y \ne a \oplus b$.

### Example

Take $\varphi = (x_1 \wedge \neg x_2) \vee (x_2 \wedge x_3)$. The gates are $y_4 = x_1 \wedge \neg x_2$, $y_5 = x_2 \wedge x_3$ and $y_6 = y_4 \vee y_5$, and the output is $y_6$. The transformation gives 10 clauses with 22 literal occurrences:

| gate | clauses |
|---|---|
| $y_4 \leftrightarrow x_1 \wedge \neg x_2$ | $(\neg y_4 \vee x_1)$, $(\neg y_4 \vee \neg x_2)$, $(y_4 \vee \neg x_1 \vee x_2)$ |
| $y_5 \leftrightarrow x_2 \wedge x_3$ | $(\neg y_5 \vee x_2)$, $(\neg y_5 \vee x_3)$, $(y_5 \vee \neg x_2 \vee \neg x_3)$ |
| $y_6 \leftrightarrow y_4 \vee y_5$ | $(y_6 \vee \neg y_4)$, $(y_6 \vee \neg y_5)$, $(\neg y_6 \vee y_4 \vee y_5)$ |
| output | $(y_6)$ |

The formula $\varphi$ has 4 models over $x_1, x_2, x_3$: $100$, $101$, $011$ and $111$. The CNF has exactly 4 models over its 6 variables, one above each of them. For the input $x = 101$ the gate values are $y_4 = 1$, $y_5 = 0$, $y_6 = 1$, and no other values of $y_4, y_5, y_6$ satisfy the clauses.

### Why it is correct

Let $D$ be the clauses of lines L1 to L3 (all clauses except the unit clause of line L4), and let $T = D \cup \{(o)\}$.

**Lemma 1.** For each $op$, the clauses of DEFINE$(op, y, a_1, \ldots, a_k)$ are satisfied by an assignment exactly when it gives $y$ the value $op(a_1, \ldots, a_k)$.

*Proof.* AND: the clauses $(\neg y \vee a_j)$ for all $j$ hold exactly when $y = 1$ implies that all $a_j = 1$. The clause $(y \vee \neg a_1 \vee \cdots \vee \neg a_k)$ holds exactly when all $a_j = 1$ implies $y = 1$. Together they say $y = a_1 \wedge \cdots \wedge a_k$. OR is the same argument with each literal negated. XOR: each of the four clauses is false on exactly one row of the truth table of $(y, a, b)$, namely $(1, 0, 0)$, $(1, 1, 1)$, $(0, 1, 0)$ and $(0, 0, 1)$. These are the four rows with $y \ne a \oplus b$. $\square$

**Lemma 2 (unique extension).** For each assignment $\alpha$ of the inputs, exactly one assignment $\beta$ of the gate variables makes $\alpha \cup \beta$ satisfy $D$, namely $\beta(y_i) = \text{val}_i(\alpha)$, the value that gate $i$ computes on $\alpha$.

*Proof.* By induction on the gate index $i$. The arguments of gate $i$ are inputs or literals of gates $j < i$. By the induction hypothesis, each assignment that satisfies the clauses of gates $0, \ldots, i-1$ gives every $y_j$ with $j < i$ the value $\text{val}_j(\alpha)$. By Lemma 1, the clauses of gate $i$ then hold exactly when $y_i = op_i(\ldots) = \text{val}_i(\alpha)$. So there is exactly one choice for $y_i$. $\square$

**Theorem.** The models of $T$ are exactly the assignments $\alpha \cup \text{val}(\alpha)$ where $\alpha$ is an input on which the circuit outputs 1. So $T$ is satisfiable if and only if the circuit is satisfiable, the projection of each model of $T$ to $x_1, \ldots, x_n$ is a satisfying input, and $T$ has exactly as many models as the circuit has satisfying inputs.

*Proof.* By Lemma 2, an assignment satisfies $D$ if and only if it has the form $\alpha \cup \text{val}(\alpha)$. It also satisfies $(o)$ if and only if the output literal is true under it, that is, if the circuit outputs 1 on $\alpha$. The map $\alpha \mapsto \alpha \cup \text{val}(\alpha)$ is a bijection between the satisfying inputs and the models of $T$. $\blacksquare$

In logical terms, the formula $\exists y_{n+1} \cdots \exists y_{n+s}\, T$ is equivalent to the circuit. The transformation preserves the number of models, so it is a [parsimonious reduction](/parsimonious-reduction/). This matters for [model counting](/model-counting/).

### Size and time

A gate of fan-in $k$ gives $k + 1$ clauses with $3k + 1$ literal occurrences if it is AND or OR, and 4 clauses with 12 literal occurrences if it is XOR. With $s$ gates and $w$ wires (the sum of the fan-ins), the result has at most $w + 2s + 1$ clauses and at most $3w + 6s + 1$ literal occurrences, and $n + s$ variables. Each gate is handled in $O(k)$ time. So the transformation takes $\Theta(n + s + w)$ time and gives a CNF of size $\Theta(s + w)$, linear in the size of the circuit. This is a worst-case bound with no hidden condition.

## Classic examples

- **Distributive blow-up.** The formula $(x_1 \wedge y_1) \vee \cdots \vee (x_k \wedge y_k)$ has a smallest CNF of $2^k$ clauses with $k$ literals each, one for each choice of $x_i$ or $y_i$ in every term. The Tseitin transformation gives $4k + 2$ clauses with $10k + 2$ literal occurrences. For $k = 10$ that is 42 clauses instead of 1024.
- **Parity.** A CNF of $x_1 \oplus \cdots \oplus x_k = 1$ without new variables needs $2^{k-1}$ clauses: a clause with fewer than $k$ variables excludes a subcube that holds assignments of both parities, so each clause excludes exactly one of the $2^{k-1}$ even assignments. A chain of $k - 1$ XOR gates gives $4(k-1) + 1$ clauses, so 37 clauses for $k = 10$ instead of 512.
- **CIRCUIT-SAT to SAT.** The [Cook-Levin theorem](/cook-levin-theorem/) and the reduction from [CIRCUIT-SAT](/circuit-sat/) to [3-SAT](/3-sat/) are this transformation: with fan-in 2, every clause has at most 3 literals.
- **Hardware and software verification.** [Bit-blasting](/bit-blasting/) turns bit-vector terms into gates, and [SAT-based bounded model checking](/sat-based-bounded-model-checking/) unrolls a transition relation into a circuit. Both then use this transformation.

## Variations

- **Plaisted-Greenbaum.** Keep only one direction of each definition, chosen by the polarity of the gate. See [Plaisted-Greenbaum transformation](/plaisted-greenbaum-transformation/). It gives fewer clauses but does not preserve the number of models.
- **Formulas instead of circuits.** For a formula tree, use one variable per subformula. Detect equal subformulas first (by hashing), so that each one gets one variable. This turns the tree into a circuit and can make the CNF much smaller.
- **No variable for small gates.** A gate that is used once and whose inputs are inputs of the circuit can be expanded in place when that gives fewer clauses. Solvers and encoders do this for small subformulas.
- **And-inverter graphs.** Many tools first rewrite the circuit with AND gates and negated edges only. Then line L5 is the only rule, and each gate gives three clauses.
- **Extended resolution.** Tseitin introduced the new variables in a proof system: the extension rule adds $y \leftrightarrow (a \wedge b)$ for a fresh $y$. The proof system extended resolution is much stronger than plain resolution. See [Haken's resolution lower bound](/haken-resolution-lower-bound/) for the limit of plain resolution.

## Pitfalls

- **The result is not equivalent.** $T$ has more variables, and a model of the circuit is not a model of $T$ until you add the gate values. Do not substitute $T$ for the formula inside a larger formula, and do not negate $T$ to get a CNF of the negated formula. To prove that $\varphi$ is valid, transform $\neg \varphi$ (output literal $\neg o$ in line L4) and check that the result is unsatisfiable.
- **Forgetting line L4.** Without the unit clause, $D$ alone is always satisfiable, by Lemma 2.
- **One variable per occurrence.** If a shared gate gets a new variable each time it is used, a circuit of size $s$ can turn into a tree of size $2^s$. Give each gate one variable.
- **Wide XOR gates.** A direct CNF of an XOR of $k$ literals has $2^{k-1}$ clauses. Split it into a chain or a tree of binary XOR gates, as in the parity example.
- **Clause width.** With fan-in $k$, line L5 makes a clause of width $k + 1$. If the solver or the reduction needs width 3, split the gates to fan-in 2 first.

## Exercises

1. Give the clauses of DEFINE for a multiplexer $y \leftrightarrow (s \wedge a) \vee (\neg s \wedge b)$ with 4 clauses of width 3, and prove them correct with the truth table.
2. Show that unit propagation on $T$ computes the circuit: if all inputs are assigned, unit propagation assigns every gate variable to its value. Does the same hold for the Plaisted-Greenbaum encoding?
3. Count the clauses of the Tseitin CNF of a ripple-carry adder of two $b$-bit numbers built from full adders with 2 XOR, 2 AND and 1 OR gate each.

## References
