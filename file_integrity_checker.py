import os
import hashlib
import json

HASH_FILE = "file_hashes.json"

def calculate_hash(file_path):
    """Calculate SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        return f"Error: {e}"

def scan_directory(directory):
    """Scan directory and return a dictionary of file paths and their hashes."""
    file_hashes = {}
    for root, dirs, files in os.walk(directory):
        for name in files:
            file_path = os.path.join(root, name)
            file_hashes[file_path] = calculate_hash(file_path)
    return file_hashes

def save_hashes(hashes, filename=HASH_FILE):
    """Save file hashes to a JSON file."""
    with open(filename, "w") as f:
        json.dump(hashes, f, indent=4)

def load_hashes(filename=HASH_FILE):
    """Load file hashes from a JSON file."""
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as f:
        return json.load(f)

def check_integrity(directory):
    """Check file integrity by comparing current and saved hashes."""
    old_hashes = load_hashes()
    current_hashes = scan_directory(directory)
    modified = []
    added = []
    deleted = []

    for path, hash_val in current_hashes.items():
        if path not in old_hashes:
            added.append(path)
        elif old_hashes[path] != hash_val:
            modified.append(path)

    for path in old_hashes:
        if path not in current_hashes:
            deleted.append(path)

    return modified, added, deleted

def main():
    print("1. Scan and Save Hashes")
    print("2. Check File Integrity")
    choice = input("Choose an option (1/2): ")

    directory = input("Enter the directory path to monitor: ")

    if choice == '1':
        hashes = scan_directory(directory)
        save_hashes(hashes)
        print(f"Hashes saved for files in '{directory}'.")
    elif choice == '2':
        modified, added, deleted = check_integrity(directory)
        print("\n=== File Integrity Report ===")
        if modified:
            print("Modified Files:")
            for file in modified:
                print(f"  - {file}")
        if added:
            print("New Files:")
            for file in added:
                print(f"  - {file}")
        if deleted:
            print("Deleted Files:")
            for file in deleted:
                print(f"  - {file}")
        if not (modified or added or deleted):
            print("All files are intact.")
    else:
        print("Invalid option.")

if __name__ == "__main__":
    main()
