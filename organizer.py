#!/usr/bin/env python3
"""
PY-AUTOMATION TOOLS - Smart Workspace Organizer
Architecture: OOP, Pathlib Integration, Safe I/O Operations & Logging
"""

import shutil
import logging
import sys
from pathlib import Path
from typing import Dict, List

# Target directory to clean (Defaults to user's Downloads folder)
TARGET_DIR = str(Path.home() / "Downloads")
LOG_FILE = "/tmp/py_automation.log"

class WorkspaceOrganizer:
    def __init__(self, target_directory: str) -> None:
        self.target = Path(target_directory)
        self.categories: Dict[str, List[str]] = {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
            "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".md", ".csv"],
            "Archives": [".zip", ".tar", ".gz", ".rar", ".7z"],
            "Executables": [".exe", ".sh", ".deb", ".AppImage", ".msi"],
            "Code": [".py", ".cpp", ".js", ".html", ".css", ".json"]
        }
        self._setup_logging()

    def _setup_logging(self) -> None:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(LOG_FILE),
                logging.StreamHandler(sys.stdout)
            ]
        )

    def _get_category(self, extension: str) -> str:
        for category, extensions in self.categories.items():
            if extension.lower() in extensions:
                return category
        return "Others"

    def run(self) -> None:
        if not self.target.exists() or not self.target.is_dir():
            logging.error(f"Target directory {self.target} is invalid.")
            return

        logging.info(f"Scanning target directory: {self.target}")
        moved_files = 0

        for file_path in self.target.iterdir():
            if file_path.is_dir() or file_path.name.startswith('.'):
                continue

            category = self._get_category(file_path.suffix)
            destination_dir = self.target / category

            if not destination_dir.exists():
                destination_dir.mkdir(parents=True)
                
            destination_path = destination_dir / file_path.name

            try:
                shutil.move(str(file_path), str(destination_path))
                logging.info(f"Moved: {file_path.name} -> {category}/")
                moved_files += 1
            except Exception as e:
                logging.error(f"Failed to move {file_path.name}: {e}")

        logging.info(f"Automation Complete. Total files organized: {moved_files}")

if __name__ == "__main__":
    organizer = WorkspaceOrganizer(target_directory=TARGET_DIR)
    organizer.run()
