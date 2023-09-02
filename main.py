import json
import sys

from elasticsearch import helpers
import matplotlib.pyplot as plt
import config


def init_elasticsearch():
    """
    Set up an ElasticSearch index if it does not exist yet.
    """

    if config.OS_CLIENT.indices.exists(index=config.INDEX_NAME):
        return

    print("Creating ElasticSearch index")
    config.OS_CLIENT.indices.create(index=config.INDEX_NAME, body={
        "mappings": {
            "properties": {
                "index_time": {
                    "type": "date"
                },
                "id": {
                    "type": "keyword"
                }
            }
        }
    })


def index_data():
    """
    Load data into ElasticSearch, use bulk indexing to improve speed and performance.
    """

    with open("data.json") as data_file:
        data = json.load(data_file)

    # Prepare indexing actions for bulk indexing
    actions = []
    for log in data:
        action = {
            "_op_type": "index",
            "_index": config.INDEX_NAME,
            "_source": log
        }
        actions.append(action)

    # Use ElasticSearch bulk API for efficient indexing
    success, _ = helpers.bulk(config.OS_CLIENT, actions)
    print(f"Indexed {success} documents")


def plot_data(start_date, end_date, plot_period):
    """
    Plot the data from ElasticSearch based on its infection_time. The function accepts an arbitrary time period.

    Args:
        start_date (str): Start date of the time period (YYYY-MM-DD).
        end_date (str): End date of the time period (YYYY-MM-DD).
        plot_period (str): Period of document aggregation e.g. 1d
    """

    aggregation_query = {
        "size": 0,
        "query": {
            "range": {
                "index_time": {
                    "gte": start_date,
                    "lte": end_date
                }
            }
        },
        "aggs": {
            "documents_per_day": {
                "date_histogram": {
                    "field": "index_time",
                    "calendar_interval": plot_period,
                    "format": "yyyy-MM-dd",
                },
            }
        },
    }

    response = config.OS_CLIENT.search(index=config.INDEX_NAME, body=aggregation_query)

    # Extract data from the aggregation response
    aggregations = response["aggregations"]["documents_per_day"]["buckets"]

    dates = [con["key_as_string"] for con in aggregations]
    counts = [con["doc_count"] for con in aggregations]

    # Create a plot using Matplotlib
    plt.figure(figsize=(10, 6))
    plt.bar(dates, counts)
    plt.xlabel("Date")
    plt.ylabel("Number of Documents Indexed")
    plt.title("Indexed Documents Over Time")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('open_search.png')
    # Display the plot
    plt.show()


def main():
    init_elasticsearch()

    # Parse command-line arguments
    action = sys.argv[1]

    # Perform action based on user input
    if action == "index":
        index_data()
    elif action == "plot":
        # Ensure proper command-line arguments
        if len(sys.argv) < 4:
            print("Usage: python main.py <action> <start_date> <end_date> <period>")
            sys.exit(1)
        start_date = sys.argv[2]
        end_date = sys.argv[3]
        plot_period = sys.argv[4]
        # Plot data
        plot_data(start_date, end_date, plot_period)


if __name__ == "__main__":
    main()
