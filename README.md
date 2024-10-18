# A simple Litestar app to test out the basic framework functionality
![Docker build workflow](https://github.com/balancy/litestar_app/actions/workflows/docker-publish.yml/badge.svg)

## 🛠 Technologies Used
- **App**: Litestar — a flexible backend framework for fast asynchronous APIs.
- **Package Manager**: UV — lightweight package manager for dependencies.
- **Docker**: Easily deployable with Docker.
- **Database**: Postgresql with async access.

## 🚀 Getting Started

### Prerequisites
- Docker installed on your machine.

### Run on local machine
1. **Clone the repository**

```sh
git clone https://github.com/balancy/litestar_app.git
```

2. **Navigate to the project directory**

```sh
cd litestar_app
```

3. **Build and run the Docker containers**

```sh
make
```

4. **Visit the app API swagger schema**

Open http://localhost:8000/schema/swagger in your browser

5. **Run tests**

```sh
make test
```

### Run on server

1. **Clone the repository**

```sh
git clone https://github.com/balancy/litestar_app.git
```

2. **Navigate to the project directory**

```sh
cd litestar_app
```

3. **Run Docker containers**

```sh
make prod
```