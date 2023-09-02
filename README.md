# Elasticsearch Data Indexing and Plotting

This Python script simplifies the process of indexing data into Elasticsearch and creating visualizations based on the indexed data over a specified time period. It's particularly useful for monitoring and analyzing data changes over time. The script supports two primary actions: indexing data and plotting data.

## Prerequisites

Before using the script, ensure that you have the following prerequisites:

1. **Elasticsearch**: You must have Elasticsearch installed and running on your system. Make sure to configure the Elasticsearch URL and credentials in the script (if necessary).

2. **Python and pip**: Make sure you have Python 3.x installed. You can download it from [python.org](https://www.python.org/downloads/). Additionally, you need pip, which usually comes bundled with Python.

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/elasticsearch-data-indexing.git
   cd elasticsearch-data-indexing
   ```

2. Install the required Python dependencies using `pip` and the provided `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Indexing Data

To index data into Elasticsearch, use the following command:

```bash
python main.py index
```

This command reads data from a file named `data.json` (you can customize the data source) and indexes it into Elasticsearch. You may need to configure Elasticsearch connection details in the script.

### 2. Plotting Data

To visualize data from Elasticsearch over a specific time period, use the following command:

```bash
python main.py plot <start_date> <end_date> <plot_period>
```

- `<start_date>`: The start date of the time period in the format `YYYY-MM-DD`.
- `<end_date>`: The end date of the time period in the format `YYYY-MM-DD`.
- `<plot_period>`: The period for document aggregation, e.g., `1d` for daily aggregation, `1w` for weekly, and so on.

This command generates a plot illustrating the number of documents indexed within the specified time period, aggregated according to the provided plot period, and saves it as `open_search.png`.

## Example

Here's an example of how to use the script to plot data for a weekly aggregation over a specific time period:

```bash
python main.py plot 2023-06-10 2023-06-20 1w
```

This command generates a plot displaying data aggregated weekly between June 10, 2023, and June 20, 2023.

## Configuration

You can configure the Elasticsearch URL and authentication credentials in the script by modifying the following lines:

```python
OS_CLIENT = Elasticsearch("http://localhost:9200", basic_auth=("user", "password"))
INDEX_NAME = "homework"
```

## License

This script is provided under the [MIT License](LICENSE).
