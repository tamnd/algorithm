---
tag: B9NQ94
kind: definition
slug: first-normal-form
name: First normal form (1NF)
aliases:
- 1NF
- first normal form
area: systems/database-algorithms
level: intro
summary: "A relation is in first normal form if each attribute value is atomic: no value is itself a set, a list or a relation. Codd's 1970 normalization removes nested relations."
prereqs: [relational-model]
see_also: [normalization, third-normal-form, boyce-codd-normal-form, relational-algebra, functional-dependency, datalog]
sources:
  - paper: doi:10.1145/362384.362685
    title: E. F. Codd, A relational model of data for large shared data banks, Communications of the ACM 13(6), 377 to 387 (1970)
    locator: Section 1.4 (normal form; the elimination of nonsimple domains, with the employee, job history and children example)
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 3 (the relational model, with atomic values); Chapter 20 (complex values, the nested relational model and its algebra)
  - book: isbn:9780881751888
    title: Jeffrey D. Ullman, Principles of Database and Knowledge-Base Systems, Volume I, Computer Science Press (1988)
    locator: Section 7.6 (normal forms for relation schemes; first normal form)
  - paper: "Gerhard Jaeschke and Hans-Jörg Schek, Remarks on the algebra of non first normal form relations, Proceedings of the 1st ACM SIGACT-SIGMOD Symposium on Principles of Database Systems (PODS 1982), 124 to 138"
    locator: the nest and unnest operators for relations that are not in first normal form
  - book: isbn:9781590597460
    title: C. J. Date, Date on Database, Writings 2000 to 2006, Apress (2006)
    locator: the chapter "What first normal form really means" (the meaning of atomicity)
---

A relation is in first normal form (1NF) if each value in each tuple is atomic: the value is not a set, a list or a relation that the database system takes apart. Codd's 1970 paper made 1NF part of the [relational model](/relational-model/), and showed how to turn a nested structure into flat relations by copying keys down. All higher [normal forms](/normalization/) assume 1NF. What "atomic" means is a matter of the operators of the system, not of the values themselves.

## Definition

Let each attribute $A$ have a domain $\mathrm{dom}(A)$. A domain is *simple* if the query language treats its elements as single values: it compares them, but it does not select, join or count their parts. A relation schema is in *first normal form* if each of its domains is simple. A relation is in 1NF if its schema is.

Codd (1970, Section 1.4) called a domain *nonsimple* if its elements are relations, and called a set of relations *normalized* if all their domains are simple. He gave a procedure to *normalize* a nested relation $R$ with primary key $K$ and a nonsimple attribute $N$ whose values are relations over $V$:

1. Replace $R$ by the projection of $R$ on all attributes except $N$.
2. Add a new relation over $K \cup V$ that holds, for each tuple $t$ of $R$ and each tuple $s$ in $t[N]$, the tuple $t[K] \cup s$.
3. Choose a primary key for the new relation: $K$ together with a key of the inner relation.
4. Repeat while some relation has a nonsimple domain.

In the new schema, each nested tuple becomes a flat tuple that carries the key of its parent.

A 1NF relation in the model has two more properties that come from "a relation is a set of tuples, and a tuple is a function from attributes to values":

- each tuple has exactly one value for each attribute, so there are no repeating groups such as $\mathit{Phone}_1, \mathit{Phone}_2, \mathit{Phone}_3$ with a varying number of used columns;
- the relation holds no tuple twice, and has no order of tuples or of attributes.

Some textbooks add the second point to the definition of 1NF and others put it in the definition of a relation.

## Examples and non-examples

**Non-example: a nested relation.** Codd's paper used an employee record with a job history and a list of children. In a smaller form:

| Emp | Name | Children |
| --- | --- | --- |
| E1 | Ann | {(Bo, 2001), (Cy, 2004)} |
| E2 | Dan | {} |

The domain of $\mathit{Children}$ is a set of relations over $(\mathit{ChildName}, \mathit{Year})$, so it is nonsimple and the relation is not in 1NF.

**Example: the normalized form.** Codd's procedure gives two relations:

| Emp | Name |
| --- | --- |
| E1 | Ann |
| E2 | Dan |

| Emp | ChildName | Year |
| --- | --- | --- |
| E1 | Bo | 2001 |
| E1 | Cy | 2004 |

The key of the second relation is $\{\mathit{Emp}, \mathit{ChildName}\}$. The query "which employees have a child born after 2002" is now a [selection and a join](/relational-algebra/). Dan has no tuple in the second relation, and a [join](/relational-join/) drops him unless the query asks for him with a difference or an outer join.

**Non-example: a repeating group.** A table $\mathrm{Contact}(\mathit{Name}, \mathit{Phone1}, \mathit{Phone2}, \mathit{Phone3})$ is flat, but a person with four phones does not fit, and the query "who has phone 555" must look in three columns. Most texts treat this as a violation of the spirit of 1NF. The fix is the same: a relation $(\mathit{Name}, \mathit{Phone})$.

**Example: a string.** An attribute $\mathit{Name}$ with the value "Ann Lee" is atomic if the system only compares whole names. If queries often ask for the family name, the design should store it in its own attribute. The value is the same; only its use changed.

**Non-example: a comma-separated list.** A value "db,os,ai" in a $\mathit{Courses}$ attribute holds a set inside a string. A query for students who take os must parse the string. This is a common design error, and it is not in 1NF in the sense that matters.

## Related definitions

- **Atomicity is relative.** C. J. Date argues that no value is atomic in itself. A string is a list of characters, a date has a year, and a system with a function to take them apart can query those parts. He concludes that 1NF means only that each tuple has one value of the right type for each attribute, and that a type can be a set or a relation, if the system offers the operators for it. Other authors keep the stricter reading of Codd.
- **Nested relations.** The non-first-normal-form (NF²) model allows relation-valued attributes. Jaeschke and Schek (1982) defined the *nest* and *unnest* operators: unnest is Codd's normalization of one attribute, and nest groups tuples with equal other values into a set. Unnest after nest gives back the relation, but nest after unnest need not. Abiteboul, Hull and Vianu treat complex values and their algebra and calculus in Chapter 20.
- **SQL and JSON.** SQL:1999 added array types, and many systems store JSON documents in a column. These are non-1NF values with their own operators. Queries that look inside them work, but the database system usually cannot index or constrain their parts as well as it can for flat columns.
- **Higher normal forms.** [Second, third](/third-normal-form/) and [Boyce-Codd](/boyce-codd-normal-form/) normal forms are conditions on [functional dependencies](/functional-dependency/) among the attributes of a 1NF schema. Without 1NF, a dependency between atomic attributes is not defined.
- **Datalog and the relational algebra.** Both work on flat relations, so they assume 1NF. [Datalog](/datalog/) with sets or nested relations needs extra operators.

## References
