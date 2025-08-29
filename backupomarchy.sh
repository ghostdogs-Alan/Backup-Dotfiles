#!/bin/bash

# Backup Omarchy DotFiles

# Needs a directory in the home directory call BackupFiles (case sensitive)
# Remember to do a chmod +x backupomarch.sh
# Run using ./backupomarchy.sh
# Creates a temporary directory called dotfiles and deletes it when finished.

# Move to home directory of user
cd ~
echo "Backing up Omarchy DotFiles"
# Make temp dotfiles directory and confirm
mkdir dotfiles
if [ $? -ne 0 ]; then
  echo "Failed: Could not make temp directory dotfiles"
  exit 1
fi
echo "Made temp directory"

# Copy dotfiles to temp directory
cp -r ~/.config/hypr ~/dotfiles 1>/dev/null
cp -r ~/.config/waybar ~/dotfiles 1>/dev/null
echo "Copied dotfiles to temp"

# Make compressed tarball
echo "Making tarball please wait...." 
tar cfJ dotfiles.tar.xz ./dotfiles --remove-files
if [ $? -ne 0 ]; then
  echo "Failed: Could not create tarball of dotfiles"
  exit 1
fi
echo "Made tarball of dotfiles"

# Set variables sfile is starting file ofile is output
now=$(date +"%d_%m_%Y-%H:%M")
sfile="dotfiles.tar.xz"
ofile="BackupFiles/dotfiles"
cp -v $sfile $ofile-$now.tar.xz
if [ $? -ne 0 ]; then
  echo "Failed: Could not copy tarball to backup directory"
  exit 1
fi
echo "Moved tarball to backup directory"
rm dotfiles.tar.xz
if [ $? -ne 0 ]; then
  echo "Failed: Could not remove temp tarball"
  exit 1
fi
echo "Cleaned up"
echo "DOTFILES Backup Complete"


