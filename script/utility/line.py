import os

directory = r"C:\Users\psalv\OneDrive\Documenti\Progetto Allarme\Software"
directory_depth = 100  # How deep you would like to go
extensions_to_consider = [".py", ".qss"]  # Change to ["all"] to include all extensions
exclude_filenames = ["venv", ".idea", "__pycache__", "cache", ".csv"]
skip_file_error_list = True

output_file = "line.txt"

with open(output_file, "w") as out_file:
    out_file.write(f"Path to ignore: {directory}\n")
    out_file.write("-------------------------------------------------\n")

    def _walk(path, depth):
        """Recursively list files and directories up to a certain depth"""
        depth -= 1
        with os.scandir(path) as p:
            for entry in p:
                skip_entry = False
                for fName in exclude_filenames:
                    if entry.path.endswith(fName):
                        skip_entry = True
                        break

                if skip_entry:
                    out_file.write(f"Skipping entry {entry.path}\n")
                    continue

                yield entry.path
                if entry.is_dir() and depth > 0:
                    yield from _walk(entry.path, depth)

    out_file.write("Caching entries\n")
    files = list(_walk(directory, directory_depth))
    out_file.write("\n\n |==================================================================================================|\n")

    out_file.write(f" |{'Counting Lines':>45} \t  {' ':>46}|\n")
    file_err_list = []
    line_count = 0
    len_files = len(files)
    for i, file_dir in enumerate(files):

        if not os.path.isfile(file_dir):
            continue

        skip_File = True
        for ending in extensions_to_consider:
            if file_dir.endswith(ending) or ending == "all":
                skip_File = False

        if not skip_File:
            try:
                with open(file_dir, "r", encoding="utf-8") as file:
                    local_count = 0
                    for line in file:
                        if line.strip():  # Consider non-empty lines only
                            local_count += 1
                    relative_path = os.path.relpath(file_dir, directory)
                    out_file.write(f" |{relative_path:<80} |\t {local_count:>10} |\n")
                    line_count += local_count
            except Exception as e:
                out_file.write(f"Errore durante la lettura del file {file_dir}: {e}\n")
                file_err_list.append(file_dir)
                continue

    out_file.write(" |==================================================================================================| \n")
    out_file.write(f" |{'Total lines':<80} |\t {line_count:>10} |\n")

print(f"Output written to {output_file}")
