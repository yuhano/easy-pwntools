# Ubuntu 24버전을 기반 이미지로 사용 (Ubuntu 24.04가 출시되었다고 가정)
FROM ubuntu:24.04

# 패키지 업데이트 및 필요한 패키지 설치: OpenJDK, Python3, pip, unzip
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    python3 \
    python3-pip \
    unzip \
    python3-requests \
 && rm -rf /var/lib/apt/lists/*

# JAVA_HOME 환경변수 설정 (설치된 OpenJDK의 경로에 따라 변경 필요)
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# 작업 디렉토리 설정
WORKDIR /app


# 소스 전체 복사
COPY . .

CMD ["bash"]