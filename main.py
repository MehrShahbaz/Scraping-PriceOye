from crawler import crawl
from timeit import default_timer as timer
from helper import (
    append_to_list_in_file,
    print_execution_time,
    write_in_file,
    check_duplicates,
    custom_print,
)


if __name__ == "__main__":
    time_start = timer()

    base_url = "https://priceoye.pk"

    results = crawl(base_url)

    custom_print(f"Total Products scraped {len(results)}", True)

    write_in_file(results, "data.json")

    check_duplicates()

    time_end = timer()
    print_execution_time(time_start, time_end)
    append_to_list_in_file("simple", time_end - time_start)
