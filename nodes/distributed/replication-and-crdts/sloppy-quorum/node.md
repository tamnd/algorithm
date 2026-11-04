---
tag: X1134J
kind: technique
slug: sloppy-quorum
name: Sloppy quorum
aliases:
- sloppy quorums
area: distributed/replication-and-crdts
level: advanced
summary: Writes go to the first healthy nodes on the ring rather than the fixed replica set, trading strict overlap for availability.
---

Writes go to the first healthy nodes on the ring rather than the fixed replica set, trading strict overlap for availability.
