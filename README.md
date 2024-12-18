# Configuration Analysis Tool with AI Integration

This tool analyzes configuration files for potential issues and misconfigurations, particularly focusing on HPC cluster environments. It combines pattern-based analysis with AI-powered insights to provide comprehensive configuration reviews.

## Key Features

- Analysis of `.bashrc` files for potential module loading issues in HPC environments
- Integration with AI services (OpenAI GPT-4 and Anthropic Claude) for advanced analysis
- Pattern-based detection of common configuration issues
- Support for EasyBuild module system configurations
- Extensible to analyze other configuration files (e.g., Schrodinger hosts configurations)
- Web-based user interface for easy interaction

## Technical Stack

- Python 3.x
- Flask web framework
- BERT embeddings for pattern matching
- Pinecone vector database (local instance)
- Docker for local database deployment
- OpenAI and Anthropic APIs for AI analysis

## Prerequisites

- Python 3.x
- Docker
- pipenv
- OpenAI API key (optional, for GPT-4 integration)
- Anthropic API key (optional, for Claude integration)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd [repository-name]
```

2. Install dependencies using pipenv:
```bash
pipenv install
```

3. Set up environment variables for AI services (optional):
```bash
export OPENAI_API_KEY='your-openai-key'
export ANTHROPIC_API_KEY='your-anthropic-key'
```

## Usage

1. Start the local Pinecone database:
```bash
pipenv run run-db-image
```

2. Initialize the database with patterns:
```bash
pipenv run init-db
```

3. Start the application:
```bash
pipenv run start
```

4. Access the web interface at `http://localhost:5000`

5. To stop the database:
```bash
pipenv run stop-db-image
```

## Configuration Analysis Types

### 1. .bashrc Analysis
- Detects conda environment initialization issues
- Identifies problematic environment variable configurations
- Checks for module system compatibility problems
- Suggests best practices for HPC environments

### 2. Schrodinger.hosts Analysis (Planned)
- Validates host configurations for Schrodinger software
- Checks resource specifications
- Verifies queue configurations

## Pattern Database

The tool uses a YAML-based pattern database located in `src/ai_ga/patterns/data/patterns.yaml`. Each pattern includes:
- Pattern ID
- Description
- Severity level
- Recommendations
- Example of problematic code

## AI Integration

The tool can provide additional analysis using:
- OpenAI's GPT-4 for advanced configuration review
- Anthropic's Claude for alternative insights
- Combined analysis with pattern-matching results

## Project Structure

```
.
├── Pipfile
├── README.md
├── docker-compose.yaml
├── src
│   └── ai_ga
│       ├── analyzer/
│       ├── embeddings/
│       ├── ai_services/
│       ├── patterns/
│       │   └── data/
│       ├── storage/
│       ├── templates/
│       └── utils/
└── tests/
```

## Development

To extend the tool for new configuration types:
1. Add new patterns to `patterns.yaml`
2. Create appropriate analyzers in the `analyzer` module
3. Update AI prompts in `ai_services` if needed
4. Add new UI elements as required

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

MIT License