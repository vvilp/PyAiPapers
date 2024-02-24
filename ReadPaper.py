from pypdf import PdfReader
from openai import OpenAI
import glob, os


pdf_summary = {}
for file in glob.glob("papers/*.pdf"):
    reader = PdfReader(file)

    all_content = ""
    for page in reader.pages:
        text = page.extract_text()
        if "References" in text:
            all_content += text[:text.find("References")]
            break
        all_content += text

    try:
        client = OpenAI(
            api_key=os.environ.get(
                "OPENAI_API_KEY", ""
            )
        )
        messages = []
        messages.append(
            {
                "role": "user",
                "content": f"""
                        Make a summary of the given research paper. Summary should include these contents. 
                        Introduction. What does it do? how does it achieve it? whats new in this research? what are result and outcomes?
                        Your summary should be easy understand for someone who is not AI expert. Your summary should be informative and factual, covering the most important aspects of the topic. 
                        Do not start with 'Summary:'
                        paper content: {all_content}""",
            }
        )
        completion = client.chat.completions.create(
            model="gpt-4-0125-preview", messages=messages
        )
        print("---------------------------------------------")
        print(completion.choices[0].message.content)
        pdf_summary[file] = completion.choices[0].message.content
        with open("output.md", "+a", encoding="utf-8") as f:
            f.write(f"##### {os.path.basename(file).split('.')[0]} \n\n")
            f.write(completion.choices[0].message.content)
            f.write("\n\n---\n\n")
    except Exception as e:
        print(e)
