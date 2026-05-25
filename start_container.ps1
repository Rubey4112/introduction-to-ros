docker run --rm -it `
    -e PUID=$(wsl id -u) `
    -e PGID=$(wsl id -g) `
    -p 22002:22 -p 3000:3000 `
    -v "${PWD}/workspace:/config/workspace" `
    -e "DISPLAY=127.0.0.1:0" `
    -v /tmp/.X11-unix:/tmp/.X11-unix `
    env-ros2