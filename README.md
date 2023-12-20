# Scaffold LLM Agent

This project provides a scaffold LLM agent to help you get started with Llamaindex, Trulens, and Streamlit. It uses advanced RAG techniques (sentence-window and automerging retrieval) to create a custom agent and Trulens to evaluate the RAG. It can run either locally or in a containerized version.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Docker (for containerized version)

### Installation

1. Fork this repo.
2. Copy the `.env.example` to `.env`, then replace the placeholder with your own OpenAI API key.

#### Local Installation

1. Install the requirements: `pip install -r requirements.txt`
2. Run the application: `streamlit run chatbot.py --server.port=8502`

Note: The port 8501 is defaulted to Trulens dashboard, so we use 8502 for this application.

#### Containerized Installation

1. Run the application: `docker-compose up`

## Usage

This scaffold is a Streamlit version of the popular course by DeepLearning.ai - Building and Evaluating Advanced RAG

In the course, the instructors build a RAG using the eBook "How to build a career in AI". It's also included here in the `/data` directory.

To start working on your own,

1. Add your data to the `/data` directory (note: there's many ways to access your data through [Llamahub](https://llamahub.ai/) and the [SampleDirectoryReader](https://docs.llamaindex.ai/en/stable/examples/data_connectors/simple_directory_reader.html) documentation)
2. Update the `load_data()` function with the new path.
3. Choose the type of RAG to run. By default, it's using automerging - but you can replace it with the sentence retrieval function on line 80 in `chatbot.py`
4. Update system_prompt.py with your custom prompt!

## Debugging

By default, the RAG is cached by streamlit, as well as saved in their respective diretory. For example, auto-merging creates a new directory called `merging_index` with the `index_store.json` along with other documents. If behaviour is outdated or unexpected, delete the directory and re-run.

## License

This project is licensed under the MIT License.
