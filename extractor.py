#!/usr/bin/env python3
"""
PY-AUTOMATION TOOLS - Enterprise Media Extractor
Architecture: OOP, Pathlib Integration, Strategy Pattern & Native Logging
"""

import yt_dlp
import logging
import sys
from pathlib import Path
from typing import Dict, Any

VAULT_DIR = str(Path.home() / "Downloads" / "MediaVault")
LOG_FILE = "/tmp/media_extractor.log"

class MediaExtractor:
    def __init__(self, target_directory: str) -> None:
        self.vault = Path(target_directory)
        self._setup_logging()
        self._ensure_vault()

    def _setup_logging(self) -> None:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(LOG_FILE),
                logging.StreamHandler(sys.stdout)
            ]
        )

    def _ensure_vault(self) -> None:
        if not self.vault.exists():
            self.vault.mkdir(parents=True)
            logging.info(f"Created secure Media Vault at: {self.vault}")

    def extract(self, url: str, audio_only: bool = False) -> None:
        logging.info(f"Initiating extraction sequence for target: {url}")
        
        ydl_opts: Dict[str, Any] = {
            'outtmpl': str(self.vault / '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': True,
        }

        if audio_only:
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        else:
            ydl_opts.update({
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
            })

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            logging.info("✅ Extraction Complete. Media secured in Vault.")
        except Exception as e:
            logging.error(f"❌ Extraction failed: {e}")

if __name__ == "__main__":
    print("\n--- 🦅 DAVOS ENTERPRISE EXTRACTOR ---")
    print("1. Video Extraction (MP4)")
    print("2. Audio Extraction (MP3)")
    
    try:
        choice = input("\n[SYSTEM] Select extraction mode (1/2): ").strip()
        
        if choice in ["1", "2"]:
            target_url = input("[SYSTEM] Enter target URL: ").strip()
            extractor = MediaExtractor(target_directory=VAULT_DIR)
            
            if choice == "1":
                extractor.extract(target_url, audio_only=False)
            else:
                extractor.extract(target_url, audio_only=True)
        else:
            print("⚠️ [ERROR] Invalid selection. Aborting sequence.")
            
    except KeyboardInterrupt:
        print("\n🛑 [SYSTEM] Extraction sequence terminated by user.")
