---
tag: ACTP73
kind: technique
slug: hash-consing
name: Hash consing
aliases:
- Hash-consing
- interning
- maximal sharing
- unique table
area: data-structures/hashing
level: advanced
summary: Store each structurally distinct value once in a hash table so that equality becomes pointer comparison.
prereqs: [hash-table, hash-function, dictionary]
see_also: [binary-decision-diagram, expression-dag, memoization, term-graph-rewriting, congruence-closure, weak-reference, abstract-syntax-tree, dedup]
sources:
  - paper: doi:10.1145/1159876.1159880
    title: Jean-Christophe Filliâtre and Sylvain Conchon, Type-safe modular hash-consing, Proceedings of the 2006 ACM SIGPLAN Workshop on ML
    locator: pp. 12 to 19 (the hash-consing module, its weak hash table and the use of unique tags)
  - paper: doi:10.1145/123186.123222
    title: Karl S. Brace, Richard L. Rudell and Randal E. Bryant, Efficient implementation of a BDD package, Proceedings of the 27th ACM/IEEE Design Automation Conference (DAC 1990)
    locator: pp. 40 to 45 (the unique table and the computed table)
  - paper: doi:10.1109/TC.1986.1676819
    title: Randal E. Bryant, Graph-based algorithms for Boolean function manipulation, IEEE Transactions on Computers C-35(8), 1986
    locator: pp. 677 to 691 (reduced ordered BDDs as canonical forms, so that two functions are equal exactly when their graphs are the same)
  - paper: doi:10.1145/368892.368907
    title: A. P. Ershov, On programming of arithmetic operations, Communications of the ACM 1(8), 1958
    locator: pp. 3 to 6
---

Hash consing is the technique of building immutable tree-shaped values through a [hash table](/hash-table/), called the unique table, so that each structurally distinct value exists only once in memory. Before it makes a new node, the constructor looks up the node's label and the identities of its children in the table, and returns the existing node if there is one. Then two values are structurally equal exactly when they are the same pointer, so equality takes $O(1)$ time instead of time linear in the size, and equal subterms share memory. It is the base of the unique table of [binary decision diagrams](/binary-decision-diagram/), of string interning, and of the term tables of theorem provers and compilers.

## In plain words

Think of a program that builds many formulas, such as "x plus y" and "(x plus y) times (x plus y)". Without care, it makes a new copy of "x plus y" each time it needs one. Then the program must compare formulas symbol by symbol to know if they are the same.

Hash consing keeps a table of all the pieces that it has built. When the program asks for "x plus y", the table is checked first. If that piece already exists, the program gets the old piece back, not a new copy. So each different piece is stored once, and two formulas are the same exactly when they are the same object in memory. A test of sameness is then one look, whatever the size of the formulas.

## When it applies

- The values are **immutable trees or DAGs**: terms, formulas, types, expressions, decision diagrams, strings.
- The program builds **many values that share large parts**, so sharing saves memory, often by a large factor.
- The program **tests equality often**, or uses values as keys of a table, for example in [memoization](/memoization/) or in a cache of results. With hash consing, the key can be the unique number of the node.
- A **canonical form** exists and the program needs one copy of each, as in reduced ordered BDDs, where equal Boolean functions must have the same graph.

It does not apply to mutable values: a change to a shared node would change each value that contains it, and it would leave the node in the wrong slot of the table.

## The template

```pseudo id=main
HASHCONS(c, a_1, …, a_k)               ▷ c: constructor label; a_1 … a_k: children, already hash-consed
L1  key ← (c, a_1.id, …, a_k.id)       ▷ hole: the shallow key, with atoms by value
L2  if key is in the unique table U then
L3      return U[key]                  ▷ the node exists: share it
L4  x ← a new node with label c and children a_1, …, a_k
L5  x.id ← the next unused number; x.hash ← H(key)   ▷ hole: the hash function H
L6  U[key] ← x
L7  return x

EQUAL(x, y)
L8  return x.id = y.id                 ▷ pointer equality
```

The program never calls a raw constructor. It calls HASHCONS for each node, bottom up, so the children are already in the table. Line L1 builds a **shallow** key: the label and the identities of the children, not the children's contents. So the key has $k + 1$ fields, and lines L1 to L6 take $O(k)$ expected time with a good hash function $H$, not time in the size of the whole value. Lines L2 and L3 return the existing node when one has the same label and the same children. Lines L4 to L6 make and record a new node. The hash value is stored in the node, so a parent can use it at once.

**Invariant.** For each two nodes $x$ and $y$ that HASHCONS returns, $x$ and $y$ are structurally equal (the same label, and children that are structurally equal in order) exactly when $x = y$. The proof is by induction on the height. For leaves, the key is the label and the atom, and the table keeps at most one node for each key. For a node of height $h + 1$, its children have height at most $h$, so by the hypothesis they are structurally equal exactly when they are the same nodes, which is exactly when their ids are equal. So two nodes of height $h + 1$ are structurally equal exactly when they have the same key, and line L2 returns the one node of that key. This invariant is what makes line L8 correct.

**Example.** Build $(x + y) \cdot (x + y)$. The calls make the leaves $x$ and $y$, then the node $p = {+}(x, y)$. The second call for ${+}(x, y)$ finds the key $({+}, x.id, y.id)$ in the table and returns $p$ itself. The product is ${\cdot}(p, p)$. The table holds 4 nodes, where a tree would have 7. In the same way, the complete binary tree of height 10 built by $t_{i+1} = \text{node}(t_i, t_i)$ has $2^{11} - 1 = 2047$ nodes as a tree, but only 11 distinct nodes, so hash consing stores it in 11 nodes.

## Classic examples

- **String interning.** Each distinct string is stored once, so names can be compared by pointer. Lisp symbols work in this way, Java has `String.intern`, and Python has `sys.intern`. A string is a value with no children, so the key is the string itself.
- **Common subexpressions.** A compiler that builds an [expression DAG](/expression-dag/) with a table of the pairs (operator, operands) finds each repeated subexpression and computes it once. Ershov's 1958 paper on the programming of arithmetic operations already used a hash table to find the repeated subexpressions of a formula.
- **Binary decision diagrams.** The unique table of a BDD package maps (variable, low child, high child) to the node, and makes each reduced ordered [binary decision diagram](/ordered-binary-decision-diagram/) unique. Brace, Rudell and Bryant describe this table, together with a computed table that memoizes the results of operations by the ids of their arguments.
- **Memoization on terms.** A function on hash-consed terms can [memoize](/memoization/) its results in a table keyed by the node id. The key is one integer, and the shared subterms are visited once, which turns a pass over a tree with much sharing into a pass over the DAG.
- **Theorem provers and SMT solvers.** Terms are hash-consed so that [congruence closure](/congruence-closure/) and [term graph rewriting](/term-graph-rewriting/) can test equality of terms and index them in $O(1)$ time.

## Variations

- **Weak unique table.** A table with strong references keeps each node alive forever. Filliâtre and Conchon use a weak hash table, whose entries do not keep their nodes alive, so the garbage collector can free the nodes that the program no longer uses. See [weak reference](/weak-reference/).
- **Unique tags.** Each node gets a distinct integer when it is made (line L5). The tag gives a cheap total order, a hash value for maps and sets of nodes, and keys for memo tables.
- **One table for each type.** Separate tables for terms, types and formulas keep the keys simple and the tables small.
- **Complement edges in BDDs.** An extra bit on each edge means "negate the function below". Then a function and its negation share one node, which can cut the number of nodes by up to a factor of two.
- **Lazy hash consing.** Build values in the normal way, and hash-cons them only when they are stored for a long time or compared often.

## Pitfalls

- **A deep key.** If line L1 hashes the whole contents of the children instead of their ids, each constructor costs time in the size of the value, and building a value of size $s$ costs $\Theta(s^2)$ in the worst case. Use the ids of the children, which are already unique.
- **A raw constructor.** One node made without HASHCONS breaks the invariant: it can be structurally equal to a node of the table and still have a different id, so line L8 gives a wrong answer. Hide the raw constructor behind the module interface, as Filliâtre and Conchon do with a private type.
- **A mutable node.** A change to a node changes each value that shares it, and the key in the table no longer matches the node. Make the nodes immutable.
- **A memory leak.** A unique table with strong references grows without bound in a long run. Use a weak table, or clear the table at known points and rebuild.
- **Ids from memory addresses.** An id taken from the address of a node changes if a garbage collector moves the node. Use a counter, as in line L5.
- **Several threads.** Two threads that build the same node at the same time can both miss in line L2 and make two copies. The unique table needs a lock or a concurrent table with an atomic insert-if-absent.

## Exercises

1. Prove that, with hash consing, the number of nodes for the complete binary tree of height $h$ built by $t_{i+1} = \text{node}(t_i, t_i)$ is $h + 1$, and that building it takes $O(h)$ expected time.
2. Show that EQUAL is wrong if line L1 uses the hash values of the children instead of their ids, by giving two different trees whose children have the same hash values under some $H$.

## References
