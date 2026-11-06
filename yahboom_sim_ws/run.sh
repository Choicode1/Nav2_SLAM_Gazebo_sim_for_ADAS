#!/usr/bin/env bash
set -euo pipefail
MODULE_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNTIME_ROOT="${AUTONOMY_STUDIO_RUNTIME_ROOT:-$HOME/autonomy-studio/runtime/nav2}"
FOLDER_NAME="$(basename "$MODULE_PATH")"
IMAGE="${NAV2_DOCKER_IMAGE:-future-nav2:humble-yahboom}"
ROS_PARAM=''
CONTAINER_NAME="${FOLDER_NAME#\[}"
CONTAINER_NAME="${CONTAINER_NAME/\]/-}"
CONTAINER_NAME="${CONTAINER_NAME%_ws}"
read -r -a DEFAULT_ARGS <<< "$ROS_PARAM"
exec bash "$RUNTIME_ROOT/docker/docker_run_nav2.sh" "$CONTAINER_NAME" "$(dirname "$MODULE_PATH")" "$FOLDER_NAME" "$IMAGE" "${ROS_DOMAIN_ID:-20}" "${GPU_ENABLED:-false}" "${DEFAULT_ARGS[@]}" "$@"
