import os

folders = ["react", "typeScript", "nextjs"]
folder_labels = {
    "react": "React",
    "typeScript": "TypeScript",
    "nextjs": "Next.js"
}

lines = ["# TIL\n", "> Today I Learned\n\n"]

for folder in folders:
    if not os.path.exists(folder):
        continue
    files = [f for f in os.listdir(folder) if f.endswith(".md")]
    if not files:
        continue
    files.sort()
    lines.append(f"## {folder_labels[folder]}\n\n")
    for file in files:
        name = file.replace(".md", "")
        lines.append(f"- [{name}]({folder}/{file})\n")
    lines.append("\n")

with open("README.md", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("README.md updated!")