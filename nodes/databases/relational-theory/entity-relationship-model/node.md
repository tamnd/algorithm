---
tag: RN0VS0
kind: model
slug: entity-relationship-model
name: Entity-relationship model
aliases:
- ER model
- entity-relationship diagram
- Chen's ER model
area: databases/relational-theory
level: intro
summary: "Chen's conceptual model of entities, attributes and relationships with cardinality constraints, and its mapping to relation schemas."
prereqs: [relational-model, candidate-key]
see_also: [normalization, join-dependency, inclusion-dependency, functional-dependency, multivalued-dependency, first-normal-form, fourth-normal-form, boyce-codd-normal-form]
sources:
  - paper: doi:10.1145/320434.320440
    title: Peter Pin-Shan Chen, The entity-relationship model, toward a unified view of data, ACM Transactions on Database Systems 1(1), 9 to 36 (1976)
    locator: entity sets, relationship sets, roles and attributes, the ER diagram, and the derivation of relations from the model
  - book: isbn:9780072465631
    title: Raghu Ramakrishnan and Johannes Gehrke, Database Management Systems, third edition, McGraw-Hill (2003)
    locator: Chapter 2 (the ER model, key and participation constraints, weak entities, class hierarchies) and Section 3.5 (from ER diagrams to relational tables)
  - book: isbn:9780078022159
    title: Abraham Silberschatz, Henry F. Korth and S. Sudarshan, Database System Concepts, seventh edition, McGraw-Hill (2020)
    locator: Chapter 6 (database design using the E-R model), including Section 6.7 on reducing E-R diagrams to relational schemas
  - paper: "Maurizio Lenzerini and Paolo Nobili, On the satisfiability of dependency constraints in entity-relationship schemata, Information Systems 15(4), 453 to 461 (1990)"
    locator: the satisfiability of cardinality constraints in ER schemas and the case of finite instances
---

The entity-relationship (ER) model of Chen (1976) describes a database at the conceptual level, as sets of entities, sets of relationships among them, attributes, and constraints on how many relationships an entity may take part in. A design in the ER model is then mapped to relation schemas of the [relational model](/relational-model/), with keys and foreign keys. The relational model and [normalization](/normalization/) work on the result of this mapping. This page defines the parts of the model, its instances, the standard mapping, and two facts about what the model can and cannot express.

## The machine

**Entity sets.** An *entity set* $E$ is a named set of entities of one kind, such as Employees. It has *attributes* $A_1, \ldots, A_m$, each with a domain, and each entity has one value for each attribute. A *key* of $E$ is a set of attributes whose values identify the entity within $E$; one key is chosen as the primary key, as for a [candidate key](/candidate-key/) of a relation.

- A *composite attribute*, such as an address, has parts, such as street and city.
- A *multivalued attribute*, such as a set of phone numbers, has a set of values for each entity.
- A *derived attribute*, such as an age computed from a birth date, is not stored.

**Relationship sets.** A *relationship set* $R$ of degree $n$ among entity sets $E_1, \ldots, E_n$ (not necessarily distinct) is a set of tuples $(e_1, \ldots, e_n)$ with $e_i \in E_i$. Each position is a *role*, and the role names are needed when an entity set occurs twice, as in a relationship Reports_To between two employees. Under set semantics a combination of entities occurs at most once. A relationship set can have its own *descriptive attributes*, such as the date since which an employee works in a department.

**Cardinality constraints.** A constraint $(\mathit{min}_i, \mathit{max}_i)$ on role $i$ of $R$ says that each entity of $E_i$ occurs in role $i$ of at least $\mathit{min}_i$ and at most $\mathit{max}_i$ tuples of $R$, with $\mathit{max}_i = \infty$ allowed. The usual special cases:

- *Key constraint* (many-to-one): $\mathit{max}_i = 1$. In a binary relationship, each entity of $E_i$ is related to at most one entity of the other set.
- *Total participation*: $\mathit{min}_i \ge 1$. Each entity of $E_i$ takes part in at least one relationship.
- *One-to-one*, *one-to-many* and *many-to-many* binary relationships: $\mathit{max} = 1$ on both roles, on one role, or on neither.

**Weak entity sets.** A *weak entity set* $W$ has no key of its own. It is identified through an *identifying relationship* with an *owner* entity set $O$, in which $W$ has a key constraint and total participation. A *partial key* of $W$ identifies a weak entity among those of one owner, so the key of $O$ together with the partial key is a key of $W$.

**Class hierarchies.** In the extended ER model, an entity set can have subclasses (ISA), whose entities are also entities of the superclass and inherit its attributes and key. *Overlap* constraints say whether an entity can be in two subclasses, and *covering* constraints say whether each entity of the superclass is in some subclass.

**Instances.** An *instance* assigns a finite set of entities, with attribute values, to each entity set, and a finite set of tuples to each relationship set. It is *legal* when the keys identify the entities, each relationship tuple uses entities of the right sets, and all cardinality, weak entity and hierarchy constraints hold.

**The mapping to relations.** The standard mapping is as follows. Here $K_E$ is the primary key of $E$.

| ER construct | relation schema | key and constraints |
|---|---|---|
| entity set $E$ | $E$ with the simple attributes of $E$, composite ones flattened into their parts | $K_E$ |
| many-to-many $R$ among $E_1, \ldots, E_n$ | $R(K_{E_1}, \ldots, K_{E_n}$, attributes of $R)$ | $K_{E_1} \cdots K_{E_n}$; a foreign key from each $K_{E_i}$ to $E_i$ |
| binary $R$ with a key constraint on $E_1$ | as above with key $K_{E_1}$, or folded into $E_1$ as the columns $K_{E_2}$ and the attributes of $R$ | if folded, the columns are null for entities of $E_1$ in no relationship |
| weak entity set $W$ with owner $O$ | $W(K_O$, partial key, attributes of $W)$ | $K_O$ with the partial key; a foreign key to $O$, with deletion cascading from $O$ |
| subclass $S$ of $E$ | $S(K_E$, attributes of $S)$, or one relation per leaf class with all inherited attributes | $K_E$; a foreign key to $E$ in the first form |
| multivalued attribute $A$ of $E$ | $E\_A(K_E, A)$ | $K_E A$; a foreign key to $E$ |

The foreign keys are [inclusion dependencies](/inclusion-dependency/) into keys. The keys are [functional dependencies](/functional-dependency/) of the form $K \to U$. Each relation of the mapping, with only its key FD, is in BCNF.

**Example.** This is the running example of Ramakrishnan and Gehrke. The entity sets are Employees(ssn, name, lot) with key ssn and Departments(did, dname, budget) with key did. Works_In is a many-to-many relationship between them with the attribute since, so it becomes Works_In(ssn, did, since) with key (ssn, did) and two foreign keys. Manages gives each department at most one manager, so it is folded into Dept_Mgr(did, dname, budget, ssn, since) with key did, where ssn is null for a department without a manager. Dependents is a weak entity set with partial key pname, owned by Employees through the relationship Policy, so it becomes Dep_Policy(pname, age, cost, ssn) with key (pname, ssn) and a foreign key to Employees with cascading deletes.

## What it counts

The model has no running time. What it counts are participations, and they give simple bounds on the sizes of a legal instance. Each tuple of $R$ has exactly one entity in role $i$, so the number of tuples of $R$ is the sum over the entities of $E_i$ of their participations in role $i$. A constraint $(\mathit{min}_i, \mathit{max}_i)$ on role $i$ then gives
$$\mathit{min}_i \cdot |E_i| \;\le\; |R| \;\le\; \mathit{max}_i \cdot |E_i|$$
for each role $i$. For example, a binary relationship that is one-to-one with total participation on both sides forces $|E_1| = |R| = |E_2|$.

The mapping gives one relation for each entity set, each weak entity set, each relationship set that is not folded, and each multivalued attribute. Folding a many-to-one relationship into its entity set saves a relation and a join, at the cost of null values for entities that take no part.

## Relation to other models

- **Relational model.** The mapping above turns an ER design into relation schemas with keys and foreign keys. Some ER constraints have no direct form as keys and foreign keys. Total participation of $E$ in a many-to-many $R$ is the inclusion dependency $\pi_{K_E}(E) \subseteq \pi_{K_E}(R)$, whose right side is not a key of $R$, so SQL needs a check, an assertion or a trigger for it. A cardinality bound such as $\mathit{max} = 3$ has no key form either.
- **Normalization.** An ER diagram shows the keys of entity sets but not the FDs among their attributes. If Employees has the attributes zip and city with zip $\to$ city, the relation Employees is not in BCNF, and [normalization](/normalization/) is still needed after the mapping. A ternary relationship among Course, Teacher and Book in which the teachers and the books of a course are independent has the [multivalued dependency](/multivalued-dependency/) course $\twoheadrightarrow$ teacher, and its relation violates [4NF](/fourth-normal-form/); the better design has two binary relationships.
- **UML and the earlier models.** UML class diagrams use the same ideas, with associations and multiplicities in place of relationship sets and cardinality constraints. Chen presented the ER model as a common view of the network, relational and entity set models of the time.

## Known results in the model

**A ternary relationship is not the join of its binary projections.** Let Supplies relate suppliers, parts and projects, with the three tuples $(s_1, p_1, j_2)$, $(s_1, p_2, j_1)$ and $(s_2, p_1, j_1)$. Its projections on supplier and part, part and project, and project and supplier contain $s_1 p_1$, $p_1 j_1$ and $j_1 s_1$, so their join contains $(s_1, p_1, j_1)$, which is not in Supplies. So replacing a ternary relationship set by three binary ones loses information in general. It is safe exactly when the relationship set satisfies the [join dependency](/join-dependency/) $\bowtie[SP, PJ, JS]$.

**Cardinality constraints can force empty sets in finite instances.** Take one entity set $E$ and a binary relationship $R$ on $E \times E$ with the constraint $(2, \infty)$ on role 1 and $(0, 1)$ on role 2. By the bounds above, $2|E| \le |R| \le |E|$, so every finite legal instance has $E = \emptyset$. An infinite instance with $E$ nonempty exists: let $E$ be the set of finite binary strings and $R = \{(w, w0), (w, w1)\}$. Each string is first in two tuples, and each string is second in at most one tuple, since the empty string is second in none. So satisfiability over finite instances and over all instances differ. Lenzerini and Nobili (1990) studied this question for ER schemas with cardinality constraints. A designer can apply the bounds of the previous section to the constraints of a schema to find such conflicts.

## References
