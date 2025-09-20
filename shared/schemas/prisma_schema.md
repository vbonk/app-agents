

```prisma
// This is your Prisma schema file,
// learn more about it in the docs: https://pris.ly/d/prisma-schema

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model Agent {
  id          String   @id @default(cuid())
  name        String
  description String?
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  prompts    Prompt[]
  logs       Log[]
  configs    Config[]
  metrics    Metric[]
  tools      ToolUsage[]
  datasets   Dataset[]
}

model Prompt {
  id        String   @id @default(cuid())
  agentId   String
  agent     Agent    @relation(fields: [agentId], references: [id])
  version   Int
  content   String
  createdAt DateTime @default(now())

  @@unique([agentId, version])
}

model Log {
  id        String   @id @default(cuid())
  agentId   String
  agent     Agent    @relation(fields: [agentId], references: [id])
  timestamp DateTime @default(now())
  message   String
  level     String
}

model Config {
  id        String   @id @default(cuid())
  agentId   String
  agent     Agent    @relation(fields: [agentId], references: [id])
  key       String
  value     String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@unique([agentId, key])
}

model Metric {
  id        String   @id @default(cuid())
  agentId   String
  agent     Agent    @relation(fields: [agentId], references: [id])
  name      String
  value     Float
  timestamp DateTime @default(now())
}

model ToolUsage {
  id        String   @id @default(cuid())
  agentId   String
  agent     Agent    @relation(fields: [agentId], references: [id])
  toolName  String
  timestamp DateTime @default(now())
  success   Boolean
}

model Dataset {
  id          String   @id @default(cuid())
  agentId     String
  agent       Agent    @relation(fields: [agentId], references: [id])
  name        String
  description String?
  format      String   // md, json, xml, etc.
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  embeddings Embedding[]
}

model Embedding {
  id        String   @id @default(cuid())
  datasetId String
  dataset   Dataset  @relation(fields: [datasetId], references: [id])
  vector    Float[]
  content   String
  createdAt DateTime @default(now())
}
```
