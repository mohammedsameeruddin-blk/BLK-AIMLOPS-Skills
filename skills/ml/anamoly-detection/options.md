# Anomaly options catalog

Fixed menus for anomaly detection.
The agent must only offer these IDs — no free-form inventing.
Mark one option **(recommended)** when asking. Save the user pick in `ml-project.yaml`.

Ask progressively (only unresolved items). Do not dump every menu at once.

---

## 1. Data source

| id | label | recommended_when |
|---|---|---|
| csv_parquet | CSV / Parquet files | local files / sample data |
| databricks_table | Databricks table (Unity Catalog) | Databricks projects |
| database | Database (SQL) | existing OLTP/warehouse |
| cloud_object_storage | Cloud object storage (S3/ADLS/GCS) | raw landing zone |
| streaming | Streaming source (Kafka / Event Hub / Kinesis) | realtime ingest |
| other | Other (describe) | only if none fit |

---

## 2. Labels

| id | label | recommended_when |
|---|---|---|
| true | Reliable anomaly/fraud labels exist | supervised path |
| false | No reliable labels (unsupervised) | most classic anomaly cases |
| partial | Weak / delayed / sparse labels | semi-supervised / eval-only |

---

## 3. Anomaly type

| id | label | recommended_when |
|---|---|---|
| point | Point — one row/event is odd | credit card txn, sensor spike |
| contextual | Contextual — odd given entity/time/context | “odd for this customer” |
| collective | Collective — a sequence/group is odd | bursts, attack sequences |

---

## 4. Entity grain (what to flag)

| id | label | example |
|---|---|---|
| transaction | Transaction / event | card swipe |
| customer | Customer / account | cardholder |
| device | Device / machine | ATM, POS, sensor |
| merchant | Merchant / location | store |
| session | Session / journey | login session |
| other | Other (user defines) | |

---

## 5. Inference mode

| id | label | recommended_when |
|---|---|---|
| batch | Batch (score table/file on schedule) | CSV, daily fraud review |
| near_realtime | Near real-time (minutes) | micro-batch / stream windows |
| realtime | Realtime / online API (seconds–ms) | payment authorization |

---

## 6. Inference frequency (if batch / near_realtime)

| id | label |
|---|---|
| hourly | Hourly |
| daily | Daily |
| weekly | Weekly |
| on_demand | On demand / manual |
| continuous | Continuous / streaming trigger |

---

## 7. Models

| id | label | needs_labels | data_shape | recommended_when |
|---|---|---|---|---|
| isolation_forest | Isolation Forest | no | tabular | unlabeled tabular (default) |
| one_class_svm | One-Class Support Vector Machine (SVM) | no | tabular | smaller tabular |
| lof | Local Outlier Factor (LOF) | no | tabular | local density outliers |
| autoencoder | Autoencoder | no | tabular_high_dim | reconstruction error |
| cnn | CNN | no | image_or_grid | spatial / image-like |
| lstm | LSTM | no | sequence_timeseries | sequences / time series |
| lightgbm | LightGBM | yes | tabular | reliable labels |

---

## 8. Metrics (primary + optional secondary)

| id | label | needs_labels | role |
|---|---|---|---|
| precision | Precision | yes | primary/secondary |
| recall | Recall | yes | primary/secondary |
| f1 | F1 score | yes | primary/secondary |
| pr_auc | PR-AUC | yes | primary (recommended if labeled) |
| roc_auc | ROC-AUC | yes | primary/secondary |
| precision_at_k | Precision@K | partial | primary (recommended if unlabeled + known cases) |
| expert_review_hit_rate | Expert review hit rate | no | primary if fully unlabeled |
| score_stability | Score stability | no | secondary |
| anomaly_score_distribution | Anomaly score distribution | no | always log |
| false_positive_rate | False positive rate | yes | secondary |
| alert_volume | Alert volume / day | no | operational secondary |

---

## 9. Threshold strategy

| id | label | recommended_when |
|---|---|---|
| quantile | Quantile of anomaly scores (e.g. top 1%/5%) | unlabeled default |
| contamination | Model contamination rate | Isolation Forest / LOF style |
| f1_optimal | Threshold that maximizes F1 on validation | labeled |
| business_cost | Cost-based (FP vs FN cost) | business costs known |
| fixed | Fixed score cutoff | policy-driven |
| top_k | Top-K alerts per day/hour | limited review capacity |

---

## 10. Train / validation split

| id | label | recommended_when |
|---|---|---|
| random | Random split | i.i.d. tabular, no strong time leak risk |
| temporal | Time-based split | transactions / sensors with time |
| entity | Entity holdout (e.g. hold out customers) | generalize to new entities |
| none_unsupervised | No classic split; score stability / expert review | fully unlabeled |

---

## 11. Feature strategy

| id | label | recommended_when |
|---|---|---|
| raw | Raw columns only | simple baselines |
| aggregated | Aggregates (sums/counts/means) | entity behavior |
| rolling_window | Rolling / sliding windows | time series, velocity |
| entity_relative | Vs own history (customer baseline) | contextual anomalies |
| sequence | Sequence / ordered windows | LSTM / collective |
| mixed | Mix of raw + derived (recommended default) | most production cases |

---

## 12. Explainability

| id | label | recommended_when |
|---|---|---|
| none | Not required | pure scoring |
| top_features | Top contributing features | fraud review teams |
| shap | SHAP / model explanations | regulated / high scrutiny |
| rule_overlay | Rules + model score | ops wants interpretable reasons |

---

## 13. Action on alert

| id | label |
|---|---|
| review_queue | Send to human review queue |
| auto_block | Auto-block / decline transaction |
| notify_only | Notify / email / Slack only |
| score_only | Write score to table; downstream decides |
| step_up_auth | Trigger step-up authentication |

---

## 14. Monitoring

| id | label | recommended_when |
|---|---|---|
| basic | Data quality + score distribution | minimum (recommended start) |
| drift | + Feature / data drift | production ongoing |
| performance | + Precision/recall when labels arrive | labeled feedback loop |
| full | Quality + drift + performance + alert volume | mature MLOps |

---

## 15. Retraining trigger

| id | label | recommended_when |
|---|---|---|
| manual | Manual only | early stage |
| schedule | Fixed schedule (e.g. weekly) | stable batch systems |
| drift | On drift alert | changing behavior |
| performance_drop | On metric drop | labels available |
| new_labels | When new labels arrive | supervised / feedback |

---

## 16. Platform

| id | label | recommended_when |
|---|---|---|
| local | Local Python / files | demo / TEST folders |
| databricks | Databricks | lakehouse / UC / Jobs |
| aws | AWS (SageMaker / etc.) | AWS-standard orgs |
| azure | Azure ML | Azure-standard orgs |
| gcp | GCP Vertex | GCP-standard orgs |

---

## 17. Expected anomaly rate (contamination / alert rate)

| id | label |
|---|---|
| 0.001 | ~0.1% |
| 0.01 | ~1% (common fraud-ish default) |
| 0.05 | ~5% |
| 0.10 | ~10% |
| custom | Custom (user provides number) |

---

## Ask order (progressive)

```text
1. data_source
2. labels
3. anomaly_type
4. entity_grain
5. inference_mode (+ frequency if batch/near_realtime)
6. model
7. primary_metric (+ optional secondary)
8. threshold_strategy
9. split_strategy
10. feature_strategy
11. explainability
12. action_on_alert
13. monitoring
14. retraining_trigger
15. platform
16. expected_anomaly_rate
```

Skip any item already known or reliably derived.
Always save each answer into the canonical spec before asking the next.
