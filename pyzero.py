import asyncio
import os

from dotenv import load_dotenv
from pyzerox import zerox

kwargs = {}

custom_system_prompt = None

load_dotenv()
model = "gemini/gemini-1.5-flash" ## "gemini/<gemini_model>" -> format <provider>/<model>
os.environ['GEMINI_API_KEY'] = os.getenv("LLM_MODEL_KEY") # your-gemini-api-key


# Define main async entrypoint
async def main():
    file_path = "./resume/2024-言志伟-研发简历.pdf" ## local filepath and file URL supported

    ## process only some pages or all
    select_pages = None ## None for all, but could be int or list(int) page numbers (1 indexed)
    if select_pages is None:
        select_pages = [1,2,3,4,5]
    output_dir = "./output_test" ## directory to save the consolidated markdown file
    result = await zerox(file_path=file_path, model=model, output_dir=output_dir,
                        custom_system_prompt=custom_system_prompt, select_pages=select_pages, **kwargs)
    return result

# run the main function:
result = asyncio.run(main())

# print markdown result
print(result)
