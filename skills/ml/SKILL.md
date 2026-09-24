# Machine Learning Skill

## Purpose

Provide ML problem-specific reasoning and design.

The ML skill determines how the identified ML problem should be approached based on the canonical project specification, data characteristics, business requirements, and operational constraints.

The ML skill produces ML design decisions. It does not generate platform-specific implementation code.

## Role in the Workflow

The ML skill operates after sufficient requirements have been collected.

```text id="1s8j1q"
User Request
     |
     v
Orchestrator
     |
     v
Requirements
     |
     v
Canonical Project Specification
     |
     v
ML Skill
     |
     v
ML Design
```

The canonical project specification is the primary input to ML reasoning.

ML design decisions should be recorded in or reflected by the canonical specification.

## Supported ML Problem Types

The framework should support:

* Anomaly Detection
* Classification
* Regression
* Forecasting
* Clustering

Additional problem types may be added later.

## Problem Selection

The orchestrator may identify a likely ML problem type for routing.

The ML skill is responsible for confirming or refining the ML problem based on the requirements.

If the problem type remains ambiguous, the ML skill should identify the minimum information required to resolve the ambiguity.

Example:

```text id="w0z3gc"
User Request
     |
     v
Likely problem: Anomaly Detection
     |
     v
Check requirements
     |
     +---- Sufficient ----> Confirm anomaly detection
     |
     +---- Ambiguous ----> Request clarification
```

The ML skill should not make a material problem-type decision without sufficient evidence.

## Problem-Specific Skills

Each ML problem type should have its own specialized skill.

Current implementation:

* Anomaly Detection

Planned:

* Classification
* Regression
* Forecasting
* Clustering

The generic ML skill provides common ML reasoning and delegates problem-specific decisions to the specialized skill.

## Responsibilities

The ML skill should determine, as applicable:

* ML problem type
* Learning paradigm
* Required data characteristics
* Feature requirements
* Candidate algorithm families
* Feasibility constraints
* Training strategy
* Validation strategy
* Evaluation metrics
* Model selection strategy
* Threshold strategy where applicable
* Model artifact requirements
* Inference requirements
* Explainability requirements where applicable

## ML Decision Process

ML decisions should follow a consistent reasoning process:

```text id="0tw4lf"
Canonical Project Specification
            |
            v
Understand ML Objective
            |
            v
Determine Learning Paradigm
            |
            v
Analyze Data Characteristics
            |
            v
Determine Candidate Algorithms
            |
            v
Apply Feasibility Constraints
            |
            v
Determine Validation Strategy
            |
            v
Determine Evaluation Metrics
            |
            v
Determine Model Selection Strategy
            |
            v
Produce ML Design
```

## Data Characteristics

The ML design should consider relevant characteristics including:

* Dataset size
* Feature count
* Numerical features
* Categorical features
* Temporal features
* Missing values
* Data quality
* Dimensionality
* Label availability
* Label quality
* Class or anomaly prevalence
* Temporal dependencies
* Expected data volume at inference
* Training frequency
* Inference frequency

Only characteristics relevant to the selected ML problem need to be evaluated.

## Algorithm Selection

Algorithm selection must use the **problem-specific option menu**.

For anomaly detection, use only the menu in `skills/ml/anamoly-detection/options.md`:

* isolation_forest, one_class_svm, lof, autoencoder, cnn, lstm, lightgbm

Show the menu to the user with a recommended default. Do not invent models outside the menu.

```text
Problem Type
     +
Data Characteristics
     +
Label availability
     |
     v
Recommended default from rules
     |
     v
Show fixed MODEL menu → user picks
     |
     v
Show fixed METRIC menu → user picks
     |
     v
Save to canonical spec
```

When a material choice depends on a user preference, present the menu and record the decision.

## Feasibility Evaluation

Candidate ML approaches should be evaluated against relevant constraints, including:

* Data compatibility
* Dataset scale
* Training cost
* Inference cost
* Inference latency
* Explainability requirements
* Accuracy or detection requirements
* Operational complexity
* Retraining requirements
* Deployment constraints

An algorithm should not be selected solely because it is theoretically appropriate if it violates known project constraints.

## Validation and Evaluation

The validation strategy should be appropriate to the ML problem and data characteristics.

The ML design should define:

* Validation approach
* Evaluation metrics
* Model selection criteria
* Threshold strategy where applicable
* Relevant business success criteria

The evaluation strategy must reflect the actual ML problem rather than defaulting to generic metrics.

## ML Design Output

The ML skill should produce a structured ML design containing, as applicable:

```text id="n5shd4"
ML Design
├── problem_type
├── learning_paradigm
├── data_requirements
├── feature_requirements
├── candidate_algorithms
├── selected_algorithm
├── selection_reason
├── training_strategy
├── validation_strategy
├── evaluation_metrics
├── threshold_strategy
├── model_artifacts
├── inference_requirements
└── explainability_requirements
```

Not every field is required for every ML problem type.

The specialized ML skill determines which fields are applicable.

## Separation of Responsibilities

The responsibilities are divided as follows:

### Orchestrator

Controls workflow and routes to the appropriate skills.

### Requirements Skill

Determines what information is required and gathers it from the user or available context.

### ML Skill

Determines the appropriate ML approach and produces ML design decisions.

### Specialized ML Skill

Provides problem-specific decision rules and requirements.

### Pipeline Skills

Determine how data, training, inference, and other pipelines should be structured.

### Platform Adapter

Determines how the platform-independent design is implemented on a specific platform.

### Validation

Validates the resulting design and implementation against the canonical specification.

## Boundary

The ML skill must not:

* Generate production implementation code
* Generate platform-specific code
* Implement Databricks-specific workflows
* Implement cloud-specific infrastructure
* Replace pipeline design skills
* Replace the requirements skill

The ML skill produces design decisions that downstream skills use for implementation.

## Example

For:

> "Detect anomalous customer transactions."

The initial ML interpretation may be:

```text
problem_type = anomaly_detection
```

The anomaly detection skill should then determine the relevant ML requirements and design decisions based on:

* Whether labels exist
* What constitutes an anomaly
* Entity definition
* Feature characteristics
* Temporal characteristics
* Expected anomaly frequency
* Inference requirements
* Business action
* Evaluation requirements

The resulting ML design should be recorded in the canonical project specification.
