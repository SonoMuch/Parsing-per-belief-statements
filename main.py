
from io_manager.file_processor import FileProcessor

def main():

    processor = FileProcessor(input_file="input.txt", output_file="output.txt")
    processor.process()
    print("Elaborazione completata.")

if __name__ == "__main__":
    main()
