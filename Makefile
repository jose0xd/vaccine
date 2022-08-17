dvwa:
	docker run -it -d -p 80:80 --name dvwa vulnerables/web-dvwa

goat:
	docker run -d -p 8080:8080 -p 9090:9090 -p 8000:8888 -e TZ=Europe/Madrid webgoat/goatandwolf:latest

stop:
	-docker stop $$(docker ps -q)

fclean: stop
	docker rmi $$(docker image ls -q)
