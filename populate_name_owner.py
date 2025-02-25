import re
import pymysql

# Database connection (adjust connection parameters as needed)
connection = pymysql.connect(
    host='localhost',
    user='admin',
    password='admin',
    database='qmodel',
    port=3307,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

def extract_project_info_from_url(commit_url):
    # Regular expression pattern to extract project owner and project name from the URL
    pattern = r"https:\/\/api\.github\.com\/repos\/([^\/]+)\/([^\/]+)"
    match = re.search(pattern, commit_url)

    if match:
        project_owner = match.group(1)  # First capturing group is the owner
        project_name = match.group(2)  # Second capturing group is the repository name
        return project_name, project_owner
    else:
        return None, None

def update_commit_info():
    try:
        with connection.cursor() as cursor:
            # Fetch commits and raw_data where project_name and project_owner are NULL or empty
            cursor.execute(
                "SELECT sha, raw_data FROM qmodel.commit WHERE project_name IS NULL OR project_name = '' OR project_owner IS NULL OR project_owner = ''")
            commits = cursor.fetchall()

            for commit in commits:
                sha = commit['sha']
                raw_data = commit['raw_data']

                # Extract project name and project owner from the URL in raw_data
                project_name, project_owner = extract_project_info_from_url(raw_data)

                if project_name and project_owner:
                    # Forcefully update the commit record with project name and owner
                    update_query = """
                    UPDATE qmodel.commit
                    SET project_name = IFNULL(NULLIF(project_name, ''), %s),
                        project_owner = IFNULL(NULLIF(project_owner, ''), %s)
                    WHERE sha = %s AND (project_name IS NULL OR project_name = '' OR project_owner IS NULL OR project_owner = '');
                    """
                    cursor.execute(update_query, (project_name, project_owner, sha))
                    connection.commit()

                    print(f"Updated commit {sha} with project_name={project_name}, project_owner={project_owner}")

    finally:
        connection.close()

# Run the update function
update_commit_info()
