import requests  # Import the requests library to make HTTP requests
from bs4 import BeautifulSoup  # Import BeautifulSoup for parsing HTML
import csv  # Import csv module for writing data to a CSV file
import pandas as pd  # Import pandas for data analysis
import matplotlib.pyplot as plt  # Import matplotlib for data visualization

# Function to scrape employee data from the given URL
def scrape_employee_data(url):
    # Send an HTTP GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"❌ Failed to retrieve the page. Status Code: {response.status_code}")
        return None
    
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find the first table in the HTML page
    table = soup.find("table")
    if not table:
        print("❌ No table found on the webpage.")
        return None
    
    # Extract all rows from the table, skipping the header row
    rows = table.find_all("tr")[1:]
    
    # Initialize an empty list to store employee data
    employees = []
    
    # Loop through each row in the table and extract data
    for row in rows:
        cols = row.find_all("td")  # Find all columns (td elements) in the row
        if len(cols) == 4:  # Ensure the row has exactly 4 columns
            employees.append([
                cols[0].text.strip(),  # Employee Name
                cols[1].text.strip(),  # Job Title
                cols[2].text.strip(),  # Department
                cols[3].text.strip()   # Email Address
            ])
    
    return employees

# Function to save employee data to a CSV file
def save_to_csv(data, filename="employees.csv"):
    if not data:
        print("❌ No data to save.")
        return
    
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Employee Name", "Job Title", "Department", "Email Address"])  # Write header row
        writer.writerows(data)  # Write employee data
    
    print(f"✅ Data successfully scraped and saved to '{filename}'!")

# Function to analyze and visualize employee data
def analyze_and_visualize(data):
    if not data:
        print("❌ No data to analyze.")
        return
    
    # Load the data into a Pandas DataFrame
    df = pd.DataFrame(data, columns=["Employee Name", "Job Title", "Department", "Email Address"])
    
    # Data Analysis
    dept_counts = df["Department"].value_counts()  # Count employees per department
    job_counts = df["Job Title"].value_counts()  # Count employees per job title
    
    # Visualization - Display both graphs on the same page
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Bar Chart - Employee Count by Department
    dept_counts.plot(kind="bar", color="skyblue", edgecolor="black", ax=axes[0])
    axes[0].set_title("Number of Employees per Department")
    axes[0].set_xlabel("Department")
    axes[0].set_ylabel("Number of Employees")
    axes[0].tick_params(axis='x', rotation=45)
    
    # Pie Chart - Job Title Distribution
    job_counts.plot(kind="pie", autopct="%1.1f%%", startangle=140, colors=["lightcoral", "gold", "lightblue", "lightgreen"], ax=axes[1])
    axes[1].set_title("Job Title Distribution")
    axes[1].set_ylabel("")
    
    # Adjust layout and display the figure
    plt.tight_layout()
    plt.show()

# Main execution block
if __name__ == "__main__":
    url = "http://darkmind.uk/SCRAPESITE/employees.html"  # Define the URL to scrape data from
    employee_data = scrape_employee_data(url)  # Scrape employee data
    save_to_csv(employee_data)  # Save data to CSV
    analyze_and_visualize(employee_data)  # Perform analysis and visualization
