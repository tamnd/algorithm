---
tag: PZF5GR
kind: theorem
slug: arden-lemma
name: Arden's lemma
aliases:
- Arden's rule
area: automata-and-parsing/regular-expressions
level: advanced
summary: The unique solution of X = AX + B when epsilon is not in A is X = A*B.
prereqs: [kleene-star, regular-language]
see_also: [dfa-to-regex-conversion, state-elimination, kleene-algebra, kleene-theorem, brzozowski-derivatives, regex-equivalence, gaussian-elimination]
sources:
  - paper: doi:10.1109/FOCS.1961.13
    title: Dean N. Arden, Delayed-logic and finite-state machines, Proceedings of the 2nd Annual Symposium on Switching Circuit Theory and Logical Design (SWCT 1961)
    locator: pp. 133 to 151
  - paper: doi:10.1145/321312.321326
    title: Arto Salomaa, Two complete axiom systems for the algebra of regular events, Journal of the ACM 13(1) (1966)
    locator: pp. 158 to 169 (the rule that X = XA + B with A free of the empty word gives X = BA*, used as an inference rule of a complete axiom system)
  - paper: doi:10.1145/321239.321249
    title: Janusz A. Brzozowski, Derivatives of regular expressions, Journal of the ACM 11(4) (1964)
    locator: pp. 481 to 494 (the decomposition of an expression by its derivatives)
---

Arden's lemma says that, for languages $A$ and $B$, the language $A^*B$ is the smallest solution of the equation $X = AX \cup B$, and the only one when the empty string is not in $A$. It is the tool that solves the linear equations of a finite automaton, one unknown per state, and so turns the automaton into a [regular expression](/regular-expression/) ([DFA to regex conversion](/dfa-to-regex-conversion/)). In [Kleene algebra](/kleene-algebra/) the same fact, as an inequality, is the axiom that defines the [star](/kleene-star/).

## Statement

**Notation.** This site writes regular expressions with $r \mid s$ for union, $rs$ for concatenation, $r^*$ for the star, $\varepsilon$ for the empty string and $\emptyset$ for the empty language. Star binds tightest, then concatenation, then union. For languages, $\cup$ is union and $AB = \{uv : u \in A, v \in B\}$.

**Theorem (Arden, 1961).** Let $A, B \subseteq \Sigma^*$ and consider the equation
$$X = AX \cup B \qquad (X \subseteq \Sigma^*).$$

1. $X = A^*B$ is a solution.
2. Every solution $X$ contains $A^*B$; so $A^*B$ is the least solution.
3. If $\varepsilon \notin A$, then $A^*B$ is the only solution.

The mirror form holds too: $BA^*$ is the least solution of $X = XA \cup B$, and the only one when $\varepsilon \notin A$.

When $\varepsilon \in A$, the solutions are exactly the languages $A^*D$ with $D \supseteq B$.

## In plain words

The equation describes a set of words $X$ by one rule: a word of $X$ is either a word of $B$, or a word of $A$ followed by a word of $X$. Unfold the rule: a word of $X$ is some words of $A$, one after another, and then a word of $B$. That is exactly $A^*B$.

The unfolding stops because each step uses up a word of $A$. If $A$ contains the empty word, a step can use up nothing, the rule can be applied forever without reading anything, and the equation no longer fixes $X$. Then $A^*B$ is still the smallest answer, but larger ones also work.

## Proof

**1. $A^*B$ is a solution.** Since $A^* = \{\varepsilon\} \cup AA^*$,
$$A(A^*B) \cup B = (AA^*)B \cup \{\varepsilon\}B = (AA^* \cup \{\varepsilon\})B = A^*B.$$

**2. Every solution contains $A^*B$.** Let $X = AX \cup B$. We show $A^nB \subseteq X$ for all $n \ge 0$ by induction on $n$. For $n = 0$, $A^0B = B \subseteq X$. If $A^nB \subseteq X$, then $A^{n+1}B = A(A^nB) \subseteq AX \subseteq X$. Hence $A^*B = \bigcup_{n \ge 0} A^nB \subseteq X$.

**3. Uniqueness when $\varepsilon \notin A$.** Let $X = AX \cup B$ and suppose that $X \not\subseteq A^*B$. Choose a word $w \in X \setminus A^*B$ of minimum length. Since $w \notin A^*B \supseteq B$, the word $w$ is in $AX$, so $w = uv$ with $u \in A$ and $v \in X$. Since $\varepsilon \notin A$, $|u| \ge 1$ and $|v| < |w|$. By the choice of $w$, $v \in A^*B$, and then $w = uv \in A A^*B \subseteq A^*B$, a contradiction. So $X \subseteq A^*B$, and with part 2, $X = A^*B$.

**The mirror form** follows from the same three steps with concatenation on the other side, or by applying the theorem to the reversed languages.

**The case $\varepsilon \in A$.** If $X$ is a solution, then $X \supseteq B$ and $AX \subseteq X$, so $A^*X \subseteq X$; since $\varepsilon \in A^*$, also $X \subseteq A^*X$, so $X = A^*X$ has the form $A^*D$ with $D = X \supseteq B$. Conversely, let $X = A^*D$ with $D \supseteq B$. Then $AX = AA^*D \subseteq A^*D = X$ and $B \subseteq D \subseteq X$, so $AX \cup B \subseteq X$; and $X = A^*D \subseteq AA^*D = AX$ because $\varepsilon \in A$ gives $A^* \subseteq AA^*$. So $X = AX \cup B$. $\blacksquare$

## Consequences

**Solving the equations of an automaton.** Let $A = (Q, \Sigma, \delta, q_0, F)$ be a DFA and let $X_q$ be the set of words that lead from $q$ to an accepting state. Then for each state $q$,
$$X_q = \bigcup_{a \in \Sigma} \{a\} X_{\delta(q, a)} \cup E_q, \qquad E_q = \{\varepsilon\} \text{ if } q \in F, \text{ else } \emptyset.$$
Every coefficient is a set of letters, so it does not contain $\varepsilon$, and Arden's lemma applies at each step. Eliminate the unknowns one by one, as in [Gaussian elimination](/gaussian-elimination/): write the equation of $X_q$ as $X_q = A X_q \cup B$, where $B$ uses only the other unknowns, replace it by $X_q = A^*B$, and substitute. The answer is $X_{q_0} = L(A)$. This is one of the standard methods of [DFA to regex conversion](/dfa-to-regex-conversion/), and it is equivalent to [state elimination](/state-elimination/).

*Example.* For the DFA over $\{a, b\}$ that accepts the words with an even number of $a$, with states 0 (start, accepting) and 1:
$$X_0 = bX_0 \cup aX_1 \cup \{\varepsilon\}, \qquad X_1 = aX_0 \cup bX_1.$$
Arden's lemma on the second equation gives $X_1 = b^*aX_0$. Substituting, $X_0 = (b \cup ab^*a)X_0 \cup \{\varepsilon\}$, and Arden's lemma again gives $X_0 = (b \mid ab^*a)^*$.

**The star as a least fixed point.** With $B = \{\varepsilon\}$, part 2 says that $A^*$ is the least language $X$ with $\{\varepsilon\} \cup AX \subseteq X$. [Kleene algebra](/kleene-algebra/) takes this as an axiom: $b + ax \le x$ implies $a^*b \le x$.

**A complete proof system.** Salomaa (1966) gave a complete axiom system for the equality of regular expressions that uses Arden's lemma as its only rule of inference besides substitution: from $X = XA \cup B$, with $\varepsilon \notin L(A)$, infer $X = BA^*$. The side condition is a property of the expression $A$ that can be checked by syntax.

**Equations from derivatives.** Brzozowski (1964) writes each expression $r$ as $r = \bigcup_{a \in \Sigma} a\, \partial_a r \cup \nu(r)$, where $\partial_a r$ is the [derivative](/brzozowski-derivatives/) and $\nu(r)$ is $\varepsilon$ or $\emptyset$. The equations among the derivatives of $r$ form a finite system of this kind, and Arden's lemma solves it.

**Proving language identities.** To show $L = M$, show that both satisfy the same equation $X = AX \cup B$ with $\varepsilon \notin A$. For example, $(ab)^*a$ and $a(ba)^*$ both satisfy $X = \{ab\} X \cup \{a\}$: the first by part 1, and the second because $\{ab\}\{a\}(ba)^* \cup \{a\} = \{a\}(\{ba\}(ba)^* \cup \{\varepsilon\}) = a(ba)^*$. So they are equal.

## Tightness

- **The condition $\varepsilon \notin A$ is needed.** With $A = \{\varepsilon, a\}$ and $B = \{b\}$, both $A^*B = a^*b$ and $\Sigma^*$ over $\{a, b\}$ are solutions. With $A = \{\varepsilon\}$ and $B = \emptyset$, every language is a solution, since the equation reads $X = X$. In both cases the least solution is still $A^*B$, as part 2 says.
- **Least, not greatest.** When $\varepsilon \in A$, $\Sigma^*$ is always a solution, since $A\Sigma^* \supseteq \Sigma^*$, so the greatest solution carries no information; only the least one is $A^*B$.
- **Infinite systems.** The elimination method needs finitely many unknowns. The infinite system $X_0 = aX_1 \cup \{\varepsilon\}$ and $X_n = aX_{n+1} \cup bX_{n-1}$ for $n \ge 1$ has as the least value of $X_0$ the balanced words, with $a$ as an opening and $b$ as a closing bracket, which are not a regular language. Arden's lemma applies to each equation, but the elimination never ends.

## History

Arden (1961) stated the lemma in a paper on delayed logic and finite-state machines, where the equations describe the behaviour of the states of a machine. Brzozowski (1964) used systems of such equations with derivatives, and Salomaa (1966) used the rule as the inference rule of one of his two complete axiom systems for regular expressions. The same least-fixed-point property became one of the star axioms of Kleene algebra.

## References
