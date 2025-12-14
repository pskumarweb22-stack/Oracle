```yaml
openapi: 3.0.3
info:
  title: Data Platform API
  version: 1.0.0
  description: |
    API for data ingestion, retrieval, and aggregation.
    Supports structured and semi-structured data processing.

servers:
  - url: https://api.dataplatform.com/v1
    description: Production server

paths:
  # --- DATA INGESTION ENDPOINTS ---
  /ingest/batch:
    post:
      summary: Ingest batch data
      description: Upload structured data in bulk (JSON, CSV, or Parquet format)
      requestBody:
        required: true
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                file:
                  type: string
                  format: binary
                  description: Data file (max 1GB)
                dataset_id:
                  type: string
                  description: Target dataset identifier
                schema_validation:
                  type: boolean
                  default: true
                  description: Enable schema validation
      responses:
        '202':
          description: Batch accepted for processing
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/JobResponse'
        '400':
          $ref: '#/components/responses/BadRequest'

  /ingest/stream:
    post:
      summary: Stream real-time data
      description: Push individual records or small batches via WebSocket or HTTP streaming
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/StreamPayload'
      responses:
        '200':
          description: Data successfully ingested
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/IngestionAck'
        '429':
          $ref: '#/components/responses/RateLimit'

  # --- DATA RETRIEVAL ENDPOINTS ---
  /data/{dataset_id}:
    get:
      summary: Retrieve dataset records
      description: Fetch data with filtering, pagination, and field selection
      parameters:
        - $ref: '#/components/parameters/DatasetId'
        - $ref: '#/components/parameters/Filter'
        - $ref: '#/components/parameters/Fields'
        - $ref: '#/components/parameters/Page'
        - $ref: '#/components/parameters/Limit'
      responses:
        '200':
          description: Successful retrieval
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DataResponse'
        '404':
          $ref: '#/components/responses/NotFound'

  /data/{dataset_id}/{record_id}:
    get:
      summary: Retrieve single record
      description: Fetch specific record by identifier
      parameters:
        - $ref: '#/components/parameters/DatasetId'
        - $ref: '#/components/parameters/RecordId'
      responses:
        '200':
          description: Record found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Record'
        '404':
          $ref: '#/components/responses/NotFound'

  # --- AGGREGATION ENDPOINTS ---
  /aggregate/{dataset_id}:
    post:
      summary: Perform data aggregation
      description: Execute aggregation queries (group by, count, sum, avg, etc.)
      parameters:
        - $ref: '#/components/parameters/DatasetId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AggregationQuery'
      responses:
        '200':
          description: Aggregation results
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AggregationResult'
        '400':
          $ref: '#/components/responses/BadRequest'

  /aggregate/materialized/{view_id}:
    get:
      summary: Retrieve materialized view
      description: Fetch pre-computed aggregation results
      parameters:
        - name: view_id
          in: path
          required: true
          schema:
            type: string
          description: Materialized view identifier
        - $ref: '#/components/parameters/Refresh'
      responses:
        '200':
          description: Materialized view data
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MaterializedView'

components:
  parameters:
    DatasetId:
      name: dataset_id
      in: path
      required: true
      schema:
        type: string
      description: Dataset identifier
    RecordId:
      name: record_id
      in: path
      required: true
      schema:
        type: string
      description: Record identifier
    Filter:
      name: filter
      in: query
      required: false
      schema:
        type: string
      description: JSON filter expression
    Fields:
      name: fields
      in: query
      required: false
      schema:
        type: string
      description: Comma-separated field list
    Page:
      name: page
      in: query
      required: false
      schema:
        type: integer
        default: 1
        minimum: 1
    Limit:
      name: limit
      in: query
      required: false
      schema:
        type: integer
        default: 100
        maximum: 1000
    Refresh:
      name: refresh
      in: query
      required: false
      schema:
        type: boolean
        default: false
      description: Force refresh materialized view

  schemas:
    JobResponse:
      type: object
      properties:
        job_id:
          type: string
        status:
          type: string
          enum: [accepted, processing, completed, failed]
        estimated_completion:
          type: string
          format: date-time

    StreamPayload:
      type: object
      properties:
        dataset_id:
          type: string
        records:
          type: array
          items:
            type: object
        timestamp:
          type: string
          format: date-time

    IngestionAck:
      type: object
      properties:
        success:
          type: boolean
        ingested_count:
          type: integer
        failed_count:
          type: integer
        errors:
          type: array
          items:
            type: string

    DataResponse:
      type: object
      properties:
        data:
          type: array
          items:
            type: object
        pagination:
          $ref: '#/components/schemas/Pagination'

    Record:
      type: object
      additionalProperties: true

    AggregationQuery:
      type: object
      properties:
        dimensions:
          type: array
          items:
            type: string
        metrics:
          type: array
          items:
            type: object
            properties:
              field:
                type: string
              operation:
                type: string
                enum: [count, sum, avg, min, max, distinct]
        filters:
          type: array
          items:
            type: object
        time_range:
          $ref: '#/components/schemas/TimeRange'

    AggregationResult:
      type: object
      properties:
        results:
          type: array
          items:
            type: object
        query_metadata:
          $ref: '#/components/schemas/QueryMetadata'

    MaterializedView:
      type: object
      properties:
        view_id:
          type: string
        data:
          type: array
          items:
            type: object
        last_refreshed:
          type: string
          format: date-time
        refresh_interval:
          type: string

    Pagination:
      type: object
      properties:
        total:
          type: integer
        page:
          type: integer
        limit:
          type: integer
        next_cursor:
          type: string

    TimeRange:
      type: object
      properties:
        start:
          type: string
          format: date-time
        end:
          type: string
          format: date-time

    QueryMetadata:
      type: object
      properties:
        execution_time_ms:
          type: integer
        scanned_records:
          type: integer
        cache_hit:
          type: boolean

  responses:
    BadRequest:
      description: Invalid request parameters or payload
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string
              details:
                type: array
                items:
                  type: string

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string
              resource:
                type: string

    RateLimit:
      description: Rate limit exceeded
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string
              retry_after:
                type: integer
```

**Key Design Principles:**
1. **Separation of Concerns** - Clear distinction between ingestion, retrieval, and aggregation
2. **Scalability** - Supports both batch and streaming ingestion patterns
3. **Flexibility** - Parameterized queries with filtering and field selection
4. **Performance** - Materialized views for pre-computed aggregations
5. **Observability** - Metadata included in all responses for debugging and monitoring

**Authentication & Authorization:** (To be implemented per deployment requirements)
- API keys via `X-API-Key` header
- OAuth2.0 for user-specific operations
- Dataset-level access controls

**Rate Limits:** (Configurable per endpoint)
- Batch ingestion: 100 requests/minute
- Streaming: 1000 records/second
- Retrieval: 1000 requests/minute
- Aggregation: 100 requests/minute
```