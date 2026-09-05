# Architecture

```mermaid
flowchart LR
    A[Streamlit Event Producer] --> B[Amazon Kinesis Data Streams]
    B --> C[AWS Lambda]
    B --> D[Amazon Data Firehose]
    C --> E[Amazon RDS MariaDB]
    D --> F[Amazon S3]
    C --> G[Amazon CloudWatch Logs]
```

## Network

Lambda and RDS are deployed in the same VPC.

```text
VPC
├── Lambda
│   └── datastory_SG
│       └── TCP 3306
│
└── RDS MariaDB
    └── default Security Group
        └── inbound TCP 3306 from Lambda SG
```
