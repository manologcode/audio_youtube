# NOTAS DESARROLLO

Correr la aplicacion

    ./runDockerDev.sh

dentro del contenedor correr

    python app

para actualizar paquetes

    pip3 install  --no-cache-dir -r requirements.txt

para ver la aplicación en el navegador

    http://localhost:5000/

Creara manualmente el contenedor

    docker build --no-cache . -t manologcode/yt_dlp     
