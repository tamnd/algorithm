---
tag: TR7EXK
kind: definition
slug: newick-format
name: Newick format
aliases:
- New Hampshire format
- Newick tree format
area: biology/phylogenetics
level: intro
summary: The standard text form of a phylogenetic tree, adopted in 1986. Nested parentheses give the subtrees, with optional labels, branch lengths after colons, and a final semicolon.
prereqs: [phylogenetic-tree, context-free-grammar]
see_also: [rooted-and-unrooted-trees, recursive-descent-parsing, ll-grammar, balanced-parentheses, postorder-traversal, tree-comparison, phylogenetic-network]
sources:
  - url: https://phylipweb.github.io/phylip/newicktree.html
    title: Joseph Felsenstein, The Newick tree format, PHYLIP documentation
    locator: the sections on the origin of the standard (26 June 1986), the conventions for names and branch lengths, and the example trees
  - url: https://phylipweb.github.io/phylip/newick_doc.html
    title: Gary Olsen, Interpretation of the Newick's 8:45 tree format standard, 30 August 1990
    locator: the grammar (tree, descendant_list, subtree, labels, branch_length), quoted labels, comments and blanks
---

The Newick format writes a [phylogenetic tree](/phylogenetic-tree/) as a string of nested parentheses: each pair of parentheses holds the subtrees of one inner vertex, separated by commas, and the string ends with a semicolon. A label may follow each vertex, and a branch length may follow a colon. It was adopted in 1986 and is the input and output format of almost every phylogenetics program. Its grammar is [context-free](/context-free-grammar/) and [LL(1)](/ll-grammar/), so a one-pass parser reads it in time linear in the length of the string.

## Definition

The standard was adopted on 26 June 1986 by an informal committee at the meetings of the Society for the Study of Evolution in Durham, New Hampshire: James Archie, William H. E. Day, Joseph Felsenstein, Wayne Maddison, Christopher Meacham, F. James Rohlf and David Swofford. The final session was at Newick's restaurant in Dover, New Hampshire, which gave the format its name. Felsenstein's description of the standard is short, and Gary Olsen wrote a precise grammar for it in 1990. This page follows both.

### Grammar

In the grammar below, square brackets mean "optional" and braces mean "zero or more times".

```
tree        ::= subtree ";"
subtree     ::= "(" subtree { "," subtree } ")" [ label ] [ ":" length ]
              | [ label ] [ ":" length ]
label       ::= unquoted | quoted
length      ::= a real number, for example 5, 0.25 or 1e-3
```

- **Vertices.** A pair of parentheses is an inner vertex, and the subtrees inside it, in order, are its children. The second form of `subtree` is a leaf. The outer `subtree` is the root of the string.
- **Labels.** The label of an inner vertex follows its closing parenthesis. Any label may be empty. An *unquoted* label is a run of printable characters with no blank, parenthesis, square bracket, single quote, colon, semicolon or comma, and each underscore in it stands for a blank. A *quoted* label is written between single quotes and may hold any character; a single quote inside it is written twice.
- **Branch lengths.** A length after a vertex is the length of the edge from that vertex to its parent. A length on the outer subtree has no edge to belong to.
- **Comments and blanks.** Text in square brackets is a comment and may appear wherever a line break may. Blanks and line breaks may appear anywhere except inside an unquoted label or a length.
- **The semicolon.** Each tree ends with `;`. A file may hold many trees, one after another, and the semicolon is what separates them.

The format has no field for "rooted" or "unrooted". By convention, a string whose outer vertex has three or more children, such as `(A,B,(C,D));`, is an unrooted tree drawn from one of its inner vertices, and a string with two outer children is a rooted tree with a root of degree 2 (see [rooted and unrooted trees](/rooted-and-unrooted-trees/)). Many programs ignore the convention and take an option instead.

### One tree, many strings

The string fixes an order of the children at each vertex, but the tree does not have one. A rooted tree whose inner vertices have $k_1, k_2, \ldots$ children has $\prod_i k_i!$ strings without lengths, all for the same tree; `((A,B),(C,D));` is one of $2! \cdot 2! \cdot 2! = 8$. An unrooted tree has still more, one set for each inner vertex chosen as the outer one. So two Newick strings must be parsed before they can be compared: string equality is not tree equality. [Tree comparison](/tree-comparison/) works on the parsed trees, for example on their [splits](/splits-of-a-tree/).

### Parsing and printing

The grammar decides each step from the next token: `(` opens an inner vertex, `,` starts a sibling, `)` closes a vertex, `:` starts a length, `;` ends the tree, and any other character starts a label. So a [recursive-descent parser](/recursive-descent-parsing/) reads it in one pass, in $O(L)$ time and $O(L)$ space for a string of $L$ characters. Real trees can nest deeply: a caterpillar on $10^5$ taxa has parentheses $10^5$ levels deep, which overflows the call stack of a recursive parser in many languages. The parser of this page keeps the open vertices on an explicit [stack](/stack/) instead.

```pseudo id=parse
PARSE-NEWICK(s)
L1  root ← new vertex; cur ← root; open ← empty stack
L2  loop
L3      skip blanks and [comments]; c ← next character
L4      if c = "(" then push cur on open; cur ← new child of cur
L5      else if c = "," then cur ← new child of top(open)        ▷ error if open is empty
L6      else if c = ")" then cur ← pop(open)                      ▷ error if open is empty
L7      else if c = ":" then cur.length ← the number that follows
L8      else if c = ";" then
L9          if open is not empty then error "unbalanced ("
L10         return root
L11     else cur.label ← the quoted or unquoted label that follows
```

The full parser also keeps the state of `cur` (fresh, closed, labeled or with a length), so that it rejects a second label, a second length, or a `(` after a label. The printer is a [preorder](/preorder-traversal/) walk for the opening parentheses and a [postorder](/postorder-traversal/) walk for the closing parentheses, labels and lengths, also with an explicit stack. It quotes a label when the label holds a special character or an underscore, and writes each blank of any other label as an underscore. With these rules, printing a tree and parsing the string gives back the same tree, with the same labels, lengths and child order.

## Examples and non-examples

**Felsenstein's example.** The string `(B:6.0,(A:5.0,C:3.0,E:4.0)Ancestor1:5.0,D:11.0);` is a tree whose outer vertex has three children: the leaf $B$ at length 6, the inner vertex *Ancestor1* at length 5, and the leaf $D$ at length 11. *Ancestor1* has the children $A$, $C$ and $E$ at lengths 5, 3 and 4. Read as an unrooted tree, it has two inner vertices, of degrees 3 and 4.

**A trace.** For `((A,B)x:1,C);` the parser does the following.

| token | action | open stack after |
|---|---|---|
| `(` | push the root; new child $v_1$ | root |
| `(` | push $v_1$; new child $v_2$ | root, $v_1$ |
| `A` | label $v_2$ as A | root, $v_1$ |
| `,` | new child $v_3$ of $v_1$ | root, $v_1$ |
| `B` | label $v_3$ as B | root, $v_1$ |
| `)` | pop: cur is $v_1$ | root |
| `x` | label $v_1$ as x | root |
| `:1` | length of $v_1$ is 1 | root |
| `,` | new child $v_4$ of the root | root |
| `C` | label $v_4$ as C | root |
| `)` | pop: cur is the root | empty |
| `;` | the stack is empty: return the root | empty |

**Quoted labels, underscores and comments.** In `('Homo sapiens':0.1,Pan_troglodytes:0.2,'it''s [x]':3)root;` the three leaf labels are `Homo sapiens`, `Pan troglodytes` and `it's [x]`, and the outer vertex is labeled `root`. The square brackets inside the quotes are part of the label, not a comment. In `( A [a comment] : 1.5 , B:2e-1 ) ;` the blanks and the comment are ignored, and the lengths are 1.5 and 0.2.

**Empty labels.** `(,(,,),);` is a valid tree with five unlabeled leaves. `A;` is a valid tree with one vertex.

**Non-examples.** Each of these strings is rejected.

| string | the error |
|---|---|
| `(A,B)` | no semicolon at the end |
| `((A,B);` | a parenthesis is not closed |
| `(A,B));` | a `)` with no matching `(` |
| `(A:1:2,B);` | two lengths on one vertex |
| `(A B,C);` | a blank inside an unquoted label |
| `(A:x,B);` | the length is not a number |
| `(A,B);C` | text after the semicolon |

## Related definitions

- A [phylogenetic tree](/phylogenetic-tree/) is the object the string encodes, and [rooted and unrooted trees](/rooted-and-unrooted-trees/) explains why the format cannot say which kind it holds.
- The parenthesis structure is a [balanced parentheses](/balanced-parentheses/) sequence with labels, so the language is not regular and needs a [context-free grammar](/context-free-grammar/).
- Inner labels are often used for support values such as [bootstrap](/phylogenetic-bootstrap/) proportions. A support value belongs to an edge, but the format attaches it to a vertex, so a program that reroots the tree must move such labels with care.
- Later formats extend Newick. Some put key-value data inside the comments, and extended Newick encodes [phylogenetic networks](/phylogenetic-network/) by repeating tagged leaves. The NEXUS format wraps Newick trees in a file with blocks for data and translation tables.

## References
