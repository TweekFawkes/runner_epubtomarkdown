import os
import sys
import argparse

### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ###

try:
    import pypandoc
except ImportError:
    print("Please install pypandoc first: pip install pypandoc")
    exit(1)

### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ###

def convert_epub_to_md_pypandoc(epub_filepath, md_filepath):
    """
    Converts an EPUB file to Markdown using the pypandoc library.

    Args:
        epub_filepath (str): Path to the input EPUB file.
        md_filepath (str): Path for the output Markdown file.

    Returns:
        bool: True if conversion was successful, False otherwise.
    """
    if not os.path.exists(epub_filepath):
        print(f"Error: Input EPUB file not found at '{epub_filepath}'")
        return False

    # Ensure the output directory exists
    output_dir = os.path.dirname(md_filepath)
    if output_dir: # Check if there's a directory part
        os.makedirs(output_dir, exist_ok=True)

    try:
        # format='epub' can often be inferred, but explicit is good.
        # 'md' is short for 'markdown'. Use 'gfm' for GitHub Flavored Markdown, etc.
        output = pypandoc.convert_file(
            source_file=epub_filepath,
            to='markdown',          # Target format
            format='epub',         # Source format (optional, often inferred)
            outputfile=md_filepath # Specify the output file path
            # extra_args=['--wrap=none'] # Optional: pass extra pandoc args
        )
        # If outputfile is specified, the return value 'output' is typically an empty string.
        assert output == "" # pypandoc returns empty string when outputfile is used
        print(f"Successfully converted '{epub_filepath}' to '{md_filepath}' using pypandoc.")
        return True

    # pypandoc raises OSError if pandoc isn't found
    except OSError as e:
         print(f"Error: pypandoc failed to run Pandoc. ({e})")
         print("Please ensure Pandoc is installed and in your system's PATH.")
         return False
    # pypandoc raises RuntimeError for Pandoc conversion errors
    except RuntimeError as e:
         print(f"Error during pypandoc conversion: {e}")
         return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ###

# --- Example Usage ---

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--epub_file', required=True, help='Input EPUB file from inputs directory')
    args = parser.parse_args()
    
    # Validate file extension
    if not args.epub_file.lower().endswith('.epub'):
        print(f"Error: Input file must be an EPUB file")
        return 1
    
    # Construct full input path
    input_path = os.path.join('inputs', args.epub_file)
    
    # Check if input file exists
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' does not exist")
        return 1

    try:
        # Create outputs directory if it doesn't exist
        os.makedirs('outputs', exist_ok=True)
        
        # Create output filename in outputs directory
        base_name = os.path.splitext(args.epub_file)[0]
        output_file = os.path.join('outputs', f"{base_name}.md")
        
        # Check if output file already exists
        if os.path.exists(output_file):
            print(f"Warning: Output file '{output_file}' already exists and will be overwritten")
        
        # Check if input file is readable
        if not os.access(input_path, os.R_OK):
            print(f"Error: Input file '{input_path}' is not readable")
            return 1
            
        # Convert SVG to PNG
        #cairosvg.svg2png(url=input_path, write_to=output_file)

        success_pypandoc = convert_epub_to_md_pypandoc(input_path, output_file)

        if success_pypandoc:
            print("EPUB to Markdown conversion finished.")
            print(f"Successfully converted {input_path} to {output_file}")
            return 0
        else:
            print("EPUB to Markdown conversion failed.")
            return 1
    except Exception as e:
        print(f"Error converting file: {str(e)}")
        return 1


### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ### --- ###

if __name__ == "__main__":
    exit(main())