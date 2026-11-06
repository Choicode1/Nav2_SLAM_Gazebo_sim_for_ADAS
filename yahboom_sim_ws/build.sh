#!/usr/bin/env bash
set -euo pipefail
MODULE_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNTIME_ROOT="${AUTONOMY_STUDIO_RUNTIME_ROOT:-$HOME/autonomy-studio/runtime/nav2}"
FOLDER_NAME="$(basename "$MODULE_PATH")"
IMAGE="${NAV2_DOCKER_IMAGE:-future-nav2:humble-yahboom}"
exec bash "$RUNTIME_ROOT/docker/docker_build_nav2.sh" "$(dirname "$MODULE_PATH")" "$FOLDER_NAME" "$IMAGE" "${ROS_DOMAIN_ID:-20}"
