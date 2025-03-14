import os

def encode_plantuml_hex(content):
    if not content.strip().startswith("@startuml"):
        content = "@startuml\n" + content
    if not content.strip().endswith("@enduml"):
        content = content + "\n@enduml"

    # code every symbol into hex
    hex_encoded = content.encode("utf-8").hex()

    # Add prefix ~h (it means HEX encoding)
    hex_encoded = "~h" + hex_encoded

    return hex_encoded

def generate_plantuml_url(content):
    hex_encoded = encode_plantuml_hex(content)
    url = f"https://www.plantuml.com/plantuml/png/{hex_encoded}"
    print(f"Generated URL: {url}\n")
    return url

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
    generate_markdown("docs", "docs/diagrams.md")