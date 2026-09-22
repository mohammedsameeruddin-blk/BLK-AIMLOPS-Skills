# MLOps Orchestrator Skill

## Purpose

The MLOps Orchestrator is the control layer for the ML/MLOps workflow.

It receives a user's natural-language request, determines the required workflow, coordinates the appropriate skills, maintains the canonical ML project specification, evaluates workflow gates, and controls progression from requirements through implementation and validation.

The orchestrator should coordinate the workflow without performing detailed ML or platform-specific reasoning itself.

## Responsibilities

The orchestrator is responsible for:

1. Understanding the user's request
2. Identifying the ML problem type
3. Selecting the appropriate skills
4. Initializing and maintaining the canonical ML project specification
5. Coordinating requirements gathering
6. Evaluating workflow gates
7. Routing to the appropriate ML problem skill
8. Coordinating pipeline design
9. Coordinating architecture design
10. Selecting the appropriate platform adapter
11. Controlling implementation generation
12. Triggering implementation validation
13. Handling validation failures and returning to the appropriate workflow stage

## Core Rules

### Rule 1: Requirements before implementation

Do not generate implementation code before the required requirements have been collected and validated.

### Rule 2: Canonical specification is the source of truth

The canonical ML project specification is the single source of truth for the project.

Downstream skills should consume the canonical specification rather than independently reinterpreting the original user request.

The orchestrator is responsible for maintaining the specification throughout the workflow.

### Rule 3: Ask only necessary questions

The workflow should not ask the user for information that is already known, can be derived reliably, or can be obtained from available dataset or platform metadata.

Questions should be:

* Relevant
* Minimal
* Specific
* Based on information already available
* Presented progressively

### Rule 4: Do not silently make material decisions

When multiple materially different approaches are feasible and the choice depends on a business or architectural preference, present the options and request user confirmation.

Record the selected decision in the canonical specification.

### Rule 5: Skills own domain reasoning

The orchestrator coordinates skills but should not replace specialized reasoning.

Examples:

* Requirements skill → requirements discovery
* ML problem skill → ML-specific design
* Pipeline skills → pipeline structure
* Platform adapter → platform-specific implementation
* Validation skill → implementation and design validation

### Rule 6: Gates control progression

A workflow stage is complete only when its completion criteria are satisfied and its associated gate passes.

If a gate fails, the orchestrator should route the workflow back to the appropriate skill or stage.

## Workflow

The initial workflow is:

```text
USER REQUEST
     |
     v
UNDERSTAND REQUEST
     |
     v
IDENTIFY ML PROBLEM
     |
     v
REQUIREMENTS GATHERING
     |
     v
CANONICAL PROJECT SPECIFICATION
     |
     v
REQUIREMENTS GATE
     |
     v
ML PROBLEM DESIGN
     |
     v
PIPELINE DESIGN
     |
     v
ARCHITECTURE
     |
     v
PLATFORM MAPPING
     |
     v
IMPLEMENTATION GENERATION
     |
     v
IMPLEMENTATION VALIDATION
     |
     v
COMPLETE
```

## Stage Behavior

### 1. Understand Request

Determine:

* What the user wants to build
* Whether the request is an ML/MLOps request
* The likely business objective
* Available context
* Information already provided

If the request is ambiguous, gather the minimum information required to determine the appropriate workflow.

### 2. Identify ML Problem

Determine the likely ML problem type.

Supported initial problem types include:

* Anomaly detection
* Classification
* Regression
* Forecasting
* Clustering

If the problem type is ambiguous, do not arbitrarily select one.

Ask the minimum clarification required or invoke the appropriate requirements skill to resolve the ambiguity.

### 3. Requirements Gathering

Invoke the requirements skill to progressively collect the information required for the selected ML problem and pipeline architecture.

The requirements skill should update the canonical project specification.

The orchestrator should monitor specification completeness and determine when the requirements gate can be evaluated.

### 4. Canonical Project Specification

Maintain a single canonical specification throughout the workflow.

The specification should capture, as applicable:

* Project information
* Business objective
* Data
* ML problem
* Features
* Training requirements
* Inference requirements
* Pipeline requirements
* Monitoring requirements
* Retraining requirements
* Platform requirements
* Architecture decisions
* User-confirmed decisions

The specification must remain synchronized with decisions made during the workflow.

### 5. Requirements Gate

The requirements gate determines whether sufficient information exists to proceed.

If the gate fails:

```text
Requirements Gate
       |
       v
Missing Information
       |
       v
Requirements Skill
       |
       v
User Question
       |
       v
Specification Update
       |
       v
Requirements Gate
```

Do not proceed to architecture or implementation while required information remains unresolved.

### 6. ML Problem Design

Invoke the specialized ML problem skill.

The ML problem skill determines the appropriate ML approach based on:

* Problem type
* Data characteristics
* Labels
* Feature characteristics
* Business requirements
* Evaluation requirements
* Inference requirements

The resulting decisions should be recorded in or reflected by the canonical specification.

### 7. Pipeline Design

Coordinate the required pipelines.

Depending on the project, these may include:

* Data pipeline
* Training pipeline
* Inference pipeline
* Retraining pipeline
* Monitoring pipeline

Training and inference should use the same logical data transformation definition where applicable.

### 8. Architecture

Produce the logical ML/MLOps architecture based on the canonical specification and preceding design decisions.

The architecture should define:

* Major components
* Data flow
* Model flow
* Artifact flow
* Training flow
* Inference flow
* Monitoring flow
* Retraining flow where required

### 9. Platform Mapping

Map the platform-independent architecture to the selected target platform.

Platform-specific decisions should be handled by the appropriate platform adapter.

The core skills should remain independent of the target platform.

### 10. Implementation Generation

Implementation may begin only after:

* Required requirements are complete
* Requirements gate has passed
* ML design is complete
* Pipeline design is complete
* Architecture is defined
* Required platform mapping is available

The implementation should be generated from the canonical specification and approved architecture.

### 11. Implementation Validation

Validate the generated implementation against:

* Canonical project specification
* Architecture
* Pipeline requirements
* ML requirements
* Platform requirements
* Required quality checks

If validation fails, identify the appropriate stage to revisit.

```text
Implementation Validation
          |
          +---- PASS ---> COMPLETE
          |
          +---- FAIL
                  |
                  v
           Identify Failure Stage
                  |
                  v
        Return to Appropriate Stage
                  |
                  v
              Revalidate
```

## Stage Completion

Each workflow stage should have:

* Defined inputs
* Defined outputs
* Completion criteria
* Associated validation or gate

The orchestrator should not advance to the next stage until the current stage satisfies its completion criteria.

## Skill Selection

The orchestrator should select skills based on the canonical project requirements.

Example:

```text
User Request
     |
     v
Orchestrator
     |
     +---- Requirements Skill
     |
     +---- Anomaly Detection Skill
     |
     +---- Data Pipeline Skill
     |
     +---- Training Pipeline Skill
     |
     +---- Inference Pipeline Skill
     |
     +---- Platform Adapter
     |
     +---- Validation
```

Not every project requires every skill.

The selected workflow should depend on the requirements and project specification.

## Initial Supported ML Problem Types

The orchestrator should support routing for:

* Anomaly detection
* Classification
* Regression
* Forecasting
* Clustering

The first fully implemented specialized ML skill is Anomaly Detection.

## Out of Scope

The orchestrator should not:

* Contain detailed algorithm-selection logic
* Contain platform-specific implementation logic
* Replace specialized ML problem skills
* Generate implementation before required gates pass
* Independently reinterpret requirements already captured in the canonical specification
