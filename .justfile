bin := if os() == "windows" { "build/moxchange.exe" } else { "build/moxchange" }
tag := `git describe --tags --abbrev=0 2>/dev/null || echo dev`
commit := `git rev-parse --short HEAD`

@default:
    just --list

@lint:
    go mod tidy
    go fmt ./...
    go vet ./...
    staticcheck ./...

@lint-full: lint
    nilaway ./...

@build: clean lint
    go build -ldflags "-X 'main.VERSION={{ tag }}-{{ commit }}'" -o {{ bin }}

@clean:
    go clean
    rm -rf build/

@run: build
    {{ bin }}

@test:
    go test -race ./...

@test-verbose:
    go test -race -v ./...

@cover:
    go test -race -coverprofile=coverage.out ./...
    go tool cover -func=coverage.out
    go tool cover -html=coverage.out -o coverage.html

@ci: lint test cover

[working-directory('docs')]
@docs-serve:
    uv run zensical serve

[working-directory('docs')]
@docs-build:
    uv run zensical build
