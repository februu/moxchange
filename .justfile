bin := if os() == "windows" { "build/moxchange.exe" } else { "build/moxchange" }

default:
    @just --list

lint:
    go mod tidy
    go fmt ./...
    go vet ./...
    staticcheck ./...

lint-full: lint
    nilaway ./...

build: lint
    go build -o {{ bin }}

clean:
    rm -rf build/

run: build
    {{ bin }}

test:
    go test -race ./...

cover:
    go test -race -coverprofile=coverage.out ./...
    go tool cover -func=coverage.out
    go tool cover -html=coverage.out -o coverage.html

ci: lint test cover
