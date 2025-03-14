# import base64
# import zlib
# import os

# def encode_plantuml(content):
#     compressed = zlib.compress(content.encode('utf-8'))
#     encoded = base64.b64encode(compressed).decode('utf-8')
#     return encoded

# def generate_plantuml_url(content):
#     encoded = encode_plantuml(content)
#     return f"https://www.plantuml.com/plantuml/png/{encoded}"

# def generate_markdown(diagrams_folder, output_file):
#     markdown_content = "# Diagrams \n\n"
#     for filename in os.listdir(diagrams_folder):
#         if filename.endswith(".puml"):
#             with open(os.path.join(diagrams_folder, filename), "r") as file:
#                 content = file.read()
#                 url = generate_plantuml_url(content)
#                 markdown_content += f"## {filename}\n\n![{filename}]({url})\n\n"
#     with open(output_file, "w") as file:
#         file.write(markdown_content)

# if __name__ == "__main__":
#     generate_markdown("docs", "diagrams.md")

import base64
import zlib
import os

def encode_plantuml(content):
    if not content.strip().startswith("@startuml"):
        content = "@startuml\n" + content
    if not content.strip().endswith("@enduml"):
        content = content + "\n@enduml"

    # pack by zlib (algorithm DEFLATE)
    compressed = zlib.compress(content.encode("utf-8"))

    # coding to base64
    encoded = base64.b64encode(compressed).decode("utf-8")

    # Add prefix ~1 for PlantUML Server
    encoded = "~1" + encoded

    return encoded

def generate_plantuml_url(content):
    encoded = encode_plantuml(content)
    return f"https://www.plantuml.com/plantuml/png/{encoded}"

def generate_markdown(diagrams_folder, output_file):
    markdown_content = "# Diagrams\n\n"
    for filename in os.listdir(diagrams_folder):
        if filename.endswith(".puml"):
            with open(os.path.join(diagrams_folder, filename), "r") as file:
                content = file.read()
                url = generate_plantuml_url(content)
                markdown_content += f"## {filename}\n\n![{filename}]({url})\n\n"
    with open(output_file, "w") as file:
        file.write(markdown_content)

if __name__ == "__main__":
    generate_markdown("docs", "diagrams.md")