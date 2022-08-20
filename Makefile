dvwa:
	docker run -it -d --name dvwa -p 80:80 vulnerables/web-dvwa

goat:
	docker run -d --name goat -p 8080:8080 -p 9090:9090 -p 8000:8888 -e TZ=Europe/Madrid webgoat/goatandwolf:latest

simple:
	docker run -d --name simple -p 1234:8000 -it appsecco/dsvw

stop:
	-docker stop $$(docker ps -q)

prune:
	docker container prune

fclean: stop
	docker rmi $$(docker image ls -q)
