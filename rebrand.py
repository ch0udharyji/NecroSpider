import os

replacements = {
    "NecroSpider": "NecroSpider",
    "Necrospider": "Necrospider",
    "necrospider": "necrospider",
    "NECROSPIDER": "NECROSPIDER"
}

def replace_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        return # Skip binary files

    new_content = content
    for old, new in replacements.items():
        new_content = new_content.replace(old, new)
        
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

for root, dirs, files in os.walk('.', topdown=False):
    if '.git' in root or '.venv' in root or 'node_modules' in root:
        continue

    for name in files:
        filepath = os.path.join(root, name)
        replace_in_file(filepath)
        
        # Rename file
        new_name = name
        for old, new in replacements.items():
            new_name = new_name.replace(old, new)
        if new_name != name:
            os.rename(filepath, os.path.join(root, new_name))

    for name in dirs:
        # Rename dir
        if '.git' == name or '.venv' == name or 'node_modules' == name:
            continue
        new_name = name
        for old, new in replacements.items():
            new_name = new_name.replace(old, new)
        if new_name != name:
            os.rename(os.path.join(root, name), os.path.join(root, new_name))

print("Rebranding complete.")
