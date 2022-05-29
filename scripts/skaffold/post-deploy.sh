#!/bin/bash

set -euo pipefail

warning() {
	printf "\r\033[2K  \033[0;31m $1 \033[0m \n"
}

warning "!!!: Keep this shell alive if you want image(s) to be rebuilt automatically."
