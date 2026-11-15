---
tag: H27VZ7
kind: problem
slug: programming-by-example
name: Programming by example
aliases:
- PBE
- inductive program synthesis
area: compilers-and-program-analysis/verification-and-synthesis
level: core
summary: Find a program in a domain-specific language that is consistent with a few given input-output examples and generalizes well.
prereqs: [program-synthesis]
see_also: [syntax-guided-synthesis, bottom-up-enumerative-synthesis, version-space-algebra, string-transformation-synthesis, type-directed-synthesis, occams-razor, overfitting, genetic-programming]
sources:
  - paper: doi:10.1145/1926385.1926423
    title: Sumit Gulwani, Automating string processing in spreadsheets using input-output examples, Principles of Programming Languages (POPL 2011)
    locator: pp. 317-330, the FlashFill language, synthesis with version space algebras, ranking, and the interaction with the user
  - paper: doi:10.1145/2814270.2814310
    title: Oleksandr Polozov and Sumit Gulwani, FlashMeta, a framework for inductive program synthesis, Object-Oriented Programming, Systems, Languages and Applications (OOPSLA 2015)
    locator: pp. 107-126, top-down synthesis with witness functions that split the examples of an operator into examples for its arguments
  - paper: doi:10.1023/A:1025671410623
    title: Tessa Lau, Steven A. Wolfman, Pedro Domingos and Daniel S. Weld, Programming by demonstration using version space algebra, Machine Learning 53(1-2), 2003
    locator: pp. 111-156, programming by demonstration in a text editor (SMARTedit), with version spaces composed by union and join
  - paper: doi:10.1145/321992.322002
    title: Phillip D. Summers, A methodology for LISP program construction from examples, Journal of the ACM 24(1), 1977
    locator: pp. 161-175, recursive LISP programs built from a few input-output examples by finding recurrences in traces
  - paper: doi:10.1007/978-3-319-21690-4_23
    title: Rishabh Singh and Sumit Gulwani, Predicting a correct program in programming by example, Computer Aided Verification (CAV 2015)
    locator: pp. 398-414, a ranking function learned from data to pick the intended program among those consistent with the examples
  - paper: doi:10.1561/2500000010
    title: Sumit Gulwani, Oleksandr Polozov and Rishabh Singh, Program Synthesis, Foundations and Trends in Programming Languages 4(1-2), 2017
    locator: chapter 7 (programming by examples, including ranking and interaction) and chapter 4 (enumerative search)
  - paper: doi:10.1145/2737924.2737977
    title: John K. Feser, Swarat Chaudhuri and Isil Dillig, Synthesizing data structure transformations from input-output examples, Programming Language Design and Implementation (PLDI 2015)
    locator: pp. 229-239, the lambda-squared tool, which combines deduction over higher-order combinators with enumeration of small terms
  - paper: doi:10.1007/978-3-642-39799-8_67
    title: Aws Albarghouthi, Sumit Gulwani and Zachary Kincaid, Recursive program synthesis, Computer Aided Verification (CAV 2013)
    locator: pp. 934-950, the Escher tool, which synthesizes recursive programs from examples by bottom-up search with goal graphs
---

Programming by example (PBE) is [program synthesis](/program-synthesis/) where the specification is a short list of inputs together with the wanted outputs. The user does not write a formula, so the method suits people who do not program. The hard part is not to find a program that fits the examples, but to find the one that the user means. This page states the problem, why it is underspecified, what is decidable, and the main families of methods. The algorithms have their own pages: [bottom-up enumerative synthesis](/bottom-up-enumerative-synthesis/), [version space algebras](/version-space-algebra/), [string transformation synthesis](/string-transformation-synthesis/) and [type-directed synthesis](/type-directed-synthesis/).

## In plain words

You show the tool a few cases. For example, "Alan Turing" becomes "A. Turing". The tool must find a small program that does the same to every row in the column.

Many programs agree with one or two examples. One program takes the first letter, adds a dot and a space, and copies the last name. Another program always writes the text "A. " and then copies the last name. Both give the right answer on the example, but only the first one is right on "Grace Hopper".

So a tool needs two things. It needs a fast way to find the programs that fit the examples, and it needs a rule to choose among them. Good tools prefer short and general programs, show the result on the other rows, and ask the user about rows where the candidates disagree.

## Definition

**Input.**

- A *domain-specific language* $L$: a grammar of programs and a semantics $[\![P]\!] : I \rightharpoonup O$.
- A finite list of *examples* $E = ((x_1, y_1), \ldots, (x_k, y_k))$ with $x_i \in I$ and $y_i \in O$.
- A *ranking function* $r : L \to \mathbb{R}$, for example minus the size of the program.

**Output.** A program $P \in L$ that is *consistent* with $E$, that is $[\![P]\!](x_i) = y_i$ for $1 \le i \le k$, with the highest rank among the consistent programs. If no program of $L$ is consistent, the answer is "none".

The set of all consistent programs is the *version space* of $E$ in $L$:
$$V(E) = \{ P \in L : [\![P]\!](x_i) = y_i \text{ for } 1 \le i \le k \}.$$
Adding an example can only make the version space smaller: $V(E \cup \{e\}) = V(E) \cap V(\{e\})$. [Version space algebras](/version-space-algebra/) store $V(E)$ in a compact form and compute this intersection.

The definition asks for consistency, but the real goal is *generalization*: the program should also give the intended output on inputs that the user did not show. Generalization cannot be checked from the examples alone. This is the same issue as [overfitting](/overfitting/) in machine learning.

## Variants

- **Input-output examples.** The basic form above.
- **Programming by demonstration.** The user shows the steps, not only the result, for example the edits in a text editor. Each step is an example for one part of the program (Lau, Wolfman, Domingos and Weld 2003).
- **Interactive PBE.** The tool finds an input on which two consistent programs disagree, a *distinguishing input*, and asks the user for the right output.
- **Negative examples.** Some pairs $(x, y)$ say that the output on $x$ must not be $y$.
- **Recursive programs from examples.** Summers (1977) built recursive LISP functions from examples. Escher (Albarghouthi, Gulwani and Kincaid 2013) and Myth (Osera and Zdancewic 2015) need examples for the recursive calls as well, so that a call can be evaluated from the example table.
- **Noisy examples.** Some examples may be wrong, and the goal is a program that fits most of them.
- **The PBE track of SyGuS.** A [syntax-guided synthesis](/syntax-guided-synthesis/) problem whose specification is a conjunction of examples.

## Examples

**Strings.** Take a language with constant strings, substrings between positions, and concatenation (see [string transformation synthesis](/string-transformation-synthesis/)). From the one example "Alan Turing" $\mapsto$ "A. Turing", three consistent programs are:

| program | on "Grace Hopper" |
|---|---|
| first letter, then ". ", then the text after the space | "G. Hopper" |
| the constant "A. ", then the text after the space | "A. Hopper" |
| the constant "A. Turing" | "A. Turing" |

A rank that counts constant strings as expensive picks the first program. A second example, "Grace Hopper" $\mapsto$ "G. Hopper", removes the other two from the version space.

**Integers.** Over the grammar of the [program synthesis](/program-synthesis/) page, with $x$, $y$, $0$, $1$, $+$, $-$, $\times$ and ite on $\le$, a script that enumerates programs by size gives these results:

| examples | smallest consistent programs |
|---|---|
| $(1, 2) \mapsto 2$, $(3, 1) \mapsto 3$ | $x \times y$ and $y \times x$, size 3 |
| add $(2, 2) \mapsto 2$ | four programs of size 6: $\mathrm{ite}(x \le y, y, x)$, $\mathrm{ite}(y \le x, x, y)$, $\mathrm{ite}(x \le 1, y, x)$, $\mathrm{ite}(y \le 1, x, y)$ |
| add $(3, 5) \mapsto 5$ and $(5, 3) \mapsto 5$ | only the two programs for the maximum |

The input $(2, 2)$ is a distinguishing input for $x \times y$ and the maximum. An interactive tool would ask the user for it.

## Known algorithms

| method | idea | notes |
|---|---|---|
| [bottom-up enumeration](/bottom-up-enumerative-synthesis/) with observational equivalence | build programs by size, keep one per vector of outputs on the example inputs | finds a smallest program; cost exponential in its size |
| top-down deduction with [version space algebras](/version-space-algebra/) | invert each operator: from the output of a node, compute the outputs its arguments must have | FlashFill (Gulwani 2011), FlashMeta witness functions (Polozov and Gulwani 2015); returns all consistent programs at once |
| [string transformation synthesis](/string-transformation-synthesis/) | a graph over output positions, with all atoms that produce each piece | the FlashFill algorithm |
| [type-directed synthesis](/type-directed-synthesis/) | refine the examples through pattern matching and recursion on well-typed terms | Myth (Osera and Zdancewic 2015) |
| deduction with combinators | split list examples over map, filter and fold, and enumerate the small bodies | lambda-squared (Feser, Chaudhuri and Dillig 2015) |
| recursive synthesis with goal graphs | bottom-up search, with a conditional that joins programs correct on parts of the examples | Escher (Albarghouthi, Gulwani and Kincaid 2013) |
| constraint solving | encode a bounded program and the examples as one formula | [program sketching](/program-sketching/) |
| stochastic search | mutate programs, with a fitness that counts correct examples | [genetic programming](/genetic-programming/) |

**Ranking.** The usual rule is [Occam's razor](/occams-razor/): prefer the shortest program, or prefer programs with few constants. Singh and Gulwani (2015) learn the ranking function from a set of tasks with known intended programs.

## Bounds

**Theorem 1 (a rich language makes consistency trivial).** If $L$ has equality tests on inputs, conditionals and a constant for each output, and the example inputs are distinct, then a consistent program always exists: the table "if $x = x_1$ then $y_1$ else if $x = x_2$ then $y_2$ ..." of size $O(k)$ times the size of the constants.

So for a general-purpose language, the question is never whether a program exists, but which one generalizes. This is why PBE uses small domain-specific languages and ranking.

**Theorem 2 (undecidable for grammars).** Consistency with a single example is undecidable for languages given by a context-free grammar, even when every program terminates.

*Proof.* Reduce Hilbert's tenth problem over the natural numbers ([Hilbert's tenth problem](/hilberts-tenth-problem/)). Given a polynomial $p(n_1, \ldots, n_k)$ with integer coefficients, take the grammar
$$S \to \texttt{let } n_1 = N \texttt{ in } \ldots \texttt{ let } n_k = N \texttt{ in } p(n_1, \ldots, n_k), \qquad N \to 0 \mid N + 1,$$
where $p(n_1, \ldots, n_k)$ is the fixed text of the polynomial. Each program picks numerals $m_1, \ldots, m_k$, ignores its input, terminates, and outputs $p(m_1, \ldots, m_k)$. Every tuple of natural numbers arises. With the one example $0 \mapsto 0$, a consistent program exists if and only if $p$ has a root in $\mathbb{N}^k$. $\square$

**Theorem 3 (decidable cases).** If every program of $L$ terminates on the example inputs, the set of consistent programs is recursively enumerable, and enumeration by size finds a smallest consistent program when one exists. If $L$ is finite, or if only programs up to a size bound are allowed, the problem is decidable.

*Proof.* Each check runs a program on $k$ inputs and terminates. Enumerate the programs by size and check each one. With a finite space the enumeration ends. $\square$

**Cost.** The number of programs grows exponentially with the size. In the integer grammar above there are 1460 programs of size at most 6 and 2,247,860 of size at most 10. Observational equivalence and version space algebras reduce the work, but the worst case stays exponential in the size of the answer.

## Reductions

- **PBE to syntax-guided synthesis.** The examples form a formula $\bigwedge_i f(x_i) = y_i$; see [syntax-guided synthesis](/syntax-guided-synthesis/).
- **PBE to version space intersection.** Build $V(\{e_i\})$ for each example and intersect them.
- **Hilbert's tenth problem to PBE.** As in Theorem 2.
- **Concept learning to PBE.** A boolean program learned from labelled examples is a classifier, and the version space is Mitchell's version space of consistent hypotheses (see [version space algebra](/version-space-algebra/)).

## Applications

- FlashFill in Microsoft Excel (2013) completes a column of strings from examples.
- Text editors that repeat an edit shown once (SMARTedit, Lau et al. 2003).
- Data wrangling: extract fields from logs or web pages, and reshape tables, from a few marked examples.
- Teaching tools that build small recursive functions on lists from examples.
- Spreadsheet and shell commands that the user describes by the result they want.

## References
