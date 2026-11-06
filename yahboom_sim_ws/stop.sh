#!/usr/bin/env bash
set -euo pipefail
MODULE_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNTIME_ROOT="${AUTONOMY_STUDIO_RUNTIME_ROOT:-$HOME/autonomy-studio/runtime/nav2}"
FOLDER_NAME="$(basename "$MODULE_PATH")"
IMAGE="${NAV2_DOCKER_IMAGE:-future-nav2:humble-yahboom}"
CONTAINER_NAME="${FOLDER_NAME#\[}"
CONTAINER_NAME="${CONTAINER_NAME/\]/-}"
CONTAINER_NAME="${CONTAINER_NAME%_ws}"
docker stop -t 10 "$CONTAINER_NAME"
