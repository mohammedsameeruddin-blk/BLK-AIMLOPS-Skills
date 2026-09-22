# Requirements Gathering Skill

## Purpose

Convert a user's natural-language ML/MLOps request into a complete and structured project specification.

This skill gathers and structures requirements before ML/MLOps architecture or implementation begins.

The skill should progressively determine what information is required, identify what can be derived from available context, ask only necessary questions, and update the canonical ML project specification.

## Responsibilities

The requirements skill is responsible for:

* Understanding the user's business and ML objective
* Identifying required project information
* Inspecting available dataset or schema information where possible
* Determining missing requirements
* Determining whether requirements are required, conditional, optional, or derivable
* Asking progressive clarification questions
* Providing feasible options when meaningful options can be determined
* Detecting conflicting or inconsistent information
* Updating the canonical ML project specification
* Determining when the requirements are complete

The skill must not generate implementation code.

## Requirement Categories

The initial requirement categories are:

### Project

* Project name
* Project description
* Business/use-case objective
* ML problem type

### Data

* Data source
* Data format
* Dataset/table
* Schema
* Entity/key
* Timestamp
* Features
* Target variable, where applicable
* Data volume
* Data frequency

### ML

* ML problem
* Labels and label availability, where applicable
* Candidate algorithms
* Training strategy
* Validation strategy
* Evaluation metrics
* Threshold requirements where applicable

### Inference

* Batch or real-time
* Inference frequency
* Input data
* Output data
* Latency requirements where applicable

### MLOps

* Training frequency
* Model versioning
* Model registry
* Monitoring
* Retraining
* Deployment requirements

### Platform

* Target platform
* Compute requirements
* Storage
* Orchestration
* Model serving where applicable

## Requirement Classification

Each requirement should be treated as one of the following:

### Required

Information that must be available before the relevant workflow gate can pass.

### Conditional

Information that becomes required only when a specific condition is met.

Example:

```text
Inference mode = real-time
        |
        v
Latency requirement = required
```

### Optional

Information that may improve the solution but is not required to proceed.

### Derived

Information that can be reliably determined from available context, metadata, schema, or established rules.

The skill should derive information where reliable derivation is possible instead of asking the user unnecessarily.

## Requirement State

Each requirement should have a logical state such as:

* Unknown
* Provided
* Derived
* Confirmed
* Conflicting

A requirement is considered satisfied when it has a valid provided, derived, or confirmed value and no unresolved conflict exists.

## Question Strategy

Do not ask all questions at once.

Ask questions progressively based on:

* Current canonical specification
* Selected ML problem
* Available dataset/schema information
* Requirement dependencies
* Previously provided answers
* Architecture requirements

The skill should ask only the highest-priority unresolved question or a small logically related group of questions.

Do not ask for information that is already known or can be reliably derived.

## Question Selection Process

For each requirements iteration:

```text
1. Read the current canonical specification
2. Identify unresolved requirements
3. Determine which unresolved requirements are required
4. Evaluate dependencies between requirements
5. Determine whether the information can be derived
6. Derive reliable information where possible
7. Identify the highest-priority unresolved user decision
8. Ask the user for that information
9. Update the canonical specification
10. Re-evaluate requirements completeness
11. Repeat until the requirements gate can pass
```

## Dynamic Options

Prefer multiple-choice options when meaningful options can be determined from available information.

Options should be derived from:

* User-provided context
* Dataset schema
* Dataset metadata
* Existing project information
* Platform capabilities
* Established decision rules

Do not present options that are unsupported by the available context.

Example:

User:

> "I want anomaly detection for customer transactions."

The skill should not ask:

> "What is your ML problem?"

The ML problem is already apparent from the request.

Instead, it may ask:

> "Where is your transaction data stored?"

Possible options:

1. Databricks table
2. CSV/Parquet
3. Database
4. Cloud object storage
5. Other

## Dataset and Schema Inspection

When dataset or schema information is available, inspect it before asking questions that can be answered from the available information.

For example, if the schema contains:

```text
customer_id
transaction_id
merchant_id
amount
transaction_timestamp
```

the skill may identify:

* Candidate entity columns
* Candidate timestamp columns
* Numerical features
* Categorical features
* Potential target columns

It should then ask the user only for unresolved business decisions.

Example:

> "I found `customer_id`, `transaction_id`, and `merchant_id`. Which entity should anomalies be associated with?"

Possible options:

1. Customer
2. Transaction
3. Merchant
4. Other

The skill should not silently select an entity when the choice represents a business decision.

## Inference and Confirmation

The skill may make deterministic inferences when supported by reliable evidence.

However, inferred information that represents a material business or architectural decision should be presented to the user for confirmation.

Example:

```text
Detected:
transaction_timestamp appears to be the timestamp column.

Decision:
Should transaction_timestamp be used as the event timestamp?
```

The confirmed decision should be recorded in the canonical specification.

## Requirement Dependencies

Requirements may depend on previous decisions.

Examples:

### Inference mode

```text
Inference mode
    |
    +-- Batch
    |     |
    |     +-- Inference frequency
    |
    +-- Real-time
          |
          +-- Latency requirement
          |
          +-- Serving requirement
```

### Label availability

```text
Labels available?
    |
    +-- Yes
    |     |
    |     +-- Label meaning
    |     +-- Label quality
    |     +-- Label coverage
    |
    +-- No
          |
          +-- Unsupervised/semi-supervised approaches
```

### Timestamp availability

```text
Timestamp available?
    |
    +-- Yes
    |     |
    |     +-- Temporal/contextual requirements
    |
    +-- No
          |
          +-- Point-anomaly considerations
```

The skill should evaluate these dependencies dynamically rather than asking every possible question.

## Conflict Handling

If new information conflicts with an existing requirement, do not silently overwrite the existing value.

Example:

```text
Existing:
Labels are not available.

New information:
Dataset contains fraud_label.
```

The skill should:

1. Detect the conflict
2. Present the conflicting information
3. Ask the user to clarify
4. Update the canonical specification after clarification

## Requirement Completeness

Requirements are complete when:

* All required requirements have a valid value
* All conditional requirements triggered by the selected architecture have a valid value
* Required user decisions have been confirmed
* No unresolved conflicts remain
* No required dependency remains unresolved

At that point, the requirements skill should indicate that the requirements gate can be evaluated.

## Canonical Specification

The canonical ML project specification is the source of truth.

The requirements skill should:

* Read the current specification
* Add newly provided information
* Add reliably derived information
* Record confirmed decisions
* Preserve unresolved information as unresolved
* Avoid silently replacing conflicting information

The skill should not maintain a separate competing project specification.

## Example Interaction

User:

> "I want anomaly detection for customer transactions."

The skill may determine:

```text
ML problem:
Anomaly Detection

Business domain:
Customer transactions

Still required:
- Dataset
- Entity
- Relevant features
- Timestamp/context
- Anomaly definition
- Label availability
- Inference mode
- Expected output
```

The skill should then ask the highest-priority unresolved question rather than asking all questions simultaneously.

## Important Rules

1. Do not generate implementation code.
2. Do not ask for information that is already known.
3. Do not ask for information that can be reliably derived.
4. Do not silently make material business decisions.
5. Do not silently overwrite conflicting requirements.
6. Update the canonical project specification after each meaningful interaction.
7. Do not declare requirements complete while required dependencies or conflicts remain unresolved.
8. Do not proceed to implementation from this skill.
