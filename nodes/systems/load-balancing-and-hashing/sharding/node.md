---
tag: 0T7Z8J
kind: concept
slug: sharding
name: Sharding
aliases:
- horizontal partitioning
area: systems/load-balancing-and-hashing
level: intro
summary: Split the records of one data set over several machines by a key, so that each machine holds and serves one part, a shard. A rule maps each key to a shard, and a map assigns shards to machines.
see_also: [hash-partitioning, range-partitioning, dynamic-partitioning-problem, load-skew, consistent-hashing, quorum-replication, two-phase-commit, partitioner]
sources:
  - book: isbn:9781449373320
    title: Martin Kleppmann, Designing Data-Intensive Applications, O'Reilly, 2017
    locator: "Chapter 6, Partitioning: the names used in different systems (shard, region, tablet, vnode, vBucket), partitioning by key range and by hash of key, partitioning and secondary indexes (local and global indexes), rebalancing, request routing"
  - paper: doi:10.1145/129888.129894
    title: David DeWitt and Jim Gray, Parallel database systems, the future of high performance database systems, Communications of the ACM 35(6), 1992, pages 85 to 98
    locator: the section on data partitioning (horizontal partitioning of a relation over the disks of the processors, by round robin, hash or range)
  - url: https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/
    title: Redis cluster specification
    locator: "Key distribution model (16,384 hash slots), Hash tags, and the MOVED and ASK redirections"
  - url: https://research.google/pubs/bigtable-a-distributed-storage-system-for-structured-data/
    title: Fay Chang, Jeffrey Dean, Sanjay Ghemawat and others, Bigtable, a distributed storage system for structured data, OSDI 2006
    locator: "Section 2, Rows (the row range of a table is dynamically partitioned into tablets), and Section 5 (tablet location and assignment)"
---

Sharding splits the records of one data set over several machines, so that each machine stores and serves only a part of the data, called a shard (or a partition, region, tablet or vnode, depending on the system). Each record has a shard key, a rule maps the key to a shard, and a second map assigns shards to machines. It is the way to grow a data set beyond the storage or the throughput of one machine. The cost is that every operation that needs more than one shard, such as a query on another attribute, a join or a transaction over two keys, is now a distributed operation.

## In plain words

One machine can hold only so much data and answer only so many requests. When a table outgrows it, cut the table into pieces by rows and give each machine some of the pieces. Each row has a key, for example the customer number, and a fixed rule tells which piece holds which key. To read or change one customer, go to the one machine that holds that piece.

This works well when most work is about one key at a time. It works less well when a question needs rows from many pieces, such as "all customers in one city", because then every machine must answer and someone must combine the results. The choice of the key decides which questions are cheap.

## The idea

**Three maps.** Sharding has three parts that are often designed apart.

1. **The shard key.** The attribute, or the prefix of a compound key, that decides placement. Operations that name one shard key value touch one shard.
2. **Key to shard.** The partitioning rule. [Hash partitioning](/hash-partitioning/) gives even shards and loses order. [Range partitioning](/range-partitioning/) keeps order, so range scans stay cheap, but needs split points that follow the data. A directory, a table from key to shard, allows any placement at the cost of a lookup.
3. **Shard to machine.** Usually many more shards than machines, so that a machine can join or leave by moving whole shards. A hash ring, [rendezvous hashing](/rendezvous-hashing/), or a table kept by a coordinator does this part; the [dynamic partitioning problem](/dynamic-partitioning-problem/) states what such a map must achieve.

**Routing.** A request must reach the machine that holds its shard. There are three common designs: a client that knows the map, a router or proxy that knows it, or any node that forwards or redirects. A Redis Cluster node that does not hold the slot of a key answers with a MOVED redirection that names the right node. In Bigtable, clients find a tablet through a small hierarchy of location tablets and cache the result.

**Sharding and replication.** Sharding divides the data; replication copies each shard to several machines for fault tolerance and read throughput. Most systems do both: each shard is a replicated group, with a primary and backups, a chain, or a [quorum](/quorum-replication/).

**What sharding costs.**

- **Queries on other attributes.** With a local secondary index, each shard indexes its own records, so a query by the indexed attribute goes to every shard and the results are merged (scatter and gather). With a global index, the index is itself sharded by the indexed value, so a query reads one index shard, but a write may touch two shards: the record's shard and the index shard.
- **The slowest shard.** A query to $k$ shards waits for the slowest one. If one shard in 100 is slow at a given moment, a query to 100 shards meets a slow shard with probability $1 - 0.99^{100} \approx 0.63$.
- **Transactions over shards.** A write to two shards needs an atomic commit protocol such as [two-phase commit](/two-phase-commit/), or the application must accept that the two parts are not atomic.
- **Skew.** Shards that are equal in size are not equal in traffic if some keys are hot; see [load skew](/load-skew/).
- **Resharding.** Changing the number of shards or their split points moves data while the system serves requests.

**Horizontal versus vertical.** Horizontal partitioning, the subject of this page, splits a table by rows. Vertical partitioning splits it by columns, for example to keep large and rarely read columns apart; it does not, by itself, spread the rows of a table over machines.

## Examples

**One table, four shards.** A table of users with the columns id, email and city is sharded by hash of id over 4 shards. The shards touched by common operations:

| operation | shards touched |
|---|---|
| read or update the user with a given id | 1 |
| find the user with a given email, local index | 4 |
| find the user with a given email, global index by email | 1 index shard, then 1 data shard |
| insert a user, global index by email | up to 2 |
| count the users in each city | 4, then a merge |
| move credit between two random users | 2 with probability $3/4$ (needs an atomic commit), else 1 |

The shard key id makes the first operation cheap. If most traffic were lookups by email, email would be the better shard key.

**Redis Cluster.** The key space is cut into 16,384 hash slots by a CRC16 of the key, and each master owns a set of slots. Hash tags let the application put related keys in one slot, so that an operation on several keys stays on one node.

**Bigtable and its successors.** The rows of a table are kept in key order and cut into tablets, contiguous key ranges that split when they grow. A master assigns tablets to tablet servers and moves them to balance load.

**Parallel databases.** DeWitt and Gray (1992) describe the horizontal partitioning of each relation over the disks of a shared-nothing machine, by round robin, hash or range, as the basis of parallel query processing. Two relations partitioned by the same hash of a join attribute can be joined shard by shard with a [hash join](/hash-join/).

## Where it is used

- Distributed key-value stores and caches: Redis Cluster, memcached client libraries, Dynamo and its successors, which shard with [consistent hashing](/consistent-hashing/).
- Wide-column and NewSQL stores: Bigtable, HBase, Spanner and others, which shard by key range and split ranges as they grow.
- Search engines and document stores: an Elasticsearch index is a fixed number of primary shards chosen by a hash of the routing value.
- Application-level sharding of relational databases, where a service routes each customer or tenant to one of many database servers.
- Parallel query engines, which shard the data for each step of a query; the [partitioner](/partitioner/) of a MapReduce job is the same rule applied to intermediate data.

## References
