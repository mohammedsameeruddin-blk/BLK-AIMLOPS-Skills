# BLK AI MLOps Skills

Reusable AI skills for designing and generating standardized ML/MLOps projects.

## Objective

The goal of this repository is to provide a consistent, AI-driven approach for designing and implementing machine learning solutions.

A user should be able to describe an ML use case in natural language, and the AI should:

1. Understand the ML use case
2. Gather the required information
3. Inspect available information such as dataset metadata where possible
4. Ask only the necessary clarifying questions
5. Present feasible options when a decision is required
6. Create a canonical ML project specification
7. Validate the specification through defined gates
8. Design the ML/MLOps architecture
9. Design the required pipelines
10. Map the design to the target platform
11. Generate the required implementation
12. Validate the generated implementation

The ultimate goal is that different users providing the same requirements should receive a highly consistent architecture, process, and implementation.

## Core Workflow

The framework follows a gated workflow:

```text
User Request
     |
     v
Understand Request
     |
     v
Identify ML Problem
     |
     v
Requirements Discovery
     |
     v
Canonical ML Project Specification
     |
     v
Requirements Gate
     |
     v
ML Design
     |
     v
Pipeline Design
     |
     v
Architecture
     |
     v
Platform Mapping
     |
     v
Implementation Generation
     |
     v
Implementation Validation
     |
     v
Final ML/MLOps Project
```

The AI should not generate implementation code before the required requirements and design decisions have been completed.

## Canonical ML Project Specification

The canonical ML project specification is the single source of truth for the project.

The original user request should not be independently reinterpreted by every downstream skill.

Instead:

```text
User Request
     |
     v
Requirements Skill
     |
     v
Canonical Project Specification
     |
     +----------+----------+----------+
     |          |          |          |
     v          v          v          v
   Data      Training   Inference  Monitoring
```

Downstream skills should consume and update the canonical specification where appropriate.

This approach is intended to improve consistency across users, projects, and AI agents.

## Requirements Discovery

The AI should gather requirements progressively rather than asking all questions at once.

Questions should:

* Be relevant to the current stage
* Avoid information that is already known
* Use available dataset metadata where possible
* Provide feasible options when meaningful options can be determined
* Ask for human input when a decision cannot be reliably inferred

The general interaction is:

```text
Question
   |
   v
User Answer
   |
   v
Update Canonical Specification
   |
   v
Evaluate Completeness
   |
   +---- Missing information ----> Ask next question
   |
   +---- Complete ---------------> Proceed to Gate
```

## Gated Workflow

The framework uses explicit gates to control progression.

Initial gates include:

### Requirements Gate

Confirms that sufficient information exists to design the ML solution.

### Architecture Gate

Confirms that the proposed ML/MLOps architecture is complete and consistent with the requirements.

### Implementation Gate

Confirms that the implementation can be generated from the approved specification and architecture.

### Validation Gate

Confirms that the generated implementation satisfies the project specification and required quality checks.

The exact gates may evolve as the framework matures.

## ML Problem Types

The framework is designed to support multiple ML problem types:

* Anomaly Detection
* Classification
* Regression
* Forecasting
* Clustering
* Other ML use cases

The first implemented use case is Anomaly Detection.

Each ML problem type should have its own specialized skill while sharing common ML concepts and pipeline capabilities.

## Pipeline Architecture

The framework separates the major ML/MLOps pipeline responsibilities:

```text
Data Pipeline
     |
     +---- Training
     |
     +---- Inference

Training Pipeline
Inference Pipeline
Retraining Pipeline
Monitoring Pipeline
```

The exact pipeline components depend on the requirements.

## Shared Data Transformation

Training and inference must use the same logical data transformation definition.

Training may fit preprocessing transformations and persist the resulting artifacts.

```text
Training Data
     |
     v
Fit Transformations
     |
     v
Persist Transformation Artifacts
     |
     v
Transform Training Data
```

Inference must reuse the artifacts produced during training.

```text
Inference Data
     |
     v
Load Transformation Artifacts
     |
     v
Transform Inference Data
```

Inference must not fit preprocessing transformations again.

Examples of transformation artifacts include:

* Scalers
* Encoders
* Imputers
* Feature transformers
* Other learned preprocessing components

## Platform Independence

The core skills are platform-independent.

Skills define:

* What needs to be done
* Why it needs to be done
* Required decisions
* Decision rules
* Expected inputs and outputs
* Validation requirements

Platform adapters define:

* How the design is implemented on a specific platform
* Platform-specific services
* Platform-specific deployment mechanisms
* Platform-specific orchestration
* Platform-specific storage and compute

For example:

```text
Generic Data Pipeline Skill
          |
          v
Platform Adapter
     /          \
Databricks       AWS
     |             |
Databricks       AWS
Implementation   Implementation
```

The core ML/MLOps reasoning should not depend on Databricks or any other specific platform.

## Consistency

A major objective of the framework is consistency.

For the same:

* Use case
* Dataset characteristics
* Business requirements
* ML requirements
* MLOps requirements
* Platform capabilities

the generated architecture and implementation should be highly similar.

Consistency should be achieved through:

* Canonical specifications
* Explicit decision rules
* Reusable templates
* Standardized pipeline structures
* Defined gates
* Platform capability mappings
* Validation rules

The AI should not rely solely on free-form reasoning for decisions that can be standardized.

## Human Decision Points

The AI should make deterministic decisions where established rules are sufficient.

When multiple materially different approaches are feasible and the choice depends on a business or architectural preference, the AI should:

1. Explain the available options
2. Provide the relevant trade-offs
3. Ask the user to select or confirm an option
4. Record the decision in the canonical project specification

The AI should not silently make material decisions that require user input.

## Extensibility

The framework is designed to evolve incrementally.

New ML problem types can be added without redesigning the core workflow.

Examples:

```text
ML
 |
 +-- Anomaly Detection
 +-- Classification
 +-- Regression
 +-- Forecasting
 +-- Clustering
```

Similarly, new platforms can be added through platform adapters:

```text
Platform
 |
 +-- Databricks
 +-- AWS
 +-- Azure
 +-- GCP
 +-- Other platforms
```

The same core skills should be reusable across these implementations.

## Current Scope

The initial implementation focuses on:

* Skill architecture
* Requirements gathering
* Canonical ML project specification
* ML problem abstraction
* Anomaly detection
* Shared data transformation principles
* Gated workflow
* Platform-independent architecture

Platform-specific implementation and full code generation will be added incrementally.
