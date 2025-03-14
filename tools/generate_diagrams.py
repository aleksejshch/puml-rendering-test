import os
import zlib
import base64

# PlantUML-specific base64 encoding
PLANTUML_BASE64 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"

def encode_plantuml_deflate(content):
    if not content.strip().startswith("@startuml"):
        content = "@startuml\n" + content
    if not content.strip().endswith("@enduml"):
        content = content + "\n@enduml"

    print(f"Original content:\n{content}\n")

    # Pack by zlib (algo DEFLATE)
    compressed = zlib.compress(content.encode("utf-8"))
    print(f"Compressed data (hex): {compressed.hex()}\n")  # Логируем сжатые данные

    # # Coding into PlantUML-specific base64
    # encoded = ""
    # buffer = 0
    # bits = 0
    # for byte in compressed:
    #     buffer = (buffer << 8) | byte
    #     bits += 8
    #     while bits >= 6:
    #         bits -= 6
    #         index = (buffer >> bits) & 0x3F
    #         encoded += PLANTUML_BASE64[index]
    # if bits > 0:
    #     index = (buffer << (6 - bits)) & 0x3F
    #     encoded += PLANTUML_BASE64[index]

    encoded = base64.b64encode(compressed).decode("utf-8")
    encoded = encoded.translate(str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/", PLANTUML_BASE64))

    # print(f"PlantUML encoded: {encoded}\n")

    return encoded

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
    # encoded = encode_plantuml_hex(content)
    encoded = encode_plantuml_deflate(content)
    url = f"https://www.plantuml.com/plantuml/png/{encoded}"
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