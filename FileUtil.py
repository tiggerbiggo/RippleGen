import os
from datetime import datetime

def generate_filename(base_filename, extension):
    # Remove leading and trailing whitespaces
    base_filename = base_filename.strip()
    extension = extension.strip()

    # If base_filename contains any period, replace it with underscore
    base_filename = base_filename.replace('.', '_')

    # Construct the full filename
    filename = f"{base_filename}.{extension}"

    # add a unique timestamp to avoid overwrite
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{base_filename}_{timestamp}.{extension}"

    return filename
