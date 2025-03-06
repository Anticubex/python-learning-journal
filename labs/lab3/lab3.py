import csv
import random
import time
import datetime
import matplotlib.pyplot as plt
import os


def generate_sales_data(filename, num_records):
    """Generate random sales data"""
    products = ["Widget", "Gadget", "Thingamajig", "Doohickey"]
    start_date = datetime.date(2000, 1, 1)

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["sale_id", "sale_date", "amount", "product"])

        for sale_id in range(num_records):
            sale_date = start_date + datetime.timedelta(days=random.randint(0, 365))
            amount = round(random.uniform(50, 500), 2)
            product = random.choice(products)
            writer.writerow([sale_id, sale_date, amount, product])


def load_sales_data(filename):
    """
    Load sales data from CSV
    Runs with O(n) time complexity
    """
    sales = []
    with open(filename, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["sale_id"] = int(row["sale_id"])
            row["amount"] = float(row["amount"])
            row["sale_date"] = datetime.datetime.strptime(row["sale_date"], "%Y-%m-%d")
            sales.append(row)
    return sales


def get_latest_sale(sales):
    """
    Retrieve latest sale
    Runs with O(n) time complexity
    """
    return max(sales, key=lambda x: x["sale_date"])


def compute_total_revenue(sales):
    """
    Compute total revenue
    Runs with O(n) time complexity
    """
    return sum(sale["amount"] for sale in sales)


def check_duplicate_ids(sales):
    """
    Check for duplicate sale IDs
    Runs with O(n) time complexity
    """
    seen = set()
    duplicates = set()
    for sale in sales:
        if sale["sale_id"] in seen:
            duplicates.add(sale["sale_id"])
        seen.add(sale["sale_id"])
    return duplicates


def search_sale_by_id(sales, sale_id):
    """
    Search for a sale by ID
    Runs with O(n) time complexity
    """
    for sale in sales:
        if sale["sale_id"] == sale_id:
            return sale
    return None


def measure_performance(sales_data, operation):
    """Measure performance"""
    start_time = time.time()
    operation(sales_data)
    end_time = time.time()
    return end_time - start_time


def main():
    """The main"""
    # dataset_sizes = [100]
    dataset_sizes = [100] + list(range(1000, 100_000, 1000))
    results = {}

    for size in dataset_sizes:
        filename = f"sales_{size}.csv"
        generate_sales_data(filename, size)

        # The other operations depend on load, so we have to do this manually
        loadtime = time.time()
        sales = load_sales_data(filename)
        loadtime = time.time() - loadtime

        times = {
            "load_sale": loadtime,
            "latest_sale": measure_performance(sales, get_latest_sale),
            "total_revenue": measure_performance(sales, compute_total_revenue),
            "check_duplicates": measure_performance(sales, check_duplicate_ids),
            "search_sale": measure_performance(
                sales,
                lambda sales: search_sale_by_id(sales, random.randint(0, size - 1)),
            ),
        }
        results[size] = times
        os.remove(filename)

    # Plot results
    for operation in [
        "load_sale",
        "latest_sale",
        "total_revenue",
        "check_duplicates",
        "search_sale",
    ]:
        plt.plot(
            dataset_sizes,
            [results[size][operation] for size in dataset_sizes],
            label=operation,
        )

    plt.xlabel("Dataset Size")
    plt.ylabel("Execution Time (seconds)")
    plt.title("Performance of Sales Data Operations")
    plt.legend()
    plt.show()


# Main execution
if __name__ == "__main__":
    main()
