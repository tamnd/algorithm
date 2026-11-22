---
tag: VTPNC3
kind: algorithm
slug: parse-tree-query-validation
name: Parse-tree validation of queries
aliases:
- SQLGuard
- SQLCheck
area: security-and-privacy/network-and-web-security
level: advanced
summary: "Parses a query once with placeholders for the inputs and once with the real inputs, and rejects it unless the trees have the same shape and each input stays inside one literal."
model: word-ram
complexity:
  vars: {n: the length of the query with inputs plus the length of the query with placeholders}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: O(n)}
properties: {deterministic: true, online: true, recursive: true}
history:
  year: 2005
  people: [Gregory Buehrer, Bruce W. Weide, Paolo A. G. Sivilotti, Zhendong Su, Gary Wassermann]
  note: "Buehrer, Weide and Sivilotti compared the parse trees of the query with and without the input in 2005. Su and Wassermann gave the general criterion of syntactic confinement in 2006."
prereqs: [sql-injection, context-free-grammar, parse-tree]
see_also: [context-sensitive-auto-escaping, recursive-descent-parsing, abstract-syntax-tree, taint-analysis, lr-parsing, cross-site-scripting]
sources:
  - paper: "Gregory Buehrer, Bruce W. Weide and Paolo A. G. Sivilotti, Using parse tree validation to prevent SQL injection attacks, 5th International Workshop on Software Engineering and Middleware (SEM 2005), pages 106 to 113, doi:10.1145/1108473.1108496"
    locator: "the comparison of the parse tree of the intended query with the parse tree of the query with the input, and the tool SQLGuard"
  - paper: "Zhendong Su and Gary Wassermann, The essence of command injection attacks in web applications, POPL 2006, pages 372 to 382"
    locator: "the definition of a command injection as input that is not syntactically confined, and the checker SQLCheck that parses with an augmented grammar"
  - url: "https://viterbi-web.usc.edu/~halfond/papers/halfond06issse.pdf"
    title: "William G. J. Halfond, Jeremy Viegas and Alessandro Orso, A classification of SQL injection attacks and countermeasures, International Symposium on Secure Software Engineering 2006"
    locator: "the section on prevention techniques, where parse tree validation is compared with the other countermeasures"
---

Parse-tree validation is a run-time check against [SQL injection](/sql-injection/). The program builds a query from static text and inputs. Before the query goes to the database, the validator parses it twice with the [grammar](/context-free-grammar/) of the query language: once with each input replaced by a fixed placeholder, which gives the [parse tree](/parse-tree/) the programmer planned, and once with the real inputs. It accepts the query only when the two trees have the same shape and each input lies inside the literal that holds its placeholder. An input can then change a value but never a keyword, a name, an operator or the nesting of the query. Buehrer, Weide and Sivilotti (2005) gave the method, and Su and Wassermann (2006) gave the general criterion, syntactic confinement. The check is linear in the length of the query. It is a second line of defense: the first is a prepared statement, which sends the inputs apart from the query text.

## In plain words

A program often makes a database query by gluing text together: a fixed part written by the programmer, then a value typed by a user, then more fixed text. The danger is that the value changes what the query means, for example because it holds a quote that ends a string early.

The check asks a simple question: does the query still have the form the programmer meant? To learn that form, it builds the same query with a harmless dummy in place of each value and reads its grammar structure. Then it reads the real query the same way. If the two structures match, and each value sits inside one quoted string or one number, the query goes on. If not, the query is stopped before the database sees it.

## The problem

The input is a query template, static parts $p_0, \ldots, p_k$ from the programmer, and the inputs $x_1, \ldots, x_k$. The query is $q = p_0 x_1 p_1 \cdots x_k p_k$. The intended query $q_0$ is the same text with each $x_i$ replaced by a placeholder, here the one-character number `1`. The task is to accept $q$ exactly when the inputs are syntactically confined: the parse tree of $q$ is the parse tree of $q_0$ with only the text of literals changed, and each input lies inside the literal that holds its placeholder.

The code of this page uses a toy subset of SQL: `SELECT` columns `FROM` a table, an optional `WHERE` condition with `AND`, `OR`, `NOT`, parentheses and the comparisons `=`, `<>`, `<`, `<=`, `>` and `>=`. Literals are numbers and strings in single quotes, with two quotes for a quote inside. A backslash is an ordinary character, as in standard SQL. The validator must know where each input starts and ends; the code keeps an origin for each character, either a static position or the number of an input.

## The algorithm

```pseudo id=main
VALIDATE(p0, ..., pk; x1, ..., xk)
L1  q ← p0 x1 p1 ... xk pk, with the origin of each character
L2  q0 ← the same with each xi replaced by the placeholder
L3  A ← PARSE(q0)
L4  if A fails, or a placeholder is not inside exactly one literal of A then template error
L5  B ← PARSE(q)
L6  if B fails then reject
L7  if SHAPE(A) ≠ SHAPE(B) then reject     ▷ SHAPE erases the text of literals
L8  for each pair of leaves a of A and b of B in the same place do
L9      if the origins of the first and the last characters of a and b differ then reject
L10 accept, with the tree B
```

PARSE builds the concrete parse tree, so each token is a leaf, and SHAPE keeps each node label and the kind and text of each leaf, but writes each literal as a bare "literal". Line L4 checks the template, not the inputs: if the programmer put a hole where a column name goes, no input can be a literal there, and the template is an error. Line L7 checks the structure. Lines L8 and L9 check the boundaries of the tokens: a token that starts or ends on a static character must start or end on the same static character in both queries. This rules out an input whose literal runs over the static text after it.

The template check of lines L2 to L4 depends only on the template, so a real system does it once and caches the tree $A$.

## Example

The template is `SELECT a FROM t WHERE name = '` then $x_1$ then `' AND id = ` then $x_2$. The inputs are $x_1 =$ `O''Brien`, a name with the quote already doubled by the program, and $x_2 =$ `42`. The table shows the tokens of the two queries and the origins of their first and last characters. $s_m$ is static character $m$ and $h_2$ is input 2.

| leaves | token of $q_0$ | token of $q$ | origins in $q_0$ | origins in $q$ | line L9 |
| --- | --- | --- | --- | --- | --- |
| 1 to 7 | `SELECT a FROM t WHERE name =` | the same | $s_0$ to $s_{27}$ | the same | equal |
| 8 | `'1'` | `'O''Brien'` | $s_{29}$, $s_{30}$ | $s_{29}$, $s_{30}$ | equal |
| 9 to 11 | `AND id =` | the same | $s_{32}$ to $s_{39}$ | the same | equal |
| 12 | `1` | `42` | $h_2$, $h_2$ | $h_2$, $h_2$ | equal |

Line L7 finds the same shape, with 12 leaves in both trees, so VALIDATE accepts. Three benign changes show the rejections:

- $x_1 =$ `O'Brien`, with the quote not doubled. The string ends after `O`, the rest of the name is read as a name, and the closing quote opens a string that never ends. Line L6 rejects.
- $x_2 =$ `4 2`. The query has 13 tokens, not 12, and the grammar allows no second number after a comparison, so line L6 rejects. A grammar that allowed it would give a different shape, and line L7 would reject.
- $x_2 =$ `id`. The query parses, but leaf 12 is a column name and not a literal, so the shapes differ at line L7.

An input with blanks around a number, such as ` 42 `, is accepted, and so is a complete string literal in place of the number.

## Correctness

The claim: when the template passes line L4, VALIDATE accepts exactly when $q$ parses, its tree has the shape of the tree of $q_0$, and the $j$-th tokens of the two queries start and end on characters of the same origin. Then each static character is in a token of the same kind and text as in $q_0$, and each non-blank character of $x_i$ is inside the literal that holds the placeholder of $x_i$. The key fact is that origins never decrease along a query and that each static character and each one-character placeholder occurs once, so a token contains a character exactly when the character lies between the origins of the ends of the token. The proof also shows a simpler form of the condition, input by input: an input in a quoted hole is accepted exactly when its runs of quotes have even length, and an input in a number position exactly when it is one literal with blanks around it. The test checks the validator against this form on random benign inputs. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

- **Time.** The lexer reads each character once. The toy grammar is LL(1), so the [recursive descent parser](/recursive-descent-parsing/) reads each token once with no backtracking. Line L4 looks at each character of $q_0$ once, and SHAPE and the loop of line L8 visit each node once. So the time is $\Theta(n)$ on every query, where $n$ counts the characters of $q$ and $q_0$.
- **Space.** The two trees and the origins take $O(n)$ space.
- **For a larger grammar.** With an [LR parser](/lr-parsing/) for an LR(1) grammar the time stays linear in the length of the query. With a general parser such as the [Earley parser](/earley-parser/), it can grow to cubic time for an ambiguous grammar.

## Properties

- **Sound for the grammar.** An accepted query has the planned structure under the grammar of the validator. The guarantee holds for the database only if its parser agrees with this grammar.
- **Complete for confined inputs.** Every input that stays inside its literal is accepted, whatever characters it holds. A name such as `O'Brien` is accepted once its quote is doubled, so the check does not block benign data.
- **No program analysis.** The validator needs only the template and the input boundaries, not the source code of the program.
- **Online.** Each query is checked when it runs, so stored data that comes back into a later query is checked then, if it is marked as an input.

## Variants and improvements

- **Syntactic confinement.** Su and Wassermann allow an input to be a complete subtree of a chosen kind, not only a literal, and check it with a grammar extended by markers around each input. Their checker is called SQLCheck.
- **A model of the intended queries.** Instead of the template at run time, a static analysis of the program can compute the set of queries each call site can build and check each query against that set.
- **Taint tracking.** [Taint analysis](/taint-analysis/) marks the characters that come from inputs, which gives the origins of line L1 without help from the programmer.
- **Other languages.** The same check works for any language with a grammar, for example a shell command, an LDAP filter or an XPath query, and the same idea underlies [context-sensitive auto-escaping](/context-sensitive-auto-escaping/) for HTML, which prevents the change instead of detecting it.

## When to use it

Use prepared statements first: the database receives the query and the values apart, so no value can be parsed as code, and there is nothing to check. Parse-tree validation is useful where the query must be built as text, for example in old code that cannot be changed, or in a proxy in front of the database, and as a second line of defense. It does not help when the programmer puts an input where a name or a keyword goes (line L4 rejects such a template); there, the program must pick the name from an allow list.

## Pitfalls

- **Checking only that the query parses.** Lines L5 and L6 alone accept a query whose input changed its structure into another valid one. Line L7 compares the shapes, and lines L8 and L9 compare the token boundaries; both are needed.
- **No boundary check.** Without lines L8 and L9, a quote at the end of an input can make its literal run over the static text up to the next quote, and the shapes can still agree if a later input supplies the missing tokens. Line L9 rejects, since the literal no longer ends on the static quote of the template.
- **A grammar that differs from the database.** If the database reads a backslash as an escape inside strings and PARSE in lines L3 and L5 does not, the two parsers see different trees. The test of the page shows that, in this dialect, a backslash before a quote does not keep the quote inside the string. PARSE must use the dialect of the database.
- **A placeholder in the wrong place.** A placeholder for a column name or a sort order is not a literal, and line L4 reports a template error. Weakening line L4 to accept a name there lets an input choose any column.

## Implementations

## History

Buehrer, Weide and Sivilotti presented parse tree validation at the SEM workshop in 2005, with a Java tool named SQLGuard that compares the tree of the query with and without the input. Su and Wassermann (POPL 2006) defined a command injection as an input that is not syntactically confined, proved that their checker SQLCheck, based on an augmented grammar, finds exactly these inputs, and measured it on real applications. Halfond, Viegas and Orso (2006) classified the attacks and the countermeasures and placed parse tree validation among the run-time techniques.

## References
