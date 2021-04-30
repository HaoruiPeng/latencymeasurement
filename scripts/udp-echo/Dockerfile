FROM python:3.9-slim

COPY udp-server.py  ./

EXPOSE 80/udp
EXPOSE 80
EXPOSE 12345/udp
EXPOSE 12345

CMD [ "python3", "-u", "udp-server.py" ]
