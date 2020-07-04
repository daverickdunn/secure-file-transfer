docker-compose build
export TRANSFER_SECRET_KEY=$(openssl rand -base64 24) TRANSFER_IV456=$(openssl rand -base64 12) FILENAMES="$@";
docker-compose up