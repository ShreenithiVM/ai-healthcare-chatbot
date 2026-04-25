import csv

def process_text_file(homeopathy_data.txt, output_csv_path, delimiter=","):
    """
    Reads a text file where each line contains a Q&A pair separated by a delimiter,
    then writes the data into a CSV file with columns 'question' and 'answer'.

    Parameters:
        input_file_path (str): Path to the input text file.
        output_csv_path (str): Path to the output CSV file.
        delimiter (str): The delimiter separating question and answer in each line.
    """
    qa_pairs = []
    
    with open(homeopathy_data.txt, "r", encoding="utf-8") as file:
        for line in file:
            # Remove any trailing newline or extra whitespace
            line = line.strip()
            if not line:
                continue

            # Split the line based on the delimiter
            parts = line.split(delimiter)
            if len(parts) < 2:
                # If there's not a valid split, you can skip or log an error.
                continue

            question = parts[0].strip()
            answer = parts[1].strip()
            qa_pairs.append({"question": question, "answer": answer})

    # Write to CSV
    with open(output_csv_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["question", "answer"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for pair in qa_pairs:
            writer.writerow(pair)

    print(f"CSV file created successfully at: {output_csv_path}")

if __name__ == "__main__":
    # Example usage:
    input_file = "homeopathy_data.txt"   # Replace with your text file path
    output_csv = "homeopathy_qa.csv"       # The CSV file to create
    process_text_file(input_file, output_csv, delimiter="|")
