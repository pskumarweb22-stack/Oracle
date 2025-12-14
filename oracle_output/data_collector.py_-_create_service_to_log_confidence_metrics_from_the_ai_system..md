```markdown
# Data Collector Service

## Overview
`data_collector.py` implements a lightweight service for logging confidence metrics from AI systems. The service provides structured logging, persistence, and real-time monitoring capabilities.

## Features
- **Structured JSON logging** with timestamps and metadata
- **Multiple output backends** (console, file, database, HTTP)
- **Thread-safe operations** for concurrent access
- **Configurable retention policies** and rotation
- **Real-time metric aggregation** and summary statistics

## Installation
```bash
pip install pandas sqlalchemy requests  # Optional dependencies
```

## Quick Start
```python
from data_collector import ConfidenceLogger

# Initialize logger
logger = ConfidenceLogger(
    system_id="ai_system_v1",
    backend="file",  # Options: console, file, sqlite, postgres, http
    config_path="config/metrics_config.yaml"
)

# Log confidence metric
logger.log_confidence(
    prediction_id="pred_001",
    confidence_score=0.92,
    model_version="gpt-4",
    features={"input_length": 150, "domain": "medical"},
    metadata={"user_id": "user_123", "session_id": "sess_456"}
)

# Get summary statistics
stats = logger.get_summary(days=7)
print(f"Average confidence: {stats['mean_confidence']:.3f}")
```

## Configuration
Create `config/metrics_config.yaml`:
```yaml
logging:
  level: INFO
  format: json
  rotation:
    max_size_mb: 100
    backup_count: 5

backends:
  file:
    path: logs/confidence_metrics.jsonl
    batch_size: 100
  
  database:
    enabled: false
    url: postgresql://user:pass@localhost/ai_metrics
    table_name: confidence_logs

aggregation:
  window_minutes: 5
  metrics: [mean, p95, std, count]

alerts:
  threshold_low: 0.6
  threshold_high: 0.98
  slack_webhook: ${SLACK_WEBHOOK}
```

## API Reference

### Core Methods
```python
log_confidence(
    prediction_id: str,
    confidence_score: float,
    model_version: str,
    features: Dict = None,
    metadata: Dict = None
) -> str

get_summary(
    hours: int = 24,
    model_version: str = None
) -> Dict[str, float]

export_data(
    start_date: datetime,
    end_date: datetime,
    format: str = "csv"  # csv, json, parquet
) -> str
```

### Advanced Features
```python
# Custom aggregation
logger.add_custom_aggregator(
    name="volatility",
    func=lambda scores: np.std(scores[-100:]) if len(scores) >= 100 else None
)

# Alert rules
logger.add_alert_rule(
    condition=lambda metrics: metrics["mean_confidence"] < 0.7,
    action=SlackNotifier(),
    cooldown_minutes=30
)

# Performance monitoring
with logger.performance_monitor("inference"):
    # AI system inference code
    result = ai_model.predict(input_data)
```

## Data Schema
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "prediction_id": "pred_001",
  "system_id": "ai_system_v1",
  "model_version": "gpt-4",
  "confidence_score": 0.92,
  "features": {
    "input_length": 150,
    "domain": "medical"
  },
  "metadata": {
    "user_id": "user_123",
    "session_id": "sess_456",
    "latency_ms": 245
  }
}
```

## Deployment

### Docker
```dockerfile
FROM python:3.9-slim
COPY data_collector.py /app/
COPY config/metrics_config.yaml /app/config/
RUN pip install pandas sqlalchemy
CMD ["python", "-m", "data_collector", "--service"]
```

### Kubernetes ConfigMap
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: confidence-logger-config
data:
  metrics_config.yaml: |
    logging:
      level: INFO
    backends:
      file:
        path: /var/log/confidence_metrics.jsonl
```

## Monitoring Dashboard
```python
# Real-time visualization
logger.start_dashboard(
    port=8050,
    metrics=["confidence_score", "prediction_count"],
    refresh_seconds=10
)
```
Access at: `http://localhost:8050/dashboard`

## Testing
```python
pytest test_data_collector.py -v

# Test coverage
pytest --cov=data_collector --cov-report=html
```

## Performance
- **Throughput**: 10K+ logs/second (batch mode)
- **Latency**: <5ms per log (async mode)
- **Storage**: ~1KB per log entry
- **Memory**: <50MB for 100K entry buffer

## License
MIT License - See LICENSE file for details.
```