```yaml
# config.yaml
# Application Configuration for Data Monitoring System

# ============================================
# DATA SOURCES CONFIGURATION
# ============================================
data_sources:
  # Database connections
  databases:
    primary_db:
      type: postgresql
      host: localhost
      port: 5432
      database: analytics_db
      username: ${DB_USER}
      password: ${DB_PASSWORD}
      ssl_mode: require
      connection_timeout: 30
      max_connections: 20

    backup_db:
      type: mysql
      host: backup.example.com
      port: 3306
      database: backup_data
      username: backup_user
      password: ${BACKUP_PASSWORD}
      ssl_enabled: true

  # API endpoints
  apis:
    weather_api:
      url: https://api.weather.com/v3
      api_key: ${WEATHER_API_KEY}
      timeout: 10
      retry_attempts: 3

    stock_api:
      url: https://api.finance.com/quotes
      api_key: ${STOCK_API_KEY}
      rate_limit: 100  # requests per minute

  # File system sources
  files:
    log_directory: /var/log/applications
    data_directory: /data/exports
    archive_directory: /data/archives

# ============================================
# UPDATE INTERVALS (in seconds)
# ============================================
update_intervals:
  realtime:
    sensor_data: 5
    system_metrics: 10
    user_activity: 30

  hourly:
    aggregated_stats: 3600
    report_generation: 3600

  daily:
    database_backup: 86400
    data_cleanup: 86400
    email_reports: 86400

  weekly:
    analytics_refresh: 604800
    system_maintenance: 604800

# ============================================
# THRESHOLD CONFIGURATION
# ============================================
thresholds:
  # System performance thresholds
  system:
    cpu_usage:
      warning: 70
      critical: 90
    memory_usage:
      warning: 75
      critical: 90
    disk_usage:
      warning: 80
      critical: 95
    response_time:
      warning: 2000  # milliseconds
      critical: 5000

  # Application-specific thresholds
  application:
    error_rate:
      warning: 1.0    # percentage
      critical: 5.0
    active_users:
      minimum: 100
      expected: 1000
    transaction_volume:
      warning_low: 100
      warning_high: 10000
      critical_low: 50
      critical_high: 15000

  # Data quality thresholds
  data_quality:
    completeness:
      minimum: 98.0  # percentage
    accuracy:
      minimum: 99.5
    freshness:
      maximum_age: 300  # seconds

# ============================================
# NOTIFICATION SETTINGS
# ============================================
notifications:
  email:
    enabled: true
    smtp_server: smtp.example.com
    smtp_port: 587
    sender: alerts@system.com
    recipients:
      - admin@example.com
      - ops@example.com
    send_on:
      - critical
      - warning

  slack:
    enabled: true
    webhook_url: ${SLACK_WEBHOOK}
    channel: "#system-alerts"
    notify_on: critical

  pagerduty:
    enabled: false
    integration_key: ${PAGERDUTY_KEY}
    escalation_policy: "ops-team"

# ============================================
# LOGGING CONFIGURATION
# ============================================
logging:
  level: INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
  file_path: /var/log/monitoring/app.log
  max_size: 10485760  # 10MB
  backup_count: 5
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ============================================
# GENERAL SETTINGS
# ============================================
general:
  environment: production  # development, staging, production
  timezone: UTC
  enable_telemetry: true
  debug_mode: false
  maintenance_window:
    start: "02:00"
    end: "04:00"
    days: ["Saturday"]
```

## Usage Notes

1. **Environment Variables**: Replace `${VARIABLE_NAME}` with actual values or set as environment variables
2. **Validation**: All numeric thresholds should be validated on application startup
3. **Hot Reload**: Configuration supports hot-reload when `enable_hot_reload: true` is set
4. **Comments**: Remove comments in production for performance and security
5. **Security**: Never commit sensitive data - use environment variables or secret management systems

## Best Practices

- Use separate configuration files for different environments
- Implement configuration validation on application startup
- Regularly review and update thresholds based on system behavior
- Monitor configuration changes through version control
- Consider using configuration management tools for production deployments

---

*Last Updated: $(date)*  
*Version: 1.0.0*  
*Maintainer: System Operations Team*
```