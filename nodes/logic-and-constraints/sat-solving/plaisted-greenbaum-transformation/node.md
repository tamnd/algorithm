---
tag: KVGY32
kind: technique
slug: plaisted-greenbaum-transformation
name: Plaisted-Greenbaum transformation
aliases:
- one-sided Tseitin encoding
- polarity-based CNF encoding
- structure-preserving clause form
area: logic-and-constraints/sat-solving
level: advanced
summary: A Tseitin encoding that keeps only the direction of each gate definition that its polarity needs, so it gives fewer clauses and stays equisatisfiable.
prereqs: [tseitin-transformation]
see_also: [tseitin-transformation, conjunctive-normal-form, boolean-circuit, model-counting, incremental-sat]
sources:
  - paper: doi:10.1016/S0747-7171(86)80028-1
    title: David A. Plaisted and Steven Greenbaum, A structure-preserving clause form translation, Journal of Symbolic Computation 2(3), 293-304, 1986
    locator: the translation that uses only one implication for each subformula, chosen by its polarity
  - book: isbn:9781643681603
    title: Biere, Heule, van Maaren and Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 2 (Prestwich, CNF Encodings), the section on the Tseitin and Plaisted-Greenbaum encodings
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms Part 2, 2022
    locator: Section 7.2.2.2, Satisfiability, the encoding of circuits into clauses
  - paper: doi:10.1007/978-3-642-12002-2_10
    title: Matti Järvisalo, Armin Biere and Marijn Heule, Blocked clause elimination, TACAS 2010, LNCS 6015, 129-144
    locator: the section on the effect of blocked clause elimination on CNF encodings of circuits (Plaisted-Greenbaum)
---

The Plaisted-Greenbaum transformation turns a [Boolean circuit](/boolean-circuit/) into a CNF in the same way as the [Tseitin transformation](/tseitin-transformation/), but it writes only one direction of each gate definition when one direction is enough. A gate that the output needs only to be true gets the clauses of $y \to \text{gate}$; a gate that it needs only to be false gets the clauses of $\text{gate} \to y$; a gate that it needs both ways gets both. The result is still equisatisfiable with the circuit, every model still restricts to a satisfying input, and for AND and OR gates it has about half the clauses. The price is that the gate variables are no longer determined by the inputs, so the number of models changes.

## In plain words

The Tseitin method writes, for each gate, "the new name is true exactly when the gate is true". That is two promises: "if the name is true, the gate is true" and "if the gate is true, the name is true".

Often only one promise is needed. Suppose the formula only ever needs a gate to be true, for example a gate inside an OR at the top. Then the solver only uses the name to claim that the gate is true. Only the first promise stops it from lying about that. The second promise never helps, so we drop it.

To know which promise each gate needs, follow the circuit from the output down. A NOT flips the need. A gate that is used in both ways keeps both promises.

## When it applies

Use it in place of the Tseitin transformation when:

- you only need a yes or no answer and a model of the inputs, not the number of models;
- many gates are used in one polarity only. In a circuit with AND, OR and NOT only, and with negations only at the inputs (negation normal form), every gate has the positive polarity alone;
- the CNF will not be changed later in a way that uses a gate in the other polarity. With [incremental SAT](/incremental-sat/), an assumption on a gate variable can need the dropped direction.

## The template

Notation: the circuit has $n$ inputs and $s$ gates, as on the [Tseitin page](/tseitin-transformation/). Gate $i$ defines the variable $y = n + 1 + i$ as AND or OR of literals of fan-in $k$, or XOR of two literals. The output is a literal $o$. The *polarity* $\text{pol}(v) \subseteq \{+, -\}$ of a variable $v$ is the set of signs with which it reaches the output.

**Definition (polarity).** The output variable $|o|$ has the polarity $+$ if $o$ is positive and $-$ if $o$ is negated. If gate $g$ is AND or OR and has an argument literal $a$, then the variable $|a|$ gets every sign of $\text{pol}(g)$, flipped when $a$ is negated. Both arguments of an XOR gate get both signs. A variable that is used several times gets the union of the signs.

```pseudo id=main
PLAISTED-GREENBAUM(n, gates, o)
L1  pol(|o|) ← {+} if o is positive, else {−}
L2  for each gate g from the last to the first do      ▷ reverse topological order
L3      for each argument literal a of g do
L4          if g is XOR: add {+, −} to pol(|a|)
L5          else: add pol(g) to pol(|a|), with each sign flipped when a is negated
L6  for each gate g with variable y do
L7      if + ∈ pol(y): add the clauses of y → op(args)
L8      if − ∈ pol(y): add the clauses of op(args) → y
L9  add the unit clause (o); return F
```

The two directions are the two halves of the Tseitin clauses:

| gate | $y \to op$ (needed for $+$) | $op \to y$ (needed for $-$) |
|---|---|---|
| $y = a_1 \wedge \cdots \wedge a_k$ | $(\neg y \vee a_j)$ for each $j$ | $(y \vee \neg a_1 \vee \cdots \vee \neg a_k)$ |
| $y = a_1 \vee \cdots \vee a_k$ | $(\neg y \vee a_1 \vee \cdots \vee a_k)$ | $(y \vee \neg a_j)$ for each $j$ |
| $y = a \oplus b$ | $(\neg y \vee a \vee b)$, $(\neg y \vee \neg a \vee \neg b)$ | $(y \vee \neg a \vee b)$, $(y \vee a \vee \neg b)$ |

Lines L1 to L5 visit each wire once, and so do lines L6 to L8. So the time is $\Theta(n + s + w)$ for $w$ wires, as for Tseitin, and the result is a subset of the Tseitin clauses.

### Example

Take $\varphi = (x_1 \wedge x_2) \vee x_3$ with the gates $y_4 = x_1 \wedge x_2$ and $y_5 = y_4 \vee x_3$, and the output $y_5$. Both gates have the polarity $\{+\}$. The result is

$$(\neg y_4 \vee x_1) \wedge (\neg y_4 \vee x_2) \wedge (\neg y_5 \vee y_4 \vee x_3) \wedge (y_5),$$

4 clauses with 8 literal occurrences. The Tseitin CNF has 7 clauses with 15 literal occurrences. The circuit has 5 satisfying inputs. The Tseitin CNF has 5 models, but this CNF has 6: for the input $x = 111$, both $y_4 = 1$ and $y_4 = 0$ satisfy it, because $y_5$ is already justified by $x_3$.

If the output is $\neg(x_1 \wedge x_2) \vee x_3$ instead, the AND gate sits under a NOT and gets the polarity $\{-\}$, so it gets only the clause $(y_4 \vee \neg x_1 \vee \neg x_2)$.

### Why it is correct

Write $\alpha$ for an assignment of the inputs and $\text{val}_g(\alpha)$ for the value that gate $g$ computes on $\alpha$. Write $P$ for the result. We order false before true, $0 < 1$.

**Lemma.** Let $\beta$ be a model of $P$, and let $\alpha$ be its restriction to the inputs. For each variable $v$ with $+ \in \text{pol}(v)$, $\beta(v) \le \text{val}_v(\alpha)$. For each variable $v$ with $- \in \text{pol}(v)$, $\beta(v) \ge \text{val}_v(\alpha)$. (For an input $v$, $\text{val}_v(\alpha) = \alpha(v) = \beta(v)$, so both hold.)

*Proof.* By induction on the gate index, from the first gate to the last. Let gate $g$ with variable $y$ have $+ \in \text{pol}(y)$. Then line L7 added $y \to op(args)$. If $\beta(y) = 0$ the claim holds. Else $op(args)$ is true under $\beta$. Take $op = $ AND. Each argument literal $a_j$ is true under $\beta$. If $a_j = v$ is positive, then $+ \in \text{pol}(v)$ by line L5, and the induction hypothesis gives $1 = \beta(v) \le \text{val}_v(\alpha)$. If $a_j = \neg v$, then $- \in \text{pol}(v)$, and $0 = \beta(v) \ge \text{val}_v(\alpha)$. In both cases the literal $a_j$ is true on $\alpha$ in the circuit, so $\text{val}_g(\alpha) = 1$. For OR, one argument literal is true under $\beta$, and the same step shows that it is true in the circuit. For XOR, both arguments have both signs, so by the induction hypothesis their values under $\beta$ equal their circuit values, and $\beta(y) = 1$ forces $\text{val}_g(\alpha) = 1$. The case $- \in \text{pol}(y)$ is the dual: line L8 added $op(args) \to y$, and if $\beta(y) = 0$ then $op(args)$ is false under $\beta$; each literal that is false under $\beta$ is false in the circuit by the induction hypothesis with the signs exchanged, so $\text{val}_g(\alpha) = 0$. $\square$

**Theorem.** $P$ is satisfiable if and only if the circuit is satisfiable. The restriction of each model of $P$ to the inputs is a satisfying input, and each satisfying input $\alpha$ extends to the model $\alpha \cup \text{val}(\alpha)$ of $P$.

*Proof.* Let $\beta$ be a model of $P$. The unit clause $(o)$ makes $o$ true. If $o = v$ is positive, then $+ \in \text{pol}(v)$, and the lemma gives $\text{val}_v(\alpha) \ge \beta(v) = 1$. If $o = \neg v$, then $- \in \text{pol}(v)$, and $\text{val}_v(\alpha) \le \beta(v) = 0$. In both cases the circuit outputs 1 on $\alpha$. Conversely, let $\alpha$ be a satisfying input. The assignment $\alpha \cup \text{val}(\alpha)$ satisfies every Tseitin clause (see Lemma 2 of the [Tseitin page](/tseitin-transformation/)), and $P$ is a subset of them, so it satisfies $P$. $\blacksquare$

### Size

An AND gate of fan-in $k$ with one polarity gets $k$ clauses with $2k$ literals ($+$) or one clause with $k + 1$ literals ($-$), instead of $k + 1$ clauses with $3k + 1$ literals. OR is the dual. An XOR gate with one polarity gets 2 clauses instead of 4. A gate with both polarities gets all its Tseitin clauses. So the result never has more clauses than the Tseitin CNF, and in a circuit in negation normal form each OR gate gets one clause.

## Classic examples

- **Formulas in negation normal form.** Every subformula has the polarity $+$, so the transformation writes only $y \to op(args)$. This is the original setting of Plaisted and Greenbaum, who translated first-order formulas into clauses this way.
- **Checking validity.** To prove that $\varphi$ is valid, encode $\neg \varphi$. The NOT at the top flips every polarity, so the gates of $\varphi$ that only had $+$ now have only $-$.
- **Bounded model checking and bit-blasting.** Encoders for [SAT-based bounded model checking](/sat-based-bounded-model-checking/) and [bit-blasting](/bit-blasting/) can use polarity to drop clauses. Gates under an XOR, an equivalence or a multiplexer select input have both polarities and keep the full Tseitin definition.

## Variations

- **Polarity of shared gates.** In a circuit (a DAG), compute the polarity as a union over all uses, as in lines L2 to L5. A gate that is used once positively and once negatively keeps both directions.
- **Polarity through other gates.** An equivalence or an XOR has no fixed polarity for its arguments, and the select input of a multiplexer has both. A gate type that is monotone in an argument passes the polarity to it unchanged; one that is antitone flips it.
- **Blocked clause view.** Järvisalo, Biere and Heule showed that [blocked clause elimination](/blocked-clause-elimination/), run to a fixpoint on the full Tseitin CNF, removes every clause that the Plaisted-Greenbaum transformation drops. The order matters: the dropped clauses of the output gate are blocked first, and each removal makes the dropped clauses of the gates below it blocked. So a solver with blocked clause elimination gets the effect of this transformation from a plain Tseitin input.

## Pitfalls

- **Counting models.** The gate variables are not determined by the inputs, so the number of models grows. In the example above it goes from 5 to 6. Do not use this transformation for [model counting](/model-counting/) or for uniform sampling of models; use the full Tseitin transformation.
- **Assumptions on gate variables.** If a later query assumes $\neg y$ for a gate that only has the polarity $+$, the solver can set $y = 0$ even when the gate is true, and the answer is wrong. With [incremental SAT](/incremental-sat/), give such gates both directions.
- **Reading values from a model.** In a model, a gate variable with polarity $+$ only can be 0 when the gate is true. Read the values of the inputs, then evaluate the circuit; do not read gate values from the model.
- **Forgetting the flip under NOT.** A negated argument flips the polarity in line L5. Without the flip, the result can be satisfiable when the circuit is not.

## Exercises

1. Show that unit propagation on the Plaisted-Greenbaum CNF, with all inputs assigned, need not assign all gate variables. Give a circuit with 2 gates where it does not.
2. Take the full Tseitin CNF and remove the dropped clauses gate by gate, from the output down. Prove that each clause is blocked at the moment it is removed. On which literal is it blocked?
3. Give a circuit in which every gate has both polarities, so the result equals the Tseitin CNF.

## References
