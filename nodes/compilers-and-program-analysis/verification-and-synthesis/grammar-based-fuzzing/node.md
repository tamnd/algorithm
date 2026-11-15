---
tag: 3N2T72
kind: technique
slug: grammar-based-fuzzing
name: Grammar-based fuzzing
aliases:
- generative fuzzing
area: compilers-and-program-analysis/verification-and-synthesis
level: advanced
summary: Generates test inputs from a grammar of the input format, so that most inputs pass the parser and test deeper code.
prereqs: [context-free-grammar]
see_also: [probabilistic-context-free-grammar, coverage-guided-fuzzing, generational-search, equivalence-modulo-inputs, differential-testing, delta-debugging, attribute-grammar, abstract-syntax-tree]
sources:
  - paper: doi:10.1007/BF01932308
    title: Paul Purdom, A sentence generator for testing parsers, BIT 12(3), 1972
    locator: pp. 366 to 375, the generation of a short set of sentences that uses every production
  - paper: doi:10.1145/1993498.1993532
    title: Xuejun Yang, Yang Chen, Eric Eide and John Regehr, Finding and understanding bugs in C compilers, Proceedings of PLDI 2011
    locator: pp. 283 to 294, the design of Csmith and its safety checks against undefined behavior
  - url: "https://www.usenix.org/conference/usenixsecurity12/technical-sessions/presentation/holler"
    title: Christian Holler, Kim Herzig and Andreas Zeller, Fuzzing with code fragments, Proceedings of the 21st USENIX Security Symposium, 2012
    locator: pp. 445 to 458, LangFuzz and the recombination of code fragments from a test suite
  - paper: doi:10.1145/1375581.1375607
    title: Patrice Godefroid, Adam Kiezun and Michael Y. Levin, Grammar-based whitebox fuzzing, Proceedings of PLDI 2008
    locator: pp. 206 to 215, symbolic tokens and the grammar-based constraint solver
  - paper: doi:10.1109/T-C.1973.223746
    title: Taylor L. Booth and Richard A. Thompson, Applying probability measures to abstract languages, IEEE Transactions on Computers C-22(5), 1973
    locator: pp. 442 to 450, the condition under which a probabilistic grammar generates finite sentences with probability 1
---

Grammar-based fuzzing makes test inputs from a grammar of the input format instead of from random bytes. A program that parses its input, such as a compiler, an interpreter or a document reader, rejects almost every random byte string in its first few lines of code. A generator that follows a [context-free grammar](/context-free-grammar/) makes inputs that the parser accepts, so the tests reach the code after the parser, where the deeper bugs are. The grammar replaces the luck that a [coverage-guided fuzzer](/coverage-guided-fuzzing/) needs to produce valid syntax. Like every fuzzer, it gives no completeness guarantee: a grammar can describe infinitely many inputs, and a generator only samples them.

## In plain words

Write down the rules of the input format: an expression is a number, or two expressions joined by plus, or an expression in brackets, and so on. To make a test input, start with "expression" and replace it by one of its rules, chosen at random. Keep replacing every part that is not yet plain text until only text is left. Every input made this way has the right form, so the program under test reads it and goes on to do real work with it. Two things need care. Random choices can make an input grow without end, so after a certain depth always pick the rule that finishes fastest. And the right form is not enough for many programs: a variable must be declared before use, and a C program must not divide by zero. Real generators add such rules by hand.

## When it applies

- The input has a known structure that a parser checks: a programming language, a query language, a markup or document format, a network protocol with nested messages. A grammar often exists already in the documentation or in the source of the parser.
- The bugs of interest are behind the parser: in type checking, optimization, code generation, the interpreter or the layout engine. For bugs in the parser itself, plain mutation of bytes is often better, because invalid input is exactly what tests it.
- There is an oracle for the generated inputs. A crash or a sanitizer report is the simplest one. For compilers, the usual oracle is [differential testing](/differential-testing/) between compilers or optimization levels, or [equivalence modulo inputs](/equivalence-modulo-inputs/).

What can be decided about the grammar is limited. Whether a nonterminal can derive any finite sentence is decidable by the fixed point below, and so is whether the grammar generates anything at all. Whether the grammar describes exactly the inputs that the program accepts is not: equivalence of context-free grammars is undecidable, and the language that a program accepts can be any recursively enumerable language. So the grammar is an approximation, and inputs that the grammar cannot produce are never tested.

## The template

**Step 1: the minimal cost of each nonterminal.** For a grammar with productions $A \to \alpha$, let $\mathrm{cost}(a) = 0$ for a terminal $a$ and compute

$$\mathrm{cost}(A) = \min_{A \to X_1 \cdots X_k} \Big(1 + \sum_{i=1}^{k} \mathrm{cost}(X_i)\Big),$$

the least number of production steps that turn $A$ into terminals. Start with $\mathrm{cost}(A) = \infty$ for every nonterminal and apply the equation to all nonterminals in rounds until nothing changes. After round $r$, every nonterminal that has a cheapest derivation tree of height at most $r$ has its final value. A cheapest tree never repeats a nonterminal on a path from the root, because the lower subtree alone would be cheaper, so as many rounds as there are nonterminals are enough. A nonterminal whose cost stays $\infty$ derives no finite sentence and should be removed.

**Step 2: depth-bounded random expansion.** Expand from the start symbol. Below a depth limit $d$, choose a production at random, uniformly or with weights. At depth $d$ and below, choose a production of least cost, so that every derivation finishes:

```
GEN(X, depth)
  if X is a terminal then return X
  if depth < d then choose a production X -> Y1 ... Yk at random
  else choose a production X -> Y1 ... Yk with the least 1 + cost(Y1) + ... + cost(Yk)
  return GEN(Y1, depth + 1) ... GEN(Yk, depth + 1)
```

Above the limit, the size of an input follows the random choices; past it, every remaining nonterminal finishes in at most its cost of steps. Real tools use an explicit stack instead of recursion, and a size budget in addition to the depth.

**Step 3: constraints the grammar cannot express.** Declarations before use, matching types, values in range and the absence of undefined behavior are not context-free. Add them to the generator: keep an environment of declared names during generation, generate only well-typed expressions, and wrap risky operations in checks. An [attribute grammar](/attribute-grammar/) is one systematic form of this step.

**Step 4: run and check.** Run each input under the oracle, save the failing ones, and reduce them with a grammar-aware [delta debugging](/delta-debugging/) before a person looks at them.

## Classic examples

**Why uniform choice can run forever.** Take $E \to E + E \mid E * E \mid n$, with each production chosen with probability $1/3$ and no depth limit. Each $E$ has, on average, $2 \cdot 2/3 = 4/3$ children that are again $E$, so the expansion is a branching process that grows on average. The probability $q$ that the expansion of one $E$ ever ends satisfies $q = 1/3 + (2/3) q^2$, whose least solution in $[0, 1]$ is $q = 1/2$. So half of all runs of the generator never stop. Booth and Thompson give the general condition for a [probabilistic grammar](/probabilistic-context-free-grammar/) to produce finite sentences with probability 1. With the depth limit of Step 2, every run stops: $\mathrm{cost}(E) = 1$, by $E \to n$, so at the limit every $E$ becomes $n$ at once.

**A short trace.** With the same grammar and $d = 2$: at depth 0, $E$ is replaced by $E * E$ at random. At depth 1 the left $E$ becomes $E + E$ and the right one $n$. At depth 2 the limit applies and both remaining $E$ become $n$. The result is $n + n * n$, read with the tree of the derivation, not with the precedence of the operators. Printing a tree as text needs brackets, or a grammar that encodes precedence, or the input will not mean what the generator meant.

**Purdom's sentence generator (1972).** To test a parser, Purdom generates a small set of short sentences that together use every production of the grammar at least once. It is a coverage criterion for grammars, the counterpart of edge coverage for programs, and it needs the minimal costs of Step 1 to finish each sentence quickly.

**Csmith (2011).** Csmith generates random C programs that avoid undefined and unspecified behavior, by tracking types, pointers and effects during generation and wrapping arithmetic in safe functions. Every program then has one meaning, and different compilers must give the same checksum of the global variables. Yang, Chen, Eide and Regehr report finding more than 325 previously unknown bugs in GCC, LLVM and other compilers with it.

**LangFuzz (2012).** Holler, Herzig and Zeller parse a test suite of JavaScript programs with the grammar, cut the syntax trees into fragments, and build new programs by replacing a fragment of one program with a fragment of the same nonterminal from another. The inputs are valid and close to the kind of code that already found bugs. They report many security bugs in the JavaScript engines of Mozilla and Google.

**Grammar-based whitebox fuzzing (2008).** Godefroid, Kiezun and Levin combine the grammar with [generational search](/generational-search/). The path conditions are over tokens instead of bytes, and a grammar-based solver only returns token sequences that the grammar accepts. On the JavaScript interpreter of Internet Explorer 7, it covered more of the code generation module than byte-level whitebox fuzzing, with fewer tests, because it wasted no runs on inputs that the parser rejects.

## Variations

- **Probabilistic weights.** Learn the weights of the productions from a corpus of real inputs, so that the generated inputs look like real ones, or invert the weights to favor rare constructs.
- **Mutation of syntax trees.** Parse seed inputs and mutate them by replacing, deleting or swapping subtrees of the same nonterminal. LangFuzz does this with fragments from a test suite.
- **Grammar coverage feedback.** Combine generation with the feedback loop of a [coverage-guided fuzzer](/coverage-guided-fuzzing/): keep the trees whose inputs reach new code and mutate them further.
- **Learned grammars.** When no grammar exists, infer an approximate one from sample inputs or from the way the program parses them.
- **Systematic enumeration.** Enumerate all sentences up to a size, smallest first, instead of sampling. It finds the smallest failing input but grows exponentially with the size.

## Pitfalls

- **Unbounded recursion.** Uniform choice in a recursive grammar can produce infinite or huge inputs, as the first example shows. Always use the minimal costs and a depth or size budget.
- **Syntax without semantics.** Inputs that parse but fail type checking or name resolution stop in the first semantic pass and test nothing deeper. Add the constraints of Step 3.
- **Undefined behavior.** For compiler testing, a program with undefined behavior has no correct output, so a difference between compilers is not a bug. Csmith exists largely to avoid this.
- **A grammar that is too strict.** Inputs outside the grammar are never tested, including the invalid inputs that test error handling. Mix generated inputs with byte-level mutation.
- **Bias of the uniform choice.** A production with a large subtree is chosen as often as a short one, so small inputs and deep nesting are both rare. Tune the weights and check the distribution of sizes.
- **No completeness.** A run of any length tests a sample. It never shows that the program handles every input of the grammar.

## Exercises

1. Compute $\mathrm{cost}$ for the grammar $S \to A B \mid c$, $A \to a A \mid a$, $B \to b B$. Which nonterminal derives no finite sentence, and which productions should be removed?
2. For $E \to E + E \mid n$, chosen with probabilities $p$ and $1 - p$, find the probability that the expansion ends, as a function of $p$, and the values of $p$ for which it is below 1.
3. Write GEN with an explicit stack and a budget on the number of terminals instead of a depth limit. Show that it always stops.
4. Design a generator for the toy IR of these pages that never reads a name before it is defined and never divides by a variable. Which of these two rules can a context-free grammar express?
5. Purdom's criterion asks that every production be used at least once. Give a grammar and a set of sentences that meets it but never uses two given productions in the same derivation, and suggest a stronger criterion.

## References
