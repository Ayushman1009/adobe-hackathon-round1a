Adobe Hackathon: PDF Outline Extractor (Round 1A)
This project is a solution for Round 1A of the Adobe India Hackathon, "Connecting the Dots." The goal is to create a system that automatically extracts a structured outline (Title, H1, H2, H3) from a given PDF document.

Our Approach
To meet the strict performance and resource constraints (≤10 seconds execution, ≤200MB model, CPU-only, offline), we opted for a lightweight, rule-based approach instead of a heavy machine learning model. Our solution uses the powerful PyMuPDF library to analyze the intrinsic properties of the text within the PDF.

The core logic works as follows:

PDF Parsing: The script first opens the PDF and iterates through every text element on every page.

Style Analysis: For each piece of text, we extract key properties: font size, font name, and whether the font is bold.

Baseline Identification: We identify the most common font size in the document, which we assume to be the standard paragraph text size. This creates a dynamic baseline for each unique PDF.

Heading Detection: Any text that is significantly larger than the baseline paragraph text is considered a potential heading. We also give weight to bolded text, as this is a common characteristic of headings.

Title Extraction: The title is identified using a simple but effective heuristic: it's typically the text with the largest font size found within the first two pages of the document.

Hierarchical Classification (H1, H2, H3): After identifying all potential headings, we group them by their font sizes. The largest font size is classified as H1, the second-largest as H2, and the third-largest as H3. This allows the system to adapt to the specific styling of any PDF.

JSON Output: Finally, the extracted title and the sorted list of headings (ordered by page number) are formatted into the required JSON structure and saved to a file.

This method is not only fast and efficient but also surprisingly accurate across a wide variety of document layouts.

Libraries & Dependencies
Python 3.9

PyMuPDF (fitz): The core library used for all PDF parsing and text extraction. It is known for its high performance and detailed output.

How to Build and Run the Solution
The entire solution is containerized using Docker for easy and consistent execution.

Prerequisites:

Docker must be installed and running on your system.

Instructions:

Place Input PDF: Put the PDF file you want to process (e.g., sample.pdf) into the input/ directory in the project root.

Build the Docker Image: Open a terminal in the project's root directory and run the following command. This will build the Docker image with the tag pdf-outline-extractor.

docker build --platform linux/amd64 -t pdf-outline-extractor .

Run the Container: After the image is built successfully, run the following command. This will start the container, which will automatically process any PDFs in the input directory and save the resulting .json files to the output directory.

docker run --rm -v "$(pwd)/input:/app/input" -v "$(pwd)/output:/app/output" --network none pdf-outline-extractor

-v "$(pwd)/input:/app/input": Mounts the local input directory to the container's /app/input directory.

-v "$(pwd)/output:/app/output": Mounts the local output directory to the container's /app/output directory, where the results will be saved.

--rm: Automatically removes the container after it finishes execution.

--network none: Ensures the container runs offline, as per the rules.

After the command completes, the output directory will contain the JSON file with the extracted document structure.#   a d o b e - h a c k a t h o n - r o u n d 1 a  
 