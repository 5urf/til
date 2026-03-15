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
        encoded = file.replace(" ", "%20")
        lines.append(f"- [{name}]({folder}/{encoded})\n")
    lines.append("\n")

lines.append("## 📚 Books\n\n")
lines.append("### Clean Code\n\n")

clean_code_path = "books/clean-code"

chapters = sorted([f for f in os.listdir(clean_code_path) if f.endswith(".md")])
for file in chapters:
    name = file.replace(".md", "")
    encoded = file.replace(" ", "%20")
    lines.append(f"- [{name}](books/clean-code/{encoded})\n")

lines.append("\n**Missions**\n\n")
missions_path = os.path.join(clean_code_path, "missions")
missions = sorted([f for f in os.listdir(missions_path) if f.endswith(".md")])
for file in missions:
    name = file.replace(".md", "")
    encoded = file.replace(" ", "%20")
    lines.append(f"- [{name}](books/clean-code/missions/{encoded})\n")

lines.append("\n")

with open("README.md", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("README.md updated!")