#!/usr/bin/env bash
set -euo pipefail

site_dir="${1:-_site}"
if [[ ! -d "$site_dir" ]]; then
  echo "Build-Verzeichnis fehlt: $site_dir" >&2
  exit 1
fi

# Nur das Build-Ergebnis bearbeiten, niemals die Originalbilder.
# Orientation bleibt erhalten, damit Hochformatbilder korrekt angezeigt werden.
# -overwrite_original verhindert, dass unbereinigte Backup-Dateien deployt werden.
exiftool -r -overwrite_original \
  -ext jpg -ext jpeg -ext png -ext webp -ext gif \
  -all= -tagsFromFile @ -Orientation \
  "$site_dir"
