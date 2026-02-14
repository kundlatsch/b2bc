![Carcule Meme](assets/carcule.jpeg)

# B2B/C Protocol v1.0

> **Important note**
> The B2B/C protocol is **educational, experimental, and intentionally playful**. It was created as a learning tool and a conceptual sandbox.
>
> The **“C” in B2B/C stands for *Carcule*** — a meme character that serves as the unofficial mascot of the protocol.

---

## 1. Overview

**B2B/C (Brain to Brain / Carcule)** is a human-readable, message-oriented protocol designed to simulate structured communication between agents (human or artificial).

It is primarily intended for:

* Teaching protocol design concepts
* Exploring agent-based communication
* Demonstrating state synchronization and message correlation
* Having fun while learning

The protocol emphasizes **clarity, semantics, and traceability** over performance or efficiency.

---

## 2. Design Philosophy

B2B/C follows a few core principles:

* **Educational first**: optimized for learning, not throughput
* **Human-readable**: logs should be understandable without tooling
* **Extensible by design**: new message types and keys can be added freely
* **Deterministic semantics**: each message has a single, clear intention

---

## 3. Message Structure

Each protocol message consists of two main parts:

```
<message_id>,<correlation_id>|<TYPE>><action>><key>[>value]
```

### 3.1 Fields

| Field            | Description                            |
| ---------------- | -------------------------------------- |
| `message_id`     | Unique UUID identifying the message    |
| `correlation_id` | UUID of the related message (optional) |
| `TYPE`           | Semantic type of the message           |
| `action`         | Primary action verb                    |
| `key`            | Hierarchical or symbolic key           |
| `value`          | Associated value (when applicable)     |

If a message has no correlation, the field is left empty:

```
<uuid>,|DELTA>set>mood.happy>0.7
```

---

## 4. Message Types

### 4.1 DELTA

Represents a **state mutation** — either setting or updating an internal value.

```
DELTA>set>mood.happy>0.7
```

Characteristics:

* Creates or overwrites a state key
* Values are typically continuous (`float`, often `0.0–1.0`)
* **Must be acknowledged** with an `ACK`

---

### 4.2 ACK

Confirms successful reception and processing of a previous message.

```
ACK>of>DELTA>ok
```

Rules:

* Always references another message via `correlation_id`
* Carries no state or payload
* Exists purely for protocol clarity and traceability

---

### 4.3 EMIT

Emits a **non-persistent semantic signal**, such as a thought, event, or notice.

```
EMIT>signal>thought>I feel a shift
```

Properties:

* Does **not** modify state
* May be logged, displayed, or ignored
* May trigger events on the side of the receiver (these events can modify state)
* Still requires an `ACK` (Carcule likes politeness)

---

### 4.4 QUERY

Requests information from the remote agent.

#### Specific key query

```
QUERY>get>mood.happy>
```

#### Aggregate or scoped query

```
QUERY>overall>>
```

Notes:

* Queries do not return inline values
* A single `QUERY` may generate **multiple DATA responses**

---

### 4.5 DATA

Provides informational responses to a `QUERY`.

```
DATA>value>mood.happy>0.7
```

Aggregate example:

```
DATA>value>overall>0.2245
```

Rules:

* Always references the originating `QUERY`
* Multiple `DATA` messages may share the same `correlation_id`

---

## 5. Hierarchical Keys

Keys follow a dot-separated hierarchy:

```
<namespace>.<subkey>[.<subkey>]
```

Examples:

* `mood.happy`
* `mood.anxious`
* `focus.depth`

### 5.1 Composite and Semantic Keys

Higher-level keys (e.g., `overall`) may represent computed or derived values. Their meaning is **implementation-defined**, not protocol-defined.

---

## 6. State Model

Each agent maintains an internal **State Map**:

```
{
  "mood.happy": 0.7,
  "mood.anxious": 0.4,
  "focus.depth": 0.9
}
```

State rules:

* Modified only by `DELTA`
* Read via `QUERY`
* Never directly altered by `DATA` or `EMIT`

---

## 7. Aggregations

Aggregations are **out of scope for the protocol** and fully delegated to the implementation.

Example (purely illustrative):

```
overall = (happy - anxious) * focus
```

The protocol defines **how to ask** for an aggregation, not **how it is calculated**.

---

## 8. Non-Goals

B2B/C explicitly does **not** aim to be:

* Efficient
* Secure
* Binary
* Network-transport specific
* A real standard
