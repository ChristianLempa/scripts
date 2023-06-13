#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Check Repos 2
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon 🤖

# Documentation:
# @raycast.author ChristianLempa
# @raycast.authorURL https://raycast.com/ChristianLempa

op run --env-file="/Users/xcad/.env" -- python3 /Users/xcad/Projects/christianlempa/scripts/repos check --list-orphaned

