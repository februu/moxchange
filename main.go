package main

import (
	"fmt"
	"log"

	"github.com/februu/moxchange/internal/datasource"
	"github.com/februu/moxchange/internal/exchange"
)

const VERSION = "x.x.x"

func main() {
	printBanner()
	ds, error := datasource.NewCSVDataSource("./test.csv", true)
	if error != nil {
		log.Println(error)
		return
	}

	for {
		row, err := ds.Next()
		if err != nil {
			log.Println(err)
			return
		}
		kline, err := exchange.NewKlineFromCSV(row)
		if err != nil {
			log.Println(err)
			return
		}
		fmt.Println(kline)

	}
}

func printBanner() {
	const cyan = "\033[36m"
	const green = "\033[32m"
	const reset = "\033[0m"
	fmt.Print(cyan + "                      __                        \n  __ _  ___ __ ______/ /  ___ ____  ___ ____    \n /  ' \\/ _ \\\\ \" / __/ _ \\/ _ `/ _ \\/ _ `/ -_)   \n/_/_/_/\\___/_\\_\\\\__/_//_/\\_,_/_//_/\\_, /\\__/    \n                                  /___/         \n" + reset)
	fmt.Printf("Version: %s%s%s | Created by %sfebruu%s\n", cyan, VERSION, reset, cyan, reset)
	fmt.Printf("Repository: %shttps://github.com/februu/moxchange%s\n", cyan, reset)
	fmt.Printf("Docs: %shttps://febru.dev/moxchange%s\n\n", cyan, reset)
	fmt.Printf("⚡ Connect your client here: %s%s%s\n\n", green, "127.0.0.1:3777/ws", reset)
}
