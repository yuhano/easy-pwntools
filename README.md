# easy-pwntools

## 개발 환경 구축

* Docker 이미지 빌드
```
docker build -t my-dev-env .
```

* 컨테이너 실행 (대화형 모드 및 볼륨 마운트)
```
docker run -it --rm -v "$(pwd)":/app my-dev-env bash
```
```
docker run -it --rm -v ${PWD}:/app my-dev-env bash
```

* 실행 중인 컨테이너 확인
```
docker ps
```

* 실행 중인 컨테이너에 접속
```
docker exec -it <컨테이너_ID_또는_이름> bash
```

