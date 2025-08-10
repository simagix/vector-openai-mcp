# Vector Search + OpenAI MCP Demo

This project demonstrates how to implement vector search using Sentence-Transformers locally and on MongoDB Atlas, followed by integrating OpenAI’s Model Context Protocol (MCP) for intelligent routing and semantic querying. For more details, see the [Gen AI & Vector Search](https://sites.google.com/simagix.com/genai-vector-search) guide.

## Table of Contents

- [Vector Search + OpenAI MCP Demo](#vector-search--openai-mcp-demo)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Setup](#setup)
  - [Environment Variables](#environment-variables)
  - [Components](#components)
    - [🔹 `load_data.py`](#-load_datapy)
    - [🔹 `sbert_vector_search.py`](#-sbert_vector_searchpy)
    - [🔹 `atlas_vector_search.py`](#-atlas_vector_searchpy)
    - [🔹 `mcp_server.py` \& `mcp_client.py`](#-mcp_serverpy--mcp_clientpy)
    - [🔹 `mcp_news_server.py`](#-mcp_news_serverpy)
    - [🔹 `openai_client.py`](#-openai_clientpy)
  - [Run Instructions](#run-instructions)
  - [Testing](#testing)
  - [License](#license)

---

## Overview

The project begins with populating data from the AG News dataset and showcases:

1. **Local Vector Search** using [Sentence-Transformers](https://www.sbert.net/)
2. **MongoDB Atlas Vector Search** using `$vectorSearch`
3. **Intent Routing via MCP** to direct user input using semantic understanding
4. **OpenAI Integration** with Azure to power a natural language interface

---

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

You can set environment variables in a `.env` file or export them in your shell. Required variables include:

- `MONGO_URL`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_ENDPOINT`
- `OPENAI_API_KEY`
- `USE_AZURE_OPENAI` (set to `true` to use Azure OpenAI)

Example for Azure OpenAI (if using `mcp_news_server.py`):

```bash
export AZURE_OPENAI_API_KEY=your_key
export AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
```

---

## Components

### 🔹 `load_data.py`

Populates the `ag_news` collection with news data for use in local and Atlas vector search.

### 🔹 `sbert_vector_search.py`

Performs vector search locally using Sentence-Transformers (`all-MiniLM-L6-v2`).

### 🔹 `atlas_vector_search.py`

Uses MongoDB Atlas's `$vectorSearch` operator to run vector search on the cloud.

### 🔹 `mcp_server.py` & `mcp_client.py`

Demonstrates a simple MCP-based server and client setup to handle tool routing using user intent.

### 🔹 `mcp_news_server.py`

Extends `mcp_server` by integrating Azure OpenAI to route user input intelligently and combine it with local vector search.

### 🔹 `openai_client.py`

Provides a unified client for querying OpenAI or Azure OpenAI models.

---

## Run Instructions

1. **Populate the database**:
   ```bash
   python load_data.py
   ```

2. **Run local vector search demo**:
   ```bash
   python sbert_vector_search.py
   ```

3. **Run Atlas vector search demo**:
   ```bash
   python atlas_vector_search.py
   ```

4. **Start the MCP server**:
   ```bash
   python mcp_server.py
   ```

5. **Send a query**:
   ```bash
   python mcp_client.py
   ```

6. **Optional**: For the AI-powered experience:
   ```bash
   python mcp_news_server.py
   ```

---

## Testing

To run all unit and integration tests:

```bash
python -m unittest discover -s tests
```

---

## License

Licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for more information.
