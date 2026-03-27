package repl

import "fmt"

func PrintBanner(version string, port int) {
	const cyan = "\033[36m"
	const green = "\033[32m"
	const reset = "\033[0m"
	fmt.Print(cyan + "                      __                        \n  __ _  ___ __ ______/ /  ___ ____  ___ ____    \n /  ' \\/ _ \\\\ \" / __/ _ \\/ _ `/ _ \\/ _ `/ -_)   \n/_/_/_/\\___/_\\_\\\\__/_//_/\\_,_/_//_/\\_, /\\__/    \n                                  /___/         \n" + reset)
	fmt.Printf("Version: %s%s%s | Created by %sfebruu%s\n", cyan, version, reset, cyan, reset)
	fmt.Printf("Repository: %shttps://github.com/februu/moxchange%s\n", cyan, reset)
	fmt.Printf("Docs: %shttps://febru.dev/moxchange%s\n\n", cyan, reset)
	fmt.Printf("⚡ Connect your client here: %s127.0.0.1:%d/ws%s\n\n", green, port, reset)
}
