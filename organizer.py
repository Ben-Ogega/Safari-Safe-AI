from pathlib import Path
import shutil

# Folder to Organize
FOLDER_TO_ORGANIZE = Path.home()/"Desktop"

FILE_CATEGORIES = {

    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".heic", ".ico", ".tif", ".bmp", ".raw"],
    "Documents": [".pdf", ".doc", ".docx", ".docm", ".dot", ".dotx", ".odt", ".rft", ".txt", ".md", ".pages"],
    "Spreadsheets": [".xls", ".xlsx", ".xlsm", ".xlsb", ".xltx", ".xltm", ".odp", ".numbers", ".csv", ".tsv"],
    "Presentations": [".ppt", ".pptx", ".pptm", ".potx", ".potm", ".pps", ".ppsx", ".odp", ".key"],
    "Videos": [".mp4" ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm", ".m4v", ".3gp", ".mpeg"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".m4a", ".ogg", ".wma", ".opus", ".aiff"],
    "Archives": [".zip", ".tar", ".gz", ".rar", ".7z", ".bz2", ".xz", ".iso", ".dmg", ".aiff"],
    "Code": [".py", ".js", ".ts", ".html", ".css", ".json", ".sh", ".rb", ".java", ".cpp", ".c", ".go", ".rs", ".php", ".sql", ".yaml", ".xml", ".ipynb"],
    "Fonts": [".ttf", ".otf", ".woff", ".woff2", ".eot"],
    "Executables": [".exe", ".msi", ".app", ".deb", ".apk"], 
    "Other": []
}

def get_category(file: Path):
    """Return the category name for a given file based on its extension"""
    ext = file.suffix.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
        return "Other"

def organize_folder(folder: Path):
    """Scan a folder and move files into category subfolders."""
    if not folder.exists():
        print(f"Folder not found: {folder}")
        return
    file_moved = 0

    for item in folder.iterdir():
        # Skip folders, only process files
        if not item.is_file():
            continue

        category = get_category(item)
        # Create the subfolder if it doesnt exist
        destination_folder = folder / category
        destination_folder.mkdir(exist_ok=True)

        # Move the file
        destination = destination_folder/item.name
        shutil.move(str(item), str(destination))
        print(f"Moved: {item.name} ---> {category}/" )
        file_moved += 1

    print(f"\nDone! {file_moved} files organized.")

organize_folder(Path(r"C:\Users\User\Desktop\Other"))
