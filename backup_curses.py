import curses
import os
import shutil
import tarfile
from datetime import datetime


def backup_dotfiles(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()

    def log(msg, line):
        stdscr.addstr(line, 2, msg)
        stdscr.refresh()

    line = 1
    log("Omarchy DotFiles Backup (curses TUI)", line)
    line += 2

    home = os.path.expanduser("~")
    backup_dir = os.path.join(home, "BackupFiles")
    temp_dir = os.path.join(home, "dotfiles")
    now = datetime.now().strftime("%d_%m_%Y-%H:%M")
    archive_name = f"dotfiles-{now}.tar.xz"
    archive_path = os.path.join(backup_dir, archive_name)

    try:
        # Create temp dir
        log("Creating temporary directory...", line)
        os.makedirs(temp_dir, exist_ok=True)
        line += 1

        # Copy configs
        log("Copying ~/.config/hypr...", line)
        shutil.copytree(os.path.join(home, ".config", "hypr"), os.path.join(temp_dir, "hypr"), dirs_exist_ok=True)
        line += 1

        log("Copying ~/.config/waybar...", line)
        shutil.copytree(os.path.join(home, ".config", "waybar"), os.path.join(temp_dir, "waybar"), dirs_exist_ok=True)
        line += 1

        # Compress
        log("Creating compressed tarball...", line)
        with tarfile.open("dotfiles.tar.xz", "w:xz") as tar:
            tar.add(temp_dir, arcname="dotfiles")
        line += 1

        # Cleanup temp dir
        log("Removing temporary directory...", line)
        shutil.rmtree(temp_dir)
        line += 1

        # Copy archive to backup dir
        os.makedirs(backup_dir, exist_ok=True)
        log(f"Saving backup to {archive_path}", line)
        shutil.move("dotfiles.tar.xz", archive_path)
        line += 1

        log("Backup complete ✅", line)
        line += 2
    except Exception as e:
        log(f"❌ Error: {e}", line)
        line += 2

    log("Press any key to exit...", line)
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(backup_dotfiles)
