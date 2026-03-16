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
books_path = "books"

for book in sorted(os.listdir(books_path)):
    book_path = os.path.join(books_path, book)
    if not os.path.isdir(book_path):
        continue

    label = book.replace("-", " ").title()
    lines.append(f"### {label}\n\n")

    files = sorted([f for f in os.listdir(book_path) if f.endswith(".md")])
    for file in files:
        name = file.replace(".md", "")
        encoded = file.replace(" ", "%20")
        lines.append(f"- [{name}](books/{book}/{encoded})\n")

    missions_path = os.path.join(book_path, "missions")
    if os.path.exists(missions_path):
        lines.append("\n**Missions**\n\n")
        missions = sorted([f for f in os.listdir(missions_path) if f.endswith(".md")])
        for file in missions:
            name = file.replace(".md", "")
            encoded = file.replace(" ", "%20")
            lines.append(f"- [{name}](books/{book}/missions/{encoded})\n")

    lines.append("\n")

with open("README.md", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("README.md updated!")