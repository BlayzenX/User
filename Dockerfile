# Faster & Secure & Special Container #
# Thanks to mkaraniya & zakaryan2004

FROM fusuf/Lostuserbot:latest
RUN git clone https://github.com/quiec/LostUserBot /root/LostUserBot
WORKDIR /root/LostUserBot/
RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]  
