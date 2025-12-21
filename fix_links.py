import os, re

root = 'd:/webs/pdf-tools-website'

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    new = content
    # Replace nav/logo Home links to root
    new = re.sub(r'href="/home"', 'href="/"', new)
    # Optional: ensure about/contact/privacy have leading slash
    new = re.sub(r'href="about"', 'href="/about"', new)
    new = re.sub(r'href="contact"', 'href="/contact"', new)
    new = re.sub(r'href="privacy"', 'href="/privacy"', new)
    if new != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new)
        return True
    return False

changed = 0
for name in os.listdir(root):
    if name.endswith('.html'):
        path = os.path.join(root, name)
        if fix_file(path):
            print(f'Updated: {name}')
            changed += 1

print(f'Done. Files changed: {changed}')
