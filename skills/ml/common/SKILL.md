# Common ML Skill

## Purpose

Define ML concepts, invariants, and requirements that are common across different ML problem types.

This skill provides shared ML rules that specialized problem skills should follow unless a documented problem-specific rule overrides them.

The common ML skill is platform-independent.

## Common Concepts

### Dataset

The data used for model development, evaluation, and/or inference.

### Features

Input variables used by the model.

Feature definitions should include, where applicable:

* Feature name
* Data type
* Source column or derivation
* Transformation
* Expected value constraints
* Whether the feature is available at inference time

### Target

The variable being predicted.

A target may not exist for unsupervised problems such as anomaly detection or clustering.

### Training Data

Data used to fit the model and any learned preprocessing transformations.

### Validation Data

Data used during model development, hyperparameter selection, threshold selection, or model comparison where applicable.

Validation data must not be used to fit transformations that are intended to represent training-time preprocessing.

### Test Data

Data reserved for final evaluation where applicable.

Test data should not be used for model selection, hyperparameter tuning, or other decisions that affect the final model.

Not every ML problem requires a conventional train/validation/test split.

### Model Artifact

The trained model and associated metadata required for inference.

A model artifact may include:

* Model parameters
* Model configuration
* Model version
* Training metadata
* Feature metadata
* Dependency information
* Evaluation information

### Transformation Artifact

Learned preprocessing objects required to transform data consistently.

Examples include:

* Scalers
* Encoders
* Imputers
* Feature transformers
* Vocabulary mappings
* Other learned preprocessing objects

Transformation artifacts must be versioned or otherwise associated with the model version that uses them.

## Transformation Consistency

Training and inference must use the same logical transformation definition.

A transformation that learns parameters from data must be fitted only during the appropriate training process.

Inference must reuse the resulting transformation artifact.

### Training

```text id="2om2rj"
Raw Training Data
        |
        v
Fit Transformations
        |
        v
Persist Transformation Artifacts
        |
        v
Transform Training Data
        |
        v
Train Model
        |
        v
Persist Model + Associated Artifacts
```

### Validation

```text id="e4br6a"
Validation Data
        |
        v
Load Training-Fitted Transformations
        |
        v
Transform Validation Data
        |
        v
Evaluate Model
```

### Test

```text id="ax2gri"
Test Data
        |
        v
Load Training-Fitted Transformations
        |
        v
Transform Test Data
        |
        v
Final Evaluation
```

### Inference

```text id="y5v9as"
New Inference Data
        |
        v
Load Model-Associated Transformation Artifacts
        |
        v
Transform Inference Data
        |
        v
Load Model
        |
        v
Generate Predictions / Scores
```

## Critical Transformation Rule

Inference must never fit learned preprocessing transformations.

Incorrect:

```text id="y5k0k5"
Inference Data
     |
     v
Fit Scaler
     |
     v
Transform
     |
     v
Predict
```

Correct:

```text id="d9x4xk"
Inference Data
     |
     v
Load Training-Fitted Scaler
     |
     v
Transform
     |
     v
Predict
```

The same principle applies to all learned preprocessing components.

## Data Leakage Prevention

Data preprocessing and feature engineering must prevent information from outside the permitted training context from influencing model training.

For learned transformations:

```text id="n4g5t2"
Training Data
     |
     v
Fit Transformation
     |
     +-------------------+
     |                   |
     v                   v
Training Data       Validation/Test
     |                   |
     |                   v
     |             Apply Transformation
     |                   |
     +--------+----------+
              |
              v
          Model Evaluation
```

Validation and test data must not be used to fit training transformations.

Feature engineering must also avoid using information that would not be available at the time predictions are made.

For temporal problems, future information must not be used to construct features for earlier observations.

## Feature Consistency

The feature definition used during inference must be compatible with the definition used during training.

Consistency should be maintained for:

* Feature names
* Feature data types
* Feature meaning
* Feature derivation
* Feature ordering where relevant
* Encoding
* Scaling
* Missing-value handling
* Expected schema
* Feature availability at inference time

The inference process should detect incompatible feature or schema changes rather than silently producing invalid model input.

## Artifact Association

Model artifacts and transformation artifacts must be associated with compatible versions.

Conceptually:

```text id="lyj44u"
Model Version
     |
     +---- Model Artifact
     |
     +---- Transformation Artifact
     |
     +---- Feature Definition
     |
     +---- Training Configuration
```

Inference must not combine artifacts from incompatible model or transformation versions.

## Reproducibility

The ML workflow should capture sufficient information to reproduce or audit a model.

Where applicable, this includes:

* Dataset or dataset-version identifier
* Feature definitions
* Transformation configuration
* Model configuration
* Training configuration
* Random seed
* Model version
* Transformation version
* Code/version identifier
* Evaluation configuration

The exact storage mechanism is platform-specific and should be handled by the platform adapter.

## Model and Transformation Versioning

A model version should have an identifiable relationship with the transformation artifacts and feature definition used to produce it.

A transformation change that materially changes model input should result in an identifiable transformation version and should be evaluated for model compatibility.

## Training/Inference Contract

The training pipeline and inference pipeline must share the same logical data contract.

The contract should define, where applicable:

* Expected input schema
* Feature definitions
* Transformation sequence
* Transformation artifacts
* Model input schema
* Output schema
* Missing-value behavior
* Data type expectations

The implementation mechanism for enforcing this contract is platform-specific.

## Evaluation Principles

Evaluation strategy should be appropriate to the ML problem.

The common ML layer should not assume that every problem requires:

* Accuracy
* Precision
* Recall
* RMSE
* A conventional train/validation/test split

Specialized ML skills should define problem-appropriate evaluation requirements.

## Separation of Responsibilities

### Common ML Skill

Defines shared ML concepts, invariants, artifact relationships, and consistency rules.

### Specialized ML Skill

Defines problem-specific ML reasoning, algorithms, validation, metrics, and thresholds.

### Pipeline Skills

Define how training, inference, and data workflows execute these concepts.

### Platform Adapter

Defines how models, artifacts, datasets, and metadata are stored and managed on a specific platform.

## Boundary

The common ML skill must not:

* Select a specific algorithm for a particular ML problem
* Generate platform-specific implementation
* Define Databricks-specific services
* Replace specialized ML problem skills
* Replace pipeline orchestration logic

It establishes the shared rules that all ML problem implementations should follow.
