# Anomaly Detection Skill

## Purpose

Design an anomaly detection solution based on the canonical project specification, business definition, data characteristics, and operational requirements.

This skill provides anomaly-detection-specific reasoning and design decisions.

It does not generate platform-specific implementation code.

## Inputs and Outputs

### Input

The primary input is the canonical ML project specification.

The skill should use:

* Business objective
* Dataset information
* Entity definition
* Timestamp information
* Feature definitions
* Label availability
* Inference requirements
* Business action
* Operational constraints

### Output

The skill should produce an anomaly detection design containing, as applicable:

```text id="v09bq1"
Anomaly Detection Design
├── anomaly_definition
├── observation_definition
├── entity_definition
├── anomaly_type
├── temporal_context
├── label_strategy
├── feature_strategy
├── candidate_algorithms
├── selected_algorithm
├── training_strategy
├── validation_strategy
├── threshold_strategy
├── inference_output
└── explanation_strategy
```

The resulting decisions should be recorded in or reflected by the canonical project specification.

## Problem Definition

Anomaly detection identifies observations or patterns that differ materially from expected behavior.

The definition of an anomaly must be specific to the business context.

Before selecting an algorithm, determine:

* What constitutes an observation
* What entity is being analyzed
* What constitutes abnormal behavior
* What normal behavior means
* What baseline is used
* Whether context changes the definition of normal
* Whether the anomaly is a point, contextual, or collective event
* What business action follows detection

The skill should not treat "unusual" as a sufficient anomaly definition.

## Anomaly Definition

The anomaly definition should answer:

```text id="1x2qk4"
What is being observed?
        +
Who or what does it belong to?
        +
What is considered normal?
        +
What makes it abnormal?
        +
Over what context or time period?
        +
What action should occur?
```

Example:

```text id="lq9j4p"
Observation:
Individual customer transaction

Entity:
Customer

Normal behavior:
Customer's historical transaction behavior

Anomaly:
Transaction materially deviates from the customer's expected behavior

Action:
Send transaction for review
```

## Anomaly Types

Determine whether the use case is primarily:

### Point Anomaly

An individual observation is anomalous relative to the expected distribution.

Example:

A transaction with an unusually large amount.

### Contextual Anomaly

An observation is anomalous given its context.

Context may include:

* Entity
* Time
* Location
* Season
* User behavior
* Historical behavior
* Other contextual variables

Example:

A transaction amount may be normal across the population but unusual for a specific customer.

Contextual anomalies may require derived historical or temporal features.

### Collective Anomaly

A group or sequence of observations is anomalous even when individual observations may not be anomalous independently.

Example:

A sequence of transactions indicates unusual behavior.

Collective anomalies may require:

* Sequence information
* Windowed features
* Aggregations
* Event ordering
* Temporal modeling

## Decision Flow

The anomaly detection design should follow this process:

```text id="xjgj4m"
Business Definition
        |
        v
Observation + Entity
        |
        v
Temporal / Contextual Requirements
        |
        v
Label Assessment
        |
        v
Anomaly Type
        |
        v
Feature Characteristics
        |
        v
Candidate Algorithms
        |
        v
Feasibility Evaluation
        |
        v
Training Strategy
        |
        v
Validation Strategy
        |
        v
Threshold Strategy
        |
        v
Inference Output
```

## Required Information

Before finalizing the anomaly detection design, determine the information required by the selected approach.

Common requirements include:

* Anomaly definition
* Observation definition
* Entity being analyzed
* Timestamp, if applicable
* Available features
* Feature availability at inference time
* Whether anomaly labels exist
* Label quality and coverage where applicable
* Expected anomaly frequency
* Batch or real-time inference
* Expected output
* Business action after detecting an anomaly

Additional requirements should be introduced when triggered by the use case.

## Entity Definition

Determine the entity to which anomalies should be associated.

Examples:

* Customer
* Transaction
* Device
* Account
* Machine
* Location
* Other business entity

If multiple candidate entity columns exist, do not silently choose one when the decision has business meaning.

## Temporal and Contextual Analysis

Determine whether anomaly detection depends on:

* Absolute time
* Time of day
* Day of week
* Seasonality
* Historical entity behavior
* Rolling windows
* Recent event history
* Event sequences

When contextual or collective anomalies are required, the feature strategy should capture the necessary context.

## Labels

Determine whether reliable anomaly labels exist.

### No reliable labels

Potential approaches include:

* Unsupervised anomaly detection
* Semi-supervised approaches
* One-class approaches
* Statistical approaches

The skill should also determine whether the training data is expected to contain mostly normal observations.

### Reliable anomaly labels

Supervised classification may be appropriate when:

* Labels represent the desired business outcome
* Label quality is sufficient
* Label coverage is sufficient
* The label definition is consistent
* The class imbalance can be handled appropriately

The presence of a label column alone does not guarantee that supervised learning is appropriate.

### Label Assessment

Where labels exist, consider:

* Label definition
* Label quality
* Label coverage
* Recency
* Class imbalance
* Label delay
* Consistency over time

## Feature Strategy

Features should reflect the anomaly definition.

Consider:

* Raw features
* Aggregated features
* Historical features
* Rolling-window features
* Frequency/velocity features
* Entity-relative features
* Temporal features
* Contextual features

For contextual anomalies, features should capture the context against which abnormality is evaluated.

For collective anomalies, features should preserve the relevant sequence or window information.

Features must be available at inference time and must not introduce future information.

## Candidate Algorithms

Potential algorithm families include:

* Isolation Forest
* Local Outlier Factor
* One-Class SVM
* Autoencoder-based methods
* Statistical methods
* Supervised classification methods where reliable labels support that approach

Algorithm selection must consider:

* Dataset size
* Feature types
* Dimensionality
* Label availability and quality
* Expected anomaly ratio
* Training cost
* Inference cost
* Latency requirements
* Explainability requirements
* Temporal/contextual requirements
* Operational complexity

Do not select an algorithm solely because it is commonly used.

## Algorithm Selection Rules

Use the following general decision logic:

```text id="7x0vpp"
Reliable anomaly labels?
        |
        +-- Yes
        |     |
        |     v
        |  Evaluate supervised classification
        |
        +-- No
              |
              v
      Mostly-normal training data?
              |
              +-- Yes
              |     |
              |     v
              |  Consider one-class /
              |  semi-supervised approaches
              |
              +-- No
                    |
                    v
               Evaluate unsupervised
               anomaly detection
```

This is a starting decision framework. Specialized constraints may narrow the candidate set further.

If multiple materially different approaches remain feasible, present the options and record the user's decision rather than making an arbitrary selection.

## Training Strategy

Determine, as applicable:

* Training data window
* Whether training data is expected to be mostly normal
* Whether known anomalies should be excluded
* Global versus entity-specific modeling
* Temporal split strategy
* Retraining frequency
* Feature availability during training
* Training data version

Training transformations must follow the common ML transformation rules.

## Validation Strategy

Validation must be appropriate to the anomaly detection problem.

### Labeled data

Where reliable labels are available, consider metrics such as:

* Precision
* Recall
* F1
* Precision-recall analysis
* Confusion-matrix-based measures
* Business-specific cost measures

Metric selection should reflect the business cost of false positives and false negatives.

### Unlabeled data

When reliable labels are unavailable, define an alternative validation strategy.

Possible approaches include:

* Historical known incidents
* Expert review
* Injected or synthetic anomalies where appropriate
* Temporal holdout analysis
* Stability analysis
* Score distribution analysis
* Comparison with established business rules

The selected validation method should be justified by the use case.

## Threshold Strategy

Anomaly scores must be converted into actionable anomaly decisions where required.

Potential threshold strategies include:

* Fixed threshold
* Quantile-based threshold
* Validation-based threshold
* Business-defined threshold
* Algorithm-specific threshold

Threshold selection should consider:

* Expected anomaly frequency
* False-positive cost
* False-negative cost
* Operational review capacity
* Business action
* Validation results

The threshold is part of the model/inference configuration and should be versioned appropriately.

## Inference Output

The inference pipeline should generally produce, as applicable:

* Entity identifier
* Observation identifier
* Timestamp
* Anomaly score
* Anomaly flag
* Model version
* Transformation/model version
* Relevant explanation or contributing features where supported

The output schema should be defined in the canonical project specification.

## Explanation Strategy

Where explanations are required, determine what information can be reliably provided by the selected method.

Possible outputs may include:

* Contributing features
* Feature deviations
* Reference statistics
* Nearest-neighbor context
* Reconstruction error components
* Other method-specific explanations

Do not claim explanations that the selected model cannot reliably support.

## Common ML Rules

This skill inherits the common ML requirements for:

* Transformation consistency
* Training-fitted preprocessing
* Data leakage prevention
* Feature consistency
* Artifact association
* Reproducibility
* Model and transformation versioning

The anomaly detection skill should extend these rules rather than redefine them.

## Separation of Responsibilities

### Requirements Skill

Determines what information is required and gathers it.

### Common ML Skill

Defines shared ML concepts and invariants.

### Anomaly Detection Skill

Determines anomaly-specific ML requirements and design decisions.

### Pipeline Skills

Determine how data, training, inference, and other workflows are structured.

### Platform Adapter

Determines how the design is implemented on a specific platform.

## Restrictions

This skill must not:

* Contain platform-specific implementation instructions
* Generate final project code
* Generate Databricks-specific code
* Generate cloud-specific infrastructure
* Replace the requirements skill
* Replace pipeline design
* Override common ML invariants without an explicit problem-specific reason
