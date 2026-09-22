# AI MLOps Skills Architecture

## Objective

The AI MLOps Skills framework converts natural-language ML/MLOps requirements into a standardized, validated, runnable ML/MLOps implementation.

The framework is designed to:

* gather requirements before implementation
* maintain a canonical machine-readable project specification
* apply standardized ML reasoning
* generate consistent pipeline architectures
* separate platform-independent ML design from platform-specific implementation
* validate generated implementations
* support multiple ML problem types and deployment platforms
* minimize unnecessary variation between projects with equivalent requirements

---

## Architectural Principles

### 1. Requirements Before Implementation

The system must not generate production implementation code until the required project decisions have been collected and validated.

```text
User Request
     |
     v
Requirements Discovery
     |
     v
Requirements Gate
     |
     +---- incomplete ----> Ask Next Question
     |
     v
ML / Pipeline Design
```

---

### 2. Canonical Specification as the Single Source of Truth

The Canonical ML Project Specification is the central contract between all skills.

The user request must not be independently reinterpreted by every downstream skill.

```text
                         +----------------------+
                         | Canonical ML Project |
                         | Specification        |
                         +----------+-----------+
                                    |
             +----------------------+----------------------+
             |                      |                      |
             v                      v                      v
       ML Design              Pipeline Design       Platform Mapping
             |                      |                      |
             +----------------------+----------------------+
                                    |
                                    v
                             Code Generation
```

The canonical specification is maintained throughout the workflow.

Skills may:

* read it
* add derived information
* add design decisions
* validate relevant sections
* update their owned sections

Skills must not create competing project specifications.

---

## High-Level Workflow

```text
User Request
     |
     v
MLOps Orchestrator
     |
     v
Understand Request
     |
     v
Identify ML Problem
     |
     v
Requirements Skill
     |
     +------------------------------+
     |                              |
     | Requirements incomplete      |
     |                              |
     +----------< Ask Question <----+
     |
     v
Canonical ML Project Specification
     |
     v
Requirements Gate
     |
     +---- FAIL ----> Requirements Skill
     |
     v
ML Problem Skill
     |
     v
Specialized ML Skill
     |
     v
Pipeline Design
     |
     v
Architecture Design
     |
     v
Platform Adapter
     |
     v
Code Generation
     |
     v
Implementation Validation
     |
     +---- FAIL ----> Relevant Design Stage
     |
     v
Final ML/MLOps Project
```

---

# Component Responsibilities

## MLOps Orchestrator

The orchestrator is the control layer.

It is responsible for:

* understanding the user's request
* selecting the appropriate skills
* controlling workflow progression
* maintaining stage order
* invoking requirements gathering
* enforcing gates
* routing to ML problem skills
* coordinating pipeline and architecture design
* selecting the platform adapter
* invoking code generation
* coordinating validation and recovery

The orchestrator should not contain detailed algorithm-selection logic or platform-specific implementation logic.

---

## Requirements Skill

The Requirements Skill converts natural language into structured project requirements.

It is responsible for:

* identifying missing requirements
* inspecting available dataset/schema information
* deriving information where possible
* asking only necessary questions
* generating context-aware options
* tracking requirement state
* detecting conflicting requirements
* updating the canonical specification
* determining when requirements are complete

The requirements interaction is iterative:

```text
Read Canonical Spec
       |
       v
Find unresolved requirements
       |
       v
Can requirement be derived?
   /             \
 Yes              No
  |                |
  v                v
Derive          Ask User
  |                |
  +-------+--------+
          |
          v
Update Canonical Spec
          |
          v
Evaluate Completeness
          |
    +-----+------+
    |            |
 Complete      Incomplete
    |            |
    v            +----> Next Question
Requirements Gate
```

---

## ML Problem Skill

The ML Skill determines the appropriate machine-learning approach from the canonical specification.

It is responsible for:

* confirming the ML problem type
* selecting the learning paradigm
* evaluating data characteristics
* identifying candidate algorithms
* evaluating algorithm feasibility
* defining training strategy
* defining validation strategy
* defining evaluation metrics
* defining threshold strategy where applicable
* defining model artifacts and inference requirements

The ML Skill determines the logical ML design.

It does not implement platform-specific infrastructure.

---

## Specialized ML Skills

Specialized skills contain problem-specific reasoning.

Initial and planned problem types include:

```text
Anomaly Detection
Classification
Regression
Forecasting
Clustering
Future ML Problem Types
```

For example:

```text
ML Skill
   |
   +---- Anomaly Detection Skill
   |
   +---- Classification Skill
   |
   +---- Regression Skill
   |
   +---- Forecasting Skill
   |
   +---- Clustering Skill
```

Specialized skills extend the common ML rules and must not contradict them.

---

# Pipeline Architecture

The framework treats the ML system as a set of logically connected pipelines.

```text
                    +----------------+
                    | Data Pipeline  |
                    +-------+--------+
                            |
             +--------------+--------------+
             |                             |
             v                             v
      +-------------+               +-------------+
      | Training    |               | Inference   |
      | Pipeline    |               | Pipeline    |
      +------+------+               +------+------+
             |                             |
             v                             v
        Model Artifact               Predictions
             |
             v
      Transformation
         Artifact
             |
             v
       Model Contract
```

## Data Pipeline

The data pipeline is responsible for:

* ingestion
* schema validation
* data-quality checks
* cleaning
* preprocessing
* feature engineering
* producing the feature contract consumed by training and inference

The logical transformation definition should be shared between training and inference.

---

## Training Pipeline

The training pipeline:

1. reads training data
2. fits learned transformations using training data only
3. persists transformation artifacts
4. transforms training/validation/test data using those fitted transformations
5. trains the model
6. evaluates the model
7. persists the model and associated metadata

Conceptually:

```text
Training Data
     |
     v
Fit Transformations
     |
     +----> Transformation Artifact
     |
     v
Transform Data
     |
     v
Train Model
     |
     +----> Model Artifact
     |
     v
Evaluate
```

---

## Inference Pipeline

The inference pipeline must reuse the artifacts produced by training.

```text
New Input
    |
    v
Schema Validation
    |
    v
Load Transformation Artifact
    |
    v
Transform
    |
    v
Load Compatible Model Artifact
    |
    v
Predict
    |
    v
Output
```

### Critical Invariant

Inference must **never fit learned preprocessing transformations**.

For example, inference must not independently fit:

* scalers
* encoders
* imputers
* feature transformers

Instead, it loads the transformation artifact produced by the appropriate training run.

---

## Retraining Pipeline

Retraining is optional and is driven by configured triggers.

Possible triggers include:

* schedule
* data drift
* model drift
* performance degradation
* business-defined threshold
* new labeled data

Retraining must pass the same model validation requirements before a new model version becomes available for inference.

---

# Artifact Consistency

Model artifacts and transformation artifacts are treated as related versioned assets.

A valid model deployment must maintain compatibility between:

```text
Model Version
     |
     +---- Transformation Version
     |
     +---- Feature Definition Version
     |
     +---- Training Configuration
     |
     +---- Data Version
     |
     +---- Code Version
```

The system should prevent incompatible combinations such as:

```text
Model v2
+
Transformation v1
+
Feature Definition v3
```

unless that compatibility has explicitly been established.

---

# Platform Independence

The core skills are platform-independent.

They define:

* requirements
* ML reasoning
* pipeline contracts
* architecture
* validation requirements
* logical artifacts
* logical platform capabilities

They should not directly encode implementation details for a specific platform.

```text
                  Core Skills
                      |
                      v
              Logical Architecture
                      |
        +-------------+-------------+
        |             |             |
        v             v             v
 Databricks        AWS           Azure/GCP
 Adapter           Adapter        Adapter
        |             |             |
        v             v             v
 Platform-specific implementation
```

Platform adapters translate the logical design into platform-specific constructs.

For example, the core architecture may require:

```text
Model Registry
Batch Inference
Workflow Orchestration
Artifact Storage
Monitoring
```

The platform adapter determines how those capabilities are implemented on the target platform.

---

# Code Generation

Code generation occurs only after:

1. requirements are complete
2. ML design is complete
3. pipeline architecture is defined
4. platform mapping is available
5. required gates have passed

Code generation consumes the canonical specification and design outputs.

It should not independently reinterpret the original user request.

---

# Validation

Validation occurs at multiple levels.

## Requirements Validation

Checks:

* required fields are populated
* conditional requirements are resolved
* conflicts are resolved
* user decisions are confirmed
* required dependencies are satisfied

## ML Design Validation

Checks:

* selected algorithm is compatible with the problem
* required data characteristics are available
* training strategy is defined
* validation strategy is defined
* metrics are appropriate
* threshold strategy is defined where required

## Pipeline Validation

Checks:

* training and inference contracts are compatible
* transformations are consistent
* inference does not fit preprocessing
* required artifacts are persisted
* model/artifact versions are compatible

## Implementation Validation

Checks:

* generated project structure is complete
* generated code follows the canonical specification
* configuration is internally consistent
* pipeline dependencies are valid
* tests/checks pass
* platform-specific implementation matches the platform mapping

Validation failures should route the workflow back to the stage responsible for the failed decision rather than blindly regenerating the entire project.

---

# Gates

Gates control progression between major stages.

```text
Requirements Gate
       |
       v
ML Design Gate
       |
       v
Architecture Gate
       |
       v
Platform Mapping Gate
       |
       v
Code Generation Gate
       |
       v
Validation Gate
```

A failed gate must identify:

* unresolved requirement/design
* blocking reason
* owning stage
* required correction

The workflow should not silently bypass a failed gate.

---

# Standardization and Consistency

The framework aims to produce highly consistent implementations when requirements are equivalent.

Consistency is achieved through:

* canonical project specifications
* explicit requirement states
* deterministic decision rules
* reusable ML design patterns
* standardized pipeline structures
* platform adapters
* reusable code-generation templates
* validation gates
* artifact contracts
* explicit assumptions and user decisions

The goal is not to eliminate all variation.

Variation should primarily result from genuine differences in:

* requirements
* data characteristics
* ML problem
* operational constraints
* platform capabilities
* explicit user decisions

The same requirements should therefore lead to substantially similar architecture and implementation.

---

# Extensibility

The architecture is designed to support two independent dimensions of expansion.

## New ML Problem

Add:

```text
skills/ml/<problem-type>/SKILL.md
```

The new skill should implement the common ML contract and define problem-specific reasoning.

Example:

```text
skills/ml/
├── common/
├── anomaly-detection/
├── classification/
├── regression/
├── forecasting/
└── clustering/
```

## New Platform

Add a platform adapter without changing the core ML reasoning.

Example:

```text
platforms/
├── databricks/
├── aws/
├── azure/
└── gcp/
```

This allows the same logical ML design to be mapped to different execution environments.

---

# Architectural Boundary

The intended responsibility boundary is:

```text
+------------------------------------------------------+
|                    ORCHESTRATOR                      |
| Workflow control, routing, gates                     |
+------------------------------------------------------+
                         |
+------------------------------------------------------+
|                  REQUIREMENTS                        |
| Understand, derive, ask, confirm                     |
+------------------------------------------------------+
                         |
+------------------------------------------------------+
|               CANONICAL SPECIFICATION                |
| Single source of truth                               |
+------------------------------------------------------+
                         |
+------------------------------------------------------+
|                    ML SKILLS                         |
| ML reasoning and problem-specific design             |
+------------------------------------------------------+
                         |
+------------------------------------------------------+
|                  PIPELINE DESIGN                     |
| Data / Training / Inference / Retraining             |
+------------------------------------------------------+
                         |
+------------------------------------------------------+
|                 PLATFORM ADAPTER                     |
| Platform-specific implementation mapping             |
+------------------------------------------------------+
                         |
+------------------------------------------------------+
|                 CODE GENERATION                      |
| Runnable project implementation                      |
+------------------------------------------------------+
                         |
+------------------------------------------------------+
|                    VALIDATION                        |
| Requirements / ML / Pipeline / Implementation        |
+------------------------------------------------------+
```

Each layer should have a clear contract with the next layer.

The framework should avoid placing business logic, ML algorithm logic, or platform-specific implementation inside the orchestrator.

```

This architecture now matches the schemas and skills we've established rather than merely documenting the happy-path flow.

**With this file, the initial eight-file architecture is internally coherent.** The next useful step is the **cross-file consistency review**—checking all eight files together for contradictions, duplicated responsibilities, missing references, and whether an agent could actually execute the workflow end-to-end.
```
