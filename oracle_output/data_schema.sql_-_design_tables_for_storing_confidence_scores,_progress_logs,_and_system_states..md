```sql
-- data_schema.sql
-- Core tables for tracking AI system confidence, progress, and state management

-- ============================================
-- CONFIDENCE SCORES TABLE
-- ============================================
CREATE TABLE confidence_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id VARCHAR(255) NOT NULL,
    component VARCHAR(100) NOT NULL,
    score DECIMAL(5,4) NOT NULL CHECK (score >= 0 AND score <= 1),
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes for common query patterns
    INDEX idx_task_id (task_id),
    INDEX idx_component (component),
    INDEX idx_created_at (created_at DESC)
);

COMMENT ON TABLE confidence_scores IS 'Stores confidence scores for AI system components during task execution';
COMMENT ON COLUMN confidence_scores.score IS 'Confidence value between 0 and 1';
COMMENT ON COLUMN confidence_scores.metadata IS 'Additional context about the confidence assessment';

-- ============================================
-- PROGRESS LOGS TABLE
-- ============================================
CREATE TABLE progress_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    task_id VARCHAR(255) NOT NULL,
    stage VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('pending', 'running', 'completed', 'failed', 'retrying')),
    progress_percent INTEGER CHECK (progress_percent >= 0 AND progress_percent <= 100),
    message TEXT,
    details JSONB,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_task_id_status (task_id, status),
    INDEX idx_stage_status (stage, status),
    INDEX idx_created_at (created_at DESC)
);

COMMENT ON TABLE progress_logs IS 'Tracks execution progress through system stages';
COMMENT ON COLUMN progress_logs.details IS 'Structured data about progress state';

-- ============================================
-- SYSTEM STATES TABLE
-- ============================================
CREATE TABLE system_states (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    state_key VARCHAR(255) UNIQUE NOT NULL,
    state_value JSONB NOT NULL,
    version INTEGER DEFAULT 1,
    last_updated TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMPTZ,
    
    INDEX idx_state_key (state_key),
    INDEX idx_expires_at (expires_at)
);

COMMENT ON TABLE system_states IS 'Persistent storage for system state snapshots and configurations';
COMMENT ON COLUMN system_states.state_key IS 'Unique identifier for the state (e.g., session_id, config_name)';
COMMENT ON COLUMN system_states.expires_at IS 'Optional TTL for automatic cleanup';

-- ============================================
-- TASK METADATA TABLE (Optional Enhancement)
-- ============================================
CREATE TABLE task_metadata (
    task_id VARCHAR(255) PRIMARY KEY,
    task_type VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMPTZ,
    overall_confidence DECIMAL(5,4),
    final_status VARCHAR(50),
    
    INDEX idx_task_type_status (task_type, final_status),
    INDEX idx_created_completed (created_at, completed_at)
);

COMMENT ON TABLE task_metadata IS 'High-level task tracking and aggregation';

-- ============================================
-- FOREIGN KEY CONSTRAINTS (if needed)
-- ============================================
-- ALTER TABLE confidence_scores 
-- ADD CONSTRAINT fk_task_metadata 
-- FOREIGN KEY (task_id) REFERENCES task_metadata(task_id) ON DELETE CASCADE;

-- ALTER TABLE progress_logs 
-- ADD CONSTRAINT fk_task_metadata 
-- FOREIGN KEY (task_id) REFERENCES task_metadata(task_id) ON DELETE CASCADE;
```