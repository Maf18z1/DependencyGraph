import sys
import subprocess
import os

def get_commit_dependencies(repo_path, tag_name=None):
    # Get commits starting from the specified tag
    if tag_name:
        start_commit = subprocess.check_output(["git", "-C", repo_path, "rev-list", "-n", "1", tag_name]).strip().decode()
    else:
        start_commit = "HEAD"
    
    # Prepare to track processed commits
    commit_dependencies = []
    processed_commits = set()  # To avoid duplicates
    to_process = [start_commit]  # Stack of commits to process

    while to_process:
        current_commit = to_process.pop(0)
        if current_commit in processed_commits:
            continue  # Skip already processed commits

        processed_commits.add(current_commit)
        
        # Get parents and commit message
        log_line = subprocess.check_output(
            ["git", "-C", repo_path, "log", "--pretty=format:%H %P", "-n", "1", current_commit]
        ).decode().strip()

        print(f"Log line for commit {current_commit}: {log_line}")  # Debugging line

        # Split the log_line into commit hash and parents, handling both cases
        parts = log_line.split()
        
        if len(parts) == 1:
            # This means there is no parent, it's just the commit hash
            commit_hash = parts[0]
            parents = []
        else:
            # Otherwise, the first part is the commit hash and the rest are parent commits
            commit_hash = parts[0]
            parents = parts[1:]

        # Get commit message
        commit_message = subprocess.check_output(
            ["git", "-C", repo_path, "log", "-1", "--pretty=%B", commit_hash]
        ).strip().decode()

        print(f"Commit hash: {commit_hash}, Parents: {parents}, Message: {commit_message}")  # Debug
        
        # Add the current commit and its details to the list
        commit_dependencies.append((commit_hash, commit_message, parents))
        
        # Add unprocessed parents to the stack
        to_process.extend(parents)
    
    return commit_dependencies

def create_plantuml_graph(dependencies, output_file, plantuml_path):
    uml_content = "@startuml\n"
    uml_content += "left to right direction\n"
    
    for commit_hash, commit_message, parents in dependencies:
        if parents:
            for parent in parents:
                uml_content += f"\"{parent}\" --> \"{commit_hash}: {commit_message}\"\n"
        else:
            uml_content += f"\"{commit_hash}: {commit_message}\"\n"
    
    uml_content += "@enduml\n"

    with open("temp_graph.txt", "w", encoding="utf-8") as f:
        f.write(uml_content)
        
    subprocess.run(
        ["java", "-jar", plantuml_path, "temp_graph.txt", "-tpng", "-o", os.path.dirname(output_file)],
        check=True
    )
    os.rename("temp_graph.png", output_file)
    os.remove("temp_graph.txt")
    print("Graph successfully saved to", output_file)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python dependency_visualizer.py <path_to_plantuml.jar> <path_to_repository> <output_png> [<tag_name>]")
        sys.exit(1)
    
    plantuml_path = sys.argv[1]
    repo_path = sys.argv[2]
    output_path = sys.argv[3]
    tag_name = sys.argv[4] if len(sys.argv) > 4 else None

    dependencies = get_commit_dependencies(repo_path, tag_name)
    create_plantuml_graph(dependencies, output_path, plantuml_path)