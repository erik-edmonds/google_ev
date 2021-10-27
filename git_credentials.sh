git config credential.helper '!f() { sleep 1; echo "username=${GIT_USERNAME}"; echo "password=${GIT_TOKEN}"; }; f'
