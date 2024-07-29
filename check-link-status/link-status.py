import csv
import requests
import pprint


def get_status(website):
    try:
        status = requests.get(website).status_code
        return "Working" if status == 200 else "Error 404"
    except:
        return "Connection Failed!!"


def main():
    with open("sites.txt", "r") as fr:
        websites = [line.strip() for line in fr]

    web_status_dict = {website: get_status(website) for website in websites}

    pprint.pprint(web_status_dict)

    # Write results to CSV file
    with open("web_status.csv", "w", newline='') as csvfile:
        fieldnames = ["Website", "Status"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for website, status in web_status_dict.items():
            writer.writerow({"Website": website, "Status": status})

        print("Data Uploaded to CSV File!!")


if __name__ == "__main__":
    main()
